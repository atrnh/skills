# Maintaining the review council

Notes for editing the [review-council](../../skills/general/review-council/SKILL.md) skill.
Agents running a council don't need them, so they live here rather than in the skill.

## Who reads what

| File | Read by |
| --- | --- |
| `SKILL.md` | The chair |
| `references/reviewer-brief.md` | The chair, who fills it in; the result goes to every reviewer |
| `references/scoring.md` | Reviewers get "Scale" and "Evidence"; the chair follows the rest to combine scores |
| `references/modes/<mode>.md` | Reviewers get everything above "For the chair"; the chair reads the rest |

Reviewers are fresh agents that may not have this repository's skills installed. Everything
they need must be written into the files they receive. Don't point a reviewer at another skill.

Reviewers return a Markdown review, and the chair works from those results directly. There are
no intermediate data files, so the review format in `reviewer-brief.md` is written for the
chair to read, not for a program to parse.

## Mode file format

Keep:

- a `Version:` line;
- the criteria table near the top, with the columns `Code`, `Criterion`, and `Gate`, a
  two-letter uppercase code per criterion, and `yes` in `Gate` for gate criteria;
- a `## For the chair` heading, which `reviewer-brief.md` uses as the end of what reviewers
  receive.

## Versions and comparable runs

The `Version:` line is how runs are told apart. Each report records the rubric version, and an
improvement loop compares only runs that share it, along with the same panel, brief, and
context. Raise the version whenever a change to the rubric or to `scoring.md` could move scores.

## Adding a mode

1. Write `references/modes/<mode>.md` in the format above. Put mode-specific judgment, such as
   what not to reward and where a problem belongs, in its reviewer section.
2. Put context the chair must gather before briefing, like curriculum's course placement, in
   its "For the chair" section.
3. Add the mode to the table in `SKILL.md` and to the skill's description, and remove it from
   the list of modes not yet written.
4. Keep `reviewer-brief.md` and `scoring.md` free of anything specific to one mode.

## Where the curriculum rubric came from

Progression, examples and concepts, language for purpose, practice design, and presented form
began as this repository's education principles. The rubric now carries that guidance itself
and doesn't depend on them.

The rest comes from instructional-design and learning research:

- Mental models and misconceptions: Greg Wilson's
  [Teaching Tech Together](https://third-bit.com/t3/models.html) and the prior-knowledge
  principle in Ambrose et al.,
  [How Learning Works](https://www.cmu.edu/teaching/principles/learning.html).
- Purpose and seeing the whole task early: Ambrose's motivation principle and Merrill's
  [First Principles of Instruction](https://nic.pressbooks.pub/lidtfoundations/chapter/using-the-first-principles-of-instruction-to-make-instruction-effective-efficient-and-engaging/).
- Economy: Mayer's [coherence principle](https://doi.org/10.1017/cbo9780511811678.007).
- Knowing when to apply an idea: Ambrose's mastery principle and Merrill's integration phase.
- Practice over time: Dunlosky et al. on
  [retrieval practice and spacing](https://journals.sagepub.com/stoken/rbtfl/Z10jaVH/60XQM/full),
  and the [expertise reversal effect](https://doi.org/10.1207/s15326985ep3801_4) on fading
  support.
- The rule against rewarding polish, the signs of shallow material written into the criteria,
  and the reading log: findings that AI judges are lenient and reward length
  and confident tone, and Sadler's argument that
  [quality judgment is learned from examples](https://doi.org/10.1080/02602930801956059).

Accessibility and inclusion are out of scope for this rubric. Assessments will get their own
mode.

## Open work

- **Contrasting examples.** For each criterion, a Weak and two different Strong excerpts on the
  same content, with a note on what differs. These need excerpts from approved material.
- **Calibration.** Run the council on three to five pieces with known scores, look for
  leniency or scores bunched in one band, and adjust the band descriptions.
- **Assessment, code, and UI modes.**
