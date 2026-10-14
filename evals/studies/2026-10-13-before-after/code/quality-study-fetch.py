import concurrent.futures, hashlib, io, json, urllib.request
from pathlib import Path
from lxml import html
from pypdf import PdfReader

ROOT=Path(__file__).parent/'output/quality-study-20261013/sources'
SOURCES={
 'rag-long':'https://aclanthology.org/2024.emnlp-industry.66.pdf',
 'lost-middle':'https://aclanthology.org/2024.tacl-1.9.pdf',
 'contextual':'https://www.anthropic.com/engineering/contextual-retrieval',
 'compute-optimal':'https://arxiv.org/html/2408.03314v1',
 's1':'https://arxiv.org/html/2501.19393v1',
 'swe-lancer':'https://openai.com/index/swe-lancer/',
 'swe-pro':'https://scale.com/blog/swe-bench-pro',
 'swe-noise':'https://openai.com/index/separating-signal-from-noise-coding-evaluations/',
 'swe-verified':'https://openai.com/index/introducing-swe-bench-verified/',
 'yicai':'https://www.yicai.com/news/102481945.html',
 'caixin':'https://companies.caixin.com/2025-12-18/102394533.html',
 'technode':'https://technode.com/2026/07/07/tencent-launches-hunyuan-hy3-integrates-model-across-multiple-products/',
 'claude-launch':'https://www.anthropic.com/news/claude-4',
 'codex-launch':'https://openai.com/index/introducing-codex/',
 'deepseek-issue':'https://api.github.com/repos/deepseek-ai/DeepSeek-V3/issues/994',
 'gemini-launch':'https://blog.google/products/gemini/gemini-2-5-model-family-expands/',
 'seed-launch':'https://seed.bytedance.com/en/seed_model_portfolio',
}
def fetch(item):
 key,url=item
 p=ROOT/key
 if p.with_suffix('.json').exists():
  previous=json.loads(p.with_suffix('.json').read_text(encoding='utf-8'))
  if 'error' not in previous: return previous
  if not p.with_suffix('.failed-network.json').exists(): p.with_suffix('.failed-network.json').write_text(json.dumps(previous,ensure_ascii=False,indent=2),encoding='utf-8')
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 ResearchToolkit source reading'}),timeout=70) as r: raw=r.read(); content_type=r.headers.get('Content-Type','')
  p.with_suffix('.original').write_bytes(raw)
  if raw.startswith(b'%PDF'):
   txt='\n'.join(f'[PAGE {i+1}]\n'+(page.extract_text() or '') for i,page in enumerate(PdfReader(io.BytesIO(raw)).pages))
  elif 'html' in content_type:
   doc=html.fromstring(raw)
   for node in doc.xpath('//script|//style|//nav|//footer'): node.drop_tree()
   article=doc.xpath('//article')
   txt=(article[0] if article else doc).text_content()
  else: txt=raw.decode('utf-8')
  txt='\n'.join(x.strip() for x in txt.splitlines() if x.strip())
  p.with_suffix('.txt').write_text(txt,encoding='utf-8',newline='\n')
  record={'id':key,'url':url,'sha256':hashlib.sha256(raw).hexdigest(),'text_sha256':hashlib.sha256(txt.encode()).hexdigest(),'characters':len(txt),'access_date':'2026-10-13'}
 except Exception as e: record={'id':key,'url':url,'error':str(e)}
 p.with_suffix('.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(record,ensure_ascii=False),flush=True)
 return record
if __name__=='__main__':
 ROOT.mkdir(parents=True,exist_ok=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: list(pool.map(fetch,SOURCES.items()))
