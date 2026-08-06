# 24 Reliability Observability

## Purpose

SLIs, SLOs, error budgets, telemetry, drift, capacity, degraded mode and audit for the three workflows, grounded in the three concrete downtime events already recorded in data/downtime_events.csv and closing the remaining numeric gaps in REQ-NF-14/15/17/18 (checkpointing, rollback, degraded mode, auditability) from 09/10/13's open issues.

## Acceptance criteria

- The artefact is evidence-led and references supplied paths, record locators and inject IDs.
- Facts, assumptions, inference, conflict, decision and residual risk are distinguishable.
- Temporal, jurisdictional, authorization and authority boundaries are explicit where relevant.
- Owners, approvals, review triggers and measurable acceptance gates are named.
- The artefact contains no unsupported coverage, pricing, reserve, payment or treaty conclusion.

## Artefact-specific acceptance criteria

- Each of the three concrete downtime events (DOWN-01 PolicyCore-IN, DOWN-02 ClaimsImages, DOWN-03 AI-Primary-EU) has a named SLI/SLO and a specified degraded behaviour, not only a general resilience statement (CTRL-RO-01).
- Every SLI has an explicit alert threshold and named owner, never left generic (CTRL-RO-02).
- DOWN-01 and DOWN-03's still-open status (no end timestamp in supplied evidence) is treated as an ongoing incident requiring current degraded-mode operation, not a resolved historical event (CTRL-RO-03).
- Every audit event referenced ties back to data/audit_events.csv or an equivalent named log, consistent with REQ-NF-18's auditability requirement (CTRL-RO-04).

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| EVID-107 | data/downtime_events.csv (event_id=DOWN-01;DOWN-02;DOWN-03) | domain_specific/incident_record | 2026-07-29 | MULTI | Three concrete downtime events: DOWN-01 PolicyCore-IN read_only mode (ransomware containment, no end time — ongoing); DOWN-02 ClaimsImages offline 2026-07-29 to 2026-07-31 (segmentation); DOWN-03 AI-Primary-EU unavailable (regional outage, no end time — ongoing). |
| EVID-106 | data/error_budgets.csv | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Evidence-envelope schema only; no inject-specific challenge_fact row present, used as generic SLI/SLO-adjacent evidence. |
| EVID-060 | knowledge/AI_DISABLED_CONTINUITY.md | approved/trusted_with_conditions | 2026-01-01 | global | Reused from 13/16; requires controlled manual/deterministic modes when model inference is unavailable — directly informs DOWN-03's degraded-behaviour specification. |
| EVID-041 | case/SOURCE_SYSTEM_FACT_PACK.md | approved/case-pack | 2026-08-01 | MULTI | Reused from 06/10/12/17/19; PolicyCore-IN's "Read-only during containment" and CatVision's "Vendor outage" caveats directly corroborate DOWN-01 and inform the capacity/failure-mode rows below. |
| EVID-045 | starter/baseline_diagnostics.py (executed output) | participant-generated diagnostic | 2026-08-06 | n/a | Reused from 06/10/13/16; confirmed stale-authorization-cache and model-artefact-mismatch defects, both re-examined here as reliability signals requiring dedicated SLIs. |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | DOWN-01 (PolicyCore-IN) and DOWN-03 (AI-Primary-EU) have no recorded end timestamp in data/downtime_events.csv, meaning both are treated as still-ongoing as of this submission's preparation date (2026-08-06); any workflow design assuming PolicyCore-IN is fully read-write or AI-Primary-EU is available would be relying on stale information. | data/downtime_events.csv (EVID-107) | Designing against an assumed-resolved incident that is actually still active would produce a workflow that fails immediately upon deployment. | AI Product Owner, CISO | Ongoing — re-verify before any deployment decision |
| A-02 | DOWN-02's exact 48-hour-58-minute duration (2026-07-29T01:20:00Z to 2026-07-31T18:00:00Z) is the only concrete, closed-duration downtime evidence in the supplied data; it is used as the empirical basis for setting a realistic (not arbitrary) SLO for ClaimsImages availability, rather than inventing an unsupported target. | data/downtime_events.csv (EVID-107) | An SLO set without reference to this real duration could be either unrealistically strict (impossible to meet given demonstrated failure modes) or unrealistically loose (masking a real risk). | AI Product Owner | Before the ClaimsImages SLO is finalised |
| A-03 | Each SLI in this artefact maps to a specific, already-established control from a prior artefact (e.g., the current-authorization re-check gate's latency is an SLI candidate, not a newly invented metric); this artefact's contribution is the SLI/SLO/alert-threshold specification, not new control logic. | Consistent with the reuse-not-reinvent discipline established in 09/11/20 | Inventing new control logic here would duplicate work already specified in 10/13/16. | AI Product Owner | Ongoing |
| A-04 | Auditability (REQ-NF-18) requires every SLI breach and every degraded-mode activation to itself generate an audit event, not only the underlying business action; this closes the previously-unassigned REQ-NF-18 gap first identified in 09_REQUIREMENTS_TRACEABILITY.md Step 10. | data/audit_events.csv (referenced but not yet directly inspected in this pass); 09_REQUIREMENTS_TRACEABILITY.md (REQ-NF-18) | Without this, a degraded-mode activation could occur without leaving an auditable trace, undermining the "auditability and AI-disabled continuity" requirement's own premise. | CISO | Before any degraded-mode transition logic is implemented |

## Required analysis and decisions

| SLI | SLO | Signal/source | Alert threshold | Degraded behaviour | Owner |
|---|---|---|---|---|---|
| PolicyCore-IN read-write availability | Currently not meetable — system is in confirmed read_only mode (DOWN-01, ongoing per A-01); target SLO for a future resolved state: 99.5% read-write availability | data/downtime_events.csv (DOWN-01 mode=read_only, cause=ransomware_containment) | Immediate alert on any workflow attempting a write to PolicyCore-IN while mode=read_only | Workflow A/B treat all PolicyCore-IN data as read-only-and-possibly-stale; no policy-administration write is attempted; endorsement/policy changes are queued for manual entry once containment lifts | Group Chief Claims Officer, CISO |
| ClaimsImages availability | 99.9% (informed by DOWN-02's demonstrated ~49-hour outage as the realistic worst-case reference point, per A-02) | data/downtime_events.csv (DOWN-02 mode=offline, cause=segmentation, duration 2026-07-29T01:20 to 2026-07-31T18:00) | Alert if ClaimsImages unavailability exceeds 4 hours (a fraction of the demonstrated 49-hour worst case, chosen to trigger response well before reaching that severity) | Workflow A operates without image evidence, explicitly labelling any output "image evidence unavailable — pending ClaimsImages restoration"; no fraud/repair-estimate conclusion is drawn from absent image data | Group Chief Claims Officer |
| AI-Primary-EU model-inference availability | Currently not meetable — system is confirmed unavailable (DOWN-03, ongoing per A-01, cause=regional_outage); target SLO for a future resolved state: 99.5% | data/downtime_events.csv (DOWN-03 mode=unavailable, cause=regional_outage) | Immediate alert on any workflow attempting a model call routed to AI-Primary-EU while unavailable | Every EU-region workflow request falls back to AI-disabled continuity mode per knowledge/AI_DISABLED_CONTINUITY.md (EVID-060); no silent regional failover to an unapproved alternate model occurs (consistent with CTRL-DGL-03's refuse-and-escalate pattern) | AI Product Owner, CISO |
| Current-authorization re-check gate latency and correctness | 100% of gated actions re-check live entitlement status; p99 re-check latency under an as-yet-unset threshold | Reused from 06/10 (CTRL-DGL-01); confirmed live cache-staleness defect (starter/baseline_diagnostics.py, EVID-045) as the motivating signal | Alert on any action proceeding without a successful live re-check (a gate-bypass event, treated as critical severity) | On entitlement-source unavailability, the gate denies the action rather than failing open, per CTRL-DGL-01's existing specification | CISO |
| Model-artefact verification gate correctness | 100% of model-backed calls verify artefact hash against model_registry.csv before use | Reused from 06/10/13 (CTRL-DGL-03); confirmed live GEN-SUM-3 mismatch (starter/baseline_diagnostics.py, EVID-045) | Alert on any mismatch event, distinguishing accidental deployment drift from suspected tampering (per 16_THREAT_ABUSE_MODEL.md's adversarial framing) | On mismatch, the call is refused and escalated, never proceeding with a best-effort fallback | AI Product Owner, CISO |
| CatVision (hazard/imagery vendor) availability | No historical downtime event recorded for CatVision in supplied evidence beyond the general "Vendor outage" caveat (case/SOURCE_SYSTEM_FACT_PACK.md); SLO deferred pending a concrete incident record | case/SOURCE_SYSTEM_FACT_PACK.md (EVID-041, CatVision row) | To be set once a concrete downtime event is recorded (currently no numeric basis exists, per A-02's evidence-based-SLO principle) | Workflow C falls back to the last-verified hazard snapshot with an explicit staleness label, per 10_C4_ARCHITECTURE.md's existing Workflow C failure-mode specification | Reinsurance Director |

## Alternatives and trade-offs

| Option | Benefits | Risks | Cost/complexity | Reversibility | Decision and rationale |
|---|---|---|---|---|---|
| Set generic, round-number SLOs (e.g., "99.9% for everything") without reference to actual demonstrated downtime evidence | Simple, uniform, easy to state | Arbitrary targets could be unrealistic given DOWN-01/02/03's demonstrated failure patterns; a target set without evidence is itself a form of the unsupported-claim problem this package prohibits | Lowest analytical effort, high risk of an indefensible SLO under panel challenge | Reversible but undermines credibility if the arbitrary basis is exposed | Rejected. A-02 requires SLOs informed by the one concrete closed-duration incident actually in evidence (DOWN-02). |
| Treat DOWN-01 and DOWN-03 as historical/resolved since no explicit "ongoing" label appears in the data, and design workflows assuming normal read-write/inference availability | Simpler workflow design (no degraded-mode branching needed for these two systems) | The absence of an end timestamp is the strongest available signal that these incidents are still active; assuming resolution without evidence risks a workflow that fails immediately in the actual current state | Lower design cost now, high deployment-failure risk | Reversible but costly if discovered only at deployment time | Rejected. A-01 requires treating the missing end timestamp as evidence of an ongoing incident, not silence to be filled with a convenient assumption. |
| Evidence-based SLO for the one system with a concrete closed-duration incident (ClaimsImages), explicit "not yet meetable" status for the two ongoing incidents (PolicyCore-IN, AI-Primary-EU) with a degraded-behaviour specification instead of a numeric SLO, and reused (not reinvented) SLIs for the two already-specified security gates | Honestly distinguishes what can be evidence-based now from what cannot; gives every one of the three downtime events and two security gates a concrete monitoring specification | Two of six SLI rows lack a numeric SLO (by design, since none can be honestly set yet); CatVision has no incident-based SLO at all | Medium — six SLI rows, three fully specified, three explicitly deferred with a stated reason | Reversible; numeric SLOs can be added once incidents resolve or new data arrives | Selected. Matches the evidence-led discipline applied throughout this submission; avoids both arbitrary numbers and false assumptions of resolution. |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-RO-01 | Each of the three downtime events has a named SLI/SLO and degraded behaviour | Review of the Required analysis and decisions table against data/downtime_events.csv | All three DOWN-* events have a corresponding row with a specific degraded-behaviour specification | This artefact, Required analysis and decisions table | AI Product Owner |
| CTRL-RO-02 | Every SLI has an explicit alert threshold and named owner | Review of the Alert threshold and Owner columns | No row leaves either column generic or blank | This artefact, Required analysis and decisions table | AI Product Owner |
| CTRL-RO-03 | DOWN-01/DOWN-03's ongoing status is treated as current, not historical | Review of workflow design assumptions against A-01 | No workflow design assumes PolicyCore-IN is read-write or AI-Primary-EU is available without re-verifying current status first | This artefact, Working assumptions table | CISO |
| CTRL-RO-04 | Every SLI breach/degraded-mode activation generates an audit event | Design review of degraded-mode transition logic against data/audit_events.csv | No degraded-mode activation occurs without a corresponding audit-event write | submission/tests (deferred) | CISO |

## Traceability

| Inject/requirement | Architecture/ADR | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| REQ-NF-14, REQ-NF-15 (checkpointing, rollback) | Cross-referenced to 16_THREAT_ABUSE_MODEL.md's checkpoint-replay idempotency control | Checkpoint/rollback mechanism (not yet implemented) | TEST-EV-13 (22_EVALUATION_TEVV.md, deferred) | This artefact does not itself close checkpointing/rollback numerically; that remains with 16's idempotency-key design. |
| REQ-NF-17 (degraded mode) | Cross-referenced to 13_MODEL_PROMPT_LIFECYCLE.md's AI-disabled continuity fallback | Degraded-mode transition logic per SLI (this artefact, not yet implemented) | Not yet defined | This artefact gives degraded mode concrete triggers (the three SLIs) but implementation remains outstanding. |
| REQ-NF-18 (auditability) | New: SLI-breach-to-audit-event linkage (this artefact, A-04) | Audit-event generation on degraded-mode transition (not yet implemented) | CTRL-RO-04 (deferred) | First explicit specification of this linkage; data/audit_events.csv's actual schema not yet cross-verified against this requirement. |
| Confirmed defects DEF-007, DEF-008 | ADR-08, ADR-09 (11) | Current-authorization and model-artefact verification gates (not yet implemented) | CTRL-DGL-01, CTRL-DGL-03 (deferred) | This artefact adds SLI/alerting framing; the gates themselves remain unimplemented as recorded since Step 6. |
| DOWN-01 (PolicyCore-IN, ransomware containment) | Cross-referenced to case/SOURCE_SYSTEM_FACT_PACK.md's "Read-only during containment" caveat | Read-only-mode-aware workflow logic (not yet implemented) | Not yet defined | Containment resolution date unknown; workflows must remain read-only-aware indefinitely until confirmed otherwise. |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| DOWN-01 and DOWN-03 have no recorded resolution; this submission cannot determine whether they remain active as of the actual current date | High | Escalate to CISO/Group Chief Claims Officer to obtain a current status confirmation before any deployment decision | CISO | Open | Before any deployment decision |
| None of the six SLI rows has an implemented monitoring/alerting mechanism yet | High | Track alongside the "no implementation code" gap already logged in ARTEFACT_STATE_LOG.md | AI Product Owner | Open | Before templates 26–28 (target operating model, production readiness) |
| CatVision has no concrete incident-based SLO; only a general vendor-outage caveat exists | Medium | Set once a concrete downtime event is recorded, per A-02's evidence-based principle | Reinsurance Director | Open | When a CatVision incident is recorded |
| The audit-event schema (data/audit_events.csv) has not been directly cross-verified against this artefact's REQ-NF-18 linkage requirement (A-04) | Medium | Verify schema compatibility during implementation | CISO | Open | Before degraded-mode transition logic is implemented |