# Participant Runbook

## 1. Preflight

```bash
python run_capstone.py
python tools/check_submission.py --mode scaffold
```

Do not proceed if package verification fails. Restore the original archive rather than repairing challenge evidence manually.

## 2. Qualify the problem

- Read the integrated case and all disclosed injects.
- Establish intended purpose, no-AI alternative, decision rights and prohibited actions.
- Build a source-authority and temporal-applicability hypothesis before coding.
- Record assumptions and open evidence gaps.

## 3. Baseline the brownfield state

- Run `python starter/baseline_diagnostics.py`.
- Inspect `starter/legacy_insurance.py`, `starter/legacy_portal.js` and incompatible API samples.
- Preserve discovered defects as evidence.
- Decide whether each component is replaced, isolated, wrapped or retired.

## 4. Design and specify

- Complete DDD, ontology, semantic, graph, requirements, C4 and ADR artefacts.
- Map every inject to a requirement, control and test.
- Use the supplied response contracts as minimum fail-closed boundaries.

## 5. Build only under submission

Recommended structure:

- `submission/src/` — implementation.
- `submission/app/` — offline UI or CLI.
- `submission/tests/` — unit, integration, security and recovery tests.
- `submission/evaluation/` — fixture results, graders and scorecards.
- `submission/evidence/` — provenance, logs, hashes and demonstrations.
- `submission/artefacts/` — completed templates.
- `submission/runbooks/` — setup, run, test, evaluation, reset, incident and fallback procedures.
- `submission/scripts/` — one-command launchers.

## 6. Evaluate and attack

```bash
python evaluation/validate_fixtures.py
python evaluation/validate_contracts.py
```

Execute all 18 fixtures and add participant-authored tests. Demonstrate prompt injection, poisoned tool manifest, stale authorization, cross-tenant request, replay, regional outage, fallback regression and cost shock.

## 7. Validate final submission

```bash
python tools/check_submission.py --mode final
python tools/hash_submission.py
```

The final validator is intentionally strict. It rejects placeholders, missing inject traceability, absent fixtures, incomplete runbooks and insufficient implementation/test evidence.

## 8. Defend

Use `requirements/FINAL_DEFENCE.md`. The panel may select any inject, evidence file, user role, policy version, model endpoint or failure mode. Trace the response to evidence and state what the system cannot decide.
