#!/usr/bin/env python3
"""One-command launcher for the Taipy interactive UI.

Usage:
    python submission/scripts/run_taipy.py

Requires the `taipy` package. Optional CLAUDE_KEY in repo-root .env enables
GEN-SUM-3 paraphrasing via submission/app_taipy/llm_summary.py; without it the
UI falls back to deterministic template summaries.
"""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAIN = ROOT / "submission" / "app_taipy" / "main.py"


def main() -> int:
    if not MAIN.exists():
        print(f"error: Taipy app not found: {MAIN}", file=sys.stderr)
        return 1
    try:
        import taipy  # noqa: F401
    except ImportError:
        print(
            "error: taipy is not installed. Install with:\n"
            "  pip install taipy\n"
            "Then re-run this script. Node.js/npm is not used.",
            file=sys.stderr,
        )
        return 1
    runpy.run_path(str(MAIN), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
