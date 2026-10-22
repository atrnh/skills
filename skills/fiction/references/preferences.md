# Delivery preferences

These preferences apply to `line-editor` and `developmental-editor`, including its first-reader mode. Resolve delivery before writing comments, in this order:

1. The author's instructions for the current review, including chat-only or read-only requests.
2. `fiction-skills.md` in the current project root, when there is an identified local project.
3. `$CODEX_HOME/fiction-skills.md`, using `~/.codex/fiction-skills.md` when `CODEX_HOME` is unset.
4. The skill default, `inline`.

Read the applicable files if present. For a remote manuscript without a local project, use the personal file; do not search unrelated directories for a project preference. These files are agent-read Markdown, not application settings loaded by Codex itself. Existing applicable instructions still govern permissions and destinations.

Set delivery independently for each editor:

```markdown
# Fiction skills preferences

line-editor.delivery: chat
developmental-editor.delivery: chat
```

`inline` posts comments on the identified manuscript, placed as the [feedback guidance](feedback.md) describes. `chat` returns all feedback in chat without writing feedback to the manuscript. Neither setting permits rewriting prose. Resolve each editor's setting separately. Missing settings inherit the next level. If a setting is invalid or conflicting within a file, disclose it and use chat for that review rather than guessing write authority.

An explicit destination in the current request takes precedence. If multiple documents could be the feedback destination, clarify the target before posting. Do not persist a one-review override unless asked.

Use `$setup-fiction-skills` to save or reset a preference. Setup is optional; absence of configuration uses the default.
