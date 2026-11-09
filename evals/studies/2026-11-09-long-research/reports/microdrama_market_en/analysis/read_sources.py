import sys, json, re, hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
PACK=HERE.parents[2]/'frozen-alternate-inputs'/'microdrama_market_en'
# HERE: implementation/research/case/codex-production
PACK=HERE.parents[2]/'frozen-alternate-inputs'/'microdrama_market_en'
sources={s['source_id']:s for s in json.loads((PACK/'sources.json').read_text(encoding='utf-8-sig'))}
ledger_path=HERE/'reading-ledger.json'
ledger=json.loads(ledger_path.read_text(encoding='utf-8')) if ledger_path.exists() else []
sid=sys.argv[1]; mode=sys.argv[2]; spec=sys.argv[3] if len(sys.argv)>3 else ''
s=sources[sid]; p=PACK/s['local_original']; raw=p.read_bytes(); body=raw.decode('utf-8-sig'); lines=body.splitlines()
if mode=='pages':
    wanted={int(x) for x in spec.split(',')}; current=None; indices=[]
    for i,line in enumerate(lines):
        m=re.match(r'## Page (\d+)',line)
        if m: current=int(m.group(1))
        if current in wanted: indices.append(i)
elif mode=='lines':
    a,b=map(int,spec.split('-')); indices=list(range(a-1,min(b,len(lines))))
elif mode=='search':
    regex=re.compile(spec); chosen=set()
    for i,line in enumerate(lines):
        if regex.search(line): chosen.update(range(max(0,i-3),min(len(lines),i+7)))
    indices=sorted(chosen)
else: indices=list(range(len(lines)))
ranges=[]
for i in indices:
    if ranges and i+1==ranges[-1][1]+1: ranges[-1][1]=i+1
    else: ranges.append([i+1,i+1])
out='\n'.join(f'{i+1}: {lines[i]}' for i in indices)
print(f'[{sid}] {s["title"]}\nURL: {s["url"]}\nTOTAL LINES: {len(lines)}\n{out}')
ledger.append({'source_id':sid,'url':s['url'],'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'reading_mode':mode,'requested_scope':spec,'actual_line_ranges':ranges,'source_pack_scope':s['locator'],'access_note':'Frozen retained web output or access record; not original full website' if sid in {'CP10','CP20','CP23'} else 'Frozen original text; reading restricted to recorded lines/pages'})
ledger_path.write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
(HERE/'reading-extracts').mkdir(exist_ok=True)
(HERE/'reading-extracts'/f'{len(ledger):02}-{sid}.txt').write_text(out,encoding='utf-8')
