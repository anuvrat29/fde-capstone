"""Unit tests for submission/src/common/contract_validation.py.

Covers: positive/negative contract_tests fixtures supplied under
evaluation/contract_tests, plus targeted checks on required fields,
prohibited fields, status enum and evidence-item shape.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

import _pathsetup  # noqa: F401
from common.contract_validation import load_schema, validate

ROOT = Path(__file__).resolve().parents[2]


class TestSuppliedContractFixtures(unittest.TestCase):
    """Re-run the same positive/negative fixtures used by
    evaluation/validate_contracts.py, proving our validator agrees with the
    reference offline harness."""

    def test_all_positive_fixtures_pass(self):
        for path in sorted((ROOT / "evaluation/contract_tests/positive").glob("*.json")):
            schema = load_schema(ROOT / "evaluation/contracts" / (path.stem + "_response.schema.json"))
            payload = json.loads(path.read_text(encoding="utf-8"))
            errors = validate(payload, schema)
            self.assertEqual(errors, [], f"{path.name} should be valid: {errors}")

    def test_all_negative_fixtures_fail(self):
        for path in sorted((ROOT / "evaluation/contract_tests/negative").glob("*.json")):
            schema = load_schema(ROOT / "evaluation/contracts" / (path.stem + "_response.schema.json"))
            payload = json.loads(path.read_text(encoding="utf-8"))
            errors = validate(payload, schema)
            self.assertTrue(errors, f"{path.name} should be rejected but passed validation")


class TestValidatorBehaviour(unittest.TestCase):
    def setUp(self):
        self.schema = load_schema(
            ROOT / "evaluation/contracts/coverage_claim_reconciliation_response.schema.json"
        )
        self.valid_payload = json.loads(
            (ROOT / "evaluation/contract_tests/positive/coverage_claim_reconciliation.json").read_text()
        )

    def test_valid_payload_has_no_errors(self):
        self.assertEqual(validate(self.valid_payload, self.schema), [])

    def test_missing_required_field_is_flagged(self):
        payload = dict(self.valid_payload)
        del payload["lineage"]
        errors = validate(payload, self.schema)
        self.assertIn("missing required field: lineage", errors)

    def test_prohibited_field_anywhere_in_payload_is_flagged(self):
        payload = json.loads(json.dumps(self.valid_payload))
        payload["coverage_decision"] = "APPROVED"
        errors = validate(payload, self.schema)
        self.assertTrue(any("prohibited field: coverage_decision" in e for e in errors))

    def test_prohibited_field_nested_inside_a_list_is_flagged(self):
        payload = json.loads(json.dumps(self.valid_payload))
        payload["facts"].append({"settlement_amount": 1000})
        errors = validate(payload, self.schema)
        self.assertTrue(any("prohibited field: settlement_amount" in e for e in errors))

    def test_invalid_status_is_flagged(self):
        payload = dict(self.valid_payload)
        payload["status"] = "bound"
        errors = validate(payload, self.schema)
        self.assertIn("invalid status", errors)

    def test_non_current_authorization_is_flagged(self):
        payload = json.loads(json.dumps(self.valid_payload))
        payload["authorization_context"]["current"] = False
        errors = validate(payload, self.schema)
        self.assertIn("authorization must be current", errors)

    def test_evidence_item_missing_field_is_flagged(self):
        payload = json.loads(json.dumps(self.valid_payload))
        del payload["evidence"][0]["sha256"]
        errors = validate(payload, self.schema)
        self.assertTrue(any("missing sha256" in e for e in errors))

    def test_evidence_item_bad_sha256_is_flagged(self):
        payload = json.loads(json.dumps(self.valid_payload))
        payload["evidence"][0]["sha256"] = "not-a-hash"
        errors = validate(payload, self.schema)
        self.assertTrue(any("invalid sha256" in e for e in errors))

    def test_additional_property_is_flagged(self):
        payload = json.loads(json.dumps(self.valid_payload))
        payload["extra_unexpected_field"] = "x"
        errors = validate(payload, self.schema)
        self.assertTrue(any("unexpected field: extra_unexpected_field" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
