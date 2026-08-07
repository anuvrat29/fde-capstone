#!/usr/bin/env python3
"""One-command launcher for Workflow C (catastrophe and reinsurance planning
support), per submission/runbooks/RUN.md.

Usage:
    python submission/scripts/run_workflow_c.py --fixture evaluation/fixtures/EV-10/fixture.json
    python submission/scripts/run_workflow_c.py --fixture evaluation/fixtures/EV-10/fixture.json --out out.json

Exits 0 and writes a schema-conformant JSON response to stdout (or --out) on
success. Exits 1 if the fixture cannot be read or does not target this
workflow.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "submission" / "src"))

from common.contract_validation import load_schema, validate  # noqa: E402
from workflow_c.engine import build_response  # noqa: E402

EXPECTED_WORKFLOW = "catastrophe_reinsurance_planning"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Workflow C against one fixture.")
    parser.add_argument("--fixture", required=True, help="Path to a fixture.json (relative to repo root or absolute).")
    parser.add_argument("--out", help="Optional path to write the JSON response to. Defaults to stdout.")
    args = parser.parse_args()

    fixture_path = Path(args.fixture)
    if not fixture_path.is_absolute():
        fixture_path = ROOT / fixture_path
    if not fixture_path.exists():
        print(f"error: fixture not found: {fixture_path}", file=sys.stderr)
        return 1

    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    if fixture.get("workflow") != EXPECTED_WORKFLOW:
        print(
            f"error: fixture workflow '{fixture.get('workflow')}' is not '{EXPECTED_WORKFLOW}'",
            file=sys.stderr,
        )
        return 1

    response = build_response(
        case_id=fixture.get("scenario_id", "UNKNOWN-CASE"),
        workflow=EXPECTED_WORKFLOW,
        authorization_context=fixture.get("authorization_context", {}),
        evidence_refs=fixture.get("evidence", []),
    )

    schema_path = ROOT / fixture["response_contract"]
    schema = load_schema(schema_path)
    errors = validate(response, schema)
    if errors:
        print("error: response failed its own contract validation:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    text = json.dumps(response, indent=2, sort_keys=False)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
