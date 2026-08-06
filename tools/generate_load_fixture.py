from pathlib import Path
import argparse,csv,random,datetime
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--rows',type=int,default=10000);p.add_argument('--seed',type=int,default=42);p.add_argument('--output',default='submission/evidence/generated_load_claims.csv');a=p.parse_args()
if a.rows<1 or a.rows>1000000: raise SystemExit('rows must be between 1 and 1,000,000')
r=random.Random(a.seed); out=ROOT/a.output; out.parent.mkdir(parents=True,exist_ok=True)
policies=['POL-IN-HO-1001','POL-IN-SME-1001','POL-DE-MO-0042','POL-US-CY-9008']; currencies=['INR','INR','EUR','USD']; losses=['flood','business_interruption','collision_fire','cyber_interruption']
with out.open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['claim_id','policy_id','reported_at','loss_type','claimed_amount','currency','synthetic_seed'])
 base=datetime.datetime(2026,7,28,tzinfo=datetime.timezone.utc)
 for i in range(a.rows):
  k=r.randrange(len(policies)); ts=base+datetime.timedelta(seconds=r.randrange(7*86400)); amt=r.randrange(1000,5000000)
  w.writerow([f'LOAD-{i+1:07d}',policies[k],ts.isoformat(),losses[k],amt,currencies[k],a.seed])
print(out)
