"""Target two located weaknesses after locking the complete first study."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import importlib.util, json, sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('review',Path(__file__).with_name('quality-study-review.py'))
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
s=r.s
OUT=s.OUT/'repairs'
TARGETS={
 'reasoning_model_competition_zh':'The complete first blind comparison consistently found this report weaker in its OpenAI comparison. Source S003 includes a concrete OpenAI Deep Research example about web understanding and source verification. Use that available evidence with its secondary-evaluation attribution to explain how OpenAI combines information acquisition, verification and reasoning; compare it directly with Claude engineering workflow and DeepSeek deployment/distribution. Preserve the existing accurate technical distinctions and source limits; do not invent new facts or simply add names. This is a comparative-quality improvement, not a claim that the first report failed acceptance.',
 'coding_benchmark_decision_zh':'The first blind comparison consistently found the pilot plan less executable than the other report. Make the initial scope, responsible roles, practical sequence/time or resource assumptions and expansion/change/stop decisions concrete; any proposed scale or duration must be labeled a proposed starting point, not a research-derived guarantee. A separate confirmed publication defect is six private browser citation tokens in this standalone Markdown report. Replace every actual citation with its correct source title and URL from the provided records. Keep the original facts, denominator distinctions and attribution of benchmark critiques. Do not add external people or outside material as requirements. Stay within 2500–4000 nonwhitespace characters including Markdown links; compress repetition to make room.'
}
EXPORT='''The destination is a standalone Markdown file read outside the originating chat. Apply the updated shared review instruction: "Review the artifact in its intended delivery format. For exported Markdown or documents, check that citations resolve to the supplied source titles, URLs or locators rather than private chat/tool tokens. For comparisons and implementation plans, check whether available distinguishing evidence and an actionable first step reach the reader; do not add equal-length quotas or new approval requirements." Both anonymous reports must be assessed by this same rule. Do not infer which is a revision or prefer one because of a guessed condition.'''

def prepare():
 p=s.plan();s.read(s.OUT/'initial-summary.json')
 methods={f:(s.REPO/f).read_text(encoding='utf-8') for f in s.METHODS}
 rp={'created_at':datetime.now(timezone.utc).isoformat(),'initial_summary_sha256':s.sha((s.OUT/'initial-summary.json').read_bytes()),'tasks':[t for t in p['tasks'] if t['id'] in TARGETS],'methods':methods,'targets':TARGETS,'settings':p['settings'],'author_system':p['author_system'],'judge_system':r.JUDGE+'\n'+EXPORT,'A_version':{'reasoning_model_competition_zh':'repaired','coding_benchmark_decision_zh':'original'},'planned_calls':{'changed_report_authors':2,'blind_original_vs_revised_reviews':2},'scope':'Post-result targeted report repair and current method clarification. First study scores/preferences/output files stay unchanged. These feedback-assisted revisions are not new first-attempt effect estimates. Reviewer input clarifies the existing standalone-Markdown citation requirement for both anonymous texts. One fresh Astra context per comparison; no author notes or prior reviews supplied.','driver_sha256':s.sha(Path(__file__).read_bytes())}
 s.save(OUT/'plan.json',rp);s.save(OUT/'plan-hash.json',{'sha256':s.sha((OUT/'plan.json').read_bytes())})
 print('Targeted repair plan frozen: two changed reports and two fresh blind comparisons.',flush=True)

def plan():
 s.plan();p=s.read(OUT/'plan.json')
 assert s.sha((OUT/'plan.json').read_bytes())==s.read(OUT/'plan-hash.json')['sha256']
 assert s.sha(Path(__file__).read_bytes())==p['driver_sha256']
 return p

def author(p,t):
 original=(s.OUT/'authors'/t['id']/'after/report.md').read_text(encoding='utf-8')
 packet={'task':t,'methods':p['methods'],'original_report':original,'stage_request':p['targets'][t['id']]+' Return ONLY JSON with report (the complete revised reader-facing Markdown string) and changes (brief concrete edit summary). You are revising an already staged complete report; do not claim a new research collection or completed review.'}
 result=s.call(p,p['author_system'],packet,OUT/t['id']/'author')
 report=result['report'].strip()+'\n';folder=OUT/t['id']
 if not (folder/'report.md').exists():
  s.textsave(folder/'report.md',report);s.save(folder/'report-record.json',{'sha256':s.sha(report),'characters':s.count(report),'minimum':t['minimum'],'maximum':t['maximum'],'length_met':t['minimum']<=s.count(report)<=t['maximum'],'original_report_sha256':s.sha(original)})
 print(t['id'],'repaired',s.count(report),'characters',flush=True)

def judge(p,t):
 key=t['id'];texts={'original':(s.OUT/'authors'/key/'after/report.md').read_text(encoding='utf-8'),'repaired':(OUT/key/'report.md').read_text(encoding='utf-8')}
 a=p['A_version'][key];mapping={'A':a,'B':'original' if a=='repaired' else 'repaired'}
 packet={'task':t,'reports':{alias:texts[v] for alias,v in mapping.items()},'measurements':{alias:{'characters':s.count(texts[v]),'minimum':t['minimum'],'maximum':t['maximum'],'unit':'nonwhitespace_unicode_characters_including_markup'} for alias,v in mapping.items()}}
 result=s.call(p,p['judge_system'],packet,OUT/key/'review')
 revised=result['reports'][next(k for k,v in mapping.items() if v=='repaired')]
 print(key,'changed_report_verdict',revised['verdict'],'preference',result['preference'],flush=True)

if __name__=='__main__':
 if sys.argv[1]=='prepare':prepare()
 else:
  p=plan()
  with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(lambda t:(author if sys.argv[1]=='authors' else judge)(p,t),p['tasks']))
