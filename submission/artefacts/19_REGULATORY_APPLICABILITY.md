# 19 Regulatory Applicability

## Purpose

Entity/product/workflow applicability across insurance, AI, privacy, resilience and conduct regulation, building the applicability matrix required by case/REGULATORY_BOUNDARY_PACK.md that distinguishes legal requirement, supervisory expectation, internal policy and design choice.

## Acceptance criteria

- The artefact is evidence-led and references supplied paths, record locators and inject IDs.
- Facts, assumptions, inference, conflict, decision and residual risk are distinguishable.
- Temporal, jurisdictional, authorization and authority boundaries are explicit where relevant.
- Owners, approvals, review triggers and measurable acceptance gates are named.
- The artefact contains no unsupported coverage, pricing, reserve, payment or treaty conclusion.

## Artefact-specific acceptance criteria

- Every one of the nine regulatory sources in sources/SOURCE_VERIFICATION.csv is classified as legal requirement, supervisory expectation, internal policy or design choice for each entity/jurisdiction it may apply to; none is left unclassified (CTRL-RA-01).
- No row asserts a definitive legal conclusion; every row names a qualified interpretation owner per case/REGULATORY_BOUNDARY_PACK.md's explicit requirement (CTRL-RA-02).
- Every source's applicability is scoped to a specific workflow (A/B/C) or explicitly marked cross-cutting; none is asserted as blanket-applicable without workflow scoping (CTRL-RA-03).
- Uncertainty is explicitly documented for every source where AMR's exact regulatory status (e.g., EU AI Act high-risk classification) cannot be determined from supplied evidence alone (CTRL-RA-04).

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| EVID-088 | case/REGULATORY_BOUNDARY_PACK.md | approved/case-pack | 2026-08-01 | MULTI | Research anchors, not legal conclusions; requires an applicability matrix distinguishing legal requirement, supervisory expectation, internal policy and design choice — primary source for this artefact's structure. |
| EVID-089 | sources/SOURCE_VERIFICATION.csv (source_id=SRC-01..SRC-09) | official | 2026-08-01 | global | Verification status and check date for all nine regulatory source anchors; all nine confirmed status=official as of 2026-08-01. |
| EVID-090 | sources/01_IAIS_AI_SUPERVISION.md (SRC-01) | official/research_anchor | 2026-08-01 | global | IAIS Application Paper on supervision of AI; supervisory-expectation-level source, not binding law in any single jurisdiction. |
| EVID-091 | sources/02_EIOPA_AI_OPINION.md (SRC-02) | official/research_anchor | 2026-08-01 | EU | EIOPA Opinion on AI governance and risk management; supervisory-expectation-level source for EU insurance entities. |
| EVID-092 | sources/03_NAIC_AI_MODEL_BULLETIN.md (SRC-03) | official/research_anchor | 2026-08-01 | US | NAIC Model Bulletin on AI Systems; a model bulletin requiring state-by-state adoption analysis, not automatically binding in every US state. |
| EVID-093 | sources/04_IRDAI_CYBER_GUIDELINES.md (SRC-04) | official_portal/research_anchor | 2026-08-01 | IN | IRDAI Information and Cyber Security Guidelines 2023; binding regulatory requirement for AMR's India operations (PolicyCore-IN, per case/SOURCE_SYSTEM_FACT_PACK.md). |
| EVID-094 | sources/05_FCA_PRICING_PRACTICES.md (SRC-05) | official/research_anchor | 2026-08-01 | UK | FCA PS21/11 General insurance pricing practices; directly relevant to protected-proxy pricing (INJ-013) and renewal price walking (INJ-018) if AMR has UK retail business. |
| EVID-095 | sources/06_EU_AI_ACT.md (SRC-06) | official/research_anchor | 2026-08-01 | EU | EU AI Act applicability and high-risk analysis; classification of AMR's AI systems as high-risk is not determinable from supplied evidence alone. |
| EVID-096 | sources/07_DORA.md (SRC-07) | official/research_anchor | 2026-08-01 | EU | Digital Operational Resilience Regulation; applies to EU financial entities and ICT dependencies, cross-referenced to vendor-outage resilience (INJ-035). |
| EVID-097 | sources/08_SOLVENCY_II.md (SRC-08) | official/research_anchor | 2026-08-01 | EU | Solvency II capital/reserving governance; relevant to reserve model drift (INJ-055) for AMR's EU-regulated entities. |
| EVID-041 | case/SOURCE_SYSTEM_FACT_PACK.md | approved/case-pack | 2026-08-01 | MULTI | Reused from 06/10/12/17; confirms AMR operates PolicyCore-IN (India), among other jurisdiction-specific systems, directly scoping which sources apply to which entity. |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | None of the nine regulatory sources is treated as a definitive legal conclusion for AMR; every applicability determination in this artefact is a working hypothesis requiring qualified legal/regulatory-affairs sign-off before being relied upon operationally, per case/REGULATORY_BOUNDARY_PACK.md's explicit instruction. | case/REGULATORY_BOUNDARY_PACK.md (EVID-088); PACKAGE_SCOPE_AND_ASSUMPTIONS.md ("not a legal interpretation service") | Treating any row as a final legal determination would exceed this package's declared scope and could mislead a reviewer into thinking regulatory compliance has been assessed, when it has not. | Legal, Group CEO | Ongoing — every row requires qualified sign-off before operational reliance |
| A-02 | AMR's exact entity structure and licensing footprint per jurisdiction (which legal entity is licensed where, under which regulator) is not fully enumerated in supplied evidence beyond case/INTEGRATED_CASE.md's six-jurisdiction statement (India, Germany, UK, US, Singapore, UAE) and data/legal_entities.csv's mutual-vs-subsidiary split; applicability rows below are scoped at the jurisdiction level, not the precise legal-entity level, until that gap is closed. | case/INTEGRATED_CASE.md Section 1; data/legal_entities.csv (reused from 01/03) | A jurisdiction-level applicability statement could be imprecise if a specific AMR legal entity is not actually licensed or regulated in that jurisdiction for the product line in question. | Legal, Data Governance Owner | Before any jurisdiction-specific compliance claim is operationalised |
| A-03 | The EU AI Act's high-risk classification for AMR's specific AI systems (Workflow A/B/C) cannot be determined from supplied evidence alone; whether an insurance-pricing or claims-evidence system meets the Act's Annex III high-risk criteria requires a fact-specific legal assessment beyond this package's scope. | sources/06_EU_AI_ACT.md (EVID-095) | Asserting a high-risk (or not-high-risk) classification without that assessment would be exactly the kind of unsupported regulatory conclusion this package prohibits. | Legal | Before any EU deployment of Workflow A/B/C |
| A-04 | Sources with a "Model Bulletin" or "Opinion" character (NAIC SRC-03, EIOPA SRC-02, IAIS SRC-01) are supervisory-expectation-level, not automatically binding law, and require jurisdiction-specific adoption analysis (e.g., which US states have adopted the NAIC bulletin) before being treated as a compliance requirement rather than a expectation to consider. | sources/03_NAIC_AI_MODEL_BULLETIN.md (EVID-092); sources/02_EIOPA_AI_OPINION.md (EVID-091); sources/01_IAIS_AI_SUPERVISION.md (EVID-090) | Treating a non-binding opinion/bulletin as binding law would overstate AMR's actual legal obligation, while ignoring it entirely would understate the supervisory expectation it represents. | Legal | Ongoing |

## Required analysis and decisions

| Source | Entity/jurisdiction | Workflow | Requirement type | Evidence | Interpretation owner |
|---|---|---|---|---|---|
| IAIS Application Paper on AI supervision (SRC-01) | AMR Group (all jurisdictions, as an internationally active insurer) | Cross-cutting (A/B/C) | Supervisory expectation | sources/01_IAIS_AI_SUPERVISION.md (EVID-090) | Legal / Group Chief Risk Officer |
| EIOPA Opinion on AI governance (SRC-02) | AMR's EU-regulated entities (Germany, per case/INTEGRATED_CASE.md Section 1) | Cross-cutting (A/B/C) | Supervisory expectation | sources/02_EIOPA_AI_OPINION.md (EVID-091) | Legal (EU) |
| NAIC AI Model Bulletin (SRC-03) | AMR's US-regulated entities (per case/INTEGRATED_CASE.md Section 1) | Workflow B (underwriting/pricing) primarily; cross-cutting secondarily | Supervisory expectation, pending state-by-state adoption analysis (A-04) | sources/03_NAIC_AI_MODEL_BULLETIN.md (EVID-092) | Legal (US) |
| IRDAI Information and Cyber Security Guidelines 2023 (SRC-04) | AMR India (PolicyCore-IN and related India operations, per case/SOURCE_SYSTEM_FACT_PACK.md) | Cross-cutting (A/B/C), given cyber-security scope | Legal requirement for India operations | sources/04_IRDAI_CYBER_GUIDELINES.md (EVID-093); case/SOURCE_SYSTEM_FACT_PACK.md (EVID-041) | CISO, Legal (India) |
| FCA PS21/11 general insurance pricing practices (SRC-05) | AMR's UK-regulated entities, if any retail UK business exists (not confirmed in supplied evidence beyond the six-jurisdiction list) | Workflow B (underwriting/pricing) | Legal requirement if UK retail business is confirmed; otherwise not applicable | sources/05_FCA_PRICING_PRACTICES.md (EVID-094); cross-referenced to INJ-013 (protected-proxy pricing) and INJ-018 (renewal price walking) | Legal (UK) |
| EU AI Act (SRC-06) | AMR's EU-regulated entities (Germany) | Cross-cutting (A/B/C), pending high-risk classification (A-03) | Legal requirement if high-risk classification applies; uncertain pending fact-specific assessment | sources/06_EU_AI_ACT.md (EVID-095) | Legal (EU) |
| Digital Operational Resilience Regulation (SRC-07) | AMR's EU financial entities and their ICT third-party dependencies (e.g., CatVision, ReSure per case/SOURCE_SYSTEM_FACT_PACK.md, if EU-domiciled) | Workflow C (catastrophe/reinsurance), given ICT-dependency and vendor-outage scope (INJ-035) | Legal requirement for EU financial entities; ICT-dependency scope depends on vendor domicile, not yet confirmed | sources/07_DORA.md (EVID-096) | Legal (EU), CISO |
| Solvency II (SRC-08) | AMR's EU-regulated (re)insurance entities | Workflow C (reserve/capital-adjacent evidence preparation, never a reserve decision itself per CTRL-ICB-04) | Legal requirement for EU (re)insurance entities; cross-referenced to reserve model drift (INJ-055) | sources/08_SOLVENCY_II.md (EVID-097) | Chief Actuary, Legal (EU) |
| ISO/IEC 42001:2023 AI management systems (SRC-09) | AMR Group-wide (voluntary management-system standard, not jurisdiction-bound) | Cross-cutting (A/B/C) | Internal policy / design choice (voluntary standard, not a legal requirement) | sources/09_ISO_IEC_42001.md; primary source for submission/artefacts/20_ISO42001_GOVERNANCE.md | AI Product Owner |

## Alternatives and trade-offs

| Option | Benefits | Risks | Cost/complexity | Reversibility | Decision and rationale |
|---|---|---|---|---|---|
| Assert a single blanket "AMR is subject to all nine sources globally" statement for simplicity | Simplest to write | Directly contradicts case/REGULATORY_BOUNDARY_PACK.md's explicit instruction to determine applicability "by entity, jurisdiction, product, workflow and intended purpose"; e.g., IRDAI clearly does not apply to AMR's Germany operations | Lowest documentation cost, highest risk of an obviously wrong applicability claim under panel challenge | Reversible but embarrassing if challenged | Rejected. Fails CTRL-RA-01 and CTRL-RA-03's workflow/jurisdiction-scoping requirement outright. |
| Treat every source as a binding legal requirement regardless of its actual character (opinion, model bulletin, voluntary standard) | Appears maximally cautious | Overstates AMR's actual legal obligations (e.g., ISO 42001 is voluntary, NAIC's bulletin requires state adoption analysis); could mislead a reviewer into thinking a compliance assessment has been performed when it has not | Lower analytical effort, high risk of a false compliance claim | Reversible but undermines the credibility of every other applicability statement in this artefact | Rejected. A-01 and A-04 require distinguishing legal requirement from supervisory expectation, internal policy and design choice, exactly as case/REGULATORY_BOUNDARY_PACK.md demands. |
| Per-source entity/jurisdiction/workflow scoping with explicit requirement-type classification (legal requirement / supervisory expectation / internal policy / design choice) and a named interpretation owner per row, with uncertainty explicitly flagged where classification cannot be determined from supplied evidence (e.g., EU AI Act high-risk status) | Directly satisfies case/REGULATORY_BOUNDARY_PACK.md's required output; distinguishes fact from inference from open question, consistent with every prior artefact's evidence discipline | Nine rows to maintain; several rows depend on facts not confirmed in supplied evidence (e.g., whether AMR has UK retail business, EU-domiciled vendors) | Medium — nine sources, each independently scoped | Reversible; classification can be refined as more facts become available | Selected. Matches the case pack's explicit required output and the package's "not a legal interpretation service" scope boundary (PACKAGE_SCOPE_AND_ASSUMPTIONS.md). |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-RA-01 | Every one of the nine sources is classified by requirement type for each applicable entity/jurisdiction | Review of the Required analysis and decisions table for completeness | All nine sources have a stated requirement type (legal requirement / supervisory expectation / internal policy / design choice) | This artefact, Required analysis and decisions table | Legal |
| CTRL-RA-02 | No row asserts a definitive legal conclusion without a qualified interpretation owner | Review of the Interpretation owner column | Every row names a specific role (Legal, CISO, Chief Actuary, etc.), never left blank or generic | This artefact, Required analysis and decisions table | AI Product Owner |
| CTRL-RA-03 | Every source's applicability is scoped to a workflow or explicitly cross-cutting | Review of the Workflow column | No row is unscoped; each states A, B, C, or "cross-cutting" with a stated reason | This artefact, Required analysis and decisions table | AI Product Owner |
| CTRL-RA-04 | Uncertainty is documented where classification cannot be determined | Review of rows referencing A-02/A-03/A-04 | EU AI Act high-risk status, UK retail-business confirmation, and NAIC state-adoption status are each explicitly flagged as uncertain, not asserted | This artefact, Working assumptions and Required analysis tables | Legal |

## Traceability

| Inject/requirement | Architecture/ADR | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| INJ-013 (protected-proxy pricing), INJ-018 (renewal price walking) | Cross-referenced to 15_ACTUARIAL_MODEL_RISK.md and 18_RESPONSIBLE_AI_FAIRNESS.md | FCA-pricing-practices compliance check (not yet implemented; depends on UK-retail-business confirmation) | Not yet defined | Whether AMR has UK retail business subject to FCA PS21/11 is not confirmed in supplied evidence. |
| INJ-035 (catastrophe vendor outage) | Cross-referenced to 10_C4_ARCHITECTURE.md's CatVision failure mode | DORA-adjacent ICT-dependency resilience check (not yet implemented; depends on vendor EU domicile) | Not yet defined | Vendor domicile for CatVision/ReSure not confirmed in supplied evidence. |
| INJ-055 (reserve model drift) | Cross-referenced to 14_INSURANCE_CONTROL_BOUNDARIES.md's reserve-authority row | Solvency II-adjacent reserve-governance check (not yet implemented) | Not yet defined | Full Solvency II applicability depends on confirming which AMR entities are EU-regulated (re)insurers. |
| Confirmed fairness breaches (15/18) | Cross-referenced to sources/03_NAIC_AI_MODEL_BULLETIN.md and sources/05_FCA_PRICING_PRACTICES.md | Model-use restriction (15) and remediation pathway (18) | Not yet defined | If AMR's US/UK entities are confirmed subject to NAIC/FCA, the confirmed breaches become a regulatory-adjacent exposure, not only an internal-governance one. |
| INJ-005 (prohibited autonomy) | Cross-referenced to ADR-03/04/12 (11_ADR_REGISTER.md) | N/A — governance principle reinforced by IAIS/EIOPA supervisory expectations | N/A | Supervisory expectations reinforce but do not replace the board-level prohibition already enforced structurally. |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| AMR's precise legal-entity-to-jurisdiction-to-regulator mapping is not fully enumerated in supplied evidence (A-02) | High | Escalate to Legal to obtain the actual entity/licensing structure before any applicability row is operationalised | Legal | Open | Before any jurisdiction-specific compliance claim is relied upon |
| EU AI Act high-risk classification for Workflow A/B/C is undetermined (A-03) | High | Escalate to Legal for a fact-specific assessment; this artefact does not and cannot resolve this question | Legal | Open | Before any EU deployment |
| UK retail-business existence (affecting FCA PS21/11 applicability) is not confirmed | Medium | Escalate to Legal/Group CEO to confirm AMR's UK business scope | Legal | Open | Before any UK-specific compliance claim |
| This artefact does not assert, and must not be read as asserting, that AMR is or is not compliant with any of the nine sources; it only builds the applicability-classification structure case/REGULATORY_BOUNDARY_PACK.md requires | High (framing risk) | Explicit disclaimer recorded here and in A-01; any reader treating this as a compliance certification is misreading its scope | Legal, Group CEO | Open — permanent framing caveat | N/A |