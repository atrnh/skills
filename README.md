# Ashley's skills

Reusable agent skills for engineering, education, and technical documentation. Skills capture both the judgments that guide the work and the workflows that carry it out.

This repository is the canonical source for the collection: the place to reinstall skills from and, eventually, to distribute them publicly. Skills still kept in agent- or provider-specific folders will move here.

## Organization

```text
.claude-plugin/marketplace.json
.github/plugin/marketplace.json
skills/
  shared/
  engineering/
  education/
  technical-documentation/
docs/
```

| Directory | Purpose |
| --- | --- |
| `skills/shared/` | Principles and workflows whose guidance transfers intact across domains. |
| `skills/engineering/` | Building and maintaining software, extensions, and internal tooling. |
| `skills/education/` | Curriculum design, teaching prose, exercises, assessments, and demos that develop learners' understanding and ability. |
| `skills/technical-documentation/` | Helping readers understand and use systems through explanations, procedures, reference material, and guides. |
| `docs/` | Repository-level design notes and supporting documentation. |
| `.claude-plugin/`, `.github/plugin/` | Plugin marketplace manifests. See [Installing](#installing). |

## Available skills

| Skill | Domain | Judgment it guides |
| --- | --- | --- |
| [Let context do its work](skills/shared/principle-let-context-do-its-work/SKILL.md) | Shared | Remove repetition while preserving the relationships readers need. |
| [Format by meaning](skills/shared/principle-format-by-meaning/SKILL.md) | Shared | Choose inline formatting by the text's role and the reader's task. |
| [Bound analysis by the decision](skills/shared/principle-bound-analysis-by-the-decision/SKILL.md) | Shared | Scope research around the uncertainty that could change the decision. |
| [Match language to teaching purpose](skills/education/principle-match-language-to-teaching-purpose/SKILL.md) | Education | Explain concepts, narrate demonstrations, and direct practice with appropriate language. |
| [Make the progression meaningful](skills/education/principle-make-the-progression-meaningful/SKILL.md) | Education | Order learning around questions, prerequisites, and the work ahead. |
| [Connect examples to concepts](skills/education/principle-connect-examples-to-concepts/SKILL.md) | Education | Ground examples and connect their details to transferable ideas. |
| [Protect practice time](skills/education/principle-protect-practice-time/SKILL.md) | Education | Reduce incidental work while preserving the intended challenge. |
| [Let demonstrations serve the lesson](skills/education/principle-let-demonstrations-serve-the-lesson/SKILL.md) | Education | Demonstrate where observation improves understanding. |
| [Put essential reasoning in view](skills/education/principle-put-essential-reasoning-in-view/SKILL.md) | Education | Keep necessary context and connections in the learner's experience. |
| [Separate the workflow from the tool](skills/engineering/principle-separate-the-workflow-from-the-tool/SKILL.md) | Engineering | Preserve reusable workflow decisions across tool-specific operations. |
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

## Choosing a domain

Classify work by its primary audience and purpose. File format and technology alone do not determine the domain:

- Python for a student exercise belongs primarily to education.
- Python for a Sphinx extension belongs to engineering.
- An administrator's guide to that extension belongs to technical documentation.

Select skills according to the purpose of the current work. Apply shared principles alongside relevant domain skills. When domain guidance differs, follow the guidance for the artifact's primary audience and purpose. A course demo can use engineering guidance for correctness while education determines what the code needs to teach.

Keep a skill in the domain where its guidance has concrete support. Move it into `shared/` when that guidance applies across domains without losing the distinctions that make it useful.

## Adding skills

Give each skill its own directory containing a `SKILL.md`, such as `skills/education/principle-connect-examples-to-concepts/SKILL.md`. Keep names unique across the repository.

Keep principles and workflows together within their domain. Use the `principle-` prefix for compact skills that guide judgment. A principle should explain when it applies, what judgment to make, how that changes the work, and where the guidance stops applying. Workflow skills describe how to carry out a task.

Agents load skills, including principles, by matching their descriptions to the current work. Begin a description with when the skill applies, and name the concrete artifacts or tasks where that happens, such as slides, labs, READMEs, or sync tooling. Keep originating examples out of the body so the guidance stays general.

A new skill in an existing domain needs no manifest changes. A new domain needs:

- An entry in `.claude-plugin/marketplace.json`, and its path added to the `all-skills` entry there.
- A matching entry in `.github/plugin/marketplace.json`, which GitHub Copilot CLI reads instead because it ignores the other manifest's `skills` paths.
- A `skills/<domain>/.github/plugin/plugin.json` for GitHub Copilot CLI, modeled on the existing ones.

Run `claude plugin validate . --strict` after changing either marketplace manifest.

Keep skill-specific examples, scripts, and references with their skill. Add further organizational layers only when the collection needs them.

Project-specific syntax, folder conventions, and build commands usually belong in the project's own instructions or workflows. Extract a reusable principle only when the broader judgment is useful independently of those details.

The [October 6 principle extraction](docs/principle-extraction-2026-10-06.md) records the conversation evidence and selection decisions behind the principles added on that date.

See [AGENTS.md](AGENTS.md) for instructions on working in this repository.

## License

Released under the [MIT License](LICENSE). Skills adapted from other authors keep their original license files beside their `SKILL.md`.
