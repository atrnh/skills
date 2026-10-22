---
name: create-mcq
description: >
  Generates multiple choice questions (MCQs) from text or documents provided by the user.
  Use this skill whenever the user asks to "generate MCQs", "generate multiple choice questions",
  "create a quiz", "make quiz questions", "write test questions", or anything similar — even if
  they don't use those exact words. Also trigger when a user shares a document, article, URL, or
  block of text and wants comprehension questions, study questions, or an assessment created from
  it, even if they haven't explicitly said "MCQ". When in doubt, trigger this skill.
---

## Step 1: Read the source material

Determine where the content is coming from and extract the text:

- **Plain text** pasted into the conversation → use it directly
- **PDF file** → use the `Read` tool on the file path
- **Word document (.docx)** → use the `Read` tool on the file path
- **URL or web page** → use the `WebFetch` tool to retrieve the page content

If no source material has been provided, ask for it before proceeding.

## Step 2: Confirm parameters

Use these defaults unless the user specifies otherwise — don't ask unless something is genuinely ambiguous:

- **Number of questions**: 5
- **Output format**: Markdown (`.md`); also supported: reStructuredText (`.rst`), Word document (`.docx`)
- **Output filename**: `mcqs.md` (or `mcqs.rst` / `mcqs.docx` to match the format)

## Step 3: Generate the MCQs

### Writing the stem

The stem is the question or problem statement. A well-written stem:

- **Tests one important concept** — focus on a "take-home message" from the source, not trivia or minutiae
- **Is self-contained** — a well-prepared reader should be able to formulate an answer before seeing the choices; if they can't, the stem is underspecified
- **Is concise** — include only the information needed to pose the problem; extra context ("window dressing") increases reading load without testing more knowledge
- **Uses positive phrasing** — avoid negative constructions like "which of the following is NOT…" or "EXCEPT"; these test test-taking skill more than content knowledge. If negative phrasing is genuinely necessary, capitalize the negative word (NOT, EXCEPT) to make it visible
- **Avoids passive voice, idioms, and absolute terms** ("always", "never") — these introduce ambiguity and can disadvantage readers unfamiliar with the phrasing
- **Is a complete question**, not an incomplete sentence that the answer choices must finish — complete-question stems prevent grammatical cuing

### Writing the answer choices

Write 4 answer choices (A, B, C, D) unless the material or user requests otherwise. Exactly one must be the single best answer.

**Parallel construction** — All options must match in grammar, length, complexity, and style. A reader should not be able to identify the correct answer because one option looks different. Specifically:
- Use the same grammatical form across all options (all noun phrases, all full sentences, all verb phrases, etc.)
- Keep lengths comparable — the correct answer must not be noticeably longer, more detailed, or more qualified than the distractors
- Use consistent verb tense, voice, and level of specificity
- Move repeated words or phrases into the stem rather than repeating them in every choice

**Ordering** — List options in a logical sequence: alphabetical for text, ascending for numbers, chronological for dates. Vary which letter holds the correct answer across the question set so it isn't always A or B.

**Distractors** — The incorrect options should be plausible to someone with only partial knowledge of the topic. Good distractors:
- Reflect common misconceptions or near-miss confusions about the material
- Are clearly wrong on reflection, but not obviously wrong at first glance
- Are independent of each other — overlapping distractors let test-takers eliminate options through logic rather than knowledge

**Avoid:**
- "All of the above" — allows partial knowledge to suffice and makes the item easier to game
- "None of the above" — shifts the task from identifying the best answer to detecting errors
- Joke or absurd options — they reduce distractor plausibility and make the correct answer easier to find by elimination
- Absolute terms in distractors ("always", "never") — experienced test-takers learn to eliminate these

### Cognitive level

Aim for variety across questions. When the source supports it, go beyond simple recall and include questions requiring:
- **Comprehension** — explaining a concept or mechanism in different terms
- **Application** — using a fact or principle to evaluate a scenario
- **Analysis** — distinguishing between similar concepts or identifying causes

Spread questions across different parts of the source rather than clustering on one section.

### Writing the explanations

For each choice, write a brief explanation of why it is correct or incorrect. Explanations should:
- Be similarly concise across all options — avoid giving the correct answer a noticeably longer explanation
- Reference the specific reasoning or fact from the source, not just restate the answer
- For distractors, name the specific misconception or confusion the option is designed to surface

## Step 4: Write the output file

### Markdown (`.md`)

```markdown
## Question 1

[Stem]

**Correct answer: A**

| Letter | Answer | Explanation |
|--------|--------|-------------|
| A | [text] | [explanation] |
| B | [text] | [explanation] |
| C | [text] | [explanation] |
| D | [text] | [explanation] |
```

Separate questions with `---`.

---

### reStructuredText (`.rst`)

```rst
Question 1
----------

.. mcq:: [Stem]
   :numbered:
   :answer: A

   A. [text]

      :feedback: [explanation]

   B. [text]

      :feedback: [explanation]

   C. [text]

      :feedback: [explanation]

   D. [text]

      :feedback: [explanation]
```

---

### Word document (`.docx`)

Generate a JSON file of the MCQ data, then run the bundled script to produce the `.docx`.

**JSON format** — save as `/tmp/mcqs.json`:

```json
{
  "title": "MCQ Set",
  "questions": [
    {
      "number": 1,
      "stem": "Question text here",
      "correct_answer": "A",
      "answers": [
        {"letter": "A", "text": "Answer text", "explanation": "Why correct or incorrect"},
        {"letter": "B", "text": "Answer text", "explanation": "Why correct or incorrect"},
        {"letter": "C", "text": "Answer text", "explanation": "Why correct or incorrect"},
        {"letter": "D", "text": "Answer text", "explanation": "Why correct or incorrect"}
      ]
    }
  ]
}
```

**Run the script:**

```bash
python "${CLAUDE_SKILL_DIR}/scripts/create_word_doc.py" /tmp/mcqs.json output.docx
```

If `python-docx` is not installed: `pip install python-docx`

## Step 5: Confirm

Tell the user the output filename, format, and number of questions generated.
