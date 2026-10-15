#!/usr/bin/env python3
"""Validate initial HTML, local links, language alternates and sitemap; optionally verify a deployed site."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import time
from urllib.parse import parse_qsl, unquote, urljoin, urlsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

from build_site import BASE, DESCRIPTIONS, DOCS, PAIRS, ROOT, url

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.lang=''; self.title=''; self.title_count=0; self.in_title=False; self.head=False
        self.descriptions=[]; self.canonicals=[]; self.alternates={}; self.robots=[]
        self.links=[]; self.ids=set(); self.visible=[]; self.hidden=0
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='html': self.lang=a.get('lang','')
        if tag=='head': self.head=True
        if tag=='title': self.in_title=True; self.title_count+=1
        if tag in ('script','style'): self.hidden+=1
        if a.get('id'): self.ids.add(a['id'])
        if self.head and tag=='meta':
            if a.get('name')=='description': self.descriptions.append(a.get('content',''))
            if a.get('name')=='robots': self.robots.append(a.get('content',''))
        if self.head and tag=='link':
            if a.get('rel')=='canonical': self.canonicals.append(a.get('href',''))
            if a.get('rel')=='alternate' and 'hreflang' in a:
                if a['hreflang'] in self.alternates: raise ValueError('Duplicate hreflang')
                self.alternates[a['hreflang']]=a.get('href','')
        if tag=='a' and a.get('href'): self.links.append(a['href'])
        if tag in ('script','img','source','video','link'):
            for attr in ('src','poster') if tag!='link' else ('href',):
                if a.get(attr): self.links.append(a[attr])
    def handle_endtag(self, tag):
        if tag=='head': self.head=False
        if tag=='title': self.in_title=False
        if tag in ('script','style'): self.hidden=max(0,self.hidden-1)
    def handle_data(self, text):
        if self.in_title: self.title+=text
        if not self.head and not self.hidden: self.visible.append(text)

def metadata_errors(path, page):
    errors=[]
    if page.title_count!=1 or not page.title.strip(): errors.append('missing or duplicate title')
    if len(page.descriptions)!=1 or page.descriptions[0]!=DESCRIPTIONS[path]: errors.append('missing, duplicate or inaccurate description')
    if page.canonicals != [url(path)]: errors.append('canonical must be the absolute clean page URL')
    expected_lang='zh-CN' if '.zh-CN.' in path or '/office-agents/' in path and not path.endswith('notes.en.html') else 'en'
    if page.lang!=expected_lang: errors.append('incorrect document language: '+page.lang)
    expected={}
    for en, zh in PAIRS:
        if path in (en,zh): expected={'en':url(en),'zh-CN':url(zh),'x-default':url(en)}
    if page.alternates != expected: errors.append('missing, unrelated or incorrect language alternates')
    if any('noindex' in x.lower() for x in page.robots): errors.append('unexpected noindex')
    if len(''.join(page.visible).strip())<100: errors.append('empty initial HTML body')
    return errors

def local_target(path, href):
    absolute=urlsplit(urljoin(BASE+path,href))
    if absolute.scheme not in ('http','https'): return None
    if absolute.netloc==urlsplit(BASE).netloc:
        if not absolute.path.startswith('/research-toolkit/'): return None
        relative=unquote(absolute.path[len('/research-toolkit/'):]); target=DOCS/relative
    elif absolute.netloc in ('github.com','raw.githubusercontent.com'):
        prefix='/rrrrrredy/research-toolkit/'+('blob/main/' if absolute.netloc=='github.com' else 'main/')
        if not absolute.path.startswith(prefix):
            prefix='/rrrrrredy/research-toolkit/tree/main/'
            if not absolute.path.startswith(prefix): return None
        target=ROOT/unquote(absolute.path[len(prefix):])
    else: return None
    if not target.resolve().is_relative_to(ROOT): raise ValueError('Link escapes repository: '+href)
    if target.is_dir():
        for index in ('index.html','README.md'):
            if (target/index).exists(): target=target/index; break
    return target,unquote(absolute.fragment)

def local_checks():
    errors=[]; pages={}; links=0
    actual={p.relative_to(DOCS).as_posix() for p in DOCS.rglob('*.html')}
    if actual!=set(DESCRIPTIONS): errors.append('HTML inventory differs from metadata manifest: '+str(actual^set(DESCRIPTIONS)))
    for path in sorted(actual):
        page=Page((DOCS/path).read_text(encoding='utf-8')); pages[path]=page
        if path in DESCRIPTIONS: errors.extend(path+': '+e for e in metadata_errors(path,page))
    for path,page in pages.items():
        for href in page.links:
            target=local_target(path,href)
            if not target: continue
            if any(k in dict(parse_qsl(urlsplit(href).query)) for k in ('lang','theme','case','detail','mode')): errors.append(path+': preference parameters in static link '+href)
            links+=1; file,fragment=target
            if not file.exists(): errors.append(path+': missing link '+href)
            elif file.suffix=='.html' and fragment:
                other=pages.get(file.relative_to(DOCS).as_posix())
                if other and fragment not in other.ids: errors.append(path+': missing fragment '+href)
        for lang,other_url in page.alternates.items():
            target=next((p for p in pages if url(p)==other_url),None)
            if target is None or pages[target].alternates!=page.alternates: errors.append(path+': non-reciprocal hreflang '+lang)
    tree=ET.parse(DOCS/'sitemap.xml'); locations=[n.text for n in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    if not locations or len(locations)!=len(set(locations)): errors.append('Empty or duplicate sitemap entries')
    for loc in locations:
        target=next((p for p in pages if url(p)==loc),None)
        if target is None or pages[target].canonicals!=[loc] or any('noindex' in x for x in pages[target].robots): errors.append('Noncanonical or unindexable sitemap URL: '+str(loc))
    if (DOCS/'robots.txt').exists(): errors.append('Project-subdirectory robots.txt does not control this origin')
    llms=(DOCS/'llms.txt').read_text(encoding='utf-8')
    for href in re.findall(r'\]\((https?://[^)]+)\)',llms):
        target=local_target('llms.txt',href)
        if target and not target[0].exists(): errors.append('llms.txt: missing '+href)
    for name in ('index.html','index.zh-CN.html'):
        source=(DOCS/name).read_text(encoding='utf-8')
        if 'coding-benchmark-update/' not in source: errors.append(name+': missing update case discovery link')
    if errors: raise ValueError('\n'.join(errors))
    print(f'PASS: {len(pages)} initial HTML pages, {links} local link/asset targets, reciprocal language links, {len(locations)} sitemap URLs and llms.txt.')

KEY_PAGES=['index.html','index.zh-CN.html','framework.html','framework.zh-CN.html','case-study/index.html','case-study/index.zh-CN.html','case-study/api-or-browser/report.html','case-study/report.en.html','case-study/report.zh-CN.html','case-study/coding-benchmark-update/index.html','case-study/coding-benchmark-update/index.zh-CN.html']

def fetch(address, github_token=None):
    headers={'User-Agent':'ResearchToolkit-SiteCheck/1.0'}
    if github_token and address=='https://api.github.com/repos/rrrrrredy/research-toolkit': headers['Authorization']='Bearer '+github_token
    with urlopen(Request(address,headers=headers),timeout=30) as response:
        if response.status!=200: raise ValueError(f'{address}: HTTP {response.status}')
        if response.geturl()!=address: raise ValueError(f'{address}: unexpected redirect to {response.geturl()}')
        return response.read().decode('utf-8')

def live_checks(base):
    base=base.rstrip('/')+'/'
    def check(path):
        address=base+(path[:-10] if path.endswith('index.html') else path)
        source=fetch(address)
        if path.endswith('.html'):
            errors=metadata_errors(path,Page(source))
            if errors: raise ValueError(address+': '+', '.join(errors))
        expected=(DOCS/path).read_text(encoding='utf-8').replace('\r\n','\n').rstrip()
        if source.replace('\r\n','\n').rstrip()!=expected: raise ValueError(address+': deployed content differs from checked-out revision')
        return address
    paths=KEY_PAGES+['sitemap.xml','llms.txt','assets/reading-preferences.js','assets/showcase.js','assets/showcase.css']
    with ThreadPoolExecutor(max_workers=4) as executor: checked=list(executor.map(check,paths))
    for path in ('','index.zh-CN.html','framework.html','framework.zh-CN.html'):
        # Parameters must not change the server's initial document or canonical.
        if fetch(base+path+'?lang=zh&theme=dark&case=writing&detail=review')!=fetch(base+path): raise ValueError('Parameter-dependent server HTML: '+path)
    print(f'PASS: deployed raw bytes and metadata for {len(checked)} resources plus legacy preference URLs at {base}')

def star_snapshot(output):
    endpoint='https://api.github.com/repos/rrrrrredy/research-toolkit'
    data=json.loads(fetch(endpoint,os.environ.get('GITHUB_TOKEN')))
    record={'observed_at':datetime.now(timezone.utc).isoformat(),'source':endpoint,'stars':data['stargazers_count'],'scope':'public repository total; no attribution to search, AI citations or website clicks'}
    Path(output).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Saved public star-count snapshot; search, AI citations and website clicks are not measured.')

def self_test():
    source=(DOCS/'index.html').read_text(encoding='utf-8')
    mutations=[source.replace('<title>','<title></title><template>',1),source.replace('rel="canonical"','rel="other"'),source.replace('hreflang="zh-CN"','hreflang="fr"'),source.replace('<html lang="en"','<html lang="zh-CN"'),source.replace(BASE,BASE+'?theme=dark',1)]
    for changed in mutations:
        if not metadata_errors('index.html',Page(changed)): raise ValueError('Mutation fixture was not detected')
    if local_target('framework.html','missing-page.html')[0].exists(): raise ValueError('Missing-link fixture unexpectedly exists')
    print('PASS: malformed title, canonical, language, hreflang and parameter fixtures rejected.')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true'); parser.add_argument('--live',action='store_true')
    parser.add_argument('--base-url',default=BASE); parser.add_argument('--attempts',type=int,default=1); parser.add_argument('--delay',type=int,default=15)
    parser.add_argument('--stars-output'); args=parser.parse_args()
    local_checks()
    if args.self_test: self_test()
    if args.live:
        for attempt in range(max(1,args.attempts)):
            try: live_checks(args.base_url); break
            except Exception as error:
                if attempt+1>=args.attempts: raise
                print(f'Deployment not ready ({attempt+1}/{args.attempts}): {error}'); time.sleep(args.delay)
    if args.stars_output: star_snapshot(args.stars_output)

if __name__=='__main__': main()
