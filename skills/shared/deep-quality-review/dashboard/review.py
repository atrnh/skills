#!/usr/bin/env python3
"""Draft a GitHub pull request review from the approved findings.

Usage: review.py RUN_DIR [--approve IDS] [--notes-handled] [--summary TEXT] [--event EVENT]

Writes RUN_DIR/review.json and prints a preview plus the command that posts it.
Nothing is posted. Fixes on lines inside the PR's diff become inline comments
with suggestion blocks; GitHub can't comment on other lines, so those findings
go in the review body with the replacement as a code block. Each comment uses
the finding's "comment" text, or its "problem" text if there is none.
"""

import argparse
import json
import re
import sys

import decisions

LANG = {"rst": "rst", "md": "markdown", "svg": "xml", "html": "html", "py": "python", "cs": "csharp",
        "js": "javascript", "ts": "typescript", "json": "json", "yml": "yaml", "yaml": "yaml"}


def fence(text, info=""):
    ticks = "`" * max(3, max((len(m) for m in re.findall(r"`+", text)), default=0) + 1)
    return f"{ticks}{info}\n{text}\n{ticks}"


def span(a, b):
    return f"lines {a}–{b}" if a != b else f"line {a}"


def explanation(f):
    parts = [f["comment"] or f["problem"]]
    links = [f"[{e['text']}]({e['url']})" for e in f["evidence"] if e.get("url")]
    if links:
        parts.append("Evidence: " + "; ".join(links) + ".")
    if f["fixNote"]:
        parts.append(f["fixNote"])
    return "\n\n".join(parts)


def inline_comment(path, start, end, body):
    c = {"path": path, "line": end, "side": "RIGHT", "body": body}
    if start != end:
        c |= {"start_line": start, "start_side": "RIGHT"}
    return c


def outside(x, text):
    lang = LANG.get(x["file"].rsplit(".", 1)[-1], "")
    where = f"[`{x['file']}` {span(x['start'], x['end'])}]({x['url']})" if x["url"] else \
        f"`{x['file']}` {span(x['start'], x['end'])}"
    replacement = fence(x["replacement"], lang) if x["replacement"] else "Delete these lines."
    return f"**{where}.** {text}\n\nSuggested replacement:\n\n{replacement}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    decisions.add_arguments(ap)
    ap.add_argument("--summary", default="", help="opening paragraph of the review body")
    ap.add_argument("--event", default="COMMENT", choices=["COMMENT", "REQUEST_CHANGES", "APPROVE"])
    args = ap.parse_args()
    run, approved = decisions.load(args)
    src = run["source"]
    m = re.match(r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)", src.get("url") or "")
    if src["kind"] != "pr" or not m or not src.get("head"):
        sys.exit("review.py needs a pull request source with a GitHub url and a Git checkout of its head.")

    comments, body_items = [], []
    for f in approved:
        text, first = explanation(f), None
        anchor = next((c for c in f["context"] if c["commentable"]), None)
        for x in f["fixes"]:
            lead = text if first is None else f"Part of the same change as {first}."
            if x["commentable"]:
                comments.append(inline_comment(x["file"], x["start"], x["end"],
                                               f"{lead}\n\n{fence(x['replacement'], 'suggestion')}"))
                first = first or f"the comment on `{x['file']}` line {x['end']}"
            elif anchor:
                hl = anchor["highlight"] or [anchor["start"], anchor["end"]]
                lang = LANG.get(x["file"].rsplit(".", 1)[-1], "")
                where = f"`{x['file']}` {span(x['start'], x['end'])}"
                where = f"[{where}]({x['url']})" if x["url"] else where
                replacement = fence(x["replacement"], lang) if x["replacement"] else "Delete them."
                comments.append(inline_comment(anchor["file"], min(hl), max(hl),
                                               f"{lead}\n\nThe fix is on {where}, which is outside the diff. "
                                               f"Suggested replacement:\n\n{replacement}"))
                first = first or f"the comment on `{anchor['file']}` line {max(hl)}"
                anchor = None
            else:
                body_items.append(outside(x, lead))
                first = first or f"the note on `{x['file']}` {span(x['start'], x['end'])} in the review body"
        if not f["fixes"]:
            c = f["context"][0] if f["context"] else None
            if c and c["commentable"]:
                hl = c["highlight"] or [c["start"], c["end"]]
                comments.append(inline_comment(c["file"], min(hl), max(hl), text))
            else:
                where = f"[`{c['file']}` {span(c['start'], c['end'])}]({c['url']}). " if c and c["url"] else ""
                body_items.append(f"**{f['title']}.** {where}{text}")

    body = [args.summary.strip()] if args.summary.strip() else []
    if body_items:
        body.append("These apply to lines outside the diff, so they can't go inline:" if comments
                    else "These apply to lines outside the diff:")
        body += body_items
    payload = {"commit_id": src["head"], "event": args.event, "body": "\n\n".join(body), "comments": comments}
    out = args.run_dir.expanduser().resolve() / "review.json"
    out.write_text(json.dumps(payload, indent=1))

    print("=== Review body ===\n" + (payload["body"] or "(empty)"))
    for c in comments:
        print(f"\n=== {c['path']} {span(c.get('start_line', c['line']), c['line'])} ===\n{c['body']}")
    owner, repo, number = m.groups()
    print(f"\nWrote {out} with {len(comments)} inline comment(s) and {len(body_items)} in the body.")
    print(f"Post it with: gh api repos/{owner}/{repo}/pulls/{number}/reviews --method POST --input {out}")


if __name__ == "__main__":
    main()
