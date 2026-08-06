"""Workflow B — Underwriting and pricing decision support.

Mirrors the structure of submission/src/workflow_a/engine.py but targets the
underwriting_pricing_support_response.schema.json contract and the
underwriting/pricing injects (fairness/proxy pricing, telematics firmware
drift, life contestability, vendor price-shock/cost-budget pressure).

Hard constraints enforced by design (per case/INTEGRATED_CASE.md §4 and the
Workflow B row in submission's decision-rights artefact):
  * Never binds, prices, declines, repudiates, reserves, settles, pays,
    cancels, places treaty business or submits a recovery. No field in this
    module can ever populate a response contract's `x-prohibited-fields`
    (binding_decision, bind, decline, accept, final_price, premium,
    adverse_action, policy_issued).
  * A confirmed fairness/model-governance breach is surfaced as a conflict
    and an immediate use restriction recommendation, never silently
    smoothed into a price or accept/decline outcome.
  * Free text embedded in knowledge/*.md evidence is treated strictly as
    data, never as a control instruction (same prompt-injection defence as
    Workflow A).
  * When authorization, integrity or model-authority cannot be established,
    the engine abstains (status="insufficient_evidence") or escalates
    (status="escalated") instead of guessing a pricing/underwriting outcome.
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
PROMPT_VERSION = "workflow-b-underwriting-pricing-1.0.0"
MODEL_VERSION = "rule-based-engine-1.0.0"

# Generic synthetic evidence rows across most data/*.csv files use this
# baseline set of statuses (see data/pricing_factors.csv, data/cost_model.csv,
# etc.). "challenge_fact" rows carry the inject-specific material fact and
# must always be surfaced.
_BASELINE_STATUS_NOTES = {
    "approved": "baseline, higher authority",
    "conflict": "material mismatch with another source",
    "stale": "out-of-order or expired event",
    "unverified": "requires authority check before use",
    "challenge_fact": "inject-specific material fact",
}

PROHIBITED_ACTIONS_STATEMENT = [
    "This workflow will not bind, extend or confirm coverage.",
    "This workflow will not price, quote or issue a policy.",
    "This workflow will not accept or decline an application.",
    "This workflow will not take an adverse action against an applicant or insured.",
    "This workflow will not change a premium, rate or underwriting tier.",
    "This workflow will not repudiate a life or general claim.",
    "Any fairness or model-governance finding produced here is a referral to "
    "the Model Risk Owner / Chief Actuary, never an automated remediation.",
]


@dataclass
class ReconciliationResult:
    payload: dict[str, Any]
    warnings: list[str] = field(default_factory=list)


def _record_locator(item: EvidenceItem, row: dict[str, str] | None = None) -> str:
    if item.kind == "document":
        return "document"
    if row is not None:
        for key in ("record_id", "model_id", "entity_id", "policy_id", "claim_id",
                    "provider", "subgroup", "user_id"):
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
            # Domain-specific row (fairness_metrics.csv, model_registry.csv, ...):
            # cite the row verbatim, excluding empty columns.
            pairs = ", ".join(f"{k}={v}" for k, v in row.items() if v)
            facts.append((locator, pairs))
    return facts


def _check_fairness_breach_conflicts(items: list[EvidenceItem]) -> list[str]:
    """INJ-013/INJ-065 pattern: fairness_metrics.csv reports a confirmed
    subgroup breach/review for a model, cross-referenced against
    model_registry.csv's approval status. A breach must never be smoothed
    into a price or accept/decline outcome; it is a use-restriction finding."""
    conflicts: list[str] = []
    fairness_rows: list[dict[str, str]] = []
    registry_rows: list[dict[str, str]] = []
    for item in items:
        if item.kind == "csv_rows" and item.source_path.endswith("fairness_metrics.csv"):
            fairness_rows.extend(item.rows)
        if item.kind == "csv_rows" and item.source_path.endswith("model_registry.csv"):
            registry_rows.extend(item.rows)
    for row in fairness_rows:
        if row.get("status") in {"breach", "review"}:
            model_id = row.get("model_id", "")
            registry_match = next((r for r in registry_rows if r.get("model_id") == model_id), None)
            approval = registry_match.get("approval_status") if registry_match else "unknown"
            severity = "confirmed breach" if row.get("status") == "breach" else "flagged for review"
            conflicts.append(
                f"Model {model_id} has a {severity} for subgroup {row.get('subgroup')} "
                f"(selection_rate={row.get('selection_rate')} vs reference_rate="
                f"{row.get('reference_rate')}, threshold={row.get('threshold')}); registry "
                f"approval_status={approval}. This finding must not be resolved into a price, "
                "acceptance or decline outcome by this workflow; it is a use-restriction referral "
                "to the Model Risk Owner and Chief Actuary."
            )
    return conflicts


def _check_conditional_model_conflicts(items: list[EvidenceItem]) -> list[str]:
    """A model_registry.csv row with approval_status=conditional (e.g.
    GEN-SUM-3) means the model's output may only be used under the stated
    conditions; this workflow surfaces that constraint rather than treating
    the model's output as unconditionally trusted."""
    conflicts: list[str] = []
    for item in items:
        if item.kind != "csv_rows" or not item.source_path.endswith("model_registry.csv"):
            continue
        for row in item.rows:
            if row.get("approval_status") == "conditional":
                conflicts.append(
                    f"Model {row.get('model_id')} ({row.get('purpose')}) has approval_status="
                    "conditional in the model registry; its output may only be used under the "
                    "conditions attached to that approval, not treated as unconditionally trusted."
                )
    return conflicts


def _check_firmware_drift_conflicts(items: list[EvidenceItem]) -> list[str]:
    """INJ-014/INJ-015 pattern: a device_firmware.csv or vehicle_telemetry.csv
    row reports a semantic change (firmware update, telemetry aggregation
    change) — either the inject-specific `challenge_fact` row, or a
    `conflict` row showing a material mismatch versus the device/telemetry
    baseline — without a corresponding pricing-model recalibration record.
    The engine must abstain from any score/price adjustment based on
    telemetry collected across the semantic change boundary."""
    conflicts: list[str] = []
    for item in items:
        if item.kind != "csv_rows":
            continue
        if Path(item.source_path).name in {"device_firmware.csv", "vehicle_telemetry.csv"}:
            for row in item.rows:
                if row.get("status") == "challenge_fact":
                    conflicts.append(
                        f"{item.source_path} record {row.get('record_id')} reports a semantic "
                        f"change: {row.get('value')} — {row.get('notes')}. No recalibration record "
                        "was supplied confirming the pricing/scoring model was re-validated after "
                        "this change; any telemetry-derived score spanning the change boundary is "
                        "unsupported and must not be used for automated pricing."
                    )
                elif row.get("status") == "conflict":
                    conflicts.append(
                        f"{item.source_path} record {row.get('record_id')} shows a material "
                        f"mismatch versus the device/telemetry baseline (source_system="
                        f"{row.get('source_system')}, event_time={row.get('event_time')}), "
                        "consistent with an unrecorded firmware/telemetry semantic change. No "
                        "recalibration record was supplied confirming the pricing/scoring model was "
                        "re-validated after this change; any telemetry-derived score spanning the "
                        "change boundary is unsupported and must not be used for automated pricing."
                    )
    return conflicts


def _check_life_contestability_conflicts(items: list[EvidenceItem]) -> list[str]:
    """INJ-025/INJ-028 pattern: life_applications.csv, life_claims.csv and
    medical_evidence.csv challenge_fact rows report contradictory disclosure
    or clinical evidence near the contestability boundary. This workflow
    constructs the timeline as fact and escalates; it never repudiates or
    confirms a life claim itself."""
    conflicts: list[str] = []
    life_files = {"life_applications.csv", "life_claims.csv", "medical_evidence.csv"}
    challenge_rows: list[tuple[str, dict[str, str]]] = []
    for item in items:
        if item.kind == "csv_rows" and Path(item.source_path).name in life_files:
            for row in item.rows:
                if row.get("status") == "challenge_fact":
                    challenge_rows.append((item.source_path, row))
    if challenge_rows:
        sources = ", ".join(sorted({src for src, _ in challenge_rows}))
        conflicts.append(
            f"Contradictory or boundary-relevant life underwriting/claims evidence found across "
            f"{sources}: " + "; ".join(
                f"{row.get('value')} ({row.get('notes')})" for _, row in challenge_rows
            ) + ". Contestability determination is a qualified human legal and claims decision "
            "per knowledge/LIFE_CONTESTABILITY_GUIDE.md; this workflow constructs the timeline "
            "only and does not repudiate, confirm or pay the claim."
        )
    return conflicts


def _check_vendor_price_shock_conflicts(items: list[EvidenceItem]) -> list[str]:
    """INJ-089/INJ-091 pattern: model_costs.csv reports a material price
    increase for a provider/model already in use; token_budgets.csv or
    cost_model.csv challenge_fact rows report unmodelled cost categories.
    The engine surfaces the cost pressure without silently degrading model
    choice or hiding a resulting quality impact."""
    conflicts: list[str] = []
    for item in items:
        if item.kind != "csv_rows" or not item.source_path.endswith("model_costs.csv"):
            continue
        for row in item.rows:
            change = (row.get("change") or "").lower()
            if "increase" in change:
                conflicts.append(
                    f"Vendor {row.get('provider')} model {row.get('model')} has a cost change of "
                    f"'{row.get('change')}' effective {row.get('effective_date')} "
                    f"(input={row.get('input_per_million')}/M, output={row.get('output_per_million')}/M "
                    f"{row.get('currency')}). No budget-response decision (absorb/substitute/renegotiate) "
                    "was supplied; any downstream substitution to a cheaper model must disclose the "
                    "resulting quality impact, not hide it behind a cost saving."
                )
    for item in items:
        if item.kind != "csv_rows" or Path(item.source_path).name not in {"token_budgets.csv", "cost_model.csv"}:
            continue
        for row in item.rows:
            if row.get("status") == "challenge_fact":
                conflicts.append(
                    f"{item.source_path} record {row.get('record_id')} flags an unmodelled cost "
                    f"category: {row.get('value')} — {row.get('notes')}. Unit-cost/budget figures "
                    "derived without this category are understated and must not be presented as "
                    "complete."
                )
    return conflicts


def _check_authorization(auth_ctx: dict[str, Any]) -> tuple[bool, list[str]]:
    """Return (current, escalation_reasons) for the requesting reviewer's
    authorization context, mirroring Workflow A's zero-trust check."""
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
    # Embedded-instruction / prompt-injection defence, same as Workflow A.
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
    """Build a full underwriting_pricing_support_response payload for one case.

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
        + _check_fairness_breach_conflicts(items)
        + _check_conditional_model_conflicts(items)
        + _check_firmware_drift_conflicts(items)
        + _check_life_contestability_conflicts(items)
        + _check_vendor_price_shock_conflicts(items)
    )

    current, auth_reasons = _check_authorization(authorization_context)
    missing_evidence.extend(auth_reasons)

    inferences: list[str] = []
    if any("must not be resolved into a price, acceptance or decline outcome" in c for c in conflicts):
        inferences.append(
            "The confirmed/flagged fairness finding indicates the affected model's pricing output "
            "should not be relied on for the affected subgroup until the Model Risk Owner and Chief "
            "Actuary choose a remediation approach (retrain, feature removal or retirement)."
        )
    if any("unsupported and must not be used for automated pricing" in c for c in conflicts):
        inferences.append(
            "Whether the pre- and post-firmware telemetry can be safely combined depends on a "
            "recalibration exercise this workflow cannot perform; treat any derived risk score as "
            "provisional until that recalibration is confirmed."
        )
    if any("qualified human legal and claims decision" in c for c in conflicts):
        inferences.append(
            "The contestability outcome depends on which disclosure was accurate at application "
            "time, a factual and legal question this workflow does not resolve."
        )
    if any("budget-response decision" in c for c in conflicts):
        inferences.append(
            "Absorbing, substituting or renegotiating the vendor price increase is a budget-owner "
            "decision with a quality trade-off attached; this workflow surfaces the trade-off but "
            "does not choose among the options."
        )

    recommendations: list[str] = []
    if conflicts:
        recommendations.append(
            "Route this case to the qualified human reviewer named in the applicable decision-rights "
            "row (submission/evidence/phase1/02_STAKEHOLDER_AND_DECISION_RIGHTS.md, Workflow B) before "
            "any pricing, acceptance, decline or adverse-action decision is made."
        )
    if missing_evidence:
        recommendations.append(
            "Obtain the missing or unverifiable evidence listed above before proceeding; do not "
            "substitute inference for a controlling record."
        )
    if not conflicts and not missing_evidence:
        recommendations.append(
            "No reconciliation conflict was detected in the supplied evidence; a human reviewer may "
            "proceed to the next underwriting process step using the cited facts."
        )

    if missing_evidence:
        status = "insufficient_evidence"
    elif any(
        keyword in c
        for c in conflicts
        for keyword in ("confirmed breach", "untrusted")
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
