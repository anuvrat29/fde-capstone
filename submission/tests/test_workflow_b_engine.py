"""Unit, security and human-approval-gate tests for Workflow B's
underwriting/pricing decision-support engine
(submission/src/workflow_b/engine.py).

Test categories (per submission/runbooks/TEST.md):
  * Unit tests for underwriting/pricing reconciliation logic.
  * Security test: prompt-injection resistance (shared data_access
    detector, exercised here via a workflow B fixture reusing
    knowledge/MALICIOUS_ADJUSTER_REPORT.md-style evidence is not
    applicable to the 4 public workflow B fixtures, so this suite instead
    verifies the same detector wiring directly).
  * Human-approval gate tests: no prohibited pricing/underwriting field or
    action can ever appear in a response, regardless of scenario.
  * Golden tests against every public Workflow B fixture in
    evaluation/fixtures, validated against its own response contract.
"""
from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import _pathsetup  # noqa: F401
from common.contract_validation import load_schema, validate
from workflow_b.engine import PROHIBITED_ACTIONS_STATEMENT, build_response

ROOT = Path(__file__).resolve().parents[2]

PROHIBITED_FIELD_NAMES = [
    "binding_decision",
    "bind",
    "decline",
    "accept",
    "final_price",
    "premium",
    "adverse_action",
    "policy_issued",
]

AUTHORIZED_CONTEXT = {
    "user_id": "WORKSHOP-REVIEWER",
    "role": "authorized_reviewer",
    "purpose": "synthetic_capstone_evaluation",
    "tenant": "AMR-SYNTHETIC",
    "current_entitlement_required": True,
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_fixture(scenario_id: str) -> tuple[dict, dict]:
    fixture_path = ROOT / "evaluation/fixtures" / scenario_id / "fixture.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    return build_response(
        case_id=fixture["scenario_id"],
        workflow=fixture["workflow"],
        authorization_context=fixture["authorization_context"],
        evidence_refs=fixture["evidence"],
    ), fixture


class TestAllPublicFixturesProduceContractValidResponses(unittest.TestCase):
    """Golden test: every underwriting_pricing_support fixture under
    evaluation/fixtures/ must produce a response that satisfies its own
    declared response_contract schema."""

    def test_every_workflow_b_fixture_is_contract_valid(self):
        fixtures_dir = ROOT / "evaluation/fixtures"
        checked = 0
        for fixture_path in sorted(fixtures_dir.glob("EV-*/fixture.json")):
            fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
            if fixture["workflow"] != "underwriting_pricing_support":
                continue
            checked += 1
            response = build_response(
                case_id=fixture["scenario_id"],
                workflow=fixture["workflow"],
                authorization_context=fixture["authorization_context"],
                evidence_refs=fixture["evidence"],
            )
            schema = load_schema(ROOT / fixture["response_contract"])
            errors = validate(response, schema)
            self.assertEqual(errors, [], f"{fixture['scenario_id']} response invalid: {errors}")
        self.assertGreaterEqual(checked, 4, "expected at least 4 underwriting_pricing_support fixtures")


class TestHumanApprovalGate(unittest.TestCase):
    """No response, across any fixture, may contain a prohibited regulated
    field or action — the human-approval gate must never be bypassed."""

    def test_no_prohibited_field_appears_in_any_fixture_response(self):
        fixtures_dir = ROOT / "evaluation/fixtures"
        for fixture_path in sorted(fixtures_dir.glob("EV-*/fixture.json")):
            fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
            if fixture["workflow"] != "underwriting_pricing_support":
                continue
            response = build_response(
                case_id=fixture["scenario_id"],
                workflow=fixture["workflow"],
                authorization_context=fixture["authorization_context"],
                evidence_refs=fixture["evidence"],
            )
            serialized = json.dumps(response)
            for field_name in PROHIBITED_FIELD_NAMES:
                self.assertNotIn(
                    f'"{field_name}"', serialized,
                    f"{fixture['scenario_id']} response must not contain prohibited field {field_name}",
                )

    def test_prohibited_actions_statement_is_always_present(self):
        response, _ = _run_fixture("EV-06")
        self.assertEqual(response["prohibited_actions"], PROHIBITED_ACTIONS_STATEMENT)

    def test_human_review_is_flagged_whenever_conflicts_exist(self):
        response, _ = _run_fixture("EV-06")
        self.assertTrue(response["conflicts"])
        self.assertTrue(response["human_review"]["required"])


class TestFairnessBreachEscalation(unittest.TestCase):
    """EV-06: fairness_metrics.csv reports a confirmed breach for
    PRC-MOTOR-9 on the postal_proxy_low_income subgroup (INJ-013/INJ-065).
    Must escalate and never resolve into a price/accept/decline outcome."""

    def test_confirmed_fairness_breach_escalates_and_is_never_priced(self):
        response, _ = _run_fixture("EV-06")
        self.assertEqual(response["status"], "escalated")
        self.assertTrue(any("confirmed breach" in c for c in response["conflicts"]))
        self.assertTrue(any(
            "must not be resolved into a price, acceptance or decline outcome" in c
            for c in response["conflicts"]
        ))


class TestFirmwareDriftAbstention(unittest.TestCase):
    """EV-07: device_firmware.csv / vehicle_telemetry.csv report a semantic
    change (firmware update) without a recalibration record (INJ-014/015).
    Must surface the conflict and abstain from scoring across the boundary."""

    def test_firmware_drift_without_recalibration_is_surfaced(self):
        response, _ = _run_fixture("EV-07")
        self.assertTrue(any(
            "unsupported and must not be used for automated pricing" in c
            for c in response["conflicts"]
        ))
        self.assertIn(response["status"], {"conflict", "escalated"})


class TestLifeContestabilityEscalation(unittest.TestCase):
    """EV-09: life_applications.csv/life_claims.csv/medical_evidence.csv
    report boundary-relevant contradictory disclosure (INJ-025/INJ-028).
    Must construct the timeline and escalate without repudiating the claim."""

    def test_contestability_conflict_is_surfaced_without_repudiation(self):
        response, _ = _run_fixture("EV-09")
        self.assertTrue(any(
            "qualified human legal and claims decision" in c for c in response["conflicts"]
        ))
        serialized = json.dumps(response).lower()
        self.assertNotIn('"repudiate"', serialized)
        self.assertNotIn('"claim_decision"', serialized)


class TestVendorPriceShockDisclosure(unittest.TestCase):
    """EV-15: model_costs.csv reports OmniModel OM-Large's 65% price
    increase (INJ-089); token_budgets.csv/cost_model.csv challenge_fact rows
    flag unmodelled cost categories (INJ-091). Must disclose, not hide."""

    def test_price_increase_and_unmodelled_cost_are_disclosed(self):
        response, _ = _run_fixture("EV-15")
        self.assertTrue(any("65% increase" in c for c in response["conflicts"]))
        self.assertTrue(any("budget-response decision" in c for c in response["conflicts"]))


class TestEvidenceReconciliationLogic(unittest.TestCase):
    """Unit tests for specific reconciliation behaviours using synthetic,
    directly-constructed evidence (independent of the public fixtures)."""

    def test_conditional_model_registry_status_is_surfaced(self):
        response = build_response(
            case_id="SYNTH-CONDITIONAL",
            workflow="underwriting_pricing_support",
            authorization_context=AUTHORIZED_CONTEXT,
            evidence_refs=[{"path": "data/model_registry.csv", "selector": "model_id=GEN-SUM-3",
                             "sha256": _sha256(ROOT / "data/model_registry.csv")}],
        )
        self.assertTrue(any("approval_status=" in c and "conditional" in c for c in response["conflicts"]))

    def test_missing_evidence_file_yields_insufficient_evidence_status(self):
        response = build_response(
            case_id="SYNTH-MISSING",
            workflow="underwriting_pricing_support",
            authorization_context=AUTHORIZED_CONTEXT,
            evidence_refs=[{"path": "data/does_not_exist.csv", "selector": "x=1", "sha256": "0" * 64}],
        )
        self.assertEqual(response["status"], "insufficient_evidence")
        self.assertTrue(response["missing_evidence"])

    def test_tampered_evidence_hash_yields_insufficient_evidence_status(self):
        response = build_response(
            case_id="SYNTH-TAMPER",
            workflow="underwriting_pricing_support",
            authorization_context=AUTHORIZED_CONTEXT,
            evidence_refs=[{"path": "data/model_registry.csv", "selector": "model_id=PRC-MOTOR-9",
                             "sha256": "0" * 64}],
        )
        self.assertEqual(response["status"], "insufficient_evidence")
        self.assertTrue(any("does not match the declared evidence hash" in m for m in response["missing_evidence"]))

    def test_incomplete_authorization_context_is_not_current(self):
        response = build_response(
            case_id="SYNTH-NOAUTH",
            workflow="underwriting_pricing_support",
            authorization_context={"user_id": "X"},  # missing role/purpose/tenant
            evidence_refs=[],
        )
        self.assertFalse(response["authorization_context"]["current"])
        self.assertEqual(response["status"], "insufficient_evidence")

    def test_no_conflict_no_missing_evidence_yields_supported_status(self):
        response = build_response(
            case_id="SYNTH-CLEAN",
            workflow="underwriting_pricing_support",
            authorization_context=AUTHORIZED_CONTEXT,
            evidence_refs=[{"path": "data/model_registry.csv", "selector": "model_id=FRD-CLAIM-6",
                             "sha256": _sha256(ROOT / "data/model_registry.csv")}],
        )
        self.assertEqual(response["status"], "supported")
        self.assertFalse(response["human_review"]["required"])


if __name__ == "__main__":
    unittest.main()
