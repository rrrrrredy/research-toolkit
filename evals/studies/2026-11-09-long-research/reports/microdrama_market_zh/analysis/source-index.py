from pathlib import Path
import json,csv,re
from datetime import datetime,timezone
p=Path(__file__).resolve().parent
rows=[]
for root in [p.parents[2]/'sources',p/'sources']:
 for d in sorted(root.iterdir()):
  if not re.fullmatch(r'(MD\d+|MDX\d+|CP\d+)',d.name):continue
  m=d/'retrieval.json'
  if not m.exists():continue
  v=json.loads(m.read_text(encoding='utf-8-sig'))
  rows.append(dict(id=d.name,title=v.get('title',''),source_url=v.get('url',''),final_url=v.get('final_url',''),
                   local_directory=str(d),retrieval_status=v.get('status',''),
                   web_fallback_saved=(d/'web-access.txt').exists(),
                   retrieved_at=v.get('accessed_at',''),sha256=v.get('sha256',''),
                   reading_record='reading-log.md; actual scope documented manually',agent_identity='/root/microdrama_research'))
with (p/'source-locations.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print('Source metadata rows:',len(rows))
for sid in ['CP18','CP27']:
 s=(p/'sources'/sid/'original.html').read_text(encoding='utf-8')
 hits=re.findall(r'updateTime[^:]{0,10}:\\?"(\d+)\\?"',s)
 print(sid,sorted(set(hits)))
