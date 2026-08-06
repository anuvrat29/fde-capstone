# 31 Elevator Pitch

## Purpose

Participant-created 60-second and 20-second pitches for AEGIS-INSURE, grounded strictly in this submission's honestly-disclosed state (28_PRODUCTION_READINESS.md's verdict), not an aspirational or inflated summary.

## Acceptance criteria

- The artefact is evidence-led and references supplied paths, record locators and inject IDs.
- Facts, assumptions, inference, conflict, decision and residual risk are distinguishable.
- Temporal, jurisdictional, authorization and authority boundaries are explicit where relevant.
- Owners, approvals, review triggers and measurable acceptance gates are named.
- The artefact contains no unsupported coverage, pricing, reserve, payment or treaty conclusion.

## Artefact-specific acceptance criteria

- Neither the 60-second nor the 20-second pitch claims the system is production-ready, live, or currently reducing cycle time/cost; both describe what has been designed and evidenced, consistent with 28's verdict (CTRL-EP-01).
- Both pitches name the specific stop condition that would halt the programme, not only its benefits (CTRL-EP-02).
- The pitch does not claim a specific cycle-time or expense-ratio improvement percentage, consistent with 01_BUSINESS_CASE.md's CTRL-BC-01 (no improvement reported without a measured baseline) (CTRL-EP-03).
- Both pitches state what the system is explicitly not authorized to do, in brief, mirroring 30_FINAL_DEFENCE.md's closing-question discipline (CTRL-EP-04).

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| EVID-122 | submission/artefacts/28_PRODUCTION_READINESS.md | participant-authored | 2026-08-06 | — | Reused from 29/30; source of the honest "not production-ready, ready to implement" verdict this pitch must not contradict. |
| — | submission/artefacts/01_BUSINESS_CASE.md through 30_FINAL_DEFENCE.md | participant-authored | 2026-08-06 | — | Source of the specific claims condensed into pitch form below; no single file locator applies across thirty files, consistent with the established multi-file evidence convention. |
| EVID-026 | requirements/SCORING_MODEL.md (section=Mandatory_non-compensable_gates) | approved | 2026-01-01 | global | Reused from 03/14/21/28; source of the ten-action prohibition summarised in brief form in both pitches. |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | The pitch's audience (per requirements/FINAL_DEFENCE.md segment 7, "60-second pitch and stop conditions") is the same panel that has already seen the full 30-artefact submission; the pitch is a condensed restatement for memorability, not an attempt to persuade an uninformed audience with claims the panel cannot already verify against the submitted evidence. | requirements/FINAL_DEFENCE.md (EVID-123, reused from 30) | Writing the pitch as if for an uninformed audience risks overclaiming in exactly the way an informed panel would immediately catch, undermining credibility at the closing moment of the defence. | AI Product Owner | Before the defence session |
| A-02 | The 20-second pitch is a strict subset of the 60-second pitch's content (same claims, same stop condition, fewer words), not a separate or differently-scoped message; this avoids the risk of the two pitches appearing to contradict each other if the panel hears both. | Consistent with the internal-consistency discipline maintained across this submission | Two pitches with different scope or emphasis could appear evasive or inconsistent if compared side by side. | AI Product Owner | Before the defence session |
| A-03 | Neither pitch may state a specific benefit percentage (e.g., "20% faster") because 01_BUSINESS_CASE.md's own ADR-01 explicitly defers any such claim until a baseline is measured, which has not yet occurred; the pitch instead describes the mechanism (evidence reconciliation, bounded recommendation) without a numeric benefit claim. | 01_BUSINESS_CASE.md (ADR-01, CTRL-BC-01, reused) | Stating a percentage the submission's own artefacts explicitly say is unmeasured would be a direct, easily-caught contradiction. | AI Product Owner | Ongoing |

## Required analysis and decisions

| Decision/question | Evidence | Analysis | Decision/output | Owner | Status |
|---|---|---|---|---|---|
| What is the 60-second pitch? | Cross-referenced to 01 (business case), 04 (three workflows), 14 (control boundaries), 28 (verdict) | Condenses: the problem (catastrophe-scale evidence fragmentation across contradictory sources), the approach (three bounded evidence-reconciliation workflows, never autonomous on regulated actions), the current state (design and control specification complete across 30 artefacts, zero implementation yet, per 28), and the ask (resource the 90-day roadmap's Workflow A focus, per 29) | 60-second pitch text: "AEGIS-INSURE addresses a real problem at Aurelia Mutual & Re: catastrophe claims, underwriting decisions and reinsurance planning depend on evidence that is fragmented, contradictory and sometimes stale across a dozen source systems — three concurrent policy wordings for one product, endorsements issued after the loss they cover, authorization caches that outlive revocation. We designed three bounded AI-assisted workflows that reconcile this evidence and prepare structured, cited recommendations for a named human decision-maker — never binding coverage, setting a price, adjusting a reserve, or moving money. Every one of those ten regulated actions remains a human-only decision, enforced at the architecture level, not just by policy. Across 30 completed design artefacts, we've specified the domain model, the data-authority rules, the security and privacy controls, the evaluation plan, and an honest gap assessment: this is a validated design, not yet a running system. Our ask is to resource a 90-day implementation sprint focused on the claims-evidence workflow first, where the specification is deepest, so we can prove the design against real fixtures before expanding. We will stop if the no-AI process-redesign alternative — which we've committed to measuring, not skipping — turns out to deliver the same benefit without the added AI governance burden." | AI Product Owner | Decided |
| What is the 20-second pitch? | Same evidence, condensed further | Strict subset per A-02: problem, approach, current state, stop condition, no ask (dropped for length) | 20-second pitch text: "AEGIS-INSURE reconciles fragmented, contradictory claims and underwriting evidence for AMR using three bounded AI workflows that prepare recommendations for a human — never bind, price, reserve, or pay. We've completed the design and control specification; implementation hasn't started. We'll stop if measuring the no-AI alternative shows it works just as well without the governance overhead." | AI Product Owner | Decided |
| What stop condition applies to both pitches? | 01_BUSINESS_CASE.md (Alternatives table, "no-AI process/data-quality remediation only" option); 02_DMAIC_WORKBOOK.md (comparator pilot requirement) | The single most defensible, already-committed stop condition in the submission is the no-AI comparator: if it delivers equivalent benefit without AI's added governance/security/fairness burden, the AI-assisted option is not justified | Stop condition: "we stop if the no-AI comparator, which we've committed to measuring, shows equivalent benefit without AI's governance overhead" | AI Product Owner | Decided |
| What ten-action summary applies in brief form? | 14_INSURANCE_CONTROL_BOUNDARIES.md (reused) | Full ten-action list is too long for either pitch verbatim; a four-action representative summary (bind, price, reserve, pay) is used in the 60-second pitch, with the full ten-action list available on request (per 30's closing-question preparation) | Brief form: "bind coverage, set a price, adjust a reserve, or move money" as the four most illustrative of the ten regulated actions | AI Product Owner | Decided |

## Alternatives and trade-offs

| Option | Benefits | Risks | Cost/complexity | Reversibility | Decision and rationale |
|---|---|---|---|---|---|
| Write an aspirational pitch describing the system as if it were already delivering the board's 20%/12% targets, to create a more compelling narrative | Sounds more impressive and business-focused | Directly contradicts 01's own ADR-01 (no improvement claimed without a measured baseline) and 28's "not production-ready" verdict; an informed panel would catch this immediately, since they have read the same 30 artefacts | Lower rhetorical effort, near-certain credibility damage if challenged | N/A — cannot be un-said once delivered in a live pitch | Rejected outright. Violates CTRL-EP-01 and CTRL-EP-03 directly. |
| Omit the stop condition to keep the pitch purely positive and benefit-focused | Marginally shorter, more upbeat-sounding | Contradicts requirements/FINAL_DEFENCE.md's explicit request for "stop conditions" as part of segment 7; omitting it would fail to answer a question the panel is specifically listening for | Lower content to prepare, guaranteed gap against the defence brief's own requirement | Reversible before the session | Rejected. CTRL-EP-02 requires the stop condition in both pitches. |
| Two pitches (60s/20s) as a strict subset of each other, condensing the actual submission state (problem, bounded-workflow approach, honest not-yet-implemented status, and the no-AI-comparator stop condition), with a brief four-action illustrative summary of the ten-action prohibition | Consistent with everything already established in 01/04/14/28; defensible if challenged since it matches, rather than exceeds, the submitted evidence | Less immediately impressive-sounding than an aspirational pitch, an intentional trade-off for honesty | Low — two short text artefacts, no new analysis beyond condensation | Reversible; wording can be refined before the actual session | Selected. The only option consistent with CTRL-EP-01 through CTRL-EP-04. |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-EP-01 | Neither pitch claims production-readiness or live benefit | Read both pitch texts against 28_PRODUCTION_READINESS.md's verdict | No sentence in either pitch implies the system is live, running, or currently reducing cost/cycle-time | This artefact, Required analysis and decisions table | AI Product Owner |
| CTRL-EP-02 | Both pitches name the stop condition | Review of both pitch texts for the stop-condition sentence | Both texts include the no-AI-comparator stop condition | This artefact, Required analysis and decisions table | AI Product Owner |
| CTRL-EP-03 | Neither pitch states a specific improvement percentage | Text scan of both pitches for numeric benefit claims | No percentage figure appears in either pitch | This artefact, Required analysis and decisions table | AI Product Owner |
| CTRL-EP-04 | Both pitches state, in brief, what the system cannot do | Review of both pitch texts for the prohibited-action summary | Both texts include at least the four-action illustrative summary | This artefact, Required analysis and decisions table | AI Product Owner |

## Traceability

| Inject/requirement | Architecture/ADR | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| requirements/FINAL_DEFENCE.md segment 7 (handover and pitch) | Cross-referenced to 26 (operating model), 29 (roadmap), 30 (defence prep) | N/A — pitch text, not a technical component | N/A | The pitch's persuasiveness depends on delivery, which cannot be evaluated by this artefact itself. |
| INJ-001, INJ-002 (board target, no-AI challenge) | Cross-referenced to 01/02's ADR-01 | N/A | N/A | The stop condition's credibility depends on the no-AI comparator actually being executed eventually, which remains an open item per 02's own status. |
| Non-compensable gate 1 (14_INSURANCE_CONTROL_BOUNDARIES.md) | Cross-referenced | N/A | N/A | The brief four-action summary is illustrative, not exhaustive; the full ten-action list must be available if the panel asks for it (per 30's closing-question preparation). |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| The pitch text has not been rehearsed for actual timing (60 seconds and 20 seconds are targets, not yet verified by a timed read-through) | Medium | Time both pitches aloud before the actual defence session and trim if over target | AI Product Owner | Open | Before the defence session |
| The stop condition depends on the no-AI comparator pilot actually being executed, which remains an open item since 02_DMAIC_WORKBOOK.md | High (inherited, not new) | This is the same residual risk already logged in 01/02; the pitch surfaces it rather than concealing it | AI Product Owner | Open — inherited | Before Business Case final sign-off (per 01's own trigger) |
| This pitch has not been reviewed by Group CEO for tone/messaging appropriateness before use in an actual defence | Medium | Escalate for review before the session | Group CEO | Open | Before the defence session |