# Triage dashboard

The dashboard turns a finished review into a page where the user approves or rejects each
proposed fix. Each card shows the problem, its evidence, the case against changing it, the
affected lines in context, and the exact replacement. The scripts in `../dashboard/` need only
Python 3 and Git; posting a review also needs `gh`.

| Script | Does |
|---|---|
| `build.py RUN/findings.json [--check]` | Checks every finding against the files and writes `index.html` and `resolved.json` |
| `serve.py start RUN` / `stop RUN` | Serves the page on localhost and saves decisions to `RUN/decisions.json` |
| `apply.py RUN [--dry-run] [--root PATH]` | Applies approved fixes to the files |
| `review.py RUN --summary TEXT` | Drafts a GitHub review from approved fixes as `RUN/review.json` (doesn't post) |

`apply.py` and `review.py` read approvals from `decisions.json`. When the user pasted their
decisions into the chat instead, pass `--approve A1,C3,...`.

## 1. Make a run folder

Use `/tmp/dqr-triage/<slug>/`, for example `/tmp/dqr-triage/pr-619/` or
`/tmp/dqr-triage/launch-email/`. Everything for this review lives there.

## 2. Point at the source

Line numbers must come from the exact text the user will judge.

- **Pull request.** Check out the PR's head commit in its own worktree, so local edits on
  the user's branch can't shift lines:

  ```bash
  gh pr view N --json headRefOid,baseRefName
  git fetch origin <baseRefName> pull/N/head
  git worktree add --detach /tmp/dqr-triage/pr-N/checkout <headRefOid>
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

## 3. Write `findings.json`

One finding per item in the report, with the same ID. The cards are only as useful as their
fields:

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
  "title": "PR #619 deep-quality review",
  "source": {
    "kind": "pr",
    "root": "checkout",
    "label": "hackbrightacademy/csharp-curriculum#619",
    "url": "https://github.com/hackbrightacademy/csharp-curriculum/pull/619",
    "base": "origin/main"
  },
  "findings": [
    {
      "id": "A1",
      "category": "Accuracy",
      "priority": 1,
      "title": "Lecture intro says OIDC secures web APIs",
      "problem": "The intro says OpenID Connect \"secures web APIs.\" The OIDC slide teaches the opposite: the ID token is never sent to the API.",
      "evidence": [{"text": "OIDC slide, lines 707–715", "url": "https://..."}],
      "counter": "Handout-only sentence; \"secure\" could be read loosely.",
      "comment": "",
      "context": [
        {"file": "contents/lectures/jm-auth/index.rst", "match": "OpenID Connect secure web APIs"},
        {"file": "contents/lectures/jm-auth/index.rst", "start": 706, "end": 715,
         "highlight": [714, 715], "label": "The lecture's own claim"}
      ],
      "fixes": [
        {"file": "contents/lectures/jm-auth/index.rst", "start": 9, "end": 10,
         "replacement": "   Learn how to ...\n   Core Identity, how web APIs use bearer tokens ..."}
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

Use the report's category names and ID letters: A Accuracy, M Completeness, C Consistency,
U Usefulness, P Precision, D Deep quality. Priority 1 misleads the reader or breaks the
material, 2 noticeably hurts it, 3 is polish.

## 4. Build and check

```bash
python3 .../dashboard/build.py RUN/findings.json --check
```

Errors block the build: a missing or ambiguous quote, a line outside the file, a duplicate
ID, a fix that overlaps another fix in the same finding. `--check` prints every highlighted
line and every line a fix replaces, so read it and confirm each one is the line you meant.
Then deal with the warnings:

- **Blank highlighted lines** usually mean a line-number slip.
- **Two findings changing the same lines** can both stay, but mention the conflict in each
  one's `fixNote`.
- **A file that differs from HEAD** means its GitHub links won't match the snippets.

## 5. Launch

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
and the user copies the Markdown at the bottom into the chat.

Tell the user:

- the URL;
- how to decide: Approve or Reject on each card, an optional note to adjust a fix, and the
  keys `a`, `r`, `u`, `j`, `k`, and `Enter`;
- that decisions are saved as they go, so they only need to say when they're done;
- which fixes deserve a close look, such as diagrams, generated files, or anything you
  couldn't render or verify.

## 6. Act on the decisions

When the user says they're done, read `RUN/decisions.json`.

1. **Notes first.** A note on an approved finding may change its fix. Update that finding in
   `findings.json`, rebuild, and pass `--notes-handled` from then on. The scripts refuse to run
   until you do. If a note asks a question, answer it before applying anything.
2. **Ask how to apply them, with a default.** Offer to edit the files or to post a GitHub review.
   - If the PR belongs to someone else (`gh pr view N --json author` doesn't match
     `gh api user --jq .login`), suggest posting a review.
   - For the user's own PR, local changes, or pasted text, suggest editing.
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

## 7. Clean up

When the user is finished:

- Stop the server with `serve.py stop RUN`.
- For a PR, remove the worktree with `git worktree remove /tmp/dqr-triage/pr-N/checkout`.
- Delete the run folder, or tell the user it's there.

The server also stops on its own after 12 idle hours, or within a minute of its run folder
being deleted.
