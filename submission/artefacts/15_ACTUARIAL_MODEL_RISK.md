# 15 Actuarial Model Risk

## Purpose

Actuarial assumptions, validation, drift, uncertainty, overrides and model-use boundaries for the pricing, catastrophe and specialty models named in data/model_registry.csv, grounded in confirmed live fairness breaches, catastrophe model-version splits, and sparse specialty portfolio risk.

## Acceptance criteria

- The artefact is evidence-led and references supplied paths, record locators and inject IDs.
- Facts, assumptions, inference, conflict, decision and residual risk are distinguishable.
- Temporal, jurisdictional, authorization and authority boundaries are explicit where relevant.
- Owners, approvals, review triggers and measurable acceptance gates are named.
- The artefact contains no unsupported coverage, pricing, reserve, payment or treaty conclusion.

## Artefact-specific acceptance criteria

- Every model in data/model_registry.csv with a confirmed subgroup breach in data/fairness_metrics.csv (PRC-MOTOR-9, FRD-CLAIM-6) has an explicit model-use restriction recorded here, not only a future deferral to template 18 (CTRL-AMR-01).
- The catastrophe model-version split (INJ-015) is resolved by requiring every exposure-aggregate output to disclose which cat_model version produced it, never a silently blended figure (CTRL-AMR-02).
- No actuarial or pricing model output is treated as a final price, reserve or underwriting decision; every row's Decision/output column states an evidence-preparation role only, consistent with non-compensable gate 1 (CTRL-AMR-03).
- The sparse specialty portfolio risk (INJ-019, cyber) requires an explicit uncertainty disclosure whenever a cyber-model output is used, never presented with the same confidence as a mature-portfolio model (CTRL-AMR-04).

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| EVID-057 | data/model_registry.csv (model_id=PRC-MOTOR-9;FRD-CLAIM-6;GEN-SUM-3) | approved | 2026-01-01 | global | Reused from 13_MODEL_PROMPT_LIFECYCLE.md; approved model registry with risk_tier and approval_status per model. |
| EVID-067 | data/pricing_factors.csv (record_id=INJ-013-PRICING_FACTORS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Protected-proxy pricing: motor pricing uses postcode, occupation and device variables that strongly proxy protected characteristics (INJ-013). |
| EVID-068 | data/fairness_metrics.csv (model_id=PRC-MOTOR-9;FRD-CLAIM-6;UW-LIFE-4) | domain_specific/model_governance | 2026-08-06 | MULTI | Confirmed live subgroup fairness breaches: PRC-MOTOR-9 postal_proxy_low_income selection_rate 0.61 vs reference 0.82 (status=breach); FRD-CLAIM-6 Hindi_language false_positive_rate 0.31 vs reference 0.14 (status=breach); UW-LIFE-4 female_45_60 status=review. |
| EVID-069 | data/cat_models.csv (record_id=INJ-015-CAT_MODELS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Catastrophe model version split: property accumulation reports use two catastrophe-model versions with materially different flood loss estimates (INJ-015). |
| EVID-070 | data/exposure_aggregates.csv (record_id=INJ-015-EXPOSURE_AGGREGATES) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Corroborates INJ-015. |
| EVID-072 | data/cyber_risks.csv (record_id=INJ-019-CYBER_RISKS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Sparse specialty portfolio: cyber model extrapolates from a small, non-representative loss history and ignores silent-cyber exposure (INJ-019). |
| EVID-025 | knowledge/UNDERWRITING_HUMAN_AUTHORITY.md | approved/trusted_with_conditions | 2026-01-01 | global | Reused from 03/04/14; AI may prepare evidence/options only, binding/declining/pricing remains a licensed human action — directly scopes every model's permitted use in this artefact. |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | data/fairness_metrics.csv's `status=breach` rows (PRC-MOTOR-9, FRD-CLAIM-6) are treated as confirmed, live governance failures requiring an immediate use restriction, not as a future finding to be addressed only in template 18 (Responsible AI and Fairness); this artefact records the actuarial-model-risk-specific restriction now, and template 18 will address the broader fairness remediation programme. | data/fairness_metrics.csv (EVID-068) | Deferring the restriction entirely to template 18 would leave these two models usable without restriction in the interim, contradicting DEFINITION_OF_DONE.md's "material fairness...failures are disclosed" requirement. | Model Risk Owner, Chief Actuary | Immediate — before any further use of PRC-MOTOR-9 or FRD-CLAIM-6 |
| A-02 | The catastrophe model-version split (INJ-015) means any exposure-aggregate figure not labelled with its source cat_model version is treated as ambiguous and must not be used for a Workflow C planning recommendation without that label. | data/cat_models.csv (EVID-069); data/exposure_aggregates.csv (EVID-070) | Blending or silently choosing one version's figure would hide a materially different flood-loss estimate from the human decision-maker, undermining CTRL-DGL-02's currency-disaggregation discipline applied here to model-version disaggregation. | Chief Actuary, Reinsurance Director | Before any Workflow C exposure-aggregate output is generated |
| A-03 | UW-LIFE-4's `status=review` (not yet `breach`) for the female_45_60 subgroup is treated as an open monitoring item requiring documented review, not as an immediate use restriction; this distinguishes it from PRC-MOTOR-9/FRD-CLAIM-6's confirmed breach status. | data/fairness_metrics.csv (EVID-068) | Treating `review` status identically to `breach` would either overstate the current evidence (if review clears the model) or understate it (if review confirms a breach); the distinction must be preserved. | Model Risk Owner | Before UW-LIFE-4's review is closed |
| A-04 | Cyber model outputs (INJ-019, sparse specialty portfolio) must carry an explicit "high model uncertainty — limited loss history" disclosure whenever used in Workflow B or C evidence preparation, distinguishing them from motor/property models with larger, more representative loss histories. | data/cyber_risks.csv (EVID-072) | Presenting a sparse-portfolio model's output with unqualified confidence could mislead an underwriter into over-relying on a statistically thin extrapolation. | Chief Actuary | Before any cyber-risk Workflow B/C feature is designed |

## Required analysis and decisions

| Decision/question | Evidence | Analysis | Decision/output | Owner | Status |
|---|---|---|---|---|---|
| What use restriction applies to PRC-MOTOR-9 given its confirmed postal_proxy_low_income breach? | data/fairness_metrics.csv (EVID-068, INJ-013 corroboration EVID-067) | PRC-MOTOR-9 is registered for "motor pricing support" at `approved` status, but its confirmed breach (selection_rate 0.61 vs reference 0.82) means its postcode-linked pricing factor is currently proxying a protected characteristic; per A-01, this model may continue to prepare bounded evidence for Workflow B only with the breach explicitly disclosed in every output touching this subgroup, pending template 18's fairness remediation | PRC-MOTOR-9 use is restricted to disclosed-breach evidence preparation only; it may not be used to prepare an undisclosed recommendation for any postal_proxy_low_income-flagged application | Chief Actuary, Model Risk Owner | Decided — restriction recorded, remediation deferred to template 18 |
| What use restriction applies to FRD-CLAIM-6 given its confirmed Hindi_language breach? | data/fairness_metrics.csv (EVID-068) | FRD-CLAIM-6 (claim fraud referral) shows a false_positive_rate of 0.31 for Hindi-language claimants against a reference rate of 0.14 — more than double — meaning Hindi-language claimants are more than twice as likely to be incorrectly flagged; this model feeds evidence into the fraud-ring graph component's human-routed output (per 13_MODEL_PROMPT_LIFECYCLE.md) but must not be the sole basis for flagging a Hindi-language claimant | FRD-CLAIM-6 output for any Hindi-language-flagged claimant must be disclosed as carrying a known elevated false-positive risk before a human investigator reviews it | Chief Actuary, Group Chief Claims Officer | Decided — restriction recorded |
| How should the catastrophe model-version split (INJ-015) be handled in exposure-aggregate reporting? | data/cat_models.csv (EVID-069); data/exposure_aggregates.csv (EVID-070) | Per A-02, every exposure-aggregate figure must disclose its source cat_model version; where two versions produce materially different flood-loss estimates for the same exposure, both figures are reported side by side, not blended or defaulted to one | Workflow C output presents version-labelled figures; no single "the" flood-loss estimate is asserted without a version citation | Chief Actuary, Reinsurance Director | Decided |
| How should sparse specialty portfolio risk (INJ-019, cyber) be disclosed in model output? | data/cyber_risks.csv (EVID-072) | Per A-04, every cyber-model output carries an explicit uncertainty disclosure distinguishing it from motor/property model outputs with larger loss histories | Cyber-risk evidence preparation includes a mandatory "high model uncertainty — limited loss history" label | Chief Actuary | Decided |

## Alternatives and trade-offs

| Option | Benefits | Risks | Cost/complexity | Reversibility | Decision and rationale |
|---|---|---|---|---|---|
| Take no action on PRC-MOTOR-9/FRD-CLAIM-6 until template 18 (Responsible AI and Fairness) is drafted | Avoids duplicating fairness analysis across two templates | Leaves two models with confirmed live breaches unrestricted in the interim, contradicting the DoD's disclosure requirement and risking a defence-panel challenge asking "why did you know about this and do nothing?" | Lowest cost now, highest reputational/compliance risk in the interim | Reversible but leaves a documented gap in the interim | Rejected. A-01 requires the actuarial-model-risk-specific restriction to be recorded now; template 18 will still separately address the broader remediation programme without duplicating this restriction. |
| Silently blend the two catastrophe model versions' flood-loss estimates into one "best estimate" figure for simplicity | Simpler reporting; one number instead of two | Directly reproduces the INJ-015 failure mode of hiding a materially different estimate; violates the evidence-preservation principle already established in every prior artefact (e.g., CTRL-OSL-03's disputed-window preservation) | Lower reporting complexity, high risk of a materially misleading combined figure | Costly to reverse if downstream planning decisions are already based on the blended figure | Rejected. Matches neither A-02 nor the package's broader "preserve contradictory... evidence" principle (knowledge/*_AUTHORITY.md boilerplate). |
| Per-model use restriction and disclosure requirements, recorded now, with detailed remediation deferred to template 18 and detailed evaluation/TEVV metrics deferred to template 22 | Closes the immediate disclosure gap without duplicating the deeper fairness-remediation and evaluation work scheduled for later templates | Requires this artefact and template 18/22 to stay synchronised so the restriction recorded here is not silently dropped when those templates are drafted | Medium — one artefact now, cross-referenced by two future artefacts | Reversible; restrictions can be tightened or loosened as more evidence arrives | Selected. Satisfies CTRL-AMR-01 through CTRL-AMR-04 without pre-empting the deeper analysis reserved for templates 18/22. |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-AMR-01 | Every model with a confirmed subgroup breach has an explicit use restriction recorded | Review of data/fairness_metrics.csv against this artefact's Required analysis and decisions table | PRC-MOTOR-9 and FRD-CLAIM-6 each have a stated restriction; UW-LIFE-4's `review` status is tracked separately per A-03 | This artefact, Required analysis and decisions table | Model Risk Owner |
| CTRL-AMR-02 | No exposure-aggregate output blends catastrophe model versions without disclosure | Test presenting a two-cat_model-version exposure scenario (data/cat_models.csv pattern) | Output shows both version-labelled figures, never one blended or silently-chosen figure | submission/tests (deferred) | Chief Actuary |
| CTRL-AMR-03 | No actuarial/pricing model output is treated as a final decision | Design review of every Decision/output column in this artefact | Every row states an evidence-preparation role, never a final price/reserve/underwriting decision | This artefact, Required analysis and decisions table | AI Product Owner |
| CTRL-AMR-04 | Cyber-model output always carries an uncertainty disclosure | Design review of any Workflow B/C output using data/cyber_risks.csv-sourced evidence | Output includes the "high model uncertainty — limited loss history" label | submission/tests (deferred) | Chief Actuary |

## Traceability

| Inject/requirement | Architecture/ADR | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| INJ-013 (protected-proxy pricing) | Reused model-registry scoping from 13_MODEL_PROMPT_LIFECYCLE.md | Breach-disclosure label on PRC-MOTOR-9 output (not yet implemented) | CTRL-AMR-01 (deferred); full remediation deferred to template 18 | Postcode-based proxy risk is disclosed but not yet removed from the pricing factor itself. |
| INJ-015 (catastrophe model version split) | New: version-disclosure requirement (this artefact) | Version-labelled exposure-aggregate output (not yet implemented) | CTRL-AMR-02 (deferred) | Two-version ambiguity is disclosed but not resolved; requires an actuarial judgement on which version to prefer, or whether both remain valid. |
| INJ-019 (sparse specialty portfolio) | New: uncertainty-disclosure requirement (this artefact) | Cyber-model uncertainty label (not yet implemented) | CTRL-AMR-04 (deferred) | Underlying data sparsity is disclosed but not remedied; requires more cyber-loss history over time. |
| Confirmed fairness breaches (data/fairness_metrics.csv) | To be further addressed in submission/artefacts/18_RESPONSIBLE_AI_FAIRNESS.md | Breach-disclosure labels (not yet implemented) | To be defined in submission/artefacts/22_EVALUATION_TEVV.md | This artefact records the immediate restriction; the deeper remediation programme (retraining, feature removal, or model retirement) is not yet designed. |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| PRC-MOTOR-9 and FRD-CLAIM-6's confirmed breaches have no implemented disclosure mechanism yet; the restriction is documented, not enforced in code | High | Track alongside the "no implementation code" gap already logged in ARTEFACT_STATE_LOG.md; escalate as non-compensable-gate-adjacent given DEFINITION_OF_DONE.md's disclosure requirement | Model Risk Owner | Open | Before any pricing/fraud-referral feature reaches a user-facing pilot |
| UW-LIFE-4's `review` status has no closure date in supplied evidence | Medium | Escalate to Model Risk Owner to obtain a review closure timeline | Model Risk Owner | Open | When the review closes |
| This artefact does not yet address D03 injects INJ-014 (telematics firmware drift), INJ-016 (clinical underwriting conflict), INJ-017 (unapproved external data), INJ-018 (renewal price walking) | Medium | Defer to a later pass if these surface additional actuarial-model-risk implications | Chief Actuary | Open | Before final submission |
| The deeper fairness-remediation programme for PRC-MOTOR-9/FRD-CLAIM-6 (retraining, feature removal, retirement) is not yet designed | High | Defer to submission/artefacts/18_RESPONSIBLE_AI_FAIRNESS.md; this artefact only records the immediate use restriction | Model Risk Owner | Open | Before template 18 is drafted |