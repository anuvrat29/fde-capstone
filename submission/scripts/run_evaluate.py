#!/usr/bin/env python3
"""One-command evaluation helpers for the AEGIS-INSURE submission.

Usage:
    python submission/scripts/run_evaluate.py

Runs the supplied offline fixture/contract validators. Fixture execution
results live in submission/evaluation/public_fixture_results.csv; release
gates live in submission/evaluation/release_gates.md.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _run(cmd: list[str]) -> int:
    print("+", " ".join(cmd), flush=True)
    completed = subprocess.run(cmd, cwd=ROOT)
    return int(completed.returncode)


def main() -> int:
    steps = [
        [sys.executable, str(ROOT / "evaluation" / "validate_fixtures.py")],
        [sys.executable, str(ROOT / "evaluation" / "validate_contracts.py")],
    ]
    for cmd in steps:
        code = _run(cmd)
        if code != 0:
            print(f"error: evaluate step failed with exit {code}", file=sys.stderr)
            return code

    results = ROOT / "submission" / "evaluation" / "public_fixture_results.csv"
    gates = ROOT / "submission" / "evaluation" / "release_gates.md"
    if not results.exists():
        print(f"warning: missing {results.relative_to(ROOT)}", file=sys.stderr)
        return 1
    if not gates.exists():
        print(f"warning: missing {gates.relative_to(ROOT)}", file=sys.stderr)
        return 1

    print("EVALUATE PASS — validators OK; fixture results and release gates present.")
    print("Re-run individual fixtures via submission/scripts/run_workflow_{a,b,c}.py")
    print("or the Taipy UI: python submission/scripts/run_taipy.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
