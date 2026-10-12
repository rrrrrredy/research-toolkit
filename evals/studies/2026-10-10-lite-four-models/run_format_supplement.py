"""Post-hoc exact JSON-fence diagnostic; original first attempts remain unchanged."""
from pathlib import Path
import argparse,hashlib,json,re
import run_live_study as live
W=Path(__file__).parent;h=live.h

def parse_original(folder):
 execution=h.read(folder/'execution.json')
 if execution['status']!='response_complete':return None
 raw=h.read(folder/'response.json')['choices'][0]['message']['content']
 stripped=raw.strip();transform='none'
 try:value=json.loads(stripped)
 except ValueError:
  match=re.fullmatch(r'```(?:json)?\s*\n([\s\S]*)\n```',stripped,re.IGNORECASE)
  if not match:return None
  try:value=json.loads(match.group(1))
  except ValueError:return None
  transform='single_enclosing_markdown_code_fence_removed'
 if not isinstance(value,dict) or not isinstance(value.get('report'),str) or not value['report'].strip() or not isinstance(value.get('notes'),str):return None
 return value,{'source_response_sha256':h.sha((folder/'response.json').read_bytes()),'transformation':transform,'report_sha256':h.sha(value['report'].encode()),'notes_sha256':h.sha(value['notes'].encode())}

def run(provider):
 primary=W/'runs'/provider
 h.require((primary/'judgments.lock.json').exists(),'Primary first attempts must lock before supplementary analysis')
 config=h.read(primary/'coordinator/frozen.json');rows={r['pair_id']:r for r in h.read(primary/'results.json')['results']}
 output=W/'format-supplement'/provider;output.mkdir(parents=True,exist_ok=False)
 h.save(output/'analysis-started.json',{'policy_sha256':h.sha((W/'format-supplement-policy.json').read_bytes()),'primary_results_sha256':h.sha((primary/'results.json').read_bytes()),'primary_judgments_lock_sha256':h.sha((primary/'judgments.lock.json').read_bytes()),'analysis_type':'post_hoc_exact_json_fence_only','author_calls':0})
 judgments={}
 for task in config['assignments']:
  pair=task['pair_id']
  if rows[pair]['status']=='judged':judgments[pair]={'status':'not_eligible_already_judged'};continue
  values={};provenance={}
  for arm in ('with_toolkit','without_toolkit'):
   result=parse_original(primary/'coordinator/author'/pair/arm)
   if result:values[arm],provenance[arm]=result
  if len(values)!=2 or not any(v['transformation']!='none' for v in provenance.values()):judgments[pair]={'status':'not_eligible_incomplete_or_unrepairable'};continue
  h.save(output/'derivations'/f'{pair}.json',provenance)
  packet={'brief':task['brief'],'sources':task['sources'],'rubric':config['rubric'],'reports':{label:values[arm]['report'] for label,arm in task['labels'].items()}}
  h.save(output/'judge-inputs'/f'{pair}.json',packet)
  content=live.judge_call(config['config']['judge'],[{'role':'system','content':h.JUDGE_SYSTEM},{'role':'user','content':json.dumps(packet,ensure_ascii=False)}],output/'judgments'/pair)
  if content is None:judgments[pair]={'status':'unresolved_supplementary_judge_failure'};continue
  try:
   value=h.validate_judgment(json.loads(content));h.save(output/'judgments'/pair/'parsed.json',value);judgments[pair]={'status':'judged','value':value}
  except (ValueError,KeyError,TypeError) as e:
   h.save(output/'judgments'/pair/'invalid.json',{'error':str(e)});judgments[pair]={'status':'unresolved_invalid_supplementary_judgment'}
 lock={p.relative_to(output).as_posix():h.sha(p.read_bytes()) for p in sorted((output/'judgments').rglob('*')) if p.is_file()} if (output/'judgments').exists() else {}
 h.save(output/'judgments.lock.json',{'status':'supplementary_first_attempts_locked','sha256':lock})
 results=[]
 for task in config['assignments']:
  item=judgments[task['pair_id']];preference=item.get('value',{}).get('preference','unresolved')
  results.append({'pair_id':task['pair_id'],'task_id':task['task_id'],'status':item['status'],'preference':preference,'outcome':task['labels'].get(preference,preference)})
 h.save(output/'results.json',{'scope':'Post-hoc envelope compatibility only; not prespecified primary','n_original_families':5,'results':results,'general_quality_advantage_established':False})
 h.save(output/'bundle-manifest.json',{'sha256':{p.relative_to(output).as_posix():h.sha(p.read_bytes()) for p in sorted(output.rglob('*')) if p.is_file()}})
 print(json.dumps({'supplement':provider,'results':results}),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--provider',choices=live.PROVIDERS,required=True);a=p.parse_args();run(a.provider)