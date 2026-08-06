# 02 Dmaic Workbook

## Purpose

Define, Measure, Analyse, Improve and Control evidence with baselines and control plan for the catastrophe claim cycle-time and expense-ratio targets raised in INJ-001, tested against the no-AI alternative raised in INJ-002.

## Acceptance criteria

- The artefact is evidence-led and references supplied paths, record locators and inject IDs.
- Facts, assumptions, inference, conflict, decision and residual risk are distinguishable.
- Temporal, jurisdictional, authorization and authority boundaries are explicit where relevant.
- Owners, approvals, review triggers and measurable acceptance gates are named.
- The artefact contains no unsupported coverage, pricing, reserve, payment or treaty conclusion.

## Artefact-specific acceptance criteria

- No improvement percentage against the 20% cycle-time / 12% expense-ratio target is published without a logged baseline measurement date and method (CTRL-DMAIC-01).
- The endorsement-timing defect (END-771 pattern) is surfaced only as a flagged conflict; no implementation auto-approves or backdates an endorsement (CTRL-DMAIC-02).
- A dated, documented no-AI comparator result exists before Business Case sign-off proceeds (CTRL-DMAIC-03).

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| EVID-001 | data/board_requests.csv (record_id=INJ-001-BOARD_REQUESTS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Defines the target statement (20% cycle-time, 12% expense-ratio); this is the Define-phase problem statement, not a measured fact. |
| EVID-003 | data/no_ai_baselines.csv (record_id=INJ-002-NO_AI_BASELINES) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Source for the Measure-phase no-AI comparator; only a narrative row is supplied, no time-series baseline. |
| EVID-004 | data/process_bottlenecks.csv (record_id=INJ-002-PROCESS_BOTTLENECKS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Candidate root-cause evidence for the Analyse phase; evidence-envelope granularity, not a process-mining extract. |
| EVID-014 | data/endorsements.csv (endorsement_id=END-771) | domain_specific/policy_administration_issuance | 2026-07-28T00:00:00+05:30 | IN | Concrete example of a cycle-time/sequencing defect (endorsement issued after the disputed loss window) usable as a control-chart data point. |
| EVID-017 | data/billing_events.csv (record_id=INJ-010-BILLING_EVENTS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Cancellation/reinstatement/premium-receipt ordering conflict; candidate bottleneck contributing to cycle-time variability. |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | The Define-phase problem statement is the board's stated target (INJ-001), not an agreed and scoped project charter. | data/board_requests.csv status is `unverified`. | Proceeding to Measure without a charter risks solving the wrong problem or an unscoped one. | Group Chief Claims Officer | Before Measure phase starts |
| A-02 | No time-series cycle-time or expense-ratio baseline exists in the supplied evidence; only narrative/challenge_fact rows are present. | Reviewed data/board_requests.csv, data/kpi_conflicts.csv — both are evidence-envelope schema (record_id, entity_id, event_time, status, value, source_system, jurisdiction, notes), not metric time series. | Any "20% reduction" claim cannot be verified without first establishing this baseline. | Chief Actuary | Before any improvement is claimed |
| A-03 | The endorsement-timing defect (INJ-008, EVID-014) is treated as one concrete, in-scope example of a cycle-time/process defect, not as a coverage or claims decision. | data/endorsements.csv, data/policies.csv, data/loss_events.csv | Treating it as a coverage decision would breach the prohibited-autonomy boundary (INJ-005). | Group Chief Claims Officer | Ongoing |

## Required analysis and decisions

| Define statement | Measure baseline | Root cause | Improvement experiment | Control metric | Control owner |
|---|---|---|---|---|---|
| Reduce catastrophe claim cycle time by up to 20% and expense ratio by up to 12% without weakening claims independence, reserving governance or consumer protection (INJ-001; data/board_requests.csv) | No quantified baseline is currently attached to the supplied evidence; this workbook records the requirement to instrument claim-open-to-decision timestamps (e.g., using loss_events.csv occurred_start/normalized_start_utc and claims.csv reported_at as start markers) before any percentage claim is made | Candidate contributing factors identified from supplied evidence: (1) endorsement issuance sequencing defect — END-771 issued 2026-07-29T10:11+05:30 for a loss window starting 2026-07-28T23:15+05:30, i.e., issued after loss occurrence (EVID-014); (2) billing/cancellation/reinstatement event ordering conflict (INJ-010, EVID-017); (3) manual evidence-reconciliation effort implied by data/process_bottlenecks.csv (INJ-002) | Bounded AI evidence-reconciliation support (Workflow A) that surfaces the endorsement-timing conflict and event-ordering conflict as flagged evidence for human review, without auto-approving or backdating any endorsement | Cycle time from claim reported_at to first documented human evidence-review decision; percentage of claims with a flagged, unresolved temporal or authority conflict at time of first review | Group Chief Claims Officer |
| Deliver most of the above benefit via policy-wording rationalisation, identity repair and workflow redesign without generative AI (INJ-002; data/no_ai_baselines.csv, data/process_bottlenecks.csv) | Requires a dated, quantified no-AI pilot or historical comparator; not present in supplied evidence — recorded here as a Measure-phase gap, not assumed true or false | Root cause of the no-AI claim's plausibility: wording fragmentation (INJ-007, three concurrent HPP wordings) and identifier fragmentation (INJ-030 address/geocode collisions) are structural data-quality defects that process redesign can address without AI | Run the no-AI remediation (wording rationalisation, identity/address repair) as a controlled comparator alongside the AI-assisted pilot, on a matched claim sample | Percentage of evidence-reconciliation time attributable to wording/identity ambiguity, measured before and after remediation | Process Excellence Lead |

## Alternatives and trade-offs

| Option | Benefits | Risks | Cost/complexity | Reversibility | Decision and rationale |
|---|---|---|---|---|---|
| Measure first, then decide AI vs no-AI (recommended) | Avoids committing to either option before evidence exists; directly responds to INJ-002's challenge | Delays visible progress on the board's cycle-time target | Low incremental cost; requires instrumentation effort | Fully reversible | Selected. Per A-02, no baseline currently exists; measuring before improving is the only evidence-led path available given the supplied data. |
| Commit to AI-assisted Workflow A immediately without a no-AI comparator | Faster visible action on the board target | Directly contradicts the no-AI challenge (INJ-002) and risks over-crediting AI for gains achievable by data-quality fixes | Higher build cost, unclear incremental benefit | Partially reversible (AI-disabled continuity mode exists, but sunk build cost is not) | Rejected for this phase. Cannot be justified without first executing the Measure phase. |
| Rely on wording/identity rationalisation only, deprioritising any AI evidence-support tooling | Lowest risk surface; addresses INJ-007/INJ-030 root causes directly | May not scale to catastrophe-volume evidence reconciliation across six jurisdictions | Lower build cost, higher ongoing manual effort | Fully reversible | Deferred. Viable candidate pending the comparator experiment above; not ruled in or out here. |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-DMAIC-01 | No cycle-time/expense-ratio improvement percentage is published without a dated baseline | Review of any benefits report against a logged baseline measurement | Every reported percentage cites a baseline measurement date and method | submission/artefacts/01_BUSINESS_CASE.md | Chief Actuary |
| CTRL-DMAIC-02 | Endorsement-timing defect (EVID-014) is surfaced as flagged evidence, never auto-corrected or backdated | Code/process review of any Workflow A implementation | Implementation raises a conflict flag for END-771-pattern cases and takes no coverage action | submission/src (to be implemented in a later pass) | Group Chief Claims Officer |
| CTRL-DMAIC-03 | No-AI comparator experiment is run on a matched sample before AI investment is finalised | Comparative pilot design review | A documented, dated comparator result exists before final Business Case sign-off | submission/artefacts/01_BUSINESS_CASE.md (CTRL-BC-02) | AI Product Owner |

## Traceability

| Inject/requirement | Architecture/ADR | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| INJ-001 | Deferred to submission/artefacts/10_C4_ARCHITECTURE.md | Not yet implemented | Baseline instrumentation not yet executed | Target may be unachievable or unmeasurable with current system fragmentation. |
| INJ-002 | N/A — governance/process decision | Comparator pilot design (not yet executed) | To be defined in submission/artefacts/22_EVALUATION_TEVV.md | Comparator may show no-AI approach insufficient at scale, requiring re-scoping. |
| INJ-008 (endorsement timing) | To be recorded in submission/artefacts/11_ADR_REGISTER.md (deferred) | Conflict-flagging logic (not yet implemented) | Unit test for END-771-pattern detection (not yet written) | Root-cause fix (why issuance postdates the loss window) is a policy-administration system defect outside this package's control. |
| INJ-010 (cancellation/reinstatement race) | Deferred | Not yet implemented | Not yet defined | Requires cross-system event-ordering reconciliation beyond the supplied evidence-envelope granularity. |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| No quantified cycle-time/expense-ratio baseline exists in supplied evidence | High | Treat the 20%/12% figures as an unverified target throughout; do not report progress against them until a baseline is measured | Chief Actuary | Open | Before any improvement percentage is published |
| No-AI comparator (INJ-002) has not been executed | High | Require comparator pilot before AI investment sign-off (CTRL-DMAIC-03) | AI Product Owner | Open | Before Business Case final sign-off |
| Endorsement-timing defect (EVID-014) root cause is in a system outside this package's control (PolicyCore-IN per case/SOURCE_SYSTEM_FACT_PACK.md) | Medium | Flag and escalate to policy administration owner; this package can only surface, not fix, the upstream defect | Group Chief Claims Officer | Open | When a policy-administration remediation owner is assigned |
