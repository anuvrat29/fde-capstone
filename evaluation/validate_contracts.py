from pathlib import Path
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]

def walk_keys(obj):
    if isinstance(obj,dict):
        for k,v in obj.items():
            yield k
            yield from walk_keys(v)
    elif isinstance(obj,list):
        for x in obj: yield from walk_keys(x)

def validate(payload,schema):
    errors=[]
    if not isinstance(payload,dict): return ['payload must be an object']
    required=schema.get('required',[])
    for k in required:
        if k not in payload: errors.append('missing required field: '+k)
    if schema.get('additionalProperties') is False:
        allowed=set(schema.get('properties',{}))
        for k in payload:
            if k not in allowed: errors.append('unexpected field: '+k)
    expected=schema.get('x-workflow')
    if expected and payload.get('workflow')!=expected: errors.append('workflow mismatch')
    status=payload.get('status')
    allowed_status=schema.get('properties',{}).get('status',{}).get('enum',[])
    if status is not None and allowed_status and status not in allowed_status: errors.append('invalid status')
    found=set(walk_keys(payload))
    for k in schema.get('x-prohibited-fields',[]):
        if k in found: errors.append('prohibited field: '+k)
    for k in ['facts','inferences','conflicts','missing_evidence','recommendations','prohibited_actions','evidence']:
        if k in payload and not isinstance(payload[k],list): errors.append(k+' must be an array')
    auth=payload.get('authorization_context',{})
    if auth and not auth.get('current',False): errors.append('authorization must be current')
    for i,e in enumerate(payload.get('evidence',[])):
        for k in ['evidence_id','source_path','record_locator','sha256','authority_status','fact']:
            if k not in e: errors.append(f'evidence[{i}] missing {k}')
        if 'sha256' in e and not re.fullmatch(r'[0-9a-f]{64}',str(e['sha256'])): errors.append(f'evidence[{i}] invalid sha256')
    return errors

def main():
    errors=[]
    for p in sorted((ROOT/'evaluation/contract_tests/positive').glob('*.json')):
        schema=json.loads((ROOT/'evaluation/contracts'/(p.stem+'_response.schema.json')).read_text())
        e=validate(json.loads(p.read_text()),schema)
        if e: errors.append(f'positive {p.name} failed: {e}')
    for p in sorted((ROOT/'evaluation/contract_tests/negative').glob('*.json')):
        schema=json.loads((ROOT/'evaluation/contracts'/(p.stem+'_response.schema.json')).read_text())
        e=validate(json.loads(p.read_text()),schema)
        if not e: errors.append(f'negative {p.name} unexpectedly passed')
    print('Contract tests:', 'PASS' if not errors else 'FAIL')
    for e in errors: print('-',e)
    return 1 if errors else 0
if __name__=='__main__': raise SystemExit(main())
