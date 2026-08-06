# 26 Target Operating Model

## Purpose

Product, claims, underwriting, actuarial, data, security, compliance and support ownership for the three workflows post-pilot, directly resolving the confirmed accountability conflict (INJ-088) between global AI owners seeking standard automation and local claims officers/actuaries/compliance leaders retaining legal accountability.

## Acceptance criteria

- The artefact is evidence-led and references supplied paths, record locators and inject IDs.
- Facts, assumptions, inference, conflict, decision and residual risk are distinguishable.
- Temporal, jurisdictional, authorization and authority boundaries are explicit where relevant.
- Owners, approvals, review triggers and measurable acceptance gates are named.
- The artefact contains no unsupported coverage, pricing, reserve, payment or treaty conclusion.

## Artefact-specific acceptance criteria

- The global-vs-local accountability conflict (INJ-088) is resolved with an explicit rule — local legal accountability always retains final authority over global standardisation — not left as an open tension (CTRL-TOM-01).
- Every operating-model role reuses an existing role from case/STAKEHOLDER_PACK.md or a prior artefact (consistent with 20_ISO42001_GOVERNANCE.md's CTRL-IG-02 discipline); no new role is invented (CTRL-TOM-02).
- Every workflow has a named operational owner distinct from its AI Product Owner design-accountability role, so "who built it" and "who runs it" are never conflated (CTRL-TOM-03).
- The Retirement lifecycle-stage gap identified in 20_ISO42001_GOVERNANCE.md is not closed here (that belongs to template 27) but is explicitly cross-referenced, not silently dropped (CTRL-TOM-04).

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| EVID-118 | data/stakeholders.csv (record_id=INJ-088-STAKEHOLDERS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Accountability conflict: global AI owners seek standard automation while local claims officers/actuaries/compliance leaders retain legal accountability (INJ-088). |
| EVID-009 | data/decision_rights.csv (record_id=INJ-088-DECISION_RIGHTS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Reused (same hash as EVID-009 from 03_STAKEHOLDER_DECISION_RIGHTS.md); this file's row also corroborates INJ-088 in addition to its original INJ-005 use. |
| EVID-046 | case/STAKEHOLDER_PACK.md | approved/case-pack | 2026-08-01 | MULTI | Reused from 03/20; source of the twelve named stakeholder roles this artefact's operating model must reuse, per CTRL-TOM-02. |
| EVID-119 | data/continuity_requirements.csv (capability=catastrophe_claim_intake;statutory_reporting;reinsurance_notice) | domain_specific/business_continuity | 2026-08-06 | MULTI | Reused from 25; the three named capabilities directly inform which operational owner is accountable for each capability's minimum-staff/RTO requirement. |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | The INJ-088 accountability conflict is resolved by an explicit precedence rule: local legal accountability (Group Chief Claims Officer, Chief Actuary, Legal/Compliance leads per jurisdiction) always retains final sign-off authority over any global AI Product Owner's standardisation proposal; global standardisation may be proposed but never imposed against local legal accountability's objection. | data/stakeholders.csv (EVID-118); data/decision_rights.csv (EVID-009, reused); consistent with case/STAKEHOLDER_PACK.md's existing decision-authority assignments | Reversing this precedence (global overrides local) would place standardisation ahead of the legal accountability the local roles actually bear, creating exactly the exposure INJ-088 warns against. | Group CEO | Ongoing — this is a standing governance rule, not a one-time decision |
| A-02 | Every role in this operating model is drawn from case/STAKEHOLDER_PACK.md's twelve named stakeholders or a role already used consistently across artefacts 01–25 (e.g., AI Product Owner, Model Risk Owner, CISO, Data Governance Owner); this artefact assigns operational (run-time) accountability to these existing roles rather than inventing new operating-model-specific titles. | case/STAKEHOLDER_PACK.md (EVID-046); consistent role usage across 01–25 | Inventing new titles would fragment the accountability map already built in 20_ISO42001_GOVERNANCE.md's nine-role structure. | AI Product Owner | Ongoing |
| A-03 | "Design accountability" (who specified a workflow's behaviour, e.g., AI Product Owner) and "operational accountability" (who is responsible for that workflow's day-to-day running once live, e.g., Group Chief Claims Officer for Workflow A) are distinct roles, even where the same individual might hold both in practice; this artefact names them separately to prevent the AI Product Owner from being treated as the ongoing operational owner by default. | Consistent with the separation-of-duties principle implicit in case/STAKEHOLDER_PACK.md's distinct stakeholder roles | Conflating design and operational accountability would concentrate too much authority in one role and blur who is accountable when something goes wrong in live operation versus at design time. | Group CEO | Before any workflow moves from pilot to live operation |
| A-04 | The Retirement lifecycle-stage gap first identified in 20_ISO42001_GOVERNANCE.md remains open after this artefact; this artefact assigns an operational owner for the target operating model as a whole but does not itself specify retirement procedures, which belong to template 27. | submission/artefacts/20_ISO42001_GOVERNANCE.md (Open issues table) | Silently dropping the cross-reference would leave the Retirement gap's ownership unclear even after two more templates have been drafted since it was identified. | AI Product Owner | Immediately after template 27 is drafted |

## Required analysis and decisions

| Decision/question | Evidence | Analysis | Decision/output | Owner | Status |
|---|---|---|---|---|---|
| How should the INJ-088 global-vs-local accountability conflict be resolved in the target operating model? | data/stakeholders.csv (EVID-118); data/decision_rights.csv (EVID-009) | Per A-01, local legal accountability retains final sign-off; the operating model formalises this as: any global AI Product Owner standardisation proposal requires sign-off from every affected jurisdiction's Group Chief Claims Officer/Chief Actuary/Legal-Compliance lead before rollout, with no override mechanism for the global role | Explicit precedence rule recorded: local accountability > global standardisation, always, with no exception clause | Group CEO | Decided |
| Who operationally owns each of the three workflows once live (distinct from who designed them)? | case/STAKEHOLDER_PACK.md (EVID-046); consistent with 04_PRODUCT_SERVICE_BLUEPRINT.md's persona assignments | Workflow A (coverage/claim/fraud evidence reconciliation): Group Chief Claims Officer, per its existing human-approval-gate role (03/04/14). Workflow B (underwriting/pricing decision support): US Chief Underwriter, per its existing persona assignment (04). Workflow C (catastrophe/liquidity/reinsurance planning): Reinsurance Director, per its existing persona assignment (04/12/14) | Three operational owners named, each already accountable for their workflow's human-approval gate since template 03/04 — no new accountability invented, only formalised as the ongoing operational role | Group CEO | Decided |
| Who owns the cross-workflow shared components (current-authorization gate, model-artefact verification gate, fraud-ring graph component)? | 10_C4_ARCHITECTURE.md Component view (reused) | These are shared, not workflow-specific; per 10/20's existing role assignments, CISO owns the two verification gates operationally, and the fraud-ring graph component is jointly owned by Group Chief Claims Officer (as the primary consumer, per 08's Workflow A/C scoping) and AI Product Owner (as the architectural owner) | Shared-component ownership formalised as CISO (gates) and joint Group Chief Claims Officer/AI Product Owner (graph component) | Group CEO | Decided |
| How does the Retirement lifecycle-stage gap (20_ISO42001_GOVERNANCE.md) relate to this operating model? | submission/artefacts/20_ISO42001_GOVERNANCE.md (Open issues table) | Per A-04, this artefact names the AI Product Owner as accountable for ensuring the gap is closed, but the actual retirement procedures are deferred to template 27 | Cross-reference recorded; gap ownership assigned, closure deferred | AI Product Owner | Decided — deferred to template 27 |

## Alternatives and trade-offs

| Option | Benefits | Risks | Cost/complexity | Reversibility | Decision and rationale |
|---|---|---|---|---|---|
| Resolve INJ-088 by giving global AI Product Owner override authority over local objections, to enable faster standard rollout | Faster, more consistent global standardisation | Directly places global efficiency ahead of the legal accountability local roles actually bear; contradicts the case pack's own framing of the conflict (local roles "retain legal accountability") | Lower coordination cost, unacceptable governance risk | Reversible but any standardisation rolled out under this rule before reversal remains a live exposure | Rejected outright. A-01 requires local accountability to retain final authority; this option inverts that. |
| Leave INJ-088 as an acknowledged but unresolved tension, to be arbitrated case-by-case without a standing rule | Avoids committing to a potentially unpopular precedence rule now | Provides no actual operating-model clarity; every future disagreement would need fresh arbitration, reproducing the same conflict repeatedly without ever resolving the underlying accountability question | Lower upfront decision cost, high ongoing friction cost | Reversible but wastes the opportunity to resolve a named inject definitively | Rejected. This artefact's purpose is explicitly to assign ownership; leaving the central accountability conflict unresolved would fail that purpose. |
| Explicit standing precedence rule (local legal accountability > global standardisation, always), three named workflow operational owners reusing existing persona assignments, and shared-component ownership formalised per existing architectural roles | Directly resolves INJ-088 with a clear, defensible rule; reuses every role already established rather than inventing new titles; makes "who runs this once live" explicit and distinct from "who designed this" | The precedence rule may slow global standardisation initiatives that lack local sign-off, which is an intended trade-off, not an oversight | Medium — one precedence rule plus three operational-owner assignments plus shared-component ownership | Reversible only by a Group CEO/Board-level decision to change the precedence rule itself | Selected. Directly resolves the named inject with a defensible, evidence-grounded rule and satisfies all four artefact-specific acceptance criteria. |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-TOM-01 | INJ-088 is resolved with an explicit precedence rule | Review of the Required analysis and decisions table for a stated rule | Rule text explicitly states local accountability prevails, with no override clause | This artefact, Required analysis and decisions table | Group CEO |
| CTRL-TOM-02 | Every role reuses an existing stakeholder/artefact role | Cross-check role names against case/STAKEHOLDER_PACK.md and artefacts 01–25 | No role name in this artefact is absent from that combined role set | This artefact, Required analysis and decisions table | AI Product Owner |
| CTRL-TOM-03 | Design and operational accountability are named separately per workflow | Review of the workflow-ownership row for both an AI Product Owner (design) and a distinct operational owner | All three workflows show two distinct roles, never the same role for both | This artefact, Required analysis and decisions table | Group CEO |
| CTRL-TOM-04 | The Retirement gap is cross-referenced, not dropped | Review of this artefact against 20_ISO42001_GOVERNANCE.md's Open issues | This artefact explicitly names the gap and assigns interim accountability pending template 27 | This artefact, Working assumptions table (A-04) | AI Product Owner |

## Traceability

| Inject/requirement | Architecture/ADR | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| INJ-088 (accountability conflict) | New: standing precedence rule (this artefact) | Sign-off workflow for global standardisation proposals (not yet implemented) | Not yet defined | The precedence rule is a governance decision, not a technical control; enforcement depends on organisational discipline, not code alone. |
| Retirement lifecycle-stage gap (20_ISO42001_GOVERNANCE.md) | Cross-referenced, deferred to submission/artefacts/27_VENDOR_EXIT_RETIREMENT.md | Not yet implemented | Not yet defined | This artefact only assigns interim accountability; actual closure is template 27's responsibility. |
| Workflow operational ownership (A/B/C) | Reused from 04_PRODUCT_SERVICE_BLUEPRINT.md's persona assignments | Operational runbooks per workflow (not yet drafted) | Not yet defined | Naming an operational owner does not itself produce the runbooks that owner would need; that is future work beyond this artefact's scope. |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| The standing precedence rule (CTRL-TOM-01) has not yet been formally approved by the Group CEO/Board; this artefact records the proposed rule, not a ratified one | High | Escalate to Group CEO/Board for formal ratification | Group CEO | Open | Before any global standardisation proposal is submitted under this rule |
| No operational runbooks exist yet for any of the three workflows' named operational owners | Medium | Track alongside the "no implementation code" gap already logged in ARTEFACT_STATE_LOG.md; runbooks depend on an implemented workflow to document | AI Product Owner | Open | Before templates 28–29 (production readiness, 90-day roadmap) |
| The Retirement lifecycle-stage gap remains open; this artefact only reassigns interim accountability, it does not close the gap | High | Close in template 27, per A-04's explicit deferral | AI Product Owner | Open | Immediately — template 27 is next |
| This artefact does not address D09 injects INJ-059/060/062 (bancassurance mis-selling, broker remuneration, complaint clock) which may have their own operating-model ownership implications | Medium | Extend if templates 28–29 surface these as in-scope | AI Product Owner | Open | Before final submission |