# Ashley's skills

Reusable agent skills for engineering, education, documentation, fiction, and personal workflows. Principle skills, prefixed `principle-`, guide judgment. Workflow skills describe how to carry out a task.

## Organization

Principle skills live together in `skills/principles/`. Workflow skills live in a folder named for their domain, such as `skills/education/`. The [skill table](#available-skills) lists each skill's domain.

| Domain | Purpose |
| --- | --- |
| General | Principles and workflows whose guidance transfers intact across domains. |
| Engineering | Building and maintaining software, extensions, and internal tooling. |
| Education | Curriculum design, teaching prose, exercises, assessments, and demos that develop learners' understanding and ability. |
| Documentation | Helping readers understand and use systems through explanations, procedures, reference material, and guides. |
| Fiction | Developing, editing, and keeping a story bible for Ashley's fiction. Skills here share the editorial contract and delivery guidance in `skills/fiction/references/`. |
| Personal | Ashley's own assistant workflows, such as sending messages on her behalf and saving responses to Obsidian. |

Domains follow the primary audience and purpose of the work. File format and technology alone do not determine the domain:

- Python for a student exercise belongs primarily to education.
- Python for a Sphinx extension belongs to engineering.
- An administrator's guide to that extension belongs to documentation.

General skills apply alongside domain skills. When domain guidance differs, the artifact's primary audience and purpose decide which applies. A course demo can use engineering guidance for correctness while education determines what the code needs to teach.

## Available skills

| Skill | Domain | Judgment it guides |
| --- | --- | --- |
| [Bound analysis by the decision](skills/principles/principle-bound-analysis-by-the-decision/SKILL.md) | General | Scope research around the uncertainty that could change the decision. |
| [Deep quality review](skills/general/deep-quality-review/SKILL.md) | General | Review writing for functional and deep quality using Diátaxis, then triage fixes in a dashboard. |
| [Match language to teaching purpose](skills/principles/principle-match-language-to-teaching-purpose/SKILL.md) | Education | Explain concepts, narrate demonstrations, and direct practice with appropriate language. |
| [Make the progression meaningful](skills/principles/principle-make-the-progression-meaningful/SKILL.md) | Education | Order learning around questions, prerequisites, and the work ahead. |
| [Connect examples to concepts](skills/principles/principle-connect-examples-to-concepts/SKILL.md) | Education | Ground examples, connect their details to transferable ideas, and scope demonstrations. |
| [Protect practice time](skills/principles/principle-protect-practice-time/SKILL.md) | Education | Reduce incidental work while preserving the intended challenge. |
| [Put essential reasoning in view](skills/principles/principle-put-essential-reasoning-in-view/SKILL.md) | Education | Keep necessary context and connections in the learner's experience. |
| [Create lecture](skills/education/create-lecture/SKILL.md) | Education | Sequence a list of topics into an outline, then write the full RST lecture. |
| [Create MCQ](skills/education/create-mcq/SKILL.md) | Education | Generate multiple choice questions from supplied text or documents. |
| [Review lab](skills/education/review-lab/SKILL.md) | Education | Give structured editorial feedback on a subject matter expert's lab or exercise draft. |
| [Student question pass](skills/education/student-question-pass/SKILL.md) | Education | Roleplay a target learner, add their questions as comments, and turn selected ones into content. |
| [Reconcile from declared authority](skills/principles/principle-reconcile-from-declared-authority/SKILL.md) | Engineering | Define ownership of synchronized values before reconciling them. |
| [Let context do its work](skills/principles/principle-let-context-do-its-work/SKILL.md) | Documentation | Remove repetition while preserving the relationships readers need. |
| [Document the current state](skills/principles/principle-document-the-current-state/SKILL.md) | Documentation | Reconcile the current explanation while preserving useful history. |
| [Developmental editor](skills/fiction/developmental-editor/SKILL.md) | Fiction | Give candid structural critique or a spoiler-bounded first-reader response. |
| [Line editor](skills/fiction/line-editor/SKILL.md) | Fiction | Edit prose closely for local reader effect while preserving deliberate style. |
| [Grill my story](skills/fiction/grill-my-story/SKILL.md) | Fiction | Pressure-test a premise, character choice, scene, or plot problem through questioning. |
| [Review fiction](skills/fiction/review-fiction/SKILL.md) | Fiction | Critique a chapter in a two-column HTML page with anchored comments. |
| [Story bible](skills/fiction/story-bible/SKILL.md) | Fiction | Build and query a fiction wiki that tracks evidence, canon status, and chronology. |
| [Set up fiction skills](skills/fiction/setup-fiction-skills/SKILL.md) | Fiction | Save how the editors deliver feedback by default. |
| [Beep](skills/personal/beep/SKILL.md) | Personal | Write and send messages on Ashley's behalf as her identified robot assistant. |
| [Vaultit](skills/personal/vaultit/SKILL.md) | Personal | Save an assistant response to Obsidian. |

## Installing

This repository is a plugin marketplace named `atrnh-skills`. It offers three plugins:

- `core` contains every skill except fiction.
- `fiction` contains the fiction skills.
- `all-skills` contains both.

Install `all-skills`, or install `core`, `fiction`, or both. Installing `all-skills` alongside either of the others loads the same skills twice.

The commands below install `all-skills`. To install another plugin, replace `all-skills` with its name.

### Claude Code

```sh
claude plugin marketplace add atrnh/skills
claude plugin install all-skills@atrnh-skills
```

To update, run `claude plugin marketplace update atrnh-skills`, then `claude plugin update all-skills@atrnh-skills`.

### Codex CLI

```sh
codex plugin marketplace add atrnh/skills
codex plugin add all-skills@atrnh-skills
```

To update, run `codex plugin marketplace upgrade atrnh-skills`.

### GitHub Copilot CLI

```sh
copilot plugin marketplace add atrnh/skills
copilot plugin install all-skills@atrnh-skills
```

To update, run `copilot plugin marketplace update atrnh-skills`, then `copilot plugin update all-skills@atrnh-skills`.

### Other agents

Use the [`skills` CLI](https://github.com/vercel-labs/skills) when your agent doesn't support plugins, or when you want individual skills:

```sh
npx skills@latest add atrnh/skills
```

Add `--list` to see the available skills, or `--skill <name>` to install specific ones. To install one domain, add its path, as in `npx skills@latest add atrnh/skills/skills/education`. To update, run `npx skills update`.

## License

Released under the [MIT License](LICENSE). Skills adapted from other authors keep their original license files beside their `SKILL.md`.
