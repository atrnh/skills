# Scoring

The "Scale" and "Evidence" sections go to every reviewer. The rest describes how
`scripts/aggregate.py` combines their scores, so keep the two in step when either changes.

## Scale

Score each criterion from 1 to 10 in two steps. First choose the band whose description fits
the material. Each mode's rubric describes the bands for every criterion; use these general
meanings when a case falls between its descriptions. Then choose a score within the band: its
top when the band's problems are few or minor there, and its bottom when they're many or close
to the band below.

| Band | Scores | Meaning |
| --- | --- | --- |
| Strong | 9–10 | The material fully serves its audience on this criterion. |
| Sound | 7–8 | Minor problems that don't get in the way of the material's purpose. |
| Weak | 4–6 | Problems that noticeably hurt the material or would mislead some of its audience. |
| Failing | 1–3 | The problems block the material's purpose, or the quality is missing entirely. |

Two other answers are allowed:

- `"na"` when the criterion doesn't apply to this artifact, such as practice design for a
  lecture with no practice. Missing something the artifact needs isn't `"na"`. Score that low.
- `"cannot_assess"` when you can't judge the criterion from what you can read, such as
  accuracy that depends entirely on software you can't run. Say what you would need.

## Evidence

Every numeric score must cite the text it rests on. For a low score, quote the problem. For a
high score, quote what earns it. Explain in the rationale why the score falls in its band, and
why it sits where it does within the band.

## Combining scores

The script first checks every review:

- A score counts only if its value is allowed and, for a number, at least one of its quotes
  appears in the cited file. Whitespace differences are ignored.
- Scores for unknown criteria, and criteria a reviewer left out, are reported as problems.

Then, for each criterion:

- If more than half the reviewers who answered said `"na"`, the criterion is not applicable and
  is left out of the council score.
- Otherwise, with at least two valid numeric scores, the criterion's score is their median. The
  spread is the highest score minus the lowest. When two scores fall in bands that aren't
  adjacent, such as Weak and Strong, the reviewers disagree about what the material is, and the
  chair adjudicates. A wide spread within neighboring bands, such as 6 and 8, isn't flagged.
- With fewer than two valid numeric scores, the criterion is insufficient and is left out of the
  council score.

The **council score** is the mean of the scored criteria's medians, rounded to two decimal
places. It runs from 1 to 10.

## Verdict

Some criteria are gates. They matter so much that a weak result fails the material however well
it does elsewhere. Each mode's rubric marks its gates.

- **Not ready:** a gate's median is below 7, or any criterion's median is 3 or lower.
- **Ready:** every gate is scored, and every scored criterion's median is 7 or higher.
- **Revise:** anything else, including a gate that is insufficient.
