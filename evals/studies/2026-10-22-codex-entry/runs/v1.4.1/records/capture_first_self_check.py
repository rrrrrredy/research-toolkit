import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
task = root / 'tasks/codex-architecture-zh-20261022'
raw = (task/'final.md').read_bytes()
text = raw.decode('utf-8')
body = re.sub(r'^# .*\n+', '', text.split('**参考文献**')[0])
body = re.sub(r'〔[^〕]*〕', '', body)
body = re.sub(r'表据S1：.*?L75–109。', '', body)
body = re.sub(r'(?m)^\|[\s|:-]+\|\s*$', '', body)
body = re.sub(r'[`*|]', '', body)
counts = {'body_han_characters': len(re.findall(r'[\u4e00-\u9fff]',body)),
    'body_alphanumeric_tokens':len(re.findall(r'[A-Za-z0-9]+(?:[.\-/][A-Za-z0-9]+)*',body)),
    'body_visible_nonwhitespace_characters':len(re.sub(r'\s','',body)),
    'scope':'正文含比较表、表后解释及证据限制；排除标题、文献、引用定位和Markdown标记。约2000字为软约定，不转成全文硬范围。',
    'artifact_sha256':hashlib.sha256(raw).hexdigest()}
with (task/'checks/first-body-count.json').open('x',encoding='utf-8') as f:
    json.dump(counts,f,ensure_ascii=False,indent=2)
    f.write('\n')
items = {
  'requirements': {'passed':True,'evidence':f'通读first-self-check-report.md全文。第3–13行覆盖组件、任务、技能与接续，第15–27行及五行比较表区分本地与托管责任，第29行讨论成本；六来源文献另列。正文实测{counts["body_visible_nonwhitespace_characters"]}个可见非空白字符，其中{counts["body_han_characters"]}汉字、{counts["body_alphanumeric_tokens"]}个英文/数字词段，含表，不含标题/文献/引用标记；符合约2000字软目标，无硬性最低。首次报告已在稿件检查前冻结，未改原件。'},
  'claims_and_sources': {'passed':False,'evidence':'核对S1 L7–49的Harness分工，S2 L194–209、L1360–1459的生命周期，S3 L33–48的目录预算，S4 L59–74、L246–357的权限，S5 L7–9/L162的案例条件及S6 L5–109的环境责任，主要解释与原文一致。具体问题：报告第11行“恢复或分叉thread”的直接定位应补S2 L194–209；首次check-draft同时发现来源read_evidence混入路径后说明，工具无法正确定位，需把说明移入locator。修正前本项不通过。'},
  'counterevidence': {'passed':True,'evidence':'第11行用thread/revert不改文件反驳“会话恢复等于成果恢复”；第13行保留完全访问、旧模型、非生产就绪并拒绝外推；第25行说明托管会话仍会等待函数结果；第27行区分命令禁网与其他连接；这些限制分别落在相关判断中。'},
  'sections': {'passed':True,'evidence':'逐段核对：第3行为职责；第5–7行为执行反馈与客户端状态；第9行为方法加载的成本与发现取舍；第11–13行为状态与长任务；第15–25行为部署选择；第27–31行为权限、产品建议与证据限制。各段有不同问题和解释，没有重复段充篇幅。'},
  'reader_edit': {'passed':True,'evidence':'通读第1–42行，示例以修复缺陷串起执行流程，表格按同一“职责/产品含义”维度比较；未发现离题的竞争产品、安装教程或战略史。正文无研究执行日志或checklist。无需删除填充段；引用定位问题单列claims_and_sources，未在自检前悄悄修改。'},
  'limitations': {'passed':False,'evidence':'第13、31行已说明历史个例、非生产就绪、未实测、没有可比成本/可靠率及闭源实现证据；参考文献说明快照日期。但当前尚无交付说明明确声明“仅作者自检，未经独立评审”。应在与正文分开的revision-notes.md和交付说明中补充。'}
}
for folder in (task,root):
    with (folder/'first-self-check.json').open('x',encoding='utf-8') as f:
        json.dump(items,f,ensure_ascii=False,indent=2)
        f.write('\n')
    with (folder/'first-self-check-report.md').open('xb') as f:
        f.write(raw)
sources = []
for n in range(1,7):
    source_id = f'S{n}'
    source_text = (task/f'sources/{source_id}.md').read_text(encoding='utf-8')
    nums = [int(v) for v in re.findall(r'^L(\d+):',source_text,re.M)]
    spans = []
    start = end = nums[0]
    for number in nums[1:]:
        if number == end+1:
            end = number
        else:
            spans.append(f'L{start}–{end}')
            start = end = number
    spans.append(f'L{start}–{end}')
    sources.append({'source_id':source_id,'read_evidence':f'sources/{source_id}.md',
        'locator':'2026-10-22快照；实际已读全部所给摘录：'+ '、'.join(spans)+'。省略内容、图片和外链未读。'})
request = {'task':'codex-architecture-zh-20261022','sources':sources}
with (root/'records/toolkit-calls/06-fix-locators.request.json').open('x',encoding='utf-8') as f:
    json.dump(request,f,ensure_ascii=False,indent=2)
    f.write('\n')
print(json.dumps(counts,ensure_ascii=False,indent=2))
print('First self-check saved: claims_and_sources=false; limitations=false. Complete associated report preserved unchanged.')
