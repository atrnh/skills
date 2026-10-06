# Ashley's skills

Reusable agent skills for engineering, education, and technical documentation. Skills capture both the judgments that guide the work and the workflows that carry it out.

## Organization

```text
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

These directories are starting points. No skills have been added yet.

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

Keep skill-specific examples, scripts, and references with their skill. Add further organizational layers only when the collection needs them.

Project-specific syntax, folder conventions, and build commands usually belong in the project's own instructions or workflows. Extract a reusable principle only when the broader judgment is useful independently of those details.

This layout organizes the source skills. Installation and agent discovery are not configured yet.

See [AGENTS.md](AGENTS.md) for instructions on working in this repository.
