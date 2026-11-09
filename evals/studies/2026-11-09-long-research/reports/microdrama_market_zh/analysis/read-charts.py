from pathlib import Path
from urllib.request import urlopen,Request
from urllib.error import HTTPError,URLError
import re,json,pypdfium2
p=Path(__file__).resolve().parent
s=(p/'sources/CP16/original.html').read_text(encoding='utf-8');rows=[]
for key in ['时长增量高度','基于抖音','但短剧应用','短剧视频行业']:
 url=re.search(r'https://ws.questmobile.cn/report/article/images/[a-f0-9]+\.png',s[s.find(key):]).group()
 folder=p/'sources/CP16/charts';folder.mkdir(exist_ok=True);f=folder/url.split('/')[-1]
 row={'section':key,'url':url,'file':str(f)}
 try:
  f.write_bytes(urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0','Referer':'https://www.questmobile.com.cn/'}),timeout=30).read());row['status']='retrieved'
 except (HTTPError,URLError) as e:row['status']=str(e)
 rows.append(row)
(folder/'chart-map.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(rows,ensure_ascii=False))
pdf=pypdfium2.PdfDocument(p/'sources/CP17/original.pdf')
for num in [6,9,11,18,19]:
 out=p/'sources/CP17/pages';out.mkdir(exist_ok=True)
 pdf[num-1].render(scale=1.5).to_pil().save(out/f'p-{num}.png')
folder=p/'sources/CP24/charts';folder.mkdir(exist_ok=True,parents=True)
for name,url in [('users','https://oss.adquan.com/uploads_img/1785232294054e6522f6b18156.jpg'),('time','https://oss.adquan.com/uploads_img/1785232294b47744a51bc342ec.jpg'),('apps','https://oss.adquan.com/uploads_img/1785232294eef8aed0eb19e34d.jpg')]:
 (folder/f'{name}.jpg').write_bytes(urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0','Referer':'https://m.adquan.com/'}),timeout=30).read())
