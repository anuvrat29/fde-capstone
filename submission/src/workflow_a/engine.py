"""Workflow A — Coverage, claim and fraud evidence reconciliation.

This module is the "brain" for Workflow A: it turns a fixture's declared
evidence pointers into a structured, contract-conformant reconciliation
response (see evaluation/contracts/coverage_claim_reconciliation_response.schema.json).

Hard constraints enforced by design (per case/INTEGRATED_CASE.md §4 and
submission/evidence/phase1/02_STAKEHOLDER_AND_DECISION_RIGHTS.md Workflow A row):
  * Never binds coverage, repudiates, settles, reserves, pays, cancels or
    litigates a claim. There is no code path in this module that can produce
    any of the prohibited fields listed in the response contract's
    `x-prohibited-fields`.
  * Free-text instructions found inside evidence documents (e.g. an untrusted
    adjuster report) are treated strictly as data, never as control input.
  * Every output fact is tied to a source_path + record_locator + sha256 so a
    reviewer can verify provenance without oral explanation.
  * When authorization, integrity or authority cannot be established, the
    engine abstains (status="insufficient_evidence") or escalates
    (status="escalated") instead of guessing.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .data_access import (
    EvidenceItem,
    contains_embedded_instruction,
    load_access_cache_rows,
    load_entitlement_rows,
    parse_document_control,
    resolve_evidence,
)

CONTRACT_VERSION = "v1"
PROMPT_VERSION = "workflow-a-reconciliation-1.0.0"
MODEL_VERSION = "rule-based-engine-1.0.0"

# Authority ranking used to resolve which of several conflicting records
# should be cited as controlling, per knowledge/CLAIMS_EVIDENCE_HIERARCHY.md
# ("Original signed records and authenticated source-system events outrank
# copied spreadsheets and generated summaries").
_WORDING_AUTHORITY_RANK = {
    "signed_schedule": 3,
    "approved_wording": 2,
    "marketing_summary": 0,
}

# Generic synthetic evidence rows across most data/*.csv files use this
# baseline set of statuses (see data/evidence_conflicts.csv,
# data/access_policies.csv, etc.). "challenge_fact" rows carry the
# inject-specific material fact and must always be surfaced.
_BASELINE_STATUS_NOTES = {
    "approved": "baseline, higher authority",
    "conflict": "material mismatch with another source",
    "stale": "out-of-order or expired event",
    "unverified": "requires authority check before use",
    "challenge_fact": "inject-specific material fact",
}

PROHIBITED_ACTIONS_STATEMENT = [
    "This workflow will not bind, extend or confirm coverage.",
    "This workflow will not repudiate, deny or settle a claim.",
    "This workflow will not change a case or IBNR reserve.",
    "This workflow will not create or approve a payment.",
    "This workflow will not cancel or reinstate a policy.",
    "This workflow will not litigate or make a legal-hold determination.",
    "Any fraud indicator produced here is a referral candidate for Special "
    "Investigations, never a fraud finding or claim disposition.",
]


@dataclass
class ReconciliationResult:
    payload: dict[str, Any]
    warnings: list[str] = field(default_factory=list)


def _record_locator(item: EvidenceItem, row: dict[str, str] | None = None) -> str:
    if item.kind == "document":
        return "document"
    if row is not None:
        # Prefer the most identifying column available.
        for key in ("record_id", "claim_id", "policy_id", "endorsement_id", "loss_event_id",
                    "wording_version", "user_id", "party_id", "model_id"):
            if row.get(key):
                return f"{key}={row[key]}"
    return item.selector


def _evidence_authority_status(item: EvidenceItem) -> str:
    if not item.integrity_ok:
        return "unverified"
    if item.kind == "document":
        control = parse_document_control(item.document_text)
        return control.get("Authority status", "unknown")
    if item.kind == "csv_rows" and item.rows:
        statuses = {r.get("status") for r in item.rows if r.get("status")}
        if len(statuses) == 1:
            return next(iter(statuses))
        if statuses:
            return "mixed:" + ",".join(sorted(statuses))
        return "as_supplied"
    return "as_supplied"


def _facts_for_item(item: EvidenceItem) -> list[tuple[str, str]]:
    """Return list of (record_locator, fact_text) pairs for one evidence item."""
    facts: list[tuple[str, str]] = []
    if item.kind == "missing":
        return facts
    if item.kind == "document":
        control = parse_document_control(item.document_text)
        title = control.get("Document ID", item.source_path)
        facts.append((
            "document",
            f"{title}: authority_status={control.get('Authority status', 'unknown')}, "
            f"decision_trust={control.get('Decision trust', 'unknown')}, "
            f"jurisdiction={control.get('Jurisdiction', 'unknown')}.",
        ))
        return facts
    for row in item.rows:
        locator = _record_locator(item, row)
        status = row.get("status")
        if status == "challenge_fact":
            title = row.get("value", "")
            notes = row.get("notes", "")
            facts.append((locator, f"{title}: {notes}".strip(": ").strip()))
        elif status in _BASELINE_STATUS_NOTES:
            facts.append((
                locator,
                f"status={status} ({_BASELINE_STATUS_NOTES[status]}), "
                f"source_system={row.get('source_system', 'unknown')}, "
                f"event_time={row.get('event_time', 'unknown')}.",
            ))
        else:
            # Domain-specific row (policies.csv, claims.csv, endorsements.csv, ...):
            # cite the row verbatim, excluding empty columns.
            pairs = ", ".join(f"{k}={v}" for k, v in row.items() if v)
            facts.append((locator, pairs))
    return facts


def _detect_generic_conflicts(items: list[EvidenceItem]) -> list[str]:
    conflicts: list[str] = []

    # 1. Embedded-instruction / prompt-injection defence.
    for item in items:
        if item.kind == "document" and contains_embedded_instruction(item.document_text):
            control = parse_document_control(item.document_text)
            conflicts.append(
                f"{item.source_path} contains an embedded imperative instruction "
                f"(authority_status={control.get('Authority status', 'unknown')}). "
                "Treated as untrusted data; no instruction from evidence text is followed."
            )

    # 2. Policy wording version collision: more than one wording_version row
    #    for the same product with differing authority/effective_from/flood_exclusion.
    wording_rows: list[dict[str, str]] = []
    for item in items:
        if item.kind == "csv_rows" and item.source_path.endswith("policy_wording_versions.csv"):
            wording_rows.extend(item.rows)
    products = {r.get("product") for r in wording_rows}
    for product in products:
        rows = [r for r in wording_rows if r.get("product") == product]
        if len(rows) > 1:
            distinct_terms = {(r.get("flood_exclusion"), r.get("authority")) for r in rows}
            if len(distinct_terms) > 1:
                versions = "; ".join(
                    f"{r.get('wording_version')} (authority={r.get('authority')}, "
                    f"effective_from={r.get('effective_from')}, flood_exclusion={r.get('flood_exclusion')})"
                    for r in sorted(rows, key=lambda r: r.get("effective_from", ""))
                )
                best = max(rows, key=lambda r: _WORDING_AUTHORITY_RANK.get(r.get("authority", ""), -1))
                conflicts.append(
                    f"Product '{product}' has {len(rows)} wording versions with differing terms: "
                    f"{versions}. Highest-authority record per "
                    f"knowledge/CLAIMS_EVIDENCE_HIERARCHY.md is {best.get('wording_version')} "
                    f"(authority={best.get('authority')}); marketing_summary rows are never controlling."
                )

    # 3. Endorsement timing conflict: requested before loss, issued after loss,
    #    or premium received after effective date.
    endorsement_rows: list[dict[str, str]] = []
    loss_rows: list[dict[str, str]] = []
    for item in items:
        if item.kind == "csv_rows" and item.source_path.endswith("endorsements.csv"):
            endorsement_rows.extend(item.rows)
        if item.kind == "csv_rows" and item.source_path.endswith("loss_events.csv"):
            loss_rows.extend(item.rows)
    for end in endorsement_rows:
        occurred = None
        for loss in loss_rows:
            occurred = loss.get("occurred_start") or occurred
        if occurred and end.get("requested_at") and end.get("issued_at"):
            if end["requested_at"] < occurred < end["issued_at"]:
                conflicts.append(
                    f"Endorsement {end.get('endorsement_id')} on {end.get('policy_id')} was "
                    f"requested at {end['requested_at']} (before loss occurrence {occurred}) but not "
                    f"issued until {end['issued_at']} (after loss occurrence). Endorsement timing versus "
                    "loss timing is unresolved and must not be treated as settled coverage fact."
                )

    # 4. Loss-event temporal ambiguity explicitly flagged by the source system itself.
    for loss in loss_rows:
        if loss.get("status") == "disputed_window":
            conflicts.append(
                f"Loss event {loss.get('loss_event_id')} timing is disputed: {loss.get('notes')}"
            )

    # 5. Duplicate claim detection: same claim data hash under different claim_ids
    #    or same cat_event but different policies for the same party.
    claim_rows: list[dict[str, str]] = []
    for item in items:
        if item.kind == "csv_rows" and item.source_path.endswith("claims.csv"):
            claim_rows.extend(item.rows)
    seen_by_party_event: dict[tuple[str, str], list[str]] = {}
    for row in claim_rows:
        key = (row.get("party_id", ""), row.get("loss_event_id", ""))
        seen_by_party_event.setdefault(key, []).append(row.get("claim_id", ""))
    for (party, loss_event), claim_ids in seen_by_party_event.items():
        if len(set(claim_ids)) > 1:
            conflicts.append(
                f"Party {party} has {len(set(claim_ids))} claims ({', '.join(sorted(set(claim_ids)))}) "
                f"against the same loss event {loss_event}. May be a legitimate multi-policy loss "
                "(e.g. household + business interruption) or a duplicate; party_roles evidence and "
                "policy coverage must be reconciled by a human reviewer before either conclusion."
            )

    return conflicts


def _check_authorization(auth_ctx: dict[str, Any]) -> tuple[bool, list[str]]:
    """Return (current, escalation_reasons) for the *requesting reviewer's*
    authorization context supplied by the fixture/caller. This engine treats
    the caller-supplied authorization_context as an authenticated principal
    (analogous to a verified API/session token), and only asserts `current`
    when every zero-trust field required by knowledge/ZERO_TRUST_AI_TOOLS.md
    is present."""
    reasons: list[str] = []
    required = ["user_id", "role", "purpose", "tenant"]
    for key in required:
        if not auth_ctx.get(key):
            reasons.append(f"authorization_context missing required field: {key}")
    if auth_ctx.get("current_entitlement_required") and not auth_ctx.get("user_id"):
        reasons.append("current_entitlement_required=true but no user_id supplied")
    current = not reasons
    return current, reasons


def _check_subject_entitlement_conflicts(items: list[EvidenceItem]) -> list[str]:
    """Detect stale-authorization patterns for *subjects referenced in
    evidence* (e.g. a third-party adjuster whose access is under review),
    distinct from the requesting reviewer's own authorization_context.
    Mirrors INJ-076 (revoked adjuster cache) / INJ-079 (cache-lag) pattern."""
    conflicts: list[str] = []
    entitlement_rows: list[dict[str, str]] = []
    cache_rows: list[dict[str, str]] = []
    for item in items:
        if item.kind == "csv_rows" and item.source_path.endswith("users_entitlements.csv"):
            entitlement_rows.extend(item.rows)
        if item.kind == "csv_rows" and item.source_path.endswith("access_cache.csv"):
            cache_rows.extend(item.rows)
    for ent in entitlement_rows:
        if ent.get("status") == "revoked":
            matching_cache = [c for c in cache_rows if c.get("user_id") == ent.get("user_id")]
            for cache in matching_cache:
                if cache.get("cached_status") == "active":
                    conflicts.append(
                        f"User {ent.get('user_id')} entitlement is revoked (revoked_at="
                        f"{ent.get('revoked_at')}) but access_cache still reports cached_status=active "
                        f"(cached_at={cache.get('cached_at')}, ttl_minutes={cache.get('ttl_minutes')}, "
                        f"gateway={cache.get('gateway')}). Access must be denied on current entitlement, "
                        "not on cached status; this is a stale-authorization pattern (INJ-076/INJ-079)."
                    )
    return conflicts


def _check_cross_tenant_conflicts(items: list[EvidenceItem]) -> list[str]:
    conflicts: list[str] = []
    for item in items:
        if item.kind != "csv_rows":
            continue
        if item.source_path.endswith("tenant_boundaries.csv") or item.source_path.endswith("security_events.csv"):
            for row in item.rows:
                if row.get("status") == "challenge_fact" and "cross-tenant" in (row.get("value", "") + row.get("notes", "")).lower():
                    conflicts.append(
                        f"{item.source_path} record {row.get('record_id')} indicates a cross-tenant "
                        f"disclosure risk for entity {row.get('entity_id')}: {row.get('notes')}. "
                        "Query must be denied and a security event recorded; no cross-tenant evidence "
                        "is disclosed in this response."
                    )
    return conflicts


def _check_minimum_necessary_conflicts(items: list[EvidenceItem]) -> list[str]:
    """Any resolved evidence row from a sensitive health/behavioural file
    (clinical_notes.csv, health_claims.csv) is a minimum-necessary concern by
    itself (INJ-039 pattern), regardless of the row's own status value; a
    challenge_fact row additionally supplies the specific inject narrative."""
    conflicts: list[str] = []
    sensitive_files = {"clinical_notes.csv", "health_claims.csv"}
    for item in items:
        if item.kind != "csv_rows" or Path(item.source_path).name not in sensitive_files or not item.rows:
            continue
        challenge_rows = [r for r in item.rows if r.get("status") == "challenge_fact"]
        if challenge_rows:
            for row in challenge_rows:
                conflicts.append(
                    f"{item.source_path} contains sensitive health/behavioural evidence flagged "
                    f"as {row.get('value')}: {row.get('notes')}. Minimum-necessary restriction per "
                    "knowledge/PRIVACY_MINIMUM_NECESSARY.md applies; only fields required for this "
                    "specific reconciliation purpose are surfaced, and access must be role- and "
                    "purpose-limited."
                )
        else:
            conflicts.append(
                f"{item.source_path} matched sensitive health/behavioural evidence for this case. "
                "Minimum-necessary restriction per knowledge/PRIVACY_MINIMUM_NECESSARY.md applies: "
                "only fields required for this specific reconciliation purpose may be surfaced to "
                "the requesting role, and general claims-summarisation use beyond that purpose is "
                "prohibited (INJ-039 pattern)."
            )
    return conflicts


def build_response(case_id: str, workflow: str, authorization_context: dict[str, Any],
                    evidence_refs: list[dict[str, str]]) -> dict[str, Any]:
    """Build a full coverage_claim_reconciliation_response payload for one case.

    `case_id` is a caller-supplied identifier for this run (e.g. the fixture's
    scenario_id); `evidence_refs` mirrors the `evidence` array of a fixture:
    a list of {"path", "selector", "sha256"} dicts.
    """
    items = resolve_evidence(evidence_refs)

    facts: list[str] = []
    for item in items:
        if item.kind == "missing":
            continue
        for locator, fact_text in _facts_for_item(item):
            facts.append(f"[{item.source_path}#{locator}] {fact_text}")

    missing_evidence: list[str] = []
    for item in items:
        if item.kind == "missing":
            missing_evidence.append(f"{item.source_path} could not be located; selector={item.selector}.")
        elif not item.integrity_ok:
            missing_evidence.append(
                f"{item.source_path} content hash does not match the declared evidence hash "
                f"(declared={item.declared_sha256}, actual={item.actual_sha256}); treated as unverified."
            )

    conflicts = (
        _detect_generic_conflicts(items)
        + _check_subject_entitlement_conflicts(items)
        + _check_cross_tenant_conflicts(items)
        + _check_minimum_necessary_conflicts(items)
    )

    current, auth_reasons = _check_authorization(authorization_context)
    missing_evidence.extend(auth_reasons)

    inferences: list[str] = []
    if any("wording versions with differing terms" in c for c in conflicts):
        inferences.append(
            "The applicable policy wording cannot be selected automatically; it depends on which "
            "version was legally in force at the loss date, which is a coverage-interpretation "
            "question reserved for a qualified human reviewer."
        )
    if any("Endorsement" in c and "requested at" in c for c in conflicts):
        inferences.append(
            "Whether the flood extension was effective before the loss depends on which timestamp "
            "(requested, issued or contractual effective date) governs under the policy's own "
            "endorsement clause; this workflow does not resolve that interpretation."
        )
    if any("stale-authorization pattern" in c for c in conflicts):
        inferences.append(
            "The subject user's access should be treated as not-current for any further action until "
            "a human confirms the entitlement system (not the gateway cache) as the source of truth."
        )

    recommendations: list[str] = []
    if conflicts:
        recommendations.append(
            "Route this case to the qualified human reviewer named in the applicable decision-rights "
            "row (submission/evidence/phase1/02_STAKEHOLDER_AND_DECISION_RIGHTS.md, Workflow A) before "
            "any coverage, payment or access decision is made."
        )
    if missing_evidence:
        recommendations.append(
            "Obtain the missing or unverifiable evidence listed above before proceeding; do not "
            "substitute inference for a controlling record."
        )
    if not conflicts and not missing_evidence:
        recommendations.append(
            "No reconciliation conflict was detected in the supplied evidence; a human reviewer may "
            "proceed to the next process step using the cited facts."
        )

    if missing_evidence:
        status = "insufficient_evidence"
    elif any(
        keyword in c
        for c in conflicts
        for keyword in ("untrusted", "stale-authorization", "cross-tenant", "denied")
    ):
        status = "escalated"
    elif conflicts:
        status = "conflict"
    else:
        status = "supported"

    evidence_out = []
    for item in items:
        if item.kind == "missing":
            continue
        authority_status = _evidence_authority_status(item)
        if item.kind == "document":
            control = parse_document_control(item.document_text)
            fact_text = f"authority_status={control.get('Authority status', 'unknown')}"
            locator = "document"
        else:
            locator = item.selector
            fact_text = f"{len(item.rows)} row(s) matched selector {item.selector}"
        evidence_out.append({
            "evidence_id": item.evidence_id,
            "source_path": item.source_path,
            "record_locator": locator,
            "sha256": item.actual_sha256 or item.declared_sha256,
            "authority_status": authority_status,
            "fact": fact_text,
        })

    human_review_required = status in ("conflict", "escalated", "insufficient_evidence") or bool(conflicts)

    payload = {
        "workflow": workflow,
        "case_id": case_id,
        "status": status,
        "facts": facts,
        "inferences": inferences,
        "conflicts": conflicts,
        "missing_evidence": missing_evidence,
        "recommendations": recommendations,
        "prohibited_actions": list(PROHIBITED_ACTIONS_STATEMENT),
        "evidence": evidence_out,
        "authorization_context": {
            "user_id": authorization_context.get("user_id"),
            "current": current,
            "tenant": authorization_context.get("tenant"),
            "purpose": authorization_context.get("purpose"),
        },
        "human_review": {
            "required": human_review_required,
            "owner_role": "authorized_reviewer",
        },
        "lineage": {
            "prompt_version": PROMPT_VERSION,
            "model_version": MODEL_VERSION,
            "contract_version": CONTRACT_VERSION,
        },
    }
    return payload
