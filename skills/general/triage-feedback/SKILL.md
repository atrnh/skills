---
name: triage-feedback
description: >
  Use after an agent or reviewer has produced a batch of proposed changes to text files, such as
  a deep-quality review, Bugbot or code-review findings, a subagent's critique, or review notes
  pasted into the chat, and the user wants to decide what to act on. Builds a local dashboard
  where the user approves or rejects each change, seeing its problem, evidence, the case against
  it, the affected lines, and the exact replacement. Then applies the approved fixes or drafts a
  GitHub review. Use when the user asks for a triage dashboard, wants to go through feedback one
  item at a time, or asks which suggestions to accept. Do NOT use for triaging issues in an issue
  tracker, or for decisions that aren't tied to specific text in files.
---

# Triage feedback

The dashboard turns a batch of feedback into a page where the user approves or rejects each
proposed fix. Each card shows the problem, its evidence, the case against changing it, the
affected lines in context, and the exact replacement. The scripts in this skill's `dashboard/`
folder need only Python 3 and Git; posting a review also needs `gh`.

| Script | Does |
|---|---|
| `build.py RUN/findings.json [--check]` | Checks every finding against the files and writes `index.html` and `resolved.json` |
| `serve.py start RUN` / `stop RUN` | Serves the page on localhost and saves decisions to `RUN/decisions.json` |
| `apply.py RUN [--dry-run] [--root PATH]` | Applies approved fixes to the files |
| `review.py RUN --summary TEXT` | Drafts a GitHub review from approved fixes as `RUN/review.json` (doesn't post) |

`apply.py` and `review.py` read approvals from `decisions.json`. When the user pasted their
decisions into the chat instead, pass `--approve F1,F3,...`.

## 1. Gather the feedback

The feedback can be a review you wrote in this session, another agent's output, a file, or
notes pasted into the chat. If a review skill produced it, follow that skill's guidance on IDs,
categories, and priorities.

Cards need a location in a file. Feedback about a design choice, a plan, or anything else
without one doesn't belong on the page. Leave it out, and tell the user which items you left
out so they can decide on them in the chat.

## 2. Make a run folder

Use `/tmp/feedback-triage/<slug>/`, for example `/tmp/feedback-triage/pr-42/` or
`/tmp/feedback-triage/launch-email/`. Everything for this triage lives there.

## 3. Point at the source

Line numbers must come from the exact text the user will judge.

- **Pull request.** Check out the PR's head commit in its own worktree, so local edits on
  the user's branch can't shift lines:

  ```bash
  gh pr view N --json headRefOid,baseRefName
  git fetch origin <baseRefName> pull/N/head
  git worktree add --detach /tmp/feedback-triage/pr-N/checkout <headRefOid>
  ```

  Source: `{"kind": "pr", "root": "checkout", "url": "<PR URL>", "base": "origin/<baseRefName>"}`.
  GitHub links to each snippet are added automatically.
- **The user's own changes.** Use their checkout as `root`. Set `base` to what the work
  branched from (such as `origin/main`), or `HEAD` to cover only uncommitted changes. Kind
  `changes`.
- **Plain files.** `root` is the folder that contains them. Kind `files`, and no `base`.
- **Pasted text** (an email, a draft in the chat). Save it verbatim to
  `RUN/source/<name>.md` (or `.txt`, `.rst`, whatever fits), then treat it as plain files with
  `"root": "source"`.

A relative `root` is resolved from the run folder.

## 4. Check each item before making a card

Treat feedback as claims to check, including feedback you wrote yourself. Reviewers, and
agents especially, cite lines that don't exist, flag problems the text doesn't have, and
report the same problem more than once.

- **Find the text.** If the quoted text or the cited lines aren't there, or the problem isn't
  where the feedback says, drop the item.
- **Confirm the problem.** Check it against the source, the code, or the facts where you can.
  If you can't confirm it, keep the card and begin its `problem` with "Unverified:".
- **Merge duplicates** into one card, and name every item it covers in `problem`.
- **Keep items you disagree with** when the user might still want them, and put your
  disagreement in `counter`.

## 5. Write `findings.json`

Give each card an ID. Keep any IDs the feedback already uses, so the user can refer to items
the same way in the chat and on the page. If it has none, number the items `F1`, `F2`, and so
on, in the order they appear. Use the feedback's own categories when it has them. Otherwise,
pick a few plain ones, such as Bug, Accuracy, Clarity, and Style. Priority 1 breaks the work or
misleads its reader, 2 noticeably hurts it, and 3 is polish.

The cards are only as useful as their fields:

- **`counter`** is the strongest honest case against making the change: scope, audience,
  intent, or cost. It's what lets the user reject with confidence. Don't leave it empty or
  make it a straw man.
- **`replacement`** is the exact text of whole lines, with the file's indentation, that
  replaces the lines from `start` to `end`. Use `""` to delete them. Prefer one tight fix per
  problem. When a finding needs a structural move with no line-level edit, use `fixNote`
  instead.
- **Anchor with `match`** (a phrase quoted from the file) rather than line numbers wherever
  you can. The build finds the lines for you and fails if the quote is missing or matches
  more than once. Use `occurrence` (1-based) only when repetition is unavoidable.

```json
{
  "title": "PR #42 review",
  "source": {
    "kind": "pr",
    "root": "checkout",
    "label": "owner/repo#42",
    "url": "https://github.com/owner/repo/pull/42",
    "base": "origin/main"
  },
  "findings": [
    {
      "id": "F1",
      "category": "Accuracy",
      "priority": 1,
      "title": "Install guide names the wrong minimum Python",
      "problem": "The guide says Python 3.8 or later, but `pyproject.toml` requires 3.10.",
      "evidence": [{"text": "pyproject.toml, requires-python", "url": "https://..."}],
      "counter": "Older versions may still run the parts of the tool this guide covers.",
      "comment": "",
      "context": [
        {"file": "docs/install.md", "match": "Python 3.8 or later"},
        {"file": "pyproject.toml", "match": "requires-python", "around": 0,
         "label": "What the package requires"}
      ],
      "fixes": [
        {"file": "docs/install.md", "match": "Python 3.8 or later",
         "replacement": "You need Python 3.10 or later."}
      ]
    }
  ]
}
```

**Top level:** `title` is shown on the page and makes up part of the key that decisions are
saved under. `source` contains `kind`, `root`, and optionally `label`, `url`, `base`, `link`, and
`changeLabel`.
`link` overrides the snippet link template (`{path}`, `{start}`, `{end}`, `{head}`).
`changeLabel` names the change in tags, and defaults to "this PR" or "these changes".

**Finding:** `id` (letters and digits, starting with a letter), `category`, `priority` (1, 2, or
3), `title`, `problem`, `counter`, `evidence` (list of `{text, url}`), `context`, `fixes`,
`fixNote`, and `comment` (optional GitHub-facing wording for `review.py`; defaults to
`problem`). Text fields accept `` `code` ``, `**bold**`, `*italic*`, and `[links](url)`.

**Context snippet:** `file` plus either `match` (shows the matched lines plus `around` lines on
each side, 3 by default) or `start` and `end`. `highlight` overrides the highlighted lines.
List line numbers or phrases that each match exactly one line in the snippet. `label` names
the snippet. Put the main location first, because it's what the card header and the review
comment point to.

**Fix:** `file`, `replacement`, and either `match` or `start` and `end`. Optional `label`.

## 6. Build and check

```bash
python3 .../dashboard/build.py RUN/findings.json --check
```

Errors block the build: a missing or ambiguous quote, a line outside the file, a duplicate
ID, a fix that overlaps another fix in the same finding. `--check` prints every highlighted
line and every line a fix replaces, so read it and confirm each one is the line you meant.
Then deal with the warnings:

- **Blank highlighted lines** usually mean a line-number slip.
- **Two findings changing the same lines** can both stay. The page marks each one and warns if
  both are approved.
- **A file that differs from HEAD** means its GitHub links won't match the snippets.

## 7. Launch

```bash
python3 .../dashboard/serve.py start RUN
```

This prints the URL and the stop command. Running it again for the same run reports the
server that's already running. The server reads files on every request, so after a rebuild
the user only needs to reload the page. Decisions are kept as long as the title and the
reviewed commit don't change.

Open the URL in the harness's in-app browser preview if it has one (in T3 Code, the
`preview_open` tool). Otherwise run `open URL` on macOS or `xdg-open URL` on Linux. If the server
can't start, open `RUN/index.html` directly. The page then saves decisions in the browser only,
and the user copies the Markdown from the page's Decisions panel into the chat.

Tell the user:

- the URL;
- how to decide: Approve or Reject on each card, an optional note to adjust a fix, and the
  keys `a`, `r`, `u`, `j`, `k`, and `Enter`;
- that decisions are saved as they go, so they only need to say when they're done;
- which items you dropped, merged, left out, or couldn't verify;
- which fixes deserve a close look, such as diagrams, generated files, or anything you
  couldn't render or verify.

## 8. Act on the decisions

When the user says they're done, read `RUN/decisions.json`. Rejected findings stay as they are.

1. **Notes first.** A note on an approved finding may change its fix. Update that finding in
   `findings.json`, rebuild, and pass `--notes-handled` from then on. The scripts refuse to run
   until you do. If a note asks a question, answer it before applying anything.
2. **Ask how to apply them, with a default.** Offer to edit the files or to post a GitHub review.
   - If the PR belongs to someone else (`gh pr view N --json author` doesn't match
     `gh api user --jq .login`), suggest posting a review.
   - For the user's own PR, local changes, or pasted text, suggest editing.
   - If the feedback came from comments already on the PR, suggest editing, because a review
     would repeat them.
3. **Edit:**

   ```bash
   python3 .../dashboard/apply.py RUN --dry-run     # show the diff
   python3 .../dashboard/apply.py RUN               # then write it
   ```

   - For the user's own PR, apply to their checkout of the head branch with `--root PATH`,
     not to the detached review worktree.
   - For pasted text, give back the revised text from `RUN/source/`.
   - Make approved structural changes (`fixNote` only) by hand.
   - Afterwards, run whatever validation the repository asks for.
4. **Review:**

   ```bash
   python3 .../dashboard/review.py RUN --summary "One-paragraph overview of the review."
   ```

   - Fixes inside the diff become inline suggestions.
   - When a fix's lines are outside the diff, the comment goes on the finding's first
     in-diff context lines, with the replacement as a code block. Otherwise it goes in the
     review body.
   - Show the user the printed preview, edit `RUN/review.json` if needed, and post it with the
     printed `gh api` command only after they confirm.

## 9. Clean up

When the user is finished:

- Stop the server with `serve.py stop RUN`.
- For a PR, remove the worktree with `git worktree remove /tmp/feedback-triage/pr-N/checkout`.
- Delete the run folder, or tell the user it's there.

The server also stops on its own after 12 idle hours, or within a minute of its run folder
being deleted.
