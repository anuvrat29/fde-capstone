from pathlib import Path
import argparse,csv,re,sys,json
ROOT=Path(__file__).resolve().parents[1]
SUB=ROOT/'submission'
p=argparse.ArgumentParser();p.add_argument('--mode',choices=['scaffold','final'],default='scaffold');a=p.parse_args()
errors=[]
required_dirs=['app','artefacts','evaluation','evidence','runbooks','scripts','src','tests']
for d in required_dirs:
    if not (SUB/d).is_dir(): errors.append('missing directory: '+d)
if a.mode=='final':
    def substantive_files(d,exts=None):
        items=[]
        for p in (SUB/d).rglob('*') if (SUB/d).exists() else []:
            if p.is_file() and p.name!='.gitkeep' and (exts is None or p.suffix.lower() in exts) and p.stat().st_size>=80: items.append(p)
        return items
    impl=substantive_files('src')+substantive_files('app')
    if len(impl)<3: errors.append('at least three substantive implementation/app files required')
    if len(substantive_files('tests'))<5: errors.append('at least five substantive test files required')
    artefacts=substantive_files('artefacts',{'.md'})
    if len(artefacts)<32: errors.append('32 completed markdown artefacts required')
    placeholders=[]
    for p in artefacts:
        t=p.read_text(encoding='utf-8',errors='ignore')
        if len(t.split())<120 or re.search(r'\|\s*\|\s*\|',t) or 'Participant content' in t: placeholders.append(p.name)
    if placeholders: errors.append('artefacts appear incomplete: '+','.join(placeholders[:8]))
    manifests={
      'evidence/evidence_manifest.csv':['evidence_id','source_path','sha256'],
      'evidence/inject_traceability.csv':['inject_id'],
      'evaluation/public_fixture_results.csv':['scenario_id','status'],
    }
    for rel,cols in manifests.items():
        p=SUB/rel
        if not p.exists(): errors.append('missing '+rel); continue
        try:
            with p.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f)); fields=f.seek(0) or []
            if not rows: errors.append(rel+' is empty')
            headers=set(rows[0].keys()) if rows else set()
            if not set(cols)<=headers: errors.append(rel+' missing columns '+','.join(set(cols)-headers))
            if rel.endswith('inject_traceability.csv') and {r.get('inject_id') for r in rows}!={f'INJ-{i:03d}' for i in range(1,97)}: errors.append('inject traceability must contain all 96 injects')
            if rel.endswith('public_fixture_results.csv') and {r.get('scenario_id') for r in rows}!={f'EV-{i:02d}' for i in range(1,19)}: errors.append('fixture results must contain all 18 scenarios')
        except Exception as e: errors.append(rel+' cannot be parsed: '+str(e))
    for rel in ['evaluation/release_gates.md','runbooks/SETUP.md','runbooks/RUN.md','runbooks/TEST.md','runbooks/EVALUATE.md','runbooks/RESET.md','runbooks/INCIDENT_AND_FALLBACK.md']:
        p=SUB/rel
        if not p.exists() or p.stat().st_size<200: errors.append('missing or incomplete '+rel)
    scripts=substantive_files('scripts')
    if len(scripts)<5: errors.append('one-command setup/run/test/evaluate/reset scripts required')
    secret_patterns=[r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'(?i)api[_-]?key\s*[:=]\s*[A-Za-z0-9_-]{16,}']
    for p in SUB.rglob('*'):
        if p.is_file() and p.stat().st_size<2_000_000:
            t=p.read_text(encoding='utf-8',errors='ignore')
            if any(re.search(x,t) for x in secret_patterns): errors.append('possible secret in '+str(p.relative_to(SUB)))
print(f'AEGIS-INSURE submission validation ({a.mode})')
if errors:
    print('FAIL'); [print('-',e) for e in errors]; raise SystemExit(1)
print('PASS')
