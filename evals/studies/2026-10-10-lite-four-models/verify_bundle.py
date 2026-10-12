"""Verify retained study data without making model calls."""
from pathlib import Path
import argparse,hashlib,json,re

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def check(root):
 plan=read(root/'study-plan.json');assert plan['families']==5
 assert sha(root/'run_live_study.py')==plan['driver_sha256']
 assert sha(root/'inputs/source-manifest.json')==plan['source_manifest_sha256']
 assert sha(root/'inputs/judge.schema.json')==plan['judge_schema_sha256']
 for src in read(root/'inputs/source-manifest.json'):assert sha(root/'inputs'/src['file'])==src['sha256']
 total_authors=total_judges=0;seen_families=set();counts={}
 for provider in ('deepseek','glm','kimi','longcat'):
  study=root/'runs'/provider;frozen=read(study/'coordinator/frozen.json');commitment=read(study/'coordinator/freeze-commitment.json')
  encoded=json.dumps(frozen,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
  assert hashlib.sha256(encoded).hexdigest()==commitment['frozen_sha256']==plan['strata_freeze_sha256'][provider]
  assert len(frozen['assignments'])==5
  assert sha(root/'harness-snapshot.py')==frozen['harness_sha256']
  for name,digest in frozen['method_sha256'].items():assert hashlib.sha256(frozen['methods'][name].encode()).hexdigest()==digest
  for p in study.rglob('bundle-manifest.json'):
   for rel,digest in read(p)['sha256'].items():assert sha(p.parent/rel)==digest,(provider,rel)
  for rel,digest in read(study/'judgments.lock.json')['sha256'].items():assert sha(study/rel)==digest
  for task in frozen['assignments']:
   seen_families.add(task['family_id']);requests=[];reports={}
   for arm in ('with_toolkit','without_toolkit'):
    f=study/'coordinator/author'/task['pair_id']/arm
    body=read(f/'request.json');record=read(f/'execution.json');requests.append(body);total_authors+=1
    assert body['model']==frozen['config']['author']['model']
    assert body['max_tokens']==frozen['config']['author']['max_completion_tokens']
    assert body['messages'][1]=={'role':'user','content':json.dumps({'brief':task['brief'],'sources':task['sources']},ensure_ascii=False)}
    if (f/'parsed.json').exists():reports[arm]=read(f/'parsed.json')['report']
   assert requests[0]['messages'][1]==requests[1]['messages'][1]
   assert {k:v for k,v in requests[0].items() if k!='messages'}=={k:v for k,v in requests[1].items() if k!='messages'}
   for base in (study,root/'format-supplement'/provider):
    packet=base/'judge-inputs'/f"{task['pair_id']}.json"
    if not packet.exists():continue
    d=read(packet)
    assert set(d)=={'brief','sources','rubric','reports'}
    assert d['brief']==task['brief'] and d['sources']==task['sources'] and d['rubric']==frozen['rubric']
    for label,arm in task['labels'].items():
     original=study/'coordinator/author'/task['pair_id']/arm
     response=read(original/'response.json')['choices'][0]['message']['content'].strip()
     if response.startswith('```'):
      match=re.fullmatch(r'```(?:json)?\s*\n([\s\S]*)\n```',response,re.I);assert match;response=match.group(1)
     assert d['reports'][label]==json.loads(response)['report']
    jr=base/'judgments'/task['pair_id'];request=read(jr/'request.json')
    assert request['messages'][1]['content']==json.dumps(d,ensure_ascii=False)
    assert read(jr/'execution.json').get('tools_observed',0)==0
    total_judges+=1
  results=read(study/'results.json');assert results['n_admitted']==5 and len(results['results'])==5
  counts[provider]={k:sum(r['outcome']==k for r in results['results']) for k in ['with_toolkit','without_toolkit','tie','unresolved']}
  supp=root/'format-supplement'/provider
  if supp.exists():
   for rel,digest in read(supp/'bundle-manifest.json')['sha256'].items():assert sha(supp/rel)==digest
   started=read(supp/'analysis-started.json')
   assert started['policy_sha256']==sha(root/'format-supplement-policy.json')
   assert started['primary_results_sha256']==sha(study/'results.json')
   assert started['primary_judgments_lock_sha256']==sha(study/'judgments.lock.json')
   primary_rows={r['pair_id']:r for r in results['results']}
   for row in read(supp/'results.json')['results']:
    if row['status'].startswith('not_eligible'):continue
    assert primary_rows[row['pair_id']]['status']!='judged'
    derivation=read(supp/'derivations'/f"{row['pair_id']}.json")
    for arm,evidence in derivation.items():
     original=study/'coordinator/author'/row['pair_id']/arm
     assert read(original/'execution.json')['status']=='response_complete'
     assert evidence['source_response_sha256']==sha(original/'response.json')
 assert len(seen_families)==5 and total_authors==40 and total_judges<=20
 print(json.dumps({'status':'verified','families':5,'author_requests':total_authors,'judge_requests':total_judges,'primary_outcomes':counts},ensure_ascii=False))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).parent);a=p.parse_args();check(a.root.resolve())