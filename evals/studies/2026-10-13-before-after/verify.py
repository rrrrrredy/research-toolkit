"""Verify archived bytes, real-response extraction, report bindings and descriptive arithmetic.

This makes zero model calls and does not judge research quality.
"""
import hashlib, json, statistics
from pathlib import Path
BASE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def digest(b):return hashlib.sha256(b).hexdigest()
def require(ok,message):
 if not ok:raise ValueError(message)
def score(report):
 values=list(report['scores'].values())
 return 5*sum(values) if all(type(v) is int for v in values) else None
def verify():
 manifest=read(BASE/'manifest.json')['files']
 actual={p.relative_to(BASE).as_posix() for p in BASE.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
 require(actual==set(manifest),'Published inventory changed')
 for path,expected in manifest.items():require(digest((BASE/path).read_bytes())==expected,'Changed bytes: '+path)
 protocol=read(BASE/'protocol.json');summary=read(BASE/'initial-summary.json');calls=read(BASE/'calls.json')
 require(len(protocol['tasks'])==len(summary['rows'])==10,'Expected ten distinct task identities')
 require(len({t['id'] for t in protocol['tasks']})==10,'Repeated task identities')
 require(len(calls)==summary['execution']['calls']==82,'Original study has 62 author-stage and 20 review calls')
 usage={k:0 for k in summary['execution']['usage']}
 for call in calls:
  path=BASE/call['slot'];events=[json.loads(line) for line in (path/'events.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
  replies=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
  completed=[e for e in events if e.get('type')=='turn.completed']
  require(len(replies)==len(completed)==1,'Missing/unexpected model return: '+call['slot'])
  require(completed[0]['usage']==call['execution']['usage'],'Usage mismatch')
  require(call['execution']['status']=='response_complete','Unresolved original call')
  for k in usage:usage[k]+=completed[0]['usage'].get(k,0)
  task=next(t for t in protocol['tasks'] if t['id'] in path.parts)
  require(call['task_sha256']==task['exact_full_task_sha256'],'Changed author/reviewer task/source binding')
  if call['slot'].startswith('reviews/'):
   require(set(call['packet_fields'])=={'task','reports','measurements'},'Unexpected blind-review packet field')
   require(json.loads(replies[0])==read(path/'parsed.json'),'Extracted review differs from original response')
   mapping=protocol['primary_A_condition'][task['id']]
   if path.name=='swap':mapping='after' if mapping=='before' else 'before'
   for alias,c in [('A',mapping),('B','after' if mapping=='before' else 'before')]:
    report=(BASE/'authors'/task['id']/c/'report.md').read_bytes()
    require(digest(report)==call['report_bindings'][alias],'Blind review did not receive exact report')
    require(sum(not x.isspace() for x in report.decode())==call['measurements'][alias]['characters'],'Wrong supplied length')
 require(usage==summary['execution']['usage'],'Usage totals differ')
 for row in summary['rows']:
  key=row['task'];a=protocol['primary_A_condition'][key]
  primary=read(BASE/'reviews'/key/'primary/parsed.json');swap=read(BASE/'reviews'/key/'swap/parsed.json')
  for alias,c in [('A',a),('B','after' if a=='before' else 'before')]:
   text=(BASE/'authors'/key/c/'report.md').read_bytes();record=read(BASE/'authors'/key/c/'report-record.json')
   require(digest(text)==record['sha256']==row['reports'][c]['sha256'],'Report hash mismatch')
   units=[]
   task=next(t for t in protocol['tasks'] if t['id']==key)
   for n in range(1,task['parts']+1):
    events=[json.loads(x) for x in (BASE/'authors'/key/c/f'unit-{n}'/'events.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
    raw=next(e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message')
    units.append(json.loads(raw)['report_unit'].strip())
   require(('\n\n'.join(units)+'\n').encode()==text,'Unrecorded edit before initial review')
   require(score(primary['reports'][alias])==row['reports'][c]['score'],'Primary score differs')
   require(primary['reports'][alias]['verdict']==row['reports'][c]['verdict'],'Primary verdict differs')
   require(score(swap['reports']['B' if alias=='A' else 'A'])==row['reports'][c]['swap_score'],'Swap score differs')
  require(row['delta']==row['reports']['after']['score']-row['reports']['before']['score'],'Paired delta differs')
 require(statistics.mean(r['delta'] for r in summary['rows'])==summary['all']['mean_delta'],'Mean paired delta differs')
 repair=read(BASE/'repair-summary.json');repair_calls=read(BASE/'repairs/calls.json')
 require(len(repair_calls)==repair['calls']==5 and repair['total_study_and_repair_calls']==87,'Repair call accounting changed')
 for call in repair_calls:
  folder=BASE/call['slot'];events=[json.loads(x) for x in (folder/'events.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
  replies=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
  complete=[e for e in events if e.get('type')=='turn.completed']
  require(len(replies)==len(complete)==1 and json.loads(replies[0])==read(folder/'parsed.json'),'Changed repair response')
  require(complete[0]['usage']==call['execution']['usage'],'Changed repair usage')
 for row in repair['selected_reports']:
  text=(BASE/row['report']).read_bytes();report=text.decode();review=read(BASE/row['review'])
  selected=review['reports']['A'] if row['task'].startswith('reasoning') else review
  require(digest(text)==row['sha256'] and sum(not x.isspace() for x in report)==row['characters'],'Changed selected repair')
  require(selected['verdict']=='pass' and not selected['findings'] and 'cite' not in report,'Unresolved selected report')
  slot=str(Path(row['review']).parent).replace('\\','/')
  call=next(c for c in repair_calls if c['slot']==slot)
  bound=call.get('report_sha256') or call['report_bindings']['A']
  require(bound==row['sha256'],'Repair review covers another version')
 require(read(BASE/'repairs/reasoning_model_competition_zh/report-record.json')['characters']==4557,'Overlength repair draft lost')
 require(read(BASE/'repairs/coding_benchmark_decision_zh/review/parsed.json')['reports']['B']['verdict']=='needs_revision','Negative targeted review lost')
 return {'tasks':10,'initial_reports':20,'author_stage_calls':62,'initial_blind_review_calls':20,'repair_calls':5,'selected_repairs_passed':2,'total_model_calls':87,'model_calls_during_verification':0}
if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
