# Lecture Style Guide

The authoritative style guide for lecture content in this curriculum. Read
this before generating any lecture content---the Do/Don't examples are
especially important for calibrating the correct register.

## Contents

- [Publication Formats](#publication-formats)
- [Page Structure & Anatomy](#page-structure--anatomy)
- [Tone & Voice](#tone--voice)
  - [Register](#register)
  - [Pronouns](#pronouns)
  - [Stance Toward the Reader](#stance-toward-the-reader)
  - [Hedging vs. Directness](#hedging-vs-directness)
- [Content Progression Pattern](#content-progression-pattern)

---

## Publication Formats

Lectures are distributed in two formats:

- **Instructor-facing lecture slides** — used by instructors in the classroom
  while presenting the material
- **Student-facing lecture handouts** — contain the same information as the
  slides, plus sidebar content (callouts with additional context and/or
  examples)

---

## Page Structure & Anatomy

Every lecture follows the same skeleton:

- Intro
- [Optional subsections]
- Goals
- [Topic section 1]
  - [Subsection]
  - [etc.]
- [Topic section N]
- Looking Ahead
- Further study
  - Self-study and reference docs
- Coming up...
  - [Describe next lab or lecture relevant to the topic]

---

## Tone & Voice

### Register

Instructional and accessible---never academic or dry, never casual or slangy.
The writing is clear enough for a reader encountering a concept for the first
time, yet substantive enough to treat them as a developing professional.

Accessible means making complex ideas approachable without oversimplifying
them. The primary tools are analogy, inline definition, and concrete example.
When a new term appears, define it on the spot---in the same sentence or the
next. When an abstract mechanism needs explaining, reach for a familiar
comparison before the formal description: a database migration becomes
immediately graspable when framed as "version control, but for your schema."

Instructional means sequencing ideas so they build on each other, motivating
each concept before introducing it, and giving the reader just enough to act
before adding complexity. Instructions are direct and specific---imperative
constructions with concrete verbs, no unnecessary hedging.

**Do:**

- "Think of migrations like version control, but for your database schema."
- "Let's say you train a simple LM on text from Green Eggs and Ham. Green Eggs
  and Ham is our model's corpus---the body of text used to train a model."
- "Don't forget to call SaveChanges to persist changes to the database!"

**Don't:**

- "Migrations constitute a versioned sequence of schema transformation
  operations that enable deterministic propagation of structural database
  modifications."
- "After selecting an appropriate training corpus---the complete body of text
  used for model training---the practitioner can proceed with the language
  model training process."
- "The SaveChanges method should be invoked in order to ensure that all pending
  modifications are persisted to the database."

---

### Pronouns

First-person plural ("we", "our") is the default voice, creating a
collaborative atmosphere. The perspective is that of an instructor working
through the material alongside the reader---not presenting to them.

"We" works best when exploring, reasoning, or building together: "we'll need to
create an initial migration" and "let's go over the steps you'd follow" both
pull instructor and reader into the same task. "You" and "your" are appropriate
when addressing the reader's specific situation or actions.

Third-person constructions---"the developer," "developers should," "one
must"---signal a textbook register that puts distance between the writing and
the reader. Even when the subject is technically "the developer," the lecture
means *you*.

**Do:**

- "To take advantage of EF Core's ORM features, we need to define our DB
  tables as model classes."
- "We'll need to create an initial migration to set up the database."

**Don't:**

- "In order to use EF Core's ORM features, the developer is required to define
  database tables as model classes."
- "The developer will need to create an initial migration to set up the
  database."

---

### Stance Toward the Reader

Address readers as developing professionals, not students memorizing facts; the
voice is mentoring rather than authoritative. The reader has a goal---building
real software---and the lecture serves that goal.

Mentoring means anticipating where readers are likely to stumble and flagging
it before they do---"this will work, but you might forget to keep all three
values in sync"---rather than presenting facts and leaving pitfalls to be
discovered. It also means motivating concepts before introducing them: a reader
who understands why something matters will retain it far better than one who is
handed a rule to memorize.

Frame content as professional practice wherever possible. Trust the reader's
existing knowledge---"Models are just normal classes, so you can add your own
methods to them" assumes competence and extends it. Over-explaining what the
reader likely already knows signals a lack of trust.

**Do:**

- "This will work, but you might forget to keep all three values in sync. Since
  changing the color will change all three values, it's better to use a single
  state value."
- "Models are just normal classes, so you can add your own methods to them!"

**Don't:**

- "Storing separate state variables for related values violates the
  single-source-of-truth principle. Developers should combine these into a
  single state variable."
- "Note that it is also possible to define additional methods within model
  classes."

---

### Hedging vs. Directness

The tone is direct in technical instructions and measured in opinion---
calibrated to the nature of the claim rather than applied uniformly.

Technical statements and instructions call for plain, confident prose. When
something is technically accurate, say it without softening. Over-hedging
erodes the signal: if everything is qualified with "generally" or "in most
cases," the reader loses the ability to tell what they can actually rely on.
Reserve hedges for the places where they're actually warranted.

When the right answer genuinely depends on context, signal that honestly. "You
might," "in some cases," and "it depends" aren't evasions---they reflect the
actual shape of the material. Use "you should" for strong recommendations; "you
might consider" or "it depends" where context varies.

**Do:**

- "A model is just a class."
- "It takes practice and experience to develop a sense for designing state!"

**Don't:**

- "A model can generally be understood as functioning similarly to a class,
  though the analogy may not hold in every context."
- "By this point you should have a thorough understanding of how to structure
  state."

---

## Content Progression Pattern

### Typical Pattern Within Sections

1. Introduce the concept (what it is, why it matters)
2. Show a concrete, minimal example
3. Expand to practical or realistic implementation

### Across the Lecture

As the lecture progresses, concepts should build on each other, starting with
simple cases and building towards advanced patterns. Problem-solution framing
is used to motivate new concepts.
