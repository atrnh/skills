---
name: graduate-skill
description: Use when a personal or incubating skill is ready to publish, or when a maintenance run proposes a graduation candidate with evidence. Moves the skill from an incubator such as `~/.agents/skills` or a host skill folder into a plugin repo. It picks the destination repo, domain folder, and plugin, and checks the skill for personal paths, names, and preferences. It leaves exactly one copy, updates manifests and the README skill table, and relinks Claude, Codex, and Cursor. Also use to plan or dry-run a graduation, or to find duplicate copies of a skill.
---

# Graduate skill

Move one skill from where it is being tested into a plugin repo, so that exactly one copy remains and every host loads that copy.

The work has two phases. **Propose** is read-only and ends with a written proposal. **Graduate** writes, and runs only after the user approves that proposal. Stop after Propose when the request asks for a plan or dry run, or when another agent invoked this skill, such as a maintenance run. In that case, ask no questions mid-run: put every open question in the proposal's decisions section and return the proposal.

## Inputs

- **The skill:** a name or a path.
- **A destination**, if the user named one: a repo, and possibly a domain folder or plugin.
- **Evidence**, if a maintenance run supplied it: how often the skill fires, when it last needed a correction, and its personal-detail scan. Record the evidence in the proposal, but run the readiness check yourself instead of relying on the scan. When an agent invocation omits evidence, mark it as missing.

## Propose

### 1. Survey every copy

From this skill's directory, run `python3 scripts/survey.py copies <name>` and `python3 scripts/survey.py repos`. Both are read-only and print JSON.

- `copies` lists every directory and symlink with the skill's name in the incubator, host skill folders, Claude's synced folder, plugin install caches, and plugin repos. `kind` is `incubator`, `link`, `host-copy`, `claude-sync`, `plugin-install`, or `repo`. `state` is `clean`, `modified`, `uncommitted` (added to git but never committed), or `untracked`. `commits` counts the commits that touch the copy. Copies with the same `digest` have identical contents. A `managed` key lists installer markers; its absence means none were found.
- `repos` lists the git repos that hold `.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`, or `.agents/plugins/` manifests at any depth. Each entry gives the remote, plugins, manifest authors, skill count, and `user_commits`, the number of commits by the current git user.

Hosts can also read the incubator directly; Cursor and Codex load `~/.agents/skills`. Treat the incubator copy as a live load, not as storage.

The survey matches by name, so it misses a skill that a repo renamed or that already does the same job. Compare the skill's description with the descriptions of the candidate destination's skills, including those on its open pull requests and unmerged branches. Extend an existing skill rather than adding a second one that covers the same work.

Choose the source copy. When copies differ, diff them and list what each has that the others lack. When more than one copy has changes the others lack, ask which is canonical.

Stop and recommend against graduating when the skill is not the user's to publish. Signs include a `managed` entry (a skills CLI lock or an installer marker), copies that exist only as plugin installs, or an upstream author or license. A skill adapted from someone else's can graduate only with its original license file beside its `SKILL.md`, and only when the destination's rules allow adapted skills.

List dependencies: other skills the skill names or loads, and shared files outside its folder. Each dependency must graduate with it, already exist in the destination, or be removed from the skill. A dependency that graduates with it needs its own survey and readiness check. Say when it lacks maintenance evidence of its own. Name any other skills that also rely on it, and say whether they will still find it after it moves.

### 2. Check readiness

Read every file in the skill and look for:

- **Personal paths:** absolute home paths, `~/` paths into personal folders, and named vaults, projects, or courses.
- **Identity:** the user's name, handles, email addresses, employer, hostnames, and account, course, or tenant IDs.
- **Personal preferences:** defaults that encode one person's taste or habits rather than what the task needs, such as tone, delivery mode, or tools the user happens to use.
- **Destination conventions:** name uniqueness, name prefixes, description style, and project-specific syntax the destination keeps out of its skills. Take these rules from the destination's `AGENTS.md` and README. When it has neither, follow the conventions its existing skills share.

For each finding, give its location, why it blocks publishing, and a generic replacement. Move preferences out of the skill. Options the skill itself offers belong in a preferences file the skill reads, with a setup skill that saves them, the way `setup-fiction-skills` keeps delivery preferences outside the editors. Habits that span the user's work belong in the user's own mode skill. List mechanical fixes, such as replacing a path with a placeholder, in the plan. Ask before any substantive rewrite.

### 3. Choose the destination

Take the first rule that applies:

1. **The repo the user named.** If its rules don't fit the skill, say so in the proposal, but don't override the choice.
2. **An existing plugin repo that fits.** Candidates are the git repos from `survey.py repos` that the user maintains. Signs are `user_commits` above zero, or manifests or remotes that name the user or an organization the user works for. Repos by other authors are not candidates. Read each candidate's README and `AGENTS.md` for its domains and plugin split, and check its open pull requests and unmerged branches for plugins that aren't on its default branch yet. A repo fits when one of its domains covers the skill's primary audience and purpose, and when its ownership matches the skill's: work skills go to work repos, personal skills to personal repos. Choose the domain folder and the plugins that include it, following the repo's rules. A repo that its README or the user describes as retired or superseded doesn't fit.
3. **A new plugin repo**, when nothing fits. Propose a kebab-case name for the domain it would hold, a location beside the existing plugin repos, and manifests modeled on theirs.
4. **Ask**, when the choice is ambiguous. Examples include two repos that fit, a fit that needs a new domain folder, or unclear ownership. Recommend either an existing repo or a new repo with a proposed name.

### 4. Choose how hosts will load it

By default, hosts load the graduated skill through development links that the shared linking script, `scripts/skill-links.py`, creates, as [the graduation steps](references/graduate.md) describe. The script lives in the skills repo that holds this skill. Check that it is on that repo's default branch, for example with `git -C <main-checkout> ls-tree <default-branch> scripts/skill-links.py`. Find the main checkout as the first entry of `git worktree list`. If the script isn't there, the plan must stop before retiring any copy. When the destination documents its own link command, the plan may use that instead; ask which.

If the destination plugin is installed on this machine, a development link would load the skill twice. `plugin-install` copies from the survey show host plugin installs; confirm them with each host's plugin list, such as `claude plugin list`. Some repos also ship their own installer, which copies skills into host folders and records its own install state. Check the destination's README for one; its copies show up as `host-copy`. When the plugin is installed either way, the plan must either uninstall it and use development links, or skip development links and update the installed plugin. Ask which.

### 5. Write the proposal

Fill in [the proposal template](references/proposal.md) and present it. This ends Propose.

## Graduate

After the user approves the proposal, follow [the graduation steps](references/graduate.md).

## Limits

- Don't push, release, or open a pull request without asking. Local commits that the approved plan lists are fine.
- Don't install a published plugin on a machine that also has development links to it.
- Create development links only with the shared linking script or the destination's documented link command, never by hand.
- Don't delete a copy that differs from the graduated one until the user has seen the difference and approved deleting it.
- Cover one skill per proposal. A dependency that must move with it joins that proposal.
