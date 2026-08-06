"""Progress report for the AEGIS-INSURE participant submission.

Summarises how much of the required submission work is complete:
- the 32 structured artefact templates (completed vs placeholder vs missing)
- inject traceability coverage across all 96 injects
- evidence manifest row count
- implementation/test/app/script/evaluation substantive file counts
- Phase 1 evidence files (charter, decision rights)

Read-only: never modifies challenge evidence or submission content.
Standard library only.

Usage:
    python tools/progress_report.py
    python tools/progress_report.py --write
"""
from pathlib import Path
import argparse, csv, re, sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
SUB = ROOT / 'submission'

TEMPLATES = [
    '01_BUSINESS_CASE.md', '02_DMAIC_WORKBOOK.md', '03_STAKEHOLDER_DECISION_RIGHTS.md',
    '04_PRODUCT_SERVICE_BLUEPRINT.md', '05_DDD_CONTEXT_MAP.md', '06_DATA_GOVERNANCE_LINEAGE.md',
    '07_ONTOLOGY_SEMANTIC_LAYER.md', '08_KNOWLEDGE_GRAPH_DECISION.md', '09_REQUIREMENTS_TRACEABILITY.md',
    '10_C4_ARCHITECTURE.md', '11_ADR_REGISTER.md', '12_INTEGRATION_CONTRACTS.md',
    '13_MODEL_PROMPT_LIFECYCLE.md', '14_INSURANCE_CONTROL_BOUNDARIES.md', '15_ACTUARIAL_MODEL_RISK.md',
    '16_THREAT_ABUSE_MODEL.md', '17_PRIVACY_CROSS_BORDER.md', '18_RESPONSIBLE_AI_FAIRNESS.md',
    '19_REGULATORY_APPLICABILITY.md', '20_ISO42001_GOVERNANCE.md', '21_ASSURANCE_CASE.md',
    '22_EVALUATION_TEVV.md', '23_TOKEN_FINOPS.md', '24_RELIABILITY_OBSERVABILITY.md',
    '25_INCIDENT_RECOVERY.md', '26_TARGET_OPERATING_MODEL.md', '27_VENDOR_EXIT_RETIREMENT.md',
    '28_PRODUCTION_READINESS.md', '29_NINETY_DAY_ROADMAP_HANDOVER.md', '30_FINAL_DEFENCE.md',
    '31_ELEVATOR_PITCH.md', '32_CHANGE_AND_BENEFITS_CONTROL.md',
]

ALL_INJECTS = [f'INJ-{i:03d}' for i in range(1, 97)]


def is_placeholder(text: str) -> bool:
    return len(text.split()) < 120 or bool(re.search(r'\|\s*\|\s*\|', text)) or 'Participant content' in text


def substantive_files(dirname: str, exts=None, min_bytes: int = 80):
    d = SUB / dirname
    if not d.exists():
        return []
    out = []
    for p in d.rglob('*'):
        if p.is_file() and p.name != '.gitkeep' and (exts is None or p.suffix.lower() in exts) and p.stat().st_size >= min_bytes:
            out.append(p)
    return out


def artefact_status():
    rows = []
    for name in TEMPLATES:
        p = SUB / 'artefacts' / name
        if not p.exists():
            rows.append((name, 'missing'))
            continue
        text = p.read_text(encoding='utf-8', errors='ignore')
        rows.append((name, 'placeholder' if is_placeholder(text) else 'complete'))
    return rows


def read_csv_rows(rel_path: str):
    p = SUB / rel_path
    if not p.exists():
        return None
    with p.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def inject_status():
    rows = read_csv_rows('evidence/inject_traceability.csv')
    if rows is None:
        return None, ALL_INJECTS, {}
    by_id = {r.get('inject_id'): r.get('status', '') for r in rows}
    missing = [i for i in ALL_INJECTS if i not in by_id]
    counts = {}
    for i in ALL_INJECTS:
        s = by_id.get(i, 'missing')
        counts[s] = counts.get(s, 0) + 1
    return by_id, missing, counts


def phase1_status():
    d = SUB / 'evidence' / 'phase1'
    expected = ['01_PROJECT_CHARTER.md', '02_STAKEHOLDER_AND_DECISION_RIGHTS.md']
    rows = []
    for name in expected:
        p = d / name
        if not p.exists():
            rows.append((name, 'missing'))
        else:
            text = p.read_text(encoding='utf-8', errors='ignore')
            rows.append((name, 'placeholder' if is_placeholder(text) else 'complete'))
    return rows


def build_report():
    lines = []
    add = lines.append
    add('AEGIS-INSURE submission progress report')
    add('Generated: ' + datetime.now(timezone.utc).isoformat())
    add('')

    # Artefacts
    art = artefact_status()
    complete = sum(1 for _, s in art if s == 'complete')
    placeholder = sum(1 for _, s in art if s == 'placeholder')
    missing = sum(1 for _, s in art if s == 'missing')
    add(f'## Artefact templates ({complete}/{len(TEMPLATES)} complete, {placeholder} placeholder, {missing} missing)')
    for name, status in art:
        add(f'  [{status:10s}] {name}')
    add('')

    # Phase 1 evidence
    p1 = phase1_status()
    add('## Phase 1 evidence files')
    for name, status in p1:
        add(f'  [{status:10s}] {name}')
    add('')

    # Inject traceability
    by_id, missing_injects, counts = inject_status()
    add('## Inject traceability (96 total)')
    if by_id is None:
        add('  evidence/inject_traceability.csv not found')
    else:
        for status in ('addressed', 'partially-addressed', 'not-yet-addressed', 'missing'):
            if counts.get(status):
                add(f'  {status}: {counts[status]}')
        other = set(counts) - {'addressed', 'partially-addressed', 'not-yet-addressed', 'missing'}
        for status in sorted(other):
            add(f'  {status}: {counts[status]}')
        if missing_injects:
            add('  not tracked at all: ' + ','.join(missing_injects))
    add('')

    # Evidence manifest
    manifest = read_csv_rows('evidence/evidence_manifest.csv')
    add('## Evidence manifest')
    add(f'  rows: {len(manifest) if manifest is not None else "file not found"}')
    add('')

    # Implementation / tests / app / scripts / evaluation
    add('## Implementation and test evidence (final-mode thresholds in parentheses)')
    impl = substantive_files('src') + substantive_files('app')
    tests = substantive_files('tests')
    scripts = substantive_files('scripts')
    fixtures = read_csv_rows('evaluation/public_fixture_results.csv')
    add(f'  src/app substantive files: {len(impl)} (>=3)')
    add(f'  test substantive files: {len(tests)} (>=5)')
    add(f'  one-command scripts: {len(scripts)} (>=5)')
    add(f'  public fixture results rows: {len(fixtures) if fixtures is not None else "file not found"} (18 expected)')
    add('')

    # Runbooks
    add('## Required runbooks')
    for rel in ['runbooks/SETUP.md', 'runbooks/RUN.md', 'runbooks/TEST.md',
                'runbooks/EVALUATE.md', 'runbooks/RESET.md', 'runbooks/INCIDENT_AND_FALLBACK.md']:
        p = SUB / rel
        ok = p.exists() and p.stat().st_size >= 200
        add(f'  [{"complete" if ok else "missing/incomplete":18s}] {rel}')
    add('')

    total_gate_items = len(TEMPLATES) + 2
    done_gate_items = complete + sum(1 for _, s in p1 if s == 'complete')
    add(f'## Overall: {done_gate_items}/{total_gate_items} tracked markdown artefacts complete')
    return '\n'.join(lines) + '\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write', action='store_true', help='also write the report to submission/evidence/PROGRESS_REPORT.md')
    args = ap.parse_args()
    report = build_report()
    print(report)
    if args.write:
        out = SUB / 'evidence' / 'PROGRESS_REPORT.md'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text('```\n' + report + '```\n', encoding='utf-8')
        print('written: ' + str(out.relative_to(ROOT)))


if __name__ == '__main__':
    sys.exit(main())
