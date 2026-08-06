# 20 Iso42001 Governance

## Purpose

AI management system roles, lifecycle controls, evidence and review design aligned to ISO/IEC 42001:2023's non-normative structure, consolidating the governance roles and control-review triggers already established across artefacts 01–19 into one AI-management-system view.

## Acceptance criteria

- The artefact is evidence-led and references supplied paths, record locators and inject IDs.
- Facts, assumptions, inference, conflict, decision and residual risk are distinguishable.
- Temporal, jurisdictional, authorization and authority boundaries are explicit where relevant.
- Owners, approvals, review triggers and measurable acceptance gates are named.
- The artefact contains no unsupported coverage, pricing, reserve, payment or treaty conclusion.

## Artefact-specific acceptance criteria

- This artefact makes no claim of ISO/IEC 42001 conformity or certification readiness, consistent with sources/09_ISO_IEC_42001.md's explicit "non-normative alignment guide...requires a licensed copy and qualified interpretation" caveat (CTRL-IG-01).
- Every AI-management-system role named (Model Risk Owner, AI Product Owner, CISO, Data Governance Owner, etc.) is mapped to a role already used in artefacts 01–19, not invented fresh for this artefact (CTRL-IG-02).
- Every lifecycle stage (design, development, verification, deployment, monitoring, retirement) has at least one existing control cross-referenced from a prior artefact, closing gaps only where none exists (CTRL-IG-03).
- The management-review trigger cadence is explicit and tied to a concrete event or date, never "periodically" alone (CTRL-IG-04).

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| EVID-098 | sources/09_ISO_IEC_42001.md (SRC-09) | official/research_anchor | 2026-08-01 | global | ISO/IEC 42001:2023 AI management systems non-normative alignment guide; explicitly requires a licensed copy and qualified interpretation for formal conformity work — this artefact aligns to its structure without claiming conformity. |
| — | submission/artefacts/01_BUSINESS_CASE.md through 19_REGULATORY_APPLICABILITY.md | participant-authored | 2026-08-06 | — | Source of every role, control and review trigger consolidated below; no single file locator applies across nineteen files, consistent with the established multi-file evidence convention. |
| EVID-050 | DEFINITION_OF_DONE.md | approved | 2026-01-01 | global | Reused from 11_ADR_REGISTER.md; the DoD's engineering/governance requirements are the acceptance bar this AI management system view must ultimately satisfy. |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | This artefact is a non-normative alignment view only; it does not claim, and must not be read as claiming, ISO/IEC 42001 conformity or certification readiness, per sources/09_ISO_IEC_42001.md's own caveat and PACKAGE_SCOPE_AND_ASSUMPTIONS.md's "not a legal interpretation service" boundary. | sources/09_ISO_IEC_42001.md (EVID-098) | Claiming conformity without a licensed standard and qualified assessor would be exactly the kind of unsupported claim this package prohibits. | AI Product Owner, Legal | Ongoing |
| A-02 | Every governance role referenced in this artefact (Model Risk Owner, AI Product Owner, CISO, Data Governance Owner, Chief Actuary, Group Chief Claims Officer, Customer Advocate, Reinsurance Director, Group CEO) is drawn from case/STAKEHOLDER_PACK.md's twelve named stakeholders or a role already used consistently across artefacts 01–19; no new role is invented for ISO-alignment purposes alone. | case/STAKEHOLDER_PACK.md (EVID-046, reused from 03); consistent role usage across 01–19 | Inventing a new role here would fragment accountability across a role with no decision-rights history in this submission. | AI Product Owner | Ongoing |
| A-03 | Lifecycle-stage controls are reused, not duplicated, from their originating artefact; this artefact's contribution is the cross-referencing structure (which stage each control belongs to) and identifying stages with no existing control, not a new control specification. | Consistent with the reuse-not-reinvent discipline established in 09_REQUIREMENTS_TRACEABILITY.md and 11_ADR_REGISTER.md | Duplicating control specifications here would create two competing definitions of the same control, exactly the risk avoided by 09/11's discipline. | AI Product Owner | Ongoing |

## Required analysis and decisions

| Decision/question | Evidence | Analysis | Decision/output | Owner | Status |
|---|---|---|---|---|---|
| Which AI-management-system roles exist and what is each accountable for? | case/STAKEHOLDER_PACK.md (EVID-046); consistent usage across 01–19 | AI Product Owner (overall system accountability, model-selection scoping per 13); Model Risk Owner (model approval status, fairness breach remediation per 15/18); CISO (security/threat controls per 16, residency compliance per 17); Data Governance Owner (data authority/lineage per 06, privacy controls per 17); Chief Actuary (actuarial model risk per 15, reserve-authority per 14); Group Chief Claims Officer (claims-workflow human authority per 03/14); Customer Advocate (vulnerable-customer/contestability per 18); Reinsurance Director (treaty/catastrophe authority per 12/14); Group CEO (entity-segmented reporting, ultimate escalation per 01/03) | Nine-role accountability map recorded, reusing existing role assignments; no new roles introduced | AI Product Owner | Decided |
| What lifecycle-stage controls already exist, and where are the gaps? | Cross-reference of every CTRL-*/REQ-C-*/ADR-* across artefacts 01–19 | Design stage: DDD/ontology model (05/07), ADR register (11); Development stage: model-registry scoping (13), integration contracts (12); Verification stage: model-artefact verification gate (10/13), fairness-breach detection (15); Deployment stage: C4 architecture placements (10), read-only/propose-only boundary (10/14); Monitoring stage: threat/abuse detection controls (16), residency-compliance flagging (17); Retirement stage: no existing control found — this is a genuine gap, deferred to template 27 (Vendor Exit and Retirement) | Five of six lifecycle stages have at least one existing control; Retirement stage is flagged as an identified gap, not fabricated with a placeholder control | AI Product Owner | Decided — gap identified, not yet closed |
| What is the management-review cadence and trigger? | Review triggers already stated across 01–19's Open issues tables (e.g., "before UW-LIFE-4's review closes", "at each architecture review cycle") | Rather than inventing a generic "periodic review", this artefact consolidates the concrete triggers already named: model-review-cycle triggers (15/18), architecture-review-cycle triggers (08/11), and evidence-completeness triggers (06/17) | Management review is event-triggered (model review closes, architecture cycle, evidence gap closes), not calendar-only; a calendar backstop (e.g., annual) is recorded as a minimum floor, not the primary trigger | AI Product Owner | Decided |

## Alternatives and trade-offs

| Option | Benefits | Risks | Cost/complexity | Reversibility | Decision and rationale |
|---|---|---|---|---|---|
| Pursue an explicit ISO/IEC 42001 conformity claim within this submission | Could appear to strengthen the governance narrative | Requires a licensed copy of the standard and a qualified assessor, neither available within this package's declared scope (PACKAGE_SCOPE_AND_ASSUMPTIONS.md); would be an unsupported claim | High cost (licensing, assessment), and not achievable within this package regardless of cost | N/A — not achievable in this context | Rejected outright. sources/09_ISO_IEC_42001.md's own caveat prohibits this; A-01 makes the boundary explicit. |
| Invent new governance roles specifically for ISO-alignment purposes, distinct from the roles already used in artefacts 01–19 | Could map more precisely to ISO 42001's own generic role vocabulary | Fragments accountability; a newly-invented role has no decision-rights history and no clear authority in this submission's existing RACI (03_STAKEHOLDER_DECISION_RIGHTS.md) | Lower conceptual mapping effort, higher accountability fragmentation risk | Reversible but wasteful | Rejected. A-02 requires reuse of existing, already-accountable roles. |
| Fabricate a placeholder control for the Retirement lifecycle stage to avoid showing a gap | Makes the lifecycle-stage table appear complete | Misrepresents the actual state of the submission; a defence panel could easily expose a fabricated control as unsupported | Low apparent cost, high credibility risk if challenged | N/A — a fabricated control cannot be "reversed" without admitting the fabrication | Rejected outright. Consistent with every prior artefact's evidence discipline, an identified gap is recorded as a gap, not disguised as a control. |
| Nine-role accountability map, five-of-six-lifecycle-stage control cross-reference with an explicit Retirement-stage gap, and an event-triggered (not calendar-only) management-review cadence, all reusing existing artefact content per A-02/A-03 | Provides a genuine AI-management-system view without overclaiming conformity or fabricating coverage | Requires this artefact to be resynchronised if a future template (e.g., 27) closes the Retirement-stage gap | Medium — one consolidation artefact, ongoing synchronisation discipline | Reversible; the gap can be closed by cross-referencing a future artefact without contradicting this one | Selected. Matches sources/09_ISO_IEC_42001.md's non-normative alignment purpose and the reuse-not-reinvent discipline already established. |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-IG-01 | No conformity/certification claim is made | Review of this artefact's language against sources/09_ISO_IEC_42001.md's caveat | No sentence in this artefact asserts ISO/IEC 42001 conformity or certification readiness | This artefact, Purpose and Acceptance criteria sections | AI Product Owner |
| CTRL-IG-02 | Every named role maps to an existing role from case/STAKEHOLDER_PACK.md or prior artefacts | Cross-check role names against case/STAKEHOLDER_PACK.md and artefacts 01–19 | No role name in this artefact is absent from that combined role set | This artefact, Required analysis and decisions table | AI Product Owner |
| CTRL-IG-03 | Every lifecycle stage has an existing control cross-reference or an explicit gap statement | Review of the lifecycle-stage table for completeness | All six stages are addressed; any without an existing control state so explicitly (Retirement) | This artefact, Required analysis and decisions table | AI Product Owner |
| CTRL-IG-04 | Management-review triggers are concrete, not generic | Review of the Required analysis and decisions table's cadence row | No trigger reads "periodically" alone; each cites a concrete event, cycle, or date-bound floor | This artefact, Required analysis and decisions table | AI Product Owner |

## Traceability

| Inject/requirement | Architecture/ADR | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| DEFINITION_OF_DONE.md governance requirements | Cross-referenced to ADR-01 through ADR-13 (11_ADR_REGISTER.md) | AI-management-system role/lifecycle map (this artefact; no new implementation) | To be defined in submission/artefacts/22_EVALUATION_TEVV.md | This artefact is a consolidation view; it does not itself add enforcement beyond what 01–19 already specify. |
| Retirement lifecycle-stage gap | Deferred to submission/artefacts/27_VENDOR_EXIT_RETIREMENT.md | Not yet implemented | Not yet defined | No retirement-stage control exists anywhere in the submission yet; this is the first explicit identification of that gap. |
| Confirmed fairness breaches (15/18), reused here under the Verification/Monitoring lifecycle stages | ADR-01 through ADR-13 collectively support the broader governance structure | Fairness-breach detection and remediation-pathway decision (15/18) | CTRL-AMR-01, CTRL-RAF-01 (deferred) | Same residual risk as recorded in 15/18: remediation approach not yet chosen. |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| No Retirement-stage lifecycle control exists anywhere in the submission as of this artefact | High | Close in submission/artefacts/27_VENDOR_EXIT_RETIREMENT.md; this artefact only identifies the gap | AI Product Owner | Open | Before template 27 is drafted |
| This artefact does not itself add any new enforceable control; it is a consolidation/cross-reference view only | Medium (by design) | Explicitly stated in A-03; readers must consult the cross-referenced originating artefacts for actual control specifications | AI Product Owner | Open — by design | N/A |
| A formal ISO/IEC 42001 gap assessment against the actual licensed standard has not been performed | High | Escalate to Legal/an external qualified assessor if formal conformity is ever pursued beyond this package's scope | Legal, AI Product Owner | Open | If formal ISO/IEC 42001 certification is pursued in the future |