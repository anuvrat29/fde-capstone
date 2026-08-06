from pathlib import Path
import subprocess,sys,os
ROOT=Path(__file__).resolve().parent
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
steps=[['tools/build_explorer.py'],['tools/verify_package.py'],['starter/baseline_diagnostics.py'],['tools/check_submission.py','--mode','scaffold']]
for args in steps:
    print('\n==>',' '.join(args))
    cp=subprocess.run([sys.executable,*[str(ROOT/x) if i==0 else x for i,x in enumerate(args)]],cwd=ROOT,env=env)
    if cp.returncode: raise SystemExit(cp.returncode)
print('\nPreflight complete. Open app/index.html and begin with START_HERE.md.')
