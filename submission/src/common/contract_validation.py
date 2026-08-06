"""Shared, dependency-free response-contract validation for all AEGIS-INSURE workflows.

Mirrors the logic in evaluation/validate_contracts.py so that participant code
(engines and tests) can check a candidate response against its JSON Schema
contract without any external jsonschema dependency, and so that the same
validator used by the offline evaluation harness is exercised by the unit
tests in submission/tests/.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def _walk_keys(obj: Any):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from _walk_keys(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from _walk_keys(item)


def load_schema(schema_path: Path) -> dict:
    return json.loads(schema_path.read_text(encoding="utf-8"))


def validate(payload: dict, schema: dict) -> list[str]:
    """Return a list of human-readable errors; empty list means the payload
    satisfies the contract's structural, workflow, status, prohibited-field
    and evidence-shape requirements."""
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["payload must be an object"]

    for key in schema.get("required", []):
        if key not in payload:
            errors.append(f"missing required field: {key}")

    if schema.get("additionalProperties") is False:
        allowed = set(schema.get("properties", {}))
        for key in payload:
            if key not in allowed:
                errors.append(f"unexpected field: {key}")

    expected_workflow = schema.get("x-workflow")
    if expected_workflow and payload.get("workflow") != expected_workflow:
        errors.append("workflow mismatch")

    status = payload.get("status")
    allowed_status = schema.get("properties", {}).get("status", {}).get("enum", [])
    if status is not None and allowed_status and status not in allowed_status:
        errors.append("invalid status")

    found_keys = set(_walk_keys(payload))
    for prohibited in schema.get("x-prohibited-fields", []):
        if prohibited in found_keys:
            errors.append(f"prohibited field: {prohibited}")

    for list_field in [
        "facts",
        "inferences",
        "conflicts",
        "missing_evidence",
        "recommendations",
        "prohibited_actions",
        "evidence",
    ]:
        if list_field in payload and not isinstance(payload[list_field], list):
            errors.append(f"{list_field} must be an array")

    auth = payload.get("authorization_context", {})
    if auth and not auth.get("current", False):
        errors.append("authorization must be current")

    for i, item in enumerate(payload.get("evidence", [])):
        for key in ["evidence_id", "source_path", "record_locator", "sha256", "authority_status", "fact"]:
            if key not in item:
                errors.append(f"evidence[{i}] missing {key}")
        if "sha256" in item and not re.fullmatch(r"[0-9a-f]{64}", str(item["sha256"])):
            errors.append(f"evidence[{i}] invalid sha256")

    return errors
