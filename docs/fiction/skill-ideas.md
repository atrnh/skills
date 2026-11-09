# Fiction skill ideas

Working notes from the September 15, 2026 discussion. These capture ideas to return
to before implementation. Names, boundaries, and behaviors are provisional. No
prototype, storage format, or new skill has been approved by these notes.

## Starting point

The repository already has `story-bible`, `developmental-editor`, and `line-editor`
skills, with a shared [editorial contract](../../skills/fiction/references/editorial-contract.md).
New skills should reuse that contract, preserve author authority, and distinguish
manuscript evidence from decisions, plans, possibilities, and interpretations.

The two main ideas are an adaptive story interview and a graph for exploring and
tracking plot structure. The graph proposal has its own
[story-map notes](story-map.md).

## Engineering inspiration

We read these connected Matt Pocock skills and templates:

- [grill-with-docs](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md)
  combines `grilling` and `domain-modeling`.
- [grill-me](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md)
  invokes `grilling`.
- [grilling](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md)
  organizes questions around dependencies between decisions. Each round asks the
  questions whose prerequisites are settled, provides recommended answers, then
  uses the answers to determine the next round. Its completion condition is an
  exhausted decision tree.
- [domain-modeling](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md)
  challenges fuzzy terminology, tests concrete scenarios, compares statements with
  the code, and records settled definitions and selected consequential decisions.
- [CONTEXT-FORMAT](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/CONTEXT-FORMAT.md)
  favors concise definitions and preferred terminology.
- [ADR-FORMAT](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/ADR-FORMAT.md)
  preserves a decision and its reasoning briefly, adding detail only when useful.

These describe the sources as read during the discussion; upstream files may change.
The useful transfers are adaptive questions, concrete hypothetical situations, and
durable memory of decisions. Fiction needs different treatment of ambiguity,
competing meanings, and when to stop asking questions.

## Grill-my-story

An interview skill for a premise, character problem, scene, or vague dissatisfaction.
It reads relevant material and pursues questions that help the author discover what
they mean or test a choice they are considering.

### Two attitudes

- **Explore:** draw out interests, images, contradictions, and possibilities when
  the author does not yet know what they want.
- **Pressure-test:** examine motivation, consequences, causality, and intended
  reader experience when the author wants a choice challenged.

Infer the approach from the request when possible rather than requiring a setup
questionnaire. These can be behaviors within one skill.

### Proposed conversation behavior

- Ask one substantial question at a time by default. Group questions only when
  they belong together.
- Follow the answers rather than marching through a generic questionnaire.
- Explain why a difficult question matters to a choice or reader effect.
- Read before asking; do not ask the author to repeat available facts.
- Avoid supplying a preferred answer immediately. Offer alternatives when the
  author is stuck or requests them.
- Accept intentional uncertainty. Distinguish a mystery worth preserving from a
  missing decision that blocks the work.
- Stop when the author has enough to write or decide. Do not require a completely
  specified story or resolve every branch.
- When capture is requested, use the story bible to record decisions. Keep
  possibilities, abandoned experiments, and commitments distinct.

Example starting claim:

> She betrays her sister because she values justice more than family.

A useful question might ask whether she has previously accepted a personal loss
for justice, to explore whether the betrayal expresses a lived conviction or a
justification she invents afterward. The next question follows the author's answer.

Occasionally preserve creative rationale as well as a decision:

> Keep the mother's motives unresolved. The daughter's inability to know her is
> part of the intended grief.

That rationale helps later editorial passes protect a deliberate choice. It does
not require importing engineering document conventions.

Guiding principle:

> Pursue the questions that matter to the author's story. Be willing to challenge
> an answer, and be equally willing to preserve a mystery.

## Worldbuilding-through-consequences

Take an invented fact and explore what living with it entails. This can apply to
magic, technologies, institutions, family customs, or social rules in a realistic
setting. Follow consequences relevant to the story rather than filling an encyclopedia.

For example, “memories can be sold” leads to questions about whether sellers lose
the memory, whether someone can sell a memory of committing a crime, and whose
ordinary work becomes difficult because this is possible.

Preserve competing definitions and who uses them. A government, religious order,
and grieving parent may mean different things by “resurrection.” A single preferred
term may erase something important to the fiction.

This could begin as a focused invocation of `grill-my-story`. A separate skill is
justified if it develops a substantially different process.

## Other candidates

| Candidate | Purpose | Distinctive result or boundary |
| --- | --- | --- |
| `character-hot-seat` | Put a character in situations that expose what the author does not yet understand. | Hypothetical choices test self-image, desire, loyalties, and contradictions. The author answers as author or character; the model does not invent authoritative answers. Could begin within `grill-my-story`. |
| `follow-the-change` | Explore the consequences of a revision, such as moving a revelation earlier. | A grounded account of affected scenes, character knowledge, motives, and reader expectations. A strong next candidate because the story bible already tracks relevant distinctions. |
| `try-the-scene` | Compare ways to realize a scene or beat. | Brief alternative beats, or sample prose when requested, with their effects compared. Experiments remain outside canon. |
| `unstick-me` | Investigate why the author keeps avoiding a scene or cannot move forward. | A short diagnostic conversation ending in a manageable writing experiment. May reveal an unwanted scene, missing decision, or obsolete constraint. |
| `track-the-reveal` | Examine when readers know, suspect, or reinterpret something. | A sequence of reader knowledge and expectations, separate from character knowledge. Could begin as a focused developmental-edit request. |

Separate skills should earn their place through distinct working methods rather
than different names for the same interview or editorial pass.

## Suggested first experiments

For `grill-my-story`, use a short instruction set on an actual unresolved story
choice. Evaluate whether its follow-up questions produce discoveries a generic
worksheet would miss, without steering the author toward the model's preferred story.

For the graph idea, see the bounded [story-map prototype proposal](story-map.md#proposed-first-prototype).

## Open decisions

- Final names and which candidates deserve standalone skills.
- How interviewing hands off to story-bible capture in the author's workflow.
- How to preserve useful creative rationale without accumulating administrative work.
- Whether real use supports one-question interviews as the default.
- Which experiment to run first and what story material to use.
