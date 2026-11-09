---
name: review-council
description: >
  Use in T3 Code when the user wants a council, panel, or multi-model review of an artifact:
  independent reviewers from different model families score it against a shared rubric while
  this session chairs the review and combines their results. Curriculum mode reviews lectures,
  labs, exercises, assessments, content outlines, and whole courses. Produces a scored report and
  a scores file that an improvement loop can use as its measurement, and can hand the findings to
  the triage-feedback dashboard. Do NOT use outside T3 Code, for a single-agent review, or for
  code or UI designs until those modes exist.
---

# Review council

A council is a set of reviewers from different model families who score one artifact against
the same rubric without seeing each other's work. Their agreement is evidence, and so is their
disagreement. You chair the council: you set up the review, brief every reviewer identically,
check their evidence, and combine their scores. You don't score the artifact yourself.

The council needs T3 Code's orchestration tools. Call `orchestrator_capabilities` first. If it
isn't available, tell the user the council runs only in T3 Code and stop.

## Modes

| Mode | Reviews | Rubric |
| --- | --- | --- |
| Curriculum | Lectures, labs, exercises, assessments, content outlines, and courses | [modes/curriculum.md](references/modes/curriculum.md) |

Code and UI modes aren't written yet. If the user asks for one, say so instead of improvising a
rubric.

## Run folder

Each review gets a run folder, `/tmp/review-council/<slug>/` by default. When the council will
measure the same artifact repeatedly, as in an improvement loop, put it somewhere that lasts and
keep it out of the artifact's repository.

| File | Holds |
| --- | --- |
| `context.md` | The artifact, its audience and purpose, and the review's scope |
| `panel.json` | The reviewers and their settings |
| `brief.md` | The brief every reviewer receives, with `{{REVIEWER_ID}}` left in place |
| `source/` | Text versions of the artifact, when it isn't already plain text |
| `reviews/<id>.json` | Each reviewer's result, as returned |
| `scores.json` | Combined scores, written by `scripts/aggregate.py` |
| `report.md` | The council's report |

## 1. Establish what's under review

1. **Find the artifact.** It may be files, a folder, or pasted text. Reviewers start with no
   history, so refer to every file by absolute path.
2. **Give every reviewer the same text.** Save pasted text verbatim in `source/`. Convert Word,
   PowerPoint, and PDF files to Markdown in `source/`, using the extract-office-content skill if
   it's installed. Reviewers then read identical text, and the script can check their quotes.
3. **State the audience and purpose.** Take them from the course outline, a README, or the user.
   Reviewers judge fit and progression against this statement, so they must all receive the
   same one. If you can't tell who the learners are and the answer would change the scores, ask.
4. **Set the scope** using the mode's scope guidance. For a large course, name the units to read
   in depth.

Write all of this to `context.md`.

## 2. Build the panel

If the user points to an earlier run's `panel.json`, reuse its reviewers and settings
unchanged and go on to step 3.

Otherwise, choose one reviewer per model family, up to five, from the providers whose
`displayName` is "Cursor" or "Work" in `orchestrator_capabilities`. Look them up by display
name, because their `providerInstanceId` can differ from it. The capability list is short and
omits models, so use its `search` argument to look for families it may hide.

- **Group models by family** using the model ID: `claude` is Anthropic, `gpt` is OpenAI,
  `gemini` is Google, `composer` is Cursor, `grok` is xAI, and so on. Treat `default` or Auto as
  no family.
- **Pick each family's most capable current model.** When the same family is on both providers,
  choose the stronger model, whichever provider it's on.
- **If more than five families are available,** keep the five whose best models read most
  carefully, and tell the user which you left out.
- **Set each reviewer's reasoning to `high`.** The option's ID varies by model, such as
  `effort`, `reasoningEffort`, `reasoning`, or `reasoning_effort`. Turn fast mode off where it
  exists. Leave other options at their defaults.
- **Use at least three families.** With fewer, tell the user and ask whether to continue.

Write `panel.json`, using the family as each reviewer's ID:

```json
{
  "reviewers": [
    {
      "id": "openai",
      "provider": "Work",
      "providerInstanceId": "codex",
      "model": "gpt-6.1-sol",
      "options": {"reasoningEffort": "high"}
    }
  ]
}
```

## 3. Brief the reviewers

Fill in [reviewer-brief.md](references/reviewer-brief.md) to make `brief.md`, following the
instructions at its top. Every reviewer receives the same text except its own ID.

Start one `delegate_task` per reviewer, all before you wait on any:

- `task`: `brief.md` with `{{REVIEWER_ID}}` replaced by the reviewer's ID.
- `target`: the reviewer's `providerInstanceId`, `model`, and `options`.
- `role: "review"`, `isolation: "shared"`, `mode: "async"`, and the title
  `Council <slug>: <id>`.

Add each `taskId` to its reviewer in `panel.json`. Then follow each task's `next` guidance to
wait for results. Don't poll.

## 4. Collect and score

Each reviewer ends with one JSON object. Save it to `reviews/<id>.json` as returned. If its JSON
is malformed, repair only the syntax, never the content. A reviewer that fails, times out, or
returns something unusable counts as missing. Don't replace it. Continue with at least three
reviews and note the gap in the report. With fewer than three, stop and tell the user.

Then combine the scores:

```bash
python3 <this skill>/scripts/aggregate.py RUN --mode <this skill>/references/modes/curriculum.md
```

The script follows [scoring.md](references/scoring.md). It checks that every reviewer scored
every criterion and that each score quotes text that exists in the cited file. It drops scores
that fail these checks, lists them, and writes `scores.json`. Don't edit `scores.json` by hand.

## 5. Adjudicate and merge

**Disagreements.** For each criterion the script flags, read the passages each side cited and
decide which reading of the artifact holds up. Record your ruling and its reasons in the report.
Rulings explain the spread. They don't replace the scores.

**Findings.** Merge findings that describe the same problem at the same place into one, and name
every reviewer who raised it. A finding raised by several families is strong evidence, but one
raised by a single reviewer can still be right. Check each finding against the artifact as the
triage-feedback skill describes: drop findings whose quoted text doesn't exist, and begin a
finding you can't confirm with "Unverified:". Give each merged finding an ID made of its
criterion code and a number, such as `AC1` or `PR2`, and a priority. Priority 1 breaks the
material or misleads learners, 2 noticeably hurts it, and 3 is polish.

## 6. Report

Write `report.md` with:

1. **Verdict.** The verdict and council score from `scores.json`, and the single biggest thing
   holding the artifact back.
2. **Scores.** A table with a row per criterion and a column per reviewer, plus the median and
   spread. Mark gate criteria and disagreements.
3. **Disagreements.** Each flagged criterion, what each side cited, and your ruling.
4. **Findings,** in priority order. Give each one's ID, location, problem, suggested fix, and the
   reviewers who raised it.
5. **Strengths** reviewers cited, so the author knows what to keep.
6. **Panel.** Each reviewer's provider, model, and settings, plus any missing reviewers and
   dropped scores.

Reply with the verdict, the council score, the top three findings, and the report's path.

## 7. Hand off

- **Triage dashboard.** If the user asked for one, follow the triage-feedback skill, with one
  card per merged finding that has a location. Use the merged IDs, and the criterion names as
  categories. If they didn't ask, end your reply with a one-line offer.
- **Improvement loop.** A loop that uses the council as its measurement needs the same
  measurement each time. Reuse the run's `panel.json` and `brief.md` unchanged. Check that the
  mode file's version matches `rubricVersion` in `scores.json`. The metric is `councilScore`,
  where higher is better, and `verdict` and the gate criteria act as a floor. Reviewers' scores
  vary between runs, so score the unchanged artifact more than once to learn how much they vary
  before trusting any single change.
