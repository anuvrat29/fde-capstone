from pathlib import Path
import csv,hashlib
ROOT=Path(__file__).resolve().parents[1]
rows=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file(): continue
    rel=str(p.relative_to(ROOT)).replace('\\','/')
    if rel.startswith('submission/') or rel.startswith('.venv/') or p.name in {'FILE_HASHES.csv','VALIDATION_REPORT.json'} or '__pycache__' in p.parts or p.suffix=='.pyc': continue
    rows.append({'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
with (ROOT/'FILE_HASHES.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['path','sha256','bytes']);w.writeheader();w.writerows(rows)
print(f'Hashed {len(rows)} immutable files')
