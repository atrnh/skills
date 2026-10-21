# Ashley's skills

Reusable agent skills for engineering, education, and technical documentation. Principle skills, prefixed `principle-`, guide judgment. Workflow skills describe how to carry out a task.

## Organization

| Directory | Purpose |
| --- | --- |
| `skills/shared/` | Principles and workflows whose guidance transfers intact across domains. |
| `skills/engineering/` | Building and maintaining software, extensions, and internal tooling. |
| `skills/education/` | Curriculum design, teaching prose, exercises, assessments, and demos that develop learners' understanding and ability. |
| `skills/technical-documentation/` | Helping readers understand and use systems through explanations, procedures, reference material, and guides. |

Domains follow the primary audience and purpose of the work. File format and technology alone do not determine the domain:

- Python for a student exercise belongs primarily to education.
- Python for a Sphinx extension belongs to engineering.
- An administrator's guide to that extension belongs to technical documentation.

Shared skills apply alongside domain skills. When domain guidance differs, the artifact's primary audience and purpose decide which applies. A course demo can use engineering guidance for correctness while education determines what the code needs to teach.

## Available skills

| Skill | Domain | Judgment it guides |
| --- | --- | --- |
| [Let context do its work](skills/shared/principle-let-context-do-its-work/SKILL.md) | Shared | Remove repetition while preserving the relationships readers need. |
| [Bound analysis by the decision](skills/shared/principle-bound-analysis-by-the-decision/SKILL.md) | Shared | Scope research around the uncertainty that could change the decision. |
| [Match language to teaching purpose](skills/education/principle-match-language-to-teaching-purpose/SKILL.md) | Education | Explain concepts, narrate demonstrations, and direct practice with appropriate language. |
| [Make the progression meaningful](skills/education/principle-make-the-progression-meaningful/SKILL.md) | Education | Order learning around questions, prerequisites, and the work ahead. |
| [Connect examples to concepts](skills/education/principle-connect-examples-to-concepts/SKILL.md) | Education | Ground examples, connect their details to transferable ideas, and scope demonstrations. |
| [Protect practice time](skills/education/principle-protect-practice-time/SKILL.md) | Education | Reduce incidental work while preserving the intended challenge. |
| [Put essential reasoning in view](skills/education/principle-put-essential-reasoning-in-view/SKILL.md) | Education | Keep necessary context and connections in the learner's experience. |
| [Reconcile from declared authority](skills/engineering/principle-reconcile-from-declared-authority/SKILL.md) | Engineering | Define ownership of synchronized values before reconciling them. |
| [Place content by applicability](skills/technical-documentation/principle-place-content-by-applicability/SKILL.md) | Technical documentation | Determine where information applies before choosing its home. |
| [Make instruction paths complete](skills/technical-documentation/principle-make-instruction-paths-complete/SKILL.md) | Technical documentation | Help readers identify and follow the procedure for their situation. |
| [Document the current state](skills/technical-documentation/principle-document-the-current-state/SKILL.md) | Technical documentation | Reconcile the current explanation while preserving useful history. |

## Installing

This repository is a plugin marketplace named `atrnh-skills`. It offers one plugin per domain (`shared`, `education`, `engineering`, and `technical-documentation`) and an `all-skills` plugin containing every skill. Install either `all-skills` or the domain plugins you need. Installing both loads the same skills twice.

The commands below install `all-skills`. To install a single domain, replace `all-skills` with the domain's plugin name.

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
