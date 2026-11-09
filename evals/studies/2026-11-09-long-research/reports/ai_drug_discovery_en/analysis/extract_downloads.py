from acquire_sources import B,f
import json,re
from pypdf import PdfReader
for d in sorted((B/'supplemental-sources').iterdir()):
 p=d/'download.bin'
 if not p.exists() or (d/'original.txt').exists():continue
 m=json.loads((d/'retrieval.json').read_text(encoding='utf-8-sig'))
 if m['status']!='retrieved':continue
 raw=p.read_bytes()
 if raw.startswith(b'%PDF'):
  (d/'original.pdf').write_bytes(raw)
  pages=[{'page':i+1,'text':p.extract_text() or ''} for i,p in enumerate(PdfReader(d/'original.pdf').pages)]
  (d/'pages.json').write_text(json.dumps(pages,indent=2,ensure_ascii=False),encoding='utf-8')
  text='\n\n'.join('## Page '+str(p['page'])+'\n'+p['text'] for p in pages)
 elif raw.lstrip().startswith(b'{'):text=raw.decode('utf-8-sig')
 else:
  (d/'original.html').write_bytes(raw)
  text=f.extract_html(raw,source_url=m['url'],accessed_at=m['accessed_at'])['text']
 (d/'original.txt').write_text(text,encoding='utf-8');print(d.name,len(text))
for d in sorted((B/'supplemental-sources').iterdir()):
 p=d/'original.txt'
 if not p.exists() or d.name.startswith('AIDD-R'):continue
 clean='\n'.join(f'{i+1}: '+re.sub(r'\[href: [^\]]+\]','',x) for i,x in enumerate(p.read_text(encoding='utf-8-sig').splitlines()))
 (d/'reading-lines.txt').write_text(clean,encoding='utf-8')
