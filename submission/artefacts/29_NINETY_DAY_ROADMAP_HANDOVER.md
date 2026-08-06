# 29 Ninety Day Roadmap Handover

## Purpose

Prioritised 90-day roadmap, dependencies, training and handover acceptance, sequencing the implementation gaps consolidated in 28_PRODUCTION_READINESS.md into a defensible sprint plan and formalising operational handover to the roles named in 26_TARGET_OPERATING_MODEL.md.

## Acceptance criteria

- The artefact is evidence-led and references supplied paths, record locators and inject IDs.
- Facts, assumptions, inference, conflict, decision and residual risk are distinguishable.
- Temporal, jurisdictional, authorization and authority boundaries are explicit where relevant.
- Owners, approvals, review triggers and measurable acceptance gates are named.
- The artefact contains no unsupported coverage, pricing, reserve, payment or treaty conclusion.

## Artefact-specific acceptance criteria

- Every 90-day roadmap item traces to a specific gap already identified in 28_PRODUCTION_READINESS.md's go/no-go criteria; no new, previously-undisclosed work item is introduced here (CTRL-NDR-01).
- The two time-sensitive items already flagged with a concrete deadline (OM-Large price-shock decision, 2026-08-15; DOWN-01/DOWN-03 status confirmation, immediate) are scheduled in week 1, not left to compete with lower-urgency items (CTRL-NDR-02).
- Handover acceptance requires each of the three named operational owners (26_TARGET_OPERATING_MODEL.md) to explicitly sign off on their workflow's readiness, not a single blanket handover signature (CTRL-NDR-03).
- The roadmap explicitly states what will NOT be achieved within 90 days (full 96-inject coverage, live pilot readiness), consistent with 28's honest "not production-ready" verdict (CTRL-NDR-04).

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| EVID-122 | submission/artefacts/28_PRODUCTION_READINESS.md | participant-authored | 2026-08-06 | — | Source of every roadmap item below; this artefact sequences 28's gaps, it does not identify new ones. |
| EVID-121 | submission/evidence/inject_traceability.csv (section=full_file_snapshot_at_Step_28) | participant-authored | 2026-08-06 | — | Reused from 28; the ~30-inject coverage gap and 11 not-yet-addressed rows directly inform which inject domains the roadmap prioritises. |
| EVID-109 | data/model_costs.csv | domain_specific/vendor_pricing | 2026-08-15 | global | Reused from 23; the OM-Large price-shock deadline (2026-08-15) is the roadmap's most time-critical single item. |
| EVID-107 | data/downtime_events.csv (event_id=DOWN-01;DOWN-02;DOWN-03) | domain_specific/incident_record | 2026-07-29 | MULTI | Reused from 24/25; DOWN-01/DOWN-03's unresolved status is the second most time-critical item. |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | 90 days is measured from this artefact's drafting date (2026-08-06), giving a roadmap window of 2026-08-06 to approximately 2026-11-04; the OM-Large price-shock deadline (2026-08-15) falls within the first 9 days of this window and must be resolved before, not during, the roadmap's later phases. | Explicit dating convention consistent with case/START_HERE.md's 2026-08-01 workshop baseline | Miscalculating the window would misalign the OM-Large deadline against the roadmap's week-1 commitment. | AI Product Owner | Ongoing |
| A-02 | The roadmap is sequenced by non-compensable-gate priority first (gates 1/2/3/5/6/8 from 28, since these block any pilot cutover), then by severity of open issues (High severity items before Medium), not by ease of implementation; this may mean harder items are scheduled earlier than easier ones. | 28_PRODUCTION_READINESS.md's go/no-go criteria; requirements/SCORING_MODEL.md's non-compensable-gate framing | Sequencing by ease-of-implementation instead would risk delivering a 90-day roadmap that completes many low-priority items while non-compensable gates remain unaddressed. | AI Product Owner | Ongoing |
| A-03 | Training for the three named operational owners (26_TARGET_OPERATING_MODEL.md) can only begin once each workflow has at least a passing implementation of its gate-1-adjacent controls (output-schema enforcement); training on a specification alone, without a working system to train against, is not counted as meaningful training in this roadmap. | 26_TARGET_OPERATING_MODEL.md (reused); 28's gate-1 go/no-go criterion | Training scheduled too early would be training against a moving target, wasting the trainees' time and requiring repetition once the implementation stabilises. | AI Product Owner | Before scheduling any training session |
| A-04 | Handover acceptance is per-workflow, mirroring 28's per-workflow cutover/rollback decision (A-03 in that artefact); a workflow may be handed over to its operational owner independently of the other two reaching the same readiness state. | 28_PRODUCTION_READINESS.md (A-03, reused) | A combined handover would force all three workflows to reach readiness simultaneously, contradicting the independent-cutover principle already established. | AI Product Owner | Ongoing |

## Required analysis and decisions

| Decision/question | Evidence | Analysis | Decision/output | Owner | Status |
|---|---|---|---|---|---|
| What are the week-1 (days 1–9) priority items, given the OM-Large deadline? | data/model_costs.csv (EVID-109); data/downtime_events.csv (EVID-107) | Per CTRL-NDR-02, two items cannot wait: (a) OM-Large budget-response decision (absorb/substitute/renegotiate, per 23's A-02) before 2026-08-15; (b) DOWN-01/DOWN-03 current-status confirmation (per 24/25's open issues), since the true incident duration affects whether the 21-day max_ai_outage_days ceiling (data/continuity_requirements.csv) is already breached | Week 1: Finance/AI Product Owner resolve the OM-Large decision; CISO/Group Chief Claims Officer confirm DOWN-01/DOWN-03's actual current status | Finance, AI Product Owner, CISO | Decided |
| What are the days 10–45 (weeks 2–7) implementation priorities? | 28_PRODUCTION_READINESS.md's go/no-go criteria (reused) | Per A-02, non-compensable-gate-blocking items come first: gate-1 output-schema/system-edge enforcement (04/10/14), gate-5 wording/endorsement preservation (05/06/07), gate-3 prompt-injection defence (16), each implemented against Workflow A first (per 28's phased-cutover decision) since Workflow A has the deepest existing specification | Weeks 2–7: implement Workflow A's gate-1/3/5-adjacent controls; begin (not complete) Workflow B implementation in parallel if capacity allows | AI Product Owner | Decided |
| What are the days 46–75 (weeks 8–11) priorities? | 28's remaining gate criteria (gate 2 tenant isolation, gate 6 manual-mode procedures, gate 8 test execution) | Gate 2 (EV-17 test) and gate 6 (manual-mode procedures for the three named continuity capabilities, per 25) are scheduled here since they depend on Workflow A/B's core logic existing first; gate-8 test execution against the 9 representative tests from 22 begins as soon as any workflow has a testable implementation | Weeks 8–11: tenant-isolation gate implementation and test; manual-mode procedure drafting and drill; begin test execution against 22's fixtures | CISO, AI Product Owner | Decided |
| What are the days 76–90 (week 12+) priorities, and what is explicitly NOT achieved? | 28's honest verdict (A-01, reused); A-02's ~30-inject coverage gap | Per CTRL-NDR-04: full 96-inject coverage is NOT achieved within 90 days (only a subset of the 66 logged plus some of the ~30 unlogged injects will be addressed); live pilot readiness is NOT achieved (28's verdict stands); Workflow C implementation is NOT started within this window given the phased-cutover sequencing | Days 76–90: consolidate Workflow A's handover to Group Chief Claims Officer (per A-03/A-04, assuming gate-1/3/5 pass); document remaining gap for the next roadmap cycle; explicitly state Workflow B/C's continued "argued, not yet implemented" status | AI Product Owner, Group CEO | Decided |

## Alternatives and trade-offs

| Option | Benefits | Risks | Cost/complexity | Reversibility | Decision and rationale |
|---|---|---|---|---|---|
| Sequence the roadmap by ease of implementation (quick wins first) to show fast, visible progress | Faster-looking early momentum | Non-compensable gates could remain unaddressed for the full 90 days if they happen to be the harder items, directly contradicting the priority discipline the entire submission has been built on | Lower planning friction, high risk of prioritising the wrong work | Reversible but wastes 90 days of the wrong sequencing | Rejected. A-02 requires gate-blocking priority regardless of implementation difficulty. |
| Attempt to complete all three workflows within 90 days to present a more complete-sounding roadmap | Appears more ambitious/complete | Given zero current implementation (28's verdict), attempting all three simultaneously risks completing none of them to a gate-passing standard; directly risks the same overclaiming problem rejected throughout this submission | Higher apparent ambition, high risk of shallow, non-gate-passing progress across all three instead of solid progress on one | Reversible but 90 days once spent cannot be redone | Rejected. Consistent with 28's phased per-workflow cutover decision (A-03), concentrating effort on Workflow A first is more likely to produce a genuinely gate-passing result. |
| Gate-priority-sequenced roadmap concentrating on Workflow A within the 90-day window, with explicit week-1 handling of the two time-critical items, and an honest statement of what is NOT achieved (full inject coverage, live pilot readiness, Workflow C start) | Directly traceable to 28's gap assessment; handles the two genuinely urgent items first; sets a realistic, defensible 90-day scope rather than an overclaimed one | A reviewer might perceive slower overall progress across all three workflows; this is an intended trade-off for genuine gate-passing depth on one workflow | Medium — one roadmap, phased by gate priority | Reversible; the next 90-day cycle can pick up Workflow B/C | Selected. Matches CTRL-NDR-01 through CTRL-NDR-04 and 28's own phased-cutover and honest-verdict decisions. |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-NDR-01 | Every roadmap item traces to a gap already identified in 28 | Cross-check each roadmap item against 28's Required analysis and decisions / Open issues tables | No roadmap item introduces previously-undisclosed work | This artefact, Required analysis and decisions table | AI Product Owner |
| CTRL-NDR-02 | The two time-sensitive items are scheduled in week 1 | Review of the Required analysis and decisions table's week-1 row | OM-Large decision and DOWN-01/03 status confirmation both appear in the days 1–9 row | This artefact, Required analysis and decisions table | AI Product Owner |
| CTRL-NDR-03 | Handover acceptance requires per-workflow sign-off | Review of the handover decision against 26's three named operational owners | Each of the three owners has an independent sign-off point, not one blanket signature | This artefact, Working assumptions table (A-04) | Group CEO |
| CTRL-NDR-04 | The roadmap explicitly states what will NOT be achieved | Review of the days 76–90 row | Full inject coverage, live pilot readiness, and Workflow C start are explicitly named as not achieved within 90 days | This artefact, Required analysis and decisions table | AI Product Owner |

## Traceability

| Inject/requirement | Architecture/ADR | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| INJ-089 (model price shock) | Cross-referenced to 23_TOKEN_FINOPS.md's A-02 | Budget-response decision (scheduled week 1) | Not yet defined | If the decision is not made by 2026-08-15, the 65% increase is absorbed by default, contradicting 23's own recommendation. |
| INJ-080 (ransomware containment) | Cross-referenced to 24/25's ongoing-incident treatment | Status-confirmation action (scheduled week 1) | Not yet defined | The 21-day max_ai_outage_days ceiling may already be breached; this is not resolvable by the roadmap itself, only by the status confirmation. |
| Non-compensable gates 1/3/5 (21_ASSURANCE_CASE.md, 28_PRODUCTION_READINESS.md) | Reused from 04/05/06/07/10/14/16 | Workflow A implementation (scheduled weeks 2–7) | Gate-specific tests per 22, execution scheduled weeks 8–11 | This is the roadmap's central bet: concentrating on Workflow A first may leave B/C further behind than a parallel approach would, an accepted trade-off per the Alternatives table. |
| Non-compensable gates 2/6/8 (21, 28) | Reused from 08/10/12/13/24/25 | Tenant-isolation gate, manual-mode procedures, test execution (scheduled weeks 8–11) | TEST-EV-17 and the 9 representative tests from 22 | Depends on weeks 2–7's Workflow A implementation existing first; if that slips, this phase slips too. |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| This roadmap has not yet been resourced (no confirmed engineering headcount/budget allocation exists in supplied evidence) | High | Escalate to Group CEO/Finance for resource allocation before week 1 begins | Group CEO, Finance | Open | Before roadmap execution begins |
| Workflow B and C will remain in "argued, not yet implemented" status at the end of this 90-day window, per CTRL-NDR-04's honest disclosure | High (accepted, not concealed) | This is an explicit, accepted trade-off (per the Alternatives table), not an oversight; the next roadmap cycle should address B/C | AI Product Owner | Open — accepted trade-off | At the start of the next 90-day cycle |
| Training for operational owners (A-03) cannot begin until an implementation exists to train against, meaning meaningful training likely does not occur within this 90-day window for any workflow reaching only partial gate-passing status | Medium | Track explicitly; do not claim training was delivered if it was only specification-based | AI Product Owner | Open | Before any handover-acceptance claim is made |
| The ~30-inject coverage gap identified in 28 is not resolved within this 90-day window; only a subset of Workflow A-relevant injects will gain implementation-level coverage | Medium | Accepted scope limitation, consistent with CTRL-NDR-04; full coverage requires multiple roadmap cycles | AI Product Owner | Open — accepted | Ongoing, tracked cycle-over-cycle |