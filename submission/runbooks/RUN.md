# Run Runbook

## Purpose

One-command procedure to run the three mandatory AEGIS-INSURE workflows (coverage/claim evidence reconciliation, underwriting/pricing decision support, catastrophe/reinsurance planning support) against the offline evaluation fixtures.

## Prerequisites

- Setup runbook (`submission/runbooks/SETUP.md`) completed successfully.

## Steps

1. Launch the offline evidence explorer (read-only case/data browser, no workflow execution):
   ```bash
   python -m http.server --directory app 8000
   ```
   then open `http://localhost:8000/index.html`, or open `app/index.html` directly in a browser.

2. Run Workflow A (coverage/claim/fraud evidence reconciliation) against any public fixture:
   ```bash
   python submission/scripts/run_workflow_a.py --fixture evaluation/fixtures/EV-01/fixture.json
   ```
   Add `--out <path>` to write the JSON response to a file instead of stdout. The script exits 0 only if the produced response also passes its own `evaluation/contracts/coverage_claim_reconciliation_response.schema.json` contract check; otherwise it fails closed (exit 1) and prints the validation errors.

   Run Workflow B (underwriting and pricing decision support) the same way:
   ```bash
   python submission/scripts/run_workflow_b.py --fixture evaluation/fixtures/EV-06/fixture.json
   ```
   It validates against `evaluation/contracts/underwriting_pricing_support_response.schema.json` and fails closed the same way.

   Run Workflow C (catastrophe and reinsurance planning support) the same way:
   ```bash
   python submission/scripts/run_workflow_c.py --fixture evaluation/fixtures/EV-10/fixture.json
   ```
   It validates against `evaluation/contracts/catastrophe_reinsurance_planning_response.schema.json` and fails closed the same way.

3. Every workflow run must emit a structured output separating fact, inference, conflict, missing evidence, recommendation and prohibited action (never a bound/priced/reserved/settled/paid/cancelled/repudiated/treaty conclusion — see `submission/evidence/01_project_charter.md` and `submission/evidence/02_STAKEHOLDER_AND_DECISION_RIGHTS.md`). Workflow A's engine (`submission/src/workflow_a/engine.py`), Workflow B's engine (`submission/src/workflow_b/engine.py`) and Workflow C's engine (`submission/src/workflow_c/engine.py`) enforce this by construction: none has a code path that can populate any field in its contract's `x-prohibited-fields` list.

## Current submission state

All three mandatory workflows are implemented end-to-end: Workflow A (`submission/src/workflow_a/`, launcher `submission/scripts/run_workflow_a.py`, validated against all 9 public `coverage_claim_reconciliation` fixtures), Workflow B (`submission/src/workflow_b/`, launcher `submission/scripts/run_workflow_b.py`, validated against all 4 public `underwriting_pricing_support` fixtures), and Workflow C (`submission/src/workflow_c/`, launcher `submission/scripts/run_workflow_c.py`, validated against all 5 public `catastrophe_reinsurance_planning` fixtures).

## Verification

A run is successful when the command exits 0 and produces a structured output file under `submission/evidence/` or `submission/evaluation/` that a reviewer can inspect without oral explanation.
