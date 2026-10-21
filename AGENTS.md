# Working in this repository

This repository is the canonical source for Ashley's reusable agent skills and the place to reinstall them from. Skills still kept in agent- or provider-specific folders will move here. Read [README.md](README.md) for the domain map, available skills, and installation.

## Find the relevant guidance

- Identify the current work's audience and purpose, then look in the matching directory under `skills/`.
- Check `skills/shared/` for applicable guidance and read the relevant `SKILL.md` files before using or changing them.
- Search existing skills before creating another one. Extend an existing skill when it already covers the same judgment or workflow.
- Use `docs/` for repository-level design notes. The [October 6 principle extraction](docs/principle-extraction-2026-10-06.md) records the conversation evidence and selection decisions behind the principles added on that date.

## Preserve domain distinctions

Ashley works as an educator, technical writer, and platform engineer. Apply standards appropriate to the artifact's purpose.

- Educational code may use repetition or explicit steps to support learning. Do not apply production-code simplification rules without considering their teaching purpose.
- Use a friendly mentoring tone for educational content.
- Do not use Ponytail skills for educational work.
- Do not trigger Superpowers skills unless Ashley explicitly requests them.
- When skills from multiple domains apply, use the artifact's primary audience and purpose to resolve conflicting guidance.

## Place skills

- Place a skill in the domain whose audience and purpose its guidance serves, as described in the README's [Organization](README.md#organization) section.
- Keep a skill in the domain where its guidance has concrete support. Move it into `shared/` when that guidance applies across domains without losing the distinctions that make it useful.
- Give each skill its own directory containing a `SKILL.md`, such as `skills/education/principle-connect-examples-to-concepts/SKILL.md`. Keep names unique across the repository.
- Keep principles and workflows together within their domain. Keep skill-specific examples, scripts, and references beside their `SKILL.md`. Add further organizational layers only when the collection needs them.
- Keep project-specific syntax, folder conventions, and build commands in the project's own instructions or workflows. Extract a reusable principle only when the broader judgment is useful independently of those details.

## Write skills

- Use the `principle-` prefix for compact skills that guide judgment. A principle should explain when it applies, what judgment to make, how that changes the work, and where the guidance stops applying. Keep each part concrete.
- Write workflow skills to describe how to carry out a task.
- Agents load skills, including principles, by matching their descriptions to the current work. Begin a description with when the skill applies, and name the concrete artifacts or tasks where that happens, such as slides, labs, READMEs, or sync tooling.
- Keep originating examples out of the skill body so the guidance stays general.
- Treat brainstormed principles as proposals until Ashley authorizes creating them.

## Maintain the packaging

A new skill in an existing domain needs no manifest changes. A new domain needs:

- An entry in `.claude-plugin/marketplace.json`, and its path added to the `all-skills` entry there. Claude Code and Codex CLI read this manifest.
- A matching entry in `.github/plugin/marketplace.json`. GitHub Copilot CLI reads this manifest instead because it ignores the other manifest's `skills` paths.
- A `skills/<domain>/.github/plugin/plugin.json` for GitHub Copilot CLI, modeled on the existing ones.

Run `claude plugin validate . --strict` after changing either marketplace manifest.

## Make focused changes

- Prefer simple structures and existing patterns. Avoid duplicate rules, speculative tooling, and extra directory layers.
- Preserve unrelated work. Update the README's skill table when adding, renaming, or removing a skill, and its other sections when domains or installation change.
- Check changed files, links, and paths before reporting completion. For prose-only changes, a focused review and `git diff --check` are sufficient; do not add tests that merely mirror the text.
- Use `uv` for Python package management and `pnpm` for JavaScript or TypeScript package management when needed.
