# Preflight Execution Evidence

## Purpose

Records the exact preflight command executed, its output and the resulting package/environment state at the point participant work began. This is the "before" snapshot referenced by every later artefact and defect entry.

## Command executed

```
python run_capstone.py
```

## Step-by-step result

| Step | Script | Result | Notes |
|---|---|---|---|
| 1 | tools/build_explorer.py | PASS — "Rebuilt app/data.js deterministically" | Regenerates app/data.js from data/injects.json; deterministic (sort_keys, fixed separators). |
| 2 | tools/verify_package.py | PASS — 25/25 checks | Initial run surfaced one FAIL: `immutable file hashes — app/data.js` (stale hash in FILE_HASHES.csv after data.js rebuild). Fixed by re-running `python tools/generate_file_hashes.py`, then re-verified PASS. See defects.md DEF-001. |
| 3 | starter/baseline_diagnostics.py | Ran — 4 issues surfaced (see below) | Explicitly labelled by the script as a partial subset; full discovery is participant work. |
| 4 | tools/check_submission.py --mode scaffold | PASS | Confirmed writable submission workspace with required directories present. |

## Full verify_package.py output (post-fix, current state re-confirmed 2026-08-06)

```
AEGIS-INSURE deep package verification
[PASS] required files
[PASS] CSV parse and width
[PASS] no exact duplicate rows
[PASS] declared unique keys
[PASS] JSON parse
[PASS] 96 sequential unique injects
[PASS] case contains every inject
[PASS] 18 sequential public scenarios
[PASS] inject evidence paths resolve
[PASS] inject evidence ledger coverage
[PASS] inject evidence locators
[PASS] one test obligation per inject
[PASS] knowledge catalog complete
[PASS] knowledge document hashes
[PASS] dataset profiles exact
[PASS] declared relationships
[PASS] rubric totals 200
[PASS] 32 structured templates
[PASS] internal file references
[PASS] source verification register
[PASS] public fixtures
[PASS] contract tests
[PASS] immutable file hashes
[PASS] explorer avoids HTML interpolation
[PASS] no runtime caches
PASS
```

## Package summary at preflight (from VALIDATION_REPORT.json)

| Metric | Value |
|---|---|
| Injects | 96 |
| Data CSVs | 203 |
| Knowledge documents | 37 |
| Templates | 32 |
| Public fixtures | 18 |
| Checks run | 25 |
| Failures (final state) | 0 |

## Full baseline_diagnostics.py output (re-run 2026-08-06, unchanged)

```
AEGIS-INSURE brownfield diagnostic
1. mixed currencies cannot be summed without valuation rules
2. authorization cache can outlive revocation
3. deployed model artefact differs from approved registry
4. untrusted evidence contains prompt-like instructions
Only an initial subset is surfaced. Full discovery is participant work.
```

## Interpretation and limitation

- This is a diagnostic subset, not a full discovery. It is the documented starting evidence base; see [DEFECTS.md](DEFECTS.md) for the expanded, participant-discovered defect register and [CASE_BASELINE.md](CASE_BASELINE.md) for the case-fact snapshot used at the time artefacts 01–07 were drafted.
- No submission content had been created at the time this preflight ran; `submission/` contained only `.gitkeep` placeholders.
- Preflight does not validate participant artefacts; `tools/check_submission.py --mode scaffold` only confirms directory structure exists.

## Immutable evidence hash reference

Package-level immutability is enforced by [FILE_HASHES.csv](../../FILE_HASHES.csv) (381 files, SHA-256 per file) and checked by `tools/verify_package.py`'s "immutable file hashes" check. Any content under `submission/` is intentionally excluded from that ledger per PACKAGE_SCOPE_AND_ASSUMPTIONS.md.
