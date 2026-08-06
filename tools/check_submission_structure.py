from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
raise SystemExit(subprocess.call([sys.executable,str(ROOT/'tools/check_submission.py'),'--mode','scaffold'],cwd=ROOT))
