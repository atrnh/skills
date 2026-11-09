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

Quote only from the artifact and context files the review lists, by their absolute paths. When
the problem is something missing, such as an unstated prerequisite or a step with no
instructions, quote the place where it belongs, such as the step that needs it or the heading of
its section, and add `missing` to the evidence item to say what you looked for and didn't find.

## Combining scores

The script reads the review's files from `sources.json` and checks every review:

- A review counts only if it's a JSON object with a list of scores and at least one valid
  answer. The council needs three that count. With fewer, the run is invalid: the script still
  writes `scores.json` for diagnosis, but with no score and the verdict `invalid`.
- An answer counts only if it names a known criterion and has an allowed value: a whole number
  from 1 to 10, `"na"`, or `"cannot_assess"`. Anything else is reported and left out.
- A numeric score also needs at least one evidence item whose quote appears in a listed file.
  Whitespace differences are ignored. The check confirms the quote's location, not that it
  supports the score; judging that is the chair's work.
- Criteria a reviewer left out, a reviewer ID that doesn't match the panel, a reading log
  without three to six entries, and rejected evidence are reported as problems. A short reading
  log doesn't drop any scores, but it suggests the reviewer skimmed.

Then, for each criterion:

- If more than half the reviewers who answered said `"na"`, the criterion is not applicable and
  is left out of the score.
- Otherwise, the criterion is scored when at least two valid numeric scores make up at least
  half of the reviews that count. Its score is their median, and its spread is the highest
  score minus the lowest.
- Otherwise, the criterion is insufficient. It applies, but too few reviewers could judge it.

The script flags a criterion for the chair to adjudicate when:

- **bands:** two scores fall in bands that aren't adjacent, such as Weak and Strong;
- **gate:** a gate criterion has scores both below 7 and 7 or higher;
- **failing:** scores fall both at or below 3 and above it;
- **applicability:** some reviewers said `"na"` and others gave a number.

A wide spread within neighboring bands, such as 6 and 8 on a criterion that isn't a gate, isn't
flagged.

## Council score

The **council score** is the mean of the scored criteria's medians, rounded to two decimal
places, from 1 to 10. It's given only when the run is complete: every applicable criterion is
scored, and no gate is `"na"`. Otherwise it's empty, and the **partial score**, the same mean
over whatever was scored, is there for diagnosis only. Two runs are comparable only when both
are complete and apply the same criteria. The decimals don't mean the measurement is that
precise.

## Verdict

Some criteria are gates. They matter so much that a weak result fails the material however well
it does elsewhere. Each mode's rubric marks its gates. The script decides in this order:

1. **Not ready:** a gate's median is below 7, or any criterion's median is 3 or lower.
2. **Incomplete:** an applicable criterion is insufficient, or a gate is `"na"`.
3. **Ready:** every scored criterion's median is 7 or higher.
4. **Revise:** anything else.

The **final verdict** is the same, except that it's **not ready** whenever the chair has
recorded a blocker in `blockers.json`. A blocker is a priority 1 finding that the chair has
confirmed against the artifact. It overrides the verdict, but never changes a score.
