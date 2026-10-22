---
name: setup-fiction-skills
description: Save or reset fiction skill preferences, including whether the line and developmental editors post inline comments or return feedback in chat. Use when the author asks to configure persistent defaults.
---

# Set up fiction skills

Read [delivery preferences](../references/preferences.md) for supported values, locations, and precedence.

Save `line-editor.delivery`, `developmental-editor.delivery`, or both as requested, using `inline` or `chat`. If the request does not identify which editor to configure, ask. If the author has not chosen a mode, ask whether they want comments on the manuscript or feedback in chat. Explain that inline is the default for both editors and preserves manuscript prose. For developmental reviews, chat holds only feedback with no obvious inline home or notes that cannot be posted, unless the author chooses otherwise.

Use project scope when the author asks for this project's default, and personal scope when they ask for their general default. If scope is unclear, ask which they intend. For project scope without an identified local project, ask for the project location or offer personal scope. Do not store settings in the installed plugin directory.

Read the chosen preference file before editing. Create it if absent, update only the requested setting, and preserve unrelated content. A reset removes that setting so it inherits the next level; it does not delete the file or other preferences. Do not edit both scopes unless asked.

Read back the saved file and report its path, value, and effective delivery mode. If a project override masks a personal setting, explain that precedence. Configuring delivery does not run a review or post comments.
