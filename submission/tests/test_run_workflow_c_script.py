"""Tests for submission/scripts/run_workflow_c.py, the one-command launcher
required by submission/runbooks/RUN.md.

Covers: successful run against a public fixture, correct non-zero exit for a
wrong-workflow fixture, and correct non-zero exit for a missing fixture file
(fail-closed behaviour rather than a silent/partial result).
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "submission" / "scripts" / "run_workflow_c.py"


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )


class TestRunWorkflowCScript(unittest.TestCase):
    def test_successful_run_exits_zero_and_prints_valid_json(self):
        result = _run(["--fixture", "evaluation/fixtures/EV-11/fixture.json"])
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["workflow"], "catastrophe_reinsurance_planning")
        self.assertEqual(payload["case_id"], "EV-11")

    def test_wrong_workflow_fixture_fails_closed(self):
        result = _run(["--fixture", "evaluation/fixtures/EV-01/fixture.json"])  # coverage_claim_reconciliation
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("is not", result.stderr)

    def test_missing_fixture_file_fails_closed(self):
        result = _run(["--fixture", "evaluation/fixtures/EV-99/fixture.json"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not found", result.stderr)

    def test_out_flag_writes_file(self):
        out_path = ROOT / "submission" / "tests" / "_scratch_ev11_output.json"
        try:
            result = _run([
                "--fixture", "evaluation/fixtures/EV-11/fixture.json",
                "--out", str(out_path.relative_to(ROOT)),
            ])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(out_path.exists())
            payload = json.loads(out_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["case_id"], "EV-11")
        finally:
            if out_path.exists():
                out_path.unlink()


if __name__ == "__main__":
    unittest.main()
