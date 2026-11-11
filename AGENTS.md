# Working in this repository

This repository is the canonical source for Ashley's personal agent skills and the place to reinstall them from. Personal skills still kept in agent- or provider-specific folders will move here. Work-related skills, such as curriculum, Canvas, and SharePoint workflows, belong in her work skills repository, cloned at `~/work/skills`, instead. Read [README.md](README.md) for the domain map, available skills, and installation.

## Find the relevant guidance

- Identify the current work's audience and purpose, then look for that domain's principles and workflows in the matching directory under `skills/`.
- Check `skills/general/` for applicable guidance, and read the relevant `SKILL.md` files before using or changing them.
- Search existing skills before creating another one. Extend an existing skill when it already covers the same judgment or workflow.
- Use `docs/` for repository-level design notes.

## Preserve domain distinctions

Ashley works as an educator, technical writer, and platform engineer. Apply standards appropriate to the artifact's purpose.

- Educational code may use repetition or explicit steps to support learning. Do not apply production-code simplification rules without considering their teaching purpose.
- Use a friendly mentoring tone for educational content.
- Do not use Ponytail skills for educational work.
- Do not trigger Superpowers skills unless Ashley explicitly requests them.
- When skills from multiple domains apply, use the artifact's primary audience and purpose to resolve conflicting guidance.

## Place skills

- Assign a skill to the domain whose audience and purpose its guidance serves, as described in the README's [Organization](README.md#organization) section, and record it in the README's skill table.
- Put principles and workflows in their domain's directory, such as `skills/fiction/`.
- Keep a skill in the domain where its guidance has concrete support. Make it general when that guidance applies across domains without losing the distinctions that make it useful. A general skill moves into `skills/general/`.
- Give each skill its own directory containing a `SKILL.md`, such as `skills/general/writing-principles/SKILL.md`. Keep names unique across the repository.
- Keep skill-specific examples, scripts, and references beside their `SKILL.md`. Add further organizational layers only when the collection needs them.
- Keep project-specific syntax, folder conventions, and build commands in the project's own instructions or workflows. Extract a reusable principle only when the broader judgment is useful independently of those details.

## Write skills

- Write principles as compact guidance for judgment. A principle should explain when it applies, what judgment to make, how that changes the work, and where the guidance stops applying. Keep each part concrete.
- Group principles that apply to the same kind of work into one skill with a section for each, such as `writing-principles`. Agents tend to load only some of several separate skills that apply together. Give a principle its own skill only when it applies to a narrow, distinct task, as `sync-from-the-source-of-truth` does, and name that skill for the action it guides.
- Write workflow skills to describe how to carry out a task.
- Agents load skills, including principles, by matching their descriptions to the current work. Begin a description with when the skill applies, and name the concrete artifacts or tasks where that happens, such as slides, labs, READMEs, or sync tooling.
- Keep originating examples out of the skill body so the guidance stays general.
- Treat brainstormed principles as proposals until Ashley authorizes creating them.

## Maintain the packaging

The repository publishes three plugins: `fiction` for `skills/fiction/`, `core` for every other domain directory, and `all-skills` for both. A new skill in an existing domain directory needs no manifest changes. A new domain directory needs its path added to the `core` and `all-skills` entries in each host's marketplace:

- `.claude-plugin/marketplace.json` for Claude Code.
- `.agents/plugins/marketplace.json` for Codex, which reads it instead of the Claude marketplace.
- `.cursor-plugin/marketplace.json` for Cursor.

GitHub Copilot CLI ignores the marketplace's `skills` paths and reads a `plugin.json` in each plugin's source directory instead. Add the new path to `skills/.github/plugin/plugin.json` for `core` and `.github/plugin/plugin.json` for `all-skills`.

Run `claude plugin validate . --strict` after changing the manifests.

Ashley links some domains into her agents with `scripts/skill-links.py`, described in the README's [linking section](README.md#linking-skills-for-live-editing). After adding, renaming, or removing a skill in a linked domain, run `scripts/skill-links.py link` on that domain once the change reaches the main checkout.

## Make focused changes

- Prefer simple structures and existing patterns. Avoid duplicate rules, speculative tooling, and extra directory layers.
- Preserve unrelated work. Update the README's skill table when adding, renaming, or removing a skill, and its other sections when domains or installation change.
- Check changed files, links, and paths before reporting completion. For prose-only changes, a focused review and `git diff --check` are sufficient; do not add tests that merely mirror the text.
- Use `uv` for Python package management and `pnpm` for JavaScript or TypeScript package management when needed.
