"""Use the repository's current five-dimension standard, before any study judgment."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json, sys
from pathlib import Path
import importlib.util
spec=importlib.util.spec_from_file_location('quality_study',Path(__file__).with_name('quality-study.py'))
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
DIMS=['task_fidelity','facts_evidence','explanation_synthesis','counterevidence_boundaries','reader_usefulness']
JUDGE=s.JUDGE.replace('task_fidelity: number, evidence: number, analysis: number, decision_usefulness: number, counterevidence: number, readability: number','task_fidelity: number, facts_evidence: number, explanation_synthesis: number, counterevidence_boundaries: number, reader_usefulness: number').replace('same six keys','same five keys')
start=JUDGE.index('Each score is 0 to 5')
end=JUDGE.index('A verdict passes',start)
JUDGE=JUDGE[:start]+'Each score is an integer 0–4 or not_assessed, following the project standard: 0 essential requirements absent; 1 major defects make the aspect unusable; 2 substantive changes needed; 3 meets the task; 4 fully developed with concrete support. Give located reasons; an aggregate must not hide actual errors. The five dimensions receive equal weight; total /100 is 5 times their sum. Reader usefulness includes readability and decision relevance. Use not_assessed only when an assessment could not actually occur. '+JUDGE[end:]

def freeze():
 assert not list((s.OUT/'reviews').glob('**/execution.json'))
 s.save(s.OUT/'review-standard-amendment.json',{'created_at':datetime.now(timezone.utc).isoformat(),'reason':'Before any study judgments, align scores to the existing report-evaluation-standard.md (five integer 0–4 dimensions) instead of introducing another six-dimension scale. Author inputs, task/source choices, order, planned counts and primary/swap roles unchanged. No study reports or scores were read when making this correction.','replaces':'plan.json judge_system and score aggregation specification only','judge_system':JUDGE,'dimensions':DIMS,'aggregate':'5 * sum of five integer scores; NA if any not_assessed','standard_sha256':s.sha((s.REPO/'docs/report-evaluation-standard.md').read_bytes()),'driver_sha256':s.sha(Path(__file__).read_bytes())})
 print('Existing five-dimension rubric frozen before first judgment.')

def judge(p,t,swap):
 primary=p['primary_A_condition'][t['id']];a=('after' if primary=='before' else 'before') if swap else primary;b='after' if a=='before' else 'before'
 packet={'task':t,'reports':{},'measurements':{}}
 for alias,c in [('A',a),('B',b)]:
  folder=s.OUT/'authors'/t['id']/c;report=(folder/'report.md').read_text(encoding='utf-8')
  assert s.sha(report)==s.read(folder/'report-record.json')['sha256']
  packet['reports'][alias]=report;packet['measurements'][alias]={'characters':s.count(report),'minimum':t['minimum'],'maximum':t['maximum'],'unit':'nonwhitespace_unicode_characters_including_markup'}
 result=s.call(p,JUDGE,packet,s.OUT/'reviews'/t['id']/('swap' if swap else 'primary'))
 for alias in ['A','B']:
  r=result['reports'][alias];assert set(r['scores'])==set(DIMS)
  assert all(v=='not_assessed' or type(v) is int and 0<=v<=4 for v in r['scores'].values())
  assert r['verdict'] in ['pass','needs_revision'] and (r['verdict']=='pass')==(len(r['findings'])==0)
 assert result['preference'] in ['A','B','tie']
 print(t['id'],'swap' if swap else 'primary',result['preference'],{k:r['verdict'] for k,r in result['reports'].items()},flush=True)

def run():
 p=s.plan();a=s.read(s.OUT/'review-standard-amendment.json');assert a['driver_sha256']==s.sha(Path(__file__).read_bytes())
 tasks=[t for t in p['tasks'] if not sys.argv[2:] or t['id'] in sys.argv[2:]]
 with ThreadPoolExecutor(max_workers=4) as pool:
  fs=[pool.submit(judge,p,t,swap) for t in tasks for swap in [False,True]]
  for f in as_completed(fs):
   try:f.result()
   except Exception as e:print('ERROR',repr(e),flush=True)
if __name__=='__main__':freeze() if sys.argv[1]=='freeze' else run()
