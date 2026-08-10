#!/usr/bin/env python3
"""Reset participant-generated runtime state under submission/ only.

Usage:
    python submission/scripts/reset_submission.py

Removes caches, logs, __pycache__, and leftover Node/API experiment folders
if present. Never deletes supplied challenge evidence outside submission/.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUBMISSION = ROOT / "submission"

# Runtime leftovers only — never wipe source, artefacts, evidence, or tests.
ORPHAN_DIRS = (
    SUBMISSION / "web",
    SUBMISSION / "api",
)
CACHE_NAMES = {"__pycache__", ".pytest_cache", ".cache", "node_modules", "dist", ".vite"}
CACHE_SUFFIXES = {".cache", ".log", ".pyc", ".pyo"}


def _rm_tree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
        print(f"removed: {path.relative_to(ROOT)}")


def main() -> int:
    if not SUBMISSION.is_dir():
        print("error: submission/ not found", file=sys.stderr)
        return 1

    for orphan in ORPHAN_DIRS:
        _rm_tree(orphan)

    hashes = SUBMISSION / "evidence" / "submission_hashes.csv"
    if hashes.exists():
        hashes.unlink()
        print(f"removed: {hashes.relative_to(ROOT)}")

    for path in SUBMISSION.rglob("*"):
        if path.is_dir() and path.name in CACHE_NAMES:
            _rm_tree(path)
        elif path.is_file() and path.suffix in CACHE_SUFFIXES:
            path.unlink(missing_ok=True)
            print(f"removed: {path.relative_to(ROOT)}")

    print("RESET PASS — submission runtime state cleared (sources retained).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
