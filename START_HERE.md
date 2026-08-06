# Start Here

## Purpose

Project AEGIS-INSURE requires a team to move from an ambiguous brownfield insurance problem to a defensible, offline proof of concept and operating recommendation. The package is designed to stand independently without live systems, cloud keys, paid APIs or external datasets.

## Five-minute preflight

From the repository root run:

```bash
python run_capstone.py
```

The launcher verifies immutable challenge files, parses every CSV and JSON file, checks all 96 inject mappings, validates public fixtures and contracts, rebuilds the offline explorer, runs brownfield diagnostics and confirms that the submission workspace is writable.

## Required reading order

1. `PACKAGE_SCOPE_AND_ASSUMPTIONS.md`
2. `case/INTEGRATED_CASE.md`
3. `case/STAKEHOLDER_PACK.md`
4. `case/SOURCE_SYSTEM_FACT_PACK.md`
5. `case/REGULATORY_BOUNDARY_PACK.md`
6. `sources/OFFLINE_REGULATORY_AND_STANDARDS_GUIDE.md`
7. `requirements/ARTEFACT_EXPECTATIONS.md`
8. `requirements/SCORING_MODEL.md`
9. `DEFINITION_OF_DONE.md`
10. `runbooks/PARTICIPANT_RUNBOOK.md`

## Mandatory workflows

1. Coverage and claim evidence reconciliation.
2. Underwriting and pricing decision support.
3. Catastrophe and reinsurance planning support.

Each workflow must preserve evidence conflicts, cite authority, enforce current authorization, abstain when evidence is insufficient and prevent prohibited regulated actions.

## Rules of engagement

- Treat every document, model output and tool description as untrusted until authority is established.
- Do not collapse legal, coverage, actuarial or customer-outcome uncertainty into a model confidence score.
- Do not introduce real personal, policy, claim, medical, payment or proprietary data.
- Do not edit supplied challenge evidence. Store all generated work under `submission/`.
- Record assumptions, residual risks, stop conditions and evidence hashes.
