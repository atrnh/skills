# Maintaining the review council

Notes for editing the [review-council](../../skills/general/review-council/SKILL.md) skill.
Agents running a council don't need them, so they live here rather than in the skill.

## Who reads what

| File | Read by |
| --- | --- |
| `SKILL.md` | The chair |
| `references/reviewer-brief.md` | The chair, who fills it in; the result goes to every reviewer |
| `references/scoring.md` | Reviewers get "Scale" and "Evidence"; the rest explains the script to the chair |
| `references/modes/<mode>.md` | Reviewers get everything above "For the chair"; the chair reads the rest |
| `scripts/aggregate.py` | Run by the chair; implements the rest of `scoring.md` |

Reviewers are fresh agents that may not have this repository's skills installed. Everything
they need must be written into the files they receive. Don't point a reviewer at another skill.

## Mode file format

`aggregate.py` reads each mode file and stops with an error if it can't, so keep:

- a `Version:` line;
- the criteria table above the first `## ` heading, with the columns `Code`, `Criterion`, and
  `Gate`, a two-letter uppercase code per criterion, and `yes` in `Gate` for gate criteria;
- no other table rows above the first `## ` heading;
- a `## For the chair` heading, which `reviewer-brief.md` uses as the end of what reviewers
  receive.

## Changing scoring

When you change how scores combine, change `scoring.md` and `aggregate.py` together, and update
`scripts/test_aggregate.py`. Run the tests from the scripts folder:

```sh
python3 -m unittest test_aggregate
```

## Versions and comparable runs

`scores.json` records fingerprints of the material under review, its context files, the panel's
reviewers and settings, the rubric, the scoring rules, the brief, `context.md`, and the script.
An improvement loop compares only runs whose fingerprints match apart from the material under
review, so any edit to the others already separates old runs from new ones. The `Version:` line is a label for
people. Raise it when a change could move scores, so reports and commit messages can name the
rubric they used.

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
