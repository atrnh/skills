# Maintaining the review council

Notes for editing the [review-council](../../skills/general/review-council/SKILL.md) skill.
Agents running a council don't need them, so they live here rather than in the skill.

## Who reads what

| File | Read by |
| --- | --- |
| `SKILL.md` | The chair |
| `references/reviewer-brief.md` | The chair, who fills it in; the result goes to every reviewer |
| `references/scoring.md` | Reviewers get "Scale" and "Evidence"; the chair follows the rest to combine scores |
| `references/modes/<mode>.md`, or `<mode>/core.md` and its modules | Reviewers get everything above "For the chair" in the core and the chosen module; the chair reads the rest |

Reviewers are fresh agents that may not have this repository's skills installed. Everything
they need must be written into the files they receive. Don't point a reviewer at another skill.

Reviewers return a Markdown review, and the chair works from those results directly. There are
no intermediate data files, so the review format in `reviewer-brief.md` is written for the
chair to read, not for a program to parse.

## Panel settings

The [setup-review-council](../../skills/general/setup-review-council/SKILL.md) skill writes
`${XDG_CONFIG_HOME:-~/.config}/review-council/settings.md`, and the chair reads it in step 2.
Each setting's default appears in both skills: setup shows the full file, and step 2 names the
default beside each rule. Change both together. Settings stay personal, because a panel depends
on the accounts and CLIs on one machine.

The CLI commands in step 3 were checked on `cursor-agent`, `codex`, and `claude`: each read a
file at an absolute path and refused a request to write one. Check again after changing a flag.

## Mode file format

Keep:

- a `Version:` line;
- the criteria table near the top, with the columns `Code`, `Criterion`, and `Gate`, a
  two-letter uppercase code per criterion, and `yes` in `Gate` for gate criteria;
- a `## For the chair` heading, which `reviewer-brief.md` uses as the end of what reviewers
  receive.

### Core and modules

A mode that serves several kinds of artifact can split into a core and modules, as curriculum
does: `modes/<mode>/core.md` plus one file per module. The chair chooses at most one module, and
reviewers get the core's text followed by the module's. They never see a module that wasn't
chosen. Each file follows the format above, and codes are unique across the core and its
modules.

- A criterion belongs in the core only when its bands can be written without naming a kind of
  artifact. If its Strong band needs "in a lab" or "in a lecture", it belongs in a module.
- Keep the core to about ten criteria and a module to about four. Every criterion added thins
  the evidence behind the others.
- A module's reviewer text opens by saying its criteria are scored after the core's, and adds
  its own "Where a problem belongs" rules for overlaps with core criteria.
- The core's "For the chair" section says how to choose the module.

## Versions and comparable runs

The `Version:` line is how runs are told apart. Each report records the rubric and module
versions, such as `curriculum core 7 + lab 1`, and an improvement loop compares only runs that
share them, along with the same panel, brief, and context. Raise a file's version whenever a
change to it, or to `scoring.md`, could move scores. Raising a module's version doesn't affect
runs that don't use it.

Curriculum core 7 isn't comparable with version 6, the single rubric it replaced. A loop already
running on version 6 keeps its copied `brief.md`, so it can finish unchanged.

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
- Checkpoints in the lab module: Hattie and Timperley's
  [The Power of Feedback](https://doi.org/10.3102/003465430298487), on feedback that tells
  learners where they stand against the goal.
- The lecture module: Mayer's
  [multimedia principles](https://doi.org/10.1017/9781316941355) for presented form, used as
  look-fors because their evidence comes mostly from short self-paced lessons, and Freeman et al.
  on [active learning](https://doi.org/10.1073/pnas.1319030111) for engagement and checks.
  Teachability draws on Wilson's Teaching Tech Together.

The split into a core and modules follows rubrics such as the
[EQuIP rubric for science](https://www.nextgenscience.org/sites/default/files/EQuIP%20Rubric%20for%20Science%20v3.pdf),
which adds criteria for units to a base set for lessons.

The lab module was tried before release on three labs, with and without it, under the same
three-reviewer panel. It made reviewers report runnability and troubleshooting problems more
consistently and gave them a home, but its scores didn't separate the labs, which were all weak
on those criteria. Presented form, then a core criterion, came back from lab reviews as a mix of
scores, `na`, and `cannot_assess`, and left one run incomplete, which is why it moved to the
lecture module.

Accessibility and inclusion are out of scope for this rubric. Assessments will get their own
mode.

## Open work

- **Contrasting examples.** For each criterion, a Weak and two different Strong excerpts on the
  same content, with a note on what differs. These need excerpts from approved material.
- **Calibration.** Run the council on three to five pieces with known scores, look for
  leniency or scores bunched in one band, and adjust the band descriptions.
- **Test the modules' scores.** The lecture module hasn't been run. For the lab module, seed
  defects into a lab that's otherwise clean on the targeted criterion, run each condition at
  least twice, and include a lab that has real troubleshooting notes.
- **Rubrics for content outlines and whole courses.** Both use the core alone for now, which
  leaves many criteria `cannot_assess` for an outline and judges a course's sequence only through
  progression and practice design.
- **Assessment, code, and UI modes.**
