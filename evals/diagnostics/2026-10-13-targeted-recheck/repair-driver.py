"""Direct located report corrections; retain initial reviews and reuse unchanged valid reviews."""
import json, os, sys
from pathlib import Path
REPO=Path(__file__).parent/'research-toolkit'
sys.path.insert(0,str(REPO/'scripts'))
sys.path.insert(0,str(Path(__file__).parent))
import run_blinded_evals as h
import codex_judge
import importlib.util
spec=importlib.util.spec_from_file_location('recheck',Path(__file__).parent/'research-targeted-recheck.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
OUT=m.OUT

REPAIRS={
 ('deepseek','review-profile-zh'): '用户明确要求独立评审，故即使简报仅800字、两份材料，也应选full并显式配置independent，不能选跳过评审的Lite（S1）。作者用Astra，评审可另开全新Astra上下文，无需外部人员或换模型。评审须直接读取完整稿件、原始需求和两份来源，核对需求、证据、推理、结构深度、读者有用性、过程语言及自然表达（S2）。保留原始意见与版本绑定，作者修正必要问题，再让当前全稿通过评估；清除正文内部ID与工作叙述，建立state/final_delivery.json绑定材料、输入、评审和交付消息，核对状态final/complete。脚本可用时运行check_delivery；以上是待执行步骤（S2）。',
 ('glm','review-profile-zh'): '应选择full并明确配置independent：S1规定，明确要求独立评审时，800字或两份材料的规模不改变档位。Astra作者之外，另启一个全新Astra评审上下文即可，不必找外部人员或其他厂商（S2）。交给评审完整成稿、原始需求及两份来源，检查需求、证据、对抗推理、结构深度、读者有用性、过程语言和自然表达。作者处理必要修改，保留原始回应及版本绑定，确保当前整篇评估通过。交付前清理内部ID和工作叙述，用state/final_delivery.json绑定材料、必要输入、评审与交付消息，确认final/complete状态；脚本可执行时再运行check_delivery（S2）。这些步骤尚须实际执行。',
 ('kimi','review-profile-zh'): '选full并显式配置independent。用户明确要求独立评审，优先于短篇、少来源通常可用Lite的建议（S1）。作者使用Astra时，另开新Astra上下文评审即可；不要求外部人员或不同模型（S2）。评审直接读完整成稿、需求及两份来源，覆盖需求、证据、对抗推理、结构深度、读者效用、过程语言清理与自然表达；领域专家仅按实际需要安排。作者修正必要问题并保留原意见及版本绑定，使当前全稿通过评估。清除正文内部ID与过程叙述，以state/final_delivery.json绑定当前材料、必要输入、评审和交付消息；核对final/complete状态，脚本可用时运行check_delivery（S2）。这是一份操作安排，未声称已执行。',
 ('longcat','review-profile-zh'): '这份内部简报应使用full并明确配置independent：用户要求独立评审，不能因约800字、两份材料而改用会跳过评审的Lite（S1）。独立是上下文分离；作者用Astra时，新的Astra上下文即可评审，不必另找人员或厂商（S2）。评审读取完整稿件、需求和两份来源，检查需求、证据、对抗推理、结构深度、读者有用性、过程语言及自然表达。作者修正必要发现，保留原意见与版本绑定，取得当前全稿通过评估的结果。清理正文内部ID和工作叙述，用state/final_delivery.json绑定材料、输入、评审和交付消息，核对final/complete状态；脚本执行可用时运行check_delivery（S2）。此处列出待办，并非执行记录。',
 ('deepseek','receipt-revision-en'): 'The old review and receipt do not cover the edited report. The edit changes the artifact hash; resealing alone cannot make an earlier review cover new prose. A local check cannot refresh the global review, and a global pass cannot refresh a task-required specialist binding (S1).\n\nPreserve the original review and prior version, and record the edit and its reason. Check the revised recommendation against the existing sources and requirements; correct affected claims where needed. Run check-draft for its record prerequisites and actual length, not as content certification. Then request independent global review of the current report using research_review with revision: true, resolve necessary findings, and call finish to bind current inputs and delivery materials in a new receipt (S2).\n\nKeep the same required scopes. Any explicitly required scope must have a passing review bound to the current artifact; do not add new specialist scopes. Unrelated source research and ordinary unit reviews covered by the new global review need not be repeated (S1). These are proposed recovery steps.',
 ('glm','receipt-revision-en'): 'The edited recommendation invalidates coverage by the old global review and receipt: both refer to the previous artifact. Resealing alone cannot make that review assess changed prose. A new global review can refresh the global binding, but cannot refresh any separately required specialist binding (S1).\n\nPreserve the original review and report version, and document the change. Verify the recommendation against the unchanged sources and conditions, correcting affected text or claims if necessary. Run check-draft to check recorded prerequisites and the declared length rule; its result does not establish content quality. Obtain independent global review of the revised artifact through research_review with revision: true. Resolve necessary findings and call finish to create the current delivery binding (S2).\n\nDo not repeat unrelated research merely to renew a receipt. Keep the existing scope requirements, without adding reviews; every declared required scope still needs a passing assessment bound to the current report. A clean global review can cover earlier ordinary unit reviews, which are distinct from explicitly required scopes (S1). Recovery is not yet claimed complete.',
 ('kimi','receipt-revision-en'): 'No: the old review and receipt bind the report as it existed before the edit. The changed artifact hash makes those bindings stale, and resealing alone cannot extend an earlier review to new prose (S1).\n\nPreserve the original review and previous report, record the changed passage and reason, and check the recommendation against the same source numbers and conditions. Correct affected claims if needed, then run check-draft for the declared length and record prerequisites. This check does not certify semantic content. Request independent global review through research_review with revision: true; resolve necessary findings and call finish for the current report and delivery records (S2).\n\nUnrelated source research need not be repeated. The required scopes themselves remain unchanged, but every explicitly required scope needs a passing assessment bound to the current artifact. A new global pass cannot refresh a required specialist binding, although it can cover earlier ordinary unit reviews. Do not add new specialist requirements (S1). These are the recovery steps to perform, not a claim they have run.',
 ('longcat','receipt-revision-en'): 'The previous global review and sealed receipt do not cover the edited report. Both are tied to the earlier artifact; a new receipt alone cannot make the earlier review cover changed prose. Local checks cannot replace the global review, and a global pass cannot refresh a separately required specialist binding (S1).\n\nRetain the original review and report version, and document the edit. Check the recommendation against the unchanged sources and conditions, repairing affected claims if necessary. Run check-draft for its record prerequisites and measured length, without treating it as content validation. Obtain independent global review using research_review with revision: true, address necessary findings, and call finish to produce current delivery bindings (S2).\n\nUnrelated research does not need repeating. Keep the same review requirements: any declared required scope must pass against the current artifact, even when its name is unchanged. Earlier ordinary unit reviews may be covered by the new global review; they are not equivalent to task-required scopes. No additional scopes are needed solely to reseal (S1). Recovery remains to be executed.'
}

def prepare():
 plan=h.read(OUT/'plan.json');tasks={t['task_id']:t for t in plan['tasks']};rows=[]
 for (provider,tid),report in REPAIRS.items():
  count=m.measure(tasks[tid],report);h.require(count['met'],f'{provider}/{tid}: {count}')
  path=OUT/'repairs'/provider/(tid+'.md');path.parent.mkdir(parents=True,exist_ok=True);path.write_text(report+'\n',encoding='utf-8',newline='\n')
  rows.append({'provider':provider,'task_id':tid,'report_path':path.relative_to(OUT).as_posix(),'report_sha256':h.sha(path.read_bytes()),'measurement':count,'author':'maintainer editorial repair, not a new provider response'})
 for provider,tid in [('deepseek','maple-storage-en'),('longcat','brook-rinse-zh')]:
  base=REPO/'evals/repairs/2026-10-13-astra';src=base/(tid+'.md');path=OUT/'repairs'/provider/(tid+'.md');path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(src.read_bytes())
  review_dir='maple-storage-en-revised' if tid=='maple-storage-en' else tid
  request=h.read(base/review_dir/'request.json');packet=json.loads(request['messages'][1]['content'])
  h.require(packet['brief']==tasks[tid]['brief'] and packet['sources']==tasks[tid]['sources'],'Cannot reuse review with different task/source inputs')
  h.require(packet['report'].strip()==src.read_text(encoding='utf-8').strip(),'Reused report differs')
  h.require(h.read(base/review_dir/'review.json')['verdict']=='pass','No reusable pass')
  rows.append({'provider':provider,'task_id':tid,'report_path':path.relative_to(OUT).as_posix(),'report_sha256':h.sha(path.read_bytes()),'measurement':m.measure(tasks[tid],src.read_text(encoding='utf-8')),'author':'maintainer correction using the previously accepted repair for this same task', 'existing_astra_review':'evals/repairs/2026-10-13-astra/'+review_dir+'/review.json','reuse_reason':'Identical report, brief and source texts; no need to repeat an unchanged valid review.'})
 repair={'purpose':'Fix ten specific rejected reports; eight new editorial revisions and two already accepted identical task repairs.', 'rows':rows,'max_new_judge_requests':2,'unchanged_original_reviews':True,
  'review_input_correction':'Initial task-source path metadata reached authors but was removed from judges. Corrected packets retain the exact full sources supplied to authors, including legitimate provenance paths; only author identity, private notes and coordinator map are hidden.',
  'adjudication':[{'task_id':'review-profile-zh','label':'B','finding_location':'参考文献','decision':'Reviewer-input mismatch, not an unsupported author invention: author sources included these paths. Preserve first finding; use complete matching sources in changed-report review.'}],
  'review_reuse':'The two older accepted repair reports are identical to the replacements and have identical task/source inputs; retain and link their actual Astra passes instead of paying to rejudge.'}
 h.save(OUT/'repair-plan.json',repair);print(json.dumps({'new_editorial_versions':8,'reused_accepted_repairs':2,'new_judge_max':2,'measurements':[r['measurement']['actual'] for r in rows]}),flush=True)

def execute():
 plan=h.read(OUT/'plan.json');rp=h.read(OUT/'repair-plan.json');results=[]
 os.environ['RESEARCH_CODEX_EXECUTABLE']=str(Path(os.environ['LOCALAPPDATA'])/'OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe')
 h.save(OUT/'repairs-started.json', {'max_requests':2,'report_hashes':{r['report_path']:r['report_sha256'] for r in rp['rows']}})
 for task in plan['tasks']:
  if task['task_id'] not in {'review-profile-zh','receipt-revision-en'}: continue
  reports=[]
  for label,provider in plan['labels_coordinator_only'][task['task_id']].items():
   row=next(r for r in rp['rows'] if r['provider']==provider and r['task_id']==task['task_id']);path=OUT/row['report_path'];h.require(h.sha(path.read_bytes())==row['report_sha256'],'Repair changed after selection')
   report=path.read_text(encoding='utf-8').strip();reports.append({'label':label,'report':report,'length_measurement':m.measure(task,report)})
  packet={'brief':task['brief'],'sources':task['sources'],'reports':reports};folder=OUT/'repair-judges'/task['task_id'];h.save(folder/'packet.json',packet)
  raw=codex_judge.request(plan['judge'],[{'role':'system','content':plan['judge_system']},{'role':'user','content':json.dumps(packet,ensure_ascii=False)}],folder)
  result={'task_id':task['task_id'],'status':'failed'}
  if raw is not None:
   (folder/'content.txt').write_text(raw,encoding='utf-8',newline='\n')
   value=json.loads(raw);reviews=value['reviews'];h.require(len(reviews)==4 and {r['label'] for r in reviews}==set('ABCD'),'Review labels differ')
   for row in reviews:h.require(row['verdict'] in {'pass','needs_revision'} and isinstance(row['findings'],list) and bool(row['basis']) and ((row['verdict']=='pass')==(not row['findings'])),'Invalid review')
   h.save(folder/'review.json',value);result.update(status='review_complete',reviews=reviews)
  results.append(result);print(json.dumps(result,ensure_ascii=False),flush=True)
 h.save(OUT/'repair-results.json',{'requests':len(results),'results':results})

if __name__=='__main__':{'prepare':prepare,'execute':execute}[sys.argv[1]]()
