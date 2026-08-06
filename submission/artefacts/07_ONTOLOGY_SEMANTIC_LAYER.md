# 07 Ontology Semantic Layer

## Purpose

Ontology, semantic definitions, temporal policy logic and ownership for the core policy, claim, coverage, peril, event and party concepts used across Workflow A and Workflow B, resolving the terminology and temporal conflicts raised by the D02–D04 injects.

## Acceptance criteria

- The artefact is evidence-led and references supplied paths, record locators and inject IDs.
- Facts, assumptions, inference, conflict, decision and residual risk are distinguishable.
- Temporal, jurisdictional, authorization and authority boundaries are explicit where relevant.
- Owners, approvals, review triggers and measurable acceptance gates are named.
- The artefact contains no unsupported coverage, pricing, reserve, payment or treaty conclusion.

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| EVID-012 | data/policy_wording_versions.csv | domain_specific/signed_schedule_and_approved_wording | 2026-04-01 | IN | Defines Wording Version concept with explicit authority column (signed_schedule, approved_wording, marketing_summary). |
| EVID-024 | knowledge/POLICY_WORDING_AUTHORITY.md | approved/trusted_with_conditions | 2026-01-01 | global | Establishes the authority-ranking rule: signed schedule/endorsement over marketing summary. |
| EVID-020 | data/parametric_contracts.csv (record_id=INJ-012-PARAMETRIC_CONTRACTS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Parametric Trigger concept: brochure describes rainfall at farm location; contract uses named weather-station index (INJ-012). |
| — | knowledge/PARAMETRIC_TRIGGER_AUTHORITY.md | approved/trusted_with_conditions | 2026-01-01 | global | Establishes that signed index/station/observation-period/fallback methodology controls, not marketing description. |
| EVID-028 | data/loss_events.csv (loss_event_id=LOSS-NILA-01) | domain_specific/claims_and_reserves | 2026-07-28 | Asia/Kolkata | Defines Loss Event temporal facts: occurred_start/occurred_end (local), reported_timezone, normalized_start_utc/end_utc, disputed_window status (INJ-022). |
| — | data/timezone_rules.csv | mixed/as_supplied | n/a | MULTI | Referenced for jurisdictional/DST normalization rules (INJ-022). |
| EVID-027 | data/claims.csv (claim_id=CLM-10001;CLM-10002) | domain_specific/claims_and_reserves | 2026-07-29 | IN | Claim concept referencing policy_id, party_id, loss_event_id, cat_event_id — demonstrates one Loss Event linking to multiple Claims (INJ-021). |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | "Effective Time" for any evidenced concept always has three components that must be kept distinct: the local/reported timestamp, the timezone/offset context, and the normalized UTC value; none substitutes for the others. | data/loss_events.csv (occurred_start, reported_timezone, normalized_start_utc) — EVID-028; PACKAGE_SCOPE_AND_ASSUMPTIONS.md "timestamps retain their supplied offset or UTC marker; local dates must not be compared without normalization" | Comparing raw local timestamps across jurisdictions without normalization risks exactly the INJ-022 temporal-ambiguity failure. | Data Governance Owner | Before any cross-jurisdiction time comparison is coded |
| A-02 | "Authority Status" is a first-class semantic property of every document/wording/index concept (values observed: `signed_schedule`, `approved_wording`, `marketing_summary`), and marketing_summary is never used to resolve a coverage-relevant question. | data/policy_wording_versions.csv (EVID-012); knowledge/POLICY_WORDING_AUTHORITY.md (EVID-024) | Without this explicit property, a query could silently pick the marketing row, reproducing INJ-007. | Data Governance Owner | Before any wording-lookup query is coded |
| A-03 | "Parametric Trigger" is defined solely by the signed index/station/observation-period/fallback methodology; the customer-facing brochure description (e.g., "rainfall at farm location") is a separate, non-authoritative concept ("Marketing Description of Trigger") that must never be substituted for the contractual definition. | data/parametric_contracts.csv (EVID-020); knowledge/PARAMETRIC_TRIGGER_AUTHORITY.md | Confusing the two concepts reproduces INJ-012 and could misinform a customer-facing explanation. | Chief Underwriter | Before any Workflow B parametric-product output is produced |
| A-04 | "Loss Event" and "Claim" are related but distinct entities in a many-to-many relationship (one Loss Event can underlie multiple Claims on different Policies for different or the same Party); the ontology must not encode a Loss-Event-to-Claim relationship as 1:1. | data/claims.csv, data/loss_events.csv (EVID-027, EVID-028) — CLM-10001 and CLM-10002 both reference LOSS-NILA-01 | A 1:1 assumption would either drop one of the linked claims or force an incorrect merge, pre-empting the human reconciliation required by INJ-021. | Group Chief Claims Officer | Before Workflow A implementation |

## Required analysis and decisions

| Concept | Definition | Identifier | Temporal rule | Jurisdiction rule | Owner |
|---|---|---|---|---|---|
| Wording Version | A specific, dated version of policy contract text for a Product, carrying an explicit authority_status (signed_schedule / approved_wording / marketing_summary) | wording_version (e.g., HPP-2025.3) | Effective from effective_from date; multiple versions may share a product name but differ in effective_from and authority_status (INJ-007) | territory column scopes applicability (e.g., India for Home Protect Plus) | Group Policy and Control Owner |
| Endorsement | A change to a Policy Instance, carrying four distinct timestamps: requested_at, issued_at, effective_at, premium_received_at | endorsement_id (e.g., END-771) | All four timestamps are independently significant; effective_at determines coverage-relevant timing, not issued_at or requested_at (INJ-008) | Inherits jurisdiction from the parent Policy Instance | Group Policy and Control Owner |
| Loss Event | A real-world occurrence with a disputed or corroborated temporal window, normalized to UTC but preserving the original local/sensor timestamps | loss_event_id (e.g., LOSS-NILA-01) | occurred_start/occurred_end in local reported_timezone; normalized_start_utc/normalized_end_utc computed; status field (e.g., disputed_window, corroborated, open_ended) preserved rather than resolved (INJ-022) | reported_timezone captures the applicable local jurisdiction context at time of loss | Group Chief Claims Officer |
| Claim | A policyholder's assertion of loss against a specific Policy, referencing exactly one Loss Event, one Party and (optionally) one Cat Event | claim_id (e.g., CLM-10001) | reported_at is the claim-notification timestamp, distinct from the underlying Loss Event's occurred_start (INJ-022 applies transitively) | currency field scopes claimed_amount; must never be aggregated across Claims without an explicit FX/valuation methodology (per 06_DATA_GOVERNANCE_LINEAGE.md A-02) | Group Chief Claims Officer |
| Parametric Trigger | The signed index, weather station, observation period and fallback methodology that contractually determines payout eligibility, as distinct from any marketing description of the peril | Defined per parametric_contracts.csv record, cross-referenced to knowledge/PARAMETRIC_TRIGGER_AUTHORITY.md | Observation period is fixed by the signed contract, independent of any brochure-described "farm location" rainfall claim (INJ-012) | Station/index location is the contractually relevant location, which may differ materially from the insured farm location | Chief Underwriter |

## Alternatives and trade-offs

| Option | Benefits | Risks | Cost/complexity | Reversibility | Decision and rationale |
|---|---|---|---|---|---|
| Flat "policy document" concept with a single "current version" flag | Simple to query | Cannot represent three concurrent wordings with different authority levels (INJ-007); would force an arbitrary "current" pick, likely defaulting to the most recent regardless of authority_status | Low | Reversible but loses historical nuance if not redesigned early | Rejected. Directly reproduces the INJ-007 failure mode. |
| Explicit Wording Version entity with authority_status and effective_from as first-class properties, queried per use-case rather than pre-collapsed | Preserves all information needed to make a defensible, cited authority decision at query time | Slightly higher query complexity (must filter by authority_status and effective date per use) | Medium | Fully reversible; no information loss | Selected. Matches the explicit case-pack requirement to build a "temporal and jurisdictional authority model rather than a single global source-of-truth ranking." |
| Collapse Loss Event and Claim into a single entity for simplicity | Simpler schema | Cannot represent the confirmed one-to-many pattern (LOSS-NILA-01 → CLM-10001, CLM-10002); would force premature duplicate/fraud judgement | Low | Costly to reverse once claims processing depends on the collapsed model | Rejected. Violates A-04 and pre-empts a human reconciliation decision reserved by INJ-005. |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-OSL-01 | Wording-authority queries never default to marketing_summary | Unit test using EVID-012 (three HPP wordings) | Query excludes marketing_summary rows from any coverage-relevant resolution | submission/tests (deferred) | Data Governance Owner |
| CTRL-OSL-02 | Endorsement temporal facts remain individually queryable | Unit test using EVID-014/END-771 | All four timestamps are retrievable independently; no derived single "endorsement date" replaces them | submission/tests (deferred) | Data Governance Owner |
| CTRL-OSL-03 | Loss Event disputed status is preserved, not silently resolved | Unit test using EVID-028/LOSS-NILA-01 disputed_window | Output retains the disputed_window status and both timestamp sources; does not pick one as "the" answer | submission/tests (deferred) | Group Chief Claims Officer |
| CTRL-OSL-04 | Parametric Trigger resolution uses only the signed index/station definition, never the brochure description, for any payout-eligibility-relevant output | Unit test using EVID-020/parametric_contracts.csv plus marketing_materials.csv brochure text | Output cites the signed index/station; brochure text, if shown, is explicitly labelled non-authoritative | submission/tests (deferred) | Chief Underwriter |

## Traceability

| Inject/requirement | Architecture/ADR | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| INJ-007 (policy version collision) | Deferred to submission/artefacts/11_ADR_REGISTER.md | Wording Version entity (defined here; not yet implemented in code) | CTRL-OSL-01 (deferred) | Ontology must be extended to all products, not only Home Protect Plus, before general use. |
| INJ-008 (endorsement timing conflict) | Deferred | Endorsement entity (defined here; not yet implemented) | CTRL-OSL-02 (deferred) | Same as 05_DDD_CONTEXT_MAP.md residual risk — upstream system defect persists. |
| INJ-012 (parametric trigger wording conflict) | Deferred | Parametric Trigger entity (defined here; not yet implemented) | CTRL-OSL-04 (deferred) | Requires the actual signed index definition text, which was not attached beyond the evidence-envelope row; full resolution needs that document. |
| INJ-021 (duplicate catastrophe claims) | Deferred to submission/artefacts/05_DDD_CONTEXT_MAP.md | Loss Event / Claim many-to-many relationship (defined here) | Cross-referenced to CTRL-DDD-03 in 05_DDD_CONTEXT_MAP.md | Identity-resolution quality (INJ-030) still affects whether "same Party" determination is reliable. |
| INJ-022 (coverage temporal ambiguity) | Deferred | Loss Event temporal-fact model (defined here) | CTRL-OSL-03 (deferred) | Ontology preserves the dispute but does not resolve which timestamp is coverage-determinative — that remains a human/legal question. |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| Ontology defined here covers only the concepts evidenced in the D02/D04 injects examined in this pass (Wording Version, Endorsement, Loss Event, Claim, Parametric Trigger); coverage, exclusion, party, treaty and model concepts are deferred | Medium | Extend in a later pass covering templates 08 (knowledge-graph decision) and onward; explicitly not claimed complete here | Data Governance Owner | Open | Before final submission (all 32 templates required per requirements/ARTEFACT_EXPECTATIONS.md) |
| No machine-readable ontology artefact (e.g., OWL/JSON-LD schema) has been produced yet — this document is the human-readable semantic definition only | Medium | Defer machine-readable encoding to the architecture/implementation pass | AI Product Owner | Open | Before Workflow A/B implementation begins |
| Signed index/station text for the parametric trigger (INJ-012) was not attached in supplied evidence beyond the evidence-envelope row | Low | Flag as a data-completeness gap; do not assert a specific index definition beyond what knowledge/PARAMETRIC_TRIGGER_AUTHORITY.md states generically | Chief Underwriter | Open | If/when the actual signed contract text becomes available |
