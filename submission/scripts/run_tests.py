#!/usr/bin/env python3
"""One-command test runner for the AEGIS-INSURE submission.

Usage:
    python submission/scripts/run_tests.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    cmd = [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        str(ROOT / "submission" / "tests"),
        "-p",
        "test_*.py",
        "-v",
    ]
    print("+", " ".join(cmd), flush=True)
    completed = subprocess.run(cmd, cwd=ROOT)
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
