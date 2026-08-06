from pathlib import Path
import csv, json, hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def selector_matches(path,selector):
    if selector=='document': return True
    if '=' not in selector: return False
    key,val=selector.split('=',1)
    if path.suffix.lower()=='.csv':
        with path.open(encoding='utf-8-sig',newline='') as f:
            return any((r.get(key) or '')==val for r in csv.DictReader(f))
    return True
errors=[]
fixtures=sorted((ROOT/'evaluation/fixtures').glob('EV-*/fixture.json'))
for p in fixtures:
    x=json.loads(p.read_text(encoding='utf-8'))
    cp=ROOT/x['response_contract']
    if not cp.exists(): errors.append(f'{p}: missing contract')
    for e in x['evidence']:
        sp=ROOT/e['path']
        if not sp.exists(): errors.append(f'{p}: missing {e["path"]}'); continue
        if sha(sp)!=e['sha256']: errors.append(f'{p}: hash mismatch {e["path"]}')
        if not selector_matches(sp,e['selector']): errors.append(f'{p}: selector not found {e["path"]} {e["selector"]}')
print(f'Public fixtures: {len(fixtures)}')
print('Fixture validation:', 'PASS' if not errors else 'FAIL')
for e in errors: print('-',e)
raise SystemExit(1 if errors else 0)
