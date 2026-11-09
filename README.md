# Ashley's skills

Reusable agent skills for engineering, education, documentation, fiction, and personal workflows. Principle skills, such as `teaching-principles`, guide judgment. Workflow skills describe how to carry out a task.

## Organization

Each skill lives in a folder named for its domain, such as `skills/education/`. The [skill table](#available-skills) lists each skill's domain.

| Domain | Purpose |
| --- | --- |
| General | Principles and workflows whose guidance transfers intact across domains. |
| Engineering | Building and maintaining software, extensions, and internal tooling. |
| Education | Curriculum design, teaching prose, exercises, assessments, and demos that develop learners' understanding and ability. |
| Documentation | Helping readers understand and use systems through explanations, procedures, reference material, and guides. |
| Fiction | Developing, editing, and keeping a story bible for Ashley's fiction. Skills here share the editorial contract in `skills/fiction/references/`; the editors also share its review conduct and delivery guidance. |
| Personal | Ashley's own assistant workflows, such as sending messages on her behalf and saving responses to Obsidian. |

Domains follow the primary audience and purpose of the work. File format and technology alone do not determine the domain:

- Python for a student exercise belongs primarily to education.
- Python for a Sphinx extension belongs to engineering.
- An administrator's guide to that extension belongs to documentation.

General skills apply alongside domain skills. When domain guidance differs, the artifact's primary audience and purpose decide which applies. A course demo can use engineering guidance for correctness while education determines what the code needs to teach.

## Available skills

| Skill | Domain | Judgment it guides |
| --- | --- | --- |
| [Writing principles](skills/general/writing-principles/SKILL.md) | General | Use established context to cut repetition, and present the current state while keeping history distinct. |
| [Deep quality review](skills/general/deep-quality-review/SKILL.md) | General | Review writing for functional and deep quality using Diátaxis. |
| [Triage feedback](skills/general/triage-feedback/SKILL.md) | General | Check a batch of proposed changes, then approve or reject each one in a dashboard before applying them. |
| [Teaching principles](skills/education/teaching-principles/SKILL.md) | Education | Sequence lessons, connect examples to concepts, match language to purpose, protect practice time, and keep reasoning in view when presenting. |
| [Create lecture](skills/education/create-lecture/SKILL.md) | Education | Sequence a list of topics into an outline, then write the full RST lecture. |
| [Create MCQ](skills/education/create-mcq/SKILL.md) | Education | Generate multiple choice questions from supplied text or documents. |
| [Review lab](skills/education/review-lab/SKILL.md) | Education | Give structured editorial feedback on a subject matter expert's lab or exercise draft. |
| [Student question pass](skills/education/student-question-pass/SKILL.md) | Education | Roleplay a target learner, add their questions as comments, and turn selected ones into content. |
| [Sync from the source of truth](skills/engineering/sync-from-the-source-of-truth/SKILL.md) | Engineering | Define ownership of synchronized values before reconciling them. |
| [Graduate skill](skills/engineering/graduate-skill/SKILL.md) | Engineering | Move a tested skill into the plugin repo that fits it, leaving one copy that every host links to. |
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

### Cursor

In Cursor, open **Customize**, import `atrnh/skills` with **From GitHub Repository**, and install `all-skills`.

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

### Linking skills for live editing

To use a domain's skills straight from a local clone, so your edits take effect without reinstalling, link them instead of installing the plugin:

```sh
scripts/skill-links.py link skills/fiction
```

The script links each skill into `~/.claude/skills` and `~/.codex/skills`. Cursor loads both folders. Links point at the repository's main checkout, even when you run the script from a worktree. Run it again after adding, renaming, or removing a skill. Use `status` instead of `link` to see where each link resolves, and `unlink` to remove the links. The script works on any git repository's skills, so you can also pass a path in another plugin repository.

The script refuses to replace a skill it didn't link. It also refuses while an installed plugin, or another skill folder these agents load, already provides a skill of the same name, because the agent would then load both copies. Uninstall the plugin or remove the other copy, then run it again.

## License

Released under the [MIT License](LICENSE). Skills adapted from other authors keep their original license files beside their `SKILL.md`.
