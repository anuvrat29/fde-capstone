# 23 Token Finops

## Purpose

Token efficiency, unit economics, cost per successful outcome, budgets and controls for the three workflows, closing the numeric-budget gap deferred from 13_MODEL_PROMPT_LIFECYCLE.md (REQ-NF-12/13) and grounded in the confirmed model price-shock and denial-of-wallet injects.

## Acceptance criteria

- The artefact is evidence-led and references supplied paths, record locators and inject IDs.
- Facts, assumptions, inference, conflict, decision and residual risk are distinguishable.
- Temporal, jurisdictional, authorization and authority boundaries are explicit where relevant.
- Owners, approvals, review triggers and measurable acceptance gates are named.
- The artefact contains no unsupported coverage, pricing, reserve, payment or treaty conclusion.

## Artefact-specific acceptance criteria

- Unit cost is calculated per successful reviewed outcome, never per raw model call, directly satisfying DEFINITION_OF_DONE.md's "Token and unit economics are measured per successful reviewed outcome, not per raw model call" requirement (CTRL-TF-01).
- The confirmed OM-Large 65% price increase (INJ-089) has a stated budget response — absorb, substitute, or re-negotiate — not left unaddressed (CTRL-TF-02).
- The confirmed denial-of-wallet pattern (INJ-090, oversized claim bundles/image reprocessing) has an explicit per-request cost ceiling closing REQ-NF-13's numeric-value gap from 13_MODEL_PROMPT_LIFECYCLE.md (CTRL-TF-03).
- No workflow's cost model excludes human-review time, consistent with the value-leakage discipline already established in 01_BUSINESS_CASE.md (CTRL-BC-03) (CTRL-TF-04).

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| EVID-109 | data/model_costs.csv (provider=OmniModel;model=OM-Large;OM-Small) | domain_specific/vendor_pricing | 2026-08-15 | global | Confirmed model price shock: OM-Large input/output per-million pricing rises 65% effective 2026-08-15; OM-Small unchanged. |
| EVID-111 | data/vendor_contracts.csv (record_id=INJ-089-VENDOR_CONTRACTS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Corroborates INJ-089; preferred provider raises input-token prices 65% and removes cached-input discounts. |
| EVID-110 | data/model_usage.csv (record_id=INJ-090-MODEL_USAGE) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Denial-of-wallet: repeated oversized claim bundles and image reprocessing cause abnormal inference/OCR/embedding cost (INJ-090). |
| EVID-010 | data/cost_model.csv (record_id=INJ-006-COST_MODEL) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Reused from 01_BUSINESS_CASE.md; cost model excluding complaints/appeals/litigation/human-review lines — the same discipline (CTRL-BC-03) is reapplied to per-outcome unit costing here. |
| EVID-061 | knowledge/AGENT_BUDGET_STOP_POLICY.md | approved/trusted_with_conditions | 2026-01-01 | global | Reused from 13/16; requires maximum steps/time/token/tool/cost budgets and deterministic stop reasons; controlling standard for the budget table below. |
| EVID-057 | data/model_registry.csv (model_id=PRC-MOTOR-9;FRD-CLAIM-6;GEN-SUM-3) | approved | 2026-01-01 | global | Reused from 13/15; approved model registry, cross-referenced to which registered model each workflow's cost driver corresponds to. |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | "Successful outcome" is defined as a workflow output that reaches human review and is either approved, escalated with clear reasoning, or explicitly abstained — never a raw model call, regardless of whether that call produced a usable output. | DEFINITION_OF_DONE.md's per-successful-reviewed-outcome requirement | Costing per raw model call would understate true unit cost by ignoring retries, escalations and abstentions that consume resources without producing a usable outcome. | AI Product Owner, Finance | Before any unit-cost figure is published |
| A-02 | The confirmed OM-Large price shock (INJ-089, 65% increase) requires an explicit budget response decision now, not a wait-and-see approach, because the price change is already effective (2026-08-15) per data/model_costs.csv. | data/model_costs.csv (EVID-109); data/vendor_contracts.csv (EVID-111) | Deferring the decision risks absorbing the full 65% increase by default, silently inflating the per-outcome cost this artefact is meant to control. | AI Product Owner, Finance | Before 2026-08-15 (the price change's effective date) |
| A-03 | The denial-of-wallet pattern (INJ-090) requires a per-request cost ceiling enforced before the request is processed, not a post-hoc cost review; this is the numeric-value closure for REQ-NF-13 (token and cost budgets), which 13_MODEL_PROMPT_LIFECYCLE.md specified only as a taxonomy without a number. | data/model_usage.csv (EVID-110); knowledge/AGENT_BUDGET_STOP_POLICY.md (EVID-061) | A post-hoc-only review would allow the abnormal cost to be incurred before detection, defeating the purpose of a budget ceiling. | AI Product Owner, CISO | Before any Workflow A image/document-reprocessing feature is designed |
| A-04 | Human-review time must be included in every workflow's per-outcome cost model, at a fully-loaded staff rate, consistent with 01_BUSINESS_CASE.md's CTRL-BC-03 (value-leakage costs must be included); this artefact reapplies that same discipline specifically to the token/cost-efficiency context. | data/cost_model.csv (EVID-010, reused) | Excluding human-review time would make an AI-assisted workflow appear artificially cheaper than a fair comparison against the no-AI alternative (01_BUSINESS_CASE.md's ADR-01 sequencing). | Chief Actuary, Finance | Before any per-outcome cost figure is compared against the no-AI baseline |

## Required analysis and decisions

| Workflow | Volume unit | Token/runtime driver | Unit cost | Budget/threshold | Quality trade-off |
|---|---|---|---|---|---|
| Workflow A (coverage/claim/fraud evidence reconciliation) | Per claim-evidence-reconciliation request reaching human review | FRD-CLAIM-6 (fraud referral) + GEN-SUM-3 (evidence summarisation) token consumption, plus OCR/image-reprocessing calls implicated in INJ-090 | Not yet computed — requires actual per-call token counts from an implemented workflow, which does not yet exist; cost driver components identified, not yet priced | Per-request cost ceiling required before oversized claim bundles are processed (A-03); numeric ceiling value deferred to implementation with CISO/Finance input | Lower token budget risks truncating evidence reconciliation on catastrophe-scale multi-document claims; higher budget risks the INJ-090 denial-of-wallet pattern recurring |
| Workflow B (underwriting/pricing decision support) | Per underwriting-recommendation request reaching human review | PRC-MOTOR-9 (motor pricing support) token/inference consumption | Not yet computed — same reason as Workflow A | Standard per-request budget (no confirmed denial-of-wallet pattern specific to Workflow B in supplied evidence); numeric value deferred | Fairness disclosure requirement (CTRL-AMR-01, 15) adds a small fixed per-request overhead (the disclosure text itself); this overhead is treated as a required cost, not an efficiency target |
| Workflow C (catastrophe/liquidity/reinsurance planning) | Per catastrophe-response-option request reaching human review | GEN-SUM-3 (evidence summarisation) plus the bounded fraud-ring graph component's traversal cost (per 12_INTEGRATION_CONTRACTS.md) | Not yet computed | Bounded-traversal-depth ceiling (REQ-NF-12, still numerically unset per 10/12/13's open issues) directly caps this workflow's worst-case token cost; this artefact does not itself set that number, only flags the dependency | Lower traversal-depth ceiling risks missing a genuine multi-hop fraud-ring pattern; higher ceiling risks unbounded cost under adversarial input (per 16_THREAT_ABUSE_MODEL.md's graph denial-of-wallet case) |
| Cross-cutting: OM-Large model substitution response to INJ-089 | N/A (vendor-pricing decision, not workflow-specific) | OM-Large input/output per-million pricing (data/model_costs.csv) | Confirmed: 65% increase on OM-Large; OM-Small unchanged | Budget response options: (a) absorb the 65% increase for OM-Large-dependent calls; (b) substitute OM-Small where quality permits; (c) re-negotiate with OmniModel citing the removed cached-input discount | Substituting OM-Small (lower cost) against OM-Large-quality-dependent tasks risks a quality regression; this trade-off must be assessed per call site, not decided once globally |

## Alternatives and trade-offs

| Option | Benefits | Risks | Cost/complexity | Reversibility | Decision and rationale |
|---|---|---|---|---|---|
| Cost per raw model call (industry-common but shallow metric) | Simple to measure directly from vendor billing | Understates true cost by excluding retries, escalations, abstentions and human-review time; would misrepresent the AI-assisted option's cost against the no-AI alternative comparison already sequenced in 01_BUSINESS_CASE.md ADR-01 | Lowest measurement complexity, high risk of a misleading business case | Reversible but any published figure using this method would need correction later | Rejected. DEFINITION_OF_DONE.md explicitly requires "per successful reviewed outcome, not per raw model call" (A-01). |
| Absorb the OM-Large 65% price increase without any budget response, treating it as an unavoidable cost pass-through | Simplest immediate action (no engineering or negotiation effort) | Silently inflates per-outcome cost; risks breaching whatever cost ceiling would otherwise be set for the affected workflow | No immediate cost, but ongoing inflated run cost | Reversible by later substituting or renegotiating, but every day of inaction compounds the cost | Rejected as the default. A-02 requires an explicit decision (absorb/substitute/renegotiate) made deliberately, not by default inaction. |
| Set no per-request cost ceiling, relying only on post-hoc monthly cost review to catch denial-of-wallet patterns like INJ-090 | Simpler to implement (no pre-request check needed) | The abnormal cost is already incurred by the time a monthly review catches it; directly fails to prevent the INJ-090 pattern, only detects it after the fact | Lower engineering cost, unacceptable residual risk for a confirmed live pattern | Reversible but every incident before the ceiling is added incurs real cost | Rejected. A-03 requires pre-request enforcement, consistent with the bounded-steps/budget discipline already established in 13/16. |
| Per-outcome (not per-call) unit costing, an explicit three-option budget response to the confirmed price shock, a pre-request cost ceiling for the confirmed denial-of-wallet pattern, and mandatory inclusion of human-review time in every cost figure | Directly satisfies all four artefact-specific acceptance criteria and reuses the existing value-leakage discipline from 01 rather than inventing a new costing philosophy | Numeric ceiling/threshold values are not yet set in this pass, requiring a follow-up decision with Finance/CISO input | Medium — costing framework specified now, numeric calibration deferred | Reversible; ceilings can be tuned as real usage data becomes available | Selected. Matches DEFINITION_OF_DONE.md's per-outcome requirement and closes the confirmed INJ-089/INJ-090 gaps with a decision framework, even though final numbers await real implementation data. |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-TF-01 | Unit cost is calculated per successful reviewed outcome | Review of any published cost figure's denominator | Denominator is "successful reviewed outcomes" per A-01, never raw model calls | This artefact, Required analysis and decisions table | Finance |
| CTRL-TF-02 | The confirmed OM-Large price shock has a stated budget response | Review of the Cross-cutting row's Budget/threshold column | One of absorb/substitute/renegotiate is explicitly selected before 2026-08-15 | This artefact, Required analysis and decisions table | AI Product Owner, Finance |
| CTRL-TF-03 | Denial-of-wallet pattern has a pre-request cost ceiling | Test submitting an oversized claim bundle (data/model_usage.csv INJ-090 pattern) against the specified ceiling | Request is rejected/throttled before full processing cost is incurred, not merely logged afterward | submission/tests (deferred) | CISO |
| CTRL-TF-04 | No cost model excludes human-review time | Review of every workflow's Unit cost calculation methodology | Human-review time at a fully-loaded rate is a line item in every workflow's cost model | This artefact, Required analysis and decisions table; cross-referenced to CTRL-BC-03 (01_BUSINESS_CASE.md) | Chief Actuary, Finance |

## Traceability

| Inject/requirement | Architecture/ADR | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| INJ-089 (model price shock) | New: three-option budget-response decision (this artefact) | Model-substitution/renegotiation logic (not yet implemented; decision not yet finalised) | TEST-COST-BUDGET (22_EVALUATION_TEVV.md, deferred) | Which of absorb/substitute/renegotiate to choose is not yet decided; requires Finance sign-off. |
| INJ-090 (denial-of-wallet) | New: pre-request cost-ceiling control (this artefact) | Cost-ceiling enforcement gate (not yet implemented) | CTRL-TF-03 (deferred) | Numeric ceiling value not yet set. |
| REQ-NF-12, REQ-NF-13 (bounded steps, token/cost budgets) | Cross-referenced to 10/13's taxonomy and architectural home | Budget/stop-reason enforcement logic (not yet implemented) | CTRL-MPL-03 (13, deferred); CTRL-TF-03 (this artefact, deferred) | This artefact adds the cost-ceiling half of the requirement; the step/time-bound half remains with 13's design. |
| Value-leakage discipline (INJ-006, 01_BUSINESS_CASE.md) | Cross-referenced to CTRL-BC-03 | Human-review-time cost-model line item (not yet implemented) | CTRL-TF-04 (deferred) | Fully-loaded staff rate for human review is not yet quantified beyond data/staff_rates.csv's evidence-envelope granularity (per 01's own limitation note). |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| No actual per-outcome unit cost has been computed for any workflow; all Unit cost cells state "not yet computed" pending an implemented workflow to measure | High | Track alongside the "no implementation code" gap already logged in ARTEFACT_STATE_LOG.md | Finance, AI Product Owner | Open | Before templates 26–28 (target operating model, production readiness) |
| The OM-Large price-shock budget response (absorb/substitute/renegotiate) is not yet decided, and the price change is already effective (2026-08-15) | High | Escalate to Finance and AI Product Owner for an immediate decision | Finance | Open | Before 2026-08-15 |
| The denial-of-wallet cost ceiling (CTRL-TF-03) has no numeric value | Medium | Set with CISO and Finance input, informed by real usage data once available | CISO, Finance | Open | Before any Workflow A image/document-reprocessing feature is implemented |
| The bounded fraud-ring graph traversal-depth ceiling (REQ-NF-12) remains numerically unset across four prior artefacts (10/12/13/16) and this one | Medium | Consolidate into a single decision point rather than deferring across five artefacts indefinitely | AI Product Owner | Open | Before Workflow A/C fraud-ring feature design freeze |