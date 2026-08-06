# 32 Change And Benefits Control

## Purpose

Change impact, benefits tracking, value leakage, adoption and stop criteria, closing the loop back to 01_BUSINESS_CASE.md's original KPI tree and stop conditions now that all 31 prior artefacts have specified the design this benefits-tracking framework must monitor.

## Acceptance criteria

- The artefact is evidence-led and references supplied paths, record locators and inject IDs.
- Facts, assumptions, inference, conflict, decision and residual risk are distinguishable.
- Temporal, jurisdictional, authorization and authority boundaries are explicit where relevant.
- Owners, approvals, review triggers and measurable acceptance gates are named.
- The artefact contains no unsupported coverage, pricing, reserve, payment or treaty conclusion.

## Artefact-specific acceptance criteria

- Every benefit tracked traces back to a specific KPI or cost line already named in 01_BUSINESS_CASE.md; no new, previously-undisclosed benefit is introduced at this final stage (CTRL-CBC-01).
- Value-leakage cost lines (complaints, appeals, human review, litigation, regulatory remediation, model-change cost) from CTRL-BC-03 are tracked continuously, not only at initial business-case sign-off (CTRL-CBC-02).
- Every stop criterion from prior artefacts (01's no-AI comparator, 15/18's fairness-remediation deadline, 23's OM-Large decision, 28's non-compensable-gate go/no-go) is consolidated into one master stop-criteria register, not scattered and easily lost across 31 files (CTRL-CBC-03).
- Adoption is measured by human-approver engagement with AI-prepared recommendations (acceptance, escalation, override rates), never by AI output volume alone, consistent with the human-in-the-loop discipline established since 03/04 (CTRL-CBC-04).

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| EVID-010 | data/cost_model.csv (record_id=INJ-006-COST_MODEL) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Reused from 01/23; the value-leakage cost lines this artefact's continuous-tracking control must monitor. |
| — | submission/artefacts/01_BUSINESS_CASE.md through 31_ELEVATOR_PITCH.md | participant-authored | 2026-08-06 | — | Source of every KPI, benefit, and stop criterion consolidated below; no single file locator applies across thirty-one files, consistent with the established multi-file evidence convention. |
| EVID-121 | submission/evidence/inject_traceability.csv (section=full_file_snapshot_at_Step_28) | participant-authored | 2026-08-06 | — | Reused from 28/29/30; the inject-coverage figures this artefact's adoption/benefits-realisation tracking must eventually close toward full coverage. |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | Every benefit tracked in this artefact must trace to a KPI or cost line already named in 01_BUSINESS_CASE.md (catastrophe cycle time, expense ratio, entity-segmented reporting, value-leakage cost lines); this artefact does not introduce a new benefit metric this late in the submission, which would be indefensible given no prior artefact established it. | 01_BUSINESS_CASE.md (KPI tree, reused) | Introducing a new, previously-undisclosed benefit metric at template 32 would look like an attempt to inflate the final impression without evidentiary basis. | AI Product Owner | Ongoing |
| A-02 | Value-leakage cost lines (complaints, appeals, human review, litigation, regulatory remediation, model-change cost, per CTRL-BC-03) must be tracked continuously throughout the programme's life, not only checked once at business-case sign-off; this closes a gap where 01's control was framed as a one-time gate rather than an ongoing measurement. | 01_BUSINESS_CASE.md (CTRL-BC-03, reused) | A one-time check at sign-off would miss value leakage that emerges later, such as complaints arising only after a workflow goes live. | Chief Actuary, Finance | Ongoing once any workflow reaches a pilot |
| A-03 | The master stop-criteria register consolidates, but does not replace or supersede, the individual stop criteria already specified in their originating artefacts (01's no-AI comparator, 15/18's fairness-remediation deadline, 23's OM-Large decision, 28's per-gate go/no-go); this artefact is a single lookup point, not a new authority. | Consistent with the reuse-not-reinvent discipline established since 09/11/20 | Treating this register as a new, separate authority could create a conflicting second source of truth for the same stop criteria. | AI Product Owner | Ongoing |
| A-04 | Adoption is measured by the rate at which human approvers accept, escalate, or override an AI-prepared recommendation, never by how many recommendations the AI produces; a high output volume with a high override rate would indicate poor adoption, not success, and this artefact's metric design must reflect that distinction. | 03_STAKEHOLDER_DECISION_RIGHTS.md, 04_PRODUCT_SERVICE_BLUEPRINT.md (human-approval-gate design, reused) | Measuring output volume alone could reward a workflow that produces many low-quality recommendations humans routinely reject, masking a real adoption failure. | AI Product Owner, Group Chief Claims Officer | Before any workflow reaches a pilot |

## Required analysis and decisions

| Decision/question | Evidence | Analysis | Decision/output | Owner | Status |
|---|---|---|---|---|---|
| What benefits does this framework track, and from where do they trace? | 01_BUSINESS_CASE.md (KPI tree); 02_DMAIC_WORKBOOK.md (control metrics) | Per A-01: (1) catastrophe claim cycle time (currently unmeasured baseline, per 01/02's open issue — tracked as "baseline pending" until measured); (2) expense ratio (same status); (3) entity-segmented benefit reporting compliance (measurable now: does every published report show figures by legal entity before any blended total, per CTRL-BC-04); (4) value-leakage cost lines (measurable now via A-02's continuous tracking) | Four tracked benefits, two of which cannot yet report a number (honestly reflecting 01/02's own open baseline status), two of which are process-compliance metrics measurable immediately | Chief Actuary, Finance | Decided |
| How are value-leakage costs tracked continuously? | data/cost_model.csv (EVID-010, reused) | Per A-02, complaints/appeals/human-review/litigation/regulatory-remediation/model-change cost lines are each logged monthly against the cost_model.csv baseline categories, with a variance-from-baseline figure reported at each review | Monthly value-leakage variance report, cross-referencing back to 01's original cost-model categories | Finance | Decided |
| What is the master stop-criteria register? | 01 (no-AI comparator); 15/18 (fairness-remediation deadline); 23 (OM-Large decision); 28 (per-gate go/no-go) | Per A-03, four stop criteria consolidated: (1) if the no-AI comparator shows equivalent benefit, stop the AI-assisted option (01/02); (2) if PRC-MOTOR-9/FRD-CLAIM-6's remediation pathway is not chosen by a set deadline, escalate to Board (15/18); (3) if the OM-Large budget-response decision is not made by 2026-08-15, the default-absorb outcome itself triggers a cost-review stop-point (23); (4) if gates 1/2/3/5/6/8 are not passing, no pilot cutover proceeds regardless of schedule pressure (28) | Four-item master register, each citing its originating artefact, none newly invented here | AI Product Owner, Group CEO | Decided |
| How is adoption measured once a workflow reaches a pilot? | 03/04 (human-approval-gate design, reused) | Per A-04, adoption = (accepted recommendations + escalated-with-clear-reasoning recommendations) / total recommendations reviewed; override rate (recommendations rejected without escalation) is tracked separately as a quality signal, not folded into the adoption figure | Adoption metric defined; not yet measurable since no workflow has reached a pilot (per 28's verdict) | Group Chief Claims Officer | Decided — definition recorded, measurement pending pilot |

## Alternatives and trade-offs

| Option | Benefits | Risks | Cost/complexity | Reversibility | Decision and rationale |
|---|---|---|---|---|---|
| Introduce new, more impressive-sounding benefit metrics at this final template, since it is the last opportunity to shape the submission's closing impression | Could present a broader-looking benefits case | Directly violates A-01 and would be indefensible under a panel challenge asking "where was this metric specified earlier?" | Lower traceability discipline, high risk of an unsupported-claim challenge at the exact worst moment (the final substantive artefact) | Reversible before submission, not during the defence | Rejected outright. |
| Measure adoption by AI output volume (number of recommendations produced), since it is simpler to instrument | Simpler metric to implement | Rewards quantity over quality; a workflow producing many recommendations humans routinely override would score well on this metric while actually failing at adoption, directly contradicting the human-in-the-loop principle this submission is built on | Lower instrumentation cost, fundamentally wrong incentive structure | Reversible but the wrong metric could already have misdirected effort by the time it's caught | Rejected. A-04 requires an acceptance/escalation-based metric, not a volume-based one. |
| Trace all tracked benefits to 01's existing KPI tree (with two explicitly marked "baseline pending"), continuous (not one-time) value-leakage tracking, a four-item master stop-criteria register consolidating (not replacing) prior artefacts' own criteria, and an acceptance/escalation-based adoption metric | Closes the loop back to 01 honestly, including the still-open baseline gap; consolidates scattered stop criteria into one lookup point without creating a competing authority; defines adoption correctly even though it cannot yet be measured | The two headline KPIs (cycle time, expense ratio) still cannot report a number, which may look incomplete at this final stage — but this is the honest state, not a flaw in this artefact | Medium — one consolidating framework, reusing every prior decision | Reversible; the two pending baselines can be filled in once 02's comparator pilot executes | Selected. The only option consistent with CTRL-CBC-01 through CTRL-CBC-04 and the evidence-led discipline maintained across all 32 templates. |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-CBC-01 | Every tracked benefit traces to 01's existing KPI tree | Review of the Required analysis and decisions table against 01_BUSINESS_CASE.md | All four tracked benefits cite their origin in 01/02; none is newly introduced | This artefact, Required analysis and decisions table | AI Product Owner |
| CTRL-CBC-02 | Value-leakage cost lines are tracked continuously, not only at sign-off | Review of the value-leakage tracking decision for a stated recurring cadence | Monthly variance reporting is specified, not a one-time check | This artefact, Required analysis and decisions table | Finance |
| CTRL-CBC-03 | All prior stop criteria are consolidated into one register without superseding their originating artefacts | Cross-check the master register's four items against 01/15/18/23/28 | Each item cites its exact originating artefact; none is restated with different terms | This artefact, Required analysis and decisions table | AI Product Owner |
| CTRL-CBC-04 | Adoption is measured by human-approver engagement, never AI output volume | Review of the adoption-metric definition | Metric is acceptance/escalation-rate-based, explicitly excluding raw output volume | This artefact, Required analysis and decisions table | Group Chief Claims Officer |

## Traceability

| Inject/requirement | Architecture/ADR | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| INJ-001, INJ-002 (board target, no-AI challenge) | ADR-01 (11_ADR_REGISTER.md) | Baseline measurement instrumentation (not yet implemented, per 01/02's own open status) | Not yet defined | Two of four tracked benefits (cycle time, expense ratio) cannot report a number until this instrumentation exists. |
| INJ-006 (value leakage) | CTRL-BC-03 (01) | Monthly value-leakage variance report (not yet implemented) | Not yet defined | Continuous tracking is specified but not yet built; this closes a design gap, not an implementation one. |
| Confirmed fairness breaches (15/18); INJ-089 (23); non-compensable gates (28) | Cross-referenced throughout | N/A — consolidation only | N/A | The master stop-criteria register's value depends on each originating artefact's own criterion remaining current; any future change to one must be reflected here too. |
| Adoption metric (03/04) | Reused human-approval-gate design | Acceptance/escalation/override tracking (not yet implemented, no pilot exists) | Not yet defined | Cannot be measured until a workflow reaches a pilot, per 28's verdict. |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| Two of the four tracked benefits (cycle time, expense ratio) still cannot report a baseline number, an open issue inherited from 01/02 and not resolved by this or any subsequent artefact | High (inherited) | This is the same residual risk logged since Step 1; this artefact makes the ongoing tracking framework explicit but does not itself close the baseline gap | Chief Actuary | Open — inherited | Before any improvement percentage is published (per CTRL-BC-01/CTRL-DMAIC-01) |
| The master stop-criteria register (this artefact) must be kept synchronised with its four source artefacts; if any of 01/15/18/23/28 is revised, this register could go stale | Medium | Establish a review trigger tied to any revision of the four source artefacts | AI Product Owner | Open | Whenever 01, 15, 18, 23, or 28 is revised |
| No workflow has reached a pilot, so the adoption metric, value-leakage variance report, and benefits-realisation tracking are all specified but unmeasured as of this final artefact | High | Consistent with 28's "not production-ready" verdict; this is the expected and honestly-disclosed state at the end of a 32-artefact design-and-specification submission | AI Product Owner, Group CEO | Open | Once any workflow reaches a pilot, per 29's 90-day roadmap |
| This is the final of 32 templates; the submission's overall completeness (32/32 artefacts, 0 implementation files) should now be independently re-verified against submission/evidence/PROGRESS_REPORT.md before final packaging | High | Re-run the progress-report tool and cross-check its count against this closing statement before declaring the submission complete | AI Product Owner | Open | Immediately after this artefact is finalised |