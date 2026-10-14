"""Decode the locked first comparisons; no model calls or report modifications."""
import json, statistics
from pathlib import Path
ROOT=Path(__file__).parent/'output/quality-study-20261013'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def score(r):
 values=list(r['scores'].values())
 return 5*sum(values) if all(type(x) is int for x in values) else None
def summarize():
 p=read(ROOT/'plan.json');rows=[]
 for t in p['tasks']:
  key=t['id'];a=p['primary_A_condition'][key];b='after' if a=='before' else 'before'
  primary=read(ROOT/'reviews'/key/'primary/parsed.json');swap=read(ROOT/'reviews'/key/'swap/parsed.json')
  r={'task':key,'group':t['group'],'reports':{},'primary_preference':{'A':a,'B':b,'tie':'tie'}[primary['preference']],'swap_preference':{'A':b,'B':a,'tie':'tie'}[swap['preference']]}
  for alias,c in [('A',a),('B',b)]:
   report=primary['reports'][alias];other=swap['reports']['B' if alias=='A' else 'A']
   r['reports'][c]={'score':score(report),'verdict':report['verdict'],'findings':len(report['findings']),'major_findings':sum(f['severity']=='major' for f in report['findings']),'scores':report['scores'],'swap_score':score(other),'swap_verdict':other['verdict'],**read(ROOT/'authors'/key/c/'report-record.json')}
  r['delta']=r['reports']['after']['score']-r['reports']['before']['score'] if all(r['reports'][c]['score'] is not None for c in ['before','after']) else None
  r['preference_consistent']=r['primary_preference']==r['swap_preference'];rows.append(r)
 def aggregate(items):
  complete=[r for r in items if r['delta'] is not None]
  return {'tasks':len(items),'scored_pairs':len(complete),'before_mean':statistics.mean(r['reports']['before']['score'] for r in complete),'after_mean':statistics.mean(r['reports']['after']['score'] for r in complete),'mean_delta':statistics.mean(r['delta'] for r in complete),'median_delta':statistics.median(r['delta'] for r in complete),'primary_preferences':{c:sum(r['primary_preference']==c for r in items) for c in ['before','after','tie']},'swap_preferences':{c:sum(r['swap_preference']==c for r in items) for c in ['before','after','tie']},'preference_consistent':sum(r['preference_consistent'] for r in items),'primary_passes':{c:sum(r['reports'][c]['verdict']=='pass' for r in items) for c in ['before','after']},'length_passes':{c:sum(r['reports'][c]['length_met'] for r in items) for c in ['before','after']},'primary_reported_findings':{c:sum(r['reports'][c]['findings'] for r in items) for c in ['before','after']}}
 records=[read(f) for part in ['authors','reviews'] for f in (ROOT/part).glob('**/execution.json')]
 result={'scope':'Unchanged initial reports and first primary judgments; swaps shown separately; reviewer findings not yet equivalent to confirmed defects.','rows':rows,'all':aggregate(rows),'original':aggregate([r for r in rows if r['group']=='original']),'new':aggregate([r for r in rows if r['group']=='new']),'execution':{'calls':len(records),'completed':sum(r['status']=='response_complete' for r in records),'usage':{k:sum(r.get('usage',{}).get(k,0) for r in records) for k in ['input_tokens','output_tokens','cached_input_tokens']}}}
 path=ROOT/'initial-summary.json'
 if path.exists():assert read(path)==result
 else:path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps({k:v for k,v in result.items() if k!='rows'},ensure_ascii=False,indent=2))
 print('\n'.join(f"{r['task']}: {r['reports']['before']['score']} -> {r['reports']['after']['score']}; primary={r['primary_preference']}, swap={r['swap_preference']}; defects={r['reports']['before']['findings']}/{r['reports']['after']['findings']}" for r in rows))
if __name__=='__main__':summarize()
