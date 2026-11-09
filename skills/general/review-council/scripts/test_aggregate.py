"""Tests for aggregate.py. Run with: python3 -m unittest test_aggregate"""

import json
import tempfile
import unittest
from pathlib import Path

import aggregate

MODE = Path(__file__).resolve().parent.parent / "references" / "modes" / "curriculum.md"
CODES = ["AC", "CO", "AU", "OB", "MM", "PR", "EX", "LA", "PD", "PF"]
QUOTE = "Run `python loop.py` to see the output."


class AggregateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.run = Path(self.tmp.name).resolve()
        (self.run / "reviews").mkdir()
        self.lab = self.run / "source" / "lab.md"
        self.lab.parent.mkdir()
        self.lab.write_text("# Lab\nRun `python loop.py`   to see the output.\n")
        self.other = self.run / "unlisted.md"
        self.other.write_text(QUOTE)
        for name in ("brief.md", "context.md"):
            (self.run / name).write_text(name)
        self.write("sources.json", {"artifact": [str(self.lab.parent)], "context": []})
        self.panel(["openai", "anthropic", "google"])

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, data):
        (self.run / name).write_text(json.dumps(data))

    def panel(self, ids):
        self.write("panel.json", {"reviewers": [{"id": rid} for rid in ids]})

    def review(self, rid, overrides=None, file=None, entries=None, log_length=3):
        overrides = overrides or {}
        log = [{"location": {"file": str(self.lab), "quote": QUOTE}, "note": "n"}] * log_length
        scores = entries if entries is not None else [
            {
                "criterion": code,
                "score": overrides.get(code, 8),
                "evidence": [{"file": str(file or self.lab), "quote": QUOTE}],
            }
            for code in CODES
        ]
        self.write(f"reviews/{rid}.json", {"reviewer": rid, "readingLog": log, "scores": scores})

    def aggregate(self):
        return aggregate.aggregate(self.run, MODE)

    def test_complete_run_is_ready(self):
        for rid in ("openai", "anthropic", "google"):
            self.review(rid)
        out = self.aggregate()
        self.assertTrue(out["valid"] and out["complete"])
        self.assertEqual(out["verdict"], "ready")
        self.assertEqual(out["councilScore"], 8)
        self.assertEqual(out["problems"], [])
        self.assertIn("aggregator", out["inputs"])
        self.assertEqual(list(out["inputs"]["sources"]), [str(self.lab)])

    def test_malformed_entries_are_reported_not_fatal(self):
        self.review("openai", entries=[None, {"criterion": "AC", "score": []}])
        self.review("anthropic", entries=[{"criterion": ["AC"], "score": 8}])
        self.review("google", {"AC": 7.0})
        out = self.aggregate()
        text = "\n".join(out["problems"])
        self.assertIn("openai: score entry 1 is not an object", text)
        self.assertIn("openai AC: score [] is not allowed", text)
        self.assertIn("anthropic: unknown criterion ['AC']", text)
        self.assertIn("google AC: score 7.0 is not allowed", text)

    def test_below_quorum_publishes_no_score(self):
        self.review("openai")
        self.review("anthropic")
        out = self.aggregate()
        self.assertFalse(out["valid"])
        self.assertEqual(out["verdict"], "invalid")
        self.assertEqual(out["finalVerdict"], "invalid")
        self.assertIsNone(out["councilScore"])
        saved = json.loads((self.run / "scores.json").read_text())
        self.assertIsNone(saved["councilScore"])

    def test_unassessed_criterion_makes_run_incomplete(self):
        for rid in ("openai", "anthropic", "google"):
            self.review(rid, {"PD": "cannot_assess"})
        out = self.aggregate()
        self.assertEqual(out["criteria"]["PD"]["status"], "insufficient")
        self.assertEqual(out["verdict"], "incomplete")
        self.assertIsNone(out["councilScore"])
        self.assertEqual(out["partialScore"], 8)

    def test_not_applicable_criterion_is_left_out(self):
        for rid in ("openai", "anthropic", "google"):
            self.review(rid, {"PF": "na"})
        out = self.aggregate()
        self.assertTrue(out["complete"])
        self.assertNotIn("PF", out["applicable"])

    def test_failing_gate_outranks_incomplete(self):
        for rid in ("openai", "anthropic", "google"):
            self.review(rid, {"AC": 5, "PD": "cannot_assess"})
        self.assertEqual(self.aggregate()["verdict"], "not_ready")

    def test_flags(self):
        self.review("openai", {"AC": 6, "EX": 9, "LA": 3, "PF": "na"})
        self.review("anthropic", {"AC": 7, "EX": 5, "LA": 4, "PF": "na"})
        self.review("google", {"LA": 4, "PF": 8})
        criteria = self.aggregate()["criteria"]
        self.assertEqual(criteria["AC"]["flags"], ["gate"])
        self.assertEqual(criteria["EX"]["flags"], ["bands"])
        self.assertEqual(criteria["LA"]["flags"], ["failing"])
        self.assertEqual(criteria["PF"]["flags"], ["applicability"])
        self.assertEqual(criteria["PF"]["status"], "na")
        self.assertEqual(criteria["CO"]["flags"], [])

    def test_quote_from_unlisted_file_is_rejected(self):
        self.review("openai", file=self.other)
        self.review("anthropic")
        self.review("google")
        out = self.aggregate()
        self.assertNotIn("openai", out["reviewers"])
        self.assertIn("is not listed in sources.json", "\n".join(out["problems"]))

    def test_blocker_overrides_final_verdict_only(self):
        for rid in ("openai", "anthropic", "google"):
            self.review(rid)
        self.write("blockers.json", [{"finding": "AC1", "reason": "Step 3 fails."}])
        out = self.aggregate()
        self.assertEqual(out["verdict"], "ready")
        self.assertEqual(out["finalVerdict"], "not_ready")
        self.assertEqual(out["councilScore"], 8)

    def test_short_reading_log_is_reported_without_dropping_scores(self):
        self.review("openai", log_length=1)
        self.review("anthropic")
        self.review("google")
        out = self.aggregate()
        self.assertIn("openai: reading log has 1 entries, not 3 to 6", out["problems"])
        self.assertIn("openai", out["reviewers"])

    def test_mismatched_reviewer_name_is_reported(self):
        self.review("openai")
        self.review("anthropic")
        self.review("google")
        self.write("reviews/google.json", {"reviewer": "gemini", "scores": []})
        out = self.aggregate()
        self.assertIn("google: review names its reviewer 'gemini'", out["problems"])


if __name__ == "__main__":
    unittest.main()
