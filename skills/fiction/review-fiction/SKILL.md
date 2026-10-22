---
name: review-fiction
description: >
  Reviews a chapter of the user's fiction and produces a two-column HTML critique page
  beside the manuscript, with the prose on the left and anchored comments on the right.
  Use this skill whenever the user wants a review, critique, edit pass, notes, or feedback
  on a chapter, scene, or draft under Areas/Fiction/ — even if they just say "review this
  chapter", "what do you think of tadpoles", "give me notes on the heist", or open a
  fiction file and ask what's wrong with it. Trigger when the user names a chapter in the
  fiction vault and wants editorial feedback, structural diagnosis, continuity checking,
  or paragraph-level comments. Do NOT trigger for writing new fiction, continuing a scene,
  or rewriting prose on the user's behalf — this skill critiques existing drafts. Do NOT
  trigger for lab, exercise, or curriculum drafts; use review-lab for those.
---

# Review Fiction

Diagnose a chapter, then publish the diagnosis as a side-by-side page the author can read
against her own prose.

## What this never does

- **Never edit the manuscript.** Not one character. No callouts added, no typos fixed, no
  strikethroughs resolved. The review is a separate file. Say so in the footer of every
  page you produce.
- **Never merge two versions of a chapter into one review.** Review the file you were given.
- **Never write in the hedging editorial register.** See Step 5. This is the whole point.

## Step 1: Locate the chapter and the folder note

Resolve what the user named to a file under `Areas/Fiction/`. Read it.

Read `_index.md` in the same folder if one exists. Its ordered list is the authority on
chapter order — the `next:` frontmatter field appears in only some files, so treat it as a
cross-check, never the source. Anything under an **Extras** heading is off the main
sequence but is usually where the backstory lives, and it has been the highest-value read
every time. With no `_index.md`, fall back to the target plus its folder siblings.

If the chapter has version siblings (`the heist.md`, `the heist v2.md`, `the heist v3.md`),
ask which is canonical before spending reads. Then review that one and read the others as
evidence — a line present in v2 and cut in v3 is a decision the author already made.

## Step 2: Decide the read set

**Always read in full:** the target, `_index.md`, and the chapters immediately before and
after it.

**Then pick at most three more.** Harvest the proper nouns, secrets, lies, and physical
rules the target asserts, and grep the rest of the folder for them:

```bash
grep -ril "cazador\|magistrate\|mephistar\|regener" "Areas/Fiction/bg3/"
```

Read in full only where hits cluster. Grep output is enough for the rest. Do not read the
whole folder. Both hand-written reviews found everything they needed in exactly three extra
files. Name the read set in the page's dek so the author knows what informed the notes.

What you are looking for in those files is listed in
`${CLAUDE_SKILL_DIR}/references/analysis.md` under Pass 3.

## Step 3: Extract and number

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/build_review.py" extract "Areas/Fiction/bg3/tadpoles.md"
```

Work from this output, not from your own count. It prints every prose paragraph with its
number, then an `EXCLUDED` block listing the callouts, struck passages, and `%%…%%`
comments that were removed, each anchored to the paragraph it followed.

**Read the excluded block.** It is the author telling you what she already knows is wrong.
A `%%…%%` comment can hide an entire alternate draft — `tadpoles.md` has one running 56
lines — so check it before concluding a scene is missing.

The numbering rule, so you can predict it: after the frontmatter, blocks split on blank
lines. A block is numbered unless it starts with `>` or `#`, is a horizontal rule, is
entirely struck through, or is nothing but a comment. Numbering is 1-based and contiguous.
`%%…%%` and inline `~~…~~` spans are stripped from the display but do not affect numbering.
The same parser runs at build time, so the paragraph numbers in your letter cannot drift
from the numbers on the rows.

## Step 4: Diagnose structure first

Run the passes in `${CLAUDE_SKILL_DIR}/references/analysis.md`, in order. Summary:

1. **Is this one draft?** Duplicated beats, a quotation stopping mid-sentence, someone
   conceding twice. Two drafts spliced together is the most common finding here and it
   invalidates most other notes until settled.
2. **Is the best material spent well?** A reveal that arrives as trivia has been pre-spent.
3. **What does the rest of the book need from this chapter?** Lies that must land, costs
   established later that should be planted here, theses stated and never paid, and
   conspicuous absences.
4. **Continuity ledger.** Knowledge before acquisition, unclaimed titles, units, who
   triggers what.
5. **Only now**, prose and typos.

## Step 5: Load the voice

Read `${CLAUDE_SKILL_DIR}/references/voice.md` in full before writing a single word of the
review. The user asked for this skill because of the register, not the file format. A
structurally correct review in the wrong voice is a failure.

`crash site.md` still contains `[!comment]` callouts in the register the user explicitly
rejected. **If a note you have written would sit comfortably beside those callouts, it is
wrong.** Rewrite it before it reaches the page.

## Step 6: Write the letter

Fixed shape, in order:

- `<h2>The short version</h2>` — two or three paragraphs. The first names the best thing in
  the chapter. The second names the single biggest problem, flatly. Do not bury it.
- `<dl class="verdict">` — exactly four cells. Cells one and two are always **Best thing
  here** and **Actual problem**. Choose the other two to fit: *Cheapest big win*, *Weakest
  moment*, *Biggest gap*, *Best sentence*. Each `dd` is a fragment, not a sentence.
- Two to five `<h3>` sections, **titled as claims** — "He never thinks about Cazador", not
  "Character motivation".
- `<ol class="rebuild">` — five to eight sequenced actions citing paragraph numbers. This is
  the part the author works from.
- A continuity `<ul>`, each item bolded-lede then evidence.
- Typos last, one line each: `¶N wrong → right`.
- If the file contains `[!comment]` callouts, add a section saying which are correct and
  where you would go further — be specific about the difference in kind.

## Step 7: Write the notes file

Write to `/tmp/<slug>-notes.txt` following `${CLAUDE_SKILL_DIR}/references/notes-format.md`,
which has the directive grammar, the tag table, and the accent-colour rule.

## Step 8: Build

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/build_review.py" build \
  "Areas/Fiction/bg3/tadpoles.md" /tmp/tadpoles-notes.txt
```

Writes `<basename-hyphenated>-review.html` beside the manuscript.

If a review already exists, the script refuses and reports how far the manuscript has
drifted since that review was written. **Ask the user** whether to write fresh, update in
place, or review only what changed, then re-run with `--force`. Never force unasked.

Cross-link every review in the folder from every other — scan for existing `*-review.html`
and put them in the meta row and the footer. A previously written review won't link back
until it is regenerated; offer that, don't do it.

## Step 9: Report

Tell the user the output path, the paragraph count, which chapters you read, and the three
findings you would act on first — in the same voice as the review, not as a table of
contents. Then **offer**, without doing it, to add the nested review link under this
chapter in `_index.md`, matching the entries already there:

```markdown
- [[tadpoles]]
	- [review](file:///absolute/percent-encoded/path/tadpoles-review.html)
```
