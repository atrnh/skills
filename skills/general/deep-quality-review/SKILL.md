---
name: deep-quality-review
description: >
  Reviews any written material (docs, guides, lectures, labs, READMEs, essays, proposals,
  specs, emails) for both functional quality and deep quality, using the Diátaxis theory of
  documentation quality. Use when the user asks for a "deep quality" review, a "Diátaxis
  review", or wants to know whether writing is truly excellent rather than merely correct:
  "is this actually good?", "why does this feel clunky?", "review this for flow", "does this
  serve the reader?". Also use when a draft is accurate and complete but still feels off.
  Can follow the review with a triage dashboard where the user approves or rejects each
  proposed fix, then applies the approved ones or posts them as a GitHub review.
  Do NOT use for pure proofreading, brand-voice checks, or writing new material from scratch.
---

# Deep Quality Review

Judge writing the way its reader will experience it. Functional quality is the price of
entry. Deep quality is what makes it excellent. Review both, in that order, because deep
quality depends on functional quality.

Read [references/theory.md](references/theory.md) once per session before your first review.
It explains the reasoning behind every step below.

## Core stance

- **Functional quality is measured against the world.** It is objective, and its dimensions
  are independent of each other, so check each one on its own. A failure in any one of them is
  a real defect and the reader will notice it.
- **Deep quality is judged against the human.** You can't measure it, only question it. Its
  aspects are tangled together. A break in flow is usually also a failure to anticipate the
  reader. So look for the **root cause** instead of listing five separate symptoms.
- **Deep quality depends on functional quality.** One inaccuracy or inconsistency spoils the
  whole experience. Never praise the flow of a piece that is wrong.
- **Recognise *what* is good, not only *that* it is good.** Name the specific moves that work
  so the author can repeat them.
- **Functional fixes are constraints to meet. Deep-quality fixes are inventions.** Suggest
  creative moves, like reordering, reframing, or anticipating a question, and not only
  corrections.

## Step 1: Establish the reader and their need

Before judging anything, state:

1. **Who is reading?** Their prior knowledge, context, and emotional state (anxious, rushed,
   curious, stuck).
2. **What do they need at this moment?** Place the material with the Diátaxis compass:

   | | Serves **action** (doing) | Serves **cognition** (knowing) |
   |---|---|---|
   | **Acquiring** (study) | Tutorial: a learning experience | Explanation: understanding, context, why |
   | **Applying** (work) | How-to guide: reaching a real goal | Reference: accurate facts to look up |

   For material that isn't documentation, such as a proposal, email, or essay, name the
   equivalent need. Examples: "decide whether to fund this" or "understand what changed and act".
3. **Is the material mixing modes?** Mixed modes are the most common structural cause of
   deep-quality failure.

If you can't tell who the reader is, say which reading you're assuming. If the answer would
change the review a lot, ask.

## Step 2: Functional quality (objective, check each dimension separately)

For each dimension, give findings with **location, evidence, and fix**:

- **Accuracy:** Does it match the thing it describes? Check the code, the product, and the
  facts where you can. If you can't verify a claim, mark it *unverified*. Don't guess.
- **Completeness:** Is anything the reader needs missing? Look for skipped steps, undefined
  terms, missing prerequisites, and unhandled cases.
- **Consistency:** Are terms, names, formatting, voice, and claims the same throughout?
- **Usefulness:** Does each part help this reader with this need? A piece can be accurate,
  complete, and consistent and still be useless.
- **Precision:** Is anything vague where the reader needs exact values, commands, or
  conditions? Is anything ambiguous?

**Use structure to expose hidden lapses.** Diátaxis can't supply functional quality, but it
can reveal where it's missing:

- Mentally move explanatory digressions out of task-focused sections. Where does the reader
  now have to work something out alone? That's a completeness gap the digression was hiding.
- For reference-like material, check whether its structure mirrors the structure of the
  subject. Gaps in the mirror are gaps in coverage.

## Step 3: Deep quality (subjective, judged by simulating the reader)

Read the piece **as the reader** from Step 1, in order, at their pace. Notice where you slow
down, get lost, feel talked down to, or stop trusting it. As with clothing, the body knows
whether something fits before the mind can say why. Then explain why.

Question each aspect, knowing they overlap:

- **Fitting human needs:** Does the form match the need? Is a learner handed a reference
  dump? Is a practitioner forced through a lecture? Are the arrangement, the relationships
  between parts, and the register right for each part?
- **Flow:** Does each step lead into the next in a way that feels right and unforced, and in
  step with what the reader cares about at that moment? Find the exact places where rhythm
  breaks: digressions, detours, backtracking, sudden jumps in difficulty, and walls of caveats
  before the point.
- **Anticipating the user:** Are questions answered just before the reader would ask them?
  Are likely mistakes headed off? Does the reader ever reach a fork with no guidance?
- **Feeling good to use:** Does the reader come away with confidence, momentum, and
  satisfaction? Or with friction, doubt, and effort?
- **Beauty:** Is the overall form clean and proportionate? Is there economy? Does anything
  feel bolted on?

Tie findings back to one or two root causes. Examples: "the piece is trying to be a tutorial
and a reference at once" or "it's organised around the author's mental model, not the
reader's task".

## Step 4: Report

Use this structure. Keep it tight and point to specific locations (quote a short phrase or
give a section/line).

Give every finding an ID: a letter for its kind and a number in order of appearance. The
letters are A Accuracy, M Completeness, C Consistency, U Usefulness, P Precision, and D Deep
quality, for example A1, C2, and D1. The user can then refer to findings by ID ("apply A1 and
C3"), and the dashboard uses the same IDs.

```
## Verdict
One or two sentences: does it have functional quality? Does it have deep quality? What is the
single biggest thing holding it back?

## Reader and need
Who, what state, which mode(s) it serves, and whether modes are mixed.

## Functional quality
Per dimension (skip clean ones, or say "no issues"): ID, location, problem, fix.
Mark unverified claims.

## Deep quality
A short account of the reading experience, followed by the root cause(s).
Then specific breaks: ID, location, what the reader experiences, why, and an inventive fix.

## What already works
Specific moves worth keeping and repeating.

## Revisions, in priority order
By ID:
1. Functional defects first (they spoil everything else).
2. Structural or mode fixes (they unlock flow and fit).
3. Local flow and anticipation improvements.
```

Don't rewrite the material unless asked. Building the dashboard counts as being asked, because
its replacements are proposals that change nothing until the user approves them.

If the user asked for a triage dashboard, go straight on to Step 5 after the report. If they
didn't, end the report with a one-line offer, such as: "Want a triage dashboard to approve or
reject each fix, then apply them or post them as a review?" Don't build it until they say yes.
Count any request for a dashboard, a triage page, or a way to approve or reject the fixes as
asking for it.

## Step 5: Triage dashboard

Follow [references/dashboard.md](references/dashboard.md). In short:

1. Put the review in a run folder under `/tmp/dqr-triage/`, with the exact text that was
   reviewed: a worktree at the PR's head commit, the user's checkout, the files, or pasted
   text saved to a file.
2. Write `findings.json` with one entry per report finding, using the same IDs. Each entry
   needs the exact replacement text and an honest case against making the change.
3. Build it with `dashboard/build.py --check`. Fix every error, and read every highlighted
   and replaced line.
4. Start it with `dashboard/serve.py start`, open it in the in-app browser preview if there is
   one or in the default browser if not, and tell the user how to decide.

## Step 6: Act on the decisions

When the user says they're done, read their decisions. Update any fix that a note changes
before anything else. Then ask whether to edit the files or post a GitHub review:

- **Someone else's PR:** suggest posting a review (`dashboard/review.py`). Show the draft, and
  post only after they confirm.
- **The user's own work:** suggest editing (`dashboard/apply.py`). Run it with `--dry-run`
  first, then apply, then run any validation the repository requires.

Rejected findings stay as they are. When the user is finished, stop the server and offer to
remove the run folder and any worktree.

## Limits (be honest about them)

- This framework sets up the conditions for deep quality. It doesn't guarantee it and it
  isn't a formula. Don't present a checklist pass as proof of excellence.
- Visual design, interaction design, and UX research matter too. If layout, navigation, or
  medium is the real problem, say so, even if it's outside the text.
- Deep quality keeps being reinterpreted. Trust a well-argued judgement over mechanical rules.
