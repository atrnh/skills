#!/usr/bin/env python3
"""Link a plugin repository's skills into Claude Code and Codex for live editing.

Usage:
  skill-links.py link PATH     Link every skill under PATH.
  skill-links.py unlink PATH   Remove the links that point under PATH.
  skill-links.py status PATH   Show where each skill under PATH resolves.

PATH is a skill directory, or a directory of skills, in any checkout of a git
repository. Links always point at the repository's main checkout, so a
worktree can be removed without breaking them.

Each skill gets an absolute symlink in ~/.claude/skills and ~/.codex/skills
(or under CLAUDE_CONFIG_DIR and CODEX_HOME). Cursor loads both folders, so it
needs no links of its own.

The script manages only symlinks that resolve inside the main checkout. It
refuses to link a skill while an unmanaged skill of the same name exists in a
linked folder, another folder these hosts load, or an installed plugin.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "__pycache__"}


def fail(message):
    sys.exit(f"skill-links: {message}")


def git(path, *args):
    result = subprocess.run(["git", "-C", str(path), *args], capture_output=True, text=True)
    if result.returncode != 0:
        fail(f"{path} is not inside a git repository")
    return result.stdout.strip()


def resolve_scope(path):
    """Return the main checkout and PATH's equivalent inside it."""
    path = Path(path).resolve()
    if not path.is_dir():
        fail(f"{path} is not a directory")
    toplevel = Path(git(path, "rev-parse", "--show-toplevel")).resolve()
    common_dir = Path(git(path, "rev-parse", "--path-format=absolute", "--git-common-dir"))
    if common_dir.name != ".git":
        fail(f"cannot find a main checkout for {toplevel}")
    checkout = common_dir.parent.resolve()
    return checkout, checkout / path.relative_to(toplevel), path


def skill_dirs(root):
    """Yield each directory under root that contains a SKILL.md, without descending into it."""
    for current, dirs, files in os.walk(root):
        if "SKILL.md" in files:
            dirs.clear()
            yield Path(current)
        else:
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]


def find_skills(root):
    skills = {}
    for directory in skill_dirs(root):
        if directory.name in skills:
            fail(f"two skills are named {directory.name}: {skills[directory.name]} and {directory}")
        skills[directory.name] = directory
    return skills


def is_within(path, root):
    return path == root or root in path.parents


def resolves_within(entry, root):
    return entry.is_symlink() and is_within(Path(os.path.realpath(entry)), root)


def home_dir(variable, default):
    return Path(os.environ.get(variable) or Path.home() / default)


def link_dirs():
    return {
        "claude": home_dir("CLAUDE_CONFIG_DIR", ".claude") / "skills",
        "codex": home_dir("CODEX_HOME", ".codex") / "skills",
    }


def other_skill_dirs():
    """Folders that Codex or Cursor also load skills from."""
    claude_synced = home_dir("CLAUDE_CONFIG_DIR", ".claude") / "skills" / "synced"
    return [Path.home() / ".agents" / "skills", Path.home() / ".cursor" / "skills",
            *sorted(p for p in claude_synced.glob("*") if p.is_dir())]


def read_json(path):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return {}


def declared_skill_dirs(root, manifest, entry=None):
    """Yield the skills an installed plugin loads, from its marketplace entry or its manifest.

    Installed copies can contain skills the plugin doesn't load, such as the
    rest of a repository whose marketplace splits it into several plugins.
    """
    paths = (entry or {}).get("skills") or read_json(root / manifest).get("skills") or "skills"
    for path in [paths] if isinstance(paths, str) else paths:
        yield from skill_dirs(root / path)


def claude_plugin_skills():
    plugins = home_dir("CLAUDE_CONFIG_DIR", ".claude") / "plugins"
    enabled = read_json(plugins.parent / "settings.json").get("enabledPlugins", {})
    marketplaces = read_json(plugins / "known_marketplaces.json")
    for key, installs in read_json(plugins / "installed_plugins.json").get("plugins", {}).items():
        if not enabled.get(key, True):
            continue
        name, _, marketplace = key.partition("@")
        location = marketplaces.get(marketplace, {}).get("installLocation")
        catalog = read_json(Path(location) / ".claude-plugin" / "marketplace.json") if location else {}
        entry = next((p for p in catalog.get("plugins", []) if p.get("name") == name), None)
        for install in installs:
            if install.get("installPath"):
                yield from declared_skill_dirs(Path(install["installPath"]), ".claude-plugin/plugin.json", entry)


def codex_plugin_skills():
    codex = home_dir("CODEX_HOME", ".codex")
    try:
        config = (codex / "config.toml").read_text()
    except OSError:
        return
    plugin = None
    for line in config.splitlines():
        header = re.match(r"""\s*\[plugins\.["']([^"'@]+)@([^"']+)["']\]\s*$""", line)
        if header:
            plugin = header.groups()
        elif line.lstrip().startswith("["):
            plugin = None
        elif plugin and re.match(r"\s*enabled\s*=\s*true\b", line):
            for root in sorted((codex / "plugins" / "cache" / plugin[1] / plugin[0]).glob("*")):
                yield from declared_skill_dirs(root, ".codex-plugin/plugin.json")


def cursor_plugin_skills():
    plugins = Path.home() / ".cursor" / "plugins"
    for root in sorted(plugins.glob("cache/*/*/*")) + sorted(plugins.glob("local/*")):
        yield from declared_skill_dirs(root, ".cursor-plugin/plugin.json")


def installed_copies(names, checkout):
    """Find skills with these names that a host would also load from somewhere else."""
    copies = []
    for directory in other_skill_dirs():
        for name in names:
            entry = directory / name
            if entry.exists() or entry.is_symlink():
                copies.append((name, entry))
    for plugin_skills in (claude_plugin_skills, codex_plugin_skills, cursor_plugin_skills):
        for directory in plugin_skills():
            if directory.name in names and not is_within(directory.resolve(), checkout):
                copies.append((directory.name, directory))
    return copies


def describe(entry):
    if entry.is_symlink():
        target = os.path.realpath(entry)
        return target if os.path.exists(target) else f"{target} (missing)"
    return "a directory" if entry.is_dir() else "a file"


def link(args):
    checkout, scope, given = resolve_scope(args.path)
    if not scope.is_dir():
        fail(f"{scope} does not exist in the main checkout yet; merge first")
    skills = find_skills(scope)
    if not skills:
        fail(f"no skills found under {scope}")
    for name in sorted(set(find_skills(given)) - set(skills)):
        print(f"Skipping {name}: it is not in the main checkout yet.")

    problems = []
    for host, directory in link_dirs().items():
        for name in skills:
            entry = directory / name
            if (entry.exists() or entry.is_symlink()) and not resolves_within(entry, checkout):
                problems.append(f"{host}: {entry} already exists and resolves to {describe(entry)}")
    for name, copy in installed_copies(set(skills), checkout):
        problems.append(f"{name} is also installed at {copy}")
    if problems:
        fail("refusing to link; resolve these first:\n  " + "\n  ".join(problems))

    for host, directory in link_dirs().items():
        directory.mkdir(parents=True, exist_ok=True)
        for entry in sorted(directory.iterdir()):
            if resolves_within(entry, scope) and skills.get(entry.name) != Path(os.path.realpath(entry)):
                entry.unlink()
                print(f"{host}: removed stale link {entry.name}")
        for name, source in sorted(skills.items()):
            entry = directory / name
            if entry.is_symlink() and Path(os.path.realpath(entry)) == source:
                continue
            temporary = directory / f".{name}.skill-link"
            if temporary.is_symlink():
                temporary.unlink()
            temporary.symlink_to(source, target_is_directory=True)
            os.replace(temporary, entry)
        print(f"{host}: linked {len(skills)} skills from {scope} into {directory}")


def unlink(args):
    _, scope, _ = resolve_scope(args.path)
    for host, directory in link_dirs().items():
        removed = []
        if directory.is_dir():
            for entry in sorted(directory.iterdir()):
                if resolves_within(entry, scope):
                    entry.unlink()
                    removed.append(entry.name)
        print(f"{host}: removed {len(removed)} links into {scope}" + (f": {', '.join(removed)}" if removed else ""))


def status(args):
    checkout, scope, _ = resolve_scope(args.path)
    skills = find_skills(scope)
    for host, directory in link_dirs().items():
        print(f"{host} ({directory}):")
        names = set(skills)
        if directory.is_dir():
            names.update(e.name for e in directory.iterdir() if resolves_within(e, scope))
        for name in sorted(names):
            entry = directory / name
            if not (entry.exists() or entry.is_symlink()):
                print(f"  {name}: not linked")
                continue
            if entry.is_symlink() and Path(os.path.realpath(entry)) == skills.get(name):
                state = "linked"
            elif resolves_within(entry, checkout):
                state = "stale link"
            else:
                state = "unmanaged"
            print(f"  {name}: {state} -> {describe(entry)}")
    copies = installed_copies(set(skills), checkout)
    print("Also loaded from:" if copies else "No other copies found.")
    for name, copy in copies:
        print(f"  {name}: {copy}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    for name, handler in (("link", link), ("unlink", unlink), ("status", status)):
        command = commands.add_parser(name)
        command.add_argument("path")
        command.set_defaults(handler=handler)
    args = parser.parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
