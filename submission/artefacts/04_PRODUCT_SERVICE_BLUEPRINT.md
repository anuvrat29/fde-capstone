# 04 Product Service Blueprint

## Purpose

Personas, jobs, service blueprint, prohibited actions, human review and contestability for the three mandatory workflows (coverage/claim evidence reconciliation, underwriting/pricing decision support, catastrophe/reinsurance planning support).

## Acceptance criteria

- The artefact is evidence-led and references supplied paths, record locators and inject IDs.
- Facts, assumptions, inference, conflict, decision and residual risk are distinguishable.
- Temporal, jurisdictional, authorization and authority boundaries are explicit where relevant.
- Owners, approvals, review triggers and measurable acceptance gates are named.
- The artefact contains no unsupported coverage, pricing, reserve, payment or treaty conclusion.

## Artefact-specific acceptance criteria

- Each of the three workflows names exactly one primary human-approver persona whose action converts an AI-prepared finding into an operational step (A-01).
- Each workflow's prohibited-action list (CTRL-PSB-01/02/03) is enforced as a structural output-schema constraint, not only as documentation.
- A prompt-injection test using knowledge/MALICIOUS_ADJUSTER_REPORT.md demonstrates that embedded instructions in evidence are never followed as system authority (CTRL-PSB-04).

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| EVID-036 | case/INTEGRATED_CASE.md Section 4 (Mandatory workflows) | approved/case-pack | 2026-08-01 | MULTI | Defines Workflow A/B/C scope and explicit prohibited actions per workflow. |
| EVID-008 | data/ai_use_boundaries.csv (record_id=INJ-005-AI_USE_BOUNDARIES) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Board-level prohibited-action list (INJ-005). |
| EVID-025 | knowledge/UNDERWRITING_HUMAN_AUTHORITY.md | approved/trusted_with_conditions | 2026-01-01 | global | AI prepares evidence/options only; humans bind/decline/price/alter terms. |
| EVID-024 | knowledge/POLICY_WORDING_AUTHORITY.md | approved/trusted_with_conditions | 2026-01-01 | global | Signed schedule/endorsement over marketing summary; applies to Workflow A/B outputs referencing wording. |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | Each workflow has exactly one primary human-approver persona whose action converts an AI-prepared finding into an operational step; the AI never performs that conversion itself. | case/INTEGRATED_CASE.md Section 4; knowledge/UNDERWRITING_HUMAN_AUTHORITY.md | Without a named approver persona per workflow, "human review" becomes an unenforceable slogan rather than a designed control. | AI Product Owner | Before design freeze |
| A-02 | Prohibited actions (bind, repudiate, settle, pay, reserve, price, decline, renew, cancel, litigate, aggregate treaty event, submit recovery, allocate capital, instruct vendor) apply identically regardless of model confidence score, per INJ-005 and knowledge/*_AUTHORITY.md documents. | data/ai_use_boundaries.csv; knowledge/POLICY_WORDING_AUTHORITY.md; knowledge/UNDERWRITING_HUMAN_AUTHORITY.md | A high-confidence AI output could otherwise be treated as sufficient authority for a prohibited action, which the case pack explicitly rejects. | AI Product Owner, CISO | Ongoing |
| A-03 | Instructions embedded in evidence documents (e.g., knowledge/MALICIOUS_ADJUSTER_REPORT.md) are data, not system instructions, per every knowledge/*_AUTHORITY.md document's "Prohibited use" section. | knowledge/*_AUTHORITY.md documents (consistent boilerplate clause) | Failure to enforce this distinction is a direct path to prompt-injection compromise, a mandatory security-evidence area in requirements/ARTEFACT_EXPECTATIONS.md. | CISO, AI Product Owner | Before any tool/agent integration is built |

## Required analysis and decisions

| Decision/question | Evidence | Analysis | Decision/output | Owner | Status |
|---|---|---|---|---|---|
| Who is the primary persona and job-to-be-done for Workflow A (coverage/claim/fraud evidence reconciliation)? | case/INTEGRATED_CASE.md Section 4; data/claims.csv; data/loss_events.csv | Claims handlers/adjusters need to reconcile policy version, endorsement timing, coverage, exclusion, claimant identity and evidence provenance across contradictory sources (e.g., INJ-007, INJ-008, INJ-021, INJ-022) without the tool ever binding, repudiating, settling, reserving, paying, cancelling or litigating a claim | Persona: Claims Handler / Senior Adjuster. Job: "Assemble a structured, evidence-cited reconciliation of a claim's coverage-relevant facts so I can make (or escalate) a claim decision." | Group Chief Claims Officer | Decided — persona and job defined; UI/service steps deferred |
| Who is the primary persona and job-to-be-done for Workflow B (underwriting/pricing/customer-outcome evidence support)? | case/INTEGRATED_CASE.md Section 4; data/underwriting_decisions.csv; data/override_events.csv | Underwriters need bounded recommendations and alternatives while retaining sole authority to bind, decline, price, renew, cancel or modify a policy (INJ-020 shows override transparency is already a live concern) | Persona: Underwriter (commercial/life/motor per product). Job: "Get a bounded, cited set of underwriting options and risk flags so I can decide within my delegated authority." | US Chief Underwriter | Decided — persona and job defined |
| Who is the primary persona and job-to-be-done for Workflow C (catastrophe/liquidity/reinsurance recovery planner)? | case/INTEGRATED_CASE.md Section 4; data/cat_events.csv (not yet detailed in this pass) | Catastrophe/reinsurance leads need traceable response options without the tool creating a payment, changing a reserve, aggregating a treaty event, submitting a recovery, allocating capital or instructing a vendor | Persona: Catastrophe Response Lead / Reinsurance Director. Job: "Get a traceable set of response options with evidence citations so I can approve (or reject) an action within my authority." | Reinsurance Director | Decided — persona and job defined |

## Alternatives and trade-offs

| Option | Benefits | Risks | Cost/complexity | Reversibility | Decision and rationale |
|---|---|---|---|---|---|
| Single generic "AI assistant" persona serving all three workflows | Simpler to build once | Blurs the distinct authority boundaries per workflow (INJ-005 lists prohibitions specific to each domain); risks a claims-context prompt leaking into a pricing decision | Lower build cost | Reversible, but with rework cost | Rejected. Distinct personas per workflow are required to keep prohibited-action lists workflow-specific and auditable. |
| Three distinct workflow services, each with its own persona, job, output schema and human-approval gate | Matches case/INTEGRATED_CASE.md structure exactly; keeps prohibited-action enforcement scoped and auditable per workflow | Higher build/maintenance cost (three service surfaces instead of one) | Higher | Fully reversible per workflow (each can be disabled independently via AI-disabled continuity) | Selected. Aligns with the case pack's explicit three-workflow mandate and supports independent kill-switch/degraded-mode operation per workflow. |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-PSB-01 | Workflow A output never contains a coverage bind/repudiate/settle/reserve/pay/cancel/litigate action | Output-schema design review; negative test cases | Schema has no field or action type representing these outcomes; attempts to request one return an abstention/escalation response | submission/tests (deferred) | Group Chief Claims Officer |
| CTRL-PSB-02 | Workflow B output never contains a bind/decline/price/renew/cancel/modify action | Output-schema design review; negative test cases | Same pattern as CTRL-PSB-01, scoped to Workflow B's prohibited list | submission/tests (deferred) | US Chief Underwriter |
| CTRL-PSB-03 | Workflow C output never creates a payment, reserve change, treaty aggregation, recovery submission, capital allocation or vendor instruction | Output-schema design review; negative test cases | Same pattern, scoped to Workflow C's prohibited list | submission/tests (deferred) | Reinsurance Director |
| CTRL-PSB-04 | Embedded instructions in evidence documents are never treated as system authority | Prompt-injection test using knowledge/MALICIOUS_ADJUSTER_REPORT.md as adversarial input | Workflow output does not follow any instruction embedded in the untrusted document; flags it as untrusted content instead | submission/tests (deferred; required per requirements/ARTEFACT_EXPECTATIONS.md security evidence) | CISO |

## Traceability

| Inject/requirement | Architecture/ADR | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| INJ-005 (prohibited autonomy) | Deferred to submission/artefacts/11_ADR_REGISTER.md | Output-schema prohibition enforcement (not yet implemented) | CTRL-PSB-01/02/03 (deferred) | Enforcement must be structural (code-level), not only documented, to survive a defence panel challenge per requirements/FINAL_DEFENCE.md. |
| Untrusted-evidence handling (starter/baseline_diagnostics.py finding: "untrusted evidence contains prompt-like instructions") | Deferred | Prompt-injection defence (not yet implemented) | CTRL-PSB-04 (deferred) | This is a disclosed, seeded risk (knowledge/MALICIOUS_ADJUSTER_REPORT.md); must be explicitly tested, not assumed handled by a generic system prompt. |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| No service-blueprint swimlane detail (front-stage/back-stage steps, touchpoints) has yet been drafted beyond persona/job/prohibition level | Medium | Defer detailed swimlane design to the implementation pass covering submission/src and submission/app | AI Product Owner | Open | Before Workflow A/B/C implementation begins |
| Prompt-injection defence (CTRL-PSB-04) is a documented requirement but has no implementation or test yet | High | Track as a non-compensable-gate-adjacent risk (requirements/SCORING_MODEL.md gate 3) requiring priority implementation | CISO | Open | Before any workflow is connected to an evidence ingestion pipeline |
| Contestability mechanism (how a customer or claimant challenges a workflow output) is named in case/STAKEHOLDER_PACK.md ("The customer must be able to challenge the evidence and the rule, not merely the prose") but not yet designed | Medium | Defer to a later pass; flag explicitly here so it is not silently dropped | Customer Advocate | Open | Before Workflow A/B go-live |
