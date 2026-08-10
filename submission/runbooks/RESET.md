# Reset Runbook

## Purpose

One-command procedure to remove participant-generated runtime state (caches,
checkpoints, logs, orphan experiment folders) without changing any supplied
challenge evidence, per `runbooks/RESET_AND_REPRODUCE.md`.

## Prerequisites

- None. Reset must be safe to run at any time.

## Steps

1. Clear submission runtime artefacts:
   ```bash
   python submission/scripts/reset_submission.py
   ```
   This removes `__pycache__`, `*.cache` / `*.log` / `*.pyc` under `submission/`,
   generated `submission/evidence/submission_hashes.csv` if present, and any
   leftover `submission/web` (Node/npm) or `submission/api` experiment trees.
   Source, artefacts, evidence markdown, tests and evaluation results are kept.

2. Re-verify package integrity after reset:
   ```bash
   python submission/scripts/run_setup.py
   ```

3. Confirm no file outside `submission/` was modified:
   ```bash
   python tools/verify_package.py
   ```

## Current submission state

`submission/scripts/reset_submission.py` is the supported reset path. The live
stack is Python engines + Taipy; Node leftovers are treated as disposable
runtime orphans if they reappear.

## Verification

Reset is complete when `tools/verify_package.py` reports `PASS` and
`submission/` contains no `__pycache__`, `node_modules`, or orphan `web`/`api`
trees.
