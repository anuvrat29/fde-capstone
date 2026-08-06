from pathlib import Path
import csv,json,hashlib,re,sys,subprocess,os
ROOT=Path(__file__).resolve().parents[1]
errors=[]; checks=[]
def add(name,ok,detail=''):
    checks.append({'check':name,'status':'PASS' if ok else 'FAIL','detail':detail})
    if not ok: errors.append(name+(': '+detail if detail else ''))
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
# Required paths
required=['README.md','START_HERE.md','DEFINITION_OF_DONE.md','case/INTEGRATED_CASE.md','data/injects.json','data/inject_evidence_records.csv','metadata/DATASET_CATALOG.csv','metadata/COLUMN_DICTIONARY.csv','metadata/RELATIONSHIP_RULES.csv','evaluation/FIXTURE_INDEX.csv','evaluation/INJECT_TEST_OBLIGATIONS.csv','requirements/SCORING_RUBRIC.csv','tools/check_submission.py']
add('required files',all((ROOT/x).exists() for x in required),'missing: '+','.join(x for x in required if not (ROOT/x).exists()))
# Parse CSV/JSON and profile
csvs=sorted((ROOT/'data').glob('*.csv')); bad=[]
for p in csvs:
    try:
        with p.open(encoding='utf-8-sig',newline='') as f:
            r=csv.reader(f); rows=list(r)
        if not rows or len(rows[0])!=len(set(rows[0])): bad.append(p.name)
        if any(len(x)!=len(rows[0]) for x in rows[1:]): bad.append(p.name)
    except Exception: bad.append(p.name)
add('CSV parse and width',not bad,','.join(sorted(set(bad))))
# Exact row duplicates and declared unique keys
dupfiles=[]
for p in csvs:
    with p.open(encoding='utf-8-sig',newline='') as f: rr=list(csv.DictReader(f)); fields=rr[0].keys() if rr else []
    if len(rr)!=len({tuple(r.get(k,'') for k in fields) for r in rr}): dupfiles.append(p.name)
add('no exact duplicate rows',not dupfiles,','.join(dupfiles))
ukerr=[]
with (ROOT/'metadata/UNIQUE_KEY_RULES.csv').open(encoding='utf-8-sig',newline='') as f: uks=list(csv.DictReader(f))
for r in uks:
    with (ROOT/'data'/r['dataset']).open(encoding='utf-8-sig',newline='') as f: rr=list(csv.DictReader(f))
    cols=r['columns'].split('+'); vals=[tuple(x.get(c,'') for c in cols) for x in rr]
    if len(vals)!=len(set(vals)): ukerr.append(r['rule_id'])
add('declared unique keys',not ukerr,','.join(ukerr))
json_bad=[]
for p in ROOT.rglob('*.json'):
    try: json.loads(p.read_text(encoding='utf-8'))
    except Exception as e: json_bad.append(str(p.relative_to(ROOT)))
add('JSON parse',not json_bad,','.join(json_bad))
# Counts and IDs
injects=json.loads((ROOT/'data/injects.json').read_text(encoding='utf-8'))
ids=[x.get('id') for x in injects]
add('96 sequential unique injects',ids==[f'INJ-{i:03d}' for i in range(1,97)])
case=(ROOT/'case/INTEGRATED_CASE.md').read_text(encoding='utf-8')
add('case contains every inject',all(i in case for i in ids))
sc=json.loads((ROOT/'evaluation/public_scenarios.json').read_text(encoding='utf-8'))
add('18 sequential public scenarios',[x.get('id') for x in sc]==[f'EV-{i:02d}' for i in range(1,19)])
# Evidence path resolution
search=[ROOT/'data',ROOT/'knowledge',ROOT/'starter/api_samples',ROOT/'starter']; missing=[]
for x in injects:
    for ref in x['evidence']:
        if not any((d/ref).exists() for d in search): missing.append(x['id']+':'+ref)
add('inject evidence paths resolve',not missing,','.join(missing))
# Injection ledger and obligations
with (ROOT/'data/inject_evidence_records.csv').open(encoding='utf-8-sig',newline='') as f: ledger=list(csv.DictReader(f))
add('inject evidence ledger coverage',set(r['inject_id'] for r in ledger)==set(ids),f'rows={len(ledger)}')
locerr=[]
for r in ledger:
    p=ROOT/r['original_evidence_path']
    loc=r.get('source_locator','')
    if loc.startswith('record_id='):
        with p.open(encoding='utf-8-sig',newline='') as f: rr=list(csv.DictReader(f))
        if not any(x.get('record_id')==loc.split('=',1)[1] for x in rr): locerr.append(r['evidence_record_id'])
add('inject evidence locators',not locerr,','.join(locerr))
with (ROOT/'evaluation/INJECT_TEST_OBLIGATIONS.csv').open(encoding='utf-8-sig',newline='') as f: obl=list(csv.DictReader(f))
add('one test obligation per inject',len(obl)==96 and set(r['inject_id'] for r in obl)==set(ids))
# Knowledge catalog
with (ROOT/'data/knowledge_catalog.csv').open(encoding='utf-8-sig',newline='') as f: kc=list(csv.DictReader(f))
kn={p.name for p in (ROOT/'knowledge').glob('*.md')}; cat={r['filename'] for r in kc}
add('knowledge catalog complete',kn==cat,f'missing={sorted(kn-cat)} stale={sorted(cat-kn)}')
kh=[r['filename'] for r in kc if not r.get('sha256') or h(ROOT/'knowledge'/r['filename'])!=r['sha256']]
add('knowledge document hashes',not kh,','.join(kh))
# Dataset catalog exact profiles
with (ROOT/'metadata/DATASET_CATALOG.csv').open(encoding='utf-8-sig',newline='') as f: profiles={r['dataset']:r for r in csv.DictReader(f)}
profile_err=[]
for p in csvs:
    with p.open(encoding='utf-8-sig',newline='') as f: rr=list(csv.reader(f))
    pr=profiles.get(p.name)
    if not pr or int(pr['rows'])!=len(rr)-1 or int(pr['columns'])!=len(rr[0]) or pr['sha256']!=h(p): profile_err.append(p.name)
add('dataset profiles exact',not profile_err,','.join(profile_err))
# Relationships
with (ROOT/'metadata/RELATIONSHIP_RULES.csv').open(encoding='utf-8-sig',newline='') as f: rels=list(csv.DictReader(f))
rel_err=[]
for r in rels:
    with (ROOT/'data'/r['child_dataset']).open(encoding='utf-8-sig',newline='') as f: child=list(csv.DictReader(f))
    with (ROOT/'data'/r['parent_dataset']).open(encoding='utf-8-sig',newline='') as f: parent=list(csv.DictReader(f))
    pv={x[r['parent_column']] for x in parent if x[r['parent_column']]}
    unmatched={x[r['child_column']] for x in child if x[r['child_column']] and x[r['child_column']] not in pv}
    if unmatched and r['allow_unmatched']!='yes': rel_err.append(r['relationship_id']+':'+','.join(sorted(unmatched)))
add('declared relationships',not rel_err,';'.join(rel_err))
# Rubric exact total
with (ROOT/'requirements/SCORING_RUBRIC.csv').open(encoding='utf-8-sig',newline='') as f: rubric=list(csv.DictReader(f))
add('rubric totals 200',sum(int(r['points']) for r in rubric)==200)
# Templates are structured rather than placeholder shells
tmpl=list((ROOT/'templates').glob('*.md')); terr=[]
for p in tmpl:
    tx=p.read_text(encoding='utf-8')
    if len(tx.splitlines())<45 or '## Acceptance criteria' not in tx or '## Traceability' not in tx: terr.append(p.name)
add('32 structured templates',len(tmpl)==32 and not terr,','.join(terr))
# Internal path references; participant-output paths and wildcards are intentionally unresolved at scaffold stage
referr=[]; known=[ROOT,ROOT/'data',ROOT/'knowledge',ROOT/'starter',ROOT/'starter/api_samples',ROOT/'evaluation',ROOT/'requirements',ROOT/'runbooks',ROOT/'sources',ROOT/'metadata']
for mp in ROOT.rglob('*.md'):
    tx=mp.read_text(encoding='utf-8')
    for m in re.finditer(r'`([^`\n]+)`',tx):
        s=m.group(1).strip()
        if s.startswith(('http://','https://')) or (' ' in s and ';' not in s): continue
        for ref in [x.strip() for x in s.split(';')]:
            if not re.search(r'\.(md|csv|json|py|js|html|sh|ps1)$',ref,re.I): continue
            if ref.startswith('submission/') or '*' in ref: continue
            candidates=[ROOT/ref,mp.parent/ref]+[d/ref for d in known]
            if not any(x.exists() for x in candidates): referr.append(str(mp.relative_to(ROOT))+':'+ref)
add('internal file references',not referr,';'.join(referr[:20]))
# Source verification metadata is present and uses official HTTPS anchors
with (ROOT/'sources/SOURCE_VERIFICATION.csv').open(encoding='utf-8-sig',newline='') as f: sr=list(csv.DictReader(f))
add('source verification register',len(sr)>=9 and all(x['url'].startswith('https://') for x in sr))
# Fixtures and contract scripts
for script,name in [('evaluation/validate_fixtures.py','public fixtures'),('evaluation/validate_contracts.py','contract tests')]:
    cp=subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    add(name,cp.returncode==0,(cp.stdout+cp.stderr).strip())
# Hashes immutable files
hashfile=ROOT/'FILE_HASHES.csv'; hash_err=[]
if hashfile.exists():
    with hashfile.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    for r in rows:
        p=ROOT/r['path']
        if not p.exists() or h(p)!=r['sha256'] or str(p.stat().st_size)!=r['bytes']: hash_err.append(r['path'])
    expected={str(p.relative_to(ROOT)).replace('\\','/') for p in ROOT.rglob('*') if p.is_file() and not str(p.relative_to(ROOT)).replace('\\','/').startswith('submission/') and p.name not in {'FILE_HASHES.csv','VALIDATION_REPORT.json'} and '__pycache__' not in p.parts}
    listed={r['path'] for r in rows}
    if expected!=listed: hash_err.append('coverage mismatch')
add('immutable file hashes',not hash_err,','.join(hash_err[:20]))
# App deterministic and no unsafe rendering in challenge explorer
app=(ROOT/'app/app.js').read_text(encoding='utf-8')
add('explorer avoids HTML interpolation','innerHTML' not in app and 'insertAdjacentHTML' not in app)
# No runtime caches
cache=[str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.name=='__pycache__' or p.suffix=='.pyc']
add('no runtime caches',not cache,','.join(cache))
report={'package':'Project AEGIS-INSURE Workshop Ready v2','generated_at':'deterministic-preflight','summary':{'injects':len(injects),'data_csv':len(csvs),'knowledge_documents':len(kn),'templates':len(list((ROOT/'templates').glob('*.md'))),'public_fixtures':len(sc),'checks':len(checks),'failures':len(errors)},'checks':checks}
(ROOT/'VALIDATION_REPORT.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('AEGIS-INSURE deep package verification')
for c in checks: print(f"[{c['status']}] {c['check']}"+(f" — {c['detail']}" if c['detail'] and c['status']=='FAIL' else ''))
print('PASS' if not errors else 'FAIL')
raise SystemExit(1 if errors else 0)
