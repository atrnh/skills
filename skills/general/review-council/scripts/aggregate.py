#!/usr/bin/env python3
"""Check a council's reviews and combine their scores into RUN/scores.json.

Usage: aggregate.py RUN --mode MODE_FILE

Implements the "Combining scores" and "Verdict" sections of references/scoring.md.
"""

import argparse
import hashlib
import json
import re
import statistics
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
WORDS = {"na", "cannot_assess"}
BANDS = ((1, 3), (4, 6), (7, 8), (9, 10))
GATE_LINE = 7
FAILING_LINE = 3
MIN_REVIEWS = 3
LOG_LENGTH = (3, 6)
ROW = re.compile(r"^\|\s*([A-Z]{2})\s*\|\s*([^|]+?)\s*\|\s*(yes)?\s*\|\s*$")
VERSION = re.compile(r"^Version:\s*(\S+)\s*$", re.MULTILINE)


def read_mode(path):
    text = path.read_text(encoding="utf-8")
    version = VERSION.search(text)
    if not version:
        sys.exit(f"{path}: no 'Version:' line")
    criteria = {}
    for line in text.splitlines():
        if line.startswith("## "):
            break
        row = ROW.match(line)
        if row:
            criteria[row[1]] = {"name": row[2], "gate": bool(row[3])}
    if not criteria:
        sys.exit(f"{path}: no criteria table above the first '## ' heading")
    return version[1], criteria


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"{path}: not found")
    except json.JSONDecodeError as error:
        sys.exit(f"{path}: not valid JSON ({error})")


def read_panel(run):
    panel = read_json(run / "panel.json")
    reviewers = panel.get("reviewers") if isinstance(panel, dict) else None
    if not isinstance(reviewers, list) or not reviewers:
        sys.exit("panel.json: needs a non-empty 'reviewers' list")
    ids = [r.get("id") if isinstance(r, dict) else None for r in reviewers]
    if not all(isinstance(rid, str) and rid for rid in ids):
        sys.exit("panel.json: every reviewer needs a string 'id'")
    if len(set(ids)) != len(ids):
        sys.exit("panel.json: reviewer IDs must be unique")
    return ids


def is_score(value):
    if isinstance(value, str):
        return value in WORDS
    return type(value) is int and 1 <= value <= 10


def band(score):
    return next(i for i, (low, high) in enumerate(BANDS) if low <= score <= high)


def squash(text):
    return " ".join(text.split())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Sources:
    """The files listed in RUN/sources.json, which evidence must come from."""

    def __init__(self, run):
        data = read_json(run / "sources.json")
        paths = []
        for key in ("artifact", "context"):
            value = data.get(key, []) if isinstance(data, dict) else None
            if not isinstance(value, list) or not all(isinstance(p, str) for p in value):
                sys.exit(f"sources.json: '{key}' must be a list of paths")
            paths += value
        if not data.get("artifact"):
            sys.exit("sources.json: 'artifact' must list at least one path")
        if not all(Path(p).is_absolute() for p in paths):
            sys.exit("sources.json: every path must be absolute")
        self.roots = [Path(p).resolve() for p in paths]
        self.text = {}

    def files(self):
        found = set()
        for root in self.roots:
            if root.is_dir():
                found.update(p for p in root.rglob("*") if p.is_file())
            elif root.is_file():
                found.add(root)
        return sorted(found)

    def problem(self, item):
        """Return why an evidence item fails, or None when its quote is found."""
        if not isinstance(item, dict):
            return "evidence item is not an object"
        file, quote = item.get("file"), item.get("quote")
        if not isinstance(file, str) or not isinstance(quote, str) or not quote.strip():
            return "evidence needs a file and a quote"
        path = Path(file)
        if not path.is_absolute():
            return f"{file} is not an absolute path"
        path = path.resolve()
        if not any(path == root or root in path.parents for root in self.roots):
            return f"{file} is not listed in sources.json"
        if path not in self.text:
            try:
                self.text[path] = squash(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError):
                self.text[path] = None
        if self.text[path] is None:
            return f"{file} can't be read as text"
        if squash(quote) not in self.text[path]:
            return f"quote not found in {file}"
        return None


def check_review(rid, review, criteria, sources, problems):
    """Return {criterion: answer} for the answers that pass every check."""
    if not isinstance(review, dict) or not isinstance(review.get("scores"), list):
        problems.append(f"{rid}: review has no list of scores")
        return {}
    if review.get("reviewer") != rid:
        problems.append(f"{rid}: review names its reviewer {review.get('reviewer')!r}")
    log = review.get("readingLog")
    if not isinstance(log, list) or not LOG_LENGTH[0] <= len(log) <= LOG_LENGTH[1]:
        size = len(log) if isinstance(log, list) else "no"
        problems.append(f"{rid}: reading log has {size} entries, not {LOG_LENGTH[0]} to {LOG_LENGTH[1]}")
    valid, seen = {}, set()
    for number, entry in enumerate(review["scores"], 1):
        if not isinstance(entry, dict):
            problems.append(f"{rid}: score entry {number} is not an object")
            continue
        code, score = entry.get("criterion"), entry.get("score")
        if not isinstance(code, str) or code not in criteria:
            problems.append(f"{rid}: unknown criterion {code!r}")
            continue
        if code in seen:
            problems.append(f"{rid} {code}: answered more than once; kept the first")
            continue
        seen.add(code)
        if not is_score(score):
            problems.append(f"{rid} {code}: score {score!r} is not allowed")
            continue
        if type(score) is int:
            evidence = entry.get("evidence")
            if not isinstance(evidence, list) or not evidence:
                problems.append(f"{rid} {code}: no evidence; score dropped")
                continue
            failures = [f for f in map(sources.problem, evidence) if f]
            if len(failures) == len(evidence):
                problems.append(f"{rid} {code}: no valid evidence ({failures[0]}); score dropped")
                continue
            if failures:
                problems.append(f"{rid} {code}: {len(failures)} evidence item(s) rejected ({failures[0]})")
        valid[code] = score
    for code in criteria:
        if code not in seen:
            problems.append(f"{rid} {code}: not answered")
    return valid


def combine(criteria, valid):
    usable = len(valid)
    results = {}
    for code, info in criteria.items():
        answers = {rid: scores[code] for rid, scores in valid.items() if code in scores}
        values = list(answers.values())
        numbers = [s for s in values if type(s) is int]
        not_applicable = values.count("na")
        result = {**info, "scores": answers, "flags": []}
        if not_applicable and numbers:
            result["flags"].append("applicability")
        if not_applicable * 2 > len(values):
            result["status"] = "na"
        elif len(numbers) >= 2 and len(numbers) * 2 >= usable:
            low, high = min(numbers), max(numbers)
            result.update(
                status="scored",
                median=statistics.median(numbers),
                min=low,
                max=high,
                spread=high - low,
            )
            if band(high) - band(low) >= 2:
                result["flags"].append("bands")
            if info["gate"] and low < GATE_LINE <= high:
                result["flags"].append("gate")
            if low <= FAILING_LINE < high:
                result["flags"].append("failing")
        else:
            result["status"] = "insufficient"
        result["disagreement"] = bool(result["flags"])
        results[code] = result
    return results


def verdict(results):
    scored = [r for r in results.values() if r["status"] == "scored"]
    if any(r["gate"] and r["median"] < GATE_LINE for r in scored) or any(
        r["median"] <= FAILING_LINE for r in scored
    ):
        return "not_ready"
    if not complete(results):
        return "incomplete"
    if all(r["median"] >= GATE_LINE for r in scored):
        return "ready"
    return "revise"


def complete(results):
    return all(
        r["status"] == "scored" or (r["status"] == "na" and not r["gate"])
        for r in results.values()
    )


def read_blockers(run):
    path = run / "blockers.json"
    if not path.exists():
        return []
    blockers = read_json(path)
    if not isinstance(blockers, list) or not all(
        isinstance(b, dict) and isinstance(b.get("finding"), str) and isinstance(b.get("reason"), str)
        for b in blockers
    ):
        sys.exit("blockers.json: must be a list of objects with 'finding' and 'reason'")
    return blockers


def fingerprint(run, mode, sources, problems):
    inputs = {"sources": {str(p): digest(p) for p in sources.files()}}
    for name, path in (
        ("brief", run / "brief.md"),
        ("context", run / "context.md"),
        ("rubric", mode),
        ("scoring", SKILL / "references" / "scoring.md"),
        ("aggregator", Path(__file__).resolve()),
    ):
        if path.is_file():
            inputs[name] = digest(path)
        else:
            inputs[name] = None
            problems.append(f"{path} not found; its fingerprint is missing")
    return inputs


def table(results, reviewers):
    head = ["Criterion", *reviewers, "Median", "Spread"]
    lines = ["| " + " | ".join(head) + " |", "|" + " --- |" * len(head)]
    for code, r in results.items():
        name = f"{code} {r['name']}" + (" (gate)" if r["gate"] else "")
        cells = [str(r["scores"].get(rid, "-")) for rid in reviewers]
        flags = f" ({', '.join(r['flags'])})" if r["flags"] else ""
        if r["status"] == "scored":
            tail = [f"{r['median']:g}", f"{r['spread']}{flags}"]
        else:
            tail = [r["status"], flags.strip()]
        lines.append("| " + " | ".join([name, *cells, *tail]) + " |")
    return "\n".join(lines)


def aggregate(run, mode):
    """Write RUN/scores.json and return it."""
    version, criteria = read_mode(mode)
    expected = read_panel(run)
    sources = Sources(run)

    problems, valid = [], {}
    for rid in expected:
        path = run / "reviews" / f"{rid}.json"
        try:
            review = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            problems.append(f"{rid}: no review")
            continue
        except json.JSONDecodeError as error:
            problems.append(f"{rid}: review is not valid JSON ({error})")
            continue
        answers = check_review(rid, review, criteria, sources, problems)
        if answers:
            valid[rid] = answers
        else:
            problems.append(f"{rid}: no valid answers; review left out")

    results = combine(criteria, valid)
    medians = [r["median"] for r in results.values() if r["status"] == "scored"]
    partial = round(statistics.mean(medians), 2) if medians else None
    is_valid = len(valid) >= MIN_REVIEWS
    is_complete = is_valid and complete(results)
    blockers = read_blockers(run)
    computed = verdict(results) if is_valid else "invalid"
    if not is_valid:
        problems.append(f"only {len(valid)} usable reviews; the council needs {MIN_REVIEWS}")

    out = {
        "mode": mode.stem,
        "rubricVersion": version,
        "valid": is_valid,
        "complete": is_complete,
        "verdict": computed,
        "blockers": blockers,
        "finalVerdict": "not_ready" if is_valid and blockers else computed,
        "councilScore": partial if is_complete else None,
        "partialScore": partial if is_valid else None,
        "applicable": [code for code, r in results.items() if r["status"] != "na"],
        "reviewers": list(valid),
        "missingReviewers": [rid for rid in expected if rid not in valid],
        "criteria": results,
        "inputs": fingerprint(run, mode, sources, problems),
        "problems": problems,
    }
    (run / "scores.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run", type=Path)
    parser.add_argument("--mode", type=Path, required=True)
    args = parser.parse_args()
    out = aggregate(args.run.resolve(), args.mode.resolve())

    print(table(out["criteria"], out["reviewers"]))
    print(
        f"\nCouncil score: {out['councilScore']}  Partial score: {out['partialScore']}"
        f"\nVerdict: {out['verdict']}  Final verdict: {out['finalVerdict']}"
    )
    if out["problems"]:
        print("\nProblems:\n" + "\n".join(f"- {p}" for p in out["problems"]))
    if not out["valid"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
