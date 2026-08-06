# 28 Production Readiness

## Purpose

Gap assessment, acceptance gates, cutover, rollback, support and residual risks for the three workflows, consolidating every "not yet implemented" and open-issue finding logged across artefacts 01–27 into one production-readiness verdict.

## Acceptance criteria

- The artefact is evidence-led and references supplied paths, record locators and inject IDs.
- Facts, assumptions, inference, conflict, decision and residual risk are distinguishable.
- Temporal, jurisdictional, authorization and authority boundaries are explicit where relevant.
- Owners, approvals, review triggers and measurable acceptance gates are named.
- The artefact contains no unsupported coverage, pricing, reserve, payment or treaty conclusion.

## Artefact-specific acceptance criteria

- The overall readiness verdict is stated honestly as "not production-ready" given zero implementation exists, consistent with the claim-strength discipline established in 21_ASSURANCE_CASE.md; no cutover date is proposed without that caveat (CTRL-PR-01).
- Every one of the 8 non-compensable gates from 21_ASSURANCE_CASE.md has an explicit go/no-go acceptance criterion here, not only a restated claim (CTRL-PR-02).
- Rollback is specified for every workflow independently, reusing the per-workflow AI-disabled continuity design from 04/13, never a single all-or-nothing rollback (CTRL-PR-03).
- The inject-coverage statistics (22 addressed, 33 partially-addressed, 11 not-yet-addressed of 66 total rows logged) are reported exactly as counted, not rounded or minimised (CTRL-PR-04).

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| EVID-106 | data/error_budgets.csv | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Reused from 24; evidence-envelope schema only, used here as the generic basis for the go/no-go error-budget-adjacent acceptance gate. |
| EVID-121 | submission/evidence/inject_traceability.csv (section=full_file_snapshot_at_Step_28) | participant-authored | 2026-08-06 | — | Source of the exact inject-coverage statistics (66 total rows: 22 addressed, 33 partially-addressed, 11 not-yet-addressed) reported in CTRL-PR-04; hash is a point-in-time snapshot since this file is actively edited at every step. |
| — | submission/artefacts/01_BUSINESS_CASE.md through 27_VENDOR_EXIT_RETIREMENT.md | participant-authored | 2026-08-06 | — | Source of every gap/open-issue this artefact consolidates; no single file locator applies across twenty-seven files, consistent with the established multi-file evidence convention. |
| EVID-026 | requirements/SCORING_MODEL.md (section=Mandatory_non-compensable_gates) | approved | 2026-01-01 | global | Reused from 03/14/21; the 8 gates this artefact's go/no-go criteria are built around. |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | This submission's actual state, as of Step 28 in ARTEFACT_STATE_LOG.md, has zero implemented code (no submission/src, no submission/tests); every CTRL-*/ADR-*/gate specified across 27 artefacts is "argued, not yet implemented" in 21_ASSURANCE_CASE.md's own terminology, and this artefact must not claim otherwise. | ARTEFACT_STATE_LOG.md (Outstanding state gaps table, reused across every step since Step 8); 21_ASSURANCE_CASE.md's honest claim-strength discipline | Claiming production readiness without implementation would be the most severe possible violation of this submission's own evidence-led discipline, directly contradicting DEFINITION_OF_DONE.md. | AI Product Owner | Ongoing until implementation begins |
| A-02 | The inject-coverage statistics reported here (66 total logged rows out of the disclosed 96-inject catalogue; 22 addressed, 33 partially-addressed, 11 not-yet-addressed) are a live snapshot as of this artefact's drafting; roughly 30 injects have no row at all yet in inject_traceability.csv, meaning even "not-yet-addressed" undercounts total remaining work. | submission/evidence/inject_traceability.csv (direct count) | Reporting only the 66 logged rows without noting the ~30 unlogged injects would understate the true remaining scope. | AI Product Owner | Before final submission |
| A-03 | Rollback must be specified per workflow, not as one shared switch, because 04_PRODUCT_SERVICE_BLUEPRINT.md already established independent per-workflow AI-disabled continuity as a design requirement; a single combined rollback would contradict that existing decision. | 04_PRODUCT_SERVICE_BLUEPRINT.md (Alternatives table, reused) | A combined rollback would force disabling all three workflows to address an issue in one, an unnecessary and disproportionate operational cost. | AI Product Owner | Ongoing |
| A-04 | "Production readiness" in this artefact means readiness to begin implementation against a validated design, not readiness for a live customer-facing pilot; the distinction matters because this submission's actual deliverable at this stage is the design and control specification (01–27), not running code. | Consistent with case/INTEGRATED_CASE.md's participant mandate ("design and demonstrate") and PACKAGE_SCOPE_AND_ASSUMPTIONS.md's scope boundary | Conflating the two would misrepresent what a 32-artefact documentation package can actually certify. | AI Product Owner | Ongoing |

## Required analysis and decisions

| Decision/question | Evidence | Analysis | Decision/output | Owner | Status |
|---|---|---|---|---|---|
| What is the overall production-readiness verdict for the three workflows? | ARTEFACT_STATE_LOG.md's cumulative "no implementation code" gap (logged at every step since Step 8); 21_ASSURANCE_CASE.md's 8-gate claim-strength table | Per A-01, every non-compensable gate is "argued, not yet implemented/tested" (gates 1, 3, 5, 6) or has an identified but unclosed gap (gate 2 tenant-isolation, gate 8 was gap-then-partially-closed by 22); gate 4 (reproducibility) and gate 7 (disclosure) are the only two gates with direct executed evidence | Verdict: NOT production-ready for a live pilot; READY to begin implementation against a validated 27-artefact design and control specification | AI Product Owner, Group CEO | Decided |
| What go/no-go criterion applies to each of the 8 non-compensable gates before any pilot cutover? | EVID-026; 21_ASSURANCE_CASE.md (all 8 claims, reused) | Gate 1: no-go until output-schema/system-edge enforcement is implemented and tested (CTRL-C4-01/CTRL-ICB-01 pass). Gate 2: no-go until EV-17's tenant-isolation test (22) passes. Gate 3: no-go until CTRL-TAM-01's prompt-injection test (16/22) passes across all three workflows. Gate 4: go — already certified per AUDIT_AND_SANITY_CHECK.md (package-level); participant code must independently re-certify once written. Gate 5: no-go until wording/endorsement preservation (CTRL-DDD-01/02) is implemented and tested. Gate 6: no-go until manual-mode procedures (deferred since 13, still deferred per 25's scenarios) are actually drafted and tested. Gate 7: go — disclosure already executed and evidenced throughout this submission. Gate 8: no-go until the 9 representative tests in 22 execute and pass, and coverage is extended toward the full 96-inject catalogue | Explicit per-gate go/no-go criteria recorded; only gates 4 and 7 currently pass; the other six require implementation before a pilot cutover decision | AI Product Owner | Decided |
| What cutover approach should be used once implementation is complete? | 04_PRODUCT_SERVICE_BLUEPRINT.md's three-independent-workflow decision (reused); A-03 | Cutover proceeds per-workflow, not as a single big-bang release: Workflow A first (most evidence-reconciliation controls already specified in depth across 05/06/07/08), then B, then C, each gated on its own go/no-go criteria passing independently | Phased per-workflow cutover; no workflow's cutover depends on another's completion | AI Product Owner | Decided |
| What rollback mechanism applies if a cutover reveals a problem? | 04_PRODUCT_SERVICE_BLUEPRINT.md; 13_MODEL_PROMPT_LIFECYCLE.md's AI-disabled continuity (reused) | Per A-03, each workflow has its own independent AI-disabled continuity switch; rolling back Workflow A does not affect B or C's live status | Per-workflow rollback confirmed as the mechanism, reusing the already-specified design rather than inventing a new one | AI Product Owner | Decided |

## Alternatives and trade-offs

| Option | Benefits | Risks | Cost/complexity | Reversibility | Decision and rationale |
|---|---|---|---|---|---|
| Declare the submission "production-ready" based on the completeness of its design documentation (27 artefacts), treating thorough specification as equivalent to operational readiness | Would present the most confident-sounding final assessment | Directly false — zero code has been executed against any of the 27 artefacts' specifications; would be the single largest unsupported claim in the entire submission, likely fatal to credibility at the final defence | Lowest honesty cost to write, catastrophic credibility cost if challenged (trivially disprovable by asking "show me the passing test run") | N/A — cannot be walked back credibly once stated | Rejected outright, consistent with every claim-strength discipline established since 09/21. |
| Propose a single all-workflow big-bang cutover with one combined kill switch, to simplify the readiness narrative | Simpler operational story | Directly contradicts the independent per-workflow AI-disabled continuity already decided in 04; would force an unnecessary all-or-nothing rollback if only one workflow has an issue | Lower narrative complexity, unnecessary operational risk concentration | Reversible but would require redesigning the already-decided per-workflow independence | Rejected. A-03 requires reusing the existing per-workflow design. |
| Honest "not production-ready, ready to begin implementation" verdict, per-gate go/no-go criteria for all 8 non-compensable gates (2 currently passing, 6 requiring implementation), phased per-workflow cutover, and per-workflow rollback reusing the existing AI-disabled continuity design | Gives a defensible, specific readiness assessment distinguishing what is actually done (disclosure, package reproducibility) from what remains (everything else); reuses existing designs rather than inventing new cutover/rollback mechanisms | The verdict is less impressive-sounding than a blanket "ready" claim, but this is the honest and defensible position | Medium — one consolidated verdict plus 8 gate-specific criteria plus phased cutover plan | Reversible; the verdict updates automatically as implementation closes each gate | Selected. This is the only option consistent with A-01's honesty requirement and 21_ASSURANCE_CASE.md's established claim-strength discipline. |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-PR-01 | No cutover date is proposed without the "not production-ready" caveat | Review of this artefact's verdict language | Verdict explicitly separates "ready to implement" from "ready for live pilot" | This artefact, Required analysis and decisions table | AI Product Owner |
| CTRL-PR-02 | Every non-compensable gate has an explicit go/no-go criterion | Cross-check against 21_ASSURANCE_CASE.md's 8 claims | All 8 gates have a stated go/no-go criterion, not merely a restated claim | This artefact, Required analysis and decisions table | AI Product Owner |
| CTRL-PR-03 | Rollback is per-workflow, never combined | Review of the Rollback mechanism decision against 04's design | Rollback decision explicitly cites independent per-workflow switches | This artefact, Required analysis and decisions table | AI Product Owner |
| CTRL-PR-04 | Inject-coverage statistics are reported exactly, not rounded | Direct count of submission/evidence/inject_traceability.csv rows by status | Figures match a live count (22/33/11 of 66 logged rows, as of this pass) | This artefact, Working assumptions table (A-02) | AI Product Owner |

## Traceability

| Inject/requirement | Architecture/ADR | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| Non-compensable gates 1–8 (21_ASSURANCE_CASE.md) | Cross-referenced to every ADR (11) and CTRL-* across 01–27 | None implemented (per A-01) | Go/no-go criteria specified here for the first time per gate | Six of eight gates require implementation before any pilot cutover; only gates 4 and 7 currently pass. |
| Inject-coverage gap (~30 unlogged injects, per A-02) | N/A | N/A | Not yet defined | The true remaining scope is larger than the 11 explicitly "not-yet-addressed" rows suggest. |
| Per-workflow cutover/rollback | Reused from 04_PRODUCT_SERVICE_BLUEPRINT.md | Independent AI-disabled continuity switches (not yet implemented) | Not yet defined | Design is specified; the actual switch mechanism (how a workflow is technically disabled) has not been built. |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| Zero implementation exists for any of the 8 non-compensable gates' go/no-go criteria | High | This is the single largest residual risk in the entire submission; no pilot cutover may proceed until at minimum gates 1, 2, 3, 5, 6, 8 pass | AI Product Owner, Group CEO | Open | Before any pilot cutover decision |
| Approximately 30 injects from the 96-inject catalogue have no row at all in inject_traceability.csv | High | Extend coverage incrementally; this gap must be closed or explicitly accepted with rationale before final submission, per DEFINITION_OF_DONE.md's "all 96 injects...mapped" requirement | AI Product Owner | Open | Before final submission |
| This artefact's verdict depends on the accuracy of every prior artefact's own self-reported "not yet implemented" status; no independent audit of those claims has been performed | Medium (framing risk) | Acknowledged explicitly; a defence panel's own challenge is the expected independent check, per requirements/FINAL_DEFENCE.md | AI Product Owner | Open — by design | At the final defence session |
| Several numeric parameters remain unset across prior artefacts (traversal-depth ceiling, cost ceilings, propagation windows, payee-change-timing trigger) and are prerequisites for gates 1/2/3/5 to pass | High | Consolidate all unset numeric parameters into a single implementation checklist, cross-referencing each to its originating artefact, before implementation begins | AI Product Owner | Open | Before implementation planning begins |