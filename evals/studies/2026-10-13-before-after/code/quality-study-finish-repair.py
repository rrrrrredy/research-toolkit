"""Keep the overlength repair draft and make its necessary local trim before review."""
from concurrent.futures import ThreadPoolExecutor
import importlib.util, json, sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('repair',Path(__file__).with_name('quality-study-repair.py'))
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
s=r.s

def prepare():
 p=r.plan()
 for t in p['tasks']:
  folder=r.OUT/t['id'];draft=(folder/'report.md').read_text(encoding='utf-8');final=draft
  edits=[]
  if t['id']=='reasoning_model_competition_zh':
   old=draft.split('\n\n')[2]
   new='Reasoning Model竞争需要同时比较能力训练、推理预算与任务执行。DeepSeek R1所代表的强化学习路线和Claude Sonnet风格的混合推理，分别涉及能力形成与调用方式，不能当作相互替代的路线。'
   assert old.startswith('Reasoning Model的竞争')
   final=draft.replace(old,new,1);edits=[{'old':old,'new':new,'reason':'The model repair was 4,557 nonwhitespace characters against an unchanged 4,500 maximum. Compress the repeated opening; preserve the full technical analysis and newly added OpenAI comparison.'}]
  assert t['minimum']<=s.count(final)<=t['maximum']
  assert 'cite' not in final
  s.textsave(folder/'report-final.md',final)
  s.save(folder/'final-selection.json',{'draft_sha256':s.sha(draft),'draft_characters':s.count(draft),'final_sha256':s.sha(final),'final_characters':s.count(final),'edits':edits,'original_study_unchanged':True,'review_pending':True})
  print(t['id'],s.count(draft),'->',s.count(final),flush=True)

def judge(p,t):
 key=t['id'];texts={'original':(s.OUT/'authors'/key/'after/report.md').read_text(encoding='utf-8'),'repaired':(r.OUT/key/'report-final.md').read_text(encoding='utf-8')}
 a=p['A_version'][key];mapping={'A':a,'B':'original' if a=='repaired' else 'repaired'}
 packet={'task':t,'reports':{alias:texts[v] for alias,v in mapping.items()},'measurements':{alias:{'characters':s.count(texts[v]),'minimum':t['minimum'],'maximum':t['maximum'],'unit':'nonwhitespace_unicode_characters_including_markup'} for alias,v in mapping.items()}}
 result=s.call(p,p['judge_system'],packet,r.OUT/key/'review')
 revised=result['reports'][next(k for k,v in mapping.items() if v=='repaired')]
 print(key,'changed_report_verdict',revised['verdict'],'preference',result['preference'],flush=True)

if __name__=='__main__':
 if sys.argv[1]=='prepare':prepare()
 else:
  p=r.plan()
  with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(lambda t:judge(p,t),p['tasks']))
