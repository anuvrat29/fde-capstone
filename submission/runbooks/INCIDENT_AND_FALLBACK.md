# Incident and Fallback Runbook

## Purpose

Defines manual fallback, kill switch, degraded mode and AI-disabled continuity procedures for the three mandatory workflows, satisfying the required operating properties in `case/INTEGRATED_CASE.md` §5 and DEFINITION_OF_DONE.md "Safety, governance and assurance".

## Trigger conditions

| Trigger | Example inject | Response |
|---|---|---|
| Regional AI endpoint outage | INJ-093 | Fail closed to manual evidence-gathering procedure below; do not fail open to an unreviewed default answer. |
| Ransomware containment / read-only core systems | INJ-080 | Operate in degraded mode: workflows may read cached/last-verified evidence only, must label all outputs as degraded-mode, and must not present any option requiring live system write access. |
| Model artefact hash mismatch against registry | INJ-081 | Kill switch: refuse to serve the mismatched model version; escalate to CISO before any resumption. |
| Revoked-user cache lag | INJ-079 | Treat any cached authorization older than the configured freshness window as invalid; require re-check against the source entitlement system before granting access. |
| Checkpoint replay producing duplicate drafts | INJ-094 | Idempotency key required on every agent step; duplicate keys are rejected, not re-executed. |
| Vendor exit / catastrophe vendor outage | INJ-035, INJ-096 | Fall back to last-verified snapshot with an explicit staleness label; escalate to the CISO/operations lead for a degraded-mode decision. |

## Manual fallback procedure (AI-disabled continuity)

1. Disable the AI workflow entry point (kill switch). No workflow output may be produced while disabled.
2. Claims handlers, underwriters and catastrophe/reinsurance leads revert to the pre-existing manual evidence-gathering procedure described in `case/SOURCE_SYSTEM_FACT_PACK.md` (system-of-record lookups performed directly by the qualified human, without AI assistance).
3. AMR must be able to operate for at least 21 days without model inference per INJ-096 (`data/continuity_requirements.csv`). This runbook, plus the decision-rights matrix in `submission/evidence/02_STAKEHOLDER_AND_DECISION_RIGHTS.md`, is the evidence that human decision-makers retain full authority and procedure independent of any AI component.
4. Record every fallback activation (trigger, start time, end time, decisions made manually) in `submission/evidence/` for later audit.

## Escalation

- Security incidents (prompt injection success, tool poisoning, cross-tenant leakage): escalate immediately to the CISO per `submission/evidence/02_STAKEHOLDER_AND_DECISION_RIGHTS.md` Workflow-specific escalation rows.
- Reserve, settlement, payment, treaty or coverage-adjacent incidents: escalate to the Group Chief Claims Officer or Chief Actuary; never resolved by the AI Product Owner alone (INJ-088 accountability rule).
- Vendor exit (120-day notice per INJ-096): Reinsurance Director and CISO jointly own the transition plan; evidence must remain inspectable throughout per `data/vendor_exit_assets.csv`.

## Current submission state

Workflow engines under `submission/src/` are deterministic and offline; they do
not call external models. The only optional model path is the Taipy UI
summariser (`submission/app_taipy/llm_summary.py`): when `CLAUDE_KEY` is absent
or the call fails, `summarize_with_fallback()` keeps serving deterministic
template text (`AI_DISABLED_CONTINUITY`) without changing engine facts. Kill the
UI by stopping the Taipy process (`run_taipy.py`); CLI workflows remain available
independently. Dedicated degraded-mode / idempotency drills remain tracked in
`submission/evidence/ARTEFACT_STATE_LOG.md` and gate 6 of
`submission/evaluation/release_gates.md`.

## Verification

This runbook is verified when a test can simulate each trigger condition above, confirm the workflow fails closed (never produces a prohibited or unreviewed output), and confirm the manual fallback procedure is executable without the AI component.
