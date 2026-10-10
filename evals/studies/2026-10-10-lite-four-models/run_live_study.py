"""Native-Codex judge adapter for one declared local study; no stored secrets."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,os,shutil,subprocess,sys,time,urllib.request,urllib.error
W=Path(__file__).parent
ROOT=Path(os.environ.get('RESEARCH_TOOLKIT_ROOT',str(W.parent/'rt-pilot'))).resolve()
spec=importlib.util.spec_from_file_location('blinded',ROOT/'scripts/run_blinded_evals.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
PROVIDERS={
 'deepseek':('https://api.deepseek.com','deepseek-flash','DEEPSEEK_API_KEY'),
 'kimi':('https://api.moonshot.cn/v1','kimi-k2.6','KIMI_API_KEY'),
 'glm':('https://open.bigmodel.cn/api/paas/v4','glm-5.3','GLM_API_KEY'),
 'longcat':('https://api.longcat.chat/openai/v1','LongCat-2.5-Preview','LONGCAT_API_KEY')}
EXTRA={'glm':{'reasoning_effort':'low'}}

def scrub(s):
 for key in ('DEEPSEEK_API_KEY','KIMI_API_KEY','GLM_API_KEY','LONGCAT_API_KEY'):
  value=os.environ.get(key)
  if value:s=s.replace(value,'[REDACTED]')
 return s

def dump(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('x',encoding='utf-8') as f:f.write(scrub(json.dumps(obj,ensure_ascii=False,indent=2))+'\n')

def author_call(provider,settings,messages,folder):
 body={'model':settings['model'],'messages':messages,'stream':False,'max_tokens':settings['max_completion_tokens'],**EXTRA.get(provider,{})}
 dump(folder/'request.json',body)
 started=time.monotonic();record={'status':'failed','transport':'chat_completions','model_requested':settings['model']};content=None
 key=os.environ[settings['api_key_env']]
 try:
  request=urllib.request.Request(h.endpoint(settings['base_url']),data=h.encode(body),headers={'Content-Type':'application/json','Authorization':'Bearer '+key},method='POST')
  with urllib.request.build_opener(h.NoRedirect).open(request,timeout=settings['timeout_seconds']) as r:raw=r.read(16*1024*1024+1)
  h.require(len(raw)<=16*1024*1024,'Response exceeds size ceiling')
  (folder/'response.json').write_text(scrub(raw.decode('utf-8')),encoding='utf-8')
  data=json.loads(raw);usage=data.get('usage',{});elapsed=time.monotonic()-started
  record.update(model_returned=data.get('model'),request_id=data.get('id'),usage=usage,elapsed_seconds=round(elapsed,3))
  h.require(data.get('model')==settings['model'],'Returned model differs from pinned model')
  h.require(h.positive_int(usage.get('total_tokens')) and usage['total_tokens']<=settings['max_total_tokens'],'Missing usage or total budget exceeded')
  h.require(h.positive_int(usage.get('completion_tokens')) and usage['completion_tokens']<=settings['max_completion_tokens'],'Missing completion usage or completion ceiling exceeded')
  h.require(elapsed<=settings['timeout_seconds'],'Request deadline exceeded')
  choice=data['choices'][0];h.require(choice['finish_reason']=='stop','Truncated/incomplete response retained')
  content=choice['message']['content'];h.require(isinstance(content,str) and content.strip(),'Empty response')
  record['status']='response_complete'
 except urllib.error.HTTPError as e:
  record['error']=f'HTTP {e.code}';(folder/'error-response.txt').write_text(scrub(e.read(1024*1024).decode('utf-8','replace')),encoding='utf-8')
 except Exception as e:record['error']=scrub(str(e))
 record.setdefault('elapsed_seconds',round(time.monotonic()-started,3));dump(folder/'execution.json',record)
 print(json.dumps({'provider':provider,'phase':'author','request':folder.relative_to(W).as_posix(),'status':record['status'],'error':record.get('error'),'seconds':record['elapsed_seconds']}),flush=True)
 return content if record['status']=='response_complete' else None

def judge_call(settings,messages,folder):
 folder.mkdir(parents=True,exist_ok=False)
 codex=os.environ.get('CODEX_BIN') or shutil.which('codex')
 if not codex:raise RuntimeError('Codex CLI is unavailable')
 isolated=W/'judge-empty';isolated.mkdir(exist_ok=True)
 args=['exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','--sandbox','read-only','--json','--model',settings['model'],'--cd',str(isolated),'-c','model_reasoning_effort="low"','-c','project_doc_max_bytes=0','-c','features.multi_agent=false','-c','web_search="disabled"','--output-schema',str(W/'inputs/judge.schema.json'),'-']
 # The recorded portable argv contains no machine paths or credentials.
 recorded=[str(x).replace(str(isolated),'<empty-directory>').replace(str(W/'inputs/judge.schema.json'),'inputs/judge.schema.json') for x in args]
 prompt='You are evaluating supplied research reports, not giving financial, legal, or operational advice. Work only from the supplied packet. Do not use tools, files, external sources, skills or memory. Return only the requested judgment JSON.\n\n'+messages[0]['content']+'\n\n'+messages[1]['content']
 dump(folder/'request.json',{'transport':'codex_exec','model_requested':settings['model'],'reasoning_effort':'low','messages':messages,'envelope':prompt[:prompt.index(messages[0]['content'])],'argv':recorded,'output_cap_enforcement':'post-response usage check; CLI has no configured hard completion cap'})
 env=os.environ.copy()
 for key in ('DEEPSEEK_API_KEY','KIMI_API_KEY','GLM_API_KEY','LONGCAT_API_KEY'):env.pop(key,None)
 started=time.monotonic();record={'status':'failed','transport':'codex_exec','model_requested':settings['model'],'model_returned':None,'model_identity_boundary':'CLI requested model only; response identity not independently attested'};content=None
 try:
  proc=subprocess.run([codex,*args],input=prompt,text=True,encoding='utf-8',errors='replace',capture_output=True,timeout=settings['timeout_seconds'],env=env)
  (folder/'response.jsonl').write_text(scrub(proc.stdout),encoding='utf-8')
  # Machine-specific diagnostics are retained in a private sidecar, outside the publishable study bundle.
  diag=W/'private-diagnostics'/folder.parent.parent.name/folder.name;diag.mkdir(parents=True,exist_ok=True)
  (diag/'stderr.txt').write_text(scrub(proc.stderr),encoding='utf-8')
  events=[json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
  usage_events=[e for e in events if e.get('type')=='turn.completed']
  messages_out=[e['item'].get('text','') for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
  tool_items=[e for e in events if e.get('type') in ('item.started','item.completed') and e.get('item',{}).get('type') not in ('agent_message','reasoning')]
  elapsed=time.monotonic()-started
  record.update(returncode=proc.returncode,elapsed_seconds=round(elapsed,3),tools_observed=len(tool_items))
  h.require(proc.returncode==0 and usage_events and messages_out,'Codex did not complete a judgment')
  usage=usage_events[-1]['usage'];record['usage']=usage
  h.require(not tool_items,'Judge used tools; masking isolation not established')
  h.require(usage['input_tokens']+usage['output_tokens']<=settings['max_total_tokens'],'Judge total-token ceiling exceeded')
  h.require(0<usage['output_tokens']<=settings['max_completion_tokens'],'Judge completion ceiling exceeded')
  h.require(elapsed<=settings['timeout_seconds'],'Judge deadline exceeded')
  content=messages_out[-1];h.validate_judgment(json.loads(content));record['status']='response_complete'
 except subprocess.TimeoutExpired as e:
  raw=e.stdout.decode('utf-8','replace') if isinstance(e.stdout,bytes) else e.stdout or ''
  (folder/'response.jsonl').write_text(scrub(raw),encoding='utf-8');record['error']='Codex judgment deadline exceeded; no retry'
 except Exception as e:record['error']=scrub(str(e))
 record.setdefault('elapsed_seconds',round(time.monotonic()-started,3));dump(folder/'execution.json',record)
 print(json.dumps({'phase':'judge','request':folder.relative_to(W).as_posix(),'status':record['status'],'error':record.get('error'),'seconds':record['elapsed_seconds']}),flush=True)
 return content if record['status']=='response_complete' else None

def freeze():
 tasks=json.loads((W/'inputs/tasks.json').read_text(encoding='utf-8'))
 # Fixed rubric output schema, used only by the native CLI judge to avoid markup envelopes.
 detail={'type':'object','properties':{'score':{'anyOf':[{'type':'integer','minimum':0,'maximum':4},{'type':'string','enum':['not_assessed']}]},'reason':{'type':'string'},'excerpt':{'type':'string'},'source_evidence':{'type':'string'}},'required':['score','reason','excerpt','source_evidence'],'additionalProperties':False}
 ratings={'type':'object','properties':{d:detail for d in h.DIMENSIONS},'required':list(h.DIMENSIONS),'additionalProperties':False}
 schema={'type':'object','properties':{'preference':{'type':'string','enum':['A','B','tie','unresolved']},'reason':{'type':'string'},'reports':{'type':'object','properties':{'A':ratings,'B':ratings},'required':['A','B'],'additionalProperties':False},'condition_clues':{'type':'string'}},'required':['preference','reason','reports','condition_clues'],'additionalProperties':False}
 dump(W/'inputs/judge.schema.json',schema)
 for i,(provider,(url,model,key)) in enumerate(PROVIDERS.items()):
  settings={'base_url':url,'model':model,'snapshot_statement':'Provider model alias and exact returned ID recorded, not immutable model weights. Same parameters in both arms. GLM Coding Plan availability probe failed because subscription expired; ordinary API selected before all GLM report runs.','api_key_env':key,'max_completion_tokens':12288,'max_total_tokens':98304,'timeout_seconds':240,'completion_parameter':'max_tokens'}
  config={'schema_version':1,'profile':'lite','source_access':'fixed_supplied_sources','cohort_status':'prospective_development','publication_rights_confirmed':True,'selection_statement':'Five purposively selected distinct decision families; 3 original English and 2 original Chinese briefs, fixed before generation. Full admitted government text units, hypothetical organizational decisions; not a random population sample. No exclusions or retries after observing outputs. Four separate same-model strata share these five families; n remains 5, not 20 independent tasks.','exposure_statement':'New task phrasing written for this prospective development pilot. Public sources may occur in model training. No held-out or unseen claim. Prior diagnostic and calibration results are unchanged.','author':settings,'judge':{'base_url':'http://127.0.0.1','model':'gpt-6-astra','snapshot_statement':'Native Codex CLI fresh ephemeral contexts; requested gpt-6-astra at low effort. This role is a declared adapter extension, not an HTTP endpoint. Returned model is not independently attested. Reported CLI token usage and tool events retained; host context remains a limitation.','api_key_env':'UNUSED_NATIVE_CODEX_AUTH','max_completion_tokens':8192,'max_total_tokens':98304,'timeout_seconds':240,'completion_parameter':'max_tokens'},'tasks':tasks}
  path=W/'inputs'/f'{provider}.json';dump(path,config)
  h.prepare(path,W/'runs'/provider,20261010+i)
 protocol={'study_id':'2026-10-10-four-model-fixed-source-lite','frozen_before_report_generation':True,'families':5,'author_calls_planned':40,'judge_calls_maximum':20,'judge':'Codex CLI requested gpt-6-astra, low effort; model identity not independently attested','same_model_pairs':True,'primary_outcome':'first blinded judge preference by model; ties and all failures preserved','scope':'fixed supplied sources; instruction-only Lite; one author response, no workflow execution or open-web search','common_judge':'same requested judge model and settings across all four author strata; independent context per pair','no_retries':True,'max_concurrent_provider_strata':2,'extra_author_parameters':EXTRA,'cli_boundary':'Fresh, read-only empty working directory; user config ignored; project docs disabled; no tools permitted; fail if tools observed. Native host base context and skill metadata may remain. Output cap checked after response, not a hard CLI cap.','driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'source_manifest_sha256':hashlib.sha256((W/'inputs/source-manifest.json').read_bytes()).hexdigest(),'judge_schema_sha256':hashlib.sha256((W/'inputs/judge.schema.json').read_bytes()).hexdigest(),'strata_freeze_sha256':{p:json.loads((W/'runs'/p/'coordinator/freeze-commitment.json').read_text())['frozen_sha256'] for p in PROVIDERS}}
 dump(W/'study-plan.json',protocol);print(json.dumps(protocol),flush=True)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('action',choices=['freeze','run']);parser.add_argument('--provider',choices=PROVIDERS);args=parser.parse_args()
 if args.action=='freeze':freeze()
 else:
  p=args.provider
  assert p,'Specify provider'
  plan=json.loads((W/'study-plan.json').read_text());assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==plan['driver_sha256'],'Driver changed after freeze'
  rows=h.run(W/'runs'/p,call=lambda settings,messages,folder:judge_call(settings,messages,folder) if settings['model']=='gpt-6-astra' else author_call(p,settings,messages,folder))
  print(json.dumps({'provider':p,'pairs':len(rows),'judged':sum(r['status']=='judged' for r in rows),'outcomes':rows}),flush=True)