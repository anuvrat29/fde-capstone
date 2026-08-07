"""Workflow C — Catastrophe and reinsurance planning support.

Mirrors the structure of submission/src/workflow_a/engine.py and
submission/src/workflow_b/engine.py but targets the
catastrophe_reinsurance_planning_response.schema.json contract and the
catastrophe/reinsurance injects (parametric trigger wording/sensor conflicts,
treaty hours-clause/event-aggregation ambiguity, mixed-currency bordereaux,
checkpoint-replay duplicate payment/notice risk, ransomware degraded-mode
continuity).

Hard constraints enforced by design (per case/INTEGRATED_CASE.md §4 and the
Workflow C row in submission's decision-rights artefact):
  * Never changes a reserve, concludes or submits a recovery, submits a
    reinsurance notice, places treaty business or creates/instructs a
    payment. No field in this module can ever populate a response
    contract's `x-prohibited-fields` (reserve_change, recovery_amount,
    recovery_conclusion, notice_submitted, treaty_placement,
    payment_instruction, payment_created).
  * A parametric trigger or event-aggregation ambiguity is surfaced as a
    conflict with alternative views, never resolved into a single trigger
    determination or recovery figure.
  * Mixed-currency/valuation-date evidence is never summed or converted
    without an explicit valuation rule; the mismatch itself is the finding.
  * A checkpoint-replay / stale-agent-state pattern is escalated and denied,
    never allowed to produce a duplicate draft payment or notice action.
  * During a degraded-mode (e.g. ransomware containment) incident, the
    engine only ever recommends operating from authorized snapshots and
    documented manual fallback steps; it never invents a data source.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from workflow_a.data_access import (
    EvidenceItem,
    contains_embedded_instruction,
    parse_document_control,
    resolve_evidence,
)

CONTRACT_VERSION = "v1"
PROMPT_VERSION = "workflow-c-catastrophe-reinsurance-1.0.0"
MODEL_VERSION = "rule-based-engine-1.0.0"

_BASELINE_STATUS_NOTES = {
    "approved": "baseline, higher authority",
    "conflict": "material mismatch with another source",
    "stale": "out-of-order or expired event",
    "unverified": "requires authority check before use",
    "challenge_fact": "inject-specific material fact",
}

PROHIBITED_ACTIONS_STATEMENT = [
    "This workflow will not change a case or IBNR reserve.",
    "This workflow will not conclude or submit a reinsurance recovery.",
    "This workflow will not submit a reinsurance notice.",
    "This workflow will not place or bind treaty business.",
    "This workflow will not create or instruct a payment.",
    "This workflow will not determine a parametric trigger outcome.",
    "Any aggregation, currency or trigger ambiguity produced here is a "
    "referral to the accountable human reviewer, never an automated "
    "recovery or notice decision.",
]


@dataclass
class ReconciliationResult:
    payload: dict[str, Any]
    warnings: list[str] = field(default_factory=list)


def _record_locator(item: EvidenceItem, row: dict[str, str] | None = None) -> str:
    if item.kind == "document":
        return "document"
    if row is not None:
        for key in ("record_id", "event_id", "treaty_id", "entity_id", "capability",
                    "claim", "policy_id", "claim_id"):
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
        if control:
            facts.append((
                "document",
                f"{title}: authority_status={control.get('Authority status', 'unknown')}, "
                f"decision_trust={control.get('Decision trust', 'unknown')}, "
                f"jurisdiction={control.get('Jurisdiction', 'unknown')}.",
            ))
        else:
            # Non-knowledge document (e.g. a starter/api_samples/*.json bordereaux
            # extract): cite its raw text as a single fact rather than a
            # document-control summary.
            snippet = " ".join(item.document_text.split())[:300]
            facts.append(("document", f"{item.source_path}: {snippet}"))
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
            # Domain-specific row (reinsurance_treaties.csv, cat_events.csv, ...):
            # cite the row verbatim, excluding empty columns.
            pairs = ", ".join(f"{k}={v}" for k, v in row.items() if v)
            facts.append((locator, pairs))
    return facts


def _check_parametric_trigger_conflicts(items: list[EvidenceItem]) -> list[str]:
    """INJ-012/INJ-034 pattern: parametric_contracts.csv/weather_observations.csv
    challenge_fact rows report wording (brochure vs contract index) or sensor
    (station vs satellite) disagreement. The engine surfaces alternative
    readings and never resolves a single trigger determination itself."""
    conflicts: list[str] = []
    for item in items:
        if item.kind != "csv_rows":
            continue
        if Path(item.source_path).name in {"parametric_contracts.csv", "weather_observations.csv"}:
            for row in item.rows:
                if row.get("status") == "challenge_fact":
                    conflicts.append(
                        f"{item.source_path} record {row.get('record_id')} reports a parametric "
                        f"trigger conflict: {row.get('value')} — {row.get('notes')}. Per "
                        "knowledge/PARAMETRIC_TRIGGER_AUTHORITY.md, the signed index definition, "
                        "station, observation period and fallback methodology control; marketing "
                        "descriptions are non-authoritative. This workflow presents both readings "
                        "and does not itself determine whether the trigger was met."
                    )
                elif row.get("status") in {"unverified", "conflict"}:
                    conflicts.append(
                        f"{item.source_path} record {row.get('record_id')} requires an authority "
                        f"check before use (status={row.get('status')}, source_system="
                        f"{row.get('source_system')}, event_time={row.get('event_time')}), "
                        "consistent with a station/satellite/contract authority reconciliation "
                        "concern. Per knowledge/PARAMETRIC_TRIGGER_AUTHORITY.md, the signed index "
                        "definition, station, observation period and fallback methodology control; "
                        "this workflow presents both readings and does not itself determine whether "
                        "the trigger was met."
                    )
    return conflicts


def _check_event_aggregation_conflicts(items: list[EvidenceItem]) -> list[str]:
    """INJ-039/INJ-040 pattern: multiple cat_events.csv rows referenced by one
    treaty claim have different hours_clause/definition_owner, and the
    treaty's own hours_clause differs by peril. Aggregation into a single
    recoverable event is ambiguous; the engine produces alternative
    aggregation views, never a single recovery submission."""
    conflicts: list[str] = []
    event_rows: list[dict[str, str]] = []
    treaty_rows: list[dict[str, str]] = []
    seen_event_ids: set[str] = set()
    for item in items:
        if item.kind == "csv_rows" and item.source_path.endswith("cat_events.csv"):
            for row in item.rows:
                key = row.get("event_id", "")
                if key and key not in seen_event_ids:
                    seen_event_ids.add(key)
                    event_rows.append(row)
        if item.kind == "csv_rows" and item.source_path.endswith("reinsurance_treaties.csv"):
            treaty_rows.extend(item.rows)
    if len(event_rows) > 1:
        distinct = {(r.get("hours_clause"), r.get("definition_owner")) for r in event_rows}
        if len(distinct) > 1:
            details = "; ".join(
                f"{r.get('event_id')} ({r.get('name')}, hours_clause={r.get('hours_clause')}h, "
                f"definition_owner={r.get('definition_owner')})"
                for r in event_rows
            )
            treaty_note = ""
            for treaty in treaty_rows:
                if treaty.get("hours_clause"):
                    treaty_note = f" Treaty {treaty.get('treaty_id')}'s own hours_clause is " \
                                  f"'{treaty.get('hours_clause')}', which itself varies by peril."
            conflicts.append(
                f"{len(event_rows)} catastrophe events are referenced with differing hours-clause "
                f"ownership/duration: {details}.{treaty_note} Per "
                "knowledge/REINSURANCE_EVENT_AGGREGATION.md, treaty-specific event definitions must "
                "be applied using signed wording and documented judgment; this workflow presents "
                "alternative aggregation views (single-event vs split-event) and does not itself "
                "submit a recovery under either view."
            )
    return conflicts


def _check_currency_valuation_conflicts(items: list[EvidenceItem]) -> list[str]:
    """INJ-042/INJ-053 pattern: bordereaux.csv/fx_rates.csv challenge_fact rows,
    or a bordereaux extract document, report multiple currencies and/or
    valuation dates in the same claim set. Per starter/baseline_diagnostics.py
    finding #1, mixed currencies must never be summed without an explicit
    valuation rule."""
    conflicts: list[str] = []
    for item in items:
        if item.kind == "csv_rows" and Path(item.source_path).name in {"bordereaux.csv", "fx_rates.csv"}:
            for row in item.rows:
                if row.get("status") == "challenge_fact":
                    conflicts.append(
                        f"{item.source_path} record {row.get('record_id')} reports {row.get('value')}: "
                        f"{row.get('notes')}. Per starter/baseline_diagnostics.py finding #1, mixed "
                        "currencies cannot be summed without valuation rules; this workflow reports "
                        "amounts per their original currency/valuation date and does not aggregate "
                        "them into a single total."
                    )
        if item.kind == "document" and Path(item.source_path).suffix == ".json":
            text = item.document_text
            currencies_found = {c for c in ("USD", "EUR", "INR", "GBP") if f'"{c}"' in text}
            if len(currencies_found) > 1:
                conflicts.append(
                    f"{item.source_path} contains claim rows denominated in {len(currencies_found)} "
                    f"different currencies ({', '.join(sorted(currencies_found))}) with distinct "
                    "valuation dates. These amounts must not be summed into a single bordereaux "
                    "total without an explicit valuation-date and FX-rate rule from a qualified "
                    "reviewer."
                )
    return conflicts


def _check_checkpoint_replay_conflicts(items: list[EvidenceItem]) -> list[str]:
    """INJ-094 pattern: agent_runs.csv/idempotency_records.csv challenge_fact
    rows report a recovery agent resuming stale state and creating duplicate
    draft payments/notices. Must escalate and deny; never allow a duplicate
    payment_instruction or notice_submitted action to be produced."""
    conflicts: list[str] = []
    for item in items:
        if item.kind != "csv_rows":
            continue
        if Path(item.source_path).name in {"agent_runs.csv", "idempotency_records.csv"}:
            for row in item.rows:
                if row.get("status") == "challenge_fact":
                    conflicts.append(
                        f"{item.source_path} record {row.get('record_id')} reports a checkpoint-"
                        f"replay pattern: {row.get('value')} — {row.get('notes')}. Any duplicate "
                        "draft payment or reinsurer notice arising from resumed stale agent state "
                        "must be denied and recorded; this workflow will not create or resubmit a "
                        "payment or notice action for a case with an unresolved replay finding."
                    )
    return conflicts


def _check_degraded_mode_continuity_conflicts(items: list[EvidenceItem]) -> list[str]:
    """INJ-091/INJ-093/INJ-096 pattern: an open-ended downtime_events.csv row
    (no end timestamp) for a capability with a continuity_requirements.csv
    max_ai_outage_days ceiling means the workflow must operate from
    authorized snapshots/manual fallback steps only, not invent data."""
    conflicts: list[str] = []
    downtime_rows: list[dict[str, str]] = []
    continuity_rows: list[dict[str, str]] = []
    fallback_rows: list[dict[str, str]] = []
    for item in items:
        if item.kind == "csv_rows" and item.source_path.endswith("downtime_events.csv"):
            downtime_rows.extend(item.rows)
        if item.kind == "csv_rows" and item.source_path.endswith("continuity_requirements.csv"):
            continuity_rows.extend(item.rows)
        if item.kind == "csv_rows" and item.source_path.endswith("manual_fallback_steps.csv"):
            fallback_rows.extend(item.rows)
    for down in downtime_rows:
        if not down.get("end"):
            cap_note = ""
            for cap in continuity_rows:
                cap_note = (
                    f" Continuity requirement for {cap.get('capability')}: "
                    f"max_ai_outage_days={cap.get('max_ai_outage_days')}, "
                    f"manual_mode={cap.get('manual_mode')}."
                )
                break
            fallback_note = " No manual fallback step evidence was supplied." if not fallback_rows else \
                f" {len(fallback_rows)} manual fallback step record(s) available."
            conflicts.append(
                f"data/downtime_events.csv record {down.get('event_id')} ({down.get('system')}, "
                f"cause={down.get('cause')}) has no recorded end timestamp and is treated as "
                f"still-ongoing.{cap_note}{fallback_note} Per the continuity requirement, this "
                "workflow must operate from authorized snapshots and documented manual fallback "
                "steps only for the duration of the incident, and must not silently invent or "
                "infer a data source that was not supplied."
            )

    # Cross-border replica finding (INJ-072 pattern, reused here as a
    # continuity-adjacent privacy/residency concern when backup_inventory.csv
    # is supplied for this workflow).
    for item in items:
        if item.kind == "csv_rows" and item.source_path.endswith("backup_inventory.csv"):
            for row in item.rows:
                if row.get("status") == "challenge_fact":
                    conflicts.append(
                        f"{item.source_path} record {row.get('record_id')} reports {row.get('value')}: "
                        f"{row.get('notes')}. Any degraded-mode snapshot restore must not rely on a "
                        "replica outside its approved region without a separate residency review."
                    )
    return conflicts


def _check_authorization(auth_ctx: dict[str, Any]) -> tuple[bool, list[str]]:
    """Return (current, escalation_reasons) for the requesting reviewer's
    authorization context, mirroring Workflows A and B's zero-trust check."""
    reasons: list[str] = []
    required = ["user_id", "role", "purpose", "tenant"]
    for key in required:
        if not auth_ctx.get(key):
            reasons.append(f"authorization_context missing required field: {key}")
    if auth_ctx.get("current_entitlement_required") and not auth_ctx.get("user_id"):
        reasons.append("current_entitlement_required=true but no user_id supplied")
    current = not reasons
    return current, reasons


def _detect_generic_conflicts(items: list[EvidenceItem]) -> list[str]:
    conflicts: list[str] = []
    for item in items:
        if item.kind == "document" and contains_embedded_instruction(item.document_text):
            control = parse_document_control(item.document_text)
            conflicts.append(
                f"{item.source_path} contains an embedded imperative instruction "
                f"(authority_status={control.get('Authority status', 'unknown')}). "
                "Treated as untrusted data; no instruction from evidence text is followed."
            )
    return conflicts


def build_response(case_id: str, workflow: str, authorization_context: dict[str, Any],
                    evidence_refs: list[dict[str, str]]) -> dict[str, Any]:
    """Build a full catastrophe_reinsurance_planning_response payload for one
    case.

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
        + _check_parametric_trigger_conflicts(items)
        + _check_event_aggregation_conflicts(items)
        + _check_currency_valuation_conflicts(items)
        + _check_checkpoint_replay_conflicts(items)
        + _check_degraded_mode_continuity_conflicts(items)
    )

    current, auth_reasons = _check_authorization(authorization_context)
    missing_evidence.extend(auth_reasons)

    inferences: list[str] = []
    if any("does not itself determine whether the trigger was met" in c for c in conflicts):
        inferences.append(
            "Whether the parametric trigger was met depends on which index source (station vs "
            "satellite vs contract-defined fallback) governs, a coverage-interpretation question "
            "reserved for a qualified human reviewer."
        )
    if any("aggregation views (single-event vs split-event)" in c for c in conflicts):
        inferences.append(
            "The total recoverable amount depends on which event-aggregation view a qualified "
            "reviewer selects; this workflow does not choose between them."
        )
    if any("cannot be summed without valuation rules" in c for c in conflicts):
        inferences.append(
            "A single bordereaux total cannot be produced until a reviewer supplies the applicable "
            "FX rate and valuation-date convention."
        )
    if any("checkpoint-replay pattern" in c for c in conflicts):
        inferences.append(
            "The case's payment/notice state should be treated as unresolved until a human "
            "confirms the idempotency ledger (not the agent's resumed run) as the source of truth."
        )
    if any("still-ongoing" in c for c in conflicts):
        inferences.append(
            "Until the downtime event is confirmed closed, any output for this capability should "
            "be treated as produced under degraded-mode continuity procedures, not normal operation."
        )

    recommendations: list[str] = []
    if conflicts:
        recommendations.append(
            "Route this case to the qualified human reviewer named in the applicable decision-rights "
            "row (submission/evidence/phase1/02_STAKEHOLDER_AND_DECISION_RIGHTS.md, Workflow C) before "
            "any recovery, notice, treaty placement or payment action is taken."
        )
    if missing_evidence:
        recommendations.append(
            "Obtain the missing or unverifiable evidence listed above before proceeding; do not "
            "substitute inference for a controlling record."
        )
    if not conflicts and not missing_evidence:
        recommendations.append(
            "No reconciliation conflict was detected in the supplied evidence; a human reviewer may "
            "proceed to the next catastrophe/reinsurance planning step using the cited facts."
        )

    if missing_evidence:
        status = "insufficient_evidence"
    elif any(
        keyword in c
        for c in conflicts
        for keyword in ("checkpoint-replay pattern", "still-ongoing", "untrusted")
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
            fact_text = f"authority_status={control.get('Authority status', 'unknown')}" if control else \
                "non-knowledge document evidence"
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
