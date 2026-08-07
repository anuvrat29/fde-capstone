"""Unit and human-approval-gate tests for Workflow C's catastrophe/
reinsurance planning-support engine (submission/src/workflow_c/engine.py).

Test categories (per submission/runbooks/TEST.md):
  * Unit tests for catastrophe/reinsurance reconciliation logic.
  * Human-approval gate tests: no prohibited reserve/recovery/notice/
    treaty/payment field or action can ever appear in a response,
    regardless of scenario.
  * Golden tests against every public Workflow C fixture in
    evaluation/fixtures, validated against its own response contract.
"""
from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import _pathsetup  # noqa: F401
from common.contract_validation import load_schema, validate
from workflow_c.engine import PROHIBITED_ACTIONS_STATEMENT, build_response

ROOT = Path(__file__).resolve().parents[2]

PROHIBITED_FIELD_NAMES = [
    "reserve_change",
    "recovery_amount",
    "recovery_conclusion",
    "notice_submitted",
    "treaty_placement",
    "payment_instruction",
    "payment_created",
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
    """Golden test: every catastrophe_reinsurance_planning fixture under
    evaluation/fixtures/ must produce a response that satisfies its own
    declared response_contract schema."""

    def test_every_workflow_c_fixture_is_contract_valid(self):
        fixtures_dir = ROOT / "evaluation/fixtures"
        checked = 0
        for fixture_path in sorted(fixtures_dir.glob("EV-*/fixture.json")):
            fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
            if fixture["workflow"] != "catastrophe_reinsurance_planning":
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
        self.assertGreaterEqual(checked, 5, "expected at least 5 catastrophe_reinsurance_planning fixtures")


class TestHumanApprovalGate(unittest.TestCase):
    """No response, across any fixture, may contain a prohibited regulated
    field or action — the human-approval gate must never be bypassed."""

    def test_no_prohibited_field_appears_in_any_fixture_response(self):
        fixtures_dir = ROOT / "evaluation/fixtures"
        for fixture_path in sorted(fixtures_dir.glob("EV-*/fixture.json")):
            fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
            if fixture["workflow"] != "catastrophe_reinsurance_planning":
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
        response, _ = _run_fixture("EV-11")
        self.assertEqual(response["prohibited_actions"], PROHIBITED_ACTIONS_STATEMENT)

    def test_human_review_is_flagged_whenever_conflicts_exist(self):
        response, _ = _run_fixture("EV-11")
        self.assertTrue(response["conflicts"])
        self.assertTrue(response["human_review"]["required"])


class TestParametricTriggerConflict(unittest.TestCase):
    """EV-10: station/satellite/contract authority reconciliation for a
    parametric trigger (INJ-012/INJ-034). Must present both readings and
    never determine the trigger outcome itself."""

    def test_parametric_conflict_is_surfaced_without_trigger_determination(self):
        response, _ = _run_fixture("EV-10")
        self.assertTrue(any(
            "does not itself determine whether the trigger was met" in c
            for c in response["conflicts"]
        ))
        serialized = json.dumps(response).lower()
        self.assertNotIn('"trigger_met"', serialized)


class TestEventAggregationConflict(unittest.TestCase):
    """EV-11: two catastrophe events with differing hours-clause ownership
    referenced by one treaty (INJ-039/INJ-040). Must produce alternative
    aggregation views, never submit a single recovery."""

    def test_event_aggregation_ambiguity_is_surfaced(self):
        response, _ = _run_fixture("EV-11")
        self.assertTrue(any(
            "alternative aggregation views (single-event vs split-event)" in c
            for c in response["conflicts"]
        ))
        serialized = json.dumps(response).lower()
        self.assertNotIn('"recovery_amount"', serialized)
        self.assertNotIn('"recovery_conclusion"', serialized)


class TestCurrencyValuationConflict(unittest.TestCase):
    """EV-12: mixed-currency bordereaux with inconsistent valuation dates
    (INJ-042/INJ-053). Must never be summed into a single total."""

    def test_mixed_currency_bordereaux_is_disclosed_not_summed(self):
        response, _ = _run_fixture("EV-12")
        self.assertTrue(any(
            "cannot be summed without valuation rules" in c for c in response["conflicts"]
        ))


class TestCheckpointReplayDenial(unittest.TestCase):
    """EV-13: a recovery agent resumes stale state and risks a duplicate
    draft payment/notice (INJ-094). Must escalate and deny."""

    def test_checkpoint_replay_is_denied_and_recorded(self):
        response, _ = _run_fixture("EV-13")
        self.assertEqual(response["status"], "escalated")
        self.assertTrue(any("checkpoint-replay pattern" in c for c in response["conflicts"]))
        serialized = json.dumps(response).lower()
        self.assertNotIn('"payment_instruction"', serialized)
        self.assertNotIn('"notice_submitted"', serialized)


class TestDegradedModeContinuity(unittest.TestCase):
    """EV-16: an open-ended ransomware-containment downtime event for a
    capability with a continuity ceiling (INJ-091/INJ-093/INJ-096). Must
    recommend authorized snapshots/manual fallback only, never invent data."""

    def test_open_ended_downtime_triggers_degraded_mode_conflict(self):
        response, _ = _run_fixture("EV-16")
        self.assertEqual(response["status"], "escalated")
        self.assertTrue(any("still-ongoing" in c for c in response["conflicts"]))
        self.assertTrue(any("authorized snapshots" in c for c in response["conflicts"]))


class TestEvidenceReconciliationLogic(unittest.TestCase):
    """Unit tests for specific reconciliation behaviours using synthetic,
    directly-constructed evidence (independent of the public fixtures)."""

    def test_missing_evidence_file_yields_insufficient_evidence_status(self):
        response = build_response(
            case_id="SYNTH-MISSING",
            workflow="catastrophe_reinsurance_planning",
            authorization_context=AUTHORIZED_CONTEXT,
            evidence_refs=[{"path": "data/does_not_exist.csv", "selector": "x=1", "sha256": "0" * 64}],
        )
        self.assertEqual(response["status"], "insufficient_evidence")
        self.assertTrue(response["missing_evidence"])

    def test_tampered_evidence_hash_yields_insufficient_evidence_status(self):
        response = build_response(
            case_id="SYNTH-TAMPER",
            workflow="catastrophe_reinsurance_planning",
            authorization_context=AUTHORIZED_CONTEXT,
            evidence_refs=[{"path": "data/cat_events.csv", "selector": "event_id=CAT-NILA-A",
                             "sha256": "0" * 64}],
        )
        self.assertEqual(response["status"], "insufficient_evidence")
        self.assertTrue(any("does not match the declared evidence hash" in m for m in response["missing_evidence"]))

    def test_incomplete_authorization_context_is_not_current(self):
        response = build_response(
            case_id="SYNTH-NOAUTH",
            workflow="catastrophe_reinsurance_planning",
            authorization_context={"user_id": "X"},  # missing role/purpose/tenant
            evidence_refs=[],
        )
        self.assertFalse(response["authorization_context"]["current"])
        self.assertEqual(response["status"], "insufficient_evidence")

    def test_no_conflict_no_missing_evidence_yields_supported_status(self):
        response = build_response(
            case_id="SYNTH-CLEAN",
            workflow="catastrophe_reinsurance_planning",
            authorization_context=AUTHORIZED_CONTEXT,
            evidence_refs=[{"path": "data/reinsurance_treaties.csv", "selector": "treaty_id=TR-2026-CY-02",
                             "sha256": _sha256(ROOT / "data/reinsurance_treaties.csv")}],
        )
        self.assertEqual(response["status"], "supported")
        self.assertFalse(response["human_review"]["required"])


if __name__ == "__main__":
    unittest.main()
