# Phase 1 Evidence — 01 Project Charter

## Purpose

Defines the business problem, the three mandatory advisory workflows, intended users, affected people, explicit non-goals and prohibited actions for the AEGIS-INSURE AI Forward Deployed Engineering intervention at Aurelia Mutual & Re Group (AMR). This charter is the Phase 1 ("Qualify and baseline") exit evidence required by `WORKSHOP_DEPLOYMENT_PLAN.md` Hours 1–5 and is a prerequisite for `02_stakeholder_and_decision_rights.md`.

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| CHTR-EVID-01 | case/INTEGRATED_CASE.md §1–3 (Organisation, converging crisis, participant mandate) | approved/case-pack | 2026-08-01 | MULTI | Establishes AMR's scale, the compound Cyclone Nila crisis and the mandate to improve evidence reconciliation without assuming regulated accountability. |
| CHTR-EVID-02 | case/INTEGRATED_CASE.md §4 (Mandatory workflows) | approved/case-pack | 2026-08-01 | MULTI | Defines the three mandatory workflows and their explicit "must never" boundaries — primary source for the non-goals section below. |
| CHTR-EVID-03 | case/INTEGRATED_CASE.md §5 (Required operating properties) | approved/case-pack | 2026-08-01 | MULTI | Purpose limitation, least privilege, current authorization, abstention, human review and AI-disabled continuity are required properties of every workflow. |
| CHTR-EVID-04 | case/STAKEHOLDER_PACK.md (stakeholder table and interview extracts) | approved/case-pack | 2026-08-01 | MULTI | Twelve named stakeholders and their objectives/tensions/decision authority; used to derive intended users and affected people. |
| CHTR-EVID-05 | data/decision_rights.csv, record_id=INJ-005-DECISION_RIGHTS | mixed/as_supplied, status=challenge_fact | 2026-08-01T06:00:00Z | MULTI | Board-level prohibition on autonomous binding, declinature, pricing, reserve changes, settlement, payment, policy cancellation, claim repudiation or treaty placement. Authoritative source for prohibited actions. |
| CHTR-EVID-06 | data/decision_rights.csv, record_id=INJ-088-DECISION_RIGHTS | mixed/as_supplied, status=challenge_fact | 2026-08-01T06:00:00Z | MULTI | Accountability conflict: global AI owners seek standard automation while local claims officers, actuaries and compliance leaders retain legal accountability. Basis for the "who decides" boundary. |
| CHTR-EVID-07 | data/ai_use_boundaries.csv, record_id=INJ-005-AI_USE_BOUNDARIES | mixed/as_supplied, status=challenge_fact | 2026-08-01T06:00:00Z | MULTI | Corroborates CHTR-EVID-05; same prohibited-action list from a second source system. |
| CHTR-EVID-08 | README.md "Challenge boundary" | approved/case-pack | 2026-08-01 | MULTI | Confirms no coverage, binding, pricing, reserve, settlement or payment decision is contained in or authorized by this package. |
| CHTR-EVID-09 | DEFINITION_OF_DONE.md "Product and business" | approved/case-pack | 2026-08-01 | MULTI | Requires intended purpose, users, affected persons, prohibited actions and decision rights to be explicit. |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | The prohibited-action list in INJ-005 (CHTR-EVID-05, CHTR-EVID-07) is a board-level, non-negotiable constraint that binds all three workflows, not a design preference that can be traded off against speed or cost. | data/decision_rights.csv (INJ-005-DECISION_RIGHTS); data/ai_use_boundaries.csv (INJ-005-AI_USE_BOUNDARIES); requirements/SCORING_MODEL.md non-compensable gates | If treated as negotiable, any design proposing autonomous binding/pricing/reserve/settlement/payment/cancellation/repudiation/treaty action fails a non-compensable gate regardless of aggregate score. | AI Product Owner | Before any architecture design freeze |
| A-02 | Job title alone does not establish legal or delegated authority; authority must be evidenced by a current, jurisdiction- and product-specific entitlement or delegation record, not inferred from role name. | case/STAKEHOLDER_PACK.md decision-authority column; INJ-009 (binder authority ambiguity) and INJ-020 (underwriter override opacity) show title-based inference already fails in practice | Inferring authority from title would misauthorize edge cases such as an MGA binding above delegated limits during an outage (INJ-009) | AI Product Owner, CISO | Ongoing — re-validate at each workflow release |
| A-03 | INJ-088's accountability conflict (global AI owners vs. local claims officers/actuaries/compliance leaders) is resolved in favour of local legal accountability: local qualified officers retain the decision, and any global standardisation is limited to advisory tooling, not decision authority. | data/decision_rights.csv (INJ-088-DECISION_RIGHTS); case/STAKEHOLDER_PACK.md (Group Chief Claims Officer, Chief Actuary rows) | If global AI owners were given decision authority, local officers would be exposed to accountability without control, contradicting case/STAKEHOLDER_PACK.md interview extracts. | Group Chief Claims Officer, Chief Actuary | Before Phase 3 product specification freeze |
| A-04 | This charter and its decision-rights companion artefact are advisory scaffolding for design and review; they are not themselves a runtime authorization mechanism. Runtime enforcement must be implemented in `submission/src` and evidenced in `submission/artefacts/04_PRODUCT_SERVICE_BLUEPRINT.md` and later security/architecture artefacts. | runbooks/PARTICIPANT_RUNBOOK.md §4–5 | A static charter mistaken for a runtime control would leave prohibited actions technically possible even though documented as forbidden. | AI Product Owner | Before any implementation PR is merged |

## Business problem

Cyclone Nila has produced a compound catastrophe (wind, storm-surge, river-flood, motor, health, business-interruption and parametric claims) that coincides with a ransomware containment event, a model-package integrity failure, a telematics firmware change, allegations of discriminatory pricing, a bancassurance mis-selling review, a reinsurance event-definition dispute and a 72-hour multi-regulator evidence request (case/INTEGRATED_CASE.md §2). AMR's operational facts — policy, party, claim, coverage, peril, location, repairer, provider, broker, treaty and currency identifiers — do not reconcile reliably across its estate of policy-administration platforms, claims systems, pricing engines, actuarial workbenches, document stores, telematics platforms, catastrophe tools, reinsurance systems, data lakes and vendor portals (case/INTEGRATED_CASE.md §1, §2).

The business problem is therefore: **AMR's human decision-makers (claims handlers, underwriters, catastrophe/reinsurance leads) cannot reliably assemble authoritative, current, jurisdiction-correct evidence fast enough to support their own decisions during a converging crisis, and no existing system distinguishes fact from inference, flags conflicts, or enforces who is currently authorized to decide.** The mandate (case/INTEGRATED_CASE.md §3) is to design and demonstrate a defensible AI Forward Deployed Engineering intervention that improves evidence reconciliation and operational decision support **without assuming regulated accountability**, and to prove — not assume — that an AI component is justified against process redesign, rules, analytics and master-data repair (case/INTEGRATED_CASE.md §8; INJ-002).

## The three mandatory advisory workflows

All three workflows are strictly advisory: they prepare evidence and bounded options for a named, currently-authorized human decision-maker. None may execute, bind, or otherwise finalize a regulated outcome (case/INTEGRATED_CASE.md §4).

### Workflow A — Coverage, claim and fraud evidence reconciliation
Reconciles policy version, endorsement timing, insured interest, loss event, peril, cause, coverage, exclusion, deductible, claimant identity, repair/provider evidence, fraud indicators, legal hold and provenance. May expose contradictions, missing evidence and candidate next actions.

### Workflow B — Underwriting, pricing and customer-outcome evidence support
Reconciles application facts, external data rights, rating factors, actuarial model version, underwriting rules, protected-proxy risk, overrides, renewal treatment, consent and explanation evidence. May provide bounded recommendations and alternatives.

### Workflow C — Bounded catastrophe, liquidity and reinsurance recovery planner
Generates traceable response options using catastrophe events, exposure accumulation, claim severity, emergency hardship, operational capacity, reserve uncertainty, reinsurance terms, hours clauses, currencies, collateral, sanctions, vendor availability and customer vulnerability.

Every workflow must demonstrate purpose limitation, least privilege, current authorization, temporal and jurisdictional applicability, source authority, provenance, structured outputs, abstention, human review, contestability, idempotency, bounded steps, token/cost budgets, checkpointing, rollback, kill switch, degraded mode, auditability and AI-disabled continuity (case/INTEGRATED_CASE.md §5; CHTR-EVID-03).

## Intended users

| Workflow | Intended user(s) | Basis |
|---|---|---|
| A | Claims handlers and adjusters with a current claim assignment; Special Investigations staff for fraud referral (not disposition) | case/STAKEHOLDER_PACK.md (Group Chief Claims Officer, Head of Special Investigations rows); case/INTEGRATED_CASE.md §4 |
| B | Underwriters with current authority for the relevant product/state/jurisdiction; actuarial staff for model-version and assumption checks | case/STAKEHOLDER_PACK.md (US Chief Underwriter, Chief Actuary rows) |
| C | Catastrophe response and reinsurance leads with current operational-capacity and treaty-notice responsibility | case/STAKEHOLDER_PACK.md (Reinsurance Director row); case/INTEGRATED_CASE.md §4 |

Product, security, privacy and compliance roles (AI Product Owner, CISO, EU DPO, Customer Advocate) are indirect users who configure, review, escalate or challenge workflow outputs but do not request evidence reconciliation for their own case decisions under this charter.

## Affected people

- **Policyholders, claimants and beneficiaries** whose claims, coverage or pricing evidence is being reconciled (parties named in `data/claimant_identities.csv`, `data/parties.csv`).
- **Vulnerable and hardship customers**, explicitly including bereaved or disabled claimants who must not be routed through generic automation without escalation (case/STAKEHOLDER_PACK.md Customer Advocate row; `data/customer_vulnerability.csv`; INJ-063).
- **Brokers, MGAs and third-party adjusters** whose delegated-authority or access status affects what evidence they may submit or act on (INJ-009; `data/delegated_authorities.csv`; `data/access_cache.csv`).
- **AMR staff** (claims handlers, underwriters, catastrophe/reinsurance leads) whose professional judgement and legal accountability must not be displaced by workflow output (INJ-088).
- **Sanctioned or sanctions-adjacent individuals** whose name-matching evidence must not silently produce a screening decision (INJ-047).

## Explicit non-goals

- The workflows are **not** a coverage determination, binding, declinature, pricing, renewal, cancellation, reserve, settlement, payment, treaty-placement or litigation system (case/INTEGRATED_CASE.md §4; README.md "Challenge boundary").
- The workflows are **not** a replacement for actuarial opinion, reserving governance, underwriting authority, claims independence or legal/compliance sign-off (case/STAKEHOLDER_PACK.md; DEFINITION_OF_DONE.md).
- The package does **not** contain or produce a reference coverage decision, binding decision, final price, reserve, settlement, payment instruction, treaty recovery conclusion or completed elevator pitch (README.md "Challenge boundary").
- A knowledge graph, autonomous agent or additional AI component is **not** assumed to be justified; each must be proven against a no-AI alternative before adoption (INJ-002, INJ-070; case/INTEGRATED_CASE.md §8).
- The workflows do **not** collapse legal, coverage, actuarial or customer-outcome uncertainty into a single model confidence score (START_HERE.md "Rules of engagement").

## Prohibited actions

The following actions are prohibited for all three workflows, sourced verbatim from the board-level inject and cross-referenced to the workflow-specific "must never" boundaries in case/INTEGRATED_CASE.md §4:

| Prohibited action (INJ-005 / INJ-005-DECISION_RIGHTS, INJ-005-AI_USE_BOUNDARIES) | Workflow(s) where this is restated explicitly in case/INTEGRATED_CASE.md §4 |
|---|---|
| Autonomous binding (of coverage or a policy) | A ("must never bind coverage"), B ("must never bind... a policy") |
| Declinature (declining a policy) | B ("must never... decline... a policy") |
| Pricing (setting or changing a price) | B ("must never... price... a policy") |
| Reserve changes | A ("must never... reserve... a claim"), C ("must never... change a reserve") |
| Settlement | A ("must never... settle... a claim") |
| Payment | A ("must never... pay... a claim"), C ("must never create a payment") |
| Policy cancellation | B ("must never... cancel... a policy") |
| Claim repudiation | A ("must never... repudiate... a claim") |
| Treaty placement | C ("must never aggregate a treaty event, submit a recovery... without authorized human approval") — treaty placement/aggregation and recovery submission are treated as the Workflow C analogue of treaty placement |

Additional workflow-specific prohibited actions not present in the INJ-005 board list but explicit in case/INTEGRATED_CASE.md §4 and retained here for completeness:

- Workflow A must never litigate a claim.
- Workflow B must never renew or modify a policy.
- Workflow C must never allocate capital or instruct a vendor without authorized human approval.

No prohibited action may be inferred as permitted from a job title; see Working assumption A-02.

## Traceability

| Inject/requirement | Evidence | Charter section | Residual risk |
|---|---|---|---|
| INJ-001, INJ-002, INJ-003, INJ-004, INJ-006 | case/INTEGRATED_CASE.md §7 D01 | Business problem (context only; full business-case quantification is out of scope for this charter — see submission/artefacts/01_BUSINESS_CASE.md) | Charter does not re-quantify board targets or cost model; readers must consult 01_BUSINESS_CASE.md for that evidence. |
| INJ-005 | data/decision_rights.csv (INJ-005-DECISION_RIGHTS); data/ai_use_boundaries.csv (INJ-005-AI_USE_BOUNDARIES) | Prohibited actions | Prohibition is documented here; runtime enforcement is deferred to submission/src and must be independently tested (see 02_stakeholder_and_decision_rights.md and later architecture/security artefacts). |
| INJ-088 | data/decision_rights.csv (INJ-088-DECISION_RIGHTS) | Intended users; Working assumption A-03 | Global-vs-local accountability tension is resolved by charter decision, not by technical enforcement; escalation mechanics are detailed in 02_stakeholder_and_decision_rights.md. |
| INJ-009, INJ-020 | data/binder_events.csv; data/delegated_authorities.csv; data/underwriting_decisions.csv; data/override_events.csv | Working assumption A-02 | Authority-inference-from-title risk is named but detection/enforcement logic is not implemented in this charter. |
| INJ-063 | data/customer_vulnerability.csv; data/contact_history.csv | Affected people | Vulnerable-customer routing rule is named as a requirement, not yet implemented or tested. |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| This charter documents prohibited actions but does not itself enforce them in code | High | Enforcement is deferred to submission/src output-schema and human-approval gates; tracked as CTRL-SDR-01/02 in 02_stakeholder_and_decision_rights.md | AI Product Owner | Open — pending implementation | Before any implementation PR is merged |
| INJ-088 accountability resolution (A-03) may be contested by global AI owners seeking standard automation | Medium | Escalate through Customer/Product governance if challenged; do not silently revise the resolution without Board/CEO sign-off | Group CEO | Open | If global AI ownership mandate conflicts with local accountability in practice |
| Intended-user list derives only from case/STAKEHOLDER_PACK.md's twelve named stakeholders; no supplementary org chart was supplied | Medium | Treat as the current, complete set until a supplementary source is provided | Group CEO | Open | Before workflow go-live |

## Sign-off

| Role | Reviewer | Status |
|---|---|---|
| Reviewer | R5 | Pending review |
| Gate | G1 — no unresolved Critical/High finding | Pending |
