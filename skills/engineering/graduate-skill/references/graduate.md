# Graduation steps

Start only from an approved proposal whose readiness decisions are settled. Rerun `scripts/survey.py copies <name>` first. If the copies changed since the proposal, update the proposal and confirm it again.

## 1. Prepare both repos

If the source copy has `modified` or `uncommitted` changes in the incubator, commit them there, staging only that skill's paths. Committing lets the imported history include them, and lets step 5 remove the copy with a plain `git rm`.

Follow the destination's own workflow. When it has a remote and works through pull requests, which its `AGENTS.md` or merged pull requests show, make the change on a branch in a worktree. Otherwise, commit on the default branch of its main checkout.

## 2. Import the skill

Keep history when the source copy has two or more commits and the destination keeps merge history. In a throwaway clone, rewrite the source to the destination path, then merge it:

```sh
tmp=$(mktemp -d)
git clone --no-local <source-repo> "$tmp/src"
git -C "$tmp/src" filter-repo --path <source-path>/ --path-rename <source-path>/:<dest-path>/
git -C <dest-checkout> fetch "$tmp/src" HEAD
git -C <dest-checkout> merge --allow-unrelated-histories --no-ff FETCH_HEAD \
  -m "feat(<domain>): graduate <skill> from <source-repo-name>"
```

Without `git filter-repo`, run `git subtree split --prefix=<source-path> -b graduate` in the clone instead, then `git subtree add --prefix=<dest-path> "$tmp/src" graduate` in the destination.

Copy the files instead, skipping `.DS_Store`, when the source has fewer than two commits, is untracked, or is a host copy, or when the destination squash-merges pull requests. Name the source path in the commit message.

Apply the approved readiness edits as separate commits after the import, so the history shows what changed for publishing.

## 3. Update the destination

- Add the skill to the manifests as the destination's rules require. A new domain folder usually needs its path in every plugin entry that should carry it, in every host's manifest.
- Add the skill's row to the README skill table, in its domain's position. When the destination has no table, update the listing it uses instead, such as a plugin README or a manifest description.
- Run the destination's validation, such as `claude plugin validate . --strict` for a Claude marketplace, and `git diff --check`.

## 4. Publish, with approval

Ask before pushing, opening a pull request, or releasing. Until the skill is on the default branch of the destination's main checkout, leave the old copy and its links in place so that hosts keep loading it. Report the graduation as pending the merge, and stop. After the merge, pull the main checkout and continue.

## 5. Retire the old copies

Confirm that the way the plan loads the graduated skill is available: the linking script from step 6, the destination's own link command, or an update of the installed plugin. If it isn't, stop before retiring anything, report what is missing, and leave the old copies serving. Don't create links by hand.

Confirm that the skill exists in the destination's main checkout, not only in a worktree, on its default branch. Confirm that the graduated copy matches the source, apart from the approved edits. Then retire every old copy before linking. The linking script refuses names it doesn't manage, and hosts that read the incubator directly would otherwise load two copies.

- **Links:** remove each `link` entry from the survey that points at an old copy. Remove only the symlink, with `rm <link>`, never recursively.
- **Incubator copy:** run `git -C <incubator> rm -r <source-path>` and commit `chore: graduate <skill> to <destination repo>`. Step 1 left no uncommitted changes, so this needs no force.
- **Host copies:** move a copy to the Trash, with `trash <path>` on macOS, when its digest matches the source. When it differs, show the difference and ask.
- **Claude-synced copies:** the Claude app restores these, so local removal doesn't last. Ask the user to remove the skill from their Claude account's skills.
- **Copies in other repos,** such as a retired fork: report them and ask.

## 6. Load the graduated skill

When the plan updates an installed plugin instead of linking, run the update the destination documents, then go to step 7.

When the plan uses the destination's own link command, run it as the destination documents, then go to step 7.

Otherwise, link the skill with the shared linking script, `scripts/skill-links.py`, from the main checkout of the skills repo that holds this skill. Find that repo by resolving this skill's directory with `realpath`, then take the first entry of `git worktree list`. The script works on any plugin repo, and its links always point at the destination's main checkout:

```sh
python3 <skills-repo>/scripts/skill-links.py link <destination>/<dest-path>
python3 <skills-repo>/scripts/skill-links.py status <destination>/<dest-path>
```

`link` accepts one skill directory or a directory of skills. It links into `~/.claude/skills` and `~/.codex/skills`, which Cursor also reads. `unlink` removes the links it made under a path. Read the script's `--help` before running it, and follow it where it differs from this description.

The script refuses to link a skill while an unmanaged copy with the same name exists in any folder these hosts load or in an installed plugin. If it refuses, a copy you haven't handled is still in place. Find it in the survey and go back to its row in the proposal.

## 7. Verify

Rerun `scripts/survey.py copies <name>`. The result should show one `repo` copy in the destination's main checkout and no `incubator` copy. With development links, expect a `link` from each linked host folder that resolves to it, and no `plugin-install` copies. With an installed plugin, expect only that plugin's installed copies and no links. Report the final state, every commit made, anything still waiting on the user, and the pull request link if one exists.
