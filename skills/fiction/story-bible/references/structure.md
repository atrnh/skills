# Story bible structure

Use this default for a new bible. For an existing collection, map these purposes to its current entries and conventions. Do not rename or move existing material merely to match the example. If its organization obstructs the task, propose a focused reorganization for the author to approve separately.

## Default organization

The tree shows how a developed bible can grow. Create only entries supported by the sources and useful to the current task. Names are defaults, not required filenames.

```text
Story bible/
├── Start here
├── Characters/
│   ├── Character index
│   └── One entry per significant character
├── Relationships/
│   └── One entry per significant relationship
├── World/
│   ├── Places
│   ├── Groups and institutions
│   └── Rules, powers, and important objects
├── Story/
│   ├── Chronology
│   ├── Plot and reveal order
│   └── Arcs and threads
└── Working notes/
    ├── Open questions
    └── Decisions and changes
```

Start with a home entry and the substantive entries the material needs. A small bible may keep several subjects under headings in one document. Split a subject into its own entry when it has enough detail to consult independently or several other entries need to link to it. Add section indexes only when they help navigation. Do not generate empty folders, placeholder pages, or character questionnaires to complete the tree.

### Start here

Include a short source-backed premise, the bible's scope, and links into the collection. Link to manuscript sources and author notes in their existing locations. Identify current manuscript versions only when the author has designated them; otherwise record the uncertainty. A newer timestamp does not establish authority.

For fiction using an existing setting, explain the applicable source-universe canon and link to documented story departures. Preserve the distinction between source canon and this story's choices on the affected claims as well.

Drafts and editorial reviews are source or feedback material with their own destinations. Link to them without absorbing or relocating them into the bible. Do not create a parallel source collection.

### Characters

Use one entry per significant character when warranted. Include only relevant, supported sections:

- Role, background, and defining traits.
- Wants, fears, motives, and constraints.
- Knowledge, beliefs, misunderstandings, and secrets at identified story points.
- Relationships and links to relevant arcs or events.

Distinguish what the character believes from what is true in the world. Attach a chapter, event, or other supported story point to changing knowledge and motives; avoid an unexplained "currently." A minor or backstory character may need only a short entry.

### Relationships

Keep brief connections on character pages. Create a relationship entry when shared history, changing trust, obligations, conflict, or power dynamics warrant independent treatment. Link both characters to that entry. Describe each person's perspective separately where they differ, and locate changes in the story.

### World

Record relevant places, groups, institutions, rules, powers, and objects. These may start as sections in a single entry and grow into separate entries or collections.

Give a shared rule or mechanism one primary home. Character and plot entries should link to it and explain its local consequences rather than restating its full definition. Distinguish a world's rule from a character's theory about that rule. Record deliberate departures from source-universe canon with their author evidence.

### Story

Keep these questions distinct, even when their answers fit in one document:

| Entry | Purpose |
| --- | --- |
| Chronology | Events in world order, including relevant backstory. Preserve uncertain dates and relative ordering rather than inventing precision. |
| Plot and reveal order | Narrative order, including when the reader encounters events or learns information. Identify planned reveals separately from those established by a draft. |
| Arcs and threads | Changes across a character, relationship, conflict, or mystery, with links to the events and reveals that develop it. |

Give an event's factual account one primary home, usually chronology or a dedicated event entry when substantial. Other entries can summarize the relevant consequence and link to that account. Character knowledge and reader knowledge may change at different moments; record each at the appropriate point.

### Working notes

Use **Open questions** for unsettled choices and competing possibilities. Link each question to affected entries and preserve which options, if any, the author favors. Do not resolve a question merely to finish the bible.

Use **Decisions and changes** for consequential author choices, their sources, any stated rationale, and what they explicitly replace. Keep the current account on its subject page. Link to retained history and evidence instead of creating a second competing account. A question becomes resolved only when supported by an author decision or appropriate source evidence, following the editorial contract.

## Common entry pattern

Every substantive entry should have a useful summary, relevant subject sections, claim status and provenance beside the information they qualify, and related links where useful. Navigation-only indexes need no invented claims or evidence sections.

Use the statuses in [story-bible](../SKILL.md#ground-rules) and the authority rules in [the editorial contract](../../references/editorial-contract.md). Status belongs to individual claims, never the whole entry. Do not divide the collection into whole-page "canon" and "planning" buckets. Summaries must preserve the uncertainty of the claims they summarize.

Choose readable prose, bullets, or a table to suit the material. For example, a claim can use this compact pattern without requiring a database:

```text
[Status] Claim, including attribution and story point where relevant.
Source: manuscript version + stable location + shortest useful passage,
or author source + date or conversation context.
Related: primary account or affected entries, when useful.
```

Do not invent missing source details. Mark any provenance that cannot be verified. Keep superseded evidence and unresolved conflicts accessible without presenting them as current facts.

## Map to the destination

The organizing unit is a named, linkable entry. Use the chosen destination's available capabilities and existing conventions.

| Concept | Markdown / Obsidian | Word documents | Notion |
| --- | --- | --- | --- |
| Bible home | Index note | Contents document | Parent page |
| Section | Folder, with an index when useful | Folder | Section page |
| Entry | Markdown note or heading | Document or heading | Subpage or heading |
| Cross-reference | Note or heading link | Document link or bookmark | Page or heading link |

Use format-specific skills and tools for actual writes. Verify supported link targets in the actual destination. When a heading cannot be linked directly, link to its containing document and name the heading.
