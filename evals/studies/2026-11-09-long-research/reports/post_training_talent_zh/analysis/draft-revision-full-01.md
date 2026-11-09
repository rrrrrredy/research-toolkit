# 全球模型后训练人才Mapping：能力组合、团队演化与公开协作网络

资料截止：2026年11月9日。面向模型研发组织与人才战略团队。本文依据公开论文、项目职责、机构页面与本人职业资料建立代表性图谱，没有开展模型实验，没有收集私人联系方式或推测个人招聘意愿。

后训练组织的能力不能用一组算法作者名单概括。2022年以来，公开成果显示至少四种需要共同工作的能力：把用户目标转成可训练反馈，构造能揭露失败的数据与评价器，把优化过程稳定运行在计算资源上，以及让模型在实际环境中完成多步任务。人才布局应首先识别这些环节由谁承担、怎样相互校验，再决定补充哪些研究专长。

本报告的人物记录支持两类具体用途：寻找已经公开展示过某种方法或工程能力的合作对象；识别现有组织缺少的能力组合。它不提供全球人才数量估计或个人优劣排名。公开论文更密集的团队更容易被观察，商业团队内部职责、未发表工程成果和未公开流动可能被低估。某方向缺少可核实个人信息时，本文保留团队级节点，不用论文单位填造当前员工名单。

## 一、能力边界：后训练工作如何相互依赖

强化学习、偏好优化、奖励建模、数据、推理和Agent训练具有交叉，但不能合并为一种技能。一个能够设计偏好损失的研究者，未必独立负责过多机rollout系统；一个维护训练系统的人，也不能仅因参与论文被认定为奖励建模负责人。

| 能力 | 需要解决的问题 | 可观察产物 | 最容易遗漏的组织依赖 |
|---|---|---|---|
| 强化学习与偏好优化 | 反馈如何变成稳定、可控的策略更新；离线偏好与在线采样如何匹配 | 目标推导、算法实现、训练消融、泛化与稳定性分析 | 数据覆盖、参考模型、奖励可靠性、采样成本 |
| 奖励模型与评价器 | 什么回答或行动算好，评价在策略变化后是否可靠 | 奖励训练数据、判别器、可执行验证器、独立评测与误差分析 | 标注规范、领域知识、语言差异、指标被利用的风险 |
| 后训练数据 | 用什么任务、难度、反馈和混合比例塑造行为 | 数据来源、筛选、去污染、合成与质量控制流程 | 基座能力、许可、标注运营、未见测试集 |
| 推理能力 | 如何使更多计算转为正确推断，而非仅增加输出长度 | 可验证任务、冷启动与RL配方、蒸馏、测试时计算分析 | 奖励覆盖、难度分布、训练与推理预算 |
| Agent后训练 | 多轮决策如何维持状态、使用工具、从稀疏结果中学习 | 环境、轨迹、动作接口、执行反馈、长时训练系统 | 沙箱可靠性、状态恢复、信用分配、外部接口变化 |
| 训练基础设施与评测工程 | 能否在相同预算下稳定复现实验并定位失败 | 训练/生成切换、并行策略、检查点、评测实现、版本记录 | 算法和系统协同，不能由单纯算力采购替代 |

这张表意味着组织中的接口往往比单个方法名称更重要。奖励团队给出可优化的信号，算法团队验证优化后是否仍代表原目标，数据团队控制覆盖与泄漏，系统团队保证采样与训练对应同一策略版本。独立评测应能发现这些环节共同忽略的失败，而不是只重复训练奖励。

## 二、2022年至2026年的变化：能力如何重新组合

### 从人类反馈到可复用偏好训练

InstructGPT的公开流程把示范数据、偏好排序、奖励模型和PPO连接起来。它表明“让模型遵循指令”需要标注、训练和评估共同完成；论文也将所学偏好限定为具体标注者与研究者群体，不能扩大成全体人类价值。对组织设计的启示是，反馈标准及其采集运营是核心研究输入，不是模型训练结束后的外包附件。[InstructGPT，2022，方法与讨论](https://arxiv.org/html/2203.02155v1)

DPO将KL约束下的奖励与策略关系重新参数化，直接用偏好对优化策略，减少显式奖励模型和在线RL这一套训练环节。由此降低的是某类配方的实现负担，并没有消除偏好数据与评价的需求。论文的贡献说明尤其有用：Rafael Rafailov负责目标推导与理论性质，Eric Mitchell编写初始实现并承担大规模模型训练、评估及人类研究，Archit Sharma承担早期方法讨论与大量实验组织；这些是明确披露的个人贡献，不需要从作者排序猜测。[DPO，2023，方法与Author Contributions](https://arxiv.org/html/2305.18290v2)

Google DeepMind团队的IPO理论论文进一步分析把成对偏好替换成点式奖励的假设与过拟合问题，其示例实验并不是全任务规模竞赛。它提示组织需要能够质疑目标函数假设的研究能力，也需要把理论现象重新放回真实数据与预算中检验。不能因采用DPO或IPO就认为奖励过优化已被彻底解决。[偏好学习理论与IPO，2023，前两页及目标定义](https://arxiv.org/pdf/2310.12036.pdf)

Hugging Face的Zephyr将蒸馏SFT、AI偏好反馈与DPO组合成公开配方，展示算法如何借助数据、代码和教程扩散。论文聚焦helpfulness，并明确未覆盖完整安全对齐，因此不能把其聊天评测表现当作整个后训练能力已完备。人才网络中的Leandro von Werra、Lewis Tunstall与Nathan Lambert连接了方法传播、工具库和开放训练实践，但“共同发布配方”不是三人各自负责所有组件的证据。[Zephyr，2023，方法、限制与署名](https://arxiv.org/html/2310.16944v1)

### 评价器与数据成为独立能力

RewardBench将回答偏好组织成可区分任务难度和行为的评测，分析分类式奖励模型与DPO隐式奖励的不同表现。它直接评估奖励模型，和只看最终聊天模型胜率的问题不同。这使“会训练奖励模型”和“能诊断奖励信号何时失真”成为需要区分的能力。[RewardBench，2024，第2–3页及评测框架](https://arxiv.org/pdf/2403.13787v1)

M-RewardBench把评价扩展到23种语言，发现同一模型的评价表现会随语言和翻译质量变化。它的价值不限于扩充语种名单：如果训练奖励在某些语言上不可靠，增加RL算力可能放大该缺陷。其团队同时包含机构研究者、大学成员与开放社区参与者，说明多语言评价可以形成不同于单一公司雇佣结构的合作网络。[M-RewardBench，ACL 2025，第1页摘要与署名](https://aclanthology.org/2025.acl-long.3.pdf)、[项目README](https://github.com/Cohere-Labs-Community/m-rewardbench/blob/main/README.md)

Tülu 3把数据整理、开发集与未见评测、SFT、DPO和可验证奖励RL连接成完整开放配方。其意义在于暴露各阶段接口、失败方法和中间产物，使外部团队能够判断改进来自哪里；不能把共同作者中的任何一人当作全部配方的独立拥有者。该版本也明确承认多语言、长上下文与工具使用仍是后续方向，因此“完整开放”描述的是可观察性，不代表任务覆盖无缺口。[Tülu 3，2024-11-22，概述与限制](https://arxiv.org/html/2411.15124v1)

### 推理训练增加在线学习与验证器依赖

DeepSeek-R1区分了不先做SFT的R1-Zero与采用冷启动、多阶段训练的R1；R1-Zero出现可读性与语言混合问题。这个区别会改变人才判断：团队既需要在线RL和可验证任务能力，也需要数据与行为质量控制，不能把R1的结果概括成“完全不需要监督数据”。邵智宏本人页面将DeepSeekMath、R1、Prover和工具推理列作研究方向，可支持其方向归纳；团队论文仍不能替代对其全部具体模块职责的披露。[DeepSeek-R1，2025](https://arxiv.org/html/2501.12948v1)、[邵智宏本人研究主页](https://zhihongshao.github.io/)

HybridFlow把分布式模型计算和RL数据流控制分开，并针对训练与生成之间的模型重分片设计执行系统。对组织而言，这类工作把“能写RL算法”与“能在给定GPU和模型规模下持续跑好算法”连接起来。论文中的加速比取决于基线和配置，本报告不把最高倍数当作任何团队采用后的收益承诺。[HybridFlow，2024预印本、EuroSys 2025](https://arxiv.org/html/2409.19256v1)

Falcon-H1R的公开技术路径同时涉及紧凑混合架构、冷启动SFT、RL和测试时扩展；日本Swallow的2026版本重新组合持续预训练、SFT与RL；AI Singapore的SEA-LION v4.8则将区域语言数据与在线on-policy蒸馏结合。它们显示后训练能力分布不宜仅沿旧的大公司清单观察，基础模型适配、区域语言资源与效率工程也能形成有区分度的研究方向。本报告对这些团队保留产物级结论，未把作者清单全部转成当前雇员表。[Falcon-H1R](https://arxiv.org/html/2601.02346v1)、[GPT-OSS Swallow，2026-02-20](https://swallow-llm.github.io/gptoss-swallow.en.html)、[SEA-LION v4.8，2026-09-16](https://arxiv.org/html/2609.18310v1)

### Agent训练把环境与系统引入核心研究

SWE-RL从开源软件演化记录构造训练数据，并使用与参考补丁相似性的轻量奖励。其软件工程评测结果不意味着训练奖励等同真实测试通过，也不能把单轮生成修复方案自动等同长时交互Agent。该论文首次公开日期按arXiv记录为2025年2月25日；本地HTML出现的2026年模板日期不能覆盖版本历史。[SWE-RL原文](https://arxiv.org/html/2502.18449v1)、[arXiv提交历史](https://arxiv.org/abs/2502.18449)

RAGEN用Bandit、Sokoban和Frozen Lake等受控环境研究多轮训练失稳、rollout多样性与奖励设计。这使它适合分析机制，却不足以证明在开放网页、企业软件或机器人环境中的普遍有效性。Kimi K2再把大规模Agent数据合成、真实及合成环境与联合RL放入生产模型配方；K3延伸到更长状态与rollout基础设施。二者证据层级不同，前者帮助拆解因果，后者显示大系统集成，但公开报告都不能直接给出每位成员的内部责任图。[RAGEN，2025](https://arxiv.org/html/2504.20073v1)、[Kimi K2，2025](https://arxiv.org/html/2507.20534v1)、[Kimi K3，2026](https://arxiv.org/html/2607.24653v1)

Arctic-SWE则强调异步RL中训练与推理一致性、策略更新间状态、奖励与重要性权重控制的共同作用。它提醒人才战略团队：一个系统基线没有调稳时，新算法或新增数据的收益很容易与工程修正混淆。能够建立可诊断基线和保存正确状态的工程研究，是Agent训练能力本身。[Arctic-SWE，2026-10](https://arxiv.org/html/2610.24914v1)

## 三、公开人物表：成果、任职和时间分别记录

下面的“观察日期”均为2026年11月9日，指本次读取公开页面的日期，不等于页面发布或入职日期。带日期的本人公告、CV和机构更新时间优先用于时期判断。只列与研究能力有关的信息。论文中的单位仅填写为该版本署名单位；若职业来源没有确认相同时间区间，则明确保留缺口。

| 人物及消歧 | 相关成果与个人贡献边界 | 公开角色、任职时期及最近确认 | 成果署名与职业证据、冲突或缺口 |
|---|---|---|---|
| Nathan Lambert，Interconnects作者、本人站natolambert.com | RewardBench、Tülu 3；后者明确标为核心贡献者。本人离职回顾描述开放后训练工作 | 本人2026-06-02回顾明确Hugging Face于2022-05入职、Ai2于2023-10入职；称前一天为Ai2最后工作日，即按其表述为2026-06-01。2026-10-01 Trillium创立公告；当前本人页称共同创办人、执行主任 | Tülu 3的2024版本署名Ai2，不等于2026仍在Ai2。Trillium公告日不当作劳动合同起始日。[职业回顾](https://www.interconnects.ai/p/farewell-ai2)、[本人页](https://natolambert.com/)、[创立公告](https://blog.trilliumlabs.org/p/introducing-trillium-labs)、[论文](https://arxiv.org/html/2411.15124v1) |
| Lester James V. Miranda，又用Lj V. Miranda，站点ljvmiranda921 | Tülu 3核心贡献者、M-RewardBench共同贡献；本人CV明确偏好数据、OLMo合成数据等工作 | 本人CV：ExplosionAI 2021–2023，Ai2 Predoctoral Young Investigator 2023–2025，Cambridge博士2025年至今；本人页另记2026-08开始Thomson Reuters Labs实习 | ACL 2025 M-RewardBench仍署名Ai2；与转入Cambridge不矛盾。月份级入离职未核实，实习不等同放弃博士身份。[本人页](https://ljvmiranda921.github.io/)、[CV](https://storage.googleapis.com/ljvmiranda/cv.pdf)、[论文](https://aclanthology.org/2025.acl-long.3.pdf) |
| Leandro von Werra，lvwerra | 本人确认TRL始于其2020年复现项目；Zephyr共同成果；不据此归属所有TRL后续实现 | 读取时本人页称Hugging Face Head of Research；2023厂商联合公告已经称其为HF机器学习工程师及BigCode共同负责人。精确入职与职位变更日未取得 | 2023 Zephyr署名H4网络；当前头衔来自本人页而非作者顺序。[本人页](https://www.lvwerra.com/)、[2023联合公告](https://s205.q4cdn.com/537566246/files/doc_news/ServiceNow-and-Hugging-Face-release-StarCoder-an-open-access-large-language-model-for-code-generation-05-04-2023-traffic-2023.pdf)、[Zephyr](https://arxiv.org/html/2310.16944v1) |
| Lewis Tunstall，lewtun | Zephyr共同贡献者，公开工具与配方工作；不把全团队成绩逐项归于个人 | HF在2022-04-13访谈称其为机器学习工程师；本人当时说已加入约九个月，可确认约2021年中，不能推精确日。本人公开职业资料仍列HF，本报告当前职责仅作开放后训练方向归纳 | Zephyr 2023署名H4。正式当前职级和任何后续变更时间未进一步核实。[机构访谈](https://huggingface.co/blog/lewis-tunstall-interview)、[本人职业资料](https://ch.linkedin.com/in/lewis-tunstall)、[论文](https://arxiv.org/html/2310.16944v1) |
| Amanda Askell，askell.io | 本人明确从事微调、诚实性、character与对齐。具体当前模型的个人训练模块未公开 | 本人页称在Anthropic工作，此前为OpenAI政策团队研究科学家；两段任职的精确起止日期未在已读资料确认 | 不把曾在OpenAI等同参与InstructGPT全部训练。Claude constitution作为相关团队产物，不据网页存在断言由其独立完成。[本人页](https://askell.io/)、[机构新constitution说明](https://www.anthropic.com/news/claude-new-constitution) |
| Rafael Rafailov，rmrafailov.github.io、DPO作者 | DPO贡献说明明确目标推导、理论证明及部分基线；其早期研究为离线RL与机器人学习 | 本人旧主页称Stanford博士，新闻最近到2022-01；可作历史职业证据，不能确认2026身份 | DPO 2023署名Stanford；该署名不是当前任职证据。截止日现职未核实，不能用于当前人员盘点。[旧本人页](https://rmrafailov.github.io/)、[DPO贡献说明](https://arxiv.org/html/2305.18290v2) |
| Eric Anthony Mitchell，ericmitchell.ai，论文常署Eric Mitchell | DPO明确初始实现、大规模训练评估、人类研究；本人称在OpenAI共同负责Post-training Frontiers | 当前本人页正文称已取得Stanford博士并在OpenAI工作；2022夏DeepMind研究实习四个月为本人明确经历。OpenAI加入日未核实 | 同页页头仍写“Ph.D. Candidate”，与更新正文冲突；采用更具体正文并保留冲突，不能据页头列为在读。DPO时期Stanford署名与当前OpenAI分开。[本人页](https://ericmitchell.ai/)、[DPO](https://arxiv.org/html/2305.18290v2) |
| Zhihong Shao，邵智宏，zhihongshao.github.io | DeepSeekMath/R1/Prover及工具推理为本人列出的研究成果；方向归纳为推理RL、验证与工具交互，未分配全部团队模块 | 本人页称DeepSeek Research Scientist，已获清华博士；加入DeepSeek及毕业精确日未从已读材料确认 | R1以DeepSeek-AI集体署名；本人研究页提供人物交叉核对，不能仅用集体作者推定职责。[本人页](https://zhihongshao.github.io/)、[R1](https://arxiv.org/html/2501.12948v1) |
| Longguang Zhong，mrggls.github.io | 本人列Kimi K2/K3参与及Agent、RL方向；K3贡献名单确认同名。没有公开模块分工，保留为参与者 | 本人页称Moonshot AI Member of Technical Staff，2025-07 K2及2026-07 K3新闻有日期；入职日期未核实 | 成果参与月不是入职月。K2贡献名单说明按姓氏字母排序，星号表示已不在团队，不能把排序作职级或默认所有作者当前在职。[本人页](https://mrggls.github.io/)、[K2](https://arxiv.org/html/2507.20534v1)、[K3](https://arxiv.org/html/2607.24653v1) |
| Zihan “Zenus” Wang，王子涵，zihanwang314 | RAGEN共同贡献作者；公开研究为Agentic RL。没有证据称其单独负责所有环境或系统 | 本人页称Northwestern博士研究者；列过去Microsoft、Yutori、DeepSeek实习；“今年夏天将去NVIDIA”的前瞻表述不证明已完成实习 | RAGEN 2025署名Northwestern。实习起止期、截止日NVIDIA任职均未确认，不生成确定流动边。[本人页](https://zihanwang314.github.io/)、[RAGEN署名](https://arxiv.org/html/2504.20073v1) |
| Guangming Sheng，HybridFlow作者、Chuan Wu实验室校友 | HybridFlow共同作者；论文支持分布式RLHF系统能力，个人组件未逐项披露 | HKU导师机构页2026-09更新：Ph.D. 2026、first job with Tencent；确认毕业年与首次去向，未确认入职月日及当前具体团队 | 2024论文署名HKU，不能在2026盘点为当前博士成员，也不能据首次去向断言现在在腾讯某模型团队。[机构校友页](https://i.cs.hku.hk/~cwu/team.html)、[HybridFlow](https://arxiv.org/html/2409.19256v1) |
| Chuan Wu，香港大学计算机科学教授 | HybridFlow共同作者；机构页明确分布式机器学习系统研究 | 机构当前页称HKU教授；2026新闻及2026-09团队页提供近期确认。本文不另推内部管理范围 | 2024论文HKU署名与当前机构资料交叉吻合；与ByteDance作者共同论文不构成雇佣或汇报关系。[机构页](https://i.cs.hku.hk/~cwu/)、[论文](https://arxiv.org/html/2409.19256v1) |
| Rio Yokota，横田理央，官方Yokota Lab页 | Swallow项目明确LLM training团队负责人；属于支撑后训练的系统训练能力，不能将整个RL配方归于其个人 | 官方履历：2023-01至2024-09东京工业大学教授，2024-10起Science Tokyo教授，另有NII及RIKEN公开并任。学校名称变化不能直接计作人员跳槽 | 当前Swallow项目页明确角色；后训练成果归团队，履历日期来自机构页。[履历](https://www.rio.gsic.titech.ac.jp/en/member/yokota.html)、[项目角色](https://swallow-llm.github.io/index.en.html) |
| Sakae Mizuki，Swallow项目页所列研究者 | 项目页明确instruction tuning与LLM evaluation团队负责人，属于直接公开职责证据 | 项目页面列Researcher，AIST / Science Tokyo；观察到截至2026-11的项目页面，精确任职起止日未公布 | GPT-OSS Swallow为对应团队产物；不把项目负责人头衔扩大为两家机构的内部管理职级。[项目成员与职责](https://swallow-llm.github.io/index.en.html)、[2026成果](https://swallow-llm.github.io/gptoss-swallow.en.html) |
| Shayekh Bin Islam，M-RewardBench共同贡献者 | 论文与项目README确认共同成果，机构社区页列为Community Researcher | Cohere Labs官方社区页面确认社区身份；ACL 2025署名KAIST及Cohere Labs Community。KAIST任职/学籍时间未由独立职业页面确认，保留未知 | 社区成员不是Cohere雇员；本文仅纳入公开项目身份，不能列入任何公司员工数。[社区说明](https://labscommunity.cohere.com/get-started/community-research)、[项目](https://github.com/Cohere-Labs-Community/m-rewardbench/blob/main/README.md)、[论文](https://aclanthology.org/2025.acl-long.3.pdf) |

这张表有意保留不同精度。Nathan的本人回顾能支持月级入职与离职陈述；Miranda的CV只支持年级区间；Guangming的机构校友页支持毕业年和首次去向；Rafael的旧主页只能支持历史身份。把它们都写成整齐的精确日期，会使图谱更美观而更不可靠。

## 四、专长—成果矩阵：从“参与过”到“可支持什么判断”

| 人物或团队 | 专长证据 | 能直接支持的判断 | 不能由该证据推出的判断 |
|---|---|---|---|
| Rafael Rafailov、Eric Mitchell | DPO明确个人贡献说明 | 理论推导与训练、评测实现可以在同一项目中形成互补 | 二人各自覆盖全部后训练链路，或当前组织分工仍与2023相同 |
| Google DeepMind IPO作者团队 | 偏好学习理论、假设与示例实验 | 对目标函数和过拟合机制的理论分析能力 | 所有作者当前仍在同一机构，或理论方法已在某商业模型全面采用 |
| Leandro von Werra、Lewis Tunstall、H4 | TRL本人项目说明与Zephyr配方 | 工具、数据、偏好方法与开放发布的连接能力 | 软件库所有模块的个人所有权；聊天成绩等同安全和Agent能力 |
| Nathan Lambert、Lester Miranda及Tülu团队 | 核心贡献标记、本人工作说明、公开完整配方 | 开放后训练配方、数据和评价的协同经验 | 离开机构后全部隐性知识、计算资源或其他成员随之迁移 |
| Amanda Askell及相关Anthropic团队 | 本人公开职责、constitution说明 | 将行为目标与微调、诚实性研究连接的专长 | 全部Claude行为由单一人物决定，或目标文件等于模型已实现该行为 |
| M-RewardBench网络 | 多语言奖励评测、翻译与验证工作、公开团队 | 评价器跨语言适用性与社区协作能力 | 所有语种、文化或专业领域均被覆盖；社区身份等于劳动关系 |
| 邵智宏及DeepSeek研究团队 | 本人研究页与Math/R1/Prover相关成果 | 推理RL、可验证反馈与工具/证明任务的交叉 | R1全部创新由个人完成，或易验证任务收益普遍迁移至开放任务 |
| Guangming Sheng、Chuan Wu及HybridFlow联合团队 | 系统论文与职业交叉核对 | 大模型训练/生成数据流和并行系统研究 | 2026腾讯与ByteDance存在同样的组织协作；作者顺序反映汇报关系 |
| Longguang Zhong及Kimi团队 | 本人方向、K2/K3参与与团队报告 | Agent和RL大系统集成的参与证据 | 个人负责长上下文系统、全部数据或全部RL，内部岗位分工仍未披露 |
| Zihan Wang及RAGEN网络 | 共同贡献署名、可控多轮环境研究 | Agent训练动态、环境和稳定性研究经验 | 已在任意企业环境中实现可靠自治，或实习计划已经完成 |
| Swallow公开角色组 | Rio的训练职责、Sakae的指令微调与评价职责及2026配方 | 语言资源、系统训练、后训练与评测可形成明确项目分工 | 日本高校/研究所全部后训练人才供给规模，或所有成员只属于一家机构 |
| AI Singapore、TII Falcon、Arctic-SWE团队 | 各自公开配方与系统论文 | 区域语言适配、效率优化及Agent系统构成不同合作入口 | 仅据团队署名生成个人现职、管理层级或完整能力排名 |

同一个产物可能连接多个能力维度。例如Miranda的职业材料明确提及偏好数据、工具SFT与多语言研究，支持其连接数据和评价的方向；它不证明其独立承担过大规模异步RL基础设施。Rio的公开项目职责说明系统训练角色，Sakae的角色说明微调与评价协调；两者共同出现在项目中使能力组合可见，但不需要猜测彼此行政汇报关系。

## 五、团队演化时间线：人员、研究与品牌分开

| 时间 | 可核实事件 | 对能力分布的意义 | 边界 |
|---|---|---|---|
| 2022 | InstructGPT公开；HF访谈确认Lewis的工程角色；Nathan本人回顾记录2022-05加入HF | 后训练知识向开放工具与配方网络扩散，数据和反馈开始形成明确工作对象 | 此处是公开成果与职业事件，不能推断所有团队实际起点 |
| 2023 | DPO、IPO、Zephyr公开；Nathan于2023-10进入Ai2 | 算法简化、理论分析与开放配方形成不同能力支点 | 同年论文的作者单位可能跨越个人换机构时点 |
| 2024 | RewardBench、M-RewardBench预印本、HybridFlow、Tülu 3公开 | 评价、跨语言数据、分布式RL与完整配方更可观察 | 不用论文数量比较组织总能力；开放程度会改变可见度 |
| 2025 | R1、SWE-RL、RAGEN、Kimi K2等公开；Miranda的CV记录Ai2结束、Cambridge开始 | 推理和多轮任务使验证器、环境与系统成为核心；公开研究能力跨机构延续 | Miranda仅有年级区间；SWE-RL首发按arXiv为2025-02-25 |
| 2025-06-02 | 加拿大登记显示Cohere For AI Institute法定名称改为Cohere Labs | 名称变化可能解释论文署名更新 | 该登记证明法人名称变更，不证明人员加入、离开或研究职责重组 |
| 2026-02 | GPT-OSS Swallow发布，组合持续预训练、SFT与RL | 区域语言和系统训练团队扩大后训练配方深度 | 不能把持续预训练收益全部归因于后训练 |
| 2026-06至10 | Nathan宣布离开Ai2；10月Trillium创立公告承诺开放后训练配方 | 可确认一条人员流动和新组织使命；完整开放配方成为独立组织目标 | 新机构宣言不是已交付全部研究产物的证明 |
| 2026年、9月机构确认 | Guangming Sheng博士毕业、首次工作腾讯 | 系统研究人才进入工业组织 | 无精确入职月日，腾讯具体团队不明；不连接未证实的内部岗位 |
| 2026-07至10 | Kimi K3、SEA-LION v4.8、Arctic-SWE等公开 | 长状态训练、区域语言蒸馏与模型系统共同设计继续发展 | 一份新论文不能自动证明作者当前组织归属与全部技术个人贡献 |

名称变更的证据来自[加拿大官方登记](https://ised-isde.canada.ca/cc/lgcy/fdrlCrpDtls.html?cStatus=1&corpId=13975631&crpNm=labs&p=2)；其他事件来源见人物表及相应论文。东京工业大学到Science Tokyo的履历变化也应保留为机构沿革背景，不在没有额外证据时编码成跨机构人才争夺。

## 六、能力网络：每一条边都有性质和时间

以下采用可追溯关系表表达图谱，不把不同关系投影成一个无时间的“人脉图”。能力互补是本报告的组织分析，不能当作已经发生的合作；共同成果、公开项目协作、任职重叠与流动分别列出。

| 起点 → 终点 | 边类型、时间 | 原始证据 | 可用于什么分析 |
|---|---|---|---|
| Rafael Rafailov ↔ Eric Mitchell | 共同成果，DPO，2023 | [DPO贡献说明](https://arxiv.org/html/2305.18290v2) | 理论与实现/评测的可观察互补；不是管理关系 |
| Leandro von Werra ↔ Lewis Tunstall ↔ Nathan Lambert | 共同成果，Zephyr，2023 | [论文署名和配方](https://arxiv.org/html/2310.16944v1) | 开放工具与配方网络；不要求三人整个发表期间在同一雇主 |
| Nathan Lambert ↔ Lester Miranda | 共同成果，Tülu 3，2024；公开任职区间交集约2023-10至2025某时点 | [Tülu 3](https://arxiv.org/html/2411.15124v1)、[Nathan回顾](https://www.interconnects.ai/p/farewell-ai2)、[Miranda CV](https://storage.googleapis.com/ljvmiranda/cv.pdf) | 同项目合作与任职重叠有各自证据；不推直属关系 |
| Miranda、Shayekh Bin Islam及M-RewardBench团队 | 共同成果与项目协作，2024–2025 | [项目README](https://github.com/Cohere-Labs-Community/m-rewardbench/blob/main/README.md)、[ACL版](https://aclanthology.org/2025.acl-long.3.pdf) | 机构与开放社区共享多语言评价工作；社区不是雇佣关系 |
| Guangming Sheng ↔ Chuan Wu及ByteDance论文作者 | 共同成果，HybridFlow，2024–2025 | [论文](https://arxiv.org/html/2409.19256v1)、[HKU项目新闻](https://i.cs.hku.hk/~cwu/) | 学术分布式系统与产业RLHF工程结合；不是2026当前联合团队证明 |
| Zihan Wang ↔ RAGEN共同作者网络 | 共同成果，2025-04 | [论文署名](https://arxiv.org/html/2504.20073v1) | 多机构Agent机制研究；不能推每对作者私交或组织汇报 |
| Rio Yokota ↔ Sakae Mizuki / Swallow | 公开项目协作，观察至2026-11；项目页明确不同职责 | [Swallow成员页](https://swallow-llm.github.io/index.en.html) | 系统训练、微调和评价如何组合；无需臆测个人负责的所有代码 |
| Hugging Face → Ai2 → Trillium（Nathan） | 公开人员流动，2022-05、2023-10、2026-06离职与10月新机构公告 | [本人回顾](https://www.interconnects.ai/p/farewell-ai2)、[Trillium公告](https://blog.trilliumlabs.org/p/introducing-trillium-labs) | 开放后训练经验延续；不推知识产权或团队整体迁移 |
| Ai2 → Cambridge（Miranda） | 公开职业/学术阶段转换，2025年 | [本人CV](https://storage.googleapis.com/ljvmiranda/cv.pdf) | 数据与多语言研究在不同组织形式中的延续 |
| HKU → Tencent（Guangming Sheng） | 机构公开毕业后首次去向，2026年；9月页面确认 | [校友页](https://i.cs.hku.hk/~cwu/team.html) | 系统人才流动的可证边；不推具体业务或离开动机 |
| Stanford → OpenAI（Eric Mitchell） | 本人公开职业阶段转换，具体日期未明，2026-11观察 | [本人页](https://ericmitchell.ai/) | 偏好训练经验与前沿部署职责的连接；不能填造起始月 |

在成果层可以画出另一组依赖：DPO方法被Zephyr配方采用，RewardBench被多语言评价扩展，Tülu展示多阶段配方，HybridFlow提供RL执行组织，RAGEN研究环境中的训练动态。这些属于产物采用或研究关联，不能直接转换成作者之间发生过合作。这个区分尤其重要：组织可能通过开源软件获得某种能力支撑，而从未与原作者建立人员关系。

图中没有把邵智宏与Longguang Zhong连接为“合作”，也没有把Zihan的过去实习列为完整时间线，因为已读资料不足以支持对应关系或日期。缺边并不表示没有关系，而是本图谱不作无法证实的补全。

## 七、组织布局与合作选择

### 先判断瓶颈，再选能力组合

对已经拥有可用基座、但指令质量不稳定的团队，优先组合数据整理、偏好优化与独立评测。DPO/Zephyr式实现可降低启动成本，仍应保留没有进入训练筛选的评测集，并分析标注一致性与任务覆盖。仅招聘算法作者、继续使用混乱的反馈数据，通常不能解决此类问题；这是一项由上述方法依赖推导出的组织判断，不是对某个人能力的评价。

对目标为数学、代码或可验证任务推理的团队，需要把验证器设计、难度分布、在线采样和训练系统一起安排。DeepSeek类研究说明可验证反馈的重要性，HybridFlow类研究说明实际训练效率依赖执行结构。合作可以围绕公开可复现的任务、奖励错误与训练稳定性展开；不宜把可验证题库上的增长直接承诺为开放研究或商业决策能力。

对面向多语言产品的团队，应在算法扩大前引入目标语言评价和数据能力。M-RewardBench、SEA-LION和Swallow展示了不同入口：跨语言奖励评价、区域语言模型适配和本地语言基础资源与训练配方。它们互补但不互相替代。翻译过的偏好数据还需检查语义、文化和任务分布；拥有英语评价冠军不能自动证明服务目标语言用户的能力。

对Agent团队，环境工程和系统一致性必须与策略学习同级。选择公开合作对象时，应区分研究失稳机制的受控环境、提供大规模集成配方的模型团队，以及解决异步执行和状态问题的系统团队。合作课题可以是同一模型、同一数据与预算下改变环境或训练组件的可解释比较。本报告没有开展这些新实验；这些是从已读证据得到的合作方向。

### 用产物评估合作接口，避免从名气推供给

如果需要开放可改造的训练能力，工具库、数据配方、评测实现与中间检查点的可获取程度，往往比作者所在公司大小更有用。Hugging Face、Ai2、开放社区和大学网络能提供不同形式的入口；Trillium的使命与这一需求一致，但截至所读创立公告只能评价其公开方向，不能把拟交付内容计作现成能力。

若需要把研究接到大规模商业训练，必须确认合作方公开或可在合作中提供的系统接口、算力条件与评价要求。Kimi、DeepSeek、OpenAI、Anthropic等商业团队论文或本人职责可揭示方向，却不会完整暴露生产系统。建议应落在可观察需求和公开研究产物上，不应据此推算未公开人员规模、薪酬、流失风险或招聘接受率。

### 组织依赖应保留在团队中

人员流动说明经验可能跨机构延续，却不意味着数据许可、计算设施、工程支持和协作网络全部可以随人转移。Nathan离开Ai2并参与创立新机构，是职业与组织事件；它不能单独说明Ai2能力下降多少或新机构立即具有何种训练规模。Miranda从Ai2转向Cambridge表明研究主题可延续，但当前资源、考核与合作方式已经不同。Guangming从学术系统研究进入产业的证据，也没有说明其具体产品职责。

因此，研发组织应把可复用资产和关键接口显式安排：谁维护任务与反馈定义，谁检查训练与评价分布，谁负责rollout与版本一致性，谁能解释改进的来源。是否由同一个人兼任取决于团队规模，公开图谱不能替代内部实际分工。它能帮助团队发现自己只有某一端的能力，并选择有明确产物和时间证据的合作入口。

## 八、如何使用这份图谱以及证据的限度

人物表可用于形成研究合作候选及需要进一步核对的职责问题；专长矩阵可用于检查团队缺口；时间线可避免把历史论文当作当前组织；关系表可区分项目合作与人员流动。它们共同支持对能力组合的判断，不能合并成一个没有时间的“人才实力分数”。

几个具体限制会直接影响使用。Rafael的个人页明显陈旧，当前身份未知；Eric页头与正文冲突；Longguang只有团队参与和本人方向，缺内部模块职责；Zihan的未来实习措辞不能证明经历已完成；Shayekh的社区身份可确认，但KAIST时期未由独立职业资料确认。将这些条目用于当前编制或招聘前，应补充对应公开职业材料，不能把表内空缺转成确定事实。

本研究读取了所引论文的摘要、相关方法、限制、署名与可用贡献说明，以及职业页面的相应段落，并未声称读完全部论文或源代码。部分页面可以通过公开网页工具读取但直接下载失败，阅读记录标明了该区别。未运行新的模型训练、基准或招聘分析。截止日之后发生的变化不在本报告范围内，网页访问日期也不会被当作历史事件发生日期。

研发与人才战略最有用的结论，是把研究方向落到可观察的工作对象和接口上：谁曾公开解决哪类问题、与什么产物和组织时期对应、还需要什么互补能力。这样的图谱允许不确定项继续存在，也能在任职或成果更新时修订具体条目，而不改变已经核实的历史。
