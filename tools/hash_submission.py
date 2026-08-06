from pathlib import Path
import csv,hashlib
ROOT=Path(__file__).resolve().parents[1]; sub=ROOT/'submission'; out=sub/'evidence/submission_hashes.csv'; out.parent.mkdir(parents=True,exist_ok=True)
rows=[]
for p in sorted(sub.rglob('*')):
    if p.is_file() and p!=out and p.name!='.gitkeep': rows.append({'path':str(p.relative_to(sub)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
with out.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['path','sha256','bytes']);w.writeheader();w.writerows(rows)
print(out)
