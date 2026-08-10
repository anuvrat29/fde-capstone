# Evaluate Runbook

## Purpose

One-command procedure to validate the 18 public evaluation fixtures and response
contracts, and to confirm the release-gate report required before final
submission.

## Prerequisites

- Setup and Test runbooks completed successfully.

## Steps

1. Run the one-command evaluate launcher (offline validators + presence checks):
   ```bash
   python submission/scripts/run_evaluate.py
   ```
   This executes:
   ```bash
   python evaluation/validate_fixtures.py
   python evaluation/validate_contracts.py
   ```
   and confirms `submission/evaluation/public_fixture_results.csv` and
   `submission/evaluation/release_gates.md` exist.

2. Re-execute any fixture via CLI or Taipy if results need refreshing:
   ```bash
   python submission/scripts/run_workflow_a.py --fixture evaluation/fixtures/EV-01/fixture.json --out /tmp/ev01.json
   python submission/scripts/run_taipy.py
   ```

3. Review `submission/evaluation/release_gates.md` against the eight
   non-compensable gates in `requirements/SCORING_MODEL.md`, including subgroup
   results, known blind spots and retained escalated/conflict cases.

## Current submission state

- All 18 public fixtures are recorded in `public_fixture_results.csv`.
- Release gates are stated in `release_gates.md` (CONDITIONAL-GO).
- Engines under `submission/src/` and the Taipy presentation layer under
  `submission/app_taipy/` are the only runtime surfaces evaluated; no Node SPA.

## Verification

Evaluation is complete when `run_evaluate.py` prints `EVALUATE PASS`, the CSV
contains all 18 scenario IDs, and `release_gates.md` states a reviewed
go/conditional-go/pivot/pause/stop recommendation.
