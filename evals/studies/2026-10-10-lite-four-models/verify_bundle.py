"""Verify retained study data without making model calls."""
from pathlib import Path
import argparse,hashlib,json,re
from audit_helpers import require

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def check_results(base, assignments):
 """Bind retained outcomes to the frozen labels and original judge preferences."""
 tasks={task['pair_id']:task for task in assignments}
 rows=read(base/'results.json')['results']
 require(len(rows)==len(tasks) and {r['pair_id'] for r in rows}==set(tasks), f'{base}: result pairs differ from frozen assignments')
 for row in rows:
  task=tasks[row['pair_id']]
  where=f"{base}/results.json {row['pair_id']}"
  require(row['task_id']==task['task_id'], f'{where}: task_id differs')
  if row['status']=='judged':
   parsed=read(base/'judgments'/row['pair_id']/'parsed.json')
   preference=parsed['preference']
   require(preference in ('A','B','tie'), f'{where}: invalid judge preference')
   require(row['preference']==preference, f'{where}: preference differs from original judgment')
   require(row['outcome']==task['labels'].get(preference,preference), f'{where}: outcome differs from frozen labels')
  else:
   require(row['outcome']=='unresolved', f'{where}: unjudged pair cannot count as a win or tie')

def check_primary(root):
 plan=read(root/'study-plan.json');require(plan['families']==5, "Failed check: plan['families'] == 5")
 require(sha(root/'run_live_study.py')==plan['driver_sha256'], "Failed check: sha(root / 'run_live_study.py') == plan['driver_sha256']")
 require(sha(root/'inputs/source-manifest.json')==plan['source_manifest_sha256'], "Failed check: sha(root / 'inputs/source-manifest.json') == plan['source_manifest_sha256']")
 require(sha(root/'inputs/judge.schema.json')==plan['judge_schema_sha256'], "Failed check: sha(root / 'inputs/judge.schema.json') == plan['judge_schema_sha256']")
 for src in read(root/'inputs/source-manifest.json'):require(sha(root/'inputs'/src['file'])==src['sha256'], "Failed check: sha(root / 'inputs' / src['file']) == src['sha256']")
 total_authors=total_judges=0;seen_families=set();counts={}
 for provider in ('deepseek','glm','kimi','longcat'):
  study=root/'runs'/provider;frozen=read(study/'coordinator/frozen.json');commitment=read(study/'coordinator/freeze-commitment.json')
  encoded=json.dumps(frozen,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
  require(hashlib.sha256(encoded).hexdigest()==commitment['frozen_sha256']==plan['strata_freeze_sha256'][provider], "Failed check: hashlib.sha256(encoded).hexdigest() == commitment['frozen_sha256'] == plan['strata_freeze_sha256'][provider]")
  require(len(frozen['assignments'])==5, "Failed check: len(frozen['assignments']) == 5")
  require(sha(root/'harness-snapshot.py')==frozen['harness_sha256'], "Failed check: sha(root / 'harness-snapshot.py') == frozen['harness_sha256']")
  for name,digest in frozen['method_sha256'].items():require(hashlib.sha256(frozen['methods'][name].encode()).hexdigest()==digest, "Failed check: hashlib.sha256(frozen['methods'][name].encode()).hexdigest() == digest")
  for p in study.rglob('bundle-manifest.json'):
   for rel,digest in read(p)['sha256'].items():require(sha(p.parent/rel)==digest, (provider,rel))
  for rel,digest in read(study/'judgments.lock.json')['sha256'].items():require(sha(study/rel)==digest, 'Failed check: sha(study / rel) == digest')
  for task in frozen['assignments']:
   seen_families.add(task['family_id']);requests=[];reports={}
   for arm in ('with_toolkit','without_toolkit'):
    f=study/'coordinator/author'/task['pair_id']/arm
    body=read(f/'request.json');record=read(f/'execution.json');requests.append(body);total_authors+=1
    require(body['model']==frozen['config']['author']['model'], "Failed check: body['model'] == frozen['config']['author']['model']")
    require(body['max_tokens']==frozen['config']['author']['max_completion_tokens'], "Failed check: body['max_tokens'] == frozen['config']['author']['max_completion_tokens']")
    require(body['messages'][1]=={'role':'user','content':json.dumps({'brief':task['brief'],'sources':task['sources']},ensure_ascii=False)}, "Failed check: body['messages'][1] == {'role': 'user', 'content': json.dumps({'brief': task['brief'], 'sources': task['sources']}, ensure_ascii=False)}")
    if (f/'parsed.json').exists():reports[arm]=read(f/'parsed.json')['report']
   require(requests[0]['messages'][1]==requests[1]['messages'][1], "Failed check: requests[0]['messages'][1] == requests[1]['messages'][1]")
   require({k:v for k,v in requests[0].items() if k!='messages'}=={k:v for k,v in requests[1].items() if k!='messages'}, "Failed check: {k: v for k, v in requests[0].items() if k != 'messages'} == {k: v for k, v in requests[1].items() if k != 'messages'}")
   for base in (study,root/'format-supplement'/provider):
    packet=base/'judge-inputs'/f"{task['pair_id']}.json"
    if not packet.exists():continue
    d=read(packet)
    require(set(d)=={'brief','sources','rubric','reports'}, "Failed check: set(d) == {'brief', 'sources', 'rubric', 'reports'}")
    require(d['brief']==task['brief'] and d['sources']==task['sources'] and d['rubric']==frozen['rubric'], "Failed check: d['brief'] == task['brief'] and d['sources'] == task['sources'] and (d['rubric'] == frozen['rubric'])")
    for label,arm in task['labels'].items():
     original=study/'coordinator/author'/task['pair_id']/arm
     response=read(original/'response.json')['choices'][0]['message']['content'].strip()
     if response.startswith('```'):
      match=re.fullmatch(r'```(?:json)?\s*\n([\s\S]*)\n```',response,re.I);require(match, 'Failed check: match');response=match.group(1)
     require(d['reports'][label]==json.loads(response)['report'], "Failed check: d['reports'][label] == json.loads(response)['report']")
    jr=base/'judgments'/task['pair_id'];request=read(jr/'request.json')
    require(request['messages'][1]['content']==json.dumps(d,ensure_ascii=False), "Failed check: request['messages'][1]['content'] == json.dumps(d, ensure_ascii=False)")
    require(read(jr/'execution.json').get('tools_observed',0)==0, "Failed check: read(jr / 'execution.json').get('tools_observed', 0) == 0")
    total_judges+=1
  check_results(study,frozen['assignments'])
  results=read(study/'results.json');require(results['n_admitted']==5 and len(results['results'])==5, "Failed check: results['n_admitted'] == 5 and len(results['results']) == 5")
  counts[provider]={k:sum(r['outcome']==k for r in results['results']) for k in ['with_toolkit','without_toolkit','tie','unresolved']}
  supp=root/'format-supplement'/provider
  if supp.exists():
   check_results(supp,frozen['assignments'])
   for rel,digest in read(supp/'bundle-manifest.json')['sha256'].items():require(sha(supp/rel)==digest, 'Failed check: sha(supp / rel) == digest')
   started=read(supp/'analysis-started.json')
   require(started['policy_sha256']==sha(root/'format-supplement-policy.json'), "Failed check: started['policy_sha256'] == sha(root / 'format-supplement-policy.json')")
   require(started['primary_results_sha256']==sha(study/'results.json'), "Failed check: started['primary_results_sha256'] == sha(study / 'results.json')")
   require(started['primary_judgments_lock_sha256']==sha(study/'judgments.lock.json'), "Failed check: started['primary_judgments_lock_sha256'] == sha(study / 'judgments.lock.json')")
   primary_rows={r['pair_id']:r for r in results['results']}
   for row in read(supp/'results.json')['results']:
    if row['status'].startswith('not_eligible'):continue
    require(primary_rows[row['pair_id']]['status']!='judged', "Failed check: primary_rows[row['pair_id']]['status'] != 'judged'")
    derivation=read(supp/'derivations'/f"{row['pair_id']}.json")
    for arm,evidence in derivation.items():
     original=study/'coordinator/author'/row['pair_id']/arm
     require(read(original/'execution.json')['status']=='response_complete', "Failed check: read(original / 'execution.json')['status'] == 'response_complete'")
     require(evidence['source_response_sha256']==sha(original/'response.json'), "Failed check: evidence['source_response_sha256'] == sha(original / 'response.json')")
 require(len(seen_families)==5 and total_authors==40 and total_judges<=20, 'Failed check: len(seen_families) == 5 and total_authors == 40 and (total_judges <= 20)')
 return {'families':5,'author_requests':total_authors,'judge_requests':total_judges,'primary_outcomes':counts}

def check(root):
 import summarize_completion
 primary=check_primary(root)
 summarize_completion.audit(root,check_primary=False)
 return {'status':'verified','scope':'primary, format supplement and completion supplement',**primary,
         'completion_author_requests':20,'completion_judge_requests':10}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).parent);a=p.parse_args()
 try:
  print(json.dumps(check(a.root.resolve()),ensure_ascii=False))
 except (OSError,ValueError,KeyError,TypeError,IndexError) as exc:
  print(json.dumps({'status':'invalid','error':str(exc)},ensure_ascii=False))
  raise SystemExit(1)
