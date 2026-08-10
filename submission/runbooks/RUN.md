# Run Runbook

## Purpose

One-command procedures to run the three mandatory AEGIS-INSURE workflows
(coverage/claim evidence reconciliation, underwriting/pricing decision support,
catastrophe/reinsurance planning support) against the offline evaluation
fixtures — via CLI or the Taipy UI. No Node.js frontend is used.

## Prerequisites

- Setup runbook (`submission/runbooks/SETUP.md`) completed successfully.
- For the interactive UI: `taipy` installed (see SETUP).

## Steps

1. (Optional) Launch the supplied offline evidence explorer (read-only case/data
   browser under package-root `app/`, not the workflow runner):
   ```bash
   python -m http.server --directory app 8000
   ```
   then open `http://localhost:8000/index.html`, or open `app/index.html` directly.

2. **Interactive UI (Taipy — preferred demo path)**  
   ```bash
   python submission/scripts/run_taipy.py
   ```
   Open `http://127.0.0.1:5000`, choose a workflow and public fixture, then Run.
   The UI calls `submission/src/workflow_{a,b,c}/engine.py` in-process, validates
   the response against the fixture's JSON Schema contract, and optionally
   paraphrases the summary via GEN-SUM-3 when `CLAUDE_KEY` is configured.

3. **CLI (headless / CI)** — Workflow A:
   ```bash
   python submission/scripts/run_workflow_a.py --fixture evaluation/fixtures/EV-01/fixture.json
   ```
   Add `--out <path>` to write JSON to a file. Exit 0 only if the response passes
   `evaluation/contracts/coverage_claim_reconciliation_response.schema.json`.

   Workflow B:
   ```bash
   python submission/scripts/run_workflow_b.py --fixture evaluation/fixtures/EV-06/fixture.json
   ```
   Contract: `evaluation/contracts/underwriting_pricing_support_response.schema.json`.

   Workflow C:
   ```bash
   python submission/scripts/run_workflow_c.py --fixture evaluation/fixtures/EV-10/fixture.json
   ```
   Contract: `evaluation/contracts/catastrophe_reinsurance_planning_response.schema.json`.

4. Every workflow run must emit structured output separating fact, inference,
   conflict, missing evidence, recommendation and prohibited action. Engines
   enforce this by construction and never populate `x-prohibited-fields`.

## Current submission state

All three mandatory workflows are implemented end-to-end. Presentation is
Taipy-only (`submission/app_taipy/`). There is no React/Vite/Node SPA and no
FastAPI companion service in this submission.

## Verification

A run is successful when the CLI exits 0 with a contract-valid JSON response, or
the Taipy UI shows status + contract PASS for the selected fixture.
