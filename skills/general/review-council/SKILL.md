---
name: review-council
description: >
  Use in T3 Code when the user wants a council, panel, or multi-model review of an artifact:
  independent reviewers from different model families score it against a shared rubric while
  this session chairs the review and combines their results. Curriculum mode reviews lectures,
  labs, exercises, homework, content outlines, and whole courses. Produces a scored report,
  structured findings that other workflows such as triage-feedback can take up, and a scores
  file an improvement loop can use as its measurement. Do NOT use outside T3 Code, for a
  single-agent review, or for assessments, code, or UI designs until those modes exist.
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
| Curriculum | Lectures, labs, exercises, homework, content outlines, and courses | [modes/curriculum.md](references/modes/curriculum.md) |

Assessment, code, and UI modes aren't written yet. If the user asks for one, say so instead of
improvising a rubric. Quizzes and tests inside curriculum are still read for how they fit the
material, but the curriculum rubric doesn't judge how well their questions are written.

## Run folder

Each review gets a run folder, `/tmp/review-council/<slug>/` by default. When the council will
measure the same artifact repeatedly, as in an improvement loop, put it somewhere that lasts and
keep it out of the artifact's repository.

| File | Holds |
| --- | --- |
| `context.md` | The artifact, its place in its larger work, its audience and purpose, and the review's scope |
| `sources.json` | Absolute paths of the files under review and the context files, which evidence must come from |
| `panel.json` | The reviewers and their settings |
| `brief.md` | The brief every reviewer receives, with `{{REVIEWER_ID}}` left in place |
| `source/` | Text versions of the artifact, when it isn't already plain text |
| `reviews/<id>.json` | Each reviewer's result, as returned |
| `blockers.json` | Confirmed blocking findings, when the chair records any |
| `scores.json` | Combined scores and input fingerprints, written by `scripts/aggregate.py` |
| `council-findings.json` | The merged findings, for any workflow the results go to next |
| `report.md` | The council's report |

## 1. Establish what's under review

1. **Find the artifact.** It may be files, a folder, or pasted text. Reviewers start with no
   history, so refer to every file by absolute path.
2. **Give every reviewer the same text.** Save pasted text verbatim in `source/`. Convert Word,
   PowerPoint, and PDF files to Markdown in `source/`, using the extract-office-content skill if
   it's installed. Reviewers then read identical text, and the script can check their quotes.
3. **Place it in its larger work,** following the mode file's "For the chair" section.
   Reviewers judge the artifact against this context, so gather it once and give them all the
   same account.
4. **State the audience and purpose.** Take them from the course outline, a README, or the user.
   Reviewers judge fit and progression against this statement, so they must all receive the
   same one. If you can't tell who the learners are and the answer would change the scores, ask.
5. **Set the scope** using the mode's scope guidance. For a large course, name the units to read
   in depth.

Write all of this to `context.md`, listing every file reviewers may read with its absolute path.
Then write `sources.json`, with the files or folders under review as `artifact` and everything
else reviewers may cite as `context`:

```json
{
  "artifact": ["/tmp/review-council/lab-2-3/source/lab.md"],
  "context": ["/path/to/course/course-outline.rst", "/path/to/course/lectures/2-2/index.rst"]
}
```

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
returns something unusable counts as missing. Don't replace it.

Then combine the scores:

```bash
python3 <this skill>/scripts/aggregate.py RUN --mode <this skill>/references/modes/curriculum.md
```

The script follows [scoring.md](references/scoring.md). It checks each review's structure and
values, and that each score quotes text that exists in a file listed in `sources.json`. It drops
answers that fail, lists every problem, and writes `scores.json` with fingerprints of every
input. Don't edit `scores.json` by hand.

- **Invalid:** fewer than three reviews count. The script exits with an error. Stop and tell the
  user, rather than reporting a score.
- **Incomplete:** an applicable criterion has too few valid scores. Report the partial score as
  diagnosis only, and say which criteria couldn't be judged and why.

## 5. Adjudicate and merge

**Disagreements.** For each criterion the script flags, read the passages each side cited and
decide which reading of the artifact holds up. For an applicability flag, decide whether the
criterion applies. Record your ruling and its reasons in the report. Rulings explain the spread.
They don't replace the scores.

**Evidence.** The script confirms only that quotes exist. For gate scores below 7, flagged
criteria, and anything that decides the verdict, check that the cited passages support the
score, and say in the report where they don't.

**Findings.** Merge findings that describe the same problem at the same place into one, and name
every reviewer who raised it. A finding raised by several families is strong evidence, but one
raised by a single reviewer can still be right. Check each finding against the artifact as the
triage-feedback skill describes: drop findings whose quoted text doesn't exist, and begin a
finding you can't confirm with "Unverified:". Give each merged finding an ID made of its
criterion code and a number, such as `AC1` or `PR2`, and a priority. Priority 1 breaks the
material or misleads learners, 2 noticeably hurts it, and 3 is polish.

**Blockers.** A median can outvote a reviewer who was right. When you've confirmed a priority 1
finding against the artifact yourself, such as a required step that can't succeed, record it in
`blockers.json` and run the script again:

```json
[{"finding": "AC1", "reason": "Step 3 fails: the command needs a flag the lab never installs."}]
```

The final verdict becomes not ready. The scores and the computed verdict stay as they were.
Record only blockers you've verified, never a disagreement with the panel's judgment.

Write the merged findings to `council-findings.json`, in priority order:

```json
[
  {
    "id": "AC1",
    "criterion": "AC",
    "priority": 1,
    "title": "Step 3's command fails",
    "problem": "The command needs a flag the lab never installs, so learners can't continue.",
    "location": {"file": "/absolute/path/to/lab.rst", "quote": "Run `deploy --prod`"},
    "suggestion": "Add the install step before step 3.",
    "replacement": "",
    "reviewers": ["openai", "google"],
    "verified": true,
    "blocker": true
  }
]
```

Keep `replacement` empty unless a reviewer proposed exact text and you've checked it. Set
`verified` to `false` for a finding you couldn't confirm.

## 6. Report

Write `report.md` with:

1. **Verdict.** The final verdict and council score from `scores.json`, and the single biggest
   thing holding the artifact back. If a blocker changed the verdict, give the computed verdict
   too. If the run is incomplete, give the partial score, labeled as partial.
2. **Scores.** A table with a row per criterion and a column per reviewer, plus the median and
   spread. Mark gate criteria, flags, and criteria that are not applicable or insufficient.
3. **Disagreements.** Each flagged criterion, what each side cited, and your ruling.
4. **Findings** from `council-findings.json`, in priority order. Give each one's ID, location,
   problem, suggested fix, and the reviewers who raised it.
5. **Strengths** reviewers cited, so the author knows what to keep.
6. **Panel.** Each reviewer's provider, model, and settings, plus any missing reviewers and
   dropped scores.

Reply with the final verdict, the council score, the top three findings, and the report's path.

## 7. Hand off

The council's results are `scores.json`, `council-findings.json`, and `report.md`. When the
user wants them to go somewhere, build what's needed from those files:

- **Use the workflow that owns the destination.** If an installed skill handles it, follow that
  skill and convert the findings into its format. Otherwise, ask the user what form they want.
- **Keep what makes the findings council findings:** their IDs, priorities, locations, whether
  they're verified or blockers, and the reviewers who raised them.
- **Leave the artifact alone** unless the user asks for fixes to be applied, whether directly or
  through a workflow that gets their approval first.

If the user didn't say where the results should go, end your reply with a one-line question
about what to do with the findings, naming one or two options that fit, such as a triage
dashboard for approving each fix.

## Measuring repeatedly

When the council measures an artifact again and again, as in an improvement loop, every run
must measure it the same way:

- **Give each measurement its own run folder.** Copy `panel.json` without its task IDs, and copy
  `brief.md`, `context.md`, and `sources.json` unchanged.
- **Keep converted text in one place.** When the artifact needs converting to text, keep the
  converted text in one folder outside the run folders, and convert into it again for each
  version of the artifact. Its paths then stay the same, and reviewers never read a stale copy.
- **Compare only comparable runs.** The metric is `councilScore`, where higher is better, and
  `finalVerdict` acts as a floor. Two runs are comparable only when both are complete, apply
  the same criteria, and have the same fingerprints for everything in `inputs` except the
  sources.
- **Learn the noise first.** Reviewers' scores vary between runs, so score the unchanged
  artifact more than once to learn how much they vary before trusting any single change.
  Deciding when a change is real belongs to whatever runs the loop.
