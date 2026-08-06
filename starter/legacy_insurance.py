"""Deliberately unsafe brownfield starter. Do not use for real insurance decisions."""
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name):
    with open(ROOT/'data'/name,newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))

def get_claim(claim_id):
    # Defect: first match, no tenant or authority check.
    return next((r for r in load('claims.csv') if r['claim_id']==claim_id),None)

def policy_for_claim(claim):
    # Defect: policy number treated as globally unique; ignores version and effective time.
    return next((r for r in load('policies.csv') if r['policy_id']==claim['policy_id']),None)

def coverage_summary(claim_id,user_role='viewer'):
    # Defect: role string is trusted; untrusted notes are treated as instructions.
    claim=get_claim(claim_id); policy=policy_for_claim(claim)
    return {'claim':claim,'policy':policy,'decision':'APPROVE','confidence':0.97,'user_role':user_role}

def total_claimed():
    # Defect: sums mixed currencies as though equivalent.
    return sum(float(r['claimed_amount']) for r in load('claims.csv'))

def set_reserve(claim_id,amount):
    # Defect: side effect exposed with no authorization, approval, currency or idempotency.
    return {'claim_id':claim_id,'reserve':amount,'status':'written'}

if __name__=='__main__':
    print(coverage_summary('CLM-10001'))
    print('unsafe mixed-currency total',total_claimed())
