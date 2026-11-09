"""Read-only public-source acquisition for author research; no model/API calls."""
from pathlib import Path
import sys, json, hashlib, urllib.request, concurrent.futures
from datetime import datetime, timezone
BASE=Path(__file__).resolve().parent
ROOT=BASE/'supplemental-sources'
R=BASE.parents[2]
sys.path.insert(0,str(R))
import fetch_sources as inherited
inherited.ROOT=ROOT
ITEMS=[
('TE-S01','https://openai.com/index/gpt-4-1/?trk=article-ssr-frontend-pulse_little-text-block'),
('TE-S02','https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/'),
('TE-S03','https://ai.google.dev/gemini-api/docs/pricing.md'),
('TE-S04','https://ai.google.dev/gemini-api/docs/caching.md'),
('TE-S05','https://api-docs.deepseek.com/news/news1226'),
('TE-S06','https://api-docs.deepseek.com/news/news250120'),
('TE-S07','https://api-docs.deepseek.com/guides/search'),
('TE-S08','https://api-docs.deepseek.com/guides/kv_cache'),
('TE-S09','https://api-docs.deepseek.com/guides/thinking_mode'),
('TE-S10','https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct/raw/main/README.md'),
('TE-S11','https://developers.googleblog.com/en/gemini-2-5-thinking-model-updates/'),
('TE-S12','https://www.anthropic.com/news/claude-3-5-sonnet'),
]
def fetch(item):
 sid,url=item
 if url.endswith('.md'):
  folder=ROOT/sid; folder.mkdir(parents=True,exist_ok=True)
  meta={'id':sid,'url':url,'accessed_at':datetime.now(timezone.utc).isoformat()}
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as response:
    raw=response.read();meta.update(final_url=response.url,status='retrieved',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
   (folder/'original.md').write_bytes(raw);(folder/'original.txt').write_bytes(raw)
  except Exception as exc:meta.update(status='failed',error=str(exc))
  (folder/'retrieval.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
  return {k:meta.get(k) for k in ('id','status','bytes','error')}
 return inherited.fetch({'id':sid,'url':url})
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for result in pool.map(fetch,ITEMS):print(json.dumps(result),flush=True)
