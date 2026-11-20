"""Compare public statements about new reviews with the implemented contract (Python 3.11+)."""
import argparse
import ast
import json
from pathlib import Path
import re
import tomllib

from host_review import DIMENSIONS, REVIEW_GROUPS
from research_workflow import CURRENT_REVIEW_CONTRACT

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = ('README', 'SKILL', 'agents/README', 'docs/research-guide')
MARKER = re.compile(r'(<!-- current-review -->).*?(<!-- /current-review -->)')
STALE = re.compile(r'\bseven (?:distinct )?independent (?:agents?|contexts?|reviewers?)\b|七位独立(?:的)?(?:\s*Agent|评审)|七个独立(?:的)?(?:上下文|审阅者)|Show the finished report for my acceptance|把成稿交给我验收|等待(?:人工|用户)验收', re.I)


def check(write=False):
    claims = tomllib.loads((ROOT/'docs/claims.toml').read_text(encoding='utf-8'))
    tools = [n.name for n in ast.parse((ROOT/'scripts/research_mcp.py').read_text(encoding='utf-8')).body
             if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith('research_')]
    flattened = [name for group in REVIEW_GROUPS.values() for name in group]
    actual = (CURRENT_REVIEW_CONTRACT, len(REVIEW_GROUPS), len(DIMENSIONS), len(tools))
    if tuple(claims[k] for k in ('review_contract','review_groups','perspectives','tools')) != actual or sorted(flattened) != sorted(DIMENSIONS):
        raise ValueError('Published figures differ from the runtime review groups or MCP registry')
    if claims['entries'] != ['Skill','Plugin','MCP','CLI']:
        raise ValueError('Entry inventory differs from the documented interfaces')
    reports = json.loads((ROOT/'evals/studies/2026-11-09-long-research/delivered-report-index.json').read_bytes())
    if (len({r["family_id"] for r in reports}), len(reports)) != (claims['long_questions'], claims['long_reports']):
        raise ValueError('Published long-research counts differ from the report index')
    for workflow in (ROOT/'.github/workflows').glob('*.yml'):
        for action in re.findall(r'(?m)^\s*(?:-\s+)?uses:\s*([^#\s]+)', workflow.read_text(encoding='utf-8')):
            if not action.startswith('./') and not re.fullmatch(r'[^@]+@[a-f0-9]{40}', action):
                raise ValueError('Unpinned workflow action: '+action)
    for stem in ENTRIES:
        for lang, suffix in [('en',''),('zh','.zh-CN')]:
            path = ROOT/(stem+suffix+'.md')
            old = path.read_text(encoding='utf-8')
            new, count = MARKER.subn(lambda m: m[1]+claims[lang]+m[2], old)
            if count != 1: raise ValueError('Expected one current review rule in '+str(path))
            if old != new:
                if not write: raise ValueError('Stale current review rule in '+str(path))
                path.write_text(new, encoding='utf-8', newline='\n')
    paths = [*ROOT.glob('README*.md'), *ROOT.glob('SKILL*.md'), *(ROOT/'agents').glob('*.md'),
             *(ROOT/'references').glob('*.md'), *(ROOT/'docs').glob('*.md'), *(ROOT/'docs').glob('*.html'),
             ROOT/'docs/llms.txt', *(ROOT/'plugins/research-toolkit/docs').glob('*.md')]
    errors = []
    for path in paths:
        for i, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            if STALE.search(line):
                errors.append(f'{path.relative_to(ROOT)}:{i}: obsolete public instruction')
            # Only claims about newly created tasks have the current contract. Saved v2 plans remain valid evidence.
            for match in re.finditer(r'(?:new (?:full.report )?tasks?|current tasks?|当前任务|新建全稿|新全稿任务)[^.;。\n]{0,70}?(?:progress\.)?review_contract\s*:\s*(\d+)', line, re.I):
                if int(match[1]) != CURRENT_REVIEW_CONTRACT: errors.append(f'{path.relative_to(ROOT)}:{i}: wrong new-task contract')
    if errors: raise ValueError('\n'.join(errors))
    print(f'Current publication rules match contract {actual[0]}, {actual[1]} groups, {actual[2]} perspectives and {actual[3]} tools.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    check(parser.parse_args().write)
