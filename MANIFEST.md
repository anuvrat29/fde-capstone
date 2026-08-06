# Repository Manifest — Workshop-Ready v2

## Package summary

- Injects: 96
- Original operational CSV datasets: 202
- Canonical inject-evidence CSV: 1
- Total CSV files under `data/`: 203
- Canonical inject-evidence records: 191
- Knowledge documents: 37
- Public evaluation fixtures: 18
- Workflow response schemas: 4
- Official research anchors: 9
- Participant templates: 32
- Assessment total: 200 points
- Total files at release build: 392

## Integrity boundary

`FILE_HASHES.csv` covers all immutable challenge and workshop files except itself and `VALIDATION_REPORT.json`. The participant-writable `submission/` directory is excluded.

## Primary entry points

- `START_HERE.md`
- `run_capstone.py`
- `tools/verify_package.py`
- `tools/check_submission.py`
- `app/index.html`
- `WORKSHOP_DEPLOYMENT_PLAN.md`
- `AUDIT_AND_SANITY_CHECK.md`
