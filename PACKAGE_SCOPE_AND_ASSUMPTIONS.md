# Package Scope and Assumptions

## What this package is

A synthetic challenge environment for demonstrating business discovery, product sense, insurance domain modelling, data authority, AI architecture, secure engineering, evaluation, governance, reliability and executive defence.

## What this package is not

- A legal interpretation service.
- An actuarial model or reserving tool.
- A policy administration, claims, pricing, payment or reinsurance production system.
- A source of real customer or insurer data.
- A reference implementation or hidden answer key.

## Synthetic-data design

The package combines detailed core tables with compact evidence-envelope tables. Compact tables intentionally represent heterogeneous brownfield exports using the common fields `record_id`, `entity_id`, `event_time`, `status`, `value`, `source_system`, `jurisdiction` and `notes`. They are evidence fragments, not complete enterprise data models.

`metadata/DATASET_CATALOG.csv`, `metadata/COLUMN_DICTIONARY.csv`, `metadata/RELATIONSHIP_RULES.csv` and `metadata/DECLARED_DATA_EXCEPTIONS.md` define how the supplied evidence may be interpreted and validated.

## Declared assumptions

- The workshop date baseline is 1 August 2026.
- All timestamps retain their supplied offset or UTC marker; local dates must not be compared without normalization.
- Currency values must not be aggregated without a stated valuation date and FX authority.
- Authority is contextual and temporal; no single system is globally authoritative.
- Missing relationships may be deliberate evidence gaps and must be surfaced rather than silently repaired.
- Public fixtures provide inputs and contracts, not expected decisions.
- Python 3.10 or later is recommended. Only the Python standard library is required.

## Mutable and immutable boundaries

Everything outside `submission/` is challenge evidence or workshop tooling and is covered by `FILE_HASHES.csv`. Participant-generated code, logs, reports, checkpoints and artefacts belong under `submission/` and are intentionally excluded from immutable package hashes.
