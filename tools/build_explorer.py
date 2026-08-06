from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
injects=json.loads((ROOT/'data/injects.json').read_text(encoding='utf-8'))
summary={'inject_count':len(injects),'csv_count':len(list((ROOT/'data').glob('*.csv'))),'knowledge_count':len(list((ROOT/'knowledge').glob('*.md')))}
payload={'injects':injects,'summary':summary}
text='window.AEGIS_DATA = '+json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':'))+';\n'
(ROOT/'app/data.js').write_text(text,encoding='utf-8')
print('Rebuilt app/data.js deterministically')
