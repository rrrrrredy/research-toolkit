from pathlib import Path
import sys,json
from concurrent.futures import ThreadPoolExecutor
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parents[2]))
import fetch_sources
fetch_sources.ROOT=BASE/'sources'
items=json.loads((BASE/'supplement-manifest-3.json').read_text(encoding='utf-8'))
with ThreadPoolExecutor(max_workers=4) as p:
    for r in p.map(fetch_sources.fetch,items):
        print(json.dumps(r,ensure_ascii=False),flush=True)

