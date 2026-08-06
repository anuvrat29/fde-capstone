# 05 Ddd Context Map

## Purpose

Bounded contexts, aggregates, events, anti-corruption layers and ubiquitous language for the policy, claim, underwriting and evidence-authority domains, grounded in the D02 (policy/coverage lifecycle) and D04 (claims) injects.

## Acceptance criteria

- The artefact is evidence-led and references supplied paths, record locators and inject IDs.
- Facts, assumptions, inference, conflict, decision and residual risk are distinguishable.
- Temporal, jurisdictional, authorization and authority boundaries are explicit where relevant.
- Owners, approvals, review triggers and measurable acceptance gates are named.
- The artefact contains no unsupported coverage, pricing, reserve, payment or treaty conclusion.

## Artefact-specific acceptance criteria

- Wording-version resolution never defaults to a marketing_summary authority row (CTRL-DDD-01).
- Endorsement temporal facts (requested_at, issued_at, effective_at, premium_received_at) remain independently queryable in any downstream representation, never collapsed to one date (CTRL-DDD-02).
- Claims sharing a loss_event_id are presented as a flagged reconciliation fact for human review, never auto-merged or auto-labelled as fraud (CTRL-DDD-03).

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| EVID-012 | data/policy_wording_versions.csv (wording_version=HPP-2025.3;HPP-2026.1;HPP-MKT-2026) | domain_specific/signed_schedule_and_approved_wording | 2026-04-01 | IN | Three concurrent wordings for "Home Protect Plus" with different flood-exclusion terms; marketing row is explicitly non-authoritative. |
| EVID-013 | data/policies.csv (policy_id=POL-IN-HO-1001) | domain_specific/policy_administration_issuance | 2026-01-01T00:00:00+05:30 | IN | Policy record references wording_version HPP-2025.3. |
| EVID-014 | data/endorsements.csv (endorsement_id=END-771) | domain_specific/policy_administration_issuance | 2026-07-28T00:00:00+05:30 | IN | Flood-extension endorsement with requested_at/issued_at/effective_at/premium_received_at all distinct and issued after the disputed loss window. |
| EVID-018 | data/group_policies.csv (record_id=INJ-011-GROUP_POLICIES) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Master-policy/certificate benefit mismatch (INJ-011). |
| EVID-019 | data/member_certificates.csv (record_id=INJ-011-MEMBER_CERTIFICATES) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Corroborates INJ-011. |
| EVID-027 | data/claims.csv (claim_id=CLM-10001;CLM-10002) | domain_specific/claims_and_reserves | 2026-07-29 | IN | Same loss_event_id LOSS-NILA-01 underlies two claims on different policies (household and SME) for party PTY-001 (INJ-021). |
| EVID-028 | data/loss_events.csv (loss_event_id=LOSS-NILA-01) | domain_specific/claims_and_reserves | 2026-07-28 | Asia/Kolkata | disputed_window status; sensor and operator timestamps differ by 35 minutes (INJ-022). |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | "Policy Wording" and "Policy Instance" are distinct concepts: a Policy Instance (policies.csv row) references exactly one Wording Version at a point in time, but multiple Wording Versions can share a marketing Product name. | data/policies.csv, data/policy_wording_versions.csv (EVID-012, EVID-013) | Conflating product marketing name with wording version would silently pick the wrong exclusion terms (INJ-007). | Data Governance Owner | Before Workflow A/B implementation |
| A-02 | An Endorsement is a first-class aggregate with four distinct temporal facts (requested_at, issued_at, effective_at, premium_received_at) that must never be collapsed into a single "endorsement date". | data/endorsements.csv (EVID-014) | Collapsing dates would hide exactly the INJ-008 timing conflict this package requires participants to detect. | Data Governance Owner | Before Workflow A implementation |
| A-03 | A Loss Event is distinct from a Claim: one Loss Event (e.g., LOSS-NILA-01) may be linked to multiple Claims across different policies and parties; this is not automatically fraud or duplication, but must be surfaced as a reconciliation question (INJ-021). | data/claims.csv, data/loss_events.csv (EVID-027, EVID-028) | Automatically merging or automatically treating linked claims as duplicates would pre-empt a fraud/coverage decision reserved for humans (INJ-005). | Group Chief Claims Officer | Before Workflow A implementation |
| A-04 | Group/Master Policy and Member/Employee Certificate are separate bounded-context aggregates that can assert conflicting benefit terms (INJ-011); the certificate is not automatically subordinate without checking which document is currently controlling for the relevant jurisdiction and product. | data/group_policies.csv, data/member_certificates.csv (EVID-018, EVID-019) | Assuming master-policy terms always control could incorrectly override a certificate promise that is in fact binding in some jurisdictions. | Chief Underwriter | Before Workflow B implementation |

## Required analysis and decisions

| Bounded context | Aggregate/root | Ubiquitous term | Upstream/downstream | Integration pattern | Ownership conflict |
|---|---|---|---|---|---|
| Policy Administration | Policy (policy_id) | "Policy Instance" vs "Wording Version" vs "Product" — kept as three distinct terms, not synonyms | Upstream of Claims (claims.csv.policy_id references policies.csv); downstream of Underwriting decision | Anti-corruption layer required at the Claims boundary to resolve which Wording Version was effective at loss date, not just which Policy Instance exists (INJ-007) | PolicyCore-IN is authoritative for issued schedule but not for scanned endorsements (case/SOURCE_SYSTEM_FACT_PACK.md) — ownership of "current wording" is contested between issuance system and document store |
| Policy Administration — Endorsement sub-context | Endorsement (endorsement_id) | "Requested", "Issued", "Effective" and "Premium received" are four distinct, non-interchangeable temporal terms | Upstream of Claims (coverage-at-loss-date determination) | Event-sourced representation preserving all four timestamps; no derived "endorsement date" field is exposed downstream | Same system (PolicyCore-IN) generates all four timestamps but INJ-008 shows they can arrive out of causal order relative to the loss event |
| Claims | Claim (claim_id) linked to Loss Event (loss_event_id) | "Loss Event" (a real-world occurrence) is distinct from "Claim" (a policyholder's assertion against a policy); one Loss Event may relate to many Claims | Downstream of Policy Administration and Party/Identity; upstream of Reserving/Reinsurance (out of scope for this pass) | Anti-corruption layer at the identity boundary — do not assume claimant_identities.csv party_id resolution is final without checking data quality (INJ-021, INJ-030 address collision, deferred to 06_DATA_GOVERNANCE_LINEAGE.md) | ClaimSphere has duplicate party/event IDs (case/SOURCE_SYSTEM_FACT_PACK.md); ownership of "canonical loss event" is contested between claims system and field-ops/IoT source |
| Group Benefits | Group Policy (master) vs Member Certificate | "Master Policy Schedule" (controlling legal document) vs "Certificate" (member-facing summary, may promise more than the schedule) | Group Policy is upstream of Member Certificate in issuance sequence, but Certificate is downstream-facing to the member/claimant | Anti-corruption layer required before any Workflow B recommendation cites certificate language as if it were master-policy authority | Ownership conflict per INJ-011: which document currently controls a specific promised benefit is unresolved in supplied evidence and must be escalated, not assumed |

## Alternatives and trade-offs

| Option | Benefits | Risks | Cost/complexity | Reversibility | Decision and rationale |
|---|---|---|---|---|---|
| Single unified "Policy" aggregate merging product, wording, and policy instance into one object | Simpler data model | Cannot represent INJ-007 (three wordings, one marketing name) without losing information; would force premature authority resolution | Lower initial cost, high correction cost later | Costly to reverse once built | Rejected. Collapses exactly the distinction the case pack requires participants to preserve. |
| Three distinct aggregates (Product, Wording Version, Policy Instance) with explicit effective-date and authority-status fields | Preserves INJ-007 distinction; supports the temporal/jurisdictional authority model required by PACKAGE_SCOPE_AND_ASSUMPTIONS.md | Higher modelling and query complexity | Higher | Fully reversible at the modelling stage (no data loss) | Selected. Matches the explicit "no single global source-of-truth" principle in case/SOURCE_SYSTEM_FACT_PACK.md. |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-DDD-01 | Wording-version resolution never defaults to the marketing_summary row | Unit test using EVID-012 (HPP-2025.3, HPP-2026.1, HPP-MKT-2026) | Query for "current wording" excludes marketing_summary authority rows unless explicitly requested for marketing-only purposes | submission/tests (deferred) | Data Governance Owner |
| CTRL-DDD-02 | Endorsement timestamps are never collapsed to a single date field | Schema/unit test on data/endorsements.csv fields | All four timestamps (requested_at, issued_at, effective_at, premium_received_at) are individually queryable in any downstream representation | submission/tests (deferred) | Data Governance Owner |
| CTRL-DDD-03 | Linked claims sharing a loss_event_id are surfaced as a reconciliation flag, not auto-merged or auto-flagged as fraud | Unit test using EVID-027 (CLM-10001, CLM-10002 on LOSS-NILA-01) | Output presents both claims with the shared loss_event_id as a fact, with an explicit "requires human review" flag, no automatic conclusion | submission/tests (deferred) | Group Chief Claims Officer |

## Traceability

| Inject/requirement | Architecture/ADR | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| INJ-007 (policy version collision) | Deferred to submission/artefacts/11_ADR_REGISTER.md | Wording-resolution component (not yet implemented) | CTRL-DDD-01 (deferred) | Requires reliable effective-date-to-wording-version mapping across all products, not only Home Protect Plus. |
| INJ-008 (endorsement timing conflict) | Deferred | Endorsement aggregate (not yet implemented) | CTRL-DDD-02 (deferred) | Upstream system (PolicyCore-IN) may continue to produce out-of-order timestamps; this package can only surface, not prevent, the defect. |
| INJ-011 (master-policy/certificate mismatch) | Deferred | Group Benefits anti-corruption layer (not yet implemented) | Not yet defined | Underlying schedule/certificate text was not attached to supplied evidence; resolution requires document retrieval out of this pass's scope. |
| INJ-021 (duplicate catastrophe claims) | Deferred | Claims anti-corruption layer (not yet implemented) | CTRL-DDD-03 (deferred) | Identity resolution quality (INJ-030, deferred to 06_DATA_GOVERNANCE_LINEAGE.md) directly affects whether linked claims are correctly identified. |
| INJ-022 (coverage temporal ambiguity) | Deferred to submission/artefacts/07_ONTOLOGY_SEMANTIC_LAYER.md | Temporal-fact preservation (partially modelled via A-02) | Not yet defined | Disputed 35-minute window (EVID-028) may be immaterial or material depending on coverage trigger definition, which is out of scope to resolve here. |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| No ownership authority has been assigned for resolving "current wording" when PolicyCore-IN and DocVault disagree (case/SOURCE_SYSTEM_FACT_PACK.md) | High | Escalate to Chief Underwriter / Group Policy Owner for a governance decision; this artefact only models the distinction, it does not resolve it | Chief Underwriter | Open | Before Workflow A/B go-live |
| Group Policy vs Member Certificate authority conflict (INJ-011) has no resolution rule in supplied evidence | Medium | Flag every Workflow B output touching group/certificate benefits with an explicit "authority unresolved" marker until a rule is supplied | Chief Underwriter | Open | Before any Workflow B group-benefits output is produced |
| Linked-claim reconciliation (INJ-021) depends on identity-resolution quality not yet assessed in this pass | Medium | Defer detailed identity-quality assessment to submission/artefacts/06_DATA_GOVERNANCE_LINEAGE.md | Data Governance Owner | Open | Before Workflow A fraud-adjacent features are designed |
