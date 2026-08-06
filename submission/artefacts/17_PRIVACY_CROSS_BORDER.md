# 17 Privacy Cross Border

## Purpose

Purpose limitation, lawful basis, minimisation, sensitive data, residency, retention and data-subject rights for the evidence used by the three workflows, grounded in the confirmed cross-border replication risk, consent-withdrawal gap, mental-health privacy boundary, and the retention-versus-legal-hold conflict.

## Acceptance criteria

- The artefact is evidence-led and references supplied paths, record locators and inject IDs.
- Facts, assumptions, inference, conflict, decision and residual risk are distinguishable.
- Temporal, jurisdictional, authorization and authority boundaries are explicit where relevant.
- Owners, approvals, review triggers and measurable acceptance gates are named.
- The artefact contains no unsupported coverage, pricing, reserve, payment or treaty conclusion.

## Artefact-specific acceptance criteria

- No workflow uses claims images or health data for model training beyond the original processing purpose without a new, explicit lawful basis, closing INJ-071 (CTRL-PCB-01).
- No policyholder data is replicated into an analytics region without an approved residency exception, closing INJ-072 (CTRL-PCB-02).
- Withdrawn consent (INJ-043) is propagated to every downstream feature store within a bounded time window; no feature continues using data after consent withdrawal (CTRL-PCB-03).
- Retention conflicts (INJ-075) and legal holds (INJ-026) are resolved by the longest-applicable-hold-wins rule, never by the earliest-deletion-rule, and every deletion request is checked against active legal holds before execution (CTRL-PCB-04).

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| EVID-075 | data/access_policies.csv (record_id=INJ-039-ACCESS_POLICIES) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Mental-health privacy boundary: behavioural-health notes exposed to a general claims summarisation workflow beyond minimum necessary use (INJ-039). |
| EVID-076 | data/data_residency.csv (record_id=INJ-072-DATA_RESIDENCY) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Cross-border replica: EU and Indian policyholder data replicated into an unapproved analytics region (INJ-072). |
| EVID-077 | data/backup_inventory.csv (record_id=INJ-072-BACKUP_INVENTORY) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Corroborates INJ-072. |
| EVID-078 | data/consents.csv (record_id=INJ-043-CONSENTS;INJ-071-CONSENTS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | INJ-043: wellness consent withdrawn but data remains in pricing/engagement features; INJ-071: claims images/health data proposed for enterprise model training beyond original purpose. |
| EVID-079 | data/deletion_requests.csv (record_id=INJ-026-DELETION_REQUESTS;INJ-075-DELETION_REQUESTS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | INJ-026: customer requests deletion while claim/complaint/class-action under legal hold; INJ-075: retention rules conflict across fraud/tax/litigation/actuarial/deletion purposes. |
| EVID-080 | data/legal_holds.csv (record_id=INJ-026-LEGAL_HOLDS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Corroborates INJ-026. |
| EVID-081 | data/retention_rules.csv (record_id=INJ-075-RETENTION_RULES) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Corroborates INJ-075. |
| EVID-041 | case/SOURCE_SYSTEM_FACT_PACK.md | approved/case-pack | 2026-08-01 | MULTI | Reused from 06/10/12; MedClaim Hub's "clinical notes require segmentation" caveat directly informs the mental-health privacy boundary row below. |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | Behavioural-health/clinical notes accessed by any workflow must be segmented from general claims summarisation per case/SOURCE_SYSTEM_FACT_PACK.md's MedClaim Hub caveat; a general-purpose summarisation model (e.g., GEN-SUM-3, per 13_MODEL_PROMPT_LIFECYCLE.md) must not receive unsegmented clinical notes as input. | data/access_policies.csv (EVID-075, INJ-039); case/SOURCE_SYSTEM_FACT_PACK.md (EVID-041) | Unsegmented access would violate minimum-necessary-use and could expose sensitive health information beyond the claims-evidence-reconciliation purpose. | CISO, Data Governance Owner | Before any Workflow A feature touching health claims is designed |
| A-02 | The confirmed cross-border replication (INJ-072, EU/Indian data into an unapproved analytics region) is treated as an active residency violation requiring immediate flagging, not a hypothetical future risk; any workflow querying DataLake-X (per case/SOURCE_SYSTEM_FACT_PACK.md, "never authoritative by itself") must additionally check the query's data-residency compliance before returning cross-border results. | data/data_residency.csv (EVID-076); data/backup_inventory.csv (EVID-077) | Continuing to serve queries against an unapproved-region replica without flagging would perpetuate a live compliance violation. | Data Governance Owner, CISO | Immediate — before any further DataLake-X-backed query is served |
| A-03 | Consent withdrawal (INJ-043, wellness data) must propagate to every downstream feature store within a bounded time window (numeric value deferred to implementation, per the pattern established in 13_MODEL_PROMPT_LIFECYCLE.md's deferred numeric budgets); a feature store still using withdrawn-consent data after that window is treated as a control failure. | data/consents.csv (EVID-078, INJ-043) | Continued use of withdrawn-consent data would breach the consent's own terms and any applicable data-protection lawful-basis requirement. | Data Governance Owner | Before any pricing/engagement feature reads consent-gated data |
| A-04 | Where retention rules conflict (INJ-075: fraud, tax, litigation, actuarial and customer-deletion rules specifying different periods) or a legal hold is active (INJ-026), the longest-applicable period or the hold — whichever is longer — always controls; a deletion request is never executed while any relevant hold or longer-retention rule remains active. | data/retention_rules.csv (EVID-081); data/deletion_requests.csv (EVID-079); data/legal_holds.csv (EVID-080) | Executing a deletion while a shorter-retention interpretation is applied, ignoring an active hold or a longer statutory period, could destroy evidence required for litigation, tax or regulatory purposes. | Data Governance Owner, Legal | Before any automated deletion-request handling is designed |

## Required analysis and decisions

| Decision/question | Evidence | Analysis | Decision/output | Owner | Status |
|---|---|---|---|---|---|
| How must behavioural-health/clinical notes be segmented from general claims summarisation? | data/access_policies.csv (EVID-075); case/SOURCE_SYSTEM_FACT_PACK.md (EVID-041) | Per A-01, clinical notes require a separate, purpose-restricted access path; Workflow A's evidence-reconciliation summary may reference the existence of clinical evidence without including its unsegmented content in a general-purpose model call | Workflow A output may cite "clinical evidence exists, segmented access required" without exposing note content through a general summarisation path | CISO, Data Governance Owner | Decided — segmentation rule recorded, implementation deferred |
| How must the confirmed cross-border replication (INJ-072) be handled at query time? | data/data_residency.csv (EVID-076); data/backup_inventory.csv (EVID-077) | Per A-02, any query against a replica outside its approved residency region must be flagged as a compliance exception at query time, not silently served | DataLake-X-backed (and any other cross-region replica) queries carry a residency-compliance flag; non-compliant results are not withheld from human review, but are explicitly labelled | Data Governance Owner | Decided — flagging rule recorded, implementation deferred |
| How must consent withdrawal (INJ-043) propagate to downstream feature stores? | data/consents.csv (EVID-078) | Per A-03, a bounded propagation window is required; until numeric implementation, this artefact records the requirement and the escalation path if the window is exceeded | Any feature-store read of consent-gated data must check current consent status, not a cached snapshot, mirroring the current-authorization re-check pattern already established in CTRL-DGL-01 | Data Governance Owner | Decided — requirement recorded, numeric window deferred |
| How must retention conflicts and legal holds (INJ-075, INJ-026) be resolved? | data/retention_rules.csv (EVID-081); data/deletion_requests.csv (EVID-079); data/legal_holds.csv (EVID-080) | Per A-04, longest-applicable-rule/hold-wins; every deletion request triggers an active-hold check before execution | Deletion requests are queued pending hold-clearance, never auto-executed against a shorter retention interpretation | Data Governance Owner, Legal | Decided |

## Alternatives and trade-offs

| Option | Benefits | Risks | Cost/complexity | Reversibility | Decision and rationale |
|---|---|---|---|---|---|
| Allow general-purpose summarisation models unrestricted access to all claim-linked data including clinical notes, for simplicity | Simpler implementation, no segmentation logic needed | Directly violates the MedClaim Hub segmentation caveat (case/SOURCE_SYSTEM_FACT_PACK.md) and the minimum-necessary-use principle; reproduces INJ-039 | Lower build cost, high privacy-compliance risk | Reversible but any past exposure cannot be retroactively contained | Rejected. A-01 requires segmentation before any general-purpose model call touches clinical notes. |
| Continue serving DataLake-X-backed queries without a residency-compliance flag, treating the replication as someone else's problem to fix later | Avoids implementation effort now | Perpetuates an active, confirmed residency violation (INJ-072) without disclosure, contradicting DEFINITION_OF_DONE.md's evidence/disclosure discipline | Lower cost now, ongoing compliance exposure | Reversible but every day of non-disclosure compounds the exposure | Rejected. A-02 requires immediate flagging, not deferral. |
| Execute deletion requests immediately upon customer request, overriding any retention rule or legal hold, to maximise responsiveness to data-subject rights | Fastest data-subject-rights response | Could destroy evidence under active litigation hold (INJ-026) or violate a longer statutory retention period (INJ-075), creating a legal/regulatory exposure worse than a delayed deletion | Lower implementation complexity, unacceptable legal risk | Irreversible once data is deleted — this is the highest-severity risk in this artefact | Rejected outright. A-04's longest-rule/hold-wins principle is the only option consistent with both data-subject rights and legal-preservation obligations. |
| Segmentation for clinical notes, residency-compliance flagging for cross-border queries, consent-status live-check for feature stores, and longest-rule/hold-wins for retention/deletion — four targeted rules, each reusing an existing pattern from prior artefacts where possible (e.g., consent check mirrors CTRL-DGL-01's live-check pattern) | Directly closes INJ-039, INJ-072, INJ-043 and INJ-075/INJ-026 with rules proportionate to each risk; reuses the current-authorization re-check pattern rather than inventing a new one for consent | Four rules to maintain instead of one; requires Legal input on the retention/hold interaction that is not fully specified in the supplied evidence-envelope schema | Medium — four targeted rules | Reversible; each rule can be revised independently | Selected. Matches the confirmed/disclosed risk pattern for each of the four injects examined without inventing an unproportionate single global privacy policy. |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-PCB-01 | No claims image/health data is used for training beyond original purpose without new lawful basis | Design review of any model-training-data pipeline proposal against data/consents.csv | No training-data pipeline includes health/claims-image data unless a new, dated, cited consent or lawful basis is attached | submission/tests (deferred) | Data Governance Owner |
| CTRL-PCB-02 | No policyholder data is replicated into an unapproved analytics region | Test querying a known cross-region replica pattern (data/data_residency.csv) | Query result carries an explicit residency-compliance flag; the exception is never silently served | submission/tests (deferred) | CISO |
| CTRL-PCB-03 | Withdrawn consent is propagated to every downstream feature store within a bounded window | Test withdrawing consent in a test fixture and checking feature-store read behaviour | Feature store denies or excludes the withdrawn-consent data on the next read, mirroring CTRL-DGL-01's live-check pattern | submission/tests (deferred) | Data Governance Owner |
| CTRL-PCB-04 | Deletion requests never execute while a longer retention rule or active legal hold applies | Test submitting a deletion request against a fixture with an active legal hold (data/legal_holds.csv pattern) | Deletion is queued/rejected, never executed, while the hold is active | submission/tests (deferred) | Legal, Data Governance Owner |

## Traceability

| Inject/requirement | Architecture/ADR | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| INJ-039 (mental-health privacy boundary) | New: clinical-notes segmentation rule (this artefact) | Segmented access path for clinical notes (not yet implemented) | CTRL-PCB-01 (deferred, distinct control ID but same underlying data) | Segmentation boundary technical enforcement not yet designed at the data-access layer. |
| INJ-072 (cross-border replica) | New: residency-compliance flagging rule (this artefact) | Residency-flag on cross-region query results (not yet implemented) | CTRL-PCB-02 (deferred) | Underlying replication itself is not yet remediated; this artefact can only flag, not prevent, continued replication. |
| INJ-043 (wellness consent withdrawal), INJ-071 (purpose expansion) | New: consent-propagation and training-data lawful-basis rules (this artefact) | Consent-status live-check for feature stores (not yet implemented) | CTRL-PCB-01, CTRL-PCB-03 (deferred) | Propagation-window numeric value not yet set. |
| INJ-026 (litigation hold vs deletion), INJ-075 (retention conflict) | New: longest-rule/hold-wins resolution (this artefact) | Deletion-request hold-check gate (not yet implemented) | CTRL-PCB-04 (deferred) | Full retention-period matrix across fraud/tax/litigation/actuarial purposes not yet enumerated for all data categories. |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| None of the four privacy controls above has a corresponding implementation yet | High | Track alongside the "no implementation code" gap already logged in ARTEFACT_STATE_LOG.md | Data Governance Owner | Open | Before templates 26–28 (target operating model, production readiness) |
| The consent-propagation window (A-03) and the full retention-period matrix (A-04) have no numeric values or complete enumeration yet | Medium | Set with Legal and Data Governance Owner input during implementation | Data Governance Owner, Legal | Open | Before any consent-gated or retention-gated feature is implemented |
| This artefact does not yet address D11 injects INJ-073 (household inference via IoT), INJ-074 (telematics family surveillance) | Medium | Defer to a later pass if these surface additional privacy implications beyond what is covered here | Data Governance Owner | Open | Before final submission |
| Cross-border remediation (actually correcting the INJ-072 replication, not just flagging it) is outside this artefact's scope | High | Escalate to CISO/Data Governance Owner as an infrastructure remediation item, distinct from the workflow-level flagging control this artefact specifies | CISO | Open | Before any workflow is deployed to a jurisdiction with strict residency enforcement |