---
name: setup-review-council
description: >
  Use when the user wants to configure, save, or reset how review-council builds its panel:
  which launchers start reviewers (T3 Code, the host's own subagents, or the cursor-agent, codex,
  and claude CLIs), which T3 providers or accounts pay for reviews, which model families to skip
  or pin, how many reviewers to seat, and their reasoning level. Detects the models actually
  available, previews the panel a review would seat, and writes a personal settings file. Use
  for /setup-review-council. Doesn't run a review.
---

# Set up the review council

Write `${XDG_CONFIG_HOME:-~/.config}/review-council/settings.md`, which the review-council skill
reads when it builds a panel. Setup is optional. Without the file, or for any setting the file
leaves out, review-council uses the defaults below.

## Settings and defaults

The file holds one setting per line. With every default written out, it reads:

```markdown
# Review council settings

Read by review-council when it builds a panel. Delete a line to use its default.

launchers: t3, subagents, cursor-agent, codex, claude
t3 providers: any
skip families: none
most reviewers: 5
reasoning: high
fast mode: off
```

- **`launchers`:** the ways reviewers can be started, in order of preference. When several
  launchers offer the same model, the first one listed starts it. Leave a launcher out to never
  use it.
  - `t3` is T3 Code's `delegate_task`, available wherever `orchestrator_capabilities` is.
  - `subagents` is the host's own subagent tool, such as Claude Code's `Agent` or Cursor's `Task`,
    with whatever models it accepts.
  - `cursor-agent`, `codex`, and `claude` are those CLIs, run non-interactively and read-only.
- **`t3 providers`:** the display names of the T3 providers reviewers may use, separated by
  commas, or `any`. T3 can run several accounts through one driver, so name the ones whose
  accounts should pay for reviews.
- **`skip families`:** model families never seated, such as `moonshot`, or `none`.
- **`most reviewers`:** the largest panel, at least 3. A council always needs reviewers from three
  different families, so this can't go lower.
- **`reasoning`:** each reviewer's reasoning level, such as `medium`, `high`, `xhigh`, or `max`. A
  model that lacks the level uses its highest level below it.
- **`fast mode`:** `off` or `on`, for models that offer it.

The file can also pin a family to one model, with one line per family:

```markdown
pin google: gemini-4-argon via t3 Cursor
pin anthropic: claude-opus-5-5-high via cursor-agent
```

A pin seats that family on every panel, using that model through that launcher. A `t3` pin names
the provider after `t3`. Review-council fills the other seats with each remaining family's most
capable available model.

## 1. Detect what's available

Check every launcher you can reach from this session, and record the models each one offers.
Never write a provider or pinned model you haven't confirmed here.

| Launcher | How to detect it |
| --- | --- |
| `t3` | Call `orchestrator_capabilities`. Its list is short and omits models, so use its `search` argument with family names, such as `gemini` or `kimi`, to find hidden ones. Record each provider's display name and models. Skip providers whose constraints say they're disabled or that can't run child tasks. |
| `subagents` | List the model slugs your subagent tool accepts in this session. Aliases such as `inherit` belong to no family. |
| `cursor-agent` | `cursor-agent models` |
| `codex` | `codex debug models`, which prints the catalog as JSON |
| `claude` | It has no list command. It accepts aliases such as `opus` and `sonnet` for the latest model of each line, as well as full model names. |

Check that each CLI is installed with `command -v`. Then note the account each one is signed in
to, using `cursor-agent status`, `codex login status`, and `claude auth status`, because reviews
started through a CLI run on that account.

## 2. Load the current settings

If the settings file exists, read it and treat its lines as the current choices. Otherwise start
from the defaults. A line that isn't one of the settings above, whether from an older version or
a typo, gets dropped. List it for the user when you confirm.

## 3. Choose and confirm

If the request already says what to change, apply it. Otherwise, show the current value of each
setting and ask what to change. Use the host's structured question tool if it has one.

Then preview the panel a review would seat right now. Follow review-council's "Build the panel"
step with the new settings and the models you detected. Show each reviewer's family, launcher,
provider, model, and options, plus the account behind each CLI. Name the families left out and
why, and mark any value you couldn't confirm as needing a choice. If the panel has fewer than
three families, say so, because review-council will stop and ask before every review. Ask the
user to accept the panel or change specific settings, and repeat the preview after each change.

A launcher this session can't reach can stay in `launchers`, since review-council checks again
at every review. Tell the user it went unchecked. T3 provider names and pins must be confirmed.
When their launcher isn't reachable here, ask the user to run setup again from a session that can
reach it, or leave them out.

## 4. Write the file

Create the folder if needed and replace the whole file, so running setup twice gives the same
result. Write the heading and the explanatory line from the default shape above. Then add only
the settings that differ from their defaults, followed by any pins. Leaving defaults out lets the
file pick up changes to them.

To reset a setting, remove its line. To reset everything, delete the file.

## 5. Report

Read the file back. Report its path, its settings, the effective value of every setting
including the defaults, and the panel you previewed. Explain that the user's instructions for a
review override the file for that review, and that a run reusing an earlier report's panel keeps
that panel. The settings apply to the next review without a restart. Setup doesn't run a review.
