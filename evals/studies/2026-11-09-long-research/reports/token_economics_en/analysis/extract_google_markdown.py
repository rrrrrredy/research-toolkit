"""Extract published noscript Markdown from acquired Google documentation, preserving raw bytes."""
from pathlib import Path
import re,html,json
B=Path(__file__).resolve().parent/'supplemental-sources'
for sid in ['TE-S03','TE-S04','TE-S19']:
 d=B/sid;p=d/('original.md' if (d/'original.md').exists() else 'original.html')
 raw=p.read_text(encoding='utf-8')
 blocks=re.findall(r'<pre[^>]*>(.*?)</pre>',raw,re.S)
 content='\n\n'.join(html.unescape(x) for x in blocks)
 (d/'readable-markdown.txt').write_text(content,encoding='utf-8')
 print(json.dumps({'id':sid,'source':str(p),'blocks':len(blocks),'characters':len(content)}))
