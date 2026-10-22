"""Preserve the first actual author self-check and prepare the completion request."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
task = root / 'tasks/codex-architecture-zh-20261022'
checklist = {
 'requirements': {
   'passed': True,
   'evidence': '已通读 final.md 全文并逐项对照 brief。第5–11行解释五层角色和单次任务；第15–23行职责表区分 CLI/SDK、本地 app-server 与三种托管环境配置；第25–31行覆盖技能、权限、跨轮接续及长任务；第33行给出选择与成本判断。按正文口径实测：含日期和表格，排除主标题、参考文献、引注编号及 Markdown 标记，2171个非空字符，其中1621个汉字、66个拉丁／数字词项；没有把全文3221字符当作正文。约2000字无硬性下限，覆盖充分且没有为长度填充。首次稿在06-check-draft之前由04-register-first-draft登记；首次自检与全文一并保存。',
   'evidence_files': ['notes/first-length-count.json']
 },
 'claims_and_sources': {
   'passed': True,
   'evidence': '已将现稿重要判断对应到已读原文：第5行开放边界与第17–18行入口对应S1 L7–49；第9–11行Thread/Turn/Item、生命周期与终态对应S2 L194–209、L1360–1361、L1429–1445；第19–23行环境与应用责任对应S6 L9–31、L52–54、L77–109；第25行技能加载与显式注入对应S3 L33–48、L93–103及S2 L1514；第27行权限及自动审批对应S4 L59–74、L246–263、L318–357；第29行历史与文件分离对应S2 L474–488、L876–878；第31行实验条件、25小时/13M token/30k行及非生产就绪对应S5 L7–9、L79–83、L162。六个文献网址与目录一致，正文引注[1]–[6]均有对应文献；数字仅作来源报告，未计算无依据价格或成功率。'
 },
 'counterevidence': {
   'passed': True,
   'evidence': '已核对限制是否实质约束结论：第23行以函数处理器不可用导致等待反驳“托管即免除可靠性责任”；第25行保留技能目录可能遗漏条目；第27行区分命令禁网与其他连接、Legacy与当前Cloud；第29行用thread/revert不改文件反驳“恢复对话即恢复工作区”；第31行保留完整访问权限和非生产就绪，并明确不能隔离项目记忆等措施的因果贡献或推广至所有版本。第33行没有凭运行规模判断成本胜负。'
 },
 'sections': {
   'passed': True,
   'evidence': '按论证单元检查全文：开篇解释组件如何分工；单次任务用具体修复请求串起输入、循环、审批、事件和终态；表格用一致的执行位置与应用责任维度比较入口；技能段解释初始占用与发现不确定性的交换；权限段连接边界、等待和审批用量；接续段区分三类状态，长任务段解释反馈及持久工件；末段给出按任务选择环境和成本组成。各段均承担不同问题，没有重复段落或背景堆叠。'
 },
 'reader_edit': {
   'passed': True,
   'evidence': '已通读第1–44行完整稿。Harness、Thread、Turn、Item均在首次出现时说明；仅保留有解释作用的少量接口名，未附安装命令或配置教程。职责表能帮助读者选择接入方式，表前标明适用判断为设计分析；引用是读者可追溯的六条公开文献，正文没有S/C/R内部编号、本地路径、检查状态或任务过程。没有竞争产品大全、战略史、长引文、跨任务模板或重复填充。未发现必须进行的正文修正，保留原稿，不为产生修订而改写。'
 },
 'limitations': {
   'passed': True,
   'evidence': '已核对第27行自动审批无延迟/误判率证据，第29行压缩细节不明，第31行历史实验条件和推广限制，第33行无可比账单或成功率，第37行厂商文档/案例不构成独立跨版本性能验证。未声称了解闭源模型或托管服务内部算法。revision-notes.md及拟交付说明集中披露“完成作者自检，未经独立评审”；没有以Lite工具状态认证研究语义质量。',
   'evidence_files': ['revision-notes.md']
 }
}

notes = '''# 修订说明

首份完整报告在第一次稿件检查和作者自检之前保存为 `first-draft.md`；首次六项自检及对应完整正文分别保存在 `first-self-check.json` 和 `first-self-check-report.md`，均以拒绝覆盖的方式创建。

一次正常稿件检查未发现记录错误。作者对照原文、任务要求与完整正文核对后，未发现需要修正的具体问题，因此未进行正文修订；`final.md` 与首稿保持相同。正文口径为含日期、表格，排除主标题、参考文献、引注编号和 Markdown 标记：2171个非空字符（其中1621个汉字、66个拉丁／数字词项），接近约2000字目标；全文计数不作为正文长度。

本次采用 Research Toolkit Lite，完成作者自检，未经独立评审；未启动其他 Agent 或测试套件，也未追加网络检索。`finish` 首次返回的七项 pending 是尚未提交作者完成结论的要求记录，随后依据实际核对更新，不代表正文被工具判定合格。

来源与主张在任务的 `data/`，研究分析与计数在 `notes/`；真实 Toolkit 请求、命令、原始返回、stderr 与退出码在工作区 `research-records/toolkit-calls/`。这些过程材料与正文分开保存。
'''
with (task/'revision-notes.md').open('x', encoding='utf-8') as f:
    f.write(notes)
report = (task/'final.md').read_bytes()
with (task/'first-self-check-report.md').open('xb') as f:
    f.write(report)
with (task/'first-self-check.json').open('x', encoding='utf-8') as f:
    json.dump(checklist,f,ensure_ascii=False,indent=2)
    f.write('\n')

resolved = [
 ('R1','final.md第5–11行：角色、请求与工具反馈循环、审批、事件及终态。'),
 ('R2','final.md第15–23行：五行比较表与托管/自有责任说明。'),
 ('R3','final.md第25–31行：按需技能、历史压缩、线程恢复与文件状态、长任务项目记忆。'),
 ('R4','final.md第23–33行：工具处理故障、发现代价、授权用量、验收与成本组成及限制。'),
 ('R5','notes/first-length-count.json：正文2171个非空字符（1621汉字、66拉丁/数字词项）；不含主标题和参考文献，无硬性最低字数。'),
 ('R6','data/source_registry.csv登记六份给定摘录实际已读位置；first-self-check.json claims_and_sources项记录逐项原文核对；正文文献1–6给出网址和原文定位。'),
 ('R7','first-draft.md于首次检查前保存；first-self-check.json与first-self-check-report.md已同时冻结；revision-notes.md说明未发现必改问题且未改稿；真实请求与返回在research-records/toolkit-calls。')
]
save = {'task':'codex-architecture-zh-20261022','requirements':[{'requirement_id':rid,'status':'satisfied','evidence':evidence} for rid,evidence in resolved]}
(root/'research-records/save-completion.json').write_text(json.dumps(save,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
finish = json.loads((root/'research-records/finish-template.json').read_text(encoding='utf-8'))
finish['checklist'] = checklist
(root/'research-records/finish.json').write_text(json.dumps(finish,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('First author self-check and its full report preserved; completion requests prepared.')
