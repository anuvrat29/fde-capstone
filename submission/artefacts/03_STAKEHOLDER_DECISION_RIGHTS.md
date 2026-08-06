# 03 Stakeholder Decision Rights

## Purpose

Stakeholders, incentives, objections, RACI, delegated authorities and escalation paths for the three mandatory AEGIS-INSURE workflows, grounded in case/STAKEHOLDER_PACK.md and the D01/D02 injects.

## Acceptance criteria

- The artefact is evidence-led and references supplied paths, record locators and inject IDs.
- Facts, assumptions, inference, conflict, decision and residual risk are distinguishable.
- Temporal, jurisdictional, authorization and authority boundaries are explicit where relevant.
- Owners, approvals, review triggers and measurable acceptance gates are named.
- The artefact contains no unsupported coverage, pricing, reserve, payment or treaty conclusion.

## Artefact-specific acceptance criteria

- No workflow output schema or code path represents a binding, pricing, reserve, settlement, payment, cancellation or treaty decision (CTRL-SDR-01).
- Authority-exceedance patterns matching INJ-009 or INJ-020 are flagged to a named human approver, never silently resolved or auto-reversed (CTRL-SDR-02).
- The static RACI in this artefact is never treated as a runtime authority source; per-jurisdiction, per-product authority is checked at time of use (A-02).

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| EVID-046 | case/STAKEHOLDER_PACK.md | approved/case-pack | 2026-08-01 | MULTI | Twelve named stakeholders with objective, tension and decision authority; primary source for the RACI below. |
| EVID-005 | data/legal_entities.csv (record_id=INJ-003-LEGAL_ENTITIES) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Mutual-parent vs listed-subsidiary tension (INJ-003) and acquisition integration (INJ-004) evidence. |
| EVID-006 | data/strategy_conflicts.csv (record_id=INJ-003-STRATEGY_CONFLICTS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Corroborates INJ-003. |
| EVID-007 | data/system_inventory.csv (record_id=INJ-004-SYSTEM_INVENTORY) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Acquisition integration identifier/tenancy fragmentation (INJ-004). |
| EVID-008 | data/ai_use_boundaries.csv (record_id=INJ-005-AI_USE_BOUNDARIES) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Board-prohibited autonomous actions (INJ-005). |
| EVID-009 | data/decision_rights.csv (record_id=INJ-005-DECISION_RIGHTS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Decision-rights evidence corroborating INJ-005. |
| EVID-015 | data/binder_events.csv (record_id=INJ-009-BINDER_EVENTS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | MGA binding above delegated authority during portal outage (INJ-009). |
| EVID-016 | data/delegated_authorities.csv (record_id=INJ-009-DELEGATED_AUTHORITIES) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Corroborates INJ-009. |
| EVID-022 | data/underwriting_decisions.csv (record_id=INJ-020-UNDERWRITING_DECISIONS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Underwriter override opacity concentrated by office/broker (INJ-020). |
| EVID-023 | data/override_events.csv (record_id=INJ-020-OVERRIDE_EVENTS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Corroborates INJ-020. |
| EVID-025 | knowledge/UNDERWRITING_HUMAN_AUTHORITY.md | approved/trusted_with_conditions | 2026-01-01 | global | AI may prepare evidence/options only; binding/declining/pricing remains a licensed/delegated human action. |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | The twelve stakeholders in case/STAKEHOLDER_PACK.md are the current, complete set of decision-relevant roles; no supplementary org chart was supplied. | case/STAKEHOLDER_PACK.md | RACI below would be incomplete for roles not named there (e.g., specific country compliance officers). | Group CEO | Before workflow go-live |
| A-02 | Decision rights are contextual and temporal (per case/SOURCE_SYSTEM_FACT_PACK.md), so a single global RACI cannot substitute for per-jurisdiction, per-product authority checks at runtime. | case/SOURCE_SYSTEM_FACT_PACK.md "Evidence-authority rules to discover and defend" | A static RACI used as a runtime authority source would misauthorize actions in edge cases (e.g., MGA outage binding, INJ-009). | AI Product Owner | Ongoing — re-validate per workflow release |
| A-03 | Delegated authority limits (INJ-009) and underwriting override patterns (INJ-020) indicate that current authority boundaries are sometimes bypassed under operational pressure; this artefact treats those as known control gaps to escalate, not as acceptable precedent. | data/binder_events.csv, data/delegated_authorities.csv, data/underwriting_decisions.csv, data/override_events.csv | If treated as acceptable precedent, the AI workflow could be designed to silently tolerate authority breaches. | Chief Underwriter, CISO | Before Workflow B design freeze |

## Required analysis and decisions

| Decision/question | Evidence | Analysis | Decision/output | Owner | Status |
|---|---|---|---|---|---|
| Who may authorize an AI-assisted evidence-reconciliation output to move from "candidate finding" to "actioned by a human"? | knowledge/UNDERWRITING_HUMAN_AUTHORITY.md; data/decision_rights.csv (EVID-009) | Human authority is explicitly required for binding/declining/pricing/reserve/settlement/payment/cancellation/treaty actions (INJ-005); AI output must remain advisory | The workflow must present findings as structured fact/inference/conflict/recommendation, gated behind a named human approver role per workflow (Workflow A: Claims Handler/Adjuster; Workflow B: Underwriter; Workflow C: Catastrophe/Reinsurance lead), consistent with case/INTEGRATED_CASE.md Section 4 | AI Product Owner | Decided — structural constraint recorded; implementation deferred |
| How should the mutual-vs-shareholder tension (INJ-003) affect who signs off benefit and risk reporting? | data/legal_entities.csv (EVID-005), data/strategy_conflicts.csv (EVID-006) | Reporting must be entity-segmented (see 01_BUSINESS_CASE.md CTRL-BC-04) so neither the mutual parent's fairness objective nor the subsidiary's growth objective is silently prioritised | Board retains sign-off; Group CEO is accountable for presenting entity-segmented figures | Board, Group CEO | Decided — structural constraint recorded |
| What happens when an MGA or underwriter acts outside delegated authority (INJ-009, INJ-020)? | data/binder_events.csv (EVID-015), data/delegated_authorities.csv (EVID-016), data/underwriting_decisions.csv (EVID-022), data/override_events.csv (EVID-023) | These are existing control gaps, not workflow requirements to automate around; the AI workflow's role is limited to flagging authority-exceedance evidence for human/compliance review | Escalation path: flagged authority-exceedance evidence routes to the Chief Underwriter / Group Chief Claims Officer for manual review; AI takes no corrective action | Chief Underwriter, Group Chief Claims Officer | Decided — escalation path recorded; detection logic not yet implemented |

## Alternatives and trade-offs

| Option | Benefits | Risks | Cost/complexity | Reversibility | Decision and rationale |
|---|---|---|---|---|---|
| Static, single global RACI matrix | Simple to build and audit | Cannot represent contextual/temporal authority (A-02); would misauthorize edge cases like INJ-009 | Low | Fully reversible | Rejected as the sole mechanism; retained only as a human-readable summary (this table), not as a runtime authority source. |
| Per-workflow, per-jurisdiction authority check evaluated at run time against current entitlement data (e.g., users_entitlements.csv, access_policies.csv) | Matches the contextual/temporal authority principle required by the case pack | Higher build complexity; requires reliable, current entitlement data (which INJ has already shown can be stale — access cache outliving revocation, per starter/baseline_diagnostics.py) | Higher | Reversible; can fall back to manual authority check in degraded mode | Preferred direction for implementation; recorded here as the design decision, execution deferred to submission/src. |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-SDR-01 | No workflow output is treated as a binding/pricing/reserve/settlement/payment/cancellation/treaty decision | Design review of output schema against knowledge/UNDERWRITING_HUMAN_AUTHORITY.md and knowledge/POLICY_WORDING_AUTHORITY.md | Output schema has no field or code path that writes a coverage/price/reserve/payment/treaty conclusion | submission/artefacts/04_PRODUCT_SERVICE_BLUEPRINT.md | AI Product Owner |
| CTRL-SDR-02 | Authority-exceedance evidence (INJ-009, INJ-020 patterns) is flagged, not silently resolved | Test case using EVID-015/EVID-016/EVID-022/EVID-023 patterns | Flag is raised and routed to named human approver; no automatic override reversal | submission/tests (to be implemented in a later pass) | Chief Underwriter |
| CTRL-SDR-03 | Benefit/risk reporting is entity-segmented per INJ-003 | Report template review | Every published report shows figures by legal entity before any blended total | submission/artefacts/01_BUSINESS_CASE.md | Group CEO |

## Traceability

| Inject/requirement | Architecture/ADR | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| INJ-003 (mutual vs shareholder) | Deferred | Reporting segmentation control (CTRL-SDR-03) | Manual review | Governance tension itself remains unresolved; only reporting transparency is controlled here. |
| INJ-004 (acquisition integration) | Deferred to submission/artefacts/06_DATA_GOVERNANCE_LINEAGE.md | Identifier-mapping component (not yet implemented) | Not yet defined | Cross-entity identifier collisions could cause incorrect authority lookups if not resolved before go-live. |
| INJ-005 (prohibited autonomy) | Deferred to submission/artefacts/11_ADR_REGISTER.md | Human-approval gate (not yet implemented) | To be defined in submission/artefacts/22_EVALUATION_TEVV.md | Gate must be enforced in code, not only in documentation; residual risk until implemented and tested. |
| INJ-009 (binder authority ambiguity) | Deferred | Authority-exceedance flag (not yet implemented) | CTRL-SDR-02 | Portal-outage scenarios may recur; detection logic must handle degraded-mode operation. |
| INJ-020 (underwriter override opacity) | Deferred | Override-pattern flag (not yet implemented) | CTRL-SDR-02 | Requires access to override_events.csv-equivalent production data at sufficient granularity, which the supplied evidence-envelope schema does not provide. |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| Delegated-authority breach pattern (INJ-009) has no attached remediation owner in supplied evidence | High | Escalate to Chief Underwriter; do not treat as resolved by this artefact | Chief Underwriter | Open | Before Workflow B go-live |
| Underwriter override concentration by office/broker (INJ-020) lacks full decision-log detail | Medium | Flag as a fairness/transparency risk; cross-reference to submission/artefacts/18_RESPONSIBLE_AI_FAIRNESS.md (deferred beyond this pass) | Chief Underwriter | Open | Before Workflow B go-live |
| Static RACI (this table) must not be mistaken for a runtime authority source | Medium | Documented explicitly in A-02; enforce via design review (CTRL-SDR-01) | AI Product Owner | Open — mitigated by documentation, not yet by code | Before any implementation PR is merged |
