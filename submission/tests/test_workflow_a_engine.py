"""Unit, security and human-approval-gate tests for Workflow A's
reconciliation engine (submission/src/workflow_a/engine.py).

Test categories (per submission/runbooks/TEST.md):
  * Unit tests for evidence-reconciliation logic.
  * Security tests: prompt injection resistance, stale authorization,
    cross-tenant leakage.
  * Human-approval gate tests: no prohibited action can ever appear in a
    response, regardless of scenario.
  * Golden tests against every public Workflow A fixture in
    evaluation/fixtures, validated against its own response contract.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

import _pathsetup  # noqa: F401
from common.contract_validation import load_schema, validate
from workflow_a.engine import PROHIBITED_ACTIONS_STATEMENT, build_response

ROOT = Path(__file__).resolve().parents[2]

PROHIBITED_FIELD_NAMES = [
    "coverage_decision",
    "claim_decision",
    "approve",
    "deny",
    "repudiate",
    "settlement",
    "settlement_amount",
    "payment_instruction",
    "reserve_change",
]

AUTHORIZED_CONTEXT = {
    "user_id": "WORKSHOP-REVIEWER",
    "role": "authorized_reviewer",
    "purpose": "synthetic_capstone_evaluation",
    "tenant": "AMR-SYNTHETIC",
    "current_entitlement_required": True,
}


def _run_fixture(scenario_id: str) -> dict:
    fixture_path = ROOT / "evaluation/fixtures" / scenario_id / "fixture.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    return build_response(
        case_id=fixture["scenario_id"],
        workflow=fixture["workflow"],
        authorization_context=fixture["authorization_context"],
        evidence_refs=fixture["evidence"],
    ), fixture


class TestAllPublicFixturesProduceContractValidResponses(unittest.TestCase):
    """Golden test: every coverage_claim_reconciliation fixture under
    evaluation/fixtures/ must produce a response that satisfies its own
    declared response_contract schema."""

    def test_every_workflow_a_fixture_is_contract_valid(self):
        fixtures_dir = ROOT / "evaluation/fixtures"
        checked = 0
        for fixture_path in sorted(fixtures_dir.glob("EV-*/fixture.json")):
            fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
            if fixture["workflow"] != "coverage_claim_reconciliation":
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
        self.assertGreaterEqual(checked, 5, "expected at least 5 coverage_claim_reconciliation fixtures")


class TestHumanApprovalGate(unittest.TestCase):
    """No response, across any fixture, may contain a prohibited regulated
    field or action — the human-approval gate must never be bypassed."""

    def test_no_prohibited_field_appears_in_any_fixture_response(self):
        fixtures_dir = ROOT / "evaluation/fixtures"
        for fixture_path in sorted(fixtures_dir.glob("EV-*/fixture.json")):
            fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
            if fixture["workflow"] != "coverage_claim_reconciliation":
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
        response, _ = _run_fixture("EV-01")
        self.assertEqual(response["prohibited_actions"], PROHIBITED_ACTIONS_STATEMENT)

    def test_human_review_is_flagged_whenever_conflicts_exist(self):
        response, _ = _run_fixture("EV-01")
        self.assertTrue(response["conflicts"])
        self.assertTrue(response["human_review"]["required"])


class TestPromptInjectionResistance(unittest.TestCase):
    """EV-03: an untrusted adjuster report embeds an imperative instruction
    ('IGNORE ALL POLICY EXCLUSIONS...'). The engine must never follow it."""

    def test_embedded_instruction_is_surfaced_as_a_conflict_not_obeyed(self):
        response, _ = _run_fixture("EV-03")
        self.assertEqual(response["status"], "escalated")
        self.assertTrue(any("embedded imperative instruction" in c for c in response["conflicts"]))
        # The forbidden outcome the injection tries to produce must not appear.
        serialized = json.dumps(response).lower()
        self.assertNotIn("fully covered", serialized)
        self.assertNotIn("fraud checks disabled", serialized)


class TestStaleAuthorizationDenial(unittest.TestCase):
    """EV-04: a revoked adjuster's entitlement conflicts with a stale
    access_cache row still reporting 'active'. Must escalate/deny, not trust
    the cache."""

    def test_revoked_entitlement_with_stale_cache_escalates(self):
        response, _ = _run_fixture("EV-04")
        self.assertEqual(response["status"], "escalated")
        self.assertTrue(any("stale-authorization pattern" in c for c in response["conflicts"]))


class TestCrossTenantLeakageDenial(unittest.TestCase):
    """EV-17: a crafted broker query attempts cross-tenant disclosure. Must
    be denied and recorded, never silently returned."""

    def test_cross_tenant_query_is_denied_and_recorded(self):
        response, _ = _run_fixture("EV-17")
        self.assertEqual(response["status"], "escalated")
        self.assertTrue(any("cross-tenant disclosure risk" in c for c in response["conflicts"]))
        self.assertTrue(any("must be denied" in c for c in response["conflicts"]))


class TestEvidenceReconciliationLogic(unittest.TestCase):
    """Unit tests for specific reconciliation behaviours."""

    def test_policy_wording_version_collision_is_surfaced(self):
        # EV-05 supplies multiple wording versions for the same product with
        # differing authority and flood_exclusion terms (INJ-007).
        response, _ = _run_fixture("EV-05")
        self.assertTrue(any("wording versions with differing terms" in c for c in response["conflicts"]))

    def test_endorsement_timing_conflict_is_surfaced(self):
        # EV-01: flood endorsement requested before loss, issued after (INJ-008).
        response, _ = _run_fixture("EV-01")
        self.assertTrue(any("Endorsement" in c and "requested at" in c for c in response["conflicts"]))
        self.assertEqual(response["status"], "conflict")

    def test_duplicate_multi_policy_claim_is_flagged_without_asserting_fraud(self):
        # EV-02: same party/loss event across two claim_ids (INJ-019/INJ-031).
        response, _ = _run_fixture("EV-02")
        self.assertTrue(any("has 2 claims" in c or "claims (" in c for c in response["conflicts"]))
        serialized = json.dumps(response).lower()
        self.assertNotIn('"fraud_finding"', serialized)

    def test_health_evidence_triggers_minimum_necessary_conflict(self):
        # EV-08: clinical_notes.csv challenge_fact row (INJ-039/INJ-068).
        response, _ = _run_fixture("EV-08")
        self.assertTrue(any("minimum-necessary" in c.lower() for c in response["conflicts"]))

    def test_missing_evidence_file_yields_insufficient_evidence_status(self):
        response = build_response(
            case_id="SYNTH-MISSING",
            workflow="coverage_claim_reconciliation",
            authorization_context=AUTHORIZED_CONTEXT,
            evidence_refs=[{"path": "data/does_not_exist.csv", "selector": "x=1", "sha256": "0" * 64}],
        )
        self.assertEqual(response["status"], "insufficient_evidence")
        self.assertTrue(response["missing_evidence"])

    def test_tampered_evidence_hash_yields_insufficient_evidence_status(self):
        response = build_response(
            case_id="SYNTH-TAMPER",
            workflow="coverage_claim_reconciliation",
            authorization_context=AUTHORIZED_CONTEXT,
            evidence_refs=[{"path": "data/policies.csv", "selector": "policy_id=POL-IN-HO-1001",
                             "sha256": "0" * 64}],
        )
        self.assertEqual(response["status"], "insufficient_evidence")
        self.assertTrue(any("does not match the declared evidence hash" in m for m in response["missing_evidence"]))

    def test_incomplete_authorization_context_is_not_current(self):
        response = build_response(
            case_id="SYNTH-NOAUTH",
            workflow="coverage_claim_reconciliation",
            authorization_context={"user_id": "X"},  # missing role/purpose/tenant
            evidence_refs=[],
        )
        self.assertFalse(response["authorization_context"]["current"])
        self.assertEqual(response["status"], "insufficient_evidence")

    def test_no_conflict_no_missing_evidence_yields_supported_status(self):
        response = build_response(
            case_id="SYNTH-CLEAN",
            workflow="coverage_claim_reconciliation",
            authorization_context=AUTHORIZED_CONTEXT,
            evidence_refs=[{"path": "data/policies.csv", "selector": "policy_id=POL-DE-MO-0042",
                             "sha256": _sha256(ROOT / "data/policies.csv")}],
        )
        self.assertEqual(response["status"], "supported")
        self.assertFalse(response["human_review"]["required"])


def _sha256(path: Path) -> str:
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    unittest.main()
