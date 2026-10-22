#!/usr/bin/env python3
"""Build a two-column review page for a fiction chapter.

    build_review.py extract <manuscript.md>
    build_review.py build   <manuscript.md> <notes.txt> [--force] [--out PATH]

The script owns the manuscript column and the paragraph numbering. The model
owns the letter and the comment cards. Both subcommands use the same parser,
so the paragraph numbers cited in the letter cannot drift from the numbers
rendered in the rows.

The manuscript is opened read-only and is never written to.
"""

import argparse
import hashlib
import html
import re
import sys
from datetime import date
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "review-template.html"

DEFAULTS = {
    "title": "Notes",
    "kicker": "Notes",
    "h1": "untitled",
    "dek": "Your prose on the left, my notes on the right. The manuscript file is unchanged.",
    "metarow": "",
    "accent": "#8c2f2f",
    "accent-dark": "#e08a86",
    "cont": "#9a6414",
    "cont-dark": "#e0b072",
}

RULE_RE = re.compile(r"^\s*([-*_])\s*(\1\s*){2,}$")
STRUCK_SPAN_RE = re.compile(r"~~(.+?)~~", re.S)
PCT_COMMENT_RE = re.compile(r"%%(.*?)%%", re.S)
BOLD_RE = re.compile(r"\*\*(.+?)\*\*", re.S)
STAR_EM_RE = re.compile(r"\*([^*\n]+)\*")
US_EM_RE = re.compile(r"(?<![A-Za-z0-9_])_([^_\n]+)_(?![A-Za-z0-9_])")


# --------------------------------------------------------------------------
# parsing
# --------------------------------------------------------------------------

class Para:
    """A numbered prose paragraph."""

    def __init__(self, number, raw):
        self.number = number
        self.raw = raw
        self.evidence = []          # (kind, text) found inside this paragraph


class Excluded:
    """A block that is not numbered and not displayed."""

    def __init__(self, kind, text, after):
        self.kind = kind
        self.text = text
        self.after = after          # paragraph number this followed (0 = before ¶1)


def strip_frontmatter(text):
    if not text.startswith("---"):
        return text
    lines = text.split("\n")
    if lines[0].strip() != "---":
        return text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[i + 1:])
    return text


SENTINEL_RE = re.compile("\x00C(\\d+)\x00")


def is_wholly_struck(block):
    """True if the block is nothing but one struck span (plus whitespace)."""
    residue = STRUCK_SPAN_RE.sub("", SENTINEL_RE.sub("", block))
    return residue.strip() == "" and "~~" in block


def read_source(path):
    """Read the manuscript exactly once and hash what we read.

    These vaults live in iCloud and are edited in Obsidian while a review is
    being written — the file can and does change mid-run. Hashing a second
    read would stamp the page with a sha that doesn't describe the content
    actually rendered, which would defeat the drift check on the next build.
    """
    data = path.read_bytes()
    return data.decode("utf-8"), hashlib.sha256(data).hexdigest()[:12]


def parse(text):
    """Return (paras, excluded). Identical for extract and build.

    %%...%% comments are lifted out document-wide *before* blocks are split,
    because Obsidian comments routinely span blank lines — tadpoles.md has one
    that runs 56 lines and hides an entire alternate draft. A per-block regex
    silently leaves the delimiters stranded in the prose.
    """
    text = strip_frontmatter(text)

    comments = []

    def stash(m):
        comments.append(m.group(0))
        return f"\x00C{len(comments) - 1}\x00"

    text = PCT_COMMENT_RE.sub(stash, text)
    blocks = re.split(r"\n\s*\n", text)

    paras, excluded, n = [], [], 0

    def comment_text(block):
        return "\n\n".join(comments[int(i)] for i in SENTINEL_RE.findall(block))

    for block in blocks:
        block = block.strip("\n")
        if not block.strip():
            continue

        first = block.lstrip()

        if first.startswith(">"):
            excluded.append(Excluded("callout", block, n))
            continue
        if first.startswith("#"):
            excluded.append(Excluded("heading", block, n))
            continue
        if RULE_RE.match(block.strip()):
            excluded.append(Excluded("rule", block, n))
            continue
        if is_wholly_struck(block):
            excluded.append(Excluded("struck", SENTINEL_RE.sub(comment_text, block), n))
            continue
        if SENTINEL_RE.sub("", block).strip() == "":
            excluded.append(Excluded("comment", comment_text(block), n))
            continue

        n += 1
        para = Para(n, block)
        for i in SENTINEL_RE.findall(block):
            para.evidence.append(("comment-span", comments[int(i)]))
        for m in STRUCK_SPAN_RE.finditer(block):
            para.evidence.append(("struck-span", m.group(0)))
        paras.append(para)

    return paras, excluded


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------

def to_html(raw):
    """Manuscript text -> display HTML. Escapes first, then adds emphasis."""
    s = SENTINEL_RE.sub("", PCT_COMMENT_RE.sub("", raw))
    s = STRUCK_SPAN_RE.sub("", s)
    s = re.sub(r"[ \t]{2,}", " ", s)
    s = html.escape(s, quote=False)
    s = BOLD_RE.sub(r"<strong>\1</strong>", s)
    s = STAR_EM_RE.sub(r"<em>\1</em>", s)
    s = US_EM_RE.sub(r"<em>\1</em>", s)
    return s.strip()


def render_rows(paras, notes, banners):
    out = []
    for p in paras:
        for cls, label, text in banners.get(p.number, []):
            if cls == "seam":
                out.append(f'<div class="seam">\n{text}\n</div>\n')
            else:
                out.append(
                    f'<div class="{cls}">\n'
                    f'  <span class="lbl">{label}</span>\n'
                    f'  <span class="txt">{text}</span>\n'
                    f'</div>\n'
                )
        body = to_html(p.raw)
        if not body:
            continue
        cards = notes.get(p.number, "").strip()
        out.append(
            f'<div class="row">\n'
            f'  <div class="ms"><span class="n">{p.number}</span>\n'
            f'    <p>{body}</p>\n'
            f'  </div>\n'
            f'  <div class="cmt">{cards}</div>\n'
            f'</div>\n'
        )
    return "\n".join(out)


# --------------------------------------------------------------------------
# notes file
# --------------------------------------------------------------------------

def parse_notes(path):
    """Directives at column zero, raw HTML between them."""
    meta, notes, banners = dict(DEFAULTS), {}, {}
    letter = footer = ""
    mode = target = None
    buf = []

    def flush():
        nonlocal letter, footer, buf
        chunk = "\n".join(buf).strip()
        buf = []
        if not chunk:
            return
        if mode == "letter":
            letter = chunk
        elif mode == "footer":
            footer = chunk
        elif mode == "note":
            notes[target] = notes.get(target, "") + "\n" + chunk
        elif mode == "banner":
            cls, num = target
            label, _, text = chunk.partition("|")
            if not text:
                label, text = "", label
            banners.setdefault(num, []).append((cls, label.strip(), text.strip()))

    for line in path.read_text(encoding="utf-8").split("\n"):
        if line.startswith("@"):
            flush()
            parts = line[1:].split(None, 1)
            directive = parts[0]
            rest = parts[1] if len(parts) > 1 else ""
            if directive == "meta":
                key, _, value = rest.partition(" ")
                meta[key.strip()] = value.strip()
                mode = None
            elif directive == "letter":
                mode = "letter"
            elif directive == "footer":
                mode = "footer"
            elif directive == "note":
                mode, target = "note", int(rest.strip())
            elif directive == "banner":
                num, _, cls = rest.strip().partition(" ")
                cls = (cls.strip() or "pass")
                if cls not in ("pass", "seam", "movement"):
                    sys.exit(f"error: unknown banner class {cls!r} (pass|seam|movement)")
                mode, target = "banner", (cls, int(num))
            else:
                sys.exit(f"error: unknown directive @{directive}")
        else:
            buf.append(line)
    flush()

    return meta, letter, footer, notes, banners


# --------------------------------------------------------------------------
# subcommands
# --------------------------------------------------------------------------

def cmd_extract(args):
    path = Path(args.manuscript)
    text, sha = read_source(path)
    paras, excluded = parse(text)

    print(f"PARAGRAPHS ({len(paras)} total)")
    print("=" * 72)
    for p in paras:
        flat = re.sub(r"\s+", " ", p.raw).strip()
        print(f"{p.number:>4} | {flat}")

    spans = [(p.number, k, t) for p in paras for k, t in p.evidence]
    print()
    print(f"EXCLUDED ({len(excluded) + len(spans)} items)")
    print("=" * 72)
    if not excluded and not spans:
        print("(none)")
    for e in excluded:
        anchor = f"after ¶{e.after}" if e.after else "before ¶1"
        flat = re.sub(r"\s+", " ", e.text).strip()
        print(f"{anchor:<12} {e.kind:<12} {flat}")
    for num, kind, text in spans:
        flat = re.sub(r"\s+", " ", text).strip()
        print(f"{'in ¶' + str(num):<12} {kind:<12} {flat}")

    print()
    print("Excluded blocks are not numbered and are not displayed in the review.")
    print("They are the author telling you what she already knows is wrong — read them.")
    print()
    print(f"source sha {sha} — if this differs when you build, the file changed under you.")


def cmd_build(args):
    src = Path(args.manuscript)
    text, sha = read_source(src)
    paras, _ = parse(text)
    if not paras:
        sys.exit(f"error: no prose paragraphs found in {src}")

    meta, letter, footer, notes, banners = parse_notes(Path(args.notes))

    valid = {p.number for p in paras}
    for num in sorted(set(notes) | set(banners)):
        if num not in valid:
            sys.exit(
                f"error: notes reference ¶{num}, but {src.name} has "
                f"{len(paras)} paragraphs (1-{len(paras)}). "
                f"Re-run `extract` — the manuscript has probably changed."
            )

    slug = src.stem.lower().replace(" ", "-")
    out = Path(args.out) if args.out else src.with_name(f"{slug}-review.html")

    if out.exists() and not args.force:
        prior = out.read_text(encoding="utf-8")
        pm = re.search(r'name="review:paragraphs" content="(\d+)"', prior)
        sm = re.search(r'name="review:source-sha" content="([0-9a-f]+)"', prior)
        if pm and sm and (sm.group(1) != sha):
            sys.exit(
                f"refusing to overwrite {out.name}\n"
                f"  existing review: {pm.group(1)} paragraphs, source sha {sm.group(1)}\n"
                f"  manuscript now:  {len(paras)} paragraphs, source sha {sha}\n"
                f"The manuscript changed since that review was written. Ask the user "
                f"whether to write a fresh review, update in place, or review only what "
                f"changed. Pass --force once they have chosen."
            )
        if not (pm and sm):
            sys.exit(f"refusing to overwrite existing {out.name}; pass --force")

    page = TEMPLATE.read_text(encoding="utf-8")
    for token, value in {
        "__PAGE_TITLE__": meta["title"],
        "__ACCENT_LIGHT__": meta["accent"],
        "__ACCENT_DARK__": meta["accent-dark"],
        "__C_CONT_LIGHT__": meta["cont"],
        "__C_CONT_DARK__": meta["cont-dark"],
        "__KICKER__": meta["kicker"],
        "__H1__": meta["h1"],
        "__DEK__": meta["dek"],
        "__META__": meta["metarow"],
        "__LETTER__": letter,
        "__BODY__": render_rows(paras, notes, banners),
        "__FOOTER__": footer,
        "__PARA_COUNT__": str(len(paras)),
        "__SRC_SHA__": sha,
        "__DATE__": date.today().isoformat(),
    }.items():
        page = page.replace(token, value)

    leftover = re.findall(r"__[A-Z_]+__", page)
    if leftover:
        sys.exit(f"error: unsubstituted tokens remain: {sorted(set(leftover))}")

    out.write_text(page, encoding="utf-8")
    print(f"wrote {out}")
    print(f"  {len(paras)} paragraphs, {len(notes)} annotated, {sum(len(v) for v in banners.values())} banners")
    print(f"  manuscript untouched (sha {sha})")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("extract", help="print numbered paragraphs and excluded blocks")
    e.add_argument("manuscript")
    e.set_defaults(func=cmd_extract)

    b = sub.add_parser("build", help="render the review page")
    b.add_argument("manuscript")
    b.add_argument("notes")
    b.add_argument("--out")
    b.add_argument("--force", action="store_true", help="overwrite a stale review")
    b.set_defaults(func=cmd_build)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
