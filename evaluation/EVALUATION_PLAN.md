# Evaluation and TEVV Plan Requirements

## Required test families

1. Temporal policy and endorsement applicability.
2. Coverage-evidence fidelity, authority and citation correctness.
3. Party, role, identity, location, event and treaty reconciliation.
4. Conflict preservation, abstention and escalation quality.
5. Fraud-link precision and legitimate-relationship preservation.
6. Underwriting and pricing fairness by relevant subgroup.
7. Multilingual extraction, evidence and citation parity.
8. Privacy leakage, purpose limitation and minimum-necessary enforcement.
9. Prompt injection, tool poisoning, privilege, tenant-isolation and denial-of-wallet attacks.
10. Agent path, step, cost, timeout, checkpoint, idempotency and recovery behaviour.
11. Reinsurance wording, event, hours-clause, currency and notice completeness.
12. Latency, throughput, token use, human-review time and cost per successful outcome.

## Supplied executable assets

- `evaluation/fixtures/`: 18 public evidence bundles.
- `evaluation/contracts/`: three workflow schemas plus shared evidence-item schema.
- `evaluation/contract_tests/`: positive and prohibited-output examples.
- `evaluation/INJECT_TEST_OBLIGATIONS.csv`: one mandatory test obligation for each inject.
- `evaluation/FIXTURE_INDEX.csv`: fixture-to-workflow and inject traceability.
- `evaluation/validate_fixtures.py` and `evaluation/validate_contracts.py`: dependency-free validators.

## Participant obligations

- Add golden, edge, adversarial, metamorphic, fairness, performance and recovery tests.
- Define transparent rule-based graders wherever possible.
- Calibrate human review and justify any model-as-judge use.
- Publish release gates, confidence intervals or sample limitations, subgroup results and known blind spots.
- Retain failed cases and overrides; do not report only aggregate success.
- Demonstrate that prohibited regulated fields and side effects are rejected, not merely hidden in the interface.
