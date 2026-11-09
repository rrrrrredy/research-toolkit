# Research brief

## question

研究在推理阶段增加计算如何改变推理模型与Agent的能力、可靠性和任务经济性，帮助系统设计者决定采用什么方法、如何分配有限预算，以及何时不应继续增加计算。仅使用long_research_test_time_compute中本题指定的冻结证据，与test_time_compute_en共用材料；不通过联网检索扩大事实范围，也不把英文报告本身当作新增来源。资料截止日为2026-11-09，重点考察2022年至该日公开的工作，材料支持时可追溯更早基础。保留论文、模型、实现和评测版本，不把截止日之后的信息当作当时已知证据。

按机制比较独立采样、自一致性、best-of-N候选选择、顺序修订、中间状态搜索、结果验证与过程反馈、自适应预算分配，以及包含工具或环境反馈的Agent循环。解释候选由谁生成、怎样筛选或淘汰、保留哪些状态、评价器能看到什么信息。区分推理时预算分配与使这些方法有效的训练变化，将固定基础模型上的比较与同时更换模型规模、后训练、数据或验证器的比较分开。

从数学推理、可执行代码任务和多步骤工具任务中选择有解释力的研究，分析随计算增加的收益、边际变化、饱和、退化及任务难度差异，而不是罗列论文。解释相关性错误、较弱或校准不良的验证器、对奖励的投机、工具不可靠、连续动作误差累积和反馈缺失如何影响结果。特别比较具有廉价可靠验证条件的任务与结果含糊、反馈延迟的任务，说明前者的收益是否有证据可以迁移到后者。

建立预算可比较的分析框架，纳入候选生成、被丢弃分支、验证器调用、已披露的隐藏或显式推理token、工具执行和重试。区分总计算或货币成本、串行延迟、并行资源需求与端到端耗时；不同模型的token数不能直接当作统一计算单位。公开结果足以支持换算时展示单位和假设，否则保留分组比较并说明缺失信息。给出一个使用已披露参数或明确假设的预算分配算例，不将说明性计算写成新实验。

交付完整研究报告，包含方法与证据矩阵、已报告扩展行为的比较，以及围绕任务可验证性、错误后果、延迟约束、工具条件和预算形成的设计决策树。解释何时应选择更强基础模型、更多采样、更深搜索、更好验证器或更简单的执行路径。区分已观察到的结果与提出的设计策略，保留不增加推理计算也更合理的情形。面向中文技术读者自然解释概念和因果关系，图表可嵌入任何连贯结构，不强制章节名称；文献清单或一页建议不能替代完整论证。

本题重点核验候选筛选成本是否计入预算、训练变化与推理变化是否可区分，以及设计选择是否有对应任务证据。基准污染、试题筛选、评价器泄漏和缺失的不确定性估计若影响结论，应具体说明。可以分析公开报告和已有复现，但没有实际独立复现就不能声称复现成功。中文稿可重新组织和解释共享证据，不要求沿用英文稿结论；冻结材料不足时说明具体缺口及其影响，不用未支持的事实补齐。任何扩展规律或推理时计算必然优越的结论都不预设。

## audience

需要分配推理计算预算的模型研究者、推理工程师和Agent系统设计者

## scope

Follow the task geography, comparison scope and evidence cutoff of 2026-11-09. Each other-language version uses its frozen sources without seeing the first-language report.

## output

Complete long-form research report final.md with the task-specific comparisons, explanations, tables and locatable citations. Preserve the first draft and actual independent results.

## depth

完整技术长研究报告，贯通方法机制、计算预算对齐、扩展收益与失败条件，并形成适用于推理和Agent工作负载的设计依据。

## evidence_standard

Use only the same-question frozen source materials; write independently without viewing the other-language answer. Conduct seven separate independent perspectives, domain review, audit and acceptance.
