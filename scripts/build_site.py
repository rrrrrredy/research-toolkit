#!/usr/bin/env python3
"""Build static discovery metadata, the Chinese homepage and sitemap (stdlib only).

English homepage + its existing i18n JSON remain the shared homepage source.
Generated files are committed because Pages deploys docs/ directly.
"""
from __future__ import annotations

import argparse
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import posixpath
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
BASE = 'https://rrrrrredy.github.io/research-toolkit/'
PAIRS = [
    ('index.html', 'index.zh-CN.html'),
    ('framework.html', 'framework.zh-CN.html'),
    ('case-study/report.en.html', 'case-study/report.zh-CN.html'),
    ('case-study/coding-benchmark-update/index.html', 'case-study/coding-benchmark-update/index.zh-CN.html'),
]
# These indexes contain different historical material, not translated equivalents.
# Do not manufacture hreflang pairs for unrelated research cases.
DESCRIPTIONS = {
    'index.html': 'Research methods and optional workflow tools for AI agents: investigate questions, revise existing reports, and trace conclusions to sources with Lite or Full.',
    'index.zh-CN.html': '面向 AI Agent 的研究方法与可选工作流工具：调研问题、修订已有报告，并通过 Lite 或 Full 工作流将判断关联到可追溯来源。',
    'framework.html': 'Research Toolkit methods for scoping a question, reading sources, developing analysis, reviewing revisions and delivering a traceable research report.',
    'framework.zh-CN.html': 'Research Toolkit 研究方法：界定问题、阅读来源、展开分析、评审修订，并交付判断明确、来源可追溯的研究报告。',
    'case-study/index.html': 'Research Toolkit case archive: API versus browser research, Chinese office agents, and source-linked updates to an existing coding-agent procurement report.',
    'case-study/index.zh-CN.html': 'Research Toolkit 案例档案：API 与浏览器、国内办公 Agent，以及已有编程智能体采购报告的来源核对与修订；保留原稿、评审及限制。',
    'case-study/report.en.html': 'English translation of the Chinese office-agent report, with information through September 9, 2026: file generation, existing work, permissions and handoffs.',
    'case-study/report.zh-CN.html': '国内办公 Agent 产品研究：比较文件生成、既有工作修改、权限与交接。信息截至 2026 年 9 月 9 日，基于公开资料，未安装实测。',
    'case-study/api-or-browser/index.html': 'An English research case comparing APIs, DOM automation and visual interaction, with an initial draft, primary sources, reviews and a migration-cost correction.',
    'case-study/api-or-browser/report.html': 'Choose an AI agent execution route by action coverage, verified completion, recovery, permissions and cost. Public-source analysis dated October 10, 2026.',
    'case-study/api-or-browser/initial.html': 'Preserved initial draft of the API-or-browser research case, before the review corrected its claim about retiring a working browser step.',
    'case-study/api-or-browser/brief.html': 'The audience, question, scope and constraints behind the API-or-browser research report for AI agent product and engineering teams.',
    'case-study/api-or-browser/sources.html': 'Primary sources and retained reading notes for the API-or-browser report: action coverage, completion, recovery, permissions and cost.',
    'case-study/api-or-browser/claims.html': 'Claim records, source support and evidence limits for the API-or-browser research case. These are research records, not measured performance results.',
    'case-study/api-or-browser/reviews.html': 'The initial review, accepted migration-cost correction and final article review for the API-or-browser research case.',
    'case-study/api-or-browser/reviews/01-draft-review.html': 'Preserved initial review of the API-or-browser draft, including the missing counterexample about migration and revalidation costs.',
    'case-study/api-or-browser/reviews/02-final-review.html': 'Preserved review of the revised API-or-browser report after the migration-cost correction. This is not a comparative performance experiment.',
    'case-study/office-agents/index.html': '国内办公 Agent 历史研究档案：完整初稿、定稿、来源、主张与评审记录。稿件修订不构成工具箱效果的对照实验。',
    'case-study/office-agents/brief.html': '国内办公 Agent 研究的任务简报、受众、问题、范围与约束；保留原研究语境。',
    'case-study/office-agents/claims.html': '国内办公 Agent 研究的主张记录、证据等级、反证与不确定性，供核查报告判断。',
    'case-study/office-agents/comparison.html': '国内办公 Agent 报告的历史稿件比较、修改理由及审阅取舍，保留具体段落和研究限制。',
    'case-study/office-agents/notes.en.html': 'English notes on historical revisions to the Chinese office-agent research report, preserving interpretation limits and links to the original evidence.',
    'case-study/office-agents/original.zh-CN.html': '国内办公 Agent 研究的历史初稿原文，保留修订前的判断与措辞，用于与定稿比较。',
    'case-study/office-agents/revised.zh-CN.html': '国内办公 Agent 研究的历史定稿原文与行号，信息截至 2026 年 9 月 9 日，供核对稿件差异。',
    'case-study/office-agents/reviews.html': '国内办公 Agent 研究的历史评审摘要与修订记录，保留不同评审阶段及其局限。',
    'case-study/office-agents/sources.html': '国内办公 Agent 研究的来源资料、阅读记录、报告用途与限制，可追溯到原始公开资料。',
    'case-study/coding-benchmark-update/index.html': 'How an existing coding-agent procurement report was updated: previous report, new source checks, concrete revisions and preserved review evidence, with limits.',
    'case-study/coding-benchmark-update/index.zh-CN.html': '一篇已有编程智能体采购报告如何更新：旧稿、新材料核对、具体正文修订与评审证据；保留真实摩擦和实验限制。',
}
TITLES = {
    'index.html': 'Research Toolkit · Research methods and tools for AI agents',
    'index.zh-CN.html': 'Research Toolkit · 面向 AI Agent 的研究工具箱',
    'framework.html': 'Research method · Research Toolkit',
    'framework.zh-CN.html': '研究方法 · Research Toolkit',
    'case-study/api-or-browser/initial.html': 'Initial API-or-browser draft · Research Toolkit',
}

def url(path):
    return BASE + (path[:-10] if path.endswith('index.html') else path)

def metadata(path, source):
    source = re.sub(r'\n?<!-- discovery:start -->.*?<!-- discovery:end -->\n?', '', source, flags=re.S)
    source = re.sub(r'<meta\b(?=[^>]*\bname=[\"\']description[\"\'])[^>]*>\s*', '', source, flags=re.I)
    title = TITLES.get(path, html.unescape(re.search(r'<title>(.*?)</title>', source, re.S)[1]))
    source = re.sub(r'<title>.*?</title>', '<title>'+html.escape(title)+'</title>', source, count=1, flags=re.S)
    description = DESCRIPTIONS[path]
    tags = ['<!-- discovery:start -->', '<meta name="description" content="'+html.escape(description, quote=True)+'"/>', '<link rel="canonical" href="'+url(path)+'"/>']
    for en, zh in PAIRS:
        if path in (en, zh):
            tags += ['<link rel="alternate" hreflang="'+lang+'" href="'+url(target)+'"/>' for lang, target in [('en',en),('zh-CN',zh),('x-default',en)]]
    tags.append('<!-- discovery:end -->')
    source = re.sub(r'(</title>)', lambda m: m[0]+'\n'+'\n'.join(tags)+'\n', source, count=1)
    # Existing OG cards must describe the same static document.
    def og(m):
        tag = m[0]; prop = re.search(r'property=[\"\']([^\"\']+)', tag)[1]
        value = {'og:title':title,'og:description':description,'og:url':url(path)}.get(prop)
        return re.sub(r'content=[\"\'][^\"\']*[\"\']', 'content="'+html.escape(value,quote=True)+'"', tag) if value else tag
    source = re.sub(r'<meta\b[^>]*property=[\"\']og:[^>]*>', og, source)
    def clean_link(match):
        tag=match[0]; href=html.unescape(re.search(r'href="([^"]+)"',tag)[1])
        target=urlsplit(urljoin(BASE+path,href))
        if not target.geturl().startswith(BASE): return tag
        params=dict(parse_qsl(target.query)); relative=target.path[len('/research-toolkit/'):]
        if relative.endswith('/') or not relative: relative+='index.html'
        for en,zh in PAIRS:
            if relative in (en,zh) and params.get('lang') in ('en','zh'): relative=zh if params['lang']=='zh' else en
        if 'data-home-link' in tag:
            page_lang=re.search(r'<html[^>]+lang="([^"]+)"',source)[1]
            relative='index.zh-CN.html' if page_lang.startswith('zh') else 'index.html'
        if not any(k in params for k in ('lang','theme','case','detail','mode')) and 'data-home-link' not in tag: return tag
        query=urlencode([(k,v) for k,v in parse_qsl(target.query) if k not in ('lang','theme','case','detail','mode')])
        new_path=posixpath.relpath(relative,posixpath.dirname(path) or '.')
        clean=urlunsplit(('', '', new_path, query, target.fragment))
        return re.sub(r'href="[^"]+"','href="'+html.escape(clean,quote=True)+'"',tag)
    return re.sub(r'<a\b[^>]*href="[^"]+"[^>]*>',clean_link,source)

VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
class Node:
    def __init__(self, tag='', attrs=()): self.tag, self.attrs, self.children = tag, dict(attrs), []
    def text(self, value): self.children = [html.escape(value)]
    def render(self):
        if not self.tag: return ''.join(c.render() if isinstance(c, Node) else c for c in self.children)
        attrs = ''.join(' '+k+('="'+html.escape(v, quote=True)+'"' if v is not None else '') for k,v in self.attrs.items())
        start = '<'+self.tag+attrs+'>'
        return start if self.tag in VOID else start+''.join(c.render() if isinstance(c,Node) else c for c in self.children)+'</'+self.tag+'>'
class Tree(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False); self.root=Node(); self.stack=[self.root]; self.nodes=[]; self.feed(source)
    def handle_starttag(self, tag, attrs):
        n=Node(tag,attrs); self.stack[-1].children.append(n); self.nodes.append(n)
        if tag not in VOID: self.stack.append(n)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag,attrs)
        if tag not in VOID: self.handle_endtag(tag)
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag == tag: self.stack=self.stack[:i]; break
    def handle_data(self, data): self.stack[-1].children.append(data)
    def handle_entityref(self, name): self.handle_data('&'+name+';')
    def handle_charref(self, name): self.handle_data('&#'+name+';')
    def handle_comment(self, data): self.handle_data('<!--'+data+'-->')
    def handle_decl(self, decl): self.handle_data('<!'+decl+'>')
    def by_id(self, value): return next(n for n in self.nodes if n.attrs.get('id') == value)

def chinese_home(source):
    tree=Tree(source); data=json.loads(''.join(tree.by_id('showcase-data').children)); words=data['i18n']['zh']; case=data['cases']; pair=case['pairs'][0]; text=pair['zh']
    links=dict(report='case-study/report.zh-CN.html', **{k:'case-study/office-agents/'+f+'.html' for k,f in [('archive','index'),('brief','brief'),('sources','sources'),('claims','claims'),('reviews','reviews')]})
    for n in tree.nodes:
        a=n.attrs
        if n.tag=='html': a['lang']='zh-CN'
        if a.get('data-i18n') in words: n.text(words[a['data-i18n']])
        if 'data-home-link' in a: a['href']='index.zh-CN.html'
        if 'data-nav-aria' in a: a['aria-label']=words['navAria']
        if 'data-report-link' in a: a['href']=links['report']
        if 'data-case-link' in a: a['href']=links[a['data-case-link']]
        if 'data-method-link' in a: a['href']='framework.zh-CN.html'
        if 'data-update-case' in a: a['href']='case-study/coding-benchmark-update/index.zh-CN.html'
        if 'data-review-home' in a: a['href']='https://github.com/rrrrrredy/research-review/blob/main/README.zh-CN.md'
        if 'data-corpus-page' in a:
            fragment=urlsplit(a['href']).fragment
            a['href']='https://github.com/rrrrrredy/agent-trajectory-data/blob/main/corpora/ai-industry/'+a['data-corpus-page']+'.zh-CN.md'+('#'+fragment if fragment else '')
        if n.tag=='a' and 'data-language' in a:
            a.pop('aria-current',None)
            if a['data-language']=='zh': a['aria-current']='page'
        for attr, filename in [('data-quickstart-link','quickstart-full'),('data-lite-link','quickstart-lite'),('data-eval-link','evaluation-status')]:
            if attr in a: a['href']='https://github.com/rrrrrredy/research-toolkit/blob/main/docs/'+filename+'.zh-CN.md'
        if 'data-continue-link' in a: a['href']='https://github.com/rrrrrredy/research-toolkit/blob/main/docs/usage-modes.zh-CN.md#接续已有研究'
        if 'data-usage-link' in a: a['href']='https://github.com/rrrrrredy/research-toolkit/blob/main/docs/usage-modes.zh-CN.md'+('#单独接入-mcp' if a.get('data-i18n')=='mcpLink' else '#安装插件')
        if 'data-agent-link' in a or a.get('data-i18n') in ('skillLink','fallbackGuide'):
            anchor={'textLink':'只能在聊天中使用时','skillLink':'安装后重复使用','fallbackGuide':'选择工具'}.get(a.get('data-i18n'),'直接读取使用')
            a['href']='https://github.com/rrrrrredy/research-toolkit/blob/main/agents/README.zh-CN.md#'+anchor
        if n.tag=='time': a['datetime']=case['information_cutoff']
        if n.tag=='video': a['poster']='assets/readme-preview.zh-CN.png'
        if n.tag=='source': a['src']='assets/case-walkthrough.zh-CN.mp4'
        if a.get('property')=='og:image': a['content']=BASE+'assets/readme-preview.zh-CN.png'
        if a.get('class')=='case-choices js-only':
            a['aria-label']=words['topicsAria']
            n.children=[''.join('<button aria-controls="case-content" aria-selected="'+str(i==0).lower()+'" data-case="'+str(i)+'" id="topic-'+p['id']+'" role="tab" tabindex="'+('0' if i==0 else '-1')+'" type="button">'+html.escape(p['zh']['label'])+'</button>' for i,p in enumerate(case['pairs']))]
        if a.get('class')=='language-switch': a['aria-label']='语言'
        if 'case-detail-tabs' in a.get('class',''): a['aria-label']=words['detailAria']
        if a.get('role')=='tab' and a.get('data-detail'):
            n.text(words[{'diff':'detailDiff','reason':'detailReason','review':'detailReview'}[a['data-detail']]])
    tree.by_id('research-prompt').text(data['prompts']['zh'])
    tree.by_id('hero-quote').text(case['hero']['zh']['quote'])
    for ident,key in [('case-context','context'),('case-title','title'),('case-why','why')]: tree.by_id(ident).text(text.get(key,''))
    tree.by_id('evidence-source').text(words['sourcesLabel']+' ↗')
    tree.by_id('report-window').attrs['data-topic-count']=str(len(case['pairs']))
    tree.by_id('case-content').attrs.update({'aria-labelledby':'topic-'+pair['id'],'role':'tabpanel'})
    parts=[]
    for side,label,target in [('before','initial','original_url'),('after','final','revised_url')]:
        parts.append('<article class="excerpt'+(' revised' if side=='after' else '')+'"><h4 class="excerpt-label">'+html.escape(words[label])+'<span>'+html.escape(words['summaryLabel'])+'</span></h4><blockquote class="excerpt-copy">'+html.escape(text[side])+'</blockquote><p class="excerpt-note">'+html.escape(text[side+'_note'])+'</p><a data-preserve-reading href="'+pair[target]+'">'+html.escape(words['passage'])+' ↗</a></article>')
    parts.append('<div class="case-difference"><h4>'+html.escape(words['changeHeading'])+'</h4><dl class="case-change-list">'+''.join('<dt>'+html.escape(c['label'])+'</dt><dd>'+html.escape(c['text'])+'</dd>' for c in text['changes'])+'</dl></div>')
    tree.by_id('case-panel').children=parts
    return metadata('index.zh-CN.html',tree.root.render())

def outputs():
    result={}
    for path in sorted(DESCRIPTIONS):
        if path=='index.zh-CN.html': continue
        result[path]=metadata(path,(DOCS/path).read_text(encoding='utf-8'))
    result['index.zh-CN.html']=chinese_home(result['index.html'])
    # Curated useful entry points; raw evidence and intermediate drafts stay accessible.
    entries=[p for p in DESCRIPTIONS if p.startswith(('index.','framework.')) or p.endswith(('index.html','index.zh-CN.html')) or p in ('case-study/report.en.html','case-study/report.zh-CN.html','case-study/api-or-browser/report.html')]
    root=ET.Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for p in sorted(entries): ET.SubElement(ET.SubElement(root,'url'),'loc').text=url(p)
    ET.indent(root)
    result['sitemap.xml']='<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(root,encoding='unicode')+'\n'
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--check',action='store_true'); args=parser.parse_args()
    stale=[]
    for path,content in outputs().items():
        target=DOCS/path
        if not target.exists() or target.read_text(encoding='utf-8') != content:
            stale.append(path)
            if not args.check: target.write_text(content,encoding='utf-8',newline='\n')
    if args.check and stale: raise SystemExit('Stale generated site files; run python scripts/build_site.py: '+', '.join(stale))
    print('Static site build '+('verified' if args.check else 'written')+' (no framework or third-party build dependencies).')

if __name__=='__main__': main()
