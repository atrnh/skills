# Curriculum rubric: lab module

Version: 1

This review is of a lab, exercise, or homework assignment, so three more criteria apply. Score
them after the criteria above, in this order. Runnability is a gate, like accuracy and
completeness: a median below 7 means the lab isn't ready, however well it scores elsewhere.

| Code | Criterion | Gate |
| --- | --- | --- |
| RN | Runnability | yes |
| CK | Checkpoints | |
| TR | Troubleshooting and recovery | |

## Reading a lab

- Read the lab page, its solution page, and the starter and solution code. Trace each step
  against the code it changes, and keep track of the state each step leaves for the next: files,
  packages, configuration, database schema and rows, a running app, and credentials such as
  tokens.
- A lab doesn't need instructor notes or a printed time estimate. Don't mark it down for
  lacking them.

## Where a problem belongs in a lab

These rules add to the ones above. Where they differ, these hold for this lab.

- A command, code block, file or interface path, package version, or setup step that fails or
  can't be followed when learners carry it out as written belongs to **runnability**, not
  accuracy. That includes a command or option the tool doesn't accept, even when the lab spells
  it correctly elsewhere.
- A step that needs state no required earlier step produces belongs to **runnability**, such as
  a step that relies on a section the lab marks optional.
- A wrong statement about what the code does, how a tool works, or what a result means belongs
  to **accuracy**, even when every step runs. So does solution code that contradicts the lab's
  stated goal, such as a solution that skips a check the lab says it adds.
- Setup, files, accounts, or state the lab never mentions belong to **completeness**. Setup the
  lab does give, but that doesn't work, belongs to runnability.
- One defect lowers one of these three. It lowers a second only when it separately harms what
  that criterion measures. A wrong command is runnability alone. A wrong command that comes
  with a wrong explanation of what it does is runnability and accuracy.
- Whether learners can tell that a step worked belongs to **checkpoints**, not practice design.
  Practice design keeps whether the work practices the intended skill, whether there's enough
  of it, and whether it fits the time available.
- Help with failures learners are likely to hit belongs to **troubleshooting and recovery**,
  not mental models. Mental models keeps whether learners understand the thing well enough to
  reason about it.
- A failure the lab causes, because one of its steps is wrong, belongs to runnability.
  Troubleshooting and recovery judges how the lab helps when its steps are right and something
  still goes wrong.

## RN Runnability (gate)

From the starting state the lab states, in the environment it names, learners can carry out
every step as written and reach the result the lab describes. This covers setup, the state each
step leaves for the next, rerunning a step after it fails, and cleanup. Judge commands, code,
file paths, interface paths, and package versions against the starter code and the tools the
lab names.

- **Strong (9–10):** Every step would work as written from the stated starting state, setup
  included. Each step's prerequisites are produced by required steps before it. A learner who
  reruns a step or restarts the app isn't left in a broken state.
- **Sound (7–8):** Minor friction that learners at this level would get past without help, such
  as a misspelled name that the next code block spells correctly.
- **Weak (4–6):** A step fails or can't be followed as written, and learners can work out the
  fix only with effort or outside help. Or a step depends on state that a required earlier step
  doesn't produce, or a rerun fails because an earlier attempt left state behind.
- **Failing (1–3):** A required step can't succeed as written, or the stated starting state
  can't produce what a later step needs, so learners can't reach the lab's outcome.

If you can't run the steps, trace them by reading, and name what you couldn't verify in the
rationale. Answer `cannot_assess` only when every step depends on something you can't read, such
as a service the lab doesn't show.

## CK Checkpoints

After each meaningful piece of work, learners can tell whether they got it right before they
build on it. The lab says what they should see at that point, such as an output, a status code,
a response body, a page, or a database row. Where a likely wrong result would look similar, it
says how to tell them apart. It describes the finished work concretely enough to check against.
For a task learners design themselves, it says how they can check their own result, such as a
request to send and the response to expect. A solution file shows the finished work, but it
doesn't replace checkpoints along the way. A screenshot counts when the text says what to look
for in it.

- **Strong (9–10):** Every step that changes what the app does ends with an observable expected
  result, specific enough to tell success from a near miss. Learners know what finished looks
  like before they open the solution.
- **Sound (7–8):** Expected results are given for most meaningful steps. One step that later
  work doesn't build on has none, or a result is described loosely, such as "it should work".
- **Weak (4–6):** A step that later work builds on has no expected result, or several steps
  don't, so learners find out only later, or from the solution, that something went wrong. Or
  results are stated so loosely that a wrong outcome would pass, or the finished work is
  undefined.
- **Failing (1–3):** Learners have no way to tell whether any step worked short of comparing
  their code with the solution.

## TR Troubleshooting and recovery

The failures learners are likely to hit are anticipated where they'd hit them, each with the
symptom learners would see, such as an error message, a status code, or a behavior, its likely
cause, and the fix or how to find it. Likely failures include what the tools commonly produce at
that step, slips the lab's design invites, such as a service not registered or a configuration
value mistyped, and differences in learners' environments. A learner who falls behind, or breaks
their project, has a way back in, such as a checkpoint version of the code, a reset step, or a
solution for the stage they're at. A failure the lab triggers on purpose to teach something
counts as anticipated when the lab explains it.

- **Strong (9–10):** Each predictable failure is addressed at its step, with its symptom, cause,
  and fix, briefly enough that the main path stays clear. A learner stuck at any stage can
  rejoin.
- **Sound (7–8):** The most likely failures are covered, but one goes unmentioned, or a fix is
  given without the symptom that would let learners recognize when they need it.
- **Weak (4–6):** Most predictable failures go unmentioned, so learners who hit a common error
  must search elsewhere or ask for help. Or the only way back in after falling behind is the
  finished solution.
- **Failing (1–3):** Nothing anticipates any failure and nothing helps learners recover. A
  learner who goes off the path can't get back on.

Don't reward volume. A note about an unlikely failure, or one that only repeats the step, earns
nothing.

## For the chair

Everything above this heading goes to reviewers, after the core's reviewer text. This section is
for the chair alone.

- **List everything a learner works from** among the files under review: the lab page, its
  solution page, and the starter and solution code. Runnability is traced against them.
- **Give the time slot** in the placement, since practice design judges whether the lab fits it.
  Take it from the course outline, syllabus, or user, never from a time estimate in the lab.
- **Don't give reviewers house style guides** as context. A mismatch with a context file counts
  against completeness, so a formatting convention would count against readiness. Run a
  style-guide review, such as the review-lab skill, separately.
