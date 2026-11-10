---
name: review-council
description: >
  Use when the user wants a council, panel, or multi-model review of an artifact: independent
  reviewers from different model families score it against a shared rubric while this session
  chairs the review and combines their results. Starts reviewers through T3 Code, the host's own
  subagents, or the cursor-agent, codex, and claude CLIs. Curriculum mode reviews lectures, labs,
  exercises, homework, content outlines, and whole courses. Shares each reviewer's findings as
  they arrive, then a scored council report that other workflows, such as triage-feedback or an
  improvement loop, can take up. Do NOT use for a single-agent review, or for assessments, code,
  or UI designs until those modes exist.
---

# Review council

A council is a set of reviewers from different model families who score one artifact against
the same rubric without seeing each other's work. Their agreement is evidence, and so is their
disagreement. You chair the council: you set up the review, brief every reviewer identically,
check their evidence, and combine their scores. You don't score the artifact yourself.

The council needs a way to start reviewers on other models: T3 Code's orchestration tools, your
host's own subagents, or the `cursor-agent`, `codex`, and `claude` CLIs. Step 2 chooses among
them.

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
| `context.md` | The artifact, its place in its larger work, known and tracked gaps, its audience and purpose, the review's scope, and every file reviewers may read |
| `brief.md` | The brief every reviewer receives, with `{{REVIEWER_ID}}` left in place |
| `source/` | Fixed copies of the artifact, such as text converted from Word or a file taken from another branch |
| `reviews/` | The reviews and error logs of reviewers started through a CLI |
| `report.md` | The council's report |

## 1. Establish what's under review

1. **Find the artifact.** It may be files, a folder, or pasted text. Reviewers start with no
   history, so refer to every file by absolute path.
2. **Give every reviewer the same text.** Save pasted text verbatim in `source/`. Convert Word,
   PowerPoint, and PDF files to Markdown in `source/`, using the extract-office-content skill if
   it's installed. When the artifact is on a branch other than the one checked out, copy it from
   that branch into `source/` rather than switching the user's checkout.
3. **Check work in progress.** When the artifact is on a feature branch, look for related work
   before treating a gap as a flaw: other branches that touch the same material, open pull or
   merge requests, and open issues. Use the project's own tracker, such as GitHub with `gh` or
   GitLab with `glab`. If you can't reach it, ask the user whether known work is pending. A gap
   that an open issue, branch, or request already covers is known and tracked. List each one in
   `context.md` with its link, so reviewers leave it out of their scores and findings.
4. **Place it in its larger work,** following the mode file's "For the chair" section.
   Reviewers judge the artifact against this context, so gather it once and give them all the
   same account.
5. **State the audience and purpose.** Take them from the course outline, a README, or the user.
   Reviewers judge fit and progression against this statement, so they must all receive the
   same one. If you can't tell who the learners are and the answer would change the scores, ask.
6. **Set the scope** using the mode's scope guidance. For a large course, name the units to read
   in depth.

Write all of this to `context.md`. End it with every file reviewers may read, by absolute path,
divided into the files under review and the context files.

## 2. Build the panel

If the user points to an earlier run's report, reuse the reviewers, launchers, and settings in
its Panel section unchanged and go on to step 3.

Otherwise, read `${XDG_CONFIG_HOME:-~/.config}/review-council/settings.md` if it exists. The
setup-review-council skill writes it. Each of its lines replaces one default named below, and the
user's instructions for this review override both. Don't save a change meant for one review
unless the user asks.

**Find the models you can reach** through each launcher in the `launchers` setting. By default
that's `t3, subagents, cursor-agent, codex, claude`, in that order of preference.

| Launcher | Models it offers |
| --- | --- |
| `t3` | Call `orchestrator_capabilities`, and skip this launcher if it isn't available. Use the providers named in the `t3 providers` setting, by default any. Look them up by `displayName`, because their `providerInstanceId` can differ from it. Skip providers that are disabled or can't run child tasks. The list is short and omits models, so use its `search` argument to look for families it may hide. |
| `subagents` | The models your host's subagent tool accepts, such as Claude Code's `Agent` or Cursor's `Task` |
| `cursor-agent` | `cursor-agent models` |
| `codex` | `codex debug models`, which prints the catalog as JSON |
| `claude` | No list command. It accepts aliases such as `opus` and `sonnet` for the latest model of each line. |

Skip a CLI that `command -v` doesn't find. Then choose one reviewer per model family:

- **Group models by family** using the model ID: `claude` is Anthropic, `gpt` is OpenAI,
  `gemini` is Google, `composer` is Cursor, `kimi` is Moonshot, and so on. Treat `default`,
  `auto`, `inherit`, and other aliases as no family.
- **Leave out** the families in the `skip families` setting, by default none.
- **Seat pinned families first.** A line such as `pin google: gemini-4-argon via t3 Cursor` fixes
  that family's model, launcher, and, for `t3`, provider. If a pinned model isn't available,
  tell the user and choose for that family as if it had no pin.
- **Pick each other family's most capable current model.** When several launchers or providers
  offer the family, choose the strongest model wherever it is. When they offer the same model,
  start it through the launcher listed first.
- **If more families are available than the `most reviewers` setting allows,** by default five,
  keep the ones whose best models read most carefully, and tell the user which you left out.
- **Set each reviewer's reasoning** to the `reasoning` setting, by default `high`, or to the
  model's highest level below it. Turn fast mode off unless the `fast mode` setting is `on`.
  Leave other options at their defaults. Step 3 shows how each launcher takes these settings.
- **Use at least three families.** With fewer, tell the user and ask whether to continue.

Use each reviewer's family as its ID, such as `openai` or `google`.

## 3. Brief the reviewers

Fill in [reviewer-brief.md](references/reviewer-brief.md) to make `brief.md`, following the
instructions at its top. Every reviewer then gets the same task:

> You are a reviewer on a review council. Your reviewer ID is `<id>`. Read
> `<run folder>/brief.md` in full and follow it exactly, using `<id>` wherever it says
> `{{REVIEWER_ID}}`. In the run folder, read only the files the brief lists.

Start every reviewer before you wait on any.

**Through `t3`,** call `delegate_task` with that `task`, a `target` holding the reviewer's
`providerInstanceId`, `model`, and `options`, `role: "review"`, `isolation: "shared"`,
`mode: "async"`, and the title `Council <slug>: <id>`. The reasoning option's ID varies by model,
such as `effort`, `reasoningEffort`, `reasoning`, or `reasoning_effort`.

**Through `subagents`,** start your host's subagent tool with the task and the reviewer's model,
in the background or in parallel where the tool allows it. When the tool can't take a setting,
such as reasoning, record that in the report's Panel section.

**Through a CLI,** create `reviews/` in the run folder. Run each command in the background from
the artifact's repository root, or from the run folder when there's no repository, without a
timeout that would cut a long review short. Each command keeps its reviewer read-only and saves
the review in `reviews/`:

```sh
cursor-agent -p --trust --mode ask --model '<model>' --add-dir '<run folder>' '<task>' \
  > '<run folder>/reviews/<id>.md' 2> '<run folder>/reviews/<id>.log'

codex exec -s read-only --ephemeral --skip-git-repo-check -m '<model>' \
  -c model_reasoning_effort='"<reasoning>"' -o '<run folder>/reviews/<id>.md' '<task>' \
  > /dev/null 2> '<run folder>/reviews/<id>.log'

printf '%s' '<task>' | claude -p --model '<model>' --effort '<reasoning>' \
  --tools Read,Grep,Glob --add-dir '<run folder>' \
  > '<run folder>/reviews/<id>.md' 2> '<run folder>/reviews/<id>.log'
```

- `cursor-agent` sets reasoning and fast mode through the model name. Choose the variant ending
  in the reasoning level, such as `claude-opus-5-5-high`, and with fast mode off, the one without
  `-fast`.
- `claude` takes several values after `--add-dir` and `--tools`, so the task goes in on standard
  input.
- Give `cursor-agent` and `claude` another `--add-dir` for each folder outside the repository
  and the run folder that reviewers must read.

Tell the user who is on the panel, then wait. Follow each T3 task's `next` guidance without
polling, and wait on subagents and CLI processes the way your host provides.

## 4. Share each review as it arrives

When a reviewer finishes, read its result and share it with the user right away, without
waiting for the others. A T3 reviewer's result comes from `task_status`, a subagent's from its
final message, and a CLI reviewer's from `reviews/<id>.md`. Share:

- The reviewer, its model, and its scores on one line.
- Its summary, and its priority 1 and 2 findings, each in a sentence with its location.

Check that the review answers every criterion, and note any score with no evidence. These are
one reviewer's views. Say so, and keep the council's judgment for the report.

A reviewer that fails, times out, or returns something unusable counts as missing. For a CLI
reviewer, that includes exiting with an error or leaving `reviews/<id>.md` empty; its
`reviews/<id>.log` says why. Don't replace it. With fewer than three usable reviews, stop and
tell the user rather than reporting a council result.

## 5. Combine, adjudicate, and merge

When every reviewer has finished, combine their scores by the rules in
[scoring.md](references/scoring.md): each criterion's median, its flags, the council score, and
the verdict.

**Evidence.** Check the quotes behind every score that decides the verdict, such as gate scores
below 7, and behind every finding you report. Search the cited file for each one. Leave out a
score whose quotes aren't there, and say so. Then check that the passages support the score.

**Disagreements.** For each flagged criterion, read the passages each side cited and decide
which reading of the artifact holds up. For an applicability flag, decide whether the criterion
applies. Record your ruling and its reasons in the report. Rulings explain the spread. They
don't replace the scores.

**Findings.** Merge findings that describe the same problem at the same place into one, and name
every reviewer who raised it. A finding raised by several families is strong evidence, but one
raised by a single reviewer can still be right. Check each finding against the artifact as the
triage-feedback skill describes: drop findings whose quoted text doesn't exist, and begin a
finding you can't confirm with "Unverified:". Drop findings about gaps that `context.md` lists as
known and tracked. Give each merged finding an ID made of its criterion code and a number, such
as `AC1` or `PR2`, and a priority. Priority 1 breaks the material or misleads learners, 2
noticeably hurts it, and 3 is polish.

**Blockers.** A median can outvote a reviewer who was right. When you've confirmed a priority 1
finding against the artifact yourself, such as a required step that can't succeed, mark it as a
blocker. The final verdict becomes not ready, and the scores and the computed verdict stay as
they were. Record only blockers you've verified, never a disagreement with the panel's judgment.

## 6. Report

Give the report in your reply and save it as `report.md`:

1. **Verdict.** The final verdict and council score, and the single biggest thing holding the
   artifact back. If a blocker changed the verdict, give the computed verdict too. If the run is
   incomplete, give the partial score, labeled as partial.
2. **Scores.** A table with a row per criterion and a column per reviewer, plus the median and
   spread. Mark gate criteria, flags, and criteria that are not applicable or insufficient.
3. **Disagreements.** Each flagged criterion, what each side cited, and your ruling.
4. **Findings,** in priority order. Give each one's ID, priority, location, problem, suggested
   fix, any replacement text you've checked, the reviewers who raised it, and whether it's
   verified or a blocker.
5. **Known and tracked.** The gaps left out because open work covers them, with their links.
6. **Strengths** reviewers cited, so the author knows what to keep.
7. **Panel.** The rubric version, and each reviewer's launcher, provider, model, and settings,
   plus any missing reviewers and dropped scores.

## 7. Hand off

When the user wants the results to go somewhere, build what's needed from the report:

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

- **Give each measurement its own run folder.** Copy `brief.md` and `context.md` unchanged, and
  reuse the panel from the first run's report.
- **Keep converted text in one place.** When the artifact needs converting or copying, keep
  those copies in one folder outside the run folders, and refresh them for each version of the
  artifact. Their paths then stay the same, and reviewers never read a stale copy.
- **Compare only comparable runs.** The metric is the council score, where higher is better, and
  the final verdict acts as a floor. Two runs are comparable only when both are complete, use
  the same panel, brief, context, and rubric version, and apply the same criteria. Only the
  material under review may change.
- **Learn the noise first.** Reviewers' scores vary between runs, so score the unchanged
  artifact more than once to learn how much they vary before trusting any single change.
  Deciding when a change is real belongs to whatever runs the loop.
