# 01 Business Case

## Purpose

Business case, measurable baseline, KPI tree, no-AI alternative, value leakage and benefits-realisation plan for the AEGIS-INSURE evidence-reconciliation and decision-support intervention at Aurelia Mutual & Re Group (AMR).

## Acceptance criteria

- The artefact is evidence-led and references supplied paths, record locators and inject IDs.
- Facts, assumptions, inference, conflict, decision and residual risk are distinguishable.
- Temporal, jurisdictional, authorization and authority boundaries are explicit where relevant.
- Owners, approvals, review triggers and measurable acceptance gates are named.
- The artefact contains no unsupported coverage, pricing, reserve, payment or treaty conclusion.

## Artefact-specific acceptance criteria

- No cycle-time or expense-ratio figure is reported as achieved without a linked, dated baseline measurement (CTRL-BC-01).
- The no-AI alternative (INJ-002) is quantified and compared line-by-line before any AI-assisted option is recommended (CTRL-BC-02).
- Every published benefit or cost figure includes complaints, appeals, human-review, litigation, regulatory-remediation and model-change cost lines (CTRL-BC-03).
- Benefit and risk figures are broken out by legal entity before any blended total is presented (CTRL-BC-04).

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| EVID-001 | data/board_requests.csv (record_id=INJ-001-BOARD_REQUESTS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Board demand for 20% cat cycle-time and 12% expense-ratio improvement; not an approved, funded programme — treated as a target hypothesis, not a fact. |
| EVID-002 | data/kpi_conflicts.csv (record_id=INJ-001-KPI_CONFLICTS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Duplicate corroboration of the same board target; does not add independent confirmation. |
| EVID-003 | data/no_ai_baselines.csv (record_id=INJ-002-NO_AI_BASELINES) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Process Excellence claim that wording rationalisation/identity repair/workflow redesign can deliver most benefit without generative AI; no quantified baseline attached. |
| EVID-004 | data/process_bottlenecks.csv (record_id=INJ-002-PROCESS_BOTTLENECKS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Bottleneck evidence supporting the no-AI counter-argument; evidence-envelope granularity only. |
| EVID-010 | data/cost_model.csv (record_id=INJ-006-COST_MODEL) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Cost model that excludes complaints, appeals, human review, litigation, regulatory remediation and model-change cost lines. |
| EVID-011 | data/staff_rates.csv (record_id=INJ-006-STAFF_RATES) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Supporting staff-cost evidence at evidence-envelope granularity; no fully-loaded rate card supplied. |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | The board's 20% cycle-time / 12% expense-ratio target (INJ-001) is a demand, not an approved, funded, resourced programme commitment. | data/board_requests.csv shows status `unverified`/`challenge_fact`, no linked funding approval record. | If the target is treated as committed, the benefits case will overstate realised value and expose the programme to non-delivery risk. | Group CEO sponsor | Prior to programme kickoff |
| A-02 | Cycle-time and expense-ratio gains must not be achieved by weakening claims independence, reserving governance or consumer protection controls. | Explicit board condition in INJ-001; corroborated by requirements/SCORING_MODEL.md non-compensable gate 1 (no autonomous binding/pricing/reserve/settlement actions). | Any design that trades control strength for speed fails a non-compensable gate and cannot receive an unconditional "go". | Chief Claims Officer, Chief Actuary | Ongoing design review |
| A-03 | A credible no-AI alternative (policy-wording rationalisation, identity repair, workflow redesign) must be quantified and compared before any AI investment is approved (INJ-002). | data/no_ai_baselines.csv, data/process_bottlenecks.csv. | Skipping this comparison risks funding AI to solve a problem better solved by data-quality remediation, contradicting the case for intervention. | AI Product Owner, Process Excellence | Before business case sign-off |
| A-04 | The benefits case must include complaints, appeals, human-review, litigation, regulatory-remediation and model-change costs, not only build/run cost (INJ-006). | data/cost_model.csv, data/staff_rates.csv. | Excluding these costs produces an artificially favourable ROI and violates the Customer Advocate and Chief Actuary stated concerns (case/STAKEHOLDER_PACK.md). | Chief Actuary, Finance | Before benefits sign-off |
| A-05 | AMR's mutual-parent fairness objective and listed-subsidiary growth objective (INJ-003) may conflict on how benefits are allocated or reported; the business case must not silently favour one. | data/legal_entities.csv, data/strategy_conflicts.csv. | Silent resolution in favour of either party risks governance and conduct exposure. | Group CEO, Board | Ongoing |

## Required analysis and decisions

| Baseline metric and period | No-AI alternative | Value hypothesis | Cost and value leakage | Benefit owner | Stop condition |
|---|---|---|---|---|---|
| Catastrophe claim cycle time, current period (baseline to be measured against ClaimSphere claim-open-to-first-decision timestamps; not yet quantified in supplied evidence) | Policy-wording rationalisation, identity/party-record repair and workflow redesign per INJ-002 (data/no_ai_baselines.csv; data/process_bottlenecks.csv) | Evidence-reconciliation support (Workflow A) reduces manual evidence-gathering time by surfacing conflicts, missing evidence and candidate next actions — without automating coverage decisions | Build/run cost (submission/scripts, submission/src) plus complaints, appeals, human-review, litigation and regulatory-remediation cost per INJ-006 (data/cost_model.csv; data/staff_rates.csv) | Group Chief Claims Officer | If cycle-time gains are only achievable by bypassing human review or evidence preservation, stop and revert to manual process. |
| Expense ratio, current period (not independently quantified in supplied evidence; board target is a demand, not a baseline) | Same as above; process redesign may deliver expense reduction without any AI component (INJ-002) | Underwriting/pricing decision support (Workflow B) reduces evidence-preparation effort for underwriters without changing pricing or binding authority | Same as above | Chief Actuary / US Chief Underwriter | If expense reduction requires removing underwriter override visibility or delegated-authority checks, stop. |
| Mutual member-fairness and shareholder growth balance (INJ-003; data/legal_entities.csv, data/strategy_conflicts.csv) | N/A — this is a governance tension, not a process gap | The business case must report benefits separately by legal entity/channel so neither constituency's outcome is obscured | Governance/reporting overhead is itself a value-leakage line, not a sunk cost | Group CEO, Board | If a single blended benefit number is required by any stakeholder without entity-level breakdown, escalate rather than comply. |

## Alternatives and trade-offs

| Option | Benefits | Risks | Cost/complexity | Reversibility | Decision and rationale |
|---|---|---|---|---|---|
| No-AI process/data-quality remediation only (INJ-002) | Lower security/fairness/governance risk surface; directly addresses identifier and wording fragmentation named in INJ-007/INJ-030 | May not fully address evidence-reconciliation speed under catastrophe volume; Process Excellence claim is unquantified (data/no_ai_baselines.csv) | Lower build cost; higher ongoing manual-labour cost (data/staff_rates.csv) | Fully reversible; no new model or agent surface introduced | Deferred final decision: quantified no-AI baseline (A-03) must be completed before comparing to the AI-assisted option; this artefact records the requirement, not the answer. |
| Bounded AI evidence-reconciliation decision support (Workflow A/B/C) restricted from binding actions (INJ-005) | Structured fact/inference/conflict/recommendation separation; explicit abstention; faster evidence assembly for human decision-makers | Requires security, fairness and reliability evidence (prompt injection, tool poisoning, tenant isolation per requirements/SCORING_MODEL.md gates); non-trivial governance overhead | Higher build/run and evaluation cost; must fund TEVV, security testing and human-review tooling | Reversible via AI-disabled continuity mode (a mandatory operating property); no data or decision is permanently automated | Preferred candidate pending completion of the no-AI comparison (A-03) and non-compensable gate compliance; final selection is a participant/board decision, not asserted here. |
| Full workflow automation with autonomous coverage/pricing/reserve actions | Fastest theoretical cycle-time reduction | Explicitly prohibited by the board (INJ-005; data/ai_use_boundaries.csv, data/decision_rights.csv) and by requirements/SCORING_MODEL.md non-compensable gate 1 | N/A | N/A | Rejected. Violates a non-compensable gate; not a viable option under any cost/benefit outcome. |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-BC-01 | Board target (INJ-001) must not be reported as an achieved or committed benefit | Manual review of benefits-realisation reporting language before publication | No report states cycle-time/expense-ratio figures as achieved without a linked, dated measurement source | submission/evidence/evidence_manifest.csv (EVID-001, EVID-002) | Chief Actuary |
| CTRL-BC-02 | No-AI alternative (INJ-002) must be quantified before AI investment approval | Comparative baseline exercise using data/no_ai_baselines.csv and data/process_bottlenecks.csv | A documented, dated no-AI baseline exists and is compared line-by-line against the AI-assisted option | submission/artefacts/02_DMAIC_WORKBOOK.md (Measure/Analyse sections) | AI Product Owner |
| CTRL-BC-03 | Value-leakage costs (INJ-006) must be included in every benefits calculation | Checklist review of cost model against data/cost_model.csv and data/staff_rates.csv line items | Complaints, appeals, human-review, litigation, regulatory-remediation and model-change cost lines are present in every published cost model | submission/evidence/evidence_manifest.csv (EVID-010, EVID-011) | Finance / Chief Actuary |
| CTRL-BC-04 | Mutual-versus-shareholder benefit reporting (INJ-003) must be entity-segmented | Report template review | Benefit figures are broken out by legal entity per data/legal_entities.csv before any blended total is presented | submission/artefacts/03_STAKEHOLDER_DECISION_RIGHTS.md | Group CEO |

## Traceability

| Inject/requirement | Architecture/ADR | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| INJ-001 (board catastrophe target) | To be recorded in submission/artefacts/10_C4_ARCHITECTURE.md and submission/artefacts/11_ADR_REGISTER.md (deferred beyond this pass) | Not yet implemented | To be defined in submission/artefacts/22_EVALUATION_TEVV.md | Target may remain unquantified if no baseline measurement is agreed; tracked as an open issue below. |
| INJ-002 (no-AI challenge) | N/A — governance decision, not architecture | submission/artefacts/02_DMAIC_WORKBOOK.md documents the comparison requirement | Comparative baseline exercise (not yet executed) | No-AI option may be under- or over-stated without real process data; tracked as an open issue below. |
| INJ-003 (mutual vs shareholder tension) | To be recorded in submission/artefacts/03_STAKEHOLDER_DECISION_RIGHTS.md | N/A — reporting/governance control | Manual review of benefit-reporting segmentation | Entity-level reporting may be resisted by stakeholders seeking a single headline number. |
| INJ-006 (value leakage) | N/A | Cost model line items (to be built under submission/src or submission/evaluation in a later pass) | CTRL-BC-03 checklist | Cost model completeness depends on Finance providing real complaint/appeal/litigation unit costs, which are not in the supplied synthetic data at full granularity. |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| Board target (INJ-001) has no attached measurement baseline or funding approval | High | Treat as an unverified target; require a dated, owned baseline measurement before any benefit is claimed | Group CEO | Open — pending baseline | Before programme funding decision |
| No-AI alternative (INJ-002) is asserted but not quantified | High | Require the DMAIC Measure phase (submission/artefacts/02_DMAIC_WORKBOOK.md) to produce a dated, quantified comparison before AI build proceeds | AI Product Owner, Process Excellence | Open — pending DMAIC Measure output | Before AI investment approval |
| Mutual-versus-shareholder benefit allocation (INJ-003) is unresolved | Medium | Require entity-segmented reporting as a structural control (CTRL-BC-04) rather than resolving the underlying governance tension in this artefact | Board | Open — structural mitigation only | Ongoing; review at each benefits report |
| Value-leakage costs (INJ-006) rely on synthetic evidence-envelope rows without full unit-cost detail | Medium | Flag as a data-completeness gap; do not finalise ROI until Finance supplies real unit costs for complaints/appeals/litigation/model-change | Finance, Chief Actuary | Open | Before final benefits sign-off |
| Acquisition-integration identifier fragmentation (INJ-004) may distort any cross-entity benefit measurement | Medium | Defer detailed remediation to submission/artefacts/06_DATA_GOVERNANCE_LINEAGE.md; note the risk here so it is not silently dropped | Data Governance Owner | Open | Before combined KPI reporting across legacy and acquired entities |
