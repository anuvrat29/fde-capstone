# Evidence and Submission Standard

Every material claim in the final submission must be reproducible from a source path, record locator, immutable hash and execution step.

## Minimum evidence fields

- evidence ID;
- source path and record locator;
- SHA-256 hash;
- authority and trust status;
- effective timestamp and jurisdiction where relevant;
- collection or generation method;
- requirement, inject, control and test references;
- reviewer and review date;
- limitation or residual uncertainty.

## Required final manifests

- `submission/evidence/evidence_manifest.csv`
- `submission/evidence/inject_traceability.csv` containing all `INJ-001` through `INJ-096`
- `submission/evaluation/public_fixture_results.csv` containing all `EV-01` through `EV-18`
- `submission/evaluation/release_gates.md`
- `submission/runbooks/SETUP.md`, `submission/runbooks/RUN.md`, `submission/runbooks/TEST.md`, `submission/runbooks/EVALUATE.md`, `submission/runbooks/RESET.md`, `submission/runbooks/INCIDENT_AND_FALLBACK.md`

Do not place secrets, real personal data, model-provider credentials or external proprietary documents in the submission.
