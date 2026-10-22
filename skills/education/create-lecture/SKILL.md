---
name: create-lecture
description: >
  Generates a structured lecture from an unordered list of topics. The agent
  sequences the topics pedagogically, produces _outline.md for review, and then
  generates the full lecture as index.rst following the Lecture Style Guide and
  RST conventions. Trigger when the user asks to "create a lecture", "generate
  lecture content", or "write a lecture from topics." Topics may be provided
  inline or in a file. Do NOT trigger for converting existing documents or
  editing already-written lectures.
---

# Create Lecture

Generate a well-structured lecture from an unordered list of topics, following
the Lecture Style Guide and producing a Sphinx-compatible `index.rst`.

## Step 1: Read the Prerequisites

Two sources define the rules that apply throughout this skill. Read both
before drafting any content:

- **`references/lecture-style-guide.md`** (bundled with this skill) --- the
  authoritative source for publication formats, page structure, tone, voice,
  pronouns, and content progression. Pay close attention to the Do/Don't
  examples; they're the fastest way to calibrate the correct register.

- **The `convert-to-restructuredtext` skill** --- defines heading decorations,
  list formatting, inline markup, code blocks, dashes and quotes, hyperlinks,
  and other general RST conventions used throughout the lecture.

Later steps reference these sources instead of restating them. If you're
unsure about a rule while writing, re-open the relevant file rather than
guessing.

## Step 2: Parse Topics

Collect all topics from the user's input. Topics may be:

- Listed inline in the user's message

- Provided in a file (use the Read tool if a path is given)

Do not assume any order is intended---you determine the order in Step 3.

If an output directory is not clear from context, ask the user where to save
the output files before continuing.

## Step 3: Determine Topic Order

Sequence the topics pedagogically so the lecture builds understanding
progressively:

- **Foundational first**: prerequisites before the concepts that depend on them

- **Cluster related topics**: group concepts that share context or vocabulary

- **Simple to complex**: concrete, narrow cases before abstract or general ones

- **Problem-solution framing**: introduce the problem a concept solves before
  introducing the concept itself

Write down your ordered list and the reasoning behind your sequencing
decisions---you'll reference this when writing the outline.

## Step 4: Create `_outline.md`

Write `_outline.md` to the output directory. Use this skeleton, following the
page structure from the Lecture Style Guide:

```markdown
# [Lecture Title]

## Overview

[One paragraph: what this lecture covers and why it matters to the reader as a
developing professional.]

## Learning Goals

- [Concrete, measurable goal 1]
- [Concrete, measurable goal 2]
- ...

## [Topic Section 1 Title]

### [Subsection Title] *(if needed)*

- **Key concept**: [What it is and why it matters]
- **Example / analogy**: [The concrete anchor to use]
- **Gotcha**: [Common mistake or stumbling block to flag] *(if applicable)*

## [Topic Section N Title]

...

## Looking Ahead

[What concepts or skills does this lecture lead into?]

## Further Study

- [Resource 1 --- title and brief description]
- [Resource 2 --- title and brief description]

## Coming Up

[Brief preview of the next related lab or lecture.]
```

After writing the file, **present the outline to the user and ask for
confirmation before generating the lecture**. If the user requests changes,
revise `_outline.md` and confirm again before proceeding.

## Step 5: Generate `index.rst`

Using the confirmed outline, write the full lecture to `index.rst` in the
output directory.

Apply the tone, voice, and content-progression rules from
`references/lecture-style-guide.md` (read in Step 1) and the general RST
formatting rules from the `convert-to-restructuredtext` skill (also read in
Step 1). Do not try to recall them from memory---re-open either file if you're
unsure.

The sections below cover only what's specific to lectures and not already in
those sources: the lecture skeleton and a handful of lecture-only RST
directives.

---

### Lecture Skeleton

Follow this structure exactly:

```
Title (H1 --- overline and underline of =)

.. only:: not revealjs

   Overview paragraph(s) for the handout.

Intro (H2)
+-- Intro (H3)      <- contextual hook; connects to prior lectures; motivates topic
+-- Goals (H3)      <- learning objectives as .. incr:: item bullet list

[Content sections] (H2)
+-- [Subsections] (H3)   <- with .. incr:: and .. newslide:: throughout

Review (H2)              <- optional; summary bullet list wrapped in .. incr:: item
+-- Review (H3)

Looking Ahead (H2)
+-- Coming up... (H3)    <- what's next: lab preview or future topics
+-- Further study (H3)   <- definition list of linked titles with descriptions
```

---

### Lecture-Specific RST Conventions

**Incremental reveals.** Every bullet list and definition list must be wrapped
in an `.. incr::` directive. Never use bare lists in lectures. Three variants:

- `.. incr:: item` --- bullet list where each item appears one at a time
- `.. incr:: nest` --- definition list (term + body pairs)
- `.. incr:: one` --- a single block that appears all at once

Example:

```rst
.. incr:: item

   - First point.

   - Second point.

   - Third point.
```

**Slide breaks.** Use `.. newslide::` where a natural pause occurs---typically
after every 3--5 bullet points or when transitioning between sub-topics. Any
H3 subsection with more than ~6 bullet points or 2 paragraphs almost certainly
needs at least one `.. newslide::`.

**Intro wrap.** The overview paragraph immediately after the H1 title must be
wrapped in `.. only:: not revealjs` so it appears in handouts but not on
slides.

**Further study format.** Use a definition list with linked titles:

```rst
`Resource Title <URL>`__
   One-sentence description of what the reader will find there.
```

**Avoid admonitions.** Notes and warnings don't render well on slides. Convert
gotchas and caveats into regular prose or incremental bullet points instead.

**Figure styling** (if images are included):

```rst
.. figure:: _images/descriptive-name.png
   :class: img-fluid
   :figclass: col-8 mx-auto

   Caption describing what the image shows.
```

---

## Step 6: Validate Against Outline

After writing `index.rst`, verify and fix any gaps before finishing:

- Every section in `_outline.md` has a corresponding section in the lecture.

- Every key concept listed in the outline is introduced in the lecture.

- Every example or analogy noted in the outline appears in the lecture.

- Every gotcha flagged in the outline is surfaced as prose or an incremental
  bullet (not an admonition).

- The topic order in the lecture matches the outline exactly.

- Every list is wrapped in an `.. incr::` directive (no bare lists).

- The overview paragraph is wrapped in `.. only:: not revealjs`.

## Step 7: Report Completion

Tell the user:

- Full paths of the files created (`_outline.md`, `index.rst`).

- Number of sections and approximate word count of the lecture.

- Any topics where you made significant assumptions the user should verify.
