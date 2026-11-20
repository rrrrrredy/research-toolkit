"""Publish readable Markdown for each custom HTML page and the Agent indexes."""
from __future__ import annotations

from html import unescape
from pathlib import PurePosixPath
import re
from urllib.parse import urljoin

RAW = 'https://raw.githubusercontent.com/rrrrrredy/research-toolkit/main/'
CORE = ('SKILL.md', 'SKILL.zh-CN.md', 'docs/quickstart.md', 'docs/quickstart.zh-CN.md',
        'docs/research-guide.md', 'docs/research-guide.zh-CN.md',
        'references/research-standard.md', 'references/research-standard.zh-CN.md',
        'references/research-workflow.md', 'references/research-workflow.zh-CN.md',
        'references/subagents-and-review-loop.md', 'references/subagents-and-review-loop.zh-CN.md',
        'docs/review-completion.md', 'docs/review-completion.zh-CN.md')


def markdown_path(page):
    return 'markdown/' + str(PurePosixPath(page).with_suffix('.md'))


def page_markdown(tree, page_url):
    """Read the published main content, including source links, tables and code."""
    def render(node):
        if isinstance(node, str):
            if node.startswith('<!--'):
                return ''
            return re.sub(r'\s+', ' ', unescape(node))
        tag, attrs = node.tag, node.attrs
        if tag in ('script', 'style', 'button', 'nav', 'noscript') or 'hidden' in attrs or attrs.get('aria-hidden') == 'true':
            return ''
        if tag == 'pre':
            def verbatim(item):
                return unescape(item) if isinstance(item, str) else ''.join(verbatim(child) for child in item.children)
            code = verbatim(node).strip('\n')
            fence = '`' * max(3, 1 + max((len(x) for x in re.findall(r'`+', code)), default=0))
            return f'\n\n{fence}\n{code}\n{fence}\n\n'
        if tag == 'table':
            def rows(item):
                if isinstance(item, str):
                    return
                if item.tag == 'tr':
                    yield [render(cell).strip().replace('|', r'\|').replace('\n', ' ') for cell in item.children
                           if not isinstance(cell, str) and cell.tag in ('td', 'th')]
                else:
                    for child in item.children:
                        yield from rows(child)
            values = [row for row in rows(node) if row]
            if not values:
                return ''
            width = max(map(len, values))
            values.insert(1, ['---'] * width)
            return '\n\n' + '\n'.join('| ' + ' | '.join(row + [''] * (width-len(row))) + ' |' for row in values) + '\n\n'
        body = ''.join(render(child) for child in node.children)
        clean = body.strip()
        if tag == 'a' and attrs.get('href') and clean:
            return '[' + clean + '](' + urljoin(page_url, attrs['href']).replace(' ', '%20') + ')'
        if re.fullmatch('h[1-6]', tag):
            return '\n\n' + '#' * int(tag[1]) + ' ' + clean + '\n\n'
        if tag == 'br':
            return ' '
        if tag == 'code':
            return '`' + clean + '`'
        if tag in ('b', 'strong') and clean:
            return '**' + clean + '**'
        if tag == 'blockquote':
            return '\n\n' + '\n'.join('> ' + line for line in clean.splitlines()) + '\n\n'
        if tag == 'li':
            return '\n- ' + clean + '\n'
        if tag in ('summary', 'dt'):
            return '\n\n**' + clean + '**\n\n' if clean else ''
        if tag in ('p', 'dd', 'section', 'article', 'ul', 'ol', 'div', 'details', 'figcaption', 'aside'):
            return '\n\n' + clean + '\n\n' if clean else ''
        return body
    main = next(n for n in tree.nodes if n.tag == 'main')
    body = render(main)
    body = re.sub(r'(?m)^[ \t]+$', '', body)
    return re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+', '\n\n', body).strip() + '\n'


def indexes(root, base, pages, descriptions):
    template = (root / 'scripts/site/llms-intro.txt').read_text(encoding='utf-8').rstrip()
    links = [f'- [{descriptions[page]}]({base}{markdown_path(page)})' for page in sorted(pages)]
    docs = root / "docs"
    guide_paths = sorted({*docs.glob("*.md"), *(docs/"en").rglob("*.md"), *(docs/"zh").rglob("*.md")},
                         key=lambda path: path.relative_to(docs).as_posix())
    guides = []
    for path in guide_paths:
        first_heading = next((line[2:].strip() for line in path.read_text(encoding="utf-8-sig").splitlines() if line.startswith("# ")), path.stem)
        guides.append(f"- [{first_heading}]({base}{path.relative_to(docs).as_posix()})")
    sections = [template, "## Documentation Markdown", "\n".join(guides)]
    for directory, title in (("references", "Research methods"), ("agents", "Agent host guides")):
        paths = sorted((root / directory).glob("*.md"), key=lambda path: path.name)
        entries = [f"- [{path.stem}]({RAW}{directory}/{path.name})" for path in paths]
        sections.extend(["## " + title, "\n".join(entries)])
    sections.extend(["## Page Markdown", "\n".join(links)])
    index = "\n\n".join(sections) + "\n"
    chunks = ['# Research Toolkit · Agent handbook\n\n'
              f'Core instructions, installation, research methods and review. [All pages]({base}llms.txt).']
    for name in CORE:
        text = (root / name).read_text(encoding='utf-8').strip()
        # Relative links in the merged handbook still refer to their own source file.
        text = re.sub(r'(\]\()([^\s)]+)(\))', lambda m: m[1] + urljoin(RAW + name, m[2]) + m[3], text)
        chunks.append(f'[Source]({RAW}{name})\n\n' + text)
    full = '\n\n---\n\n'.join(chunks) + '\n'
    if len(full.encode('utf-8')) > 300_000:
        raise ValueError('Core Agent handbook exceeds 300 KB. Select complete core documents and keep other pages in llms.txt.')
    return {'llms.txt': index, 'llms-full.txt': full}
