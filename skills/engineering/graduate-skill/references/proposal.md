# Graduation proposal template

Use these sections in this order, so that a maintenance run can collect several proposals into one review. Omit a section's table when it has no rows, and say so in a sentence instead.

```markdown
# Graduation proposal: <skill>

**Recommendation:** <one of the following>
- Graduate to `<repo>` as `<domain folder>/<skill>` in the `<plugin>` plugins.
- Decide first: <the question>. Recommended: <an existing repo, or a new repo with a proposed name>.
- Don't graduate: <reason, such as a third-party skill or a blocking readiness finding>.

## Evidence

- **Source:** `<path>`, <commit count> commits, <the survey's state>.
- **Maintenance evidence:** <firing frequency, last correction, scan result, or "not supplied">.
- **Readiness scan:** <agrees with or differs from the supplied scan, and how>.

## Destination

<The repo, domain folder, and plugins, and the rule that chose them: named, fits, new, or ask. Name the other repos considered and why each doesn't fit.>

## Readiness

| Location | Finding | Blocks | Proposed fix | Needs approval |
| --- | --- | --- | --- | --- |

List blocking findings first. In **Blocks**, name the destinations the finding blocks, `all`, or `none`. A finding needs approval when its fix changes what the skill does or says, rather than substituting a placeholder.

## Copies and links

| Path | Kind | Digest | Plan |
| --- | --- | --- | --- |

Give each row one plan:

- **Import, then retire:** the source copy. Import it into the destination, then remove it with `git rm` after the destination change merges.
- **Keep:** the copy already in the destination.
- **Unlink:** a link to an old copy. Remove it, and let the linking script create the new link.
- **Trash:** a copy that matches the source.
- **Ask:** a copy that differs from the source.
- **User action:** a Claude-synced copy, which only the user can remove from their Claude account.

## Dependencies

<Each skill or shared file this skill relies on, and whether it moves with it, already exists in the destination, or must be removed from the skill.>

## Plan

<Numbered steps from the graduation steps: the history method, approved edits, manifest and README changes, validation, the publishing step and its approval, relinking, removals, and verification. Mark each step that waits on a pull request merge.>

## Decisions needed

<Numbered questions, each with a recommended answer.>
```
