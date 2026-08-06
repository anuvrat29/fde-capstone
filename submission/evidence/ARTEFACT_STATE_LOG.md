# Artefact-by-Artefact State Log

## Purpose

Records the state of the submission after each artefact was completed: what existed before, what was added, what evidence/defects it consumed, what remained open, and what validation was run. This is the step-by-step audit trail requested in addition to the evidence manifest and traceability CSVs.

Baseline before any artefact work: see [PREFLIGHT.md](PREFLIGHT.md) (preflight PASS, `submission/` contained only `.gitkeep` placeholders) and [CASE_BASELINE.md](CASE_BASELINE.md) (case facts as read).

---

## Step 1 — 01_BUSINESS_CASE.md

- **State before:** No submission artefacts existed. Case baseline and preflight evidence available (see above).
- **Action:** Drafted business case using INJ-001 (board catastrophe target), INJ-002 (no-AI challenge), INJ-003 (mutual vs shareholder tension), INJ-004 (acquisition integration), INJ-006 (value leakage).
- **Evidence consumed:** EVID-001, EVID-002, EVID-003, EVID-004, EVID-005, EVID-006, EVID-010, EVID-011.
- **Defects referenced:** None new; relied on case baseline only.
- **State after:** Business case exists with 5 open issues (unquantified board target, unquantified no-AI comparator, unresolved mutual/shareholder allocation, incomplete cost model, acquisition identifier fragmentation flagged for later resolution). No implementation, no numeric benefit claimed as achieved.
- **Validation run:** None yet (validation deferred to end of batch, see Step 8 below).

## Step 2 — 02_DMAIC_WORKBOOK.md

- **State before:** 01_BUSINESS_CASE.md complete; its open issues (no baseline, no no-AI comparator) carried forward as the Define-phase input.
- **Action:** Drafted DMAIC workbook analysing INJ-001/INJ-002 as Define/Measure inputs, and used INJ-008 (endorsement timing) and INJ-010 (billing/cancellation race) as concrete root-cause candidates for cycle-time variability.
- **Evidence consumed:** EVID-001, EVID-003, EVID-004, EVID-014, EVID-017.
- **Defects referenced:** DEF-003 (endorsement issued after loss window).
- **State after:** DMAIC workbook exists recording that no quantified baseline currently exists (A-02) and that a no-AI comparator experiment has not been executed — both explicitly flagged as pre-conditions before any improvement percentage may be published (CTRL-DMAIC-01/03).
- **Validation run:** None yet.

## Step 3 — 03_STAKEHOLDER_DECISION_RIGHTS.md

- **State before:** Business case and DMAIC workbook complete; decision-rights gaps referenced in both (e.g., who approves benefit reporting) were still unresolved.
- **Action:** Drafted stakeholder/decision-rights artefact using case/STAKEHOLDER_PACK.md's 12 stakeholders, plus INJ-003, INJ-004, INJ-005 (prohibited autonomy), INJ-009 (binder authority ambiguity), INJ-020 (underwriter override opacity).
- **Evidence consumed:** EVID-005, EVID-006, EVID-007, EVID-008, EVID-009, EVID-015, EVID-016, EVID-022, EVID-023, EVID-025.
- **Defects referenced:** DEF-011 (override concentration, evidence-envelope granularity only), DEF-012 (delegated authority limit not independently reconciled).
- **State after:** RACI/escalation structure defined; explicit decision recorded that no workflow output may be a binding/pricing/reserve/settlement/payment/cancellation/treaty action (CTRL-SDR-01), and that authority-exceedance evidence must be flagged to a named human, never auto-corrected (CTRL-SDR-02). Two open issues carried forward: no remediation owner yet named for the binder-authority breach pattern, and override-pattern detection has no implementation.
- **Validation run:** None yet.

## Step 4 — 04_PRODUCT_SERVICE_BLUEPRINT.md

- **State before:** Decision-rights structure defined; persona/workflow boundaries not yet formally documented.
- **Action:** Drafted persona/job/blueprint artefact defining one primary human-approver persona per workflow (Claims Handler for A, Underwriter for B, Catastrophe Response Lead/Reinsurance Director for C), enforcing INJ-005's full prohibited-action list per workflow, and explicitly addressing the prompt-injection risk named by DEF-009.
- **Evidence consumed:** EVID-008, EVID-024, EVID-025.
- **Defects referenced:** DEF-009 (knowledge/MALICIOUS_ADJUSTER_REPORT.md flagged by baseline diagnostic as containing prompt-like instructions).
- **State after:** Three workflow personas and their prohibited-action boundaries are documented; a specific control (CTRL-PSB-04) is defined requiring a negative test against the malicious-adjuster document before any evidence-ingestion pipeline is connected. No code exists yet to enforce any of the four CTRL-PSB controls — recorded as high-severity open issues.
- **Validation run:** None yet.

## Step 5 — 05_DDD_CONTEXT_MAP.md

- **State before:** Workflow/persona boundaries defined; no domain model yet existed to back Workflow A's evidence-reconciliation logic.
- **Action:** Drafted DDD context map defining Wording Version, Endorsement, Loss Event, Claim and Group Policy/Certificate as distinct bounded-context aggregates, directly modelling INJ-007, INJ-008, INJ-011, INJ-021.
- **Evidence consumed:** EVID-012, EVID-013, EVID-014, EVID-018, EVID-019, EVID-027, EVID-028.
- **Defects referenced:** DEF-002 (three concurrent HPP wordings), DEF-003 (endorsement timing), DEF-005 (LOSS-NILA-01 linked to two claims).
- **State after:** Explicit modelling decision recorded that Loss Event and Claim are many-to-many, not 1:1 (A-04) — directly preventing an automatic duplicate/fraud judgement. Ownership conflicts flagged for Policy Administration (PolicyCore-IN vs DocVault) and Group Benefits (master policy vs certificate) with no resolution rule yet supplied.
- **Validation run:** None yet.

## Step 6 — 06_DATA_GOVERNANCE_LINEAGE.md

- **State before:** Domain model defined; authority/lineage rules referenced only informally in prior artefacts (e.g., "PolicyCore-IN not authoritative for scanned endorsements").
- **Action:** Drafted data governance artefact directly executing/re-confirming `starter/baseline_diagnostics.py` findings and combining them with case/SOURCE_SYSTEM_FACT_PACK.md's 12-system authority caveats and INJ-004, INJ-010, INJ-030.
- **Evidence consumed:** EVID-007, EVID-017; direct diagnostic re-execution (see PREFLIGHT.md); metadata/DATASET_CATALOG.csv and metadata/RELATIONSHIP_RULES.csv referenced for hash/relationship verification.
- **Defects referenced:** DEF-006 (mixed currencies), DEF-007 (stale auth cache), DEF-008 (model artefact/registry mismatch), DEF-010 (address/geocode fragmentation).
- **State after:** Four concrete runtime controls defined (CTRL-DGL-01 through 04) covering authorization re-check, currency non-aggregation, model-artefact verification and provisional-labelling of accumulation outputs. All four are still unimplemented — recorded as high-severity open issues requiring resolution before any workflow reaches a user-facing pilot.
- **Validation run:** None yet.

## Step 7 — 07_ONTOLOGY_SEMANTIC_LAYER.md

- **State before:** Data governance/authority rules defined; domain model (Step 5) existed but lacked a unifying semantic/temporal definition layer.
- **Action:** Drafted ontology defining Wording Version, Endorsement, Loss Event, Claim and Parametric Trigger with explicit authority_status and temporal-fact properties, directly resolving the terminology ambiguity behind INJ-007, INJ-008, INJ-012, INJ-021, INJ-022.
- **Evidence consumed:** EVID-012, EVID-020, EVID-024, EVID-027, EVID-028; knowledge/PARAMETRIC_TRIGGER_AUTHORITY.md.
- **Defects referenced:** DEF-002, DEF-003, DEF-004 (disputed 35-minute window), DEF-005.
- **State after:** Semantic layer defines 5 core concepts with explicit identifier, temporal rule and jurisdiction rule columns. A transcription error in the "Alternatives and trade-offs" table separator (`---ifiable-`) was introduced during drafting and corrected via `replace_string_in_file` before this artefact was finalised. Ontology explicitly scoped to only the concepts evidenced in this pass; coverage/exclusion/party/treaty/model concepts deferred.
- **Validation run:** `get_errors` not applicable (Markdown); table syntax corrected manually.

## Step 8 — Evidence manifests and validation

- **State before:** 7 artefacts complete; no machine-readable evidence index existed yet.
- **Action:** Built `evidence_manifest.csv` (28 rows) and `inject_traceability.csv` (22 injects, INJ-001–INJ-022) cross-referencing every artefact back to a source path, record locator and SHA-256 hash.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS**.
- **State after this step:** `submission/artefacts/` contains 7 of 32 required templates. `submission/evidence/` contains `evidence_manifest.csv`, `inject_traceability.csv`, `PREFLIGHT.md`, `DEFECTS.md`, `CASE_BASELINE.md`, this file. No `submission/src`, `submission/tests`, `submission/app`, or final-mode manifests exist yet.

## Interim review — post-Step 8 hardening (before Step 9)

- **State before:** 7 artefacts complete per Step 8; two evidence-manifest rows (EVID-011, EVID-022) had blank SHA-256 hashes, and every artefact carried only the shared five-bullet acceptance criteria with no artefact-specific, measurable bar.
- **Action:** Computed and filled the two missing hashes directly from the source CSVs (`Get-FileHash -Algorithm SHA256`); added an "Artefact-specific acceptance criteria" section (3–4 measurable, control-ID-linked bullets) to each of artefacts 01–07.
- **Evidence consumed:** data/staff_rates.csv, data/underwriting_decisions.csv (direct hash computation only, no new inject evidence).
- **State after:** `evidence_manifest.csv` has no blank hash fields across EVID-001–EVID-028. Every artefact 01–07 now states its own measurable pass/fail bar in addition to the shared boilerplate criteria.
- **Validation run:** Manual review only; `check_submission.py` not re-run (no structural change to artefact count or evidence schema).

## Step 9 — 08_KNOWLEDGE_GRAPH_DECISION.md

- **State before:** 7 artefacts complete; ontology (07) defined core entities but no decision existed on whether a knowledge graph was needed on top of the relational/ontology model. INJ-045 (fraud-ring graph ambiguity) and INJ-070 (graph overreach) were undocumented; INJ-021 was only partially addressed from the claims/loss-event angle in 05/07.
- **Action:** Drafted the knowledge-graph decision artefact, testing four candidate questions (fraud-ring linkage INJ-045, provider-identity resolution INJ-037, repair-network similarity INJ-023, and the INJ-070 overreach test itself) against a variable-hop-traversal qualification rule (A-01). Treated `knowledge/RESEARCH_NOTE_GRAPH_EVERYTHING.md` (a planted "build a graph for everything" research note) as non-controlling draft data per its own document-control block, consistent with the embedded-instructions-are-data principle already established in 04_PRODUCT_SERVICE_BLUEPRINT.md.
- **Evidence consumed:** EVID-029 (fraud_links.csv), EVID-030 (claimant_identities.csv), EVID-031 (repair_estimates.csv), EVID-032 (providers.csv), EVID-033 (provider_aliases.csv), EVID-034 (graph_candidate_questions.csv), EVID-003 (no_ai_baselines.csv, shared), EVID-035 (RESEARCH_NOTE_GRAPH_EVERYTHING.md). All six new evidence rows added to `evidence_manifest.csv` with freshly computed SHA-256 hashes.
- **Defects referenced:** DEF-013 (graph-everything research note is draft/non-controlling, new), DEF-014 (provider alias reuse, evidence-envelope granularity only, new).
- **Decision recorded:** Only the fraud-ring candidate question (INJ-045) qualifies for a graph; provider-identity (INJ-037) and repair-network (INJ-023) candidate questions are rejected for graph treatment in favour of relational/analytics alternatives — directly satisfying the INJ-070 graph-overreach test with a defensible rejection rationale for each declined case (CTRL-KGD-04).
- **State after:** `submission/artefacts/` contains 8 of 32 required templates. Graph scope is bounded to shared-device/address/repairer fraud-ring evidence surfacing only, with output restricted to human-reviewable linked evidence, never an automated fraud/sanctions/identity conclusion (CTRL-KGD-03, non-compensable gate 1). `inject_traceability.csv` updated: INJ-045 now `addressed`; INJ-023, INJ-037, INJ-047 now `partially-addressed` (candidate-question level only, no confirmed finding). `evidence_manifest.csv` grew from 28 to 34 rows.
- **Validation run:** Hashes for all six new evidence files computed and verified at 64 hex characters via `Get-FileHash -Algorithm SHA256`; `python tools/check_submission.py` not yet re-run for this step (pending confirmation of intent to proceed to Step 10).

## Step 10 — 09_REQUIREMENTS_TRACEABILITY.md

- **State before:** 8 artefacts complete (01–08), each with its own internal "Traceability" table pointing forward to future templates, but no single index existed cross-referencing every CTRL-* control, every mandatory operating property from case/INTEGRATED_CASE.md Section 5, and every scoring dimension in requirements/SCORING_RUBRIC.csv.
- **Action:** Built a consolidated requirement-ID scheme without renaming any existing control: REQ-F-01/02/03 for the three workflow functional mandates (case/INTEGRATED_CASE.md Section 4); REQ-NF-01 through REQ-NF-18 for the 18 mandatory operating properties (Section 5), enumerated for the first time in this pass; REQ-C-01 through REQ-C-21, one per existing CTRL-* control found across artefacts 01–08 by direct search. Mapped every requirement to a requirements/SCORING_RUBRIC.csv dimension.
- **Evidence consumed (as originally drafted, later corrected — see Interim correction below):** case/INTEGRATED_CASE.md Sections 4–5, requirements/SCORING_MODEL.md, requirements/SCORING_RUBRIC.csv, and the eight completed artefacts. The initial draft incorrectly cited three of these documents with a placeholder `—` in the Scope and evidence register instead of a real Evidence ID, even though one (requirements/SCORING_MODEL.md) already had an assigned ID (EVID-026) from artefact 03 and the other two had never been hashed.
- **Defects referenced:** None new; surfaced a coverage gap (see below) rather than a data defect.
- **Key finding:** Of the 18 Section-5 operating properties, 9 (REQ-NF-02 through REQ-NF-07, REQ-NF-09) already have at least one CTRL-* control from artefacts 01–08; 9 (REQ-NF-01, REQ-NF-08, REQ-NF-10 through REQ-NF-18) have no assigned control and are recorded as "documented, not yet controlled". This is the first explicit confirmation that purpose limitation (as a standalone control), abstention, contestability, idempotency, bounded steps, token/cost budgets, checkpointing, rollback, kill switch, degraded mode and full auditability remain undesigned.
- **State after (as originally drafted):** `submission/artefacts/` contains 9 of 32 required templates. A single requirements index now exists that a panel can use to jump from any REQ-* ID to its originating inject, control and artefact.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS** (re-run after this step).

## Interim correction — missing evidence IDs in 09_REQUIREMENTS_TRACEABILITY.md (post-Step 10)

- **State before:** Step 10 as drafted above used `—` (the "no single hashable locator" placeholder) for three document-level evidence rows in 09_REQUIREMENTS_TRACEABILITY.md's Scope and evidence register: `case/INTEGRATED_CASE.md` (cited twice, Sections 4 and 5), `requirements/SCORING_MODEL.md`, and `requirements/SCORING_RUBRIC.csv`. This was inconsistent with the manifest discipline established from Step 1 onward: `requirements/SCORING_MODEL.md` already had an assigned Evidence ID (EVID-026, from 03_STAKEHOLDER_DECISION_RIGHTS.md), and `case/INTEGRATED_CASE.md` / `requirements/SCORING_RUBRIC.csv` had never been hashed at all despite being cited as load-bearing evidence for real decisions (the same standard applied to `case/STAKEHOLDER_PACK.md` and `case/SOURCE_SYSTEM_FACT_PACK.md` in artefacts 03 and 06).
- **How found:** User inspection of the completed artefact directly questioned the missing Evidence ID column values.
- **Action:** Computed SHA-256 hashes for `case/INTEGRATED_CASE.md` and `requirements/SCORING_RUBRIC.csv` via `Get-FileHash -Algorithm SHA256`; added them to `evidence_manifest.csv` as EVID-036 and EVID-037 respectively; updated 09_REQUIREMENTS_TRACEABILITY.md's Scope and evidence register to cite EVID-026 (reused, not duplicated), EVID-036 and EVID-037 in place of `—`. The one remaining `—` row (the reference spanning all eight prior artefacts 01–08 collectively, with no single file locator) was left as `—` by design, consistent with the manifest's existing convention for multi-file references.
- **Evidence consumed:** EVID-026 (requirements/SCORING_MODEL.md, reused); EVID-036 (case/INTEGRATED_CASE.md, new); EVID-037 (requirements/SCORING_RUBRIC.csv, new).
- **Defects referenced:** None — this was a participant drafting inconsistency, not a package defect; recorded here rather than in DEFECTS.md because DEFECTS.md is reserved for defects in the supplied package/data, not in participant-authored artefacts.
- **State after:** `evidence_manifest.csv` grew from 34 to 36 rows (EVID-001–EVID-037, accounting for the gap where EVID-036/EVID-037 were appended after EVID-035). No artefact row in 09_REQUIREMENTS_TRACEABILITY.md's evidence register now uses `—` where a real, hashable, single-file source exists.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS** (re-run after the correction).

## Interim correction — workspace-wide sweep for missing evidence IDs (post-Step 10, second pass)

- **State before:** The first interim correction (above) fixed only 09_REQUIREMENTS_TRACEABILITY.md. A full `grep_search` across all completed artefacts for the placeholder pattern `| — |` at the start of an evidence-register row found 14 total matches spanning five artefacts: 03_STAKEHOLDER_DECISION_RIGHTS.md (1), 04_PRODUCT_SERVICE_BLUEPRINT.md (1), 06_DATA_GOVERNANCE_LINEAGE.md (5), 07_ONTOLOGY_SEMANTIC_LAYER.md (2), 08_KNOWLEDGE_GRAPH_DECISION.md (3), and 09_REQUIREMENTS_TRACEABILITY.md (1, already corrected and confirmed intentional). Several of the uncorrected rows cited files that had already been hashed and assigned an Evidence ID elsewhere (e.g., `knowledge/RESEARCH_NOTE_GRAPH_EVERYTHING.md` already existed as EVID-035; `case/INTEGRATED_CASE.md` already existed as EVID-036; `metadata/RELATIONSHIP_RULES.csv` was cited with `—` in both 06 and 08 and needed one shared ID, not two).
- **How found:** User instruction to check all artefacts for missing evidence IDs, following on from the first interim correction.
- **Action:** Computed SHA-256 hashes for nine previously unhashed files (`metadata/RELATIONSHIP_RULES.csv`, `knowledge/PARAMETRIC_TRIGGER_AUTHORITY.md`, `data/timezone_rules.csv`, `case/SOURCE_SYSTEM_FACT_PACK.md`, `metadata/DATASET_CATALOG.csv`, `data/addresses.csv`, `data/geocodes.csv`, `starter/baseline_diagnostics.py`, `case/STAKEHOLDER_PACK.md`) plus one participant-authored artefact (`submission/artefacts/07_ONTOLOGY_SEMANTIC_LAYER.md`, cited as a cross-artefact evidence source in 08). Added ten new rows to `evidence_manifest.csv` as EVID-038 through EVID-047. Updated all five artefacts to replace every `—` placeholder with the correct Evidence ID, reusing EVID-035/EVID-036/EVID-038 where a row cited a file already hashed elsewhere rather than creating duplicate IDs.
- **Evidence consumed:** EVID-038 (metadata/RELATIONSHIP_RULES.csv, new — reused in both 06 and 08); EVID-039 (knowledge/PARAMETRIC_TRIGGER_AUTHORITY.md, new); EVID-040 (data/timezone_rules.csv, new); EVID-041 (case/SOURCE_SYSTEM_FACT_PACK.md, new); EVID-042 (metadata/DATASET_CATALOG.csv, new); EVID-043 (data/addresses.csv, new); EVID-044 (data/geocodes.csv, new); EVID-045 (starter/baseline_diagnostics.py executed output, new); EVID-046 (case/STAKEHOLDER_PACK.md, new); EVID-047 (submission/artefacts/07_ONTOLOGY_SEMANTIC_LAYER.md, new); EVID-035 and EVID-036 (reused, not duplicated).
- **Defects referenced:** None — participant drafting inconsistency, not a package defect; consistent with the previous interim correction's treatment.
- **State after:** `evidence_manifest.csv` grew from 37 to 47 rows (EVID-001–EVID-047). Every evidence-register row across artefacts 01–09 now cites either a real, hashed Evidence ID or an explicitly justified `—` for the single remaining case (a reference spanning eight separate artefact files with no single locator, in 09_REQUIREMENTS_TRACEABILITY.md). `inject_traceability.csv` unchanged — this correction added evidence-manifest rigor, not new inject coverage.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS** (re-run after the correction).

## Step 11 — 10_C4_ARCHITECTURE.md

- **State before:** 9 artefacts complete (01–09). The requirements matrix (09) had identified 9 non-functional requirements with no assigned control and no architectural home. The fraud-ring graph component (08) was qualified in principle but had no Container/Component-level placement. No Context, Container or Component view existed yet for any of the three workflows.
- **Action:** Drafted Context/Container/Component views grounded in case/SOURCE_SYSTEM_FACT_PACK.md's 12 source systems. Placed the fraud-ring graph component (08) as a bounded Workflow A/C-only component per A-04. Placed a current-authorization re-check gate and a model-artefact verification gate as shared Component-level controls, using data/access_cache.csv and data/model_artifacts.csv as concrete illustrative evidence of the confirmed staleness/mismatch defects (DEF-007, DEF-008). Assigned all 9 previously-uncontrolled REQ-NF-* items a named architectural responsibility (CTRL-C4-03), closing the "no home" gap identified in Step 10 without yet closing the "no implementation" gap.
- **Evidence consumed:** EVID-041 (case/SOURCE_SYSTEM_FACT_PACK.md, reused), EVID-036 (case/INTEGRATED_CASE.md Section 4, reused), EVID-007 (data/system_inventory.csv, reused), EVID-045 (starter/baseline_diagnostics.py, reused), EVID-048 (data/access_cache.csv, new), EVID-049 (data/model_artifacts.csv, new).
- **Defects referenced:** DEF-007 and DEF-008 (both previously logged in DEFECTS.md; no new defects, but both given an explicit architectural remediation home for the first time).
- **State after:** `submission/artefacts/` contains 10 of 32 required templates. `evidence_manifest.csv` grew from 47 to 49 rows (EVID-048, EVID-049 added). `inject_traceability.csv` updated: INJ-004 upgraded to reflect architectural extension; INJ-035 (catastrophe vendor outage) newly added as partially-addressed.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS**.

## Step 12 — 11_ADR_REGISTER.md

- **State before:** 10 artefacts complete (01–10). Many meaningful decisions had been made and reasoned through across those artefacts' own "Alternatives and trade-offs" tables, but no consolidated ADR register existed, and DEFINITION_OF_DONE.md requires "at least 12 meaningful ADRs."
- **Action:** Consolidated 13 ADRs (ADR-01 through ADR-13), each citing its originating artefact and reusing that artefact's own rejected-alternative reasoning rather than inventing a new comparison (A-01). Covered business sequencing (ADR-01/02), workflow architecture (ADR-03/04), domain modelling (ADR-05/06/07), data-governance controls (ADR-08/09), the graph decision (ADR-10/11), the system-of-record write boundary (ADR-12), and the NFR-placement decision from Step 11 (ADR-13).
- **Evidence consumed:** No new data/knowledge evidence files — pure consolidation over artefacts 01–10, same pattern as Step 10's treatment of 09_REQUIREMENTS_TRACEABILITY.md. No new EVID-* rows required.
- **Defects referenced:** None new; ADR-08/09 formalise the already-logged DEF-007/DEF-008 as architecture decisions rather than introducing new defects.
- **State after:** `submission/artefacts/` contains 11 of 32 required templates. 13 ADRs recorded, satisfying the 12-ADR minimum with a two-ADR margin. `evidence_manifest.csv` and `inject_traceability.csv` unchanged (no new evidence introduced).
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS**.

## Interim correction — missing evidence ID in 11_ADR_REGISTER.md (post-Step 12)

- **State before:** 11_ADR_REGISTER.md's Scope and evidence register cited `DEFINITION_OF_DONE.md` (the source of the "at least 12 meaningful ADRs" requirement) with a placeholder `—` instead of a real Evidence ID, even though it is a single, real, hashable file — the same class of miss corrected twice already in 09_REQUIREMENTS_TRACEABILITY.md and across artefacts 03/04/06/07/08. 10_C4_ARCHITECTURE.md was also re-checked at the same time; its one remaining `—` row (spanning submission/artefacts/08 and 09 collectively) was confirmed to be a legitimate multi-file reference with no single locator, consistent with the established convention, and left unchanged.
- **How found:** User instruction to re-check templates 10 and 11 specifically for missing evidence IDs, following the two prior interim corrections on template 09.
- **Action:** Computed the SHA-256 hash for `DEFINITION_OF_DONE.md` via `Get-FileHash -Algorithm SHA256`; added it to `evidence_manifest.csv` as EVID-050; updated 11_ADR_REGISTER.md's evidence register to cite EVID-050 in place of `—`. Confirmed via `grep_search` that no other single-file `—` rows remain in either 10_C4_ARCHITECTURE.md or 11_ADR_REGISTER.md.
- **Evidence consumed:** EVID-050 (DEFINITION_OF_DONE.md, new).
- **Defects referenced:** None — participant drafting inconsistency, not a package defect; consistent with the prior two interim corrections' treatment.
- **State after:** `evidence_manifest.csv` grew from 49 to 50 rows (EVID-001–EVID-050). Both 10_C4_ARCHITECTURE.md and 11_ADR_REGISTER.md now cite a real Evidence ID for every single-file source; the only remaining `—` rows in either file are legitimate multi-artefact references with no single locator.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS** (re-run after the correction).

## Step 13 — 12_INTEGRATION_CONTRACTS.md

- **State before:** 11 artefacts complete (01–11). No integration-contract-level treatment existed yet for ACORD mapping loss (INJ-067), bordereaux currency errors (INJ-053), treaty wording ambiguity (INJ-051) or catastrophe event-definition conflict (INJ-052), despite these being explicitly named in case/INTEGRATED_CASE.md's D08/D09 domains.
- **Action:** Drafted five contracts: ACORD claim/policy event mapping, bordereaux ingestion/currency-disaggregation, treaty wording/hours-clause resolution, catastrophe event-identifier cross-reference, and a read contract for the fraud-ring graph component (reusing, not re-specifying, the component from 08/10). Every contract with retry semantics was given a bounded retry count and idempotency key (CTRL-IC-03); every edge touching PayFlow/ClaimSphere/ReSure was confirmed read/propose-only (CTRL-IC-04).
- **Evidence consumed:** EVID-051 (data/acord_messages.csv, new), EVID-052 (data/integration_errors.csv, new), EVID-053 (data/bordereaux.csv, new), EVID-054 (data/reinsurance_treaties.csv, new), EVID-055 (data/treaty_documents.csv, new), EVID-056 (data/reinsurance_events.csv, new), EVID-058 (knowledge/ACORD_INTEGRATION_STANDARD.md, new), EVID-041 (case/SOURCE_SYSTEM_FACT_PACK.md, reused).
- **Defects referenced:** None new; INJ-067/051/052/053 were disclosed-but-unaddressed injects, not confirmed package defects.
- **State after:** `submission/artefacts/` contains 12 of 32 required templates. `evidence_manifest.csv` grew to include EVID-051 through EVID-058 (added together with template 13/14 evidence in this batch — see consolidated count below). `inject_traceability.csv` updated: INJ-067 addressed; INJ-051, INJ-052, INJ-053 partially-addressed.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS**.

## Step 14 — 13_MODEL_PROMPT_LIFECYCLE.md

- **State before:** 12 artefacts complete (01–12). The model-artefact verification gate had an architectural home (10) but no lifecycle-level model-selection, prompt-versioning, budget, or substitution/fallback design existed yet. REQ-NF-12/13 (bounded steps, token/cost budgets) and REQ-NF-16/17 (kill switch, degraded mode) had architectural homes (Step 11) but no governance taxonomy.
- **Action:** Mapped each of the three registered models (data/model_registry.csv) to its permitted workflow and purpose, explicitly flagging GEN-SUM-3's `conditional` approval status as requiring disclosure, not silent treatment as unconditional. Specified a structured-output provenance-citation requirement per knowledge/GENAI_SAFE_SUMMARISATION.md, a budget/stop-reason taxonomy per knowledge/AGENT_BUDGET_STOP_POLICY.md (closing REQ-NF-12/13's taxonomy gap), and a controlled-manual-mode substitution/fallback design per knowledge/AI_DISABLED_CONTINUITY.md (closing REQ-NF-16/17's design gap).
- **Evidence consumed:** EVID-057 (data/model_registry.csv, new), EVID-059 (knowledge/GENAI_SAFE_SUMMARISATION.md, new), EVID-060 (knowledge/AI_DISABLED_CONTINUITY.md, new), EVID-061 (knowledge/AGENT_BUDGET_STOP_POLICY.md, new), EVID-045 and EVID-035 (reused).
- **Defects referenced:** None new; reuses DEF-008 (model artefact/registry mismatch) as the motivating case for the verification-gate lifecycle placement.
- **State after:** `submission/artefacts/` contains 13 of 32 required templates. REQ-NF-12/13/16/17 now have both an architectural home (10) and a governance taxonomy/design (13), though still no implementation.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS**.

## Step 15 — 14_INSURANCE_CONTROL_BOUNDARIES.md

- **State before:** 13 artefacts complete (01–13). The board-level prohibited-action list (INJ-005) was already enforced structurally at the workflow-output-schema level (CTRL-PSB-01/02/03) and the system-of-record-edge level (CTRL-C4-01/ADR-12), but no single artefact consolidated all ten regulated insurance actions (bind, decline, price, reserve, settle, pay, cancel, place treaty, submit recovery, emergency advance) into one per-action authority matrix with evidence and audit-event requirements. Three confirmed/disclosed defects (INJ-027 reserve leakage, INJ-036 emergency payment pressure, INJ-048 insider claim manipulation) had no pattern-specific control yet.
- **Action:** Built a ten-row action-authority matrix, each row naming the AI-permitted preparatory step, explicit prohibition, human authority, evidence required and audit-event reference. Three rows carry an additional pattern-specific control directly closing a confirmed/disclosed defect: the reserve row requires pre/post-value audit logging (closes INJ-027, per A-02); the payment row requires a payee-change-timing trigger for mandatory secondary review (closes INJ-048, per A-04); the hardship-advance row requires explicit incomplete-check disclosure and override justification (addresses INJ-036, per A-03).
- **Evidence consumed:** EVID-062 (knowledge/PAYMENT_CONTROL_POLICY.md, new), EVID-063 (data/emergency_payment_requests.csv, new), EVID-064 (data/claim_reserves.csv, new), EVID-065 (data/payment_changes.csv, new), EVID-066 (data/subrogation_cases.csv, new), EVID-008, EVID-025, EVID-026, EVID-054 (all reused).
- **Defects referenced:** None new; INJ-027, INJ-036, INJ-048, INJ-028, INJ-055 were disclosed-but-unaddressed injects prior to this step.
- **State after:** `submission/artefacts/` contains 14 of 32 required templates. `evidence_manifest.csv` grew from 50 to 66 rows across Steps 13–15 combined (EVID-051 through EVID-066). `inject_traceability.csv` updated: INJ-067 addressed; INJ-027, INJ-028, INJ-036, INJ-048, INJ-051, INJ-052, INJ-053, INJ-055 all newly partially-addressed. Every Evidence ID cited across templates 12–14 was cross-checked against `evidence_manifest.csv` before finalising, and no `—` placeholder remains where a real, hashable single-file source exists in any of the three new artefacts.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS**.

## Step 16 — 15_ACTUARIAL_MODEL_RISK.md

- **State before:** 14 artefacts complete (01–14). data/fairness_metrics.csv and data/model_performance.csv (both real, non-evidence-envelope datasets with concrete subgroup metrics) had not yet been inspected in any prior artefact. No use restriction existed for any model despite two confirmed live subgroup fairness breaches.
- **Action:** Inspected data/fairness_metrics.csv directly and found two confirmed `status=breach` rows (PRC-MOTOR-9 postal_proxy_low_income, FRD-CLAIM-6 Hindi_language) and one `status=review` row (UW-LIFE-4 female_45_60). Recorded an immediate, actuarial-model-risk-specific use restriction for the two confirmed breaches (disclosure required on every output touching the affected subgroup) without waiting for template 18's deeper remediation programme. Also inspected data/model_performance.csv and found confirmed multilingual quality degradation for GEN-SUM-3 (groundedness 0.91 English vs 0.68 Arabic), corroborating INJ-064. Added version-disclosure and uncertainty-disclosure requirements for the catastrophe model-version split (INJ-015) and sparse cyber portfolio (INJ-019) respectively.
- **Evidence consumed:** EVID-067 (data/pricing_factors.csv, new), EVID-068 (data/fairness_metrics.csv, new — confirmed breach data), EVID-069 (data/cat_models.csv, new), EVID-070 (data/exposure_aggregates.csv, new), EVID-071 (data/model_performance.csv, new — confirmed multilingual degradation data), EVID-072 (data/cyber_risks.csv, new), EVID-057 and EVID-025 (reused).
- **Defects referenced:** None new; this step treats data/fairness_metrics.csv's confirmed breach rows as live governance findings, distinct from the four starter/baseline_diagnostics.py-seeded defects (DEF-002 through DEF-012).
- **State after:** `submission/artefacts/` contains 15 of 32 required templates. `inject_traceability.csv` updated: INJ-013, INJ-015, INJ-019 upgraded from not-yet-addressed to addressed; INJ-064 newly partially-addressed. The two stale not-yet-addressed rows for INJ-013/015/019 (originally logged in Step 8) were removed rather than duplicated.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS**.

## Step 17 — 16_THREAT_ABUSE_MODEL.md

- **State before:** 15 artefacts complete (01–15). knowledge/MALICIOUS_ADJUSTER_REPORT.md's prompt-injection defence had been referenced (CTRL-PSB-04) but never formally specified as a test across all three workflows. The checkpoint-replay risk (INJ-094) was undisclosed in any prior artefact.
- **Action:** Formally specified the prompt-injection negative test using knowledge/MALICIOUS_ADJUSTER_REPORT.md's literal embedded instruction, extending its scope from Workflow A only (as in 04) to all three workflows' external-evidence ingestion paths. Specified an idempotency-key prevention control for the checkpoint-replay threat (INJ-094). Re-examined the two confirmed defects (DEF-007 stale auth cache, DEF-008 model mismatch) under an adversarial framing as privilege-escalation and model-tampering vectors, reusing rather than duplicating their existing gate specifications from 10/13.
- **Evidence consumed:** EVID-073 (knowledge/MALICIOUS_ADJUSTER_REPORT.md, new), EVID-074 (data/agent_runs.csv, new — INJ-094), EVID-045, EVID-008, EVID-038, EVID-035 (all reused).
- **Defects referenced:** DEF-007 and DEF-008 (both reused, reframed as threat vectors, no new defects).
- **State after:** `submission/artefacts/` contains 16 of 32 required templates. `inject_traceability.csv` updated: INJ-094 newly partially-addressed. This formally closes CTRL-PSB-04's deferred test obligation from 04_PRODUCT_SERVICE_BLUEPRINT.md as CTRL-TAM-01.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS**.

## Step 18 — 17_PRIVACY_CROSS_BORDER.md

- **State before:** 16 artefacts complete (01–16). No privacy-specific artefact existed; INJ-026 (litigation hold), INJ-039 (mental-health boundary), INJ-043 (consent withdrawal), INJ-071 (purpose expansion), INJ-072 (cross-border replica) and INJ-075 (retention conflict) were all undisclosed in any prior artefact.
- **Action:** Specified four privacy controls: clinical-notes segmentation (INJ-039, reusing case/SOURCE_SYSTEM_FACT_PACK.md's MedClaim Hub caveat), residency-compliance flagging for cross-border queries (INJ-072), consent-status live-check mirroring CTRL-DGL-01's pattern (INJ-043, INJ-071), and longest-rule/hold-wins for retention/deletion conflicts (INJ-026, INJ-075) — explicitly rejecting immediate-deletion-on-request as an option due to legal-hold/retention risk.
- **Evidence consumed:** EVID-075 (data/access_policies.csv, new), EVID-076 (data/data_residency.csv, new), EVID-077 (data/backup_inventory.csv, new), EVID-078 (data/consents.csv, new), EVID-079 (data/deletion_requests.csv, new), EVID-080 (data/legal_holds.csv, new), EVID-081 (data/retention_rules.csv, new), EVID-041 (reused).
- **Defects referenced:** None new; INJ-026/039/043/071/072/075 were disclosed-but-unaddressed injects prior to this step.
- **State after:** `submission/artefacts/` contains 17 of 32 required templates. `evidence_manifest.csv` grew from 66 to 81 rows across Steps 16–18 combined (EVID-067 through EVID-081). `inject_traceability.csv` updated: INJ-026, INJ-039, INJ-043, INJ-071, INJ-072, INJ-075 all newly partially-addressed.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS**.

## Interim correction — duplicate INJ-004 row and stale not-yet-addressed rows in inject_traceability.csv (post-Step 18)

- **State before:** A `Group-Object` count check across `inject_traceability.csv` found one duplicate inject ID: INJ-004 appeared twice (once from Step 3, once from Step 11's architectural extension), the second row superseding but not replacing the first. Separately, Step 16's edit had briefly left both the original Step-8 "not-yet-addressed" rows for INJ-013/015/016/017/018/019 and new rows for the same IDs in the file simultaneously before being caught and corrected within the same editing pass.
- **How found:** User instruction to complete templates 15–17 "with same instructions" (no missing IDs, update the state log), prompting a full duplicate-ID check via a PowerShell `Group-Object` scan of the CSV rather than relying on visual inspection alone.
- **Action:** Removed the earlier, less complete INJ-004 row (Step 3's version), keeping only the Step-11 version that includes the architectural extension. Confirmed the INJ-013/015/016/017/018/019 rows were already correctly singular (the near-duplicate had been corrected inline during Step 16's own edit, not left stale). Re-ran the `Group-Object` duplicate scan after the fix and confirmed zero duplicate inject IDs remain across all rows.
- **Evidence consumed:** None — this was a CSV row de-duplication, not a new evidence addition.
- **Defects referenced:** None — participant drafting inconsistency, not a package defect.
- **State after:** `inject_traceability.csv` has exactly one row per inject ID across all covered injects; verified via `Group-Object | Where-Object { $_.Count -gt 1 }` returning no results.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS** (re-run after the correction).

## Step 19 — 18_RESPONSIBLE_AI_FAIRNESS.md

- **State before:** 17 artefacts complete (01–17). Template 15 had recorded an immediate disclosure requirement for PRC-MOTOR-9/FRD-CLAIM-6's confirmed fairness breaches but explicitly deferred the deeper remediation programme to this template. INJ-085 (unexplainable adverse outcome), INJ-063 (vulnerable customer handling) and INJ-087 (accessibility failure) were undisclosed in any prior artefact.
- **Action:** Specified remediation pathways (retrain/feature-removal/retirement) for the two confirmed breaches, an at-output-time controlling-evidence/policy-rule citation requirement closing INJ-085, a cross-workflow vulnerability-routing rule closing INJ-063, and three pattern-specific accessibility design requirements closing INJ-087. Also addressed INJ-064's multilingual quality gap (corroborated by data/model_performance.csv, reused from 15) and partially addressed INJ-061 (dark-pattern renewal) via its accessibility angle.
- **Evidence consumed:** EVID-068, EVID-071 (both reused from 15), EVID-084 (knowledge/FAIRNESS_AND_ADVERSE_ACTION.md, new), EVID-086 (data/explanation_tests.csv, new), EVID-085 (data/customer_vulnerability.csv, new), EVID-082 (knowledge/ACCESSIBILITY_STANDARD.md, new), EVID-087 (data/usability_findings.csv, new), EVID-083 (knowledge/CLAIM_APPEAL_CONTESTABILITY.md, new).
- **Defects referenced:** None new; extends the treatment of the confirmed fairness breaches (data/fairness_metrics.csv) already logged as governance findings in Step 16.
- **State after:** `submission/artefacts/` contains 18 of 32 required templates. `inject_traceability.csv` updated: INJ-063, INJ-085, INJ-087 newly addressed; INJ-025, INJ-061, INJ-064 partially-addressed.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS**.

## Step 20 — 19_REGULATORY_APPLICABILITY.md

- **State before:** 18 artefacts complete (01–18). case/REGULATORY_BOUNDARY_PACK.md's required applicability matrix (distinguishing legal requirement, supervisory expectation, internal policy and design choice) had not yet been built. sources/ contained nine regulatory source anchors never previously cited in any artefact.
- **Action:** Built a nine-row applicability matrix, one per regulatory source, each scoped to entity/jurisdiction/workflow with an explicit requirement-type classification and a named interpretation owner. Explicitly flagged three areas of genuine uncertainty (EU AI Act high-risk classification, UK retail-business existence, AMR's precise legal-entity-to-regulator mapping) rather than asserting a definitive legal conclusion, consistent with the package's "not a legal interpretation service" scope boundary.
- **Evidence consumed:** EVID-088 (case/REGULATORY_BOUNDARY_PACK.md, new), EVID-089 (sources/SOURCE_VERIFICATION.csv, new), EVID-090 through EVID-097 (all nine sources/*.md files except ISO 42001, new), EVID-041 (reused).
- **Defects referenced:** None new; this is a governance/legal-scoping exercise, not a data-defect examination.
- **State after:** `submission/artefacts/` contains 19 of 32 required templates. No new inject rows — this artefact addresses cross-cutting regulatory scoping rather than a specific numbered inject, consistent with case/REGULATORY_BOUNDARY_PACK.md's own framing as a research pack rather than an inject.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS**.

## Step 21 — 20_ISO42001_GOVERNANCE.md

- **State before:** 19 artefacts complete (01–19). No single artefact consolidated the AI-management-system roles and lifecycle-stage controls already established across the submission into one ISO/IEC 42001-aligned view. No retirement-lifecycle-stage control existed anywhere in the submission.
- **Action:** Built a nine-role accountability map (reusing existing roles from case/STAKEHOLDER_PACK.md and prior artefacts, inventing none), a six-lifecycle-stage control cross-reference (five stages with existing controls, Retirement explicitly flagged as a gap), and an event-triggered management-review cadence. Explicitly disclaimed any ISO/IEC 42001 conformity or certification claim, per sources/09_ISO_IEC_42001.md's own non-normative caveat.
- **Evidence consumed:** EVID-098 (sources/09_ISO_IEC_42001.md, new), EVID-050 (reused).
- **Defects referenced:** None new.
- **State after:** `submission/artefacts/` contains 20 of 32 required templates. First explicit identification of the Retirement-lifecycle-stage gap, to be closed in template 27.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS**.

## Step 22 — 21_ASSURANCE_CASE.md

- **State before:** 20 artefacts complete (01–20). No single artefact structured the 8 non-compensable gates (requirements/SCORING_MODEL.md) as top-level claims with sub-claims, invalidation conditions and honest claim-strength reporting.
- **Action:** Built an 8-claim assurance case, one per non-compensable gate, each decomposed into sub-claims cross-referenced to specific artefact/control IDs, with an explicit falsifiable invalidation condition and an honest three-state claim-strength rating (argued-and-controlled / argued-not-yet-implemented / gap). Discovered two new gaps in the process: gate 2 (tenant isolation) has no specified multi-tenant test scenario anywhere in the submission, and gate 8 (fixture traceability) has zero sub-claims since template 22 (Evaluation and TEVV) does not yet exist. Cited AUDIT_AND_SANITY_CHECK.md and PREFLIGHT.md as gate 4's direct evidence, initially without proper Evidence IDs — caught and corrected within the same drafting pass by computing their hashes and adding EVID-100/EVID-101 before finalising.
- **Evidence consumed:** EVID-026, EVID-050 (both reused), EVID-100 (AUDIT_AND_SANITY_CHECK.md, new), EVID-101 (submission/evidence/PREFLIGHT.md, new).
- **Defects referenced:** None new; gate 7's claim directly cites the disclosure trail already logged in DEFECTS.md/ARTEFACT_STATE_LOG.md as its own evidence.
- **State after:** `submission/artefacts/` contains 21 of 32 required templates. `evidence_manifest.csv` grew from 99 to 101 rows (EVID-100, EVID-101). Two new gaps surfaced: gate-2 tenant-isolation test scenario (no owner assignment yet beyond CISO escalation) and gate-8 fixture-traceability (fully deferred to template 22).
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS**.

## Step 23 — 22_EVALUATION_TEVV.md

- **State before:** 21 artefacts complete (01–21). Non-compensable gate 8 (21_ASSURANCE_CASE.md) had zero sub-claims since this template did not yet exist. The supplied evaluation/ directory (18 public fixtures, 96-inject test obligations, 12 required test families) had never been directly inspected in any prior artefact.
- **Action:** Cross-verified evaluation/fixtures/EV-01/fixture.json's evidence hashes against evidence_manifest.csv and confirmed an exact match with EVID-013/014/028 (already logged from artefacts 05/06/07), confirming fixture-to-submission consistency. Built 9 representative test rows spanning 7 of 18 public fixtures and 7 of 12 required test families, applying the fail-closed/review-required distinction from evaluation/INJECT_TEST_OBLIGATIONS.csv and requiring per-subgroup (not aggregate) reporting for fairness/multilingual tests. Explicitly identified EV-17 (Cross-tenant broker query) as the concrete fixture that resolves gate 2's previously-identified tenant-isolation test-scenario gap from Step 22.
- **Evidence consumed:** EVID-102 (evaluation/EVALUATION_PLAN.md, new), EVID-103 (evaluation/FIXTURE_INDEX.csv, new), EVID-104 (evaluation/INJECT_TEST_OBLIGATIONS.csv, new), EVID-068, EVID-105 (data/candidate_outputs.csv, new), EVID-073 (all reused/new as noted).
- **Defects referenced:** None new; this artefact is an evaluation-design exercise confirming fixture integrity, not a new defect discovery.
- **State after:** `submission/artefacts/` contains 22 of 32 required templates. Gate 8 in 21_ASSURANCE_CASE.md now has real (execution-pending) sub-claims available for cross-referencing — flagged as an immediate follow-up in this artefact's own Open issues. Gate 2's tenant-isolation gap now has a concrete fixture (EV-17) identified, though still not executed.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS**.

## Step 24 — 23_TOKEN_FINOPS.md

- **State before:** 22 artefacts complete (01–22). REQ-NF-12/13 (bounded steps, token/cost budgets) had a taxonomy (13_MODEL_PROMPT_LIFECYCLE.md) but no numeric costing framework. INJ-089 (model price shock) and INJ-090 (denial-of-wallet) were undisclosed in any prior artefact, and INJ-089's price change (65% increase on OM-Large) was found to already be effective per data/model_costs.csv.
- **Action:** Specified a per-successful-reviewed-outcome costing methodology (never per raw model call), directly implementing DEFINITION_OF_DONE.md's economics requirement. Required an explicit three-option budget-response decision (absorb/substitute/renegotiate) for the already-effective OM-Large price shock. Specified a pre-request cost ceiling for the confirmed denial-of-wallet pattern, closing half of REQ-NF-13's numeric-value gap (the cost half; the step/time half remains with 13's design). Reapplied 01_BUSINESS_CASE.md's CTRL-BC-03 value-leakage discipline (human-review time must be included) to the token-efficiency context.
- **Evidence consumed:** EVID-109 (data/model_costs.csv, new), EVID-111 (data/vendor_contracts.csv, new), EVID-110 (data/model_usage.csv, new), EVID-010, EVID-061, EVID-057 (all reused).
- **Defects referenced:** None new; INJ-089's price change is confirmed live evidence, not a package defect.
- **State after:** `submission/artefacts/` contains 23 of 32 required templates. No numeric unit-cost figures exist yet (honestly stated as "not yet computed" pending implementation); the OM-Large price-shock decision is flagged as urgent (effective date 2026-08-15).
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS**.

## Step 25 — 24_RELIABILITY_OBSERVABILITY.md

- **State before:** 23 artefacts complete (01–23). data/downtime_events.csv (three concrete incident records) had never been directly inspected in any prior artefact. REQ-NF-14/15/17/18 (checkpointing, rollback, degraded mode, auditability) had architectural homes but no SLI/SLO specification.
- **Action:** Inspected data/downtime_events.csv directly and found DOWN-01 (PolicyCore-IN, ransomware containment) and DOWN-03 (AI-Primary-EU, regional outage) both have no recorded end timestamp — treated as still-ongoing incidents, not resolved history, per an explicit working assumption (A-01). Used DOWN-02's one concrete closed-duration incident (~49 hours, ClaimsImages) as the evidence-based reference point for setting a realistic SLO, rather than an arbitrary round number. Specified six SLI rows total: three tied to the concrete downtime events, two reusing the already-specified current-authorization and model-artefact verification gates (10/13), and one (CatVision) explicitly deferred pending a concrete incident record.
- **Evidence consumed:** EVID-107 (data/downtime_events.csv, new), EVID-106 (data/error_budgets.csv, new), EVID-060, EVID-041, EVID-045 (all reused).
- **Defects referenced:** DEF-007, DEF-008 (both reused, given SLI/alerting framing for the first time).
- **State after:** `submission/artefacts/` contains 24 of 32 required templates. `evidence_manifest.csv` grew from 101 to 111 rows across Steps 23–25 combined (EVID-102 through EVID-111). Two ongoing incidents (DOWN-01, DOWN-03) flagged as requiring current-status confirmation before any deployment decision.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS**.

## Step 26 — 25_INCIDENT_RECOVERY.md

- **State before:** 24 artefacts complete (01–24). data/network_zones.csv and data/security_events.csv had never been directly inspected. REQ-NF-14/15 (checkpointing, rollback) and the manual-mode-procedure gap (flagged in 13/24's open issues) had no concrete scenario specification yet.
- **Action:** Inspected data/network_zones.csv directly and found its INJ-080 row describes the same ransomware-containment parameters (PolicyCore-IN read-only, ClaimsImages offline, payments degraded) as data/downtime_events.csv's DOWN-01/DOWN-02 rows already logged in Step 25 — cross-confirmed as one incident from two independent evidence sources (A-01). Built four incident scenarios (ransomware containment, cross-tenant leakage, denial-of-wallet, model-artefact mismatch), each naming a specific data/continuity_requirements.csv manual_mode value and reusing (not duplicating) the verification gates already specified in 06/10/13/16/23 for recovery validation.
- **Evidence consumed:** EVID-112 (knowledge/AI_INCIDENT_RESPONSE.md, new), EVID-114 (data/network_zones.csv, new), EVID-113 (data/security_events.csv, new), EVID-119 (data/continuity_requirements.csv, new), EVID-107, EVID-045 (both reused).
- **Defects referenced:** None new; DEF-007/DEF-008 reused with incident-response framing.
- **State after:** `submission/artefacts/` contains 25 of 32 required templates. Cross-confirmation between network_zones.csv and downtime_events.csv strengthens the evidence base for the ransomware-containment scenario. The 21-day max_ai_outage_days ceiling (data/continuity_requirements.csv) is flagged as potentially already exceeded given DOWN-01's still-open status.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS**.

## Step 27 — 26_TARGET_OPERATING_MODEL.md

- **State before:** 25 artefacts complete (01–25). INJ-088 (accountability conflict between global AI owners and local legal-accountability roles) was undisclosed in any prior artefact. No artefact had yet distinguished "who designed a workflow" from "who operationally owns it once live."
- **Action:** Resolved INJ-088 with an explicit standing precedence rule (local legal accountability always retains final sign-off over global standardisation, no override clause). Named three workflow operational owners (Group Chief Claims Officer, US Chief Underwriter, Reinsurance Director) reusing their existing persona assignments from 04, explicitly distinct from the AI Product Owner's design-accountability role. Cross-referenced (but explicitly did not close) the Retirement lifecycle-stage gap from 20_ISO42001_GOVERNANCE.md, deferring closure to template 27 per this artefact's own A-04.
- **Evidence consumed:** EVID-118 (data/stakeholders.csv, new), EVID-009 (data/decision_rights.csv, reused — same hash confirmed to also corroborate INJ-088), EVID-046, EVID-119 (both reused).
- **Defects referenced:** None new.
- **State after:** `submission/artefacts/` contains 26 of 32 required templates. INJ-088 fully addressed with a named, evidence-grounded rule. Retirement gap ownership formally reassigned to AI Product Owner pending template 27.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS**.

## Step 28 — 27_VENDOR_EXIT_RETIREMENT.md

- **State before:** 26 artefacts complete (01–26). The Retirement lifecycle-stage gap, first identified in 20_ISO42001_GOVERNANCE.md and re-flagged in 26, remained open. INJ-092 (stack concentration, one vendor hosting six capabilities) and INJ-017 (unapproved external data) had no exit/portability treatment.
- **Action:** Built a capability-level fallback analysis identifying key management as the single highest-severity point of failure among the six stack-concentrated capabilities (INJ-092). Specified model portability via the existing model_registry.csv abstraction layer (reusing 13's design, not inventing a new one). Specified non-proprietary, hash-preserving data export addressing INJ-017's provenance concern applied to AMR's own data. Set transition-period floors from data/continuity_requirements.csv's rto_hours values, flagging CatVision (INJ-035's confirmed outage vendor) for priority fallback planning. Formally closed the Retirement gap at the specification level.
- **Evidence consumed:** EVID-115 (data/vendor_dependencies.csv, new), EVID-116 (data/vendor_status.csv, new), EVID-117 (data/data_licenses.csv, new), EVID-119, EVID-057 (both reused).
- **How a miss was caught and fixed within this step:** The initial draft cited `submission/artefacts/20_ISO42001_GOVERNANCE.md` with a placeholder `—` in the Scope and evidence register, incorrectly treating a single-file reference as if it were a multi-file span (the established convention that legitimately uses `—`). Caught during the same drafting pass's evidence-integrity sweep: computed the file's hash, added it as EVID-120, and updated the artefact to cite EVID-120 instead of `—`, before finalising.
- **Defects referenced:** None new.
- **State after:** `submission/artefacts/` contains 27 of 32 required templates. `evidence_manifest.csv` grew from 111 to 120 rows across Steps 26–28 combined (EVID-112 through EVID-120). The Retirement lifecycle-stage gap is now closed at the specification level; 20_ISO42001_GOVERNANCE.md's Open issues table should be updated to reflect this (flagged as an immediate follow-up in 27's own Open issues).
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS** (re-run after the EVID-120 correction).

## Step 29 — 28_PRODUCTION_READINESS.md

- **State before:** 27 artefacts complete (01–27). No single artefact had consolidated the cumulative "no implementation code" finding (logged at every step since Step 8) into one explicit readiness verdict, per-gate go/no-go criteria and cutover/rollback plan.
- **Action:** Directly counted `inject_traceability.csv`'s rows by status (66 total logged: 22 addressed, 33 partially-addressed, 11 not-yet-addressed) and explicitly flagged that ~30 of the 96-inject catalogue have no row at all yet — a more honest framing than reporting only the 66 logged rows. Issued an explicit "NOT production-ready, READY to begin implementation" verdict, rejecting the alternative of claiming readiness based on documentation completeness alone. Built per-gate go/no-go criteria for all 8 non-compensable gates (only gates 4 and 7 currently pass). Confirmed phased per-workflow cutover and independent per-workflow rollback, reusing rather than replacing 04's existing design.
- **Evidence consumed:** EVID-106 (reused), EVID-026 (reused), EVID-121 (submission/evidence/inject_traceability.csv, new — point-in-time snapshot hash, since this file is actively edited at every step).
- **How a miss was caught and fixed within this step:** The initial draft cited `submission/evidence/inject_traceability.csv` with a placeholder `—`, incorrectly reasoning that a live-count evidence source could not be given a stable single-file hash. Caught during this step's evidence-integrity sweep (informed by the same pattern already caught twice before, in Steps 22 and 28): computed the file's hash as a point-in-time snapshot, added it as EVID-121 with an explicit caveat about its snapshot nature, and updated the artefact before finalising.
- **Defects referenced:** None new.
- **State after:** `submission/artefacts/` contains 28 of 32 required templates. The submission's actual implementation status is now formally and honestly documented in one place, distinguishing "argued, not yet implemented" (6 of 8 gates) from genuinely passing (2 of 8 gates: reproducibility, disclosure).
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS** (re-run after the EVID-121 correction).

## Step 30 — 29_NINETY_DAY_ROADMAP_HANDOVER.md

- **State before:** 28 artefacts complete (01–28). 28's gap assessment existed but had not been sequenced into a prioritised timeline or connected to 26's three named operational owners for formal handover acceptance.
- **Action:** Sequenced 28's gaps by non-compensable-gate priority (not ease-of-implementation), scheduling the two genuinely time-critical items (OM-Large price-shock decision, due 2026-08-15; DOWN-01/DOWN-03 status confirmation) in week 1. Concentrated weeks 2–11 on Workflow A specifically (per 28's phased-cutover decision), explicitly rejecting an attempt to progress all three workflows simultaneously. Required per-workflow handover sign-off from each of 26's three named operational owners, and explicitly stated what will NOT be achieved within 90 days (full inject coverage, live pilot readiness, Workflow C start) rather than overclaiming scope.
- **Evidence consumed:** EVID-122 (submission/artefacts/28_PRODUCTION_READINESS.md, new), EVID-121, EVID-109, EVID-107 (all reused).
- **How a miss was caught and fixed within this step:** The initial draft again cited a single participant-authored file (`28_PRODUCTION_READINESS.md`) with a placeholder `—`, repeating the same class of error already caught and corrected in Steps 22, 28 and this same step's own first correction. Caught immediately during the same drafting pass: computed the file's hash, added it as EVID-122, and updated the artefact before finalising, without waiting for external review this time.
- **Defects referenced:** None new.
- **State after:** `submission/artefacts/` contains 29 of 32 required templates. `evidence_manifest.csv` grew from 120 to 122 rows across Steps 29–30 combined (EVID-121, EVID-122). No new inject_traceability.csv rows were needed since this artefact pair sequences and consolidates existing gaps rather than identifying new inject-level findings.
- **Validation run:** `python tools/check_submission.py --mode scaffold` → **PASS** (re-run after the EVID-122 correction).

## Outstanding state gaps (as of this log)

| Gap | Why it matters | Next step |
|---|---|---|
| Templates 22–32 not started | Required for `--mode final`; scoring dimensions for evaluation/TEVV, token economics, reliability/incident response, vendor exit/retirement, target operating model, handover and defence remain entirely unevidenced | Continue artefact drafting in numeric order |
| No implementation code (submission/src, submission/app) | All CTRL-*/REQ-C-*/ADR-* controls referenced across artefacts 01–21 are currently documentation-only, not enforced, including the fairness-remediation pathways (18), the regulatory-applicability rows (19), and the assurance-case claims (21) | Begin Workflow A implementation against the DDD/ontology model (05/07), the bounded graph decision (08), the C4 component placements (10) and the integration contracts (12) |
| No tests (submission/tests) | Cannot demonstrate the negative/security tests referenced across all artefacts (CTRL-TAM-01/02, CTRL-RAF-02/03, gate-2 EV-17, gate-8's 9 representative tests) | Author tests alongside first implementation increment; sequenced in 29's 90-day roadmap weeks 8–11 |
| Zero implementation exists for any of the 8 non-compensable gates' go/no-go criteria (28's central finding); only gates 4 (reproducibility) and 7 (disclosure) currently pass | This is the single largest residual risk in the entire submission | No pilot cutover until gates 1/2/3/5/6/8 pass; sequenced in 29's 90-day roadmap by gate priority |
| 28/20's Open-issues tables have not been cross-updated to reflect 27's closure of the Retirement gap | 20's text still describes the gap as open even though 27 resolves it at the specification level | Update 20_ISO42001_GOVERNANCE.md's Open issues table to cite 27 |
| Neither PRC-MOTOR-9 nor FRD-CLAIM-6 has a chosen remediation approach yet (retrain vs feature-removal vs retirement), despite template 18 specifying that a choice is required | Confirmed fairness breaches remain only disclosed, not yet remediated | Escalate to Model Risk Owner and Chief Actuary for a decision with a target date |
| AMR's precise legal-entity-to-jurisdiction-to-regulator mapping, EU AI Act high-risk classification, and UK retail-business existence are all undetermined (19) | Three genuine regulatory-uncertainty gaps requiring qualified legal input, not resolvable from supplied evidence alone | Escalate to Legal before any jurisdiction-specific compliance claim is operationalised |
| The standing precedence rule resolving INJ-088 (26) has not yet been formally ratified by the Group CEO/Board | Proposed, not yet approved governance rule | Escalate to Group CEO/Board for formal ratification |
| Key management is the highest-severity single point of failure in the stack-concentration finding (27), but no specific fallback vendor/mechanism has been evaluated | Losing key-management access could block recovery of five other dependent capabilities simultaneously | Escalate to CISO for a dedicated key-management continuity assessment |
| No operational runbooks exist yet for any of the three workflows' named operational owners (26); training cannot meaningfully begin until an implementation exists (29's A-03) | Naming an owner/scheduling training does not itself produce a working system to train against | Author runbooks and begin training only once Workflow A's gate-1-adjacent controls pass (per 29's roadmap) |
| DOWN-01 (PolicyCore-IN) and DOWN-03 (AI-Primary-EU) have no recorded end timestamp and are treated as still-ongoing incidents; current actual status is unknown to this submission | Scheduled as a week-1 priority in 29's 90-day roadmap given the 21-day max_ai_outage_days ceiling may already be breached | Escalate to CISO/Group Chief Claims Officer for current-status confirmation — most time-critical open item |
| The OM-Large 65% price increase is already effective (2026-08-15) and has no chosen budget response yet (absorb/substitute/renegotiate) | Scheduled as a week-1 priority in 29's 90-day roadmap; delay risks silently absorbing the full increase by default | Escalate to Finance/AI Product Owner for an immediate decision before the effective date |
| This submission's 90-day roadmap (29) explicitly concentrates on Workflow A only; Workflow B/C remain "argued, not yet implemented" at the end of the window, and ~30 of 96 injects have no logged row at all | Accepted, disclosed scope limitation, not an oversight | Address in the next 90-day roadmap cycle after this one completes |
| D09 injects INJ-059 (bancassurance mis-selling), INJ-060 (broker remuneration conflict), INJ-062 (complaint clock mismatch) remain entirely unexamined | Conduct-risk rubric dimension partially touched (18's dark-pattern/accessibility angle) but not these three | Sequence into a future roadmap cycle if they surface additional implications |
| Graph-schema-level design for the fraud-ring component (INJ-045), the PayFlow read-only/propose-only technical enforcement, three pattern-specific controls in 14 (reserve logging, payee-change trigger, hardship-advance override), TR-2026-CY-02's pending signed wording, and several unset numeric parameters (traversal depth, cost ceilings, propagation windows) all remain open from earlier steps | Consolidated list of implementation-time parameters/designs still required before their respective controls are enforceable | Consolidate into a single implementation checklist per 28's own recommendation, cross-referenced to each originating artefact |
