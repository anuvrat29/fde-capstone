# Phase 1 Evidence — 02 Stakeholder and Decision Rights

## Purpose

Builds the decision-rights matrix for the three mandatory AEGIS-INSURE workflows: for each workflow, who may request support, what the system may produce, what it must reject, which qualified human decides, and who handles escalation. Grounded in `case/STAKEHOLDER_PACK.md`, `data/decision_rights.csv` and `data/ai_use_boundaries.csv`. Companion to `01_project_charter.md`; does not restate the charter's business problem or non-goals.

## Procedure used to build the matrix

1. Enumerate the stakeholder rows in `case/STAKEHOLDER_PACK.md` and extract each stakeholder's stated **decision authority** column verbatim — never inferred from job title alone (per charter Working assumption A-02).
2. Map each stakeholder's decision authority to the workflow(s) it governs, using the workflow boundaries in `case/INTEGRATED_CASE.md` §4.
3. For each workflow, populate five fields from disclosed evidence only: **who may request**, **what the system may produce**, **what it must reject**, **which qualified human decides**, **who handles escalation**.
4. Cross-check the "must reject" column against the full INJ-005 prohibited-action list (`data/decision_rights.csv` record `INJ-005-DECISION_RIGHTS`; `data/ai_use_boundaries.csv` record `INJ-005-AI_USE_BOUNDARIES`) so that every prohibited action appears explicitly in at least one workflow row.
5. Record the INJ-088 accountability conflict (`data/decision_rights.csv` record `INJ-088-DECISION_RIGHTS`) as an explicit escalation path rather than resolving it silently in favour of either global or local ownership.
6. Flag any authority reference that cannot be evidenced by a current, dated, jurisdiction-specific record (rather than a title) as a residual risk, not as a decided fact.

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| DR-EVID-01 | case/STAKEHOLDER_PACK.md (full stakeholder table) | approved/case-pack | 2026-08-01 | MULTI | Primary source for all "decision authority" and "escalation" values in the matrix below; twelve stakeholders, no supplementary org chart supplied. |
| DR-EVID-02 | case/STAKEHOLDER_PACK.md "Interview extracts" | approved/case-pack | 2026-08-01 | MULTI | Corroborating qualitative evidence (e.g., "Do not collapse a coverage conflict into a confidence score"; "A read-only tool that can mutate a payee is not read-only") used to derive "must reject" entries. |
| DR-EVID-03 | data/decision_rights.csv, record_id=INJ-005-DECISION_RIGHTS | mixed/as_supplied, status=challenge_fact | 2026-08-01T06:00:00Z | MULTI | Full prohibited-action list: autonomous binding, declinature, pricing, reserve changes, settlement, payment, policy cancellation, claim repudiation, treaty placement. Authoritative source for the "must reject" column across all three workflows. |
| DR-EVID-04 | data/decision_rights.csv, record_id=INJ-088-DECISION_RIGHTS | mixed/as_supplied, status=challenge_fact | 2026-08-01T06:00:00Z | MULTI | Accountability conflict between global AI owners and local claims officers/actuaries/compliance leaders; authoritative source for the escalation-ownership rule below. |
| DR-EVID-05 | data/ai_use_boundaries.csv, record_id=INJ-005-AI_USE_BOUNDARIES | mixed/as_supplied, status=challenge_fact | 2026-08-01T06:00:00Z | MULTI | Second-source corroboration of DR-EVID-03's prohibited-action list. |
| DR-EVID-06 | data/binder_events.csv, record_id=INJ-009-BINDER_EVENTS; data/delegated_authorities.csv, record_id=INJ-009-DELEGATED_AUTHORITIES | mixed/as_supplied, status=challenge_fact | 2026-08-01T06:00:00Z | MULTI | Evidence that title-based authority inference has already failed in practice (MGA bound above delegated authority during outage); used to justify Working assumption A-02 and the "current authority" requirement in every row below. |
| DR-EVID-07 | data/underwriting_decisions.csv, record_id=INJ-020-UNDERWRITING_DECISIONS; data/override_events.csv, record_id=INJ-020-OVERRIDE_EVENTS | mixed/as_supplied, status=challenge_fact | 2026-08-01T06:00:00Z | MULTI | Underwriter override concentration by office/broker; used to justify escalation of Workflow B overrides to a named human rather than silent AI resolution. |
| DR-EVID-08 | knowledge/UNDERWRITING_HUMAN_AUTHORITY.md | approved/trusted_with_conditions | 2026-01-01 | global | Confirms AI may prepare evidence/options only; binding/declining/pricing remains a licensed/delegated human action — corroborates DR-EVID-03 for Workflow B. |
| DR-EVID-09 | requirements/SCORING_MODEL.md (non-compensable gates section) | approved | 2026-01-01 | global | Confirms that any implementation permitting a prohibited action fails a non-compensable gate regardless of aggregate score. |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | The twelve stakeholders in case/STAKEHOLDER_PACK.md are the current, complete set of decision-relevant roles for the three mandatory workflows. | case/STAKEHOLDER_PACK.md | Matrix rows below would omit roles not named there (e.g., country-specific compliance officers, per-state underwriting delegates). | Group CEO | Before workflow go-live |
| A-02 | "Decision authority" in this matrix means a role, not a named individual, and every runtime use must resolve the role to a currently-entitled individual via an authoritative, dated entitlement record — never via job title alone. | case/STAKEHOLDER_PACK.md; DR-EVID-06 (INJ-009 authority-inference failure) | If a workflow authorized any user holding a matching title without checking a current entitlement record, it would repeat the INJ-009 failure pattern. | AI Product Owner, CISO | Ongoing — re-validate per workflow release |
| A-03 | This matrix is a design-time, human-readable summary. It is not a runtime authorization source; runtime enforcement must query current entitlement data (e.g., an equivalent of `data/access_policies.csv`, `data/access_cache.csv`) and must not rely on this document at execution time. | data/access_cache.csv (INJ-079 revocation-cache-lag evidence pattern) | Using this static matrix as a runtime source would risk stale-authorization failures analogous to INJ-079 (terminated adjuster remaining authorized in gateway cache). | AI Product Owner | Before any implementation PR is merged |
| A-04 | The INJ-088 accountability conflict is resolved for this matrix by giving the named local qualified role final decision authority in every workflow; "global AI owner" / "AI Product Owner" roles are limited to product scope (tooling, prompts, evidence pipeline) and hold no decision authority over any individual case. | data/decision_rights.csv (INJ-088-DECISION_RIGHTS); case/STAKEHOLDER_PACK.md ("AI Product Owner ... Decision authority: Product scope only") | If global product ownership were treated as decision authority, local officers would carry legal accountability without control — the exact conflict INJ-088 warns against. | Group CEO, Group Chief Claims Officer | Before Phase 3 product specification freeze |

## Decision-rights matrix

### Workflow A — Coverage, claim and fraud evidence reconciliation

| Field | Content | Evidence |
|---|---|---|
| Who may request support | Claims handler or adjuster with a current claim assignment; Special Investigations staff requesting a fraud-referral evidence pack (not a fraud disposition) | case/STAKEHOLDER_PACK.md (Group Chief Claims Officer, Head of Special Investigations rows) |
| What the system may produce | Structured evidence pack separating fact, inference, conflict and missing evidence across policy version, endorsement timing, insured interest, loss event, peril, cause, coverage, exclusion, deductible, claimant identity, repair/provider evidence, fraud indicators, legal hold and provenance; candidate next actions for human review | case/INTEGRATED_CASE.md §4 Workflow A |
| What it must reject | Binding coverage; repudiating a claim; settling a claim; changing a reserve; paying a claim; cancelling a policy; litigating a claim; any output that presents a fraud referral as a fraud finding or disposition | DR-EVID-03, DR-EVID-05 (INJ-005); DR-EVID-02 ("Do not collapse a coverage conflict into a confidence score") |
| Which qualified human decides | Claims handler/adjuster holding a current, dated claim assignment for the specific policy/claim (assignment verified against an authoritative claims-assignment record, not title) | case/STAKEHOLDER_PACK.md (Group Chief Claims Officer row: "Claims operating standards"); Working assumption A-02 |
| Who handles escalation | Coverage or evidence conflicts that the assigned handler cannot resolve escalate to the Group Chief Claims Officer; fraud-ring or organised-fraud ambiguity (INJ-045) escalates to the Head of Special Investigations for referral decision only, never for claim disposition; legal-hold/deletion conflicts (INJ-026) escalate jointly to Group Chief Claims Officer and EU Data Protection Officer | case/STAKEHOLDER_PACK.md; data/legal_holds.csv; data/deletion_requests.csv |

### Workflow B — Underwriting, pricing and customer-outcome evidence support

| Field | Content | Evidence |
|---|---|---|
| Who may request support | Underwriter holding current authority for the specific product/state/jurisdiction; Chief Actuary or delegate requesting a model-version/assumption check | case/STAKEHOLDER_PACK.md (US Chief Underwriter, Chief Actuary rows) |
| What the system may produce | Structured evidence pack on application facts, external data rights, rating factors, actuarial model version, underwriting rules, protected-proxy risk, override history, renewal treatment, consent and explanation evidence; bounded recommendations and alternatives with rationale | case/INTEGRATED_CASE.md §4 Workflow B; DR-EVID-08 |
| What it must reject | Binding a policy; declining a policy; pricing a policy; renewing a policy; cancelling a policy; modifying a policy; any output that silently resolves an underwriter override without flagging it for review; any recommendation built on external data lacking documented provenance/purpose (INJ-017) | DR-EVID-03, DR-EVID-05 (INJ-005); DR-EVID-08 |
| Which qualified human decides | Underwriter with current, product- and jurisdiction-specific delegated authority (verified against an authoritative delegation record, not title alone); Chief Actuary for reserving/model-assumption matters only, not individual underwriting decisions | case/STAKEHOLDER_PACK.md (US Chief Underwriter row: "Underwriting authority by state/product"); Working assumption A-02 |
| Who handles escalation | Protected-proxy pricing risk (INJ-013) and override concentration by office/broker (INJ-020; DR-EVID-07) escalate to the Chief Underwriter for manual review — the workflow flags the pattern but takes no corrective action; customer-outcome/mis-selling conflicts (INJ-059, INJ-060) escalate to the Customer Advocate; cross-border data-rights conflicts (INJ-017, INJ-072) escalate to the EU Data Protection Officer | case/STAKEHOLDER_PACK.md; DR-EVID-07 |

### Workflow C — Bounded catastrophe, liquidity and reinsurance recovery planner

| Field | Content | Evidence |
|---|---|---|
| Who may request support | Catastrophe response lead or Reinsurance Director with current operational-capacity or treaty-notice responsibility for the specific event | case/STAKEHOLDER_PACK.md (Reinsurance Director row) |
| What the system may produce | Traceable response options using catastrophe events, exposure accumulation, claim severity, emergency hardship indicators, operational capacity, reserve uncertainty, reinsurance terms, hours clauses, currencies, collateral, sanctions screening status and customer-vulnerability indicators, each option scored on evidence quality and citing its source | case/INTEGRATED_CASE.md §4 Workflow C |
| What it must reject | Creating a payment; changing a reserve; aggregating a treaty event; submitting a recovery; allocating capital; instructing a vendor — in every case, without prior authorized human approval; any emergency hardship-advance option that has not confirmed coverage, sanctions and duplicate checks are complete (INJ-036) | DR-EVID-03, DR-EVID-05 (INJ-005); data/emergency_payment_requests.csv (INJ-036) |
| Which qualified human decides | Reinsurance Director for treaty event aggregation/notice/recovery submission; a named Catastrophe Response Lead (or equivalent local claims/finance authority) for hardship-advance and vendor-instruction approval, each verified against a current authorization record | case/STAKEHOLDER_PACK.md (Reinsurance Director row: "Notice and recovery governance") |
| Who handles escalation | Treaty wording or event-definition disputes (INJ-051, INJ-052) escalate to the Reinsurance Director; sanctions-name collisions with incomplete identity data (INJ-047) escalate jointly to the Reinsurance Director/Catastrophe Response Lead and Special Investigations before any hardship payment option is presented; vendor outage during peak triage (INJ-035) escalates to the CISO/operations lead for degraded-mode decision | case/STAKEHOLDER_PACK.md; data/reinsurance_treaties.csv; data/sanctions_screening.csv |

## Accountability escalation rule (INJ-088)

Per Working assumption A-04: when global AI Product Owner priorities (standard automation, consistent workflow behaviour) conflict with a local claims officer's, actuary's or compliance leader's judgement on a specific case, the **local qualified role's decision governs that case**. The AI Product Owner may escalate a systemic disagreement (e.g., a recurring pattern across many cases) to the Group CEO for a product-scope policy change, but may not override an individual case decision. This rule must be implemented as a non-bypassable approval gate in `submission/src`, not only documented here (see Controls table, CTRL-DR-04).

## Full INJ-005 prohibited-action coverage check

Every prohibited action from `data/decision_rights.csv` record `INJ-005-DECISION_RIGHTS` and `data/ai_use_boundaries.csv` record `INJ-005-AI_USE_BOUNDARIES` appears explicitly in the "What it must reject" column of at least one workflow above:

| Prohibited action | Appears in |
|---|---|
| Autonomous binding | Workflow A, Workflow B |
| Declinature | Workflow B |
| Pricing | Workflow B |
| Reserve changes | Workflow A, Workflow C |
| Settlement | Workflow A |
| Payment | Workflow A, Workflow C |
| Policy cancellation | Workflow A, Workflow B |
| Claim repudiation | Workflow A |
| Treaty placement (aggregation/recovery submission, Workflow C analogue) | Workflow C |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-DR-01 | No workflow output is treated as a binding/pricing/reserve/settlement/payment/cancellation/repudiation/treaty decision | Design review of output schema against DR-EVID-03/DR-EVID-05 and this matrix | Output schema has no field or code path that writes a coverage/price/reserve/payment/treaty conclusion | submission/artefacts/04_PRODUCT_SERVICE_BLUEPRINT.md | AI Product Owner |
| CTRL-DR-02 | Authority is never inferred from title | Test case: submit a request tagged with a matching title but no current entitlement record; verify rejection | Request is rejected/abstains until a current entitlement record is presented | submission/tests (to be implemented) | CISO |
| CTRL-DR-03 | Authority-exceedance evidence (INJ-009, INJ-020 patterns) is flagged, not silently resolved | Test case using DR-EVID-06/DR-EVID-07 patterns | Flag is raised and routed to the named human approver in the relevant workflow row above; no automatic override reversal | submission/tests (to be implemented) | Chief Underwriter, Group Chief Claims Officer |
| CTRL-DR-04 | INJ-088 accountability rule (local role governs individual case decisions) is enforced as a non-bypassable approval gate | Design review plus test case simulating a global-policy vs. local-officer conflict | Local officer's case-level decision cannot be overridden by a global/product-scope role in the implemented workflow | submission/artefacts/04_PRODUCT_SERVICE_BLUEPRINT.md; submission/tests (to be implemented) | Group Chief Claims Officer |

## Traceability

| Inject/requirement | Matrix section | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| INJ-005 | Full INJ-005 prohibited-action coverage check; all three workflow rows | Human-approval gate (not yet implemented) | CTRL-DR-01; to be defined further in submission/artefacts/22_EVALUATION_TEVV.md | Gate must be enforced in code, not only documented; residual risk until implemented and tested. |
| INJ-088 | Accountability escalation rule | Non-bypassable approval gate (not yet implemented) | CTRL-DR-04 | Escalation rule could be contested by global AI owners in practice; requires Board/CEO-level reaffirmation if challenged. |
| INJ-009 | Working assumption A-02; CTRL-DR-02 | Entitlement-check component (not yet implemented) | CTRL-DR-02 | Portal-outage/degraded-mode scenarios (as in INJ-009) may require a documented manual fallback authority path, not yet designed. |
| INJ-020 | Workflow B escalation; CTRL-DR-03 | Override-pattern flag (not yet implemented) | CTRL-DR-03 | Requires access to override-event data at sufficient granularity, which the supplied evidence-envelope schema does not fully provide. |
| INJ-013, INJ-017, INJ-045, INJ-047, INJ-051, INJ-052, INJ-059, INJ-060 | Workflow-specific escalation rows | Deferred to later workflow-specific artefacts | Not yet defined | Each escalation path is named here but not yet implemented or tested; tracked individually in the relevant later template (e.g., 14, 16, 18, 19). |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| This matrix is a design-time summary and could be mistaken for a runtime authority source (Working assumption A-03) | Medium | Documented explicitly; enforce via design review (CTRL-DR-01) and entitlement-check implementation (CTRL-DR-02) | AI Product Owner | Open — mitigated by documentation, not yet by code | Before any implementation PR is merged |
| INJ-088 accountability rule (local role governs) has not been independently confirmed by the Group CEO or Board | High | Treat as the working resolution for this artefact only; escalate for Board confirmation before go-live | Group CEO | Open — pending Board confirmation | Before workflow go-live |
| Delegated-authority breach pattern (INJ-009) and override concentration (INJ-020) have no attached remediation owner beyond the escalation path named above | High | Escalate to Chief Underwriter / Group Chief Claims Officer; do not treat as resolved by this artefact | Chief Underwriter, Group Chief Claims Officer | Open | Before Workflow B/A go-live |

## Sign-off

| Role | Reviewer | Status |
|---|---|---|
| Reviewer | R5 | Pending review |
| Gate | G1 — no unresolved Critical/High finding | Pending |
