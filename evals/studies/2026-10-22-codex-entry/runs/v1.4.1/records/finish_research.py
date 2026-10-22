import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
task = root/'tasks/codex-architecture-zh-20261022'
checklist = {
 'requirements': {'passed':True,'evidence':'通读final.md第3–31行，任务循环、各组件、技能、接续与长任务、部署和权限均覆盖，表格比较五种使用组合，六项参考文献另列。正文2139个可见非空白字符（1610汉字及63英文/数字词段），含表不含标题/文献/引用定位，约2000字无硬性最低。首次产物、终稿及修订说明均保存，具体计数和核对见checks/final-author-check.md。'},
 'claims_and_sources': {'passed':True,'evidence':'逐项核对S1 Harness与入口、S2生命周期和状态、S3渐进披露、S4权限、S5历史实验与S6托管/环境职责。第11行已补S2 L194–209，直接支持恢复/分叉；来源本地证据路径与locator现已分离。修正后的check-draft返回ok=true且无errors。正文明确区分文档事实、来源作者的案例结果与本文分析，未据工具状态推定内容正确。'},
 'counterevidence': {'passed':True,'evidence':'复核第11行：撤回历史不改文件且压缩无无损保证；第13行：旧模型、完全访问的历史实验未生产就绪且不外推；第25行：托管Harness仍会等待函数处理器；第27行：本地命令禁网不覆盖MCP/模型/搜索。限制均嵌入相应结论。'},
 'sections': {'passed':True,'evidence':'全文分别解释职责（第3行）、执行与界面（第5–7行）、方法加载（第9行）、接续/长任务（第11–13行）、部署比较（第15–25行）、权限与成本（第27–29行）和限制（第31行）。表格使用统一责任/产品含义维度，各段不是同义重复。'},
 'reader_edit': {'passed':True,'evidence':'重新通读当前报告第1–42行及交付说明，示例从修复缺陷进入闭环，比较表可用于选型，末段不夸大证据。没有离题扩展、套话填充、重复段落或正文生产记录。实际正文修改仅补一处必要引用定位，保留原有解释与分析；修订和统计说明另置revision-notes.md。'},
 'limitations': {'passed':True,'evidence':'第13行交代案例模型、权限和非生产结论；第31行说明只有官方摘录、未经性能实测、缺可比成本/可靠率和闭源实现证据。revision-notes.md首段和拟交付说明现明确“仅作者自检，未经独立评审”，解决首次自检缺项。'}
}
for item in checklist.values():
    item['evidence_files']=['checks/final-author-check.md','revision-notes.md']
with (task/'author-self-check.json').open('x',encoding='utf-8') as f:
    json.dump(checklist,f,ensure_ascii=False,indent=2)
    f.write('\n')
for name in ('final.md','revision-notes.md'):
    with (root/name).open('xb') as f:
        f.write((task/name).read_bytes())
request = json.loads((root/'records/toolkit-calls/09-finish-template.request.json').read_text(encoding='utf-8'))
request['checklist'] = checklist
with (root/'records/toolkit-calls/10-finish.request.json').open('x',encoding='utf-8') as f:
    json.dump(request,f,ensure_ascii=False,indent=2)
    f.write('\n')
