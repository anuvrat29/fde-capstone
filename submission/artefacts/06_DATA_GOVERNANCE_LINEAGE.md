# 06 Data Governance Lineage

## Purpose

Data inventory, quality, contracts, provenance, authority, retention and residency for the datasets used by Workflow A and Workflow B, grounded in the D01–D02 injects and the source-system fact pack.

## Acceptance criteria

- The artefact is evidence-led and references supplied paths, record locators and inject IDs.
- Facts, assumptions, inference, conflict, decision and residual risk are distinguishable.
- Temporal, jurisdictional, authorization and authority boundaries are explicit where relevant.
- Owners, approvals, review triggers and measurable acceptance gates are named.
- The artefact contains no unsupported coverage, pricing, reserve, payment or treaty conclusion.

## Artefact-specific acceptance criteria

- No workflow proceeds on a cached authorization status alone; a live re-check against the current entitlement source is performed or the action is denied (CTRL-DGL-01).
- No combined cross-currency total is produced without a cited FX methodology and valuation date; per-currency figures are shown by default (CTRL-DGL-02).
- Any model-backed component refuses to use a deployed artefact that mismatches the approved registry and raises an escalation instead (CTRL-DGL-03).
- Accumulation/duplicate-detection outputs are labelled "provisional — address resolution incomplete" whenever unresolved address/geocode variants are present (CTRL-DGL-04).

## Scope and evidence register

| Evidence ID | Source path and locator | Authority/status | Effective time | Jurisdiction | Use and limitation |
|---|---|---|---|---|---|
| EVID-041 | case/SOURCE_SYSTEM_FACT_PACK.md | approved/case-pack | 2026-08-01 | MULTI | Twelve source systems with known issues and authority caveats; primary source for the lineage/authority table below. |
| EVID-042 | metadata/DATASET_CATALOG.csv | as_supplied/verified (hash-checked by tools/verify_package.py) | n/a | n/a | Row/column counts and SHA-256 per dataset; used to confirm dataset integrity before use. |
| EVID-038 | metadata/RELATIONSHIP_RULES.csv | as_supplied/verified | n/a | n/a | Declared foreign-key relationships (e.g., REL-007 access_cache.csv→users_entitlements.csv; REL-008 model_artifacts.csv→model_registry.csv). |
| EVID-007 | data/system_inventory.csv (record_id=INJ-004-SYSTEM_INVENTORY) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Acquisition integration creates identifier/tenancy fragmentation (INJ-004). |
| EVID-017 | data/billing_events.csv (record_id=INJ-010-BILLING_EVENTS) | mixed/as_supplied | 2026-08-01T06:00:00Z | MULTI | Cancellation/reinstatement/premium-receipt event-ordering conflict (INJ-010). |
| EVID-043;EVID-044 | data/addresses.csv; data/geocodes.csv | mixed/as_supplied | n/a | MULTI | INJ-030: one apartment complex has six address forms and two geocodes, fragmenting accumulation/duplicate detection. |
| EVID-045 | starter/baseline_diagnostics.py (executed output) | participant-generated diagnostic | 2026-08-06 | n/a | Confirms via direct execution: mixed currencies in claims.csv; access_cache.csv can show `active` after a user is `revoked` in users_entitlements.csv; model_artifacts.csv has a `mismatch` status against model_registry.csv. |

## Working assumptions and constraints

| ID | Assumption or constraint | Basis | Impact if false | Validation owner | Due/review date |
|---|---|---|---|---|---|
| A-01 | No single system is globally authoritative; authority is contextual (issuance vs interpretation vs identity vs paid-amount) and must be modelled per use, not as one ranked list. | case/SOURCE_SYSTEM_FACT_PACK.md "Evidence-authority rules to discover and defend"; PACKAGE_SCOPE_AND_ASSUMPTIONS.md | A single global ranking would misapply authority in the many documented exceptions (e.g., PolicyCore-IN authoritative for issued schedule but not scanned endorsements). | Data Governance Owner | Before any cross-system query is built |
| A-02 | Currency values must not be aggregated without a stated valuation date and FX authority. | PACKAGE_SCOPE_AND_ASSUMPTIONS.md; confirmed live by starter/baseline_diagnostics.py flagging mixed currencies in claims.csv (INR, EUR, USD present) | Summing claimed_amount across currencies without FX normalization would produce a materially wrong total. | Chief Actuary | Before any cross-currency total is reported |
| A-03 | Authorization cache staleness (access_cache.csv cached_status can remain `active` after users_entitlements.csv status becomes `revoked`) is a live, confirmed data-quality/security defect, not a hypothetical. | starter/baseline_diagnostics.py output: "authorization cache can outlive revocation"; metadata/RELATIONSHIP_RULES.csv REL-007 | Any workflow trusting access_cache.csv without re-checking users_entitlements.csv at time of use risks acting on stale authorization — a security-relevant failure. | CISO | Before any workflow reads access_cache.csv for an authorization decision |
| A-04 | Deployed model artefacts can differ from the approved registry (model_artifacts.csv status=`mismatch` vs model_registry.csv), confirmed live by starter/baseline_diagnostics.py. | starter/baseline_diagnostics.py output: "deployed model artefact differs from approved registry"; metadata/RELATIONSHIP_RULES.csv REL-008 | A workflow calling a mismatched model artefact could produce outputs from an unapproved, unvalidated model version. | AI Product Owner, Model Risk Owner | Before any model-backed workflow component goes live |
| A-05 | Address and geocode fragmentation (INJ-030: six address forms, two geocodes for one apartment complex) means naive string-matching or single-geocode accumulation will under- or double-count exposure/claims. | data/addresses.csv, data/geocodes.csv | Catastrophe accumulation and duplicate-claim detection (Workflow A/C) would be unreliable without an explicit identity-resolution step. | Data Governance Owner | Before Workflow A/C accumulation logic is built |

## Required analysis and decisions

| Decision/question | Evidence | Analysis | Decision/output | Owner | Status |
|---|---|---|---|---|---|
| Which source system is authoritative for which fact, and under what condition? | case/SOURCE_SYSTEM_FACT_PACK.md (12 systems) | Authority is per-fact-type, not per-system: e.g., PolicyCore-IN → authoritative for issued schedule, not scanned endorsements; ClaimSphere → claims/reserves but has duplicate party/event IDs; AI Gateway → model/tool access but has revocation cache lag | Build an explicit authority-lookup table (fact type × system × condition) rather than a single source-of-truth ranking; recorded here as a design requirement, full table deferred to implementation | Data Governance Owner | Decided — principle recorded; full lookup table not yet built |
| How should the authorization-cache staleness defect (A-03) be handled at runtime? | starter/baseline_diagnostics.py; access_cache.csv; users_entitlements.csv; metadata/RELATIONSHIP_RULES.csv REL-007 | Any workflow action gated by user authorization must re-check users_entitlements.csv (or an equivalent current source) at time of use, never relying solely on a cached status | Runtime authorization check is a mandatory operating property ("current authorization") per case/START_HERE.md rules of engagement | CISO | Decided — requirement recorded; implementation deferred |
| How should mixed-currency claim amounts (A-02) be handled in any reporting or accumulation? | claims.csv (INR, EUR, USD observed); starter/baseline_diagnostics.py | No sum is produced without an explicit valuation date and FX-rate source cited; absent that, the workflow must report per-currency figures separately or abstain from a combined total | Reporting outputs must show currency-disaggregated figures by default; combined totals require an explicit, cited FX methodology | Chief Actuary | Decided — requirement recorded |
| How should address/geocode fragmentation (A-05) be handled for accumulation and duplicate detection? | data/addresses.csv; data/geocodes.csv | An identity-resolution step (canonicalising address forms and reconciling geocodes) must run before any accumulation or duplicate-claim logic; absent that step, the system must flag accumulation results as provisional | Accumulation outputs must be labelled "provisional — address resolution incomplete" until an identity-resolution component exists | Data Governance Owner | Decided — requirement recorded; identity-resolution component not yet built |

## Alternatives and trade-offs

| Option | Benefits | Risks | Cost/complexity | Reversibility | Decision and rationale |
|---|---|---|---|---|---|
| Trust access_cache.csv-equivalent caches directly for speed | Lower latency, simpler implementation | Confirmed security defect (A-03): stale `active` status can outlive revocation | Low | Reversible, but the exposure window during use is not retroactively fixable | Rejected. Directly contradicts the "current authorization" mandatory operating property. |
| Always re-check current entitlement source at time of use, accepting latency cost | Closes the stale-cache exposure window | Higher latency per action; requires reliable access to the entitlement source, which may itself be degraded during an incident (per case/SOURCE_SYSTEM_FACT_PACK.md AI Gateway note) | Medium | Fully reversible; can fall back to a documented degraded-mode procedure if the entitlement source is unavailable | Selected. Matches the required operating property; degraded-mode fallback must still be designed (deferred). |
| Report a single blended-currency claim total for simplicity | Easier to read | Materially misleading given confirmed mixed currencies without FX/valuation-date basis (A-02) | Low | Reversible | Rejected. Violates PACKAGE_SCOPE_AND_ASSUMPTIONS.md currency-aggregation constraint. |

## Controls, tests and acceptance

| Control/test ID | Risk or requirement | Method | Pass criterion | Evidence location | Owner |
|---|---|---|---|---|---|
| CTRL-DGL-01 | No workflow relies solely on a cached authorization status | Test: revoke a user in users_entitlements.csv-equivalent test fixture while access_cache.csv-equivalent cache still shows active; verify workflow denies or re-checks | Workflow denies the action or performs a live re-check; it does not proceed on cached `active` status alone | submission/tests (deferred) | CISO |
| CTRL-DGL-02 | No combined currency total is produced without a cited FX methodology and valuation date | Test using claims.csv mixed-currency rows (CLM-10001 INR, CLM-20042 EUR, CLM-90008 USD) | Output shows per-currency breakdown by default; any combined figure cites FX source and valuation date | submission/tests (deferred) | Chief Actuary |
| CTRL-DGL-03 | Model-backed workflow components verify the deployed artefact matches the approved registry before use | Test using model_artifacts.csv/model_registry.csv mismatch pattern (starter/baseline_diagnostics.py finding) | Workflow refuses to use a mismatched artefact and raises an escalation instead | submission/tests (deferred) | AI Product Owner |
| CTRL-DGL-04 | Accumulation/duplicate-detection outputs are labelled provisional until address/geocode identity resolution is complete | Test using data/addresses.csv six-form / data/geocodes.csv two-geocode pattern (INJ-030) | Output includes an explicit "provisional — address resolution incomplete" label whenever unresolved address variants are detected | submission/tests (deferred) | Data Governance Owner |

## Traceability

| Inject/requirement | Architecture/ADR | Implementation component | Test/evaluation | Residual risk |
|---|---|---|---|---|
| INJ-004 (acquisition integration) | Deferred to submission/artefacts/11_ADR_REGISTER.md | Identifier-mapping/authority-lookup component (not yet implemented) | Not yet defined | Full per-fact-type authority lookup table has not yet been enumerated for all 12 source systems. |
| INJ-010 (cancellation/reinstatement race) | Deferred | Event-ordering reconciliation (not yet implemented) | Not yet defined | Root-cause fix is outside this package's system boundary; only detection/flagging is in scope. |
| INJ-030 (geospatial address collision) | Deferred | Identity-resolution component (not yet implemented) | CTRL-DGL-04 (deferred) | Without the component, all accumulation outputs remain provisional; scope/timeline for building it is not yet set. |
| Stale authorization cache (confirmed defect, starter/baseline_diagnostics.py) | Deferred to submission/artefacts/11_ADR_REGISTER.md | Runtime entitlement re-check (not yet implemented) | CTRL-DGL-01 (deferred) | Degraded-mode fallback (entitlement source itself unavailable) is not yet designed. |
| Model artefact/registry mismatch (confirmed defect, starter/baseline_diagnostics.py) | Deferred | Artefact-verification gate (not yet implemented) | CTRL-DGL-03 (deferred) | Requires a reliable, tamper-resistant registry check; registry availability during an incident is not addressed here. |

## Open issues, residual risk and sign-off

| Issue/risk | Severity | Treatment or acceptance | Accountable owner | Approval/status | Review trigger |
|---|---|---|---|---|---|
| No full per-fact-type authority lookup table exists yet across all 12 source systems | High | Track as a required deliverable for the architecture pass (submission/artefacts/10_C4_ARCHITECTURE.md, deferred) | Data Governance Owner | Open | Before Workflow A/B go-live |
| Confirmed stale-authorization-cache defect has no implemented runtime mitigation yet | High | Non-compensable-gate-adjacent; must be resolved before any workflow performs a gated action | CISO | Open | Before any workflow reaches a user-facing pilot |
| Confirmed model-artefact/registry mismatch has no implemented verification gate yet | High | Same treatment as above | AI Product Owner | Open | Before any model-backed workflow component goes live |
| Address/geocode identity-resolution component does not yet exist | Medium | Accumulation outputs must remain explicitly provisional until built | Data Governance Owner | Open | Before Workflow C accumulation reporting is trusted for planning |
