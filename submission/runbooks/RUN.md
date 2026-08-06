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

2. Run each workflow's entry point (to be implemented under `submission/src/` and invoked via `submission/scripts/run_workflow_a.py`, `run_workflow_b.py`, `run_workflow_c.py` or an equivalent single launcher):
   ```bash
   python submission/scripts/run_all_workflows.py --fixture evaluation/fixtures/<fixture_id>.json
   ```

3. Every workflow run must emit a structured output separating fact, inference, conflict, missing evidence, recommendation and prohibited action (never a bound/priced/reserved/settled/paid/cancelled/repudiated/treaty conclusion — see `submission/evidence/01_project_charter.md` and `submission/evidence/02_STAKEHOLDER_AND_DECISION_RIGHTS.md`).

## Current submission state

No workflow implementation exists yet under `submission/src/` or launcher scripts under `submission/scripts/`. This runbook records the required one-command run contract; it will be updated with the exact command line once the workflows are implemented. Until then, running a workflow is not possible and this gap is tracked as an open item in `submission/evidence/ARTEFACT_STATE_LOG.md`.

## Verification

A run is successful when the command exits 0 and produces a structured output file under `submission/evidence/` or `submission/evaluation/` that a reviewer can inspect without oral explanation.
