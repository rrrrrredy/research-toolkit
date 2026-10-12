"""Derive tables from retained first attempts; no model calls or raw-data edits."""
from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parent
PROVIDERS=('deepseek','kimi','glm','longcat')
DIMENSIONS=('task_fidelity','facts_and_evidence','explanation_and_synthesis','counterevidence_and_boundaries','reader_usefulness')
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def derive():
 summary={'scope':'Five shared development families, four same-model strata; no general efficacy claim','primary':{},'format_supplement':{},'authors':{},'judges':{}}
 scores=[];usage_rows=[]
 for provider in PROVIDERS:
  primary=ROOT/'runs'/provider;frozen=read(primary/'coordinator/frozen.json');assignments={x['pair_id']:x for x in frozen['assignments']}
  for analysis,base in [('primary',primary),('format_supplement',ROOT/'format-supplement'/provider)]:
   result=read(base/'results.json');rows=result['results'];judged=[x for x in rows if x['status']=='judged']
   summary[analysis][provider]={'families':5,'judged':len(judged),**{k:sum(x['outcome']==k for x in judged) for k in ['with_toolkit','without_toolkit','tie','unresolved']},'unresolved_attempts':sum(x['status'].startswith('unresolved') for x in rows),'not_eligible':sum(x['status'].startswith('not_eligible') for x in rows)}
   for row in rows:
    task=assignments[row['pair_id']];jp=base/'judgments'/row['pair_id']/'parsed.json';judgment=read(jp) if jp.exists() else None
    for label,arm in task['labels'].items():
     item={'analysis':analysis,'provider':provider,'pair_id':row['pair_id'],'task_id':row['task_id'],'language':task['language'],'condition':arm,'presentation':label,'status':row['status'],'outcome':row['outcome']}
     for dimension in DIMENSIONS:item[dimension]=judgment['reports'][label][dimension]['score'] if judgment else ''
     item['judgment_path']=jp.relative_to(ROOT).as_posix() if judgment else ''
     scores.append(item)
  for role,bases in [('author',[primary/'coordinator/author']),('judge',[primary/'judgments',ROOT/'format-supplement'/provider/'judgments'])]:
   records=[]
   for base in bases:
    for path in sorted(base.rglob('execution.json')):
     r=read(path);u=r.get('usage',{});records.append(r)
     usage_rows.append({'provider':provider,'role':role,'path':path.relative_to(ROOT).as_posix(),'status':r['status'],'error':r.get('error',''),'input_tokens':u.get('prompt_tokens',u.get('input_tokens','')),'completion_tokens':u.get('completion_tokens',u.get('output_tokens','')),'total_tokens':u.get('total_tokens',u['input_tokens']+u['output_tokens'] if 'input_tokens' in u and 'output_tokens' in u else ''),'elapsed_seconds':r.get('elapsed_seconds','')})
   summary['authors' if role=='author' else 'judges'][provider]={'calls':len(records),'response_complete':sum(r['status']=='response_complete' for r in records),'missing_usage':sum(not r.get('usage') for r in records)}
 for name,rows in [('scores.csv',scores),('usage.csv',usage_rows)]:
  with (ROOT/name).open('w',encoding='utf-8',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 (ROOT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':derive()
