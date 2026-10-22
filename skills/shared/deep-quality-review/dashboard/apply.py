#!/usr/bin/env python3
"""Apply the approved fixes from a triage dashboard to the source files.

Usage: apply.py RUN_DIR [--approve IDS] [--notes-handled] [--root PATH] [--dry-run]

Approvals come from RUN_DIR/decisions.json unless --approve is given. Each fix
replaces whole lines. Before writing, the lines a fix replaces must still read
exactly as they did at build time; if they've moved, the fix is applied where
that exact block now appears, provided it appears only once. --root applies the
fixes to another checkout of the same files, such as the author's own branch.
"""

import argparse
import difflib
import sys
from pathlib import Path

import decisions


def span(a, b):
    return f"lines {a}–{b}" if a != b else f"line {a}"


def locate(lines, fix):
    start, block = fix["start"] - 1, fix["lines"]
    if lines[start:start + len(block)] == block:
        return start
    hits = [i for i in range(len(lines) - len(block) + 1) if lines[i:i + len(block)] == block]
    return hits[0] if len(hits) == 1 else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    decisions.add_arguments(ap)
    ap.add_argument("--root", type=Path, help="apply to this checkout instead of the reviewed one")
    ap.add_argument("--dry-run", action="store_true", help="print a diff instead of writing")
    args = ap.parse_args()
    run, approved = decisions.load(args)
    root = (args.root or Path(run["source"]["root"])).expanduser().resolve()

    by_file, manual = {}, []
    for f in approved:
        if not f["fixes"]:
            manual.append(f)
        for x in f["fixes"]:
            by_file.setdefault(x["file"], []).append((f["id"], x))

    failed, report = [], []
    for rel, fixes in by_file.items():
        path = root / rel
        if not path.is_file():
            failed.append(f"{rel}: not found under {root}")
            continue
        text = path.read_text()
        nl = "\r\n" if "\r\n" in text else "\n"
        lines = text.splitlines()
        placed, problems = [], []
        for fid, x in fixes:
            at = locate(lines, x)
            if at is None:
                problems.append(f"{fid}: {rel} {span(x['start'], x['end'])} changed after the review")
                continue
            placed.append((at, at + len(x["lines"]), fid, x))
        placed.sort(key=lambda p: p[0])
        for a, b in zip(placed, placed[1:]):
            if b[0] < a[1]:
                problems.append(f"{a[2]} and {b[2]} both change {rel} near line {b[0] + 1}; approve only one")
        if problems:
            failed += problems
            continue
        new = list(lines)
        for at, end, fid, x in sorted(placed, key=lambda p: p[0], reverse=True):
            new[at:end] = x["replacement"].split("\n") if x["replacement"] else []
            moved = "" if at + 1 == x["start"] else f" (found at line {at + 1})"
            report.append(f"{fid}: {rel} {span(x['start'], x['end'])}{moved}")
        out = nl.join(new) + (nl if text.endswith(("\n", "\r")) else "")
        if args.dry_run:
            sys.stdout.writelines(difflib.unified_diff(
                text.splitlines(keepends=True), out.splitlines(keepends=True), f"a/{rel}", f"b/{rel}"))
        else:
            path.write_text(out)

    verb = "Would apply" if args.dry_run else "Applied"
    if report:
        print(f"\n{verb} {len(report)} fix(es) in {root}:")
        print("\n".join(f"  {r}" for r in sorted(report)))
    if manual:
        print("\nApproved without a line-level fix, so make these by hand:")
        for f in manual:
            print(f"  {f['id']}: {f['title']}" + (f"\n    {f['fixNote']}" if f["fixNote"] else ""))
    if failed:
        print("\nNot applied (files with a problem were left unchanged):", file=sys.stderr)
        print("\n".join(f"  {e}" for e in failed), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
