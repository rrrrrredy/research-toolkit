"""Acquire public model/runtime originals, without model inference or application changes."""
from pathlib import Path
import json,sys,concurrent.futures,urllib.request,urllib.parse,hashlib
from datetime import datetime,timezone
B=Path(__file__).resolve().parent;R=B.parents[2]
sys.path.insert(0,str(R));import fetch_sources as f
f.ROOT=B/'supplemental-sources'
def raw(sid,url):
 d=f.ROOT/sid;d.mkdir(parents=True,exist_ok=True)
 m={'id':sid,'url':url,'accessed_at':datetime.now(timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ResearchToolkit-Author'}),timeout=40) as response:
   data=response.read();m.update(final_url=response.url,status='retrieved',bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
  (d/'original.txt').write_bytes(data)
 except Exception as exc:m.update(status='failed',error=str(exc))
 (d/'retrieval.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
 return {k:m.get(k) for k in ['id','status','bytes','error']}
ITEMS=[
('ODM-S01','https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/raw/main/config.json'),
('ODM-S02','https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/raw/main/README.md'),
('ODM-S03','https://api.github.com/repos/NVIDIA-AI-IOT/whisper_trt/commits?until=2026-11-09T23:59:59Z&per_page=1'),
('ODM-S04','https://api.github.com/repos/google-ai-edge/LiteRT-LM/commits?path=README.md&until=2025-08-01T00:00:00Z&per_page=1'),
('ODM-S05','https://api.github.com/repos/zzadiues3338/ASR-energy-jetson/git/trees/main?recursive=1'),
('ODM-S06','https://raw.githubusercontent.com/meta-llama/llama-models/main/models/llama3_2/MODEL_CARD.md'),
('ODM-S07','https://api.github.com/repos/basecompute/baseRT/git/trees/main?recursive=1'),
('ODM-S08','https://machinelearning.apple.com/research/apple-foundation-models-tech-report-2025'),
('ODM-S09','https://proceedings.mlr.press/v267/yang25s.html'),
]
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for result in pool.map(lambda x:raw(*x),ITEMS):print(json.dumps(result),flush=True)
