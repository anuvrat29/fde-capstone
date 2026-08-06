"""Evidence loading and integrity verification for Workflow A.

Every function here is read-only: it never mutates a source file under
`data/` or `knowledge/`, never calls a network or paid API, and never
produces a side effect. It only resolves the evidence a fixture points at,
hashes the underlying file, and returns structured rows/documents so the
reconciliation engine can reason about them.
"""
from __future__ import annotations

import csv
import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass
class EvidenceItem:
    """One resolved evidence pointer from a fixture's `evidence` array."""

    evidence_id: str
    source_path: str
    selector: str
    declared_sha256: str
    actual_sha256: str
    integrity_ok: bool
    kind: str  # "csv_rows" | "document" | "missing"
    rows: list[dict[str, str]] = field(default_factory=list)
    document_text: str = ""


def resolve_evidence(evidence_refs: list[dict[str, str]]) -> list[EvidenceItem]:
    """Resolve fixture-declared evidence pointers against the repository.

    Mirrors the integrity check performed by evaluation/validate_fixtures.py
    so a candidate case is only reasoned about if the underlying source file
    still matches the hash the fixture declared (tamper/staleness defence).
    """
    resolved: list[EvidenceItem] = []
    for i, ref in enumerate(evidence_refs, start=1):
        evidence_id = f"E-{i}"
        rel_path = ref["path"]
        selector = ref.get("selector", "document")
        declared_hash = ref.get("sha256", "")
        abs_path = ROOT / rel_path

        if not abs_path.exists():
            resolved.append(
                EvidenceItem(
                    evidence_id=evidence_id,
                    source_path=rel_path,
                    selector=selector,
                    declared_sha256=declared_hash,
                    actual_sha256="",
                    integrity_ok=False,
                    kind="missing",
                )
            )
            continue

        actual_hash = sha256_of(abs_path)
        integrity_ok = actual_hash == declared_hash

        if selector == "document":
            resolved.append(
                EvidenceItem(
                    evidence_id=evidence_id,
                    source_path=rel_path,
                    selector=selector,
                    declared_sha256=declared_hash,
                    actual_sha256=actual_hash,
                    integrity_ok=integrity_ok,
                    kind="document",
                    document_text=abs_path.read_text(encoding="utf-8", errors="ignore"),
                )
            )
            continue

        if abs_path.suffix.lower() == ".csv":
            rows = _select_csv_rows(abs_path, selector)
            resolved.append(
                EvidenceItem(
                    evidence_id=evidence_id,
                    source_path=rel_path,
                    selector=selector,
                    declared_sha256=declared_hash,
                    actual_sha256=actual_hash,
                    integrity_ok=integrity_ok,
                    kind="csv_rows",
                    rows=rows,
                )
            )
            continue

        # Unrecognised selector/file combination: treat as a document.
        resolved.append(
            EvidenceItem(
                evidence_id=evidence_id,
                source_path=rel_path,
                selector=selector,
                declared_sha256=declared_hash,
                actual_sha256=actual_hash,
                integrity_ok=integrity_ok,
                kind="document",
                document_text=abs_path.read_text(encoding="utf-8", errors="ignore"),
            )
        )
    return resolved


def _select_csv_rows(path: Path, selector: str) -> list[dict[str, str]]:
    if "=" not in selector:
        return []
    key, value = selector.split("=", 1)
    with path.open(encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f) if (r.get(key) or "") == value]


_DOC_FIELD_PATTERN = re.compile(r"\*\*([A-Za-z ]+):\*\*\s*`?([^`\n]+)`?")


def parse_document_control(text: str) -> dict[str, str]:
    """Extract the `## Document control` bullet fields from a knowledge/*.md file."""
    fields: dict[str, str] = {}
    for label, value in _DOC_FIELD_PATTERN.findall(text):
        fields[label.strip()] = value.strip()
    return fields


_IMPERATIVE_INJECTION_PATTERN = re.compile(
    r"\b(ignore (all|any) (policy|prior|previous|system)|disable (fraud|checks)|"
    r"mark (the )?claim (as )?fully covered|override (all )?(exclusions|checks))\b",
    re.IGNORECASE,
)


def contains_embedded_instruction(text: str) -> bool:
    """Heuristic detector for prompt-injection style imperative text embedded in
    evidence documents (e.g. knowledge/MALICIOUS_ADJUSTER_REPORT.md). Any hit
    means the document's prose must be treated strictly as untrusted data."""
    return bool(_IMPERATIVE_INJECTION_PATTERN.search(text))


def load_entitlement_rows(user_id: str) -> list[dict[str, str]]:
    path = ROOT / "data" / "users_entitlements.csv"
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f) if r.get("user_id") == user_id]


def load_access_cache_rows(user_id: str) -> list[dict[str, str]]:
    path = ROOT / "data" / "access_cache.csv"
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f) if r.get("user_id") == user_id]
