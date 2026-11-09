"""Apply EV-IRWZH-01 only, using existing owner and official save/prepare; no model execution."""
from pathlib import Path
import sys,json,hashlib,difflib,datetime
R=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(R))
from managed_research import WORKSPACE,invoke,write

CID='instant_retail_warehouses_zh'
AUTHOR='/root/microdrama_research'
FOLDER=R/'research'/CID
O=FOLDER/'codex-production'
TASK=WORKSPACE/CID
CURRENT=TASK/'reports/current.md'
POINTER=FOLDER/'native-full-prepared.json'
REV=O/'draft-revision-full-02.md'
NOTE=O/'change-note-full-02.md'
EXEC=O/'execution-full-02.json'
BACKUP=FOLDER/'native-full-before-evidence-conditions-prepared.json'
NEWPREP=FOLDER/'native-full-evidence-conditions-prepared.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()

for p in [REV,NOTE,EXEC,BACKUP,NEWPREP]:
    if p.exists():raise FileExistsError(str(p))
started=now()
status=invoke(CID,'author-evidence-conditions-status','status',{'task':CID})
progress=json.loads((TASK/'state/progress.json').read_text(encoding='utf-8'))
if progress['current_artifact']['owner']!=AUTHOR:raise ValueError('Existing owner differs; do not change owner.')
if progress['current_artifact']['path']!='reports/current.md':raise ValueError('Unexpected current artifact')
source=CURRENT.read_bytes();old=source.decode('utf-8')
prepared=POINTER.read_bytes();request=json.loads(prepared)['request']
findings=json.loads((FOLDER/'native-full-current-reviews/evidence/response.json').read_text(encoding='utf-8'))
if not any(f.get('finding_id')=='EV-IRWZH-01' for f in findings['findings']):raise ValueError('Missing actual finding')
script=O/'warehouse-model.py'
script_text=script.read_text(encoding='utf-8')
if "'delivery':7.5,'ads':1.5" not in script_text or "'loss':.025 if month<4 else .02" not in script_text or "'ads':1.5 if month<4 else 1" not in script_text:
    raise ValueError('Existing model conditions differ')
changes=[
 ('毛利30%，损耗3.5%，拣选2.2元，配送7.5元 | 4.58','毛利30%，损耗3.5%，拣选2.2元，配送7.5元，投流1.5元/单 | 4.58'),
 ('生鲜新区域还需承受爬坡。以下假设设备及开仓资本60万元、保证金7.5万元，存货按现款采购；','生鲜新区域还需承受爬坡。其中，第1—3个月损耗率为2.5%、投流为1.5元/单；第4个月起，损耗率降至2%、投流降至1元/单。以下假设设备及开仓资本60万元、保证金7.5万元，存货按现款采购；')
]
new=old
for a,b in changes:
    if new.count(a)!=1:raise ValueError('Expected one exact edit target')
    new=new.replace(a,b,1)
preserved=[O/'draft-final.md',O/'draft-final.first-complete.md',O/'draft-revision-full-01.md',O/'change-note-full-01.md',script,O/'warehouse-results.json',O/'warehouse-results.csv',O/'financial-bridges.py',O/'financial-bridges.json']
before={str(p):sha(p.read_bytes()) for p in preserved}
REV.write_bytes(new.encode('utf-8'))
BACKUP.write_bytes(prepared)
diff=''.join(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),fromfile='reports/current.md before EV-IRWZH-01',tofile='draft-revision-full-02.md',n=2))
NOTE.write_text('# 全文精确修订说明 02\n\n对应独立证据finding：`EV-IRWZH-01`。作者：`'+AUTHOR+'`。\n\n只补两项已有条件：弱商圈投流为1.5元/单；现金桥第1—3个月损耗2.5%、投流1.5元/单，第4个月起分别降至2%和1元/单。原计算脚本、全部数值、输出及其余正文不变，没有重跑计算。\n\n基准稿SHA-256：`'+sha(source)+'`\n\n修订稿SHA-256：`'+sha(new.encode('utf-8'))+'`\n\n已读原始finding、warehouse-model.py中fresh_weak与六个月循环参数，未新增调查。按原登记作者身份通过官方save保存，并复用原native-full-prepared请求重新prepare；实际结果见execution-full-02.json。\n\n```diff\n'+diff+'```\n',encoding='utf-8',newline='\n')
execution={'host_task':AUTHOR,'kind':'author_revision_not_independent_review','status':'started','started_at':started,'finding_id':'EV-IRWZH-01','previous_input_version':json.loads(prepared)['result']['input_version'],'previous_report_sha256':sha(source),'revision_report_sha256':sha(new.encode('utf-8')),'revision_path':str(REV),'change_note':str(NOTE),'model_executed':False,'owner_before':progress['current_artifact']['owner'],'preserved_hashes':before,'diff':diff}
write(EXEC,execution)
save_request={'task':CID,'draft':{'path':'reports/current.md','content':new,'main':True,'complete':True,'kind':'report','unit_id':'report','host_task':AUTHOR,'handoff':{'summary':'EV-IRWZH-01: disclose existing weak-market ad cost and month-four loss/ad changes; all model inputs and outputs retained without re-execution.','pending':['Independent recheck of this condition-disclosure revision and existing full-report review responsibilities.']}}}
saved=invoke(CID,'author-save-evidence-conditions-full-02','save',save_request)
if saved.get('ok') is False:raise ValueError(str(saved))
if sha(CURRENT.read_bytes())!=sha(new.encode('utf-8')):raise ValueError('Saved report differs from revision')
result=invoke(CID,'author-prepare-evidence-conditions-full-02','review',request)
if result.get('ok') is False:raise ValueError(str(result))
pack={'request':request,'result':result}
write(NEWPREP,pack)
write(POINTER,pack)
after=json.loads((TASK/'state/progress.json').read_text(encoding='utf-8'))
if after['current_artifact']['owner']!=AUTHOR:raise ValueError('Owner changed unexpectedly')
for p,h in before.items():
    if sha(Path(p).read_bytes())!=h:raise ValueError('Preserved calculation or draft changed: '+p)
execution.update(status='completed',completed_at=now(),save_result=saved,prepare_request=request,new_input_version=result['input_version'],prepared_path=str(NEWPREP),default_pointer=str(POINTER),default_pointer_sha256=sha(POINTER.read_bytes()),current_report_sha256=sha(CURRENT.read_bytes()),owner_after=after['current_artifact']['owner'],originals_and_calculations_unchanged=True,assignments_prepared=[a['slot_id'] for a in result.get('assignments',[])],independent_reviews_run_by_author=False)
write(EXEC,execution)
print(json.dumps({k:execution[k] for k in ['status','new_input_version','current_report_sha256','revision_path','change_note','prepared_path','default_pointer','owner_after','originals_and_calculations_unchanged']},ensure_ascii=False,indent=2))
