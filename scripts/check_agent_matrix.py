"""Render both language views of the maintained host inventory. Python 3.11+ for TOML."""
import argparse
from pathlib import Path
import re
import tomllib

from agent_session import HOSTS

ROOT = Path(__file__).resolve().parents[1]
WORDS = {'documented': ('Documented', '有接入说明'), 'exercised': ('Run recorded', '有运行记录'),
         'packaged': ('Packaged', '有插件包'), 'opt_in': ('Opt-in', '可选开启'),
         'unverified': ('—', '—'), 'released': ('Released', '已发布'),
         'preview': ('Preview', '预览'), 'experimental': ('Experimental', '实验')}


def cards(hosts, zh):
    lang, suffix = ('zh', '.zh-CN') if zh else ('en', '')
    setup = ['| 客户端 | 首次任务入口 | 指南 |' if zh else '| Client | First-task route | Guide |', '| --- | --- | --- |']
    title = '宿主能力' if zh else 'Host capabilities'
    intro = ('这张表列出本项目有依据的接入方式。横线表示此项未在 Toolkit 登记。宿主可以自行派原生子 Agent。内置执行器还可以按空位排队，处理审计、改稿和最终复查。'
             if zh else 'The table lists routes with evidence for this project. A dash means this combination has no Toolkit evidence recorded. Hosts can dispatch their own subagents. A bundled driver can also queue work, revise and complete final checks.')
    matrix = ['<a id="capabilities"></a>', '', '### '+title, '', intro, '',
              '| 客户端 | 指南状态 | 插件 | 本地 MCP | 宿主子 Agent | Toolkit 自动派工 | 使用记录 hooks | 依据 |' if zh else
              '| Client | Guide status | Plugin | Local MCP | Host subagents | Toolkit driver | Usage hooks | Evidence |', '| --- | --- | --- | --- | --- | --- | --- | --- |']
    edits = {}
    for key, host in hosts.items():
        name = host['name_'+lang]
        route = host['install_'+lang]
        label = host['guide_'+lang]
        setup.append(f'| {name} | {route} | [{label}]({key}{suffix}.md) |')
        evidence = '../'+host['evidence']
        values = {k: WORDS[host[k]][int(zh)] for k in ('plugin','mcp','native_subagents','hooks')}
        if host.get('mcp_source'):
            values['mcp'] = '['+values['mcp']+']('+host['mcp_source']+')'
        driver = host['driver'] or '—'
        proof = '记录' if zh else 'Record'
        matrix.append(f"| {name} | {WORDS[host['status']][int(zh)]} | {values['plugin']} | {values['mcp']} | {values['native_subagents']} | {driver} | {values['hooks']} | [{proof}]({evidence}) |")
        card = (f'**接入**　{route}。' if zh else f'**Entry**　{route}. ')
        if host['driver']:
            card += (f' 自动派工支持 `{driver}`。' if zh else f' Bundled dispatch driver: `{driver}`. ')
        card += f' [ {title} ](README{suffix}.md#capabilities)'.replace('[ ', '[').replace(' ]', ']')
        edits[f'{key}{suffix}.md'] = card
    edits[f'README{suffix}.md'] = '\n'.join(setup+['']+matrix)
    return edits


def check(write=False):
    data = tomllib.loads((ROOT/'integrations/capabilities.toml').read_text(encoding='utf-8'))
    hosts = data['hosts']
    if data['schema_version'] != 1 or {v['driver'] for v in hosts.values() if v['driver']} != set(HOSTS):
        raise ValueError('Host inventory does not match the bundled drivers')
    for zh in (False, True):
        wanted = {p.name for p in (ROOT/'agents').glob('*.md') if ('.zh-CN.' in p.name) == zh}
        entries = cards(hosts, zh)
        if set(entries) != wanted:
            raise ValueError('Host guide inventory differs: '+str(set(entries)^wanted))
        for name, body in entries.items():
            path = ROOT/'agents'/name
            source = path.read_text(encoding='utf-8')
            new, count = re.subn(r'<!-- hosts:start -->.*?<!-- hosts:end -->',
                                 lambda _: '<!-- hosts:start -->\n'+body+'\n<!-- hosts:end -->', source, flags=re.S)
            if count != 1: raise ValueError('Expected one host view in '+name)
            if new != source:
                if not write: raise ValueError('Stale host view in '+name+'; use --write')
                path.write_text(new, encoding='utf-8', newline='\n')
    for name, host in hosts.items():
        if host['status'] not in ('released', 'experimental', 'preview') or not host['evidence'] or not (ROOT/host['evidence']).is_file():
            raise ValueError('Missing status or evidence for '+name)
        if host['mcp'] == 'documented' and not host.get('mcp_source','').startswith('https://'):
            raise ValueError('Missing MCP source for '+name)
    print(f'Verified {len(hosts)} paired host guides, both matrices and {len(HOSTS)} bundled drivers.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    check(parser.parse_args().write)
