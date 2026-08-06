# Test Runbook

## Purpose

One-command procedure to execute unit, integration, security and recovery tests for the three mandatory workflows.

## Prerequisites

- Setup runbook completed successfully.

## Steps

1. Run the full participant-authored test suite (standard library `unittest`, no external test framework required):
   ```bash
   python -m unittest discover -s submission/tests -p "test_*.py" -v
   ```

2. Required test categories, per `runbooks/EVIDENCE_AND_SUBMISSION_STANDARD.md` and `requirements/ARTEFACT_EXPECTATIONS.md`:
   - Unit tests for evidence-reconciliation logic (Workflow A), underwriting/pricing evidence assembly (Workflow B) and catastrophe/reinsurance option generation (Workflow C).
   - Security tests: prompt injection resistance (using `knowledge/MALICIOUS_ADJUSTER_REPORT.md`), tool-manifest poisoning (using `tool_manifest_poisoned.json`), stale authorization (INJ-079 pattern), cross-tenant leakage (INJ-082 pattern), replay/idempotency (INJ-094 pattern) and denial-of-wallet (INJ-090 pattern).
   - Human-approval gate tests: confirm no prohibited action (binding, pricing, reserve change, settlement, payment, cancellation, repudiation, treaty placement) can be produced without an authorized human approval step, per `submission/evidence/02_STAKEHOLDER_AND_DECISION_RIGHTS.md` CTRL-DR-01 through CTRL-DR-04.
   - Recovery tests: regional outage, fallback regression, AI-disabled continuity.

3. Fail closed: any test that cannot execute offline (requires network, paid API or real customer data) is a defect, not an accepted limitation.

## Current submission state

`submission/tests/` currently contains no substantive test files beyond a `.gitkeep` placeholder. `tools/check_submission.py --mode final` requires at least five substantive test files before final validation passes. This is tracked as an open item.

## Verification

Testing is complete when `python -m unittest discover -s submission/tests` exits 0 and the security/human-approval-gate test categories above are each represented by at least one passing test plus one deliberately-failing (attack) case that is correctly rejected.
