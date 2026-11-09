from pathlib import Path
import sys,json,urllib.request,urllib.parse,hashlib,concurrent.futures
from datetime import datetime,timezone
B=Path(__file__).resolve().parent; R=B.parents[2]
sys.path.insert(0,str(R));import fetch_sources as f
f.ROOT=B/'supplemental-sources'
items=[
('TE-S13','https://raw.githubusercontent.com/meta-llama/llama-models/main/models/llama3_1/MODEL_CARD.md'),
('TE-S14','https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/gpu-accelerated/ncadsh100v5-series'),
('TE-S15','https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027'),
('TE-S16','https://www.microsoft.com/en-us/investor/earnings/fy-2027-q1/press-release-webcast'),
('TE-S17','https://www.microsoft.com/en-us/Investor/earnings/FY-2027-Q1/metrics'),
('TE-S18','https://arxiv.org/html/2507.09089v1'),
('TE-S19','https://ai.google.dev/gemini-api/docs/caching?generate-content=true'),
('TE-S20','https://raw.githubusercontent.com/pChitral/vllm-cost-meter/1c40823/README.md'),
]
def raw(sid,url):
 d=f.ROOT/sid;d.mkdir(parents=True,exist_ok=True)
 m={'id':sid,'url':url,'accessed_at':datetime.now(timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ResearchToolkit-Author'}),timeout=45) as res:
   data=res.read();m.update(final_url=res.url,status='retrieved',bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
  (d/'original.txt').write_bytes(data)
 except Exception as e:m.update(status='failed',error=str(e))
 (d/'retrieval.json').write_text(json.dumps(m,indent=2),encoding='utf-8');return {k:m.get(k) for k in ['id','status','bytes','error']}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for result in pool.map(lambda x:raw(*x) if 'raw.githubusercontent' in x[1] else f.fetch({'id':x[0],'url':x[1]}),items):print(json.dumps(result),flush=True)
 query="serviceName eq 'Virtual Machines' and armRegionName eq 'eastus' and armSkuName eq 'Standard_NC80adis_H100_v5' and priceType eq 'Consumption'"
 url='https://prices.azure.com/api/retail/prices?'+urllib.parse.urlencode({'$filter':query,'currencyCode':'USD'})
 print(json.dumps(raw('TE-S21',url)),flush=True)
 print(json.dumps(raw('TE-S22','https://api.github.com/repos/pChitral/vllm-cost-meter/git/trees/1c40823?recursive=1')),flush=True)
