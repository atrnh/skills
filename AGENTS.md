# Working in this repository

This repository holds Ashley's reusable agent skills. Read [README.md](README.md) for the domain map and placement rules before adding or moving a skill.

## Find the relevant guidance

- Identify the current work's audience and purpose, then look in the matching directory under `skills/`.
- Check `skills/shared/` for applicable guidance and read the relevant `SKILL.md` files before using or changing them.
- Search existing skills before creating another one. Extend an existing skill when it already covers the same judgment or workflow.
- Keep principles and workflows together in their domain. Keep skill names unique across domains.
- Use `docs/` for repository-level documentation; keep a skill's supporting files beside its `SKILL.md`.

## Preserve domain distinctions

Ashley works as an educator, technical writer, and platform engineer. Apply standards appropriate to the artifact's purpose.

- Educational code may use repetition or explicit steps to support learning. Do not apply production-code simplification rules without considering their teaching purpose.
- Use a friendly mentoring tone for educational content. Match language to the passage's purpose: explain concepts and relationships, and give instructions in procedures and practice.
- Do not use Ponytail skills for educational work.
- Do not trigger Superpowers skills unless Ashley explicitly requests them.
- When skills from multiple domains apply, use the artifact's primary audience and purpose to resolve conflicting guidance.

## Make focused changes

- Keep principles concrete. State their applicability, the judgment they guide, the resulting behavior, and the boundary that prevents overapplication.
- Treat brainstormed principles as proposals until Ashley authorizes creating them.
- Keep project-specific conventions with the project unless their reuse justifies a skill here.
- Prefer simple structures and existing patterns. Avoid duplicate rules, speculative tooling, and extra directory layers.
- Preserve unrelated work. Update the README when the repository's organization or discovery process changes.
- Check changed files, links, and paths before reporting completion. For prose-only changes, a focused review and `git diff --check` are sufficient; do not add tests that merely mirror the text.
- Use `uv` for Python package management and `pnpm` for JavaScript or TypeScript package management when needed.
