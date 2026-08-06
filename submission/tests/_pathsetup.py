"""Shared sys.path setup so tests can import submission/src modules and reach
the repository root for fixtures/data, regardless of the current working
directory used to invoke unittest."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "submission" / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
