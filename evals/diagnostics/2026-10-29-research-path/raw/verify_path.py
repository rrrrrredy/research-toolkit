"""One controlled CLI integration path; synthetic inputs, no research/model rerun."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[1] / 'research-toolkit'
WORKSPACE = BASE / 'tasks'
CALLS = BASE / 'calls'
CALLS.mkdir(parents=True, exist_ok=True)
if (WORKSPACE / 'handoff').exists():
    raise SystemExit('Preserve prior runs: choose a separate output directory before rerunning.')
env = dict(os.environ, PYTHONIOENCODING='utf-8')
for key in list(env):
    if key.startswith('RESEARCH_TOOLKIT_REVIEW'):
        env.pop(key)
calls = []
def call(action, request, success=True):
    n = len(calls) + 1
    path = CALLS / f'{n:02}-{action}.request.json'
    path.write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding='utf-8')
    command = [sys.executable, '-B', str(REPO / 'scripts/research_workflow.py'), action,
               '--workspace', str(WORKSPACE), '--request', str(path)]
    began = time.monotonic()
    run = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', env=env)
    result = json.loads(run.stdout)
    (CALLS / f'{n:02}-{action}.response.json').write_text(run.stdout, encoding='utf-8')
    calls.append({'command': command, 'elapsed_seconds': round(time.monotonic()-began, 6),
                  'returncode': run.returncode, 'stderr': run.stderr})
    (BASE / 'execution.json').write_text(json.dumps(calls, indent=2), encoding='utf-8')
    assert (run.returncode == 0) == success, result
    return result

brief = dict(question='Compare two cooling retrofit options for a warehouse.', audience='Operations manager',
             scope='Synthetic integration fixture: two options; preserve reliability conditions.',
             output='English decision memo', depth='Explain cost and reliability trade-offs',
             evidence_standard='Use supplied inputs; do not turn a pilot into a population estimate.')
call('start', {'task':'handoff', 'brief':brief})
root = WORKSPACE / 'handoff'
(root / 'sources').mkdir()
(root / 'sources/a.md').write_text('Synthetic fixture. A costs 100 units; pilot saves 20 units annually. Pilot excludes peak-load days.\n', encoding='utf-8')
(root / 'sources/b.md').write_text('Synthetic fixture. B costs 140 units; pilot saves 28 units annually and includes peak-load days.\n', encoding='utf-8')
call('save', {'task':'handoff', 'sources':[
    dict(source_id='S1',title='A pilot',url='sources/a.md',source_type='primary',read_scope='full_text',read_evidence='sources/a.md'),
    dict(source_id='S2',title='B pilot',url='sources/b.md',source_type='primary',read_scope='full_text',read_evidence='sources/b.md')],
    'requirements':[dict(requirement_id='R1', summary='Retain peak-load limitations in every revision.', status='satisfied', evidence='Initial memo preserves this condition.', source_turn='fixture-1', quote='Keep the pilot limitations.'),
                    dict(requirement_id='R2', summary='Compare total cost and reliability.',status='pending')],
    'claims':[dict(claim_id='C1',claim='Both simple paybacks are five years; reliability coverage differs.',claim_type='analysis',supporting_sources=['S1'],counter_evidence='S2',uncertainty='Pilots have different operating conditions.')],
    'draft':dict(path='report.md',content='# Retrofit decision\n\nA and B have different pilot coverage. Peak-load reliability remains important.\n',main=True)})
work = dict(question='Explain comparable payback and reliability conditions.',claim_ids=['C1'],requirement_ids=['R2'])
prepared = call('status', {'task':'handoff','work':work,'methods':['compare']})
context = prepared['work_context']
assert any(r['requirement_id']=='R1' for r in context['effective_requirements'])
assert {s['source_id'] for s in context['sources']} == {'S1','S2'}
assert all(p in context['files'] for p in ('sources/a.md','sources/b.md'))
assert 'Compare:' in prepared['guidance'][0]['content']
assert 'Explain:' not in prepared['guidance'][0]['content']
call('status', {'task':'handoff','work':{'paths':['sources/missing.md']}}, success=False)
out = call('save', {'task':'handoff','draft':dict(path='analysis/cost.md',kind='analysis',
    content='Synthetic analyst result: 100/20 and 140/28 both give five years. The evidence does not establish equal reliability: A excludes peak load. Keep this condition when choosing.\n',
    based_on=context['inputs'],host_task='fixture-host:cost-branch')})
assert out['current_work']['artifact']['path']=='report.md'
assert out['current_work']['research_outputs'][0]['host_task']=='fixture-host:cost-branch'
assert not out['current_work']['research_outputs'][0]['changed_inputs']
call('save', {'task':'handoff','requirements':[dict(requirement_id='R2',summary='Compare cost and reliability; peak-load continuity is now decisive.',source_turn='fixture-2',quote='Prioritize peak-load continuity.') ]})
resumed = call('status', {'task':'handoff'})
assert 'state/requirements.jsonl' in resumed['current_work']['research_outputs'][0]['changed_inputs']
assert any(r['requirement_id']=='R1' for r in resumed['current_work']['effective_requirements'])
new = call('status', {'task':'handoff','work':{**work,'paths':['analysis/cost.md']},'methods':['assemble']})
assert 'analysis/cost.md' in new['work_context']['files']
final = '# Warehouse cooling retrofit\n\nBoth pilots imply a five-year simple payback (100/20 and 140/28). That equality does not establish equal operating reliability: the A pilot excludes peak-load days, while B includes them. With peak-load continuity now decisive, B has the more relevant operating evidence. Confirm site fit before commitment; neither pilot establishes a general failure rate.\n\nSources: [A pilot](sources/a.md), [B pilot](sources/b.md).\n'
call('save', {'task':'handoff','requirements':[dict(requirement_id='R2',status='satisfied',evidence='report.md compares payback and preserves peak-load coverage.')], 'draft':dict(path='report.md',content=final,main=True,complete=True)})
review = call('review', {'task':'handoff','evidence_paths':['sources/a.md','sources/b.md'], 'artifact':'report.md','reviewer':'self'})
assert 'R1' in review['assignment']['requirements'] and 'peak-load continuity' in review['assignment']['requirements']
answer = dict(input_version=review['input_version'],report_verdict='pass',findings=[],coverage={d:dict(location='report.md paragraph 1',basis='Synthetic interface exercise: both ratios, operating conditions, new priority and references are present. No model quality assessment.') for d in review['assignment']['dimensions']})
call('review', {'task':'handoff','evidence_paths':['sources/a.md','sources/b.md'],'artifact':'report.md','reviewer':'self','self_review':answer})
call('finish', {'task':'handoff','artifact':'report.md','message':'Synthetic integration memo; no measured research quality or time-saving claim.'})
(BASE / 'result.json').write_text(json.dumps({'ok':True,'nature':'Controlled CLI integration, supplied analyst prose and self-review; no model or host execution', 'operations':len(calls),'elapsed_seconds':sum(c['elapsed_seconds'] for c in calls),'observed':['effective satisfied constraints retained','counter-evidence included','selected methods only','missing input rejected','branch output and host reference recovered','changed requirements visible on handoff','full report reaches existing review and delivery']},indent=2),encoding='utf-8')
print((BASE / 'result.json').read_text())
