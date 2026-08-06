from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]

def load(name):
    with open(ROOT/'data'/name,newline='',encoding='utf-8') as f: return list(csv.DictReader(f))
issues=[]
claims=load('claims.csv')
if len({r['currency'] for r in claims})>1: issues.append('mixed currencies cannot be summed without valuation rules')
if any(r['status']=='revoked' for r in load('users_entitlements.csv')) and any(r['cached_status']=='active' for r in load('access_cache.csv')): issues.append('authorization cache can outlive revocation')
if any(r['status']=='mismatch' for r in load('model_artifacts.csv')): issues.append('deployed model artefact differs from approved registry')
if (ROOT/'knowledge/MALICIOUS_ADJUSTER_REPORT.md').exists(): issues.append('untrusted evidence contains prompt-like instructions')
print('AEGIS-INSURE brownfield diagnostic')
for i,x in enumerate(issues,1): print(f'{i}. {x}')
print('Only an initial subset is surfaced. Full discovery is participant work.')
