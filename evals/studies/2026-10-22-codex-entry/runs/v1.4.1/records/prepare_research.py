import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent
task = root / "tasks/codex-architecture-zh-20261022"
(task / "sources").mkdir(exist_ok=True)
catalog = json.loads((root / "inputs/sources.json").read_text(encoding="utf-8"))
sources = []
for item in catalog:
    shutil.copyfile(root / "inputs" / item["path"], task / item["path"])
    sources.append({"source_id": item["source_id"], "title": item["title"],
        "url": item["url"], "source_type": "primary", "read_scope": "relevant_sections",
        "read_evidence": item["path"] + "；已阅读给定快照全部所存段落，原文L行号定位，实际范围以文件提供内容为准。省略内容和外链未读；快照日期2026-10-22。",
        "evidence_path": item["path"]})
claim_data = [
    ("C1", "开源Harness提供状态、工具循环、流式执行和权限边界；模型访问与托管服务另属其他层。", "fact", ["S1"], "S1 L7–37；不代表模型权重或托管实现公开。"),
    ("C2", "app-server以thread/turn/item组织交互，支持开始、恢复、分叉、引导和中断，通过事件返回状态。", "fact", ["S2"], "S2 L194–209、L1085–1125、L1358–1399；completed不认证业务正确性。"),
    ("C3", "技能先提供名称描述路径，选中再加载全文；目录预算可能截短描述或省略技能。", "fact", ["S3","S2"], "S3 L33–48、L91–103；S2 L1512–1514。目录预算不约束被选中全文。"),
    ("C4", "跨轮接续涉及持久历史、有限模型上下文和外部产物；恢复或压缩历史不等于文件回滚或无损记忆。", "analysis", ["S2","S5"], "S2 L474–488、L874–878及S5 L56–83的综合推断；压缩细节与无损性未证明。"),
    ("C5", "GPT-5.3-Codex Extra High在空仓库、完全访问条件下约运行25小时、13M tokens并生成30k行代码，是来源作者报告的非生产实验。", "source_report", ["S5"], "S5 L7–9、L79–83、L162、L177–185；不能推断所有版本成功率或费用，无法分离模型、Harness、提示和验证的因果贡献。"),
    ("C6", "Agents API由OpenAI托管Harness，可无执行环境、托管执行环境或自备执行环境；应用仍需维护函数工具与自备环境生命周期。", "fact", ["S6"], "S6 L5–31、L50–54、L75–109；自备环境不意味着Harness自托管，函数处理器不可用会阻塞。"),
    ("C7", "沙箱限制技术能力，审批决定何时放行；本地命令网络限制不覆盖模型请求、MCP、搜索等所有连接。", "fact", ["S4"], "S4 L59–74、L246–265、L300–306；不能把本地默认或Legacy云配置推广至所有形态。"),
    ("C8", "自动审批可减少人工中断，却增加模型调用；只审已需审批的合资格动作，超时或审查失败时仍不执行。", "analysis", ["S4"], "S4 L318–357；减少人工中断是机制推断，无延迟、费用或误判率测量。"),
    ("C9", "按交互、文件计算和私网需求分配Harness及环境责任；总成本要考虑模型、计算、应用运维和修复。", "analysis", ["S1","S4","S5","S6"], "S1 L39–49、S4 L356、S5 L7、S6 L75–109的作者建议，缺可比价格与成功率数据。")
]
claims = [{"claim_id":i,"claim":c,"claim_type":t,"supporting_sources":s,"uncertainty":u} for i,c,t,s,u in claim_data]
claims[4]["counter_evidence"] = "S5 L9、L162明确不是生产部署/生产就绪。"
requirements = [
    {"requirement_id":"R1","summary":"解释一次任务及各组件配合，覆盖跨轮与长任务。","status":"pending"},
    {"requirement_id":"R2","summary":"区分本地app-server、CLI/SDK与托管服务；比较能力、成本和体验，含有用比较表。","status":"pending"},
    {"requirement_id":"R3","summary":"仅用给定S1—S6，重要判断按原始行号追溯，区分文档、历史案例与推断。","status":"pending","required_source_ids":["S1","S2","S3","S4","S5","S6"],"read_scope":"relevant_sections"},
    {"requirement_id":"R4","summary":"中文Markdown正文约2000字，无硬性下限；参考文献另列。作者按正文实测，不登记whole_artifact硬范围。","status":"pending"},
    {"requirement_id":"R5","summary":"UTF-8，保留检查前first-draft.md和首次自检及对应全文，不覆盖；交付final.md、revision-notes.md，保留Toolkit实际请求返回，记录与正文分开。","status":"pending"},
    {"requirement_id":"R6","summary":"Lite正常自检，不联网、不读越界材料、不启动其他Agent/独立评审/测试套件、不改toolkit或inputs；完成即结束。","status":"pending"}
]
request = {"task":"codex-architecture-zh-20261022","sources":sources,"claims":claims,"requirements":requirements}
with (root / "records/toolkit-calls/02-evidence.request.json").open("x", encoding="utf-8") as stream:
    json.dump(request, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
with (task / "state/task_spec.md").open("a", encoding="utf-8") as stream:
    stream.write("\n## 写作提纲与篇幅口径\n\n一次任务的闭环→上下文与技能加载→跨轮和长任务→本地/托管责任比较表→权限和成本取舍。正文约2000字、无硬性最低/最高，参考文献另列；按正文单独计数，不转成全文约束。\n")
