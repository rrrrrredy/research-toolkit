"""Convert actual author reading and claims to handoff records. Not an independent review."""
from pathlib import Path
import json,csv,re,hashlib
R=Path(__file__).resolve().parents[3]
READER='/root/microdrama_research'
DATE='2026-11-09'

ed={
 'ED01':('2025-11-19','文章正文Deployment Highlights、Overview、Hardware Reliability完整阅读；未观看视频。9万件/1250小时/3万辆、目标与要求、前臂故障及F03修改。'),
 'ED02':('2026-02-27','重定向BMW新闻正文至引语段完整阅读，不含图片页脚；生产试点、10个月、工厂接口及Leipzig未来计划。'),
 'ED03':('2026-06-25','原文正文lines17–34；F03物流排序新项目、未来运行措辞及既有STR接口。'),
 'ED04':('2024-02-19','文章正文lines24–54；CNC作业、双夹爪、76件型、I/O、夜班与周末、产能翻倍的客户表述。'),
 'ED06':('2026-10-26','web原文lines8–32；2023 POC、2024 RaaS、10万料箱、2027新点计划、6.5万小时的总项目范围。已存web访问返回。'),
 'ED07':('2025-05-13','web正文lines4–43；首次商业时间、英国/欧洲扩展、最高700箱/小时、1000余台MOU。未将MOU算交付。'),
 'ED08':('2026-02-26，2025年度业绩','PDF第5–6页国际客户段及OGRP/live modules相关脚注搜索段；Kroger三处2026-01关闭、Sobeys Calgary需求与10个OGRP中心。未通读82页。'),
 'ED09':('2026年中期业绩，2026-07版本','网页Financial highlights lines450–462；含/不含关停相关款项的收入EBITDA现金流，14个OGRP CFC。未以下载的ECP03全文冒充已读。'),
 'ED12':('2026-11-09所见现行产品页','产品正文、价格、基本自主/专家、手机VR控制、发货和保修描述；FAQ仅取得问题未取得回答。'),
 'ED13':('2026-04-30','工厂说明前约100行正文，制造启动、内部家庭测试、2026发货承诺、预订及产能；未全读后续页尾。'),
 'ED14':('2026-11-09读取的main文档','MoveIt PlanningScene overview短入口说明；未读整个API或软件手册。'),
 'ED16':('arXiv 2504.16054v1','第III–IV节lines83–137；第V节及实验/消融相关lines142–225分段读取。三留出住宅、每任务环境10次、任务进度、训练数据类型与数据消融。'),
 'ED17':('2026-11-09项目页，包含2024-12/2025-04数据更新说明','项目页前110行，76k/350h/564场景/86任务/50采集者/13机构及硬件、标定和语言更新。'),
 'ED18':('π*.6 RECAP公开PDF当前所存版','PDF第8–10页，文本lines795–949与方法关键词段、评价无人工纠正相关line964；任务时间、评分、吞吐和失败。未审计延时视频。'),
 'ED19':('arXiv 2604.15483v1','第VI节lines160–163及IX节lines242–286，图7/9/12/18相关解释与部分跨本体实验；非全文通读。'),
 'ED21':('arXiv 2405.05941v1','引言及方法相关lines80–93，真实训练策略模拟评估方向、视觉与控制匹配；未将其当训练Sim2Real实证。'),
 'ED22':('arXiv 2506.07339v1','第3–5节方法和实验关键词定位段逐段读取；480 episodes/28小时纯执行、六任务、延迟及保护停止；非全附录阅读。'),
 'ED23':('2026-11-09 OSHA技术手册网页','lines367–457集成、操作、维护、应用整体边界及低负载危险；未通读全部标准条文。'),
 'ED26':('2026-10-13','API beta正文前约100行完整文章部分；托管微调/推理、数据迭代与网络困难。未观看伙伴视频。'),
 'ED28':('Stretch Brochure 2025','PDF第4–8页文本；矩形箱体、尺寸承重、5–45℃、7轴、输送机与产品规格。'),
 'ED29':('2023-01-31','DHL首次商业部署文章正文完整读取；1500万美元投资、输送机、落箱恢复与持续减少干预。'),
 'ED31':('DreamGen v305论文','PDF第6–8页真实任务、数据比例、表1和任务评分；九个真实任务及部分进度计分；未把全部表项视为严格整任务成功。'),
 'ED32':('2026-11-09 legal网页现行预订条款','预订/Order Invitation/接受订单/取消退款相关前部条款；未完整读取全部法律和隐私条款。'),
 'ECP01':('arXiv 2210.13702v2，2024-01-02','PDF第1、14–15页完整规范化文本；Allegro立方体旋转、ADR与手调对照、每组10次及严格10帧标准。'),
 'ECP02':('UR10e SW5.20，711-039-00','PDF第73–75及232–233页选定段；安全双通道I/O、门/光幕和重启条件。未通读242页。'),
 'ECP05':('Kroger 8-K 2025-11-18','web Item2.06 lines80–85、7.01/前瞻段；预计26亿美元减值原因。已保存web返回。')
}
irw={
 'IRW02':('2025年度20-F，2026发布','web lines1492/1521/1545、2170、2192–2215、2313–2340、2367–2435及经营财务相关find结果；2023–25收入成本费用、AOV、网络、自有品牌、成本分类。未通读全部20-F。'),
 'IRW03':('2026Q2，2026-08-20公告/08-21提交','SEC公告附件经click取得实际业绩正文；lines132–168、395–396、479–480、599等财务表脚注；国内终止经营、停折旧1.991亿、站点调整和条件交易。'),
 'IRW07':('2026-02-05港交所交易公告','PDF收购条件及业务范围相关段（第7–17页选读）；未把协议视为完成交割。'),
 'IRW09':('2022年度20-F，2023-08-03提交','web lines1867–1916、1953–2026、3652–3668及收入确认4210–4211；2021/22收入成本履约与2022-07关闭DMW。'),
 'IRW10':('2024-11-18','文章正文lines1–51完整阅读；深圳经营者转让非全部关仓、日单变化、人工房租排除、投流配送报价及平台未回应。'),
 'IRW11':('2024-12-11','南方周末/南方+正文lines17–84；广州白云、番禺、佛山案例，45万招商/35万库存等原话；未声称读取全部后部或核账。'),
 'IRW13':('永辉2025年度报告，2026-04-17','PDF第8–9页线上业务段及主要财务数据关键词段；线上100.9亿、56.6/44.3亿、349门店及全仓并列范围；未通读262页。'),
 'IRW14':('上海2025统计公报，2026-03-30','正文人口与人民生活lines112–118相关段；人口2485.41万、收入91987和消费54765。不推导商圈密度。'),
 'IRW15':('2023-05-23','报道正文完整阅读；成都/重庆App公告5月29日18时停止，报道时仍可下单，公司效率解释。'),
 'IRW17':('市场监管总局令124号，2026-05-20施行','官方web第1–29条取得并阅读；重点第10–12/18/22–25条，地址许可、保存3年、温控与责任。不是餐饮123号规定。'),
 'IRW18':('2024-02-26发布的指引','正文第2–14条；适用劳动关系范围、工作与等待准备时间、连续和每日上限的合理确定、报酬。'),
 'IRW22':('2026-10-27发行文件，2026-11-04披露URL','原件正文文本lines1699–1703 Dingdong收购协议subject to closing conditions；仅对交易状态选读，不声称完整债券文件阅读。'),
 'IRW23':('2023-11月20-F/A修订','web Explanatory Note lines198–205；修订Item16I和附件，不更新财务表。'),
 'IRW25':('深圳2025统计公报，2026发布','人口段line152，1824.85万/增加25.9万/城镇化99.79%；未将全市数推成具体仓可行性。'),
 'IRW28':('2026-05-19','正文lines102–130和后部续读，海淀/房山多位经营者、自述日单/补贴/库存/人力/仓店转换；15:30的286单是部分日不是日均。')
}
extra={'ECP05':{'id':'ECP05','url':'https://www.sec.gov/Archives/edgar/data/56873/000110465925113746/tm2531591d1_8k.htm','title':'Kroger 2025-11-18 8-K Item2.06'}}
webpaths={
 'ED06':'sources/ED06-web-access.json','ECP05':'sources/kroger-8k-web.txt',
 'IRW02':'sources/ddl-annual-web.txt','IRW03':'sources/ddl-q2-web.txt','IRW09':'sources/missfresh-and-amendment-web.txt','IRW23':'sources/missfresh-and-amendment-web.txt','IRW11':'sources/web-finance-2026-nf.txt','IRW17':'sources/regulations-web.txt','IRW18':'sources/regulations-web.txt'
}

def write_records(cid,scopes):
    O=R/'research'/cid/'codex-production'
    entries=json.loads((R/'research'/cid/'codex-inputs'/'sources.json').read_text(encoding='utf-8-sig'))
    index={x['id']:x for x in entries}
    if (O/'supplement-manifest.json').exists():index.update({x['id']:x for x in json.loads((O/'supplement-manifest.json').read_text(encoding='utf-8'))})
    index.update(extra)
    ledger=[]
    for sid,(version,scope) in scopes.items():
        obj=index[sid];base=(O/'sources'/sid) if sid.startswith('ECP') else R/'sources'/sid
        path=base/'original.txt'
        web=O/webpaths[sid] if sid in webpaths else None
        rec={'source_id':sid,'title':obj.get('title',''),'url':obj['url'],'source_version':version,'read_at':DATE,'reading_location':scope,'reader':READER,'original_text_path':str(path) if path.exists() else None,'web_note':str(web) if web and web.exists() else None,'scope_type':'selected_actual_reading','full_document_read':False}
        if path.exists():rec['original_text_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        if not rec['original_text_path'] and not rec['web_note']:rec['web_note']='实际web返回阅读；位置见reading_location，未另存原HTML，不宣称本地全文原件。'
        ledger.append(rec)
    (O/'reading-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
    with (O/'source-registry.csv').open('w',newline='',encoding='utf-8-sig') as f:
        cols=['source_id','title','url','source_version','original_text_path','web_note','reading_location','reader'];w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(ledger)
    note=['# 实际阅读记录',f'作者：`{READER}`；资料及读取截止：{DATE}。这里只登记实际读到的段落；下载、提取、搜索命中均不替代全文阅读。', '正文中的页码指物理PDF页，另注明印刷页时除外。论文固定到所列版本。网页视频未观看或未逐帧审计，未登记视频运行结论。', '|ID|版本|实际位置|','|---|---|---|']
    note += [f"|{x['source_id']}|{x['source_version']}|{x['reading_location']}|" for x in ledger]
    note += ['','未列的候选来源不等于已读。原始材料包中失败URL、仅摘要或下载后未用于判断的文件未升级为已核证据。经济模型全部输入显式列在计算脚本中；正文推断和情景由claims记录分别标明。','此记录是作者工作记录，不是独立评审通过证明。']
    (O/'reading-log.md').write_text('\n\n'.join(note),encoding='utf-8')
    return O,{x['source_id']:x for x in ledger}

def claims_write(O,registry,items,prefix):
    claims=[]
    for i,(kind,section,statement,sids,calc) in enumerate(items,1):
        claims.append({'claim_id':f'{prefix}-{i:03d}','claim_text':statement,'claim_type':kind,'report_section':section,'source_ids':sids,'source_urls':[registry[s]['url'] for s in sids],'evidence_locator':[{'source_id':s,'reading_location':registry[s]['reading_location']} for s in sids],'calculation_files':calc,'reader':READER,'report_file':str(O/'draft-final.md'),'review_status':'author_statement_pending_independent_review'})
    (O/'claims.jsonl').write_text('\n'.join(json.dumps(c,ensure_ascii=False) for c in claims)+'\n',encoding='utf-8')
    return len(claims)

EO,ER=write_records('embodied_deployment_zh',ed)
IO,IR=write_records('instant_retail_warehouses_zh',irw)
edclaims=[
 ('fact','一/四','F02公开累计9万余件、约1250小时和支持3万辆；84秒/37秒是任务要求、99%是目标，不是实际连续无干预统计。',['ED01','ED02'],[]),
 ('fact','四','BMW F03物流排序为2026-06新项目，不能继承F02钣金上料的累计成果当作同任务新一代成绩。',['ED03'],[]),
 ('fact','四','METEC案例依赖夹爪、机床I/O和缓存流程，翻倍产能同时包含夜间周末运行，公开资料未给完整ROI。',['ED04'],[]),
 ('fact','四','GXO已有RaaS商业服务并超过10万料箱；新增NC/TN部署预计2027，6.5万小时涵盖Agility各商业客户项目。',['ED06'],[]),
 ('fact','一/四','DHL已商业使用Stretch并扩展地区，1000余台为MOU未来安排；纸箱边界和最高吞吐不等于整班净吞吐。',['ED07','ED28','ED29'],[]),
 ('fact','四','OGRP应用中心数量扩大与部分Kroger/Sobeys履约中心关闭并存；客户财务不达预期不能单因归为抓取模型失败。',['ED08','ED09','ECP05'],[]),
 ('inference','四','Figure前臂故障与下一代结构改变说明系统可靠性进步需要区分模型、数据和硬件贡献。',['ED01'],[]),
 ('fact','二','DROID公开76k轨迹350小时564场景86任务等采集规模，并标明硬件和校准更新；数据量本身不代表全部任务覆盖。',['ED17'],[]),
 ('fact','二/五','π0.5在三处未见住宅及每任务环境10次试验评价任务进度，训练数据类型与消融结果需分别解读。',['ED16'],[]),
 ('fact','二/五','π0.7区分多步指令、跨本体及新任务指导；用过的评估数据与留出泛化评测应区分。',['ED19'],[]),
 ('fact','二/五','RECAP的吞吐及成功评价含具体超时和关键错误标准，汇总实验不证明普通家庭长期运营。',['ED18'],[]),
 ('fact','二','DreamGen部分任务评分含部分进度；SIMPLER为真实训练策略的模拟评估；DeXtreme为限定立方体任务的仿真到现实迁移。',['ED31','ED21','ECP01'],[]),
 ('fact','三','RTC真实480episodes和28小时是汇总纯执行；异步动作块解决部分延迟，不能取代本地控制和安全机制。',['ED22'],[]),
 ('fact','三','OSHA与UR具体手册要求从整套应用、安全I/O及恢复条件分析；低负载或规划避碰不等于应用安全已验证。',['ED23','ECP02'],[]),
 ('fact','三','Pi API beta提供托管微调推理，官方也披露网络连接问题，本地执行与恢复仍需工程处理。',['ED26'],[]),
 ('fact','四/五','NEO当前产品价格、基本自主和专家服务、预订与制造承诺分属不同阶段；本报告缺普通付费客户持续运行队列。',['ED12','ED13','ED32'],[]),
 ('scenario','六','受年需求17万次限制，工业柔性情景每次成本1.193元/年差额-1.73万；同边界专用情景0.573元/+8.80万，非品牌报价或真实ROI。',[],['economics.py','economics-results.json','economics-results.csv']),
 ('scenario','六','工业U从65%到85%因需求封顶几乎不再改善经济性；劳动节省兑现仅50%时差额约-11万元。',[],['economics.py','economics-results.json']),
 ('scenario','六','物流和家庭成本分别按不同任务计算，家庭499美元仅为已读订阅标价，其他参数全为假设。',['ED12'],['economics.py','economics-results.json']),
 ('inference','七','采用应先定义合格任务和需求，再比较专用及柔性方案，部署数据闭环需区分模型、硬件、集成和需求失败。',['ED01','ED04','ED06','ED08','ED16','ED22'],[])
]
irclaims=[
 ('inference','一','自营、社会化、加盟和门店履约须按库存、定价、费用和流量责任分别建账，不能用GMV或日单直接比较利润。',['IRW02','IRW10','IRW11'],[]),
 ('scenario','一','同一假设50元商品订单，仓固定成本前贡献6元、平台贡献0；内部补贴和费用不得重复算市场规模。',[],['warehouse-model.py','warehouse-results.json']),
 ('fact','二','每日优鲜2021净收入69.515亿、成本61.310亿、毛利约8.205亿小于21.214亿履约费用；2022-07关闭DMW。',['IRW09'],['financial-bridges.py','financial-bridges.json']),
 ('fact','二','2023年20-F/A修订境外检查披露及附件，明确未更新财务报表，不能误当上述数字被全面财务重述。',['IRW23'],[]),
 ('fact','二/三','成都重庆2023-05-23报道为5月29日18时停止服务公告，报道时仍可下单；2026Q2叮咚同时在华东加站和关闭其他城市低效站。',['IRW15','IRW03'],[]),
 ('fact','二','叮咚2025履约费率21.9%、销售成本率70.8%；营业和净利润低于2024，仓级盈利不能直接等于公司净利。',['IRW02'],[]),
 ('fact','二','叮咚2026Q2因国内停止折旧摊销增加净利润1.991亿；报告净利2.717亿机械扣除为0.726亿，非正式可比利润。',['IRW03'],['financial-bridges.py','financial-bridges.json']),
 ('fact','二','2026-02收购协议、8月待审批与10月发行文件条件状态均不证明已交割；终止经营会计分类不等于现实业务停止。',['IRW07','IRW03','IRW22'],[]),
 ('fact','二/三','深圳2024受访经营者订单下降及转让仓；其20%表述不含人工房租，非净利率。',['IRW10'],[]),
 ('fact','二/三','广州佛山采访显示住宅密度仍需选品和供货适配；45万投入35万库存是招商方案，不是已实现回本。',['IRW11'],[]),
 ('fact','二/三','北京2026采访显示部分受访仓订单回落、缩员或转仓店一体，属于自述；部分日286单不能转为日均。',['IRW28'],[]),
 ('inference','三','沪深统计仅支持城市背景，仓密度应由实际家庭、频次、份额与路网决定，不能从全国/全市均值直接推导。',['IRW14','IRW25'],['financial-bridges.py']),
 ('scenario','四','成熟自营900日单的仓级月利润73940元，分摊后25340元；社会化400日单利润12000元但库存298200元，均为假设。',[],['warehouse-model.py','warehouse-results.json']),
 ('scenario','四/五','社会化加入2%加盟费在400日单恰好盈亏平衡；基准单仓最小整数平衡334日单，自营分摊后697日单，均需通过产能需求条件。',[],['warehouse-model.py','warehouse-results.json']),
 ('scenario','五','订单增长会触发固定费用阶梯；降价促销联合情景使生鲜日单增长20%而分摊后亏7.73万元。',[],['warehouse-model.py','warehouse-results.json']),
 ('scenario','五','峰时900日单生鲜需至少6名同时拣货和约32名并发运力，社会化2名拣货仅81单/小时，均非全天编制标准。',[],['warehouse-model.py','warehouse-results.json','financial-bridges.json']),
 ('scenario','六','新增500日单仓中300单为原仓分流时，网络净增200日单而月利润较原网络下降90480元。',[],['warehouse-model.py','warehouse-results.json']),
 ('scenario','六','新区域六个月爬坡到950日单仍亏，累计现金缺口约104.9万元，非全生命周期峰值或回本期。',[],['warehouse-model.py','warehouse-results.json']),
 ('fact','六','永辉2025线上100.9亿含自营及第三方、门店及全仓，不能都视为门店拣货或将集团亏损归为线上。',['IRW13'],[]),
 ('scenario','六','门店线上增量结果与全额分摊结果可相反；例子200日单增量利润1.3万而完整分摊-2.7万。',[],['financial-bridges.py','financial-bridges.json']),
 ('fact','七','124号网络食品销售规定2026-05-20施行，地址许可、信息留存和温控委托监督责任进入实际成本。',['IRW17'],[]),
 ('fact','七','新就业指引区分关系与适用范围、工作和必要准备等待时间，不是统一允许12小时连续工作的规则。',['IRW18'],[]),
 ('inference','八','成熟城区扩张要看净增利润及服务容量，新区域要验证正常价格复购和爬坡资金；改品类、合仓、门店和退出是条件性选择。',['IRW03','IRW10','IRW11','IRW15','IRW28'],['warehouse-results.json'])
]
counts={};counts['embodied_deployment_zh']={'read_sources':len(ER),'claims':claims_write(EO,ER,edclaims,'EDC')};counts['instant_retail_warehouses_zh']={'read_sources':len(IR),'claims':claims_write(IO,IR,irclaims,'IRWC')}

# Microdrama: transcribe only explicit read rows in existing human ledger, not all registered sources.
MO=R/'research'/'microdrama_market_zh'/'codex-production'
with (MO/'source-locations.csv').open(encoding='utf-8-sig') as f:mi={x['id']:x for x in csv.DictReader(f)}
excluded={'MD001','MD002','MD007','MDX003','CP06'}
ml=[]
for line in (MO/'reading-log.md').read_text(encoding='utf-8').splitlines():
    parts=[p.strip() for p in line.split('|')]
    if len(parts)<5 or not re.fullmatch(r'(?:MD\d+|MDX\d+|CP\d+)',parts[1]):continue
    sid=parts[1]
    if sid in excluded:continue
    obj=mi[sid];directory=Path(obj['local_directory']);path=directory/'original.txt'
    web=next((p for p in [directory/'web-access.txt',directory/'web-access.json'] if p.exists()),None)
    ml.append({'source_id':sid,'title':obj['title'],'url':obj['source_url'],'source_version':'版本及日期见既有reading-log.md的对应行，原读取时保存','original_text_path':str(path) if path.exists() else None,'web_note':str(web) if web else ('仅既有阅读笔记；实际web读取范围和失败情况见reading_location' if not path.exists() else None),'reading_location':parts[2]+'；'+parts[3],'reader':READER,'read_at':DATE,'record_origin':'仅转存既有reading-log.md真实阅读，不重读或补形式'})
(MO/'reading-ledger.json').write_text(json.dumps(ml,ensure_ascii=False,indent=2),encoding='utf-8')
MR={x['source_id']:x for x in ml}
mc=[
 ('inference','一','终端内容消费和外部广告支出、企业收入、产业内中间交易分层；充值未消耗、退款和投流不能简单相加。',['MD004','MD012','MD005'],[]),
 ('fact','一','1210/570亿元属于2026全年预测语境，220亿元为半年转引估计；AI/真人/整体集合仍未充分披露。',['MD005'],[]),
 ('fact','一','各公开市场估计在流水/产值/收入及预测时点上不一致，不取平均生成统一实际市场序列。',['MD006','MD009','MD010','MD012'],[]),
 ('fact','二','CNNIC2024/2025末6.62/6.64亿相对可比，微小差值不构成已证统计显著增长；应用端MAU另有分母。',['CP19','CP08'],[]),
 ('fact','二','QM2026-05三类应用端去重8.51亿不含另列主版触达4.72亿；2026-09 App MAU4.87亿。',['CP24','CP16'],[]),
 ('fact','二','QM2月App和小程序样本门槛及回看方式不同，跨期比较须保留产品集合变化。',['CP17'],[]),
 ('inference','二','26.9小时/125.6次与13小时/62次相除，每次约12.9/12.6分钟，时长增量主要表现为频次而非单次明显延长。',['CP24'],[]),
 ('fact','二','CSM观看付费内容、未来意愿不是实际自费转化，18岁以上网民调查与CNNIC总体不同。',['MD003'],[]),
 ('fact','三','红果4月宣布内容基金与10月取消金币是不同事件；无成熟后测队列证明取消激励已提高长期利润。',['MD013','MD014'],[]),
 ('fact','三','抖音方案支付分佣1%–29%、0–3日自动发起和T+7各有适用对象，不能混成单一短剧收费或付款规则。',['CP18','CP27'],[]),
 ('fact','三','快手短剧供给和投放消耗披露支持营销服务需求，不等于片方利润或可直接相加的终端市场。',['CP20'],[]),
 ('inference','四','承制、保底、纯分账与自营按合同承担不同商业化风险，IP价值须看保留权利而非题材标签。',['MD006','MD009','CP26'],[]),
 ('fact','五','中文在线与掌阅集团财务、分部范围、营销投入和现金差异不能用作纯境内短剧行业平均利润。',['CP12','CP13','CP14','MD005','MD008'],['financial-calculations.py','financial-results.json']),
 ('fact','五','2026Q3和累计财报必须区分，集团利润与经营现金受营运资金和业务范围影响。',['CP01','CP02'],['financial-calculations.py','financial-results.json']),
 ('scenario','六','付费基准合计贡献20.32万元而内容方-4.94万元；免费基准合计63.68万而应用经营者仅6.89万，均为显式假设。',[],['scenario-model.py','scenario-results.json']),
 ('scenario','六','分成改变分配不直接增加合计盈余，留存/完播/获客/广告价格须按队列和合同评估。',[],['scenario-model.py','scenario-results.json','completion-sensitivity.py','completion-results.json']),
 ('scenario','六','7/30/60日回款延迟造成不同垫资，最终项目盈利不能消除过程中现金缺口。',[],['scenario-model.py','cashflow-free-7days.csv','cashflow-free-30days.csv','cashflow-free-60days.csv','cashflow-paid-7days.csv','cashflow-paid-30days.csv','cashflow-paid-60days.csv']),
 ('fact','七','2026管理办法和分类规则按生效时间、真人/AI门槛及平台责任分别处理，审核周期影响交付和资金。',['MD004','CP04','CP09','CP21'],[]),
 ('fact','七','自动续费、退款、未成年人及盗版权利链会影响最终可收金额；法院案例介绍不当作已读判决全文。',['CP10','CP11','CP22','CP18'],[]),
 ('inference','八','平台按净LTV、制作发行按合同与资金能力、投资者按真实业务和现金范围选择进入位置。',['MD006','MD005','MD008','CP12','CP14','CP16','CP18'],['scenario-results.json'])
]
counts['microdrama_market_zh']={'read_sources':len(MR),'claims':claims_write(MO,MR,mc,'MDC')}

for cid,O in [('embodied_deployment_zh',EO),('instant_retail_warehouses_zh',IO)]:
    draft=O/'draft-final.md';first=O/'draft-final.first-complete.md'
    if not first.exists():first.write_bytes(draft.read_bytes())
    counts[cid]['draft_characters']=len(draft.read_text(encoding='utf-8'))
    counts[cid]['draft_lines']=len(draft.read_text(encoding='utf-8').splitlines())
    counts[cid]['draft_sha256']=hashlib.sha256(draft.read_bytes()).hexdigest()
    record={'case_id':cid,'author':READER,'author_draft_status':'complete_author_draft','independent_review_status':'not_performed_by_author','cutoff':DATE,'report':str(draft),'first_complete_snapshot':str(first),'reading_ledger':str(O/'reading-ledger.json'),'claims':str(O/'claims.jsonl'),'counts':counts[cid]}
    (O/'full-response.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    calculations='economics.py、economics-results.json/csv' if cid.startswith('embodied') else 'warehouse-model.py、warehouse-results.json/csv；financial-bridges.py/json'
    hand=f'''# 完整作者稿交接

任务：{cid}；作者：`{READER}`；资料截止：{DATE}。

完整当前稿为`draft-final.md`，首次完整稿已封存`draft-final.first-complete.md`，不得覆盖首稿。两者现在均完整。提纲已由协调任务安排独立requirements及structure_and_depth通过，该状态只覆盖提纲，未表述为全文通过。

正文、全部重要矩阵、图示、正反证及经济模型已落盘。实际阅读位置和版本见`reading-log.md`及`reading-ledger.json`；`source-registry.csv`只列实际已读来源，`claims.jsonl`区分事实、作者推断和情景。计算原件：{calculations}。原始包位于`implementation/sources`，新增原件和web返回在本目录`sources`。

作者只执行来源阅读、研究算术及组稿，没有调用已耗尽额度的Astra API，没有运行软件测试、修改产品或自我独立批准。独立7视角、领域审查、audit及acceptance由root另行安排。所有未披露的部署分母、商家未经审计口述和情景输入已在影响判断处说明；没有把下载文件或规划记录冒充全文阅读和实证。

字符数：{counts[cid]['draft_characters']}；行数：{counts[cid]['draft_lines']}；实际来源：{counts[cid]['read_sources']}；主要claims：{counts[cid]['claims']}。这些数量仅供交接定位，不代表研究质量通过。
'''
    (O/'production-handoff.md').write_text(hand,encoding='utf-8')
print(json.dumps(counts,ensure_ascii=False,indent=2))
