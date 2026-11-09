from pathlib import Path
import sys,json,hashlib,urllib.request,concurrent.futures
from datetime import datetime,timezone
B=Path(__file__).resolve().parent;R=B.parents[2]
sys.path.insert(0,str(R));import fetch_sources as f
f.ROOT=B/'supplemental-sources'
def raw(sid,url):
 d=f.ROOT/sid;d.mkdir(parents=True,exist_ok=True);m={'id':sid,'url':url,'accessed_at':datetime.now(timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 ResearchAuthor contact research@example.org'}),timeout=40) as r:data=r.read();m.update(final_url=r.url,status='retrieved',bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
  (d/'original.txt').write_bytes(data)
 except Exception as e:m.update(status='failed',error=str(e))
 (d/'retrieval.json').write_text(json.dumps(m,indent=2),encoding='utf-8');return {k:m.get(k) for k in ['id','status','bytes','error']}
ITEMS=[
('AIDD-S01','https://www.nature.com/articles/s41587-024-02143-0'),
('AIDD-S02','https://www.nature.com/articles/s41591-025-03743-2'),
('AIDD-S03','https://ir.recursion.com/static-files/644d572d-a9f8-430a-9412-559e361c3dd5'),
('AIDD-S04','https://ir.recursion.com/node/13186/pdf'),
('AIDD-S05','https://www.sec.gov/Archives/edgar/data/1601830/000160183026000039/rxrx-20251231.htm'),
('AIDD-S06','https://pmc.ncbi.nlm.nih.gov/articles/PMC7745180/'),
('AIDD-S07','https://pmc.ncbi.nlm.nih.gov/articles/PMC8409066/'),
('AIDD-S08','https://pmc.ncbi.nlm.nih.gov/articles/PMC9333998/'),
('AIDD-S09','https://pmc.ncbi.nlm.nih.gov/articles/PMC4356181/'),
('AIDD-S10','https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2021.709856/full')]
REGS=[('AIDD-R01','NCT05938920'),('AIDD-R02','NCT07687459'),('AIDD-R03','NCT05085561')]
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as p:
  for r in p.map(f.fetch,[{'id':i,'url':u} for i,u in ITEMS]):print(json.dumps(r),flush=True)
  for r in p.map(lambda x:raw(x[0],'https://clinicaltrials.gov/api/v2/studies/'+x[1]),REGS):print(json.dumps(r),flush=True)
