---
name: student-question-pass
description: Reviews curriculum material by roleplaying as a target learner, adding student questions as source comments, then interactively turning selected questions into teachable content. Use when the user asks to pretend to be a student, learner, or course participant; add questions as comments; answer questions one by one; or expand a lecture/lab based on learner questions.
---

# Student Question Pass

## Quick Start

Use this skill in two phases:

1. **Question pass**: read the target material as the specified learner persona, then add source comments immediately after passages that would raise reasonable student questions.
2. **Answer pass**: process those comments in file order. For each question, ask whether to answer or skip. If answering, brainstorm answer directions, ask the user to choose, then replace the comment with appropriate instructional content.

## Question Pass

Before editing, gather enough context to roleplay plausibly:

- Read the target file.
- If the user mentions prior units, labs, learner background, or course sequence, skim only the relevant surrounding material.
- Identify the learner's likely knowledge, confidence level, job context, and misconceptions.

Add questions as comments, not rendered content, unless the user asks otherwise.
For RST, use this format:

```rst
.. Student question: How would I know whether the uploaded file was read correctly?
   Should I ask the tool to list what it saw first?
```

Placement rules:

- Place each comment immediately after the paragraph, list, directive, or example that elicited it.
- Ask authentic learner questions, not editorial notes disguised as questions.
- Prefer questions about judgment, usage, risk, missing examples, vocabulary, and next actions.
- Avoid answering during the question pass unless the user explicitly asks for both phases at once.
- Preserve existing source formatting and conventions.

After editing, run the smallest relevant build or lint check available.

## Answer Pass

Process questions one at a time, in source order.

For each question:

1. Show the question and ask whether to answer or skip.
2. If skipped, leave the comment unchanged and move to the next question.
3. If answering, brainstorm several plausible answer directions.
4. Recommend one direction, but ask the user to choose.
5. When the user chooses, replace the question comment with rendered instructional content near the original passage.
6. Run the smallest relevant build or lint check after each edit or small batch.

For RST, choose a directive that matches the teaching purpose:

- `.. tip::` for reusable prompts, rules of thumb, or practical workflows.
- `.. note::` for conceptual clarification or extra explanation.
- `.. caution::` for common risks, failure modes, or verification warnings.
- `.. important::` for high-stakes policy, privacy, or safety guidance.

## Answer Style

Good answers should:

- Address the exact student confusion that triggered the question.
- Stay at the learner's technical level.
- Include reusable prompts, checklists, or examples when useful.
- Make judgment calls concrete: what to do, when to verify, and when to escalate.
- Avoid overloading a lecture with every possible edge case.

When replacing a comment, remove only that question comment.
Skipped questions remain as comments so an instructor can revisit them later.

## Example Answer Brainstorm

For a question like:

```rst
.. Student question: How do I know if the AI actually calculated this, or just guessed?
```

Offer options such as:

- Visible tool signals: look for labels, code steps, generated charts, or analysis mode.
- Verification test: ask for the formula or calculation steps and spot-check one result.
- Governance angle: check which modes are enabled in the approved workplace tool.

Then recommend a direction and wait for the user's choice before editing.
