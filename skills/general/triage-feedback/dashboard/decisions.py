"""Load a built run and the user's approvals for apply.py and review.py."""

import json
import sys
from pathlib import Path


def add_arguments(ap):
    ap.add_argument("run_dir", type=Path, help="folder containing resolved.json")
    ap.add_argument("--approve", metavar="IDS",
                    help="comma-separated approved IDs, used instead of decisions.json "
                         "(for decisions pasted into the chat)")
    ap.add_argument("--notes-handled", action="store_true",
                    help="confirm that findings.json was updated for every note on an approved finding")


def load(args):
    run_dir = args.run_dir.expanduser().resolve()
    resolved = run_dir / "resolved.json"
    if not resolved.exists():
        sys.exit(f"No resolved.json in {run_dir}. Run build.py first.")
    run = json.loads(resolved.read_text())
    by_id = {f["id"]: f for f in run["findings"]}

    if args.approve is not None:
        ids = [i.strip() for i in args.approve.split(",") if i.strip()]
        unknown = [i for i in ids if i not in by_id]
        if unknown:
            sys.exit(f"Unknown finding IDs: {', '.join(unknown)}")
        decisions = {i: {"decision": "approved", "note": ""} for i in ids}
    else:
        path = run_dir / "decisions.json"
        if not path.exists():
            sys.exit(f"No decisions.json in {run_dir}. If the user pasted their decisions, pass --approve IDS.")
        saved = json.loads(path.read_text())
        if saved.get("key") != run["key"]:
            sys.exit("decisions.json was saved for a different build of this dashboard (the reviewed "
                     "commit or title changed). Ask the user to triage the rebuilt dashboard, or pass --approve IDS.")
        decisions = {d["id"]: d for d in saved.get("decisions", []) if d.get("id") in by_id}

    approved = [f for f in run["findings"] if decisions.get(f["id"], {}).get("decision") == "approved"]
    noted = [(f, decisions[f["id"]].get("note", "").strip()) for f in approved]
    noted = [(f, n) for f, n in noted if n]
    if noted and not args.notes_handled:
        print("These approved findings have notes from the user:\n", file=sys.stderr)
        for f, note in noted:
            print(f"  {f['id']}: {f['title']}\n    Note: {note}", file=sys.stderr)
        sys.exit("\nIf a note changes a fix, update findings.json and rebuild. "
                 "Then rerun with --notes-handled.")
    if not approved:
        sys.exit("No findings are approved.")
    return run, approved
