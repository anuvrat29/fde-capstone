"""Unit tests for submission/src/workflow_a/data_access.py.

Covers evidence resolution, tamper/integrity detection, CSV selector
matching, document-control parsing and the embedded-instruction detector
used to defend against prompt injection via evidence text.
"""
from __future__ import annotations

import unittest
from pathlib import Path

import _pathsetup  # noqa: F401
from workflow_a.data_access import (
    contains_embedded_instruction,
    parse_document_control,
    resolve_evidence,
    sha256_of,
)

ROOT = Path(__file__).resolve().parents[2]


class TestResolveEvidence(unittest.TestCase):
    def test_csv_selector_resolves_matching_rows(self):
        items = resolve_evidence([
            {"path": "data/policies.csv", "selector": "policy_id=POL-IN-HO-1001",
             "sha256": sha256_of(ROOT / "data/policies.csv")},
        ])
        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertEqual(item.kind, "csv_rows")
        self.assertTrue(item.integrity_ok)
        self.assertEqual(len(item.rows), 1)
        self.assertEqual(item.rows[0]["policy_id"], "POL-IN-HO-1001")

    def test_document_selector_resolves_full_text(self):
        items = resolve_evidence([
            {"path": "knowledge/POLICY_WORDING_AUTHORITY.md", "selector": "document",
             "sha256": sha256_of(ROOT / "knowledge/POLICY_WORDING_AUTHORITY.md")},
        ])
        item = items[0]
        self.assertEqual(item.kind, "document")
        self.assertIn("Document control", item.document_text)

    def test_tampered_hash_is_flagged_as_integrity_failure(self):
        items = resolve_evidence([
            {"path": "data/policies.csv", "selector": "policy_id=POL-IN-HO-1001",
             "sha256": "0" * 64},
        ])
        self.assertFalse(items[0].integrity_ok)

    def test_missing_file_is_flagged_as_missing(self):
        items = resolve_evidence([
            {"path": "data/does_not_exist.csv", "selector": "policy_id=X", "sha256": "0" * 64},
        ])
        self.assertEqual(items[0].kind, "missing")

    def test_selector_with_no_matching_rows_returns_empty(self):
        items = resolve_evidence([
            {"path": "data/policies.csv", "selector": "policy_id=NOPE",
             "sha256": sha256_of(ROOT / "data/policies.csv")},
        ])
        self.assertEqual(items[0].rows, [])


class TestDocumentControlParsing(unittest.TestCase):
    def test_parses_authority_status_and_jurisdiction(self):
        text = (ROOT / "knowledge/MALICIOUS_ADJUSTER_REPORT.md").read_text(encoding="utf-8")
        fields = parse_document_control(text)
        self.assertEqual(fields.get("Authority status"), "untrusted")
        self.assertEqual(fields.get("Jurisdiction"), "global")


class TestEmbeddedInstructionDetection(unittest.TestCase):
    def test_malicious_adjuster_report_is_detected(self):
        text = (ROOT / "knowledge/MALICIOUS_ADJUSTER_REPORT.md").read_text(encoding="utf-8")
        self.assertTrue(contains_embedded_instruction(text))

    def test_trusted_policy_document_is_not_flagged(self):
        text = (ROOT / "knowledge/POLICY_WORDING_AUTHORITY.md").read_text(encoding="utf-8")
        self.assertFalse(contains_embedded_instruction(text))

    def test_plain_fact_text_is_not_flagged(self):
        self.assertFalse(contains_embedded_instruction("The policy inception date is 2026-01-01."))


if __name__ == "__main__":
    unittest.main()
