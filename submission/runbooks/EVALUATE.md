# Evaluate Runbook

## Purpose

One-command procedure to execute the 18 public evaluation fixtures and contract tests, and to produce the release-gate report required before final submission.

## Prerequisites

- Setup and Test runbooks completed successfully.

## Steps

1. Validate the supplied public fixtures and response contracts (dependency-free, read-only):
   ```bash
   python evaluation/validate_fixtures.py
   python evaluation/validate_contracts.py
   ```

2. Run each of the 18 fixtures (`evaluation/fixtures/EV-01.json` through `EV-18.json`) against the implemented workflows and record pass/fail plus evidence-fidelity, citation quality, abstention and security results in `submission/evaluation/public_fixture_results.csv` with columns at minimum `scenario_id,status` for all `EV-01` through `EV-18` (see `runbooks/EVIDENCE_AND_SUBMISSION_STANDARD.md`).

3. Score against the required test families in `evaluation/EVALUATION_PLAN.md`: temporal applicability, coverage-evidence fidelity, party/role/identity/event/treaty reconciliation, conflict preservation and abstention, fraud-link precision, fairness by subgroup, multilingual parity, privacy leakage, security/injection/tenant-isolation/denial-of-wallet, agent recovery behaviour, reinsurance completeness, and latency/cost per successful outcome.

4. Publish `submission/evaluation/release_gates.md` stating go/conditional-go/pivot/pause/stop against the eight non-compensable gates in `requirements/SCORING_MODEL.md`, with subgroup results, known blind spots and retained failed cases (not aggregate-only success).

## Current submission state

`submission/evaluation/` contains no `public_fixture_results.csv` or `release_gates.md` yet, and no workflow implementation exists to execute fixtures against. This is tracked as an open item; the supplied dependency-free validators (`evaluation/validate_fixtures.py`, `evaluation/validate_contracts.py`) can be run today and will pass against the unmodified challenge package.

## Verification

Evaluation is complete when `public_fixture_results.csv` contains all 18 scenario IDs with a recorded status, and `release_gates.md` states a reviewed go/pivot/pause/stop recommendation with no unresolved Critical/High finding against the non-compensable gates.
