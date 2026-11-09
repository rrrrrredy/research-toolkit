import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT = BASE.parents[2] / 'frozen-alternate-inputs' / 'test_time_compute_zh'
p = argparse.ArgumentParser()
p.add_argument('source')
p.add_argument('--start', type=int, default=1)
p.add_argument('--end', type=int)
p.add_argument('--headings', action='store_true')
a = p.parse_args()
path = INPUT / 'sources' / (a.source + '.txt')
raw = path.read_bytes()
lines = raw.decode('utf-8-sig').splitlines()
if a.headings:
    import re
    for i, line in enumerate(lines, 1):
        if len(line) < 170 and (re.match(r'^(?:[1-9][0-9]?(?:\.[0-9]+)*\s|[A-K](?:\.[0-9]+)*\s|Abstract|Table\s|Figure\s|Limitations|Conclusion|References|Page\s|=====)', line)):
            print(f'{i}: {line}')
    print('TOTAL_LINES', len(lines))
else:
    end = a.end or min(a.start + 40, len(lines))
    chosen = lines[a.start-1:end]
    content = '\n'.join(f'{i}: {line}' for i,line in enumerate(chosen,a.start))
    if len(content)>26000:
        raise SystemExit(f'Chunk too large ({len(content)} chars); narrow range')
    print(content)
    ledger_path = BASE / 'reading-ledger.json'
    ledger = json.loads(ledger_path.read_text('utf-8')) if ledger_path.exists() else []
    ledger.append({'source_id':a.source,'path':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'range_type':'line','start':a.start,'end':end,'actual_read_scope':'displayed original lines','at':datetime.now(timezone.utc).isoformat()})
    ledger_path.write_text(json.dumps(ledger,ensure_ascii=False,indent=2),'utf-8')
