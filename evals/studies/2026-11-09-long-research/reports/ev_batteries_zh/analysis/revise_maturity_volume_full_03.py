"""Author repair of REQ-EV-01/02 using newly read originals and one new scenario."""
from pathlib import Path
from datetime import datetime, timezone
import csv, difflib, hashlib, json, shutil, sys

R = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(R))
from managed_research import ROOT, WORKSPACE, invoke, write

CID = 'ev_batteries_zh'
AUTHOR = '/root/remaining_research_inputs'
F = ROOT / 'research' / CID
O = F / 'codex-production'
T = WORKSPACE / CID
sha = lambda b: hashlib.sha256(b).hexdigest()
now = datetime.now(timezone.utc).isoformat()
current = T / 'reports/current.md'
before_bytes = current.read_bytes()
before = current.read_text(encoding='utf8')
prior = json.loads((F / 'native-full-prepared.json').read_text(encoding='utf8'))
review = json.loads((F / 'native-full-final-reviews/requirements/response.json').read_text(encoding='utf8'))
if prior['result']['input_version'] != review['input_version']:
    raise ValueError('Current review version changed')
history = F / ('native-full-final-reviews-before-maturity-volume-' + review['input_version'][:16])
if not history.is_dir():
    raise ValueError('Archive the actual reviews before revision')
for name in ['draft-before-full-03.md', 'draft-revision-full-03.md', 'change-note-full-03.md', 'execution-full-03.json']:
    if (O / name).exists():
        raise FileExistsError(name)
preserved = {str(p): sha(p.read_bytes()) for p in [O/'calculate_scenarios.py', O/'calculations.json', O/'report.md', O/'report-v1.md', O/'draft-revision-full-01.md', O/'draft-revision-full-02.md']}
(O / 'draft-before-full-03.md').write_bytes(before_bytes)
shutil.copy2(F/'native-full-prepared.json', F/'native-full-before-maturity-volume-prepared.json')

volume = '''再把体积约束单独算清。前一段以75 kWh名义电量换算质量；这里另设75 kWh可用电量、90%可用比例，因此需要83.33 kWh名义电量。假设车辆给电池及安装接口留下300 L布置空间，其中20 L用于包外管路接头、电气接口和装配避让，完整电池包只能占280 L。候选A拟采用成熟LFP，候选B拟采用高能三元，完整包级体积能量密度分别假设为240和320 Wh/L。这是用于检查选择边界的分析输入，不是刀片或麒麟实测参数，也不代表两种化学路线的通用区间；密度分母已包含包壳、包内冷却、保护与BMS，不能再重复扣除这些体积。

所需安装体积 = 可用电量 × 1000 ÷（可用比例 × 包级Wh/L）＋包外安装预留。

| 相同车辆空间下的候选 | 假设完整包级体积能量密度 | 提供75 kWh可用电量所需包体积 | 加20 L预留后的安装体积 | 300 L空间内最多可用电量 | 体积判断 |
|---|---:|---:|---:|---:|---|
| A：拟用成熟LFP | 240 Wh/L | 347.22 L | 367.22 L | 60.48 kWh | 超出67.22 L，原目标不可行 |
| B：拟用高能三元 | 320 Wh/L | 260.42 L | 280.42 L | 80.64 kWh | 余19.58 L，满足体积必要条件 |

在这组条件下，满足75 kWh可用目标要求包级体积能量密度至少297.62 Wh/L。候选B即使每kWh更贵，也可能因A装不下而进入下一轮车型验证；但这并不构成三元路线的普遍优胜。若通过降低续航目标或提高整车效率，把可用电量需求降到60 kWh，即减少20%，A的安装体积降至297.78 L，也能进入报价比较。真正改变选型的是同一车辆下的能量需求、完整包密度和可用窗口，不能把LMFP的525 Wh/L电芯值直接代入这张包级表。

该算例采用同一参考温度、新包状态和可用窗口，不含冬季或老化折减；寿命末期的可用能量要求会提高密度或空间需求。总升数合格还不是几何装配合格，仍需核对包的形状、厚度、碰撞结构、质量、功率和热管理。新增输入、公式和结果单独保存在calculate_volume_full_03.py与volume-scenario-full-03.json。

'''
maturity = '''成熟路线已有可定位的实际应用链。比亚迪2024年年报第22页将刀片电池定义为磷酸铁锂电池，第27—28页记录其自2020年7月起逐步应用于比亚迪、腾势、方程豹和仰望的纯电及插混车型，并披露2024年刀片电池装机量近200 GWh；同页还列出海豹的CTB装车应用。这是公司对已经发生的年度装机和车型应用的披露，证据强于计划产能，不能换算成某一款包的产量、外售量、良率或采购价，也不能拿2024年数量证明2026年第二代刀片已经同规模供货。[比亚迪2024年年报，第22、27—28页（PDF第23、28—29页）](https://static.cninfo.com.cn/finalpage/2025-03-24/1222882857.PDF)

成熟三元的具名参照采用麒麟的NCM商业版本。CATL的2023年4月17日官方公告及海报明确“极氪009 ME版正式交付”，使麒麟从2022年的发布计划推进到具名车型交付；海报本身没有说明电芯化学。2025年5月招股书第177页将乘用车麒麟作为NCM产品介绍，第184页进一步说明CTP 3.0可集成高镍三元或其他化学体系，已有长续航、高功率、快充等版本；第258页在回顾2022—2024年经营时明确提到麒麟、神行的规模化商业应用。因此可以把麒麟的NCM版本作为已商业化系列比较，并把极氪009 ME交付作为该系列的具名整车事件；不能把所有麒麟车型归为同一化学配方，也不能将2025年的最高快充指标倒赋给2023年交付车。现有材料尚未拆出各版本的年度装机量和当前供应合同。[CATL正式交付公告及海报](https://www.catl.com/news/7136.html)、[CATL 2025年招股书，第177、184、258页（PDF第187、194、268页）](https://www.catl.com/en/uploads/1/file/public/202505/20250512071033_9of2dqw816.pdf)

'''
oldrow = '| 麒麟2022发布；Astroinno 2023发布 | 产品与工艺主张，并给出未来生产计划 | 对这两个具体版本的连续合格产出、车型覆盖和实际采购价；不据早年计划自动补成已实现 |'
newrow = '''| 成熟LFP：比亚迪刀片系列，2020年起应用，2024年度装机披露 | 年报将其确认为LFP，列多品牌纯电/插混应用、海豹CTB应用与2024年近200 GWh装机 | 公司装机披露不等于单车型产量、对外销量或良率；不外推2026第二代产品规模，采购价仍需询价 |
| 成熟三元代表：麒麟NCM商业系列；2023-04-17极氪009 ME交付，2025招股书回顾 | 官方海报确认具名整车正式交付；招股书确认NCM产品、多个版本与2022—2024年间规模化商业应用 | 系列内可含其他化学体系，后发性能不倒置到2023版本；未披露分版本年度装机和当前合同 |
| Astroinno L600，2023发布 | 产品与工艺主张，并给出2024生产计划 | 本文材料仍未证明该具体版本的连续合格产出、车型覆盖和实际采购价；不据早年计划补成已实现 |'''
changes = [
 ('对运营车，假设平均每天真实减少15分钟停机', volume + '对运营车，假设平均每天真实减少15分钟停机'),
 ('全部输入、公式与输出保存在同目录`calculate_scenarios.py`和`calculations.json`，可以复算。', '既有成本、质量及运营算例的输入、公式与输出保存在同目录`calculate_scenarios.py`和`calculations.json`；新增体积算例使用前述独立文件，均可复算。'),
 ('## 七、量产证据链：公告中已经发生了哪一步\n\n', '## 七、量产证据链：公告中已经发生了哪一步\n\n' + maturity),
 (oldrow, newrow),
 ('公告当时把2023量产写为未来目标；无单品采购价', '公告当时把2023量产写为未来目标；后续具名交付见第七节，不能据交付确认全部最高指标；无单品采购价'),
 ('| 经济型通勤，有稳定慢充 | 成熟LFP作为基准；', '| 经济型通勤，有稳定慢充 | 以刀片等已有装机证据的成熟LFP系列作为基准；'),
 ('| 长续航、质量体积受限或高性能 | 高能量三元、硅碳改进与已验证的固液混合方案；全固态可进入并行验证 | 持续功率、低SOC输出、热管理、碰撞、充电衰减及售后可维护性 | 整车效率提升会降低所需容量；', '| 长续航、质量体积受限或高性能 | 已商业化的高能三元（如麒麟NCM版本）、硅碳改进与已验证的固液混合方案；全固态可进入并行验证 | 完整包级Wh/L、安装空间与可用窗口，并验证持续功率、低SOC输出、热管理、碰撞、充电衰减及售后可维护性 | 第六节假设下75 kWh可用目标需至少297.62 Wh/L；需求降至60 kWh时假设LFP候选也可装入。整车效率提升会降低所需容量；'),
]
after = before
for a, b in changes:
    if after.count(a) != 1:
        raise ValueError('Expected exact passage: ' + a[:90])
    after = after.replace(a, b, 1)
(O/'draft-revision-full-03.md').write_text(after, encoding='utf8', newline='\n')
(O/'analysis-maturity-volume-full-03.md').write_text('# 已定位遗漏的补充分析\n\n' + maturity + volume, encoding='utf8', newline='\n')

readings = []
source_rows = []
descriptions = {
 'EVB25': ('公告标题、2023-04-17日期及海报完整可见文字：宁德时代麒麟电池全球量产首发车型，ZEEKR 009 ME版正式交付。', '官方交付事件；海报未列化学体系、容量、批量或持续供货统计。', None),
 'EVB26': ('PDF第23、28、29页（正文第22、27、28页）实际视觉核读；另读PDF第1—3页身份/报告期文字。核对LFP定义、跨页刀片研发进展列、2020年7月起应用、2024年近200GWh及海豹CTB应用。', '291页文件只读相关位置；近200GWh是公司刀片年度装机披露，不能改为单型号/对外销量/产能；不采用同表零风险宣传结论。', [23,28,29]),
 'EVB27': ('PDF第187、194、268页（正文第177、184、258页）实际视觉核读；另读PDF第2、19页相关文字。核对NCM产品分类、高镍三元或其他化学、多版本与规模化商业应用回顾；第2页确认2025-05-12。', '626页招股书仅相关页；系列最高值不归给2023单车，未获得分版本装机量；不将企业利润变化归因于单一电池。', [187,194,268]),
}
for sid, (scope, boundary, pages) in descriptions.items():
    src = ROOT/'sources'/sid
    meta = json.loads((src/'retrieval.json').read_text(encoding='utf8'))
    destination = T/'sources/actual'/sid
    if destination.exists():
        raise FileExistsError(destination)
    shutil.copytree(src, destination)
    text = (src/'original.txt').read_text(encoding='utf8')
    if pages:
        allpages = json.loads((src/'pages.json').read_text(encoding='utf8'))
        excerpts = [{'pdf_page': n, 'text': allpages[n-1]['text']} for n in pages]
        binary = destination/'original.pdf'
    else:
        excerpts = [{'html_text': text}, {'poster_transcription': '宁德时代麒麟电池；全球量产首发车型；ZEEKR 009 ME版；正式交付。'}]
        binary = destination/'delivery-poster.jpg'
    reading = {'source_id': sid, 'title':meta['title'], 'url':meta['url'], 'published_at':meta.get('published_at'),
        'accessed_at':meta['accessed_at'], 'recorded_at':now, 'reader':AUTHOR, 'actually_read':scope,
        'boundary':boundary, 'full_text_read':False, 'original_sha256':meta['sha256'],
        'bound_binary_sha256':sha(binary.read_bytes()), 'method':'local original plus visual inspection of specified poster/PDF pages',
        'selected_text':excerpts, 'local_original_directory':str(src), 'managed_original_directory':destination.relative_to(T).as_posix()}
    readings.append(reading)
    note = T/'notes/actual-reading'/f'{sid}.json'
    write(note, reading)
    source_rows.append({'source_id':sid,'title':meta['title'],'url':meta['url'],'source_type':'public_primary',
        'read_scope':'relevant_sections','read_evidence':note.relative_to(T).as_posix(),
        'evidence_path':binary.relative_to(T).as_posix(),'locator':scope,'reader':AUTHOR})

calcfile = 'volume-scenario-full-03.json'
calcdest = T/'analysis/calculations'
calcdest.mkdir(parents=True,exist_ok=True)
for name in ['calculate_volume_full_03.py', calcfile]:
    shutil.copy2(O/name, calcdest/name)
source_rows.append({'source_id':calcfile,'title':'New explicit pack-volume and usable-energy scenario',
    'url':'analysis/calculations/'+calcfile,'source_type':'author_calculation','read_scope':'full_text',
    'read_evidence':'analysis/calculations/calculate_volume_full_03.py','evidence_path':'analysis/calculations/'+calcfile,
    'locator':'75 usable kWh, 90% window, 300 L envelope, 20 L outside reserve; assumed 240/320 Wh/L; 60 kWh sensitivity. New calculation only.','reader':AUTHOR})
claims = [
 {'claim_id':'EV-F03-01','claim':'刀片年报确认为LFP，2020年7月起车型应用，2024年公司刀片装机近200GWh，并列海豹CTB应用。','claim_type':'fact','supporting_sources':['EVB26'],'evidence_detail':'Annual report printed pp22,27–28 / PDF23,28–29','uncertainty':'Issuer disclosure, not per-model production, external sales, nameplate capacity or 2026 second-generation volume.'},
 {'claim_id':'EV-F03-02','claim':'CATL官方2023-04-17海报确认极氪009 ME版正式交付。','claim_type':'fact','supporting_sources':['EVB25'],'evidence_detail':'Official dated page and entire delivery poster','uncertainty':'The poster does not identify cell chemistry, volume or subsequent supply statistics.'},
 {'claim_id':'EV-F03-03','claim':'2025招股书把麒麟列为NCM产品并说明CTP可集成高镍三元或其他体系、多版本已推出，经营回顾描述麒麟规模化商业应用。','claim_type':'fact','supporting_sources':['EVB27'],'evidence_detail':'Printed pp177,184,258 / PDF187,194,268','uncertainty':'Series-level classification and commercialization; no retroactive assignment of 2025 maximum specifications to 2023 ME delivery.'},
 {'claim_id':'EV-F03-04','claim':'明确假设下，75kWh可用目标及300L安装空间要求至少297.62Wh/L包级密度；A/B需367.22/280.42L，A在60kWh目标时需297.78L。','claim_type':'assumption','supporting_sources':[calcfile],'evidence_detail':'New executed scenario inputs, formulas and results','uncertainty':'Hypothetical densities, not Blade/Qilin measurements or chemistry-wide typical ranges. Volume is a necessary, not sufficient, vehicle condition.'},
]
for row in claims:
    row['author'] = AUTHOR
    row['recorded_at'] = now
    row['review_status'] = 'author_revision_pending_independent_review'
(O/'reading-ledger-full-03.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in readings),encoding='utf8',newline='\n')
(O/'claims-full-03.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in claims),encoding='utf8',newline='\n')
write(O/'sources-full-03.json', source_rows)
shutil.copy2(O/'reading-ledger-full-03.jsonl', T/'notes/author-reading-ledger-full-03.jsonl')
diff = ''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='reports/current-before-full-03.md',tofile='draft-revision-full-03.md'))
note = '# EV完整稿修订03\n\n作者：'+AUTHOR+'。时间：'+now+'。\n\n对应真实requirements意见REQ-EV-01、REQ-EV-02。原input_version：'+review['input_version']+'；assignment_version：'+review['assignment_version']+'。\n\n原始final reviews已复制到'+str(history)+'，不替换其负面finding或真实通过原件。\n\n原报告文件字节SHA-256：'+sha(before_bytes)+'\n\n原报告规范文本SHA-256：'+sha(before.encode())+'\n\n修订稿SHA-256：'+sha(after.encode())+'\n\nREQ-EV-01：新增刀片LFP实际装机/车型链、麒麟正式交付海报以及招股书NCM分类与商业化后续；按系列、车型事件、年份和披露口径区分，未把结构名当化学配方。\n\nREQ-EV-02：新增完整包级体积、可用窗口、安装余量算例与阈值，连接长续航车型选择及需求下降后的选择反转；240/320Wh/L均为假设。只执行新脚本calculate_volume_full_03.py，没有运行旧计算。\n\n实际阅读范围、原件、source/claim映射分别在reading-ledger-full-03.jsonl、sources-full-03.json、claims-full-03.jsonl。原始291/626页文档未被登记为全文已读。\n\n原报告与各次首稿、既有计算保持不变，当前稿另存draft-before-full-03.md。此为作者修订，不是独立审阅通过。\n\n## 完整文本diff\n\n'+chr(96)*3+'diff\n'+diff+chr(96)*3+'\n'
(O/'change-note-full-03.md').write_text(note,encoding='utf8',newline='\n')

registered = invoke(CID,'register-maturity-volume-originals','save',{'task':CID,'sources':source_rows,'claims':claims})
if registered.get('ok') is False:
    raise ValueError(registered)
write(O/'managed-materials-full-03.json',registered)
sources = list(csv.DictReader((T/'data/source_registry.csv').open(encoding='utf-8-sig')))
allclaims = list(csv.DictReader((T/'data/claims_registry.csv').open(encoding='utf-8-sig')))
ctx = invoke(CID,'select-current-maturity-volume-inputs','status',{'task':CID,'work':{
    'unit_id':'report','question':'Integrate the complete battery report, including actual mature LFP/NCM commercialization and pack-volume constraints.',
    'source_ids':[x['source_id'] for x in sources], 'claim_ids':[x['claim_id'] for x in allclaims],
    'requirement_ids':['R_TASK','R_LANGUAGE','R_DATE'],'depends_on':['outline']}})
inputs = {k:v for k,v in ctx['work_context']['inputs'].items() if k!='reports/current.md'}
if not all(any(sid in k for k in inputs) for sid in ['EVB25','EVB26','EVB27',calcfile]):
    raise ValueError('New source inputs were not bound')
write(O/'selected-inputs-full-03.json',inputs)
saved = invoke(CID,'save-author-maturity-volume-full-03','save',{'task':CID,'draft':{
    'path':'reports/current.md','content':after,'main':True,'complete':True,'kind':'report','unit_id':'report',
    'host_task':AUTHOR,'based_on':inputs,'depends_on':['outline'],
    'handoff':{'summary':'REQ-EV-01/02 author repair: issuer originals establish mature-route commercialization; one new explicit pack-volume scenario. Earlier computations retained.',
    'pending':['Independent requirements recheck and the remaining full-report responsibilities on this exact revised version.']}}})
if saved.get('ok') is False:
    raise ValueError(saved)
dest = T/'analysis/author-production'
for name in ['draft-before-full-03.md','draft-revision-full-03.md','change-note-full-03.md','analysis-maturity-volume-full-03.md','calculate_volume_full_03.py',calcfile,'reading-ledger-full-03.jsonl','claims-full-03.jsonl','sources-full-03.json','selected-inputs-full-03.json']:
    shutil.copy2(O/name,dest/name)
request = {**prior['request'],'revision':True}
request['evidence_paths'] = list(dict.fromkeys(request.get('evidence_paths',[]) + ['notes/author-reading-ledger-full-03.jsonl','analysis/calculations/'+calcfile,'analysis/author-production/analysis-maturity-volume-full-03.md']))
result = invoke(CID,'prepare-maturity-volume-full-03','review',request)
write(F/'native-full-maturity-volume-prepared.json',{'request':request,'result':result})
write(F/'native-full-prepared.json',{'request':request,'result':result})
for p, h in preserved.items():
    if sha(Path(p).read_bytes()) != h:
        raise ValueError('Original changed: '+p)
if current.read_text(encoding='utf8') != after:
    raise ValueError('Current differs from author revision')
execution = {'status':'completed','kind':'author_revision_not_independent_review','host_task':AUTHOR,'completed_at':datetime.now(timezone.utc).isoformat(),
    'findings':['REQ-EV-01','REQ-EV-02'],'previous_input_version':review['input_version'],'new_input_version':result.get('input_version'),
    'revision_sha256':sha(after.encode()),'current_file_sha256':sha(current.read_bytes()),'new_calculation_sha256':sha((O/calcfile).read_bytes()),
    'source_original_sha256':{sid:json.loads((ROOT/'sources'/sid/'retrieval.json').read_text(encoding='utf8'))['sha256'] for sid in descriptions},
    'new_sources':list(descriptions),'new_calculation':calcfile,'new_claim_ids':[x['claim_id'] for x in claims],
    'selected_inputs':inputs,'originals_preserved':preserved,'history_directory':str(history),'save_result':saved,
    'prepared_assignments':[x['slot_id'] for x in result.get('assignments',[])],'delivery_ready':result.get('delivery_ready')}
write(O/'execution-full-03.json',execution)
shutil.copy2(O/'execution-full-03.json',dest/'execution-full-03.json')
print(json.dumps({k:execution[k] for k in ['status','new_input_version','revision_sha256','current_file_sha256','new_calculation_sha256','source_original_sha256','new_sources','new_claim_ids','prepared_assignments','delivery_ready']},ensure_ascii=False,indent=2))
