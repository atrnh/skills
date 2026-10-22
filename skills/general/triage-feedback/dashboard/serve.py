#!/usr/bin/env python3
"""Serve a triage dashboard on localhost and record decisions to decisions.json.

Usage:
  serve.py start RUN_DIR [--port N]   start in the background, or report the running server
  serve.py stop RUN_DIR               stop it
  serve.py run RUN_DIR PORT           run in the foreground (start uses this)

On macOS, start hands the server to launchd, because agent harnesses stop
background processes after a short time. Elsewhere it detaches into its own
session. The server binds to loopback only, stops itself after 12 idle hours,
and stops if RUN_DIR is deleted.
"""

import argparse
import errno
import hashlib
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import threading
import time
import urllib.request
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

IDLE_SECONDS = 12 * 3600
MAX_BODY = 2_000_000


def label_for(run_dir):
    digest = hashlib.sha1(str(run_dir).encode()).hexdigest()[:8]
    safe = "".join(c if c.isalnum() or c in "-." else "-" for c in run_dir.name)
    return f"com.triage-feedback.{safe}.{digest}"


def responds(port):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/index.html", timeout=1) as r:
            return r.status == 200
    except OSError:
        return False


def free_port():
    while True:
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]
        try:
            with socket.socket(socket.AF_INET6) as s6:
                s6.bind(("::1", port))
        except OSError as e:
            if e.errno != errno.EADDRNOTAVAIL:  # no IPv6 loopback, so IPv4 alone is fine
                continue
        return port


def use_launchd():
    return sys.platform == "darwin" and shutil.which("launchctl")


def start(run_dir, port):
    info_path = run_dir / "server.json"
    if info_path.exists():
        info = json.loads(info_path.read_text())
        if responds(info["port"]):
            report(run_dir, info, "already running")
            return
        stop(run_dir, quiet=True)
    port = port or free_port()
    label = label_for(run_dir)
    log = run_dir / "server.log"
    cmd = [sys.executable, str(Path(__file__).resolve()), "run", str(run_dir), str(port), "--label", label]
    if use_launchd():
        subprocess.run(["launchctl", "remove", label], capture_output=True)
        subprocess.run(["launchctl", "submit", "-l", label, "-o", str(log), "-e", str(log), "--", *cmd], check=True)
        info = {"port": port, "label": label}
    else:
        with open(log, "a") as out:
            p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=out, stderr=out, start_new_session=True)
        info = {"port": port, "pid": p.pid}
    for _ in range(50):
        if responds(port):
            break
        time.sleep(0.1)
    else:
        sys.exit(f"The server didn't come up on port {port}. See {log}.")
    info_path.write_text(json.dumps(info))
    report(run_dir, info, "started")


def report(run_dir, info, what):
    print(f"Dashboard {what}: http://localhost:{info['port']}/")
    print(f"Stop it with: python3 {Path(__file__).resolve()} stop {run_dir}")


def stop(run_dir, quiet=False):
    info_path = run_dir / "server.json"
    info = json.loads(info_path.read_text()) if info_path.exists() else {"label": label_for(run_dir)}
    if info.get("label") and shutil.which("launchctl"):
        subprocess.run(["launchctl", "remove", info["label"]], capture_output=True)
    if info.get("pid"):
        try:
            os.kill(info["pid"], signal.SIGTERM)
        except ProcessLookupError:
            pass
    info_path.unlink(missing_ok=True)
    if not quiet:
        print("Dashboard server stopped.")


def write_atomic(path, text):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    tmp.replace(path)


class Handler(SimpleHTTPRequestHandler):
    last_request = time.monotonic()
    allowed_origins = set()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def handle_one_request(self):
        Handler.last_request = time.monotonic()
        super().handle_one_request()

    def do_POST(self):
        if self.path != "/decisions":
            return self.send_error(404)
        origin = self.headers.get("Origin")
        if origin and origin not in self.allowed_origins:
            return self.send_error(403, "Decisions can only be saved from the dashboard page")
        length = int(self.headers.get("Content-Length") or 0)
        if not 0 < length <= MAX_BODY:
            return self.send_error(413)
        try:
            body = json.loads(self.rfile.read(length))
            if not (isinstance(body, dict) and isinstance(body.get("key"), str)
                    and isinstance(body.get("decisions"), list)):
                raise ValueError
        except ValueError:
            return self.send_error(400, "Expected a decisions payload")
        run_dir = Path(self.directory)
        markdown = body.pop("markdown", "")
        write_atomic(run_dir / "decisions.json", json.dumps(body, indent=1))
        write_atomic(run_dir / "decisions.md", markdown if isinstance(markdown, str) else "")
        self.send_response(204)
        self.end_headers()


def shut_down(label):
    if label and shutil.which("launchctl"):
        subprocess.run(["launchctl", "remove", label], capture_output=True)
    os._exit(0)


def run(run_dir, port, label):
    if not run_dir.is_dir():
        shut_down(label)
    Handler.allowed_origins = {f"http://{h}:{port}" for h in ("localhost", "127.0.0.1", "[::1]")}
    handler = partial(Handler, directory=str(run_dir))
    servers = [ThreadingHTTPServer(("127.0.0.1", port), handler)]
    try:
        class V6(ThreadingHTTPServer):
            address_family = socket.AF_INET6
        servers.append(V6(("::1", port), handler))
    except OSError:
        pass
    for s in servers:
        threading.Thread(target=s.serve_forever, daemon=True).start()
    print(f"serving {run_dir} on port {port}", flush=True)
    while True:
        time.sleep(30)
        if not run_dir.is_dir():
            shut_down(label)
        if time.monotonic() - Handler.last_request > IDLE_SECONDS:
            (run_dir / "server.json").unlink(missing_ok=True)
            shut_down(label)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("start")
    p.add_argument("run_dir", type=Path)
    p.add_argument("--port", type=int)
    p = sub.add_parser("stop")
    p.add_argument("run_dir", type=Path)
    p = sub.add_parser("run")
    p.add_argument("run_dir", type=Path)
    p.add_argument("port", type=int)
    p.add_argument("--label")
    args = ap.parse_args()
    run_dir = args.run_dir.expanduser().resolve()
    if args.cmd == "start":
        if not (run_dir / "index.html").exists():
            sys.exit(f"No index.html in {run_dir}. Run build.py first.")
        start(run_dir, args.port)
    elif args.cmd == "stop":
        stop(run_dir)
    else:
        run(run_dir, args.port, args.label)


if __name__ == "__main__":
    main()
