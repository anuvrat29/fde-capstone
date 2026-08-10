# Setup Runbook

## Purpose

One-command environment setup for the AEGIS-INSURE participant submission. The
stack is **Python-only**: rule engines under `submission/src/`, CLI launchers
under `submission/scripts/`, and an optional **Taipy** UI under
`submission/app_taipy/`. Node.js, npm, Vite and React are not part of this
submission and must not be introduced.

## Prerequisites

- Python 3.10 or later.
- Repository cloned or extracted with `FILE_HASHES.csv` intact and unmodified outside `submission/`.
- Optional UI: `taipy` installed in the local environment (`pip install taipy` or equivalent).
- Optional LLM paraphrase in the UI: `anthropic` plus `CLAUDE_KEY` in the repo-root `.env` (never commit secrets).

## Steps

1. From the repository root, run the one-command setup launcher:
   ```bash
   python submission/scripts/run_setup.py
   ```
   This runs `python run_capstone.py` (rebuilds `app/data.js`, verifies package
   hashes, validates inject mappings) and `python tools/check_submission.py --mode scaffold`.
   Do not proceed if this fails — restore the original archive rather than repairing
   challenge evidence manually.

2. (Optional) Install the Taipy UI dependency offline/local:
   ```bash
   pip install taipy
   ```
   If you want GEN-SUM-3 paraphrasing in the UI, also install `anthropic` and set
   `CLAUDE_KEY` in `.env`. Without a key the UI uses deterministic template summaries.

3. Confirm no Node/npm toolchain is required. If leftover `submission/web` or
   `submission/api` directories appear from a prior experiment, remove them with:
   ```bash
   python submission/scripts/reset_submission.py
   ```

## Current submission state

- Workflows A/B/C are implemented under `submission/src/workflow_{a,b,c}/`.
- Interactive UI is Taipy (`submission/app_taipy/`), launched via
  `submission/scripts/run_taipy.py`.
- One-command scripts: `run_setup.py`, `run_tests.py`, `run_evaluate.py`,
  `reset_submission.py`, `run_taipy.py`, plus `run_workflow_{a,b,c}.py`.

## Verification

Setup is complete when `run_setup.py` prints `SETUP PASS` with no errors.
