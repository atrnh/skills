#!/usr/bin/env python3
"""Build a triage dashboard from a findings.json.

Usage: build.py RUN_DIR/findings.json [--check]

Writes index.html and resolved.json next to findings.json. Nothing is written
when a finding can't be resolved against the source files. --check also prints
every highlighted line and every line a fix replaces, for a final read-through.
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

TEMPLATE = Path(__file__).with_name("template.html")
DEFAULT_AROUND = 3
ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
GITHUB_PR_RE = re.compile(r"^https://github\.com/([^/]+/[^/]+)/pull/\d+")


class Invalid(Exception):
    pass


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)


def hunks(diff_text):
    for m in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", diff_text, re.M):
        start, count = int(m.group(1)), int(m.group(2) if m.group(2) is not None else 1)
        if count:
            yield start, start + count - 1


class Source:
    def __init__(self, spec, findings_path):
        self.spec = spec
        self.kind = spec.get("kind", "files")
        if self.kind not in ("pr", "changes", "files"):
            raise Invalid(f'source.kind must be "pr", "changes", or "files", not {self.kind!r}')
        root = Path(spec.get("root", ".")).expanduser()
        self.root = (root if root.is_absolute() else findings_path.parent / root).resolve()
        if not self.root.is_dir():
            raise Invalid(f"source.root {self.root} is not a directory")
        self.is_git = git(self.root, "rev-parse", "--is-inside-work-tree").returncode == 0
        self.head = git(self.root, "rev-parse", "HEAD").stdout.strip() if self.is_git else None
        self.base = spec.get("base")
        self.merge_base = None
        if self.base:
            if not self.is_git:
                raise Invalid(f"source.base is set but {self.root} is not a Git checkout")
            r = git(self.root, "merge-base", self.base, "HEAD")
            if r.returncode:
                raise Invalid(f"can't find a merge base for {self.base!r} and HEAD: {r.stderr.strip()}")
            self.merge_base = r.stdout.strip()
        self.link = spec.get("link")
        m = GITHUB_PR_RE.match(spec.get("url") or "")
        if not self.link and self.kind == "pr" and m:
            self.link = f"https://github.com/{m.group(1)}/blob/{{head}}/{{path}}?plain=1#L{{start}}-L{{end}}"
        if self.link and "{head}" in self.link and not self.head:
            raise Invalid("source.link uses {head}, but the source root isn't a Git checkout")
        self.change_label = spec.get("changeLabel") or ("this PR" if self.kind == "pr" else "these changes")
        self.files = {}

    def file(self, rel, where):
        if not isinstance(rel, str) or not rel:
            raise Invalid(f"{where}: file is required")
        if rel in self.files:
            return self.files[rel]
        path = (self.root / rel).resolve()
        if not path.is_file():
            raise Invalid(f"{where}: {rel} not found under {self.root}")
        text = path.read_text()
        info = {"text": text, "lines": text.splitlines(), "added": set(), "commentable": [],
                "dirty": False}
        if self.is_git:
            tracked = git(self.root, "ls-files", "--error-unmatch", "--", rel).returncode == 0
            info["dirty"] = not tracked or git(self.root, "diff", "--quiet", "HEAD", "--", rel).returncode != 0
            if self.merge_base:
                if tracked:
                    zero = git(self.root, "diff", "--unified=0", self.merge_base, "--", rel).stdout
                    info["added"] = {n for a, b in hunks(zero) for n in range(a, b + 1)}
                    three = git(self.root, "diff", "--unified=3", self.merge_base, "HEAD", "--", rel).stdout
                    info["commentable"] = list(hunks(three))
                else:
                    info["added"] = set(range(1, len(info["lines"]) + 1))
        self.files[rel] = info
        return info

    def url(self, rel, start, end):
        if not self.link:
            return None
        return self.link.format(head=self.head or "", path=rel, start=start, end=end)


def find(info, rel, quote, occurrence, where):
    if not isinstance(quote, str) or not quote.strip():
        raise Invalid(f"{where}: match must be a non-empty string")
    text, hits, i = info["text"], [], info["text"].find(quote)
    while i != -1:
        hits.append(i)
        i = text.find(quote, i + 1)
    lines_of = lambda idx: (text.count("\n", 0, idx) + 1,
                            text.count("\n", 0, idx + len(quote.rstrip("\n")) - 1) + 1)
    if not hits:
        raise Invalid(f"{where}: {quote!r} not found in {rel}")
    if occurrence is None and len(hits) > 1:
        at = ", ".join(str(lines_of(h)[0]) for h in hits)
        raise Invalid(f"{where}: {quote!r} matches {len(hits)} times in {rel} (lines {at}); "
                      f"quote more text or add \"occurrence\"")
    n = occurrence or 1
    if not 1 <= n <= len(hits):
        raise Invalid(f"{where}: occurrence {n} requested, but {quote!r} matches {len(hits)} time(s)")
    return lines_of(hits[n - 1])


def check_range(info, rel, start, end, where):
    if not (isinstance(start, int) and isinstance(end, int)):
        raise Invalid(f"{where}: start and end must be integers")
    if not 1 <= start <= end <= len(info["lines"]):
        raise Invalid(f"{where}: lines {start}–{end} are outside {rel} (1–{len(info['lines'])})")


def resolve_context(src, spec, where, warnings):
    rel = spec.get("file")
    info = src.file(rel, where)
    if "match" in spec:
        ms, me = find(info, rel, spec["match"], spec.get("occurrence"), where)
        around = spec.get("around", DEFAULT_AROUND)
        start = spec.get("start", max(1, ms - around))
        end = spec.get("end", min(len(info["lines"]), me + around))
        highlight = spec.get("highlight", list(range(ms, me + 1)))
    else:
        if "start" not in spec or "end" not in spec:
            raise Invalid(f"{where}: give either match or start and end")
        start, end, highlight = spec["start"], spec["end"], spec.get("highlight", [])
    check_range(info, rel, start, end, where)
    hl = set()
    for h in highlight:
        if isinstance(h, str):
            hits = [n for n in range(start, end + 1) if h in info["lines"][n - 1]]
            if len(hits) != 1:
                raise Invalid(f"{where}: highlight {h!r} matches {len(hits)} lines in {rel} {start}–{end}; "
                              f"it must match exactly one")
            hl.add(hits[0])
        elif isinstance(h, int) and start <= h <= end:
            hl.add(h)
        else:
            raise Invalid(f"{where}: highlight {h!r} is outside lines {start}–{end}")
    for n in sorted(hl):
        if not info["lines"][n - 1].strip():
            warnings.append(f"{where}: highlighted line {rel}:{n} is blank")
    span = (min(hl), max(hl)) if hl else (start, end)
    return {"file": rel, "start": start, "end": end, "label": spec.get("label"),
            "highlight": sorted(hl), "lines": info["lines"][start - 1:end],
            "added": [n for n in range(start, end + 1) if n in info["added"]],
            "commentable": any(a <= span[0] and span[1] <= b for a, b in info["commentable"]),
            "url": src.url(rel, start, end)}


def resolve_fix(src, spec, where):
    rel = spec.get("file")
    info = src.file(rel, where)
    if not isinstance(spec.get("replacement"), str):
        raise Invalid(f"{where}: replacement must be a string (use \"\" to delete the lines)")
    if "match" in spec:
        start, end = find(info, rel, spec["match"], spec.get("occurrence"), where)
    else:
        start, end = spec.get("start"), spec.get("end", spec.get("start"))
    check_range(info, rel, start, end, where)
    return {"file": rel, "start": start, "end": end, "label": spec.get("label"),
            "lines": info["lines"][start - 1:end], "replacement": spec["replacement"],
            "added": [n for n in range(start, end + 1) if n in info["added"]],
            "commentable": any(a <= start and end <= b for a, b in info["commentable"]),
            "url": src.url(rel, start, end)}


def origin(src, finding):
    if not src.merge_base:
        return None
    targets = {(x["file"], n) for x in finding["fixes"] for n in range(x["start"], x["end"] + 1)}
    if not targets and finding["context"]:
        c = finding["context"][0]
        targets = {(c["file"], n) for n in c["highlight"]}
    if not targets:
        return None
    new = sum(n in src.files[f]["added"] for f, n in targets)
    return "new" if new == len(targets) else "older" if new == 0 else "mixed"


def resolve(data, findings_path):
    if not isinstance(data.get("findings"), list) or not data["findings"]:
        raise Invalid("findings must be a non-empty list")
    src = Source(data.get("source") or {}, findings_path)
    errors, warnings, out, seen = [], [], [], set()
    for i, f in enumerate(data["findings"]):
        fid = f.get("id")
        where = fid or f"finding #{i + 1}"
        try:
            if not isinstance(fid, str) or not ID_RE.match(fid):
                raise Invalid(f"{where}: id must start with a letter and use only letters, digits, - or _")
            if fid in seen:
                raise Invalid(f"{where}: duplicate id")
            seen.add(fid)
            for key in ("title", "category", "problem"):
                if not isinstance(f.get(key), str) or not f[key].strip():
                    raise Invalid(f"{where}: {key} is required")
            if f.get("priority") not in (1, 2, 3):
                raise Invalid(f"{where}: priority must be 1, 2, or 3")
            if not f.get("counter"):
                warnings.append(f"{where}: no counter (the case against making this change)")
            context = [resolve_context(src, c, f"{where} context {j + 1}", warnings)
                       for j, c in enumerate(f.get("context", []))]
            fixes = [resolve_fix(src, x, f"{where} fix {j + 1}") for j, x in enumerate(f.get("fixes", []))]
            if not context:
                warnings.append(f"{where}: no context, so the card shows no source lines")
            if not fixes and not f.get("fixNote"):
                warnings.append(f"{where}: neither fixes nor fixNote, so the card proposes nothing")
            evidence = f.get("evidence", [])
            if not all(isinstance(e, dict) and e.get("text") for e in evidence):
                raise Invalid(f"{where}: each evidence item needs text (and usually url)")
            r = {"id": fid, "category": f["category"], "priority": f["priority"], "title": f["title"],
                 "problem": f["problem"], "counter": f.get("counter", ""), "fixNote": f.get("fixNote", ""),
                 "comment": f.get("comment", ""), "evidence": evidence, "context": context, "fixes": fixes}
            r["origin"] = origin(src, r)
            out.append(r)
        except Invalid as e:
            errors.append(str(e))

    ranges = sorted((x["file"], x["start"], x["end"], f["id"]) for f in out for x in f["fixes"])
    conflicts = {}
    for i, a in enumerate(ranges):
        for b in ranges[i + 1:]:
            if b[0] != a[0] or b[1] > a[2]:
                continue
            where = f"{a[0]} lines {b[1]}–{min(a[2], b[2])}"
            if a[3] == b[3]:
                errors.append(f"{a[3]}: two of its fixes both change {where}")
            else:
                warnings.append(f"{a[3]} and {b[3]} both change {where}; approving both will conflict")
                conflicts.setdefault(a[3], set()).add(b[3])
                conflicts.setdefault(b[3], set()).add(a[3])
    for f in out:
        f["conflicts"] = [g["id"] for g in out if g["id"] in conflicts.get(f["id"], ())]
    if src.link and "{head}" in src.link:
        for rel, info in src.files.items():
            if info["dirty"]:
                warnings.append(f"{rel} differs from HEAD, so its source links won't match these lines")
    if errors:
        raise Invalid("\n".join(errors))

    source = {"kind": src.kind, "label": src.spec.get("label") or data.get("title"),
              "url": src.spec.get("url"), "root": str(src.root), "base": src.base,
              "mergeBase": src.merge_base, "head": src.head, "changeLabel": src.change_label}
    key_basis = json.dumps([data.get("title"), source["label"], source["url"], src.head])
    run = {"title": data.get("title") or "Review triage",
           "key": "triage:" + hashlib.sha1(key_basis.encode()).hexdigest()[:12],
           "source": source, "findings": out}
    return run, warnings


def print_check(run):
    for f in run["findings"]:
        print(f"\n{f['id']}  P{f['priority']}  {f['category']}: {f['title']}")
        for c in f["context"]:
            label = f" ({c['label']})" if c["label"] else ""
            print(f"  context {c['file']} {c['start']}–{c['end']}{label}")
            for n in c["highlight"]:
                print(f"    {n:>5} | {c['lines'][n - c['start']]}")
        for x in f["fixes"]:
            print(f"  fix {x['file']} replaces {x['start']}–{x['end']}")
            for n, line in enumerate(x["lines"], x["start"]):
                print(f"    {n:>5} | {line}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("findings", type=Path)
    ap.add_argument("--check", action="store_true", help="print highlighted and replaced lines")
    args = ap.parse_args()
    path = args.findings.resolve()
    try:
        run, warnings = resolve(json.loads(path.read_text()), path)
    except (Invalid, json.JSONDecodeError, OSError) as e:
        sys.exit(f"Not built. Fix these and rebuild:\n{e}")
    out_dir = path.parent
    (out_dir / "resolved.json").write_text(json.dumps(run, indent=1))
    embedded = json.dumps(run).replace("</", "<\\/")
    (out_dir / "index.html").write_text(TEMPLATE.read_text().replace("/*DATA*/null", embedded))
    if args.check:
        print_check(run)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    print(f"wrote {out_dir / 'index.html'} with {len(run['findings'])} findings and {len(warnings)} warnings")


if __name__ == "__main__":
    main()
