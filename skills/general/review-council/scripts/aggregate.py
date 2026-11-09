#!/usr/bin/env python3
"""Check a council's reviews and combine their scores into RUN/scores.json.

Usage: aggregate.py RUN --mode MODE_FILE

Implements the "Combining scores" and "Verdict" sections of references/scoring.md.
"""

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

ALLOWED = {*range(1, 11), "na", "cannot_assess"}
BANDS = ((1, 3), (4, 6), (7, 8), (9, 10))
ROW = re.compile(r"^\|\s*([A-Z]{2})\s*\|\s*([^|]+?)\s*\|\s*(yes)?\s*\|\s*$")
VERSION = re.compile(r"^Version:\s*(\S+)\s*$", re.MULTILINE)
MIN_REVIEWS = 3


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


def squash(text):
    return " ".join(text.split())


def quote_found(item, run, cache):
    file, quote = item.get("file"), item.get("quote")
    if not isinstance(file, str) or not isinstance(quote, str) or not quote.strip():
        return False
    path = Path(file) if Path(file).is_absolute() else run / file
    if path not in cache:
        try:
            cache[path] = squash(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError):
            cache[path] = None
    return cache[path] is not None and squash(quote) in cache[path]


def check_review(rid, review, criteria, run, cache, problems):
    """Return {criterion: score} for the scores that pass every check."""
    valid, seen = {}, set()
    for entry in review.get("scores") or []:
        code, score = entry.get("criterion"), entry.get("score")
        if code not in criteria:
            problems.append(f"{rid}: unknown criterion {code!r}")
            continue
        if code in seen:
            problems.append(f"{rid} {code}: scored more than once; kept the first")
            continue
        seen.add(code)
        if isinstance(score, bool) or score not in ALLOWED:
            problems.append(f"{rid} {code}: score {score!r} is not allowed")
            continue
        if isinstance(score, int):
            evidence = entry.get("evidence") or []
            found = [quote_found(item, run, cache) for item in evidence]
            if not any(found):
                problems.append(f"{rid} {code}: no quote found in its cited file; score dropped")
                continue
            if not all(found):
                problems.append(f"{rid} {code}: {found.count(False)} quote(s) not found")
        valid[code] = score
    for code in criteria.keys() - seen:
        problems.append(f"{rid} {code}: not scored")
    return valid


def band(score):
    return next(i for i, (low, high) in enumerate(BANDS) if low <= score <= high)


def combine(criteria, valid):
    results = {}
    for code, info in criteria.items():
        answers = {rid: scores[code] for rid, scores in valid.items() if code in scores}
        numbers = [s for s in answers.values() if isinstance(s, int)]
        result = {**info, "scores": answers}
        if list(answers.values()).count("na") * 2 > len(answers):
            result["status"] = "na"
        elif len(numbers) < 2:
            result["status"] = "insufficient"
        else:
            result.update(
                status="scored",
                median=statistics.median(numbers),
                min=min(numbers),
                max=max(numbers),
                spread=max(numbers) - min(numbers),
            )
            result["disagreement"] = band(max(numbers)) - band(min(numbers)) >= 2
        results[code] = result
    return results


def verdict(results):
    scored = [r for r in results.values() if r["status"] == "scored"]
    gates = [r for r in results.values() if r["gate"]]
    if any(r["status"] == "scored" and r["median"] < 7 for r in gates) or any(
        r["median"] <= 3 for r in scored
    ):
        return "not_ready"
    if all(r["status"] == "scored" for r in gates) and all(r["median"] >= 7 for r in scored):
        return "ready"
    return "revise"


def table(results, reviewers):
    head = ["Criterion", *reviewers, "Median", "Spread"]
    lines = ["| " + " | ".join(head) + " |", "|" + " --- |" * len(head)]
    for code, r in results.items():
        name = f"{code} {r['name']}" + (" (gate)" if r["gate"] else "")
        cells = [str(r["scores"].get(rid, "-")) for rid in reviewers]
        if r["status"] == "scored":
            flag = " (disagreement)" if r["disagreement"] else ""
            tail = [f"{r['median']:g}", f"{r['spread']}{flag}"]
        else:
            tail = [r["status"], ""]
        lines.append("| " + " | ".join([name, *cells, *tail]) + " |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run", type=Path)
    parser.add_argument("--mode", type=Path, required=True)
    args = parser.parse_args()
    run = args.run.resolve()

    version, criteria = read_mode(args.mode)
    panel = json.loads((run / "panel.json").read_text(encoding="utf-8"))
    expected = [r["id"] for r in panel["reviewers"]]

    problems, valid, cache = [], {}, {}
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
        scores = check_review(rid, review, criteria, run, cache, problems)
        if scores:
            valid[rid] = scores
        else:
            problems.append(f"{rid}: no valid scores; review left out")

    results = combine(criteria, valid)
    medians = [r["median"] for r in results.values() if r["status"] == "scored"]
    out = {
        "mode": args.mode.stem,
        "rubricVersion": version,
        "reviewers": list(valid),
        "missingReviewers": [rid for rid in expected if rid not in valid],
        "councilScore": round(statistics.mean(medians), 2) if medians else None,
        "verdict": verdict(results),
        "criteria": results,
        "problems": problems,
    }
    (run / "scores.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    print(table(results, list(valid)))
    print(f"\nCouncil score: {out['councilScore']}  Verdict: {out['verdict']}")
    if problems:
        print("\nProblems:\n" + "\n".join(f"- {p}" for p in problems))
    if len(valid) < MIN_REVIEWS:
        sys.exit(f"\nOnly {len(valid)} usable reviews; the council needs {MIN_REVIEWS}.")


if __name__ == "__main__":
    main()
