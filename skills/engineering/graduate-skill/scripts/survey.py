#!/usr/bin/env python3
"""Read-only survey of plugin repos and skill copies for graduate-skill.

    survey.py repos [--root DIR ...]
    survey.py copies NAME [--root DIR ...]
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

HOME = Path.home()
MANIFEST_DIRS = (".claude-plugin", ".codex-plugin", ".cursor-plugin")
PRUNE = {".git", "node_modules", "Library", ".Trash", ".venv"}
MANAGED_MARKERS = (".aws-skill-metadata", ".installed-version")


def skill_folders():
    codex = Path(os.environ.get("CODEX_HOME", HOME / ".codex"))
    return [HOME / ".agents/skills", HOME / ".claude/skills", codex / "skills",
            HOME / ".cursor/skills", HOME / ".copilot/skills"]


def plugin_caches():
    codex = Path(os.environ.get("CODEX_HOME", HOME / ".codex"))
    return [HOME / ".claude/plugins/cache", codex / "plugins/cache",
            HOME / ".cursor/plugins/cache", HOME / ".copilot/installed-plugins"]


def git(path, *args):
    result = subprocess.run(["git", "-C", str(path), *args],
                            capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def walk(root, max_depth, keep_hidden=()):
    root = Path(root)
    if not root.is_dir():
        return
    base = len(root.parts)
    for current, dirs, files in os.walk(root, followlinks=False):
        depth = len(Path(current).parts) - base
        dirs[:] = [d for d in dirs if d not in PRUNE
                   and (not d.startswith(".") or d in keep_hidden)
                   and depth < max_depth]
        yield Path(current), dirs, files


def is_manifest_dir(path):
    return path.name in MANIFEST_DIRS or path.parts[-2:] == (".agents", "plugins")


def is_skills_dir(path, dirs):
    """A repo's top-level `skills/` folder that holds skill folders directly, as repos without manifests use."""
    return (path.name == "skills" and (path.parent / ".git").exists()
            and any((path / d / "SKILL.md").is_file() for d in dirs))


def find_repos(roots):
    repos = set()
    for root in roots:
        for current, dirs, files in walk(root, 6, keep_hidden=(*MANIFEST_DIRS, ".agents")):
            if is_skills_dir(current, dirs) and not current.is_relative_to(HOME / ".agents"):
                repos.add(current.parent.resolve())
                continue
            if (not is_manifest_dir(current) or not any(f.endswith(".json") for f in files)
                    or current.is_relative_to(HOME / ".agents")):
                continue
            start = current.parent.parent if current.name == "plugins" else current.parent
            top = git(start, "rev-parse", "--show-toplevel")
            repos.add(Path(top).resolve() if top else start.resolve())
    return sorted(repos)


def read_json(path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


def describe_repo(repo):
    manifests, plugins, authors = [], [], set()
    for current, _, files in walk(repo, 4, keep_hidden=(*MANIFEST_DIRS, ".agents")):
        if not is_manifest_dir(current):
            continue
        for manifest in sorted(current / f for f in files if f.endswith(".json")):
            manifests.append(str(manifest.relative_to(repo)))
            data = read_json(manifest) or {}
            for plugin in data.get("plugins", [data] if "name" in data else []):
                plugins.append(plugin.get("name", "?"))
            for key in ("author", "owner"):
                if isinstance(data.get(key), dict):
                    authors.add(data[key].get("name", "?"))
    top = git(repo, "rev-parse", "--show-toplevel")
    email = git(repo, "config", "user.email") if top else None
    mine = git(repo, "rev-list", "--count", f"--author={email}", "HEAD") if email else None
    return {
        "repo": str(repo),
        "git": bool(top),
        "remote": git(repo, "remote", "get-url", "origin") if top else None,
        "branch": git(repo, "branch", "--show-current") if top else None,
        "dirty": bool(git(repo, "status", "--porcelain")) if top else None,
        "manifests": manifests,
        "plugins": sorted(set(plugins)),
        "authors": sorted(authors),
        "user_commits": int(mine or 0),
        "skills": sum(1 for _, _, files in walk(repo, 5) if "SKILL.md" in files),
    }


def frontmatter_name(skill_md):
    try:
        head = skill_md.read_text(errors="replace")[:2000]
    except OSError:
        return None
    match = re.search(r"^name:\s*['\"]?([^'\"\n]+)", head, re.MULTILINE)
    return match.group(1).strip() if match else None


def digest(directory):
    hasher = hashlib.sha256()
    for path in sorted(p for p in directory.rglob("*")
                       if p.is_file() and p.name != ".DS_Store"):
        hasher.update(str(path.relative_to(directory)).encode())
        hasher.update(path.read_bytes())
    return hasher.hexdigest()[:12]


def locked_skills():
    data = read_json(HOME / ".agents/.skill-lock.json") or {}
    return data.get("skills", {})


def classify(entry):
    if entry.is_symlink():
        return "link"
    if entry.is_relative_to(HOME / ".claude/skills/synced"):
        return "claude-sync"
    if any(entry.is_relative_to(cache) for cache in plugin_caches()):
        return "plugin-install"
    if entry.is_relative_to(HOME / ".agents/skills"):
        return "incubator"
    if any(entry.is_relative_to(folder) for folder in skill_folders()[1:]):
        return "host-copy"
    return "repo"


def describe_copy(entry, locks):
    resolved = entry.resolve()
    info = {"path": str(entry), "kind": classify(entry)}
    if entry.is_symlink():
        info["link"] = os.readlink(entry)
        info["resolves"] = str(resolved) if resolved.exists() else "DANGLING"
    if not resolved.is_dir():
        return info
    top = git(resolved, "rev-parse", "--show-toplevel")
    if top:
        tracked = git(resolved, "ls-files", "--", ".")
        changes = git(resolved, "status", "--porcelain", "--", ".")
        commits = git(resolved, "rev-list", "--count", "HEAD", "--", ".")
        info["git"] = top
        info["state"] = ("untracked" if not tracked
                         else "uncommitted" if commits == "0"
                         else "modified" if changes else "clean")
        info["commits"] = int(commits or 0)
    markers = [m for m in MANAGED_MARKERS if (resolved / m).exists()]
    markers += [p.name for p in resolved.glob(".managed-by-*")]
    if resolved.parent == (HOME / ".agents/skills").resolve() and resolved.name in locks:
        source = locks[resolved.name].get("source", "?")
        markers.append(f"skill-lock:{source}")
    if markers:
        info["managed"] = markers
    info["digest"] = digest(resolved)
    return info


def find_copies(name, roots):
    locks, seen, copies = locked_skills(), set(), []
    for root in skill_folders():
        for pattern in (name, f"*/{name}", f"*/*/{name}"):
            for entry in root.glob(pattern):
                if entry.is_symlink():
                    copies.append(describe_copy(entry, locks))
    for root in [*skill_folders(), *plugin_caches(), *roots]:
        for current, _, files in walk(root, 8):
            if "SKILL.md" not in files or current.resolve() in seen:
                continue
            if current.name == name or frontmatter_name(current / "SKILL.md") == name:
                seen.add(current.resolve())
                copies.append(describe_copy(current, locks))
    return copies


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    repos = sub.add_parser("repos", help="list skill repos found by manifest or top-level skills folder")
    repos.add_argument("--root", action="append", type=Path)
    copies = sub.add_parser("copies", help="list every copy and link of a skill")
    copies.add_argument("name")
    copies.add_argument("--root", action="append", type=Path)
    args = parser.parse_args()

    found = find_repos(args.root or [HOME])
    if args.command == "repos":
        result = [describe_repo(repo) for repo in found]
    else:
        result = find_copies(args.name, [*(args.root or []), *found])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
