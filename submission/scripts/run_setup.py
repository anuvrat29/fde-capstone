#!/usr/bin/env python3
"""One-command setup for the AEGIS-INSURE submission (Python + Taipy only).

Usage:
    python submission/scripts/run_setup.py

Verifies package integrity and the writable submission scaffold. Does not
install Node.js or any npm packages — the interactive UI is Taipy
(submission/app_taipy/). Optional third-party wheels (taipy, anthropic) are
documented in submission/runbooks/SETUP.md.
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
        [sys.executable, str(ROOT / "run_capstone.py")],
        [sys.executable, str(ROOT / "tools" / "check_submission.py"), "--mode", "scaffold"],
    ]
    for cmd in steps:
        code = _run(cmd)
        if code != 0:
            print(f"error: setup step failed with exit {code}", file=sys.stderr)
            return code
    print("SETUP PASS — Python/Taipy submission scaffold is ready.")
    print("Optional UI: install taipy (and optionally anthropic), then:")
    print("  python submission/scripts/run_taipy.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
