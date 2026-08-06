# Reset Runbook

## Purpose

One-command procedure to remove participant-generated state (caches, checkpoints, logs, outputs) without changing any supplied challenge evidence, per `runbooks/RESET_AND_REPRODUCE.md`.

## Prerequisites

- None. Reset must be safe to run at any time.

## Steps

1. Remove generated runtime artefacts (adjust paths as implementation adds them; never delete supplied challenge evidence outside `submission/`):
   ```bash
   python submission/scripts/reset_submission.py
   ```
   Until that script exists, reset manually with:
   ```bash
   Remove-Item -Recurse -Force submission/evidence/submission_hashes.csv -ErrorAction SilentlyContinue
   Get-ChildItem -Recurse submission -Include *.cache,*.log,__pycache__ | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
   ```

2. Re-verify package integrity after reset:
   ```bash
   python run_capstone.py
   python tools/check_submission.py --mode scaffold
   ```

3. Confirm no file outside `submission/` was modified by comparing against `FILE_HASHES.csv`:
   ```bash
   python tools/verify_package.py
   ```

## Current submission state

No caches, checkpoints or runtime logs exist yet because no implementation has been built. `submission/scripts/reset_submission.py` does not exist yet; this is tracked as an open item and the manual PowerShell fallback above is the current procedure.

## Verification

Reset is complete when `tools/verify_package.py` reports `PASS` for all checks, confirming no challenge evidence was altered, and `submission/` contains no generated artefacts other than the participant's committed source, tests, artefacts and evidence files.
