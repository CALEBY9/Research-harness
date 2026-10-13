# Research Harness

**面向环境科学、地理科学的 AI Research Partner。**

**从模糊 idea 出发，形成可检验的研究问题，以真实证据构建论证，准备完整投稿稿件。**

Research Harness 是研究者主导的科研协作框架。它把问题筛选、文献证据、方法设计、
数据分析、图件叙事和论文写作连接在同一个项目中。研究者决定科学方向与核心主张，
Research Agent 在已授权范围内完成相应工作，并把需要选择的研究路线、缺失证据和
可审阅产物交给研究者。已有数据、手稿或审稿意见也可以直接作为起点。

当前公开入口是 [`research-agent`](skills/research-agent/SKILL.md)。仓库维护
**29 个技能源码与共享参考目录**：28 个维护中的入口（含共享依赖），
另有 ARS 仅为发现目录之外的版本化参考。功能精简结果见
[全部技能功能审查](docs/skill_function_audit.md)。
科研流程技能统一采用 `nature-<capability>` 命名；更名对应关系见
[技能命名](docs/skill_naming.md)。
[`nature-scientific-insight`](skills/nature-scientific-insight/SKILL.md)（科研洞察与判断）是核心技能，
Nature Skills 是默认写作底座，同时保留本地
知识库、研究设计、数据分析和证据审计能力。其他专业可以复用通用科研能力；
完整研究设计需要结合该专业的方法、数据条件和证据标准。

## 适合谁，哪些专业可以使用？

适合希望把初步想法发展成研究项目的本科生、研究生和青年研究者，已有数据但需要凝练贡献、
组织图件与论证的作者，以及希望保留科学决策权、同时获得检索与执行支持的科研团队。
也适合只需要论文阅读、润色、开题报告、图件或返修协助的使用者。

**环境科学与地理科学是当前重点设计场景，专业名称并不是通用模块的使用限制。**
已有写作技能支持研究、方法、算法、假说和综述等论文类型，也有通用期刊路径。
跨专业的可复用范围与需要补充的条件如下；这表示设计适用性，不代表已经完成所有
专业的实际任务验证。

| 研究领域 | 可以复用的内容 | 使用时需要补充 |
|---|---|---|
| 环境科学、地理科学及相关地球科学研究 | 问题筛选、空间与时间尺度、观测及情景设计、分析与论文生产 | 具体对象定义、数据权威、尺度与领域方法 |
| 计算机科学、数据科学与工程 | 文献、算法或方法论文组织、分析脚本、图件、基线与结果报告 | 合适的任务、数据划分、比较基线、运行环境与验证标准 |
| 生命科学、医学、化学与材料研究 | 文献检索、论文阅读、方法与结果表达、统计报告、图件和投稿材料 | 专业实验或研究方案、真实实验数据及相应报告要求 |
| 社会科学、管理学及人文研究 | 文献与引文、研究计划、论证组织、语言编辑、格式与项目连续性 | 本领域理论、定量或定性方法、文章结构和目标刊物规范 |

`nature-research-discovery`、`nature-method-design`、`nature-experiment-plan` 的现有研究设计默认围绕环境科学。
其他专业使用完整项目路径时，应提供领域问题、代表文献、成熟方法与验证标准，
先检查这些默认假设是否适用。通用写作和润色可以直接使用；Nature 写作底座也可
服务其他期刊，最终结构与提交材料按目标期刊调整。

## 核心特色与设计创新

本项目的设计创新集中在**科学判断、证据治理、任务协作与论文生产的衔接**。
已有 Nature 等技能提供写作与工具基础，本地增强把它们组织成作者可控制、
证据可追溯、任务可接续的研究过程。

1. **用可证伪问题筛选 idea。** 将最接近的先行研究、实际剩余贡献、数据可行性和
   否定条件一起比较。候选想法需要回答“什么发现会改变现有认识”“什么结果会
   否定我的解释”，再据此比较值得推进的研究路线。
2. **把证据贯穿到最终主张。** 文献保留原文定位，分析保留数据与计算依据；
   核心主张对应具体比较、结果和图件。检索、分析与写作交接时沿用这些证据及限制，
   区分已支持的发现、待验证解释和缺失资料。
3. **围绕新增知识组织论文。** Nature 写作底座与本地科学定位指导共同处理
   “本文改变了什么认识”：已有解释、未解决问题、关键结果和贡献范围形成一条
   可检查的论证，图件与正文呈现同一个科学比较。
4. **在作者决策下完成跨任务交付。** 一个入口按交付物选择负责技能，协调检索、
   分析、图件和写作。作者选择方向与关键取舍后，Agent 在授权范围内继续执行、
   验证和修复；已确认材料可以直接进入所需阶段。
5. **让长期项目可以恢复和修订。** 复用项目已有事实、决定和证据，保持正文、
   图件、引用与回复之间的一致性；采用针对性修改，保留作者已认可的研究对象、
   提纲、主张边界和正式产物。
6. **让改进可以核查。** 技能源码版本化，真实任务问题推动局部维护；结构检查、
   工具测试和科研质量评估分别记录。上游改进先审阅差异，再选择性吸收并验证。

## 科研流程与对应技能

从模糊想法开始时，通常按下列步骤推进。已有文献、明确问题、分析结果或稿件时，
可以从对应步骤开始。每次只使用当前任务需要的技能，复用已完成的证据和判断。

| 步骤 | 要做什么及完成标志 | 对应技能 |
|---|---|---|
| 1. 澄清模糊想法 | 明确感兴趣的现象、研究对象、尺度与资源约束，形成可检索的问题范围 | [nature-research-discovery](skills/nature-research-discovery/SKILL.md) |
| 2. 检索领域与先行研究 | 多源检索、查询相关本地论文库，识别领域共识、最接近研究和证据缺口；保留来源及覆盖范围 | [nature-academic-search](skills/nature-academic-search/SKILL.md)、[nature-literature-kb](skills/nature-literature-kb/SKILL.md) |
| 3. 获取全文并精读关键论文 | 合法取得全文，核查关键方法、结果与局限，形成有原文定位的证据卡；按请求提供完整或双语阅读 | [nature-downloader](skills/nature-downloader/SKILL.md)、[nature-reader](skills/nature-reader/SKILL.md) |
| 4. 形成并筛选候选 idea | 根据文献提出少量可检验问题，比较科学价值、已有研究重合、剩余贡献、数据可行性与风险，给出推荐或重构建议 | [nature-research-discovery](skills/nature-research-discovery/SKILL.md)（候选组织）、[nature-scientific-insight](skills/nature-scientific-insight/SKILL.md)（核心判断标准） |
| 5. 确定研究问题与方向 | 研究者依据证据和建议选择方向，明确核心问题、假设或描述目标，以及保留和放弃的范围 | 研究者决定；[nature-scientific-insight](skills/nature-scientific-insight/SKILL.md)辅助取舍 |
| 6. 设计方法与验证计划 | 比较成熟方法和竞争解释，确定数据需求、对照、基线、区分性观测与最小验证，形成可执行方案 | [nature-method-design](skills/nature-method-design/SKILL.md)、[nature-experiment-plan](skills/nature-experiment-plan/SKILL.md) |
| 7. 获取数据并执行分析 | 在可用访问和实验条件下整理数据、运行分析、检查误差与不确定性，保留负结果和可复现计算依据 | [nature-data-analysis](skills/nature-data-analysis/SKILL.md)；实际采样或实验由研究者及获授权工具完成 |
| 8. 解释结果并确定科学主线 | 复用已完成计算，区分观测、解释和可支持主张，比较新增认识与竞争解释，由研究者决定核心主线 | [nature-data-analysis](skills/nature-data-analysis/SKILL.md)（结果解释）、[nature-scientific-insight](skills/nature-scientific-insight/SKILL.md)（科学取舍） |
| 9. 组织图件并撰写论文 | 让关键图件、章节和引用共同支持已确认的主线，形成论文或学位论文章节；提纲与证据说明单独交付 | [nature-figure](skills/nature-figure/SKILL.md)、[nature-writing](skills/nature-writing/SKILL.md) |
| 10. 润色与格式修订 | 保留科学含义和主张强度，按需要润色、翻译、压缩及修订版式，形成干净的正文和页面 | [nature-polishing](skills/nature-polishing/SKILL.md)、[nature-paper-format](skills/nature-paper-format/SKILL.md) |
| 11. 投稿前检查与修正 | 按具体风险核查证据、可复现性和统计报告，开展审稿人视角预审；补证据或修正后同步相关正文和图件 | [nature-evidence-audit](skills/nature-evidence-audit/SKILL.md)、[nature-statistics](skills/nature-statistics/SKILL.md)、[nature-reviewer](skills/nature-reviewer/SKILL.md) |
| 12. 整理投稿材料 | 核查目标期刊要求，整理投稿信、数据与代码可用性声明、附件及必要 source-data，由作者最终确认提交包 | [nature-writing](skills/nature-writing/SKILL.md)、[nature-data](skills/nature-data/SKILL.md) |
| 13. 根据审稿意见返修 | 收到意见后制定修订方案，按审稿人组织回复，同步修改正文、图件和回复定位 | [nature-response](skills/nature-response/SKILL.md)；正文与图件仍由相应技能处理 |

步骤 2–5 可以反复迭代：文献会改变候选问题，重合较高或证据不足时应补充检索、
收窄或重构想法。没有搜到相同论文不能直接证明创新成立。步骤 4 的筛选可以在
一份候选报告中完成；已有判断充分时直接复用。

`nature-scientific-insight` 是贯穿选题、设计和结果解释的核心判断支持。“核心”
表示采用什么科学判断标准，执行顺序仍由当前问题、可用证据和研究者的选择决定。

其他交付按需要插入对应步骤：

- 确定问题与设计后，需撰写开题报告、项目书或研究计划时，使用 [nature-proposal-writer](skills/nature-proposal-writer/SKILL.md)。
- 做系统综述或元分析时，使用 [nature-literature-synthesis](skills/nature-literature-synthesis/SKILL.md)制定适用的检索、筛选与综合方案；按研究类型调整后续分析步骤。
- 从学者公开研究提取判断框架时，使用 [nature-scholar-distiller](skills/nature-scholar-distiller/SKILL.md)；明确需要周期文献监测时，使用 [nature-literature-pipeline](skills/nature-literature-pipeline/SKILL.md)。
- 需独立文风修订时，可使用 [humanizer-zh](skills/humanizer-zh/SKILL.md)或 [Humanizer](skills/humanizer/SKILL.md)；汇报材料用 [nature-paper2ppt](skills/nature-paper2ppt/SKILL.md)，已有图片幻灯片重建用 [nature-image2ppt](skills/nature-image2ppt/SKILL.md)。

Nature 技能按需使用 [nature-shared](skills/nature-shared/SKILL.md) 的共享参考，
它承担参考支持。ARS 保留为停用的备选材料；本机独立 `scientific-agent-vnext`
候选仅供明确选择的任务使用。默认写作使用 Nature，不自动混用其他写作体系。

## 从模糊 idea 到投稿级手稿

例如，使用者只有“想研究城市绿地与居民热暴露的关系”这个方向，还没有明确问题。
起步时提供研究背景、已有资料、可能获得的数据、时间与计算条件即可；目标期刊
可以稍后根据实际贡献与证据确定。

### 第一次如何调用

在已安装技能的会话中，可以这样描述一个完整项目的目标：

```text
调用 Research agent。
我只有一个初步 idea：想研究城市绿地与居民热暴露的关系。
我的背景、已有资料、可获得的数据和时间条件如下：[填写或指向项目文件]。
目标是发展成有真实证据支撑的研究，并准备投稿稿件。
请先核查先行研究、比较可检验的问题和数据路径，让我选择研究方向；
选定问题与关键方法后，在已授权范围内继续分析、图件、写作和投稿前检查。
缺少真实数据或无法解决的科学选择时，明确指出缺口，不把假设写成结果。
```

### 项目如何推进

按上方流程表推进：起步时先检索和精读关键研究，再形成、筛选并确定问题。
方向与关键方法确定后，研究者提供数据或可用访问方式，Agent 在授权范围内完成
分析、解释、图件、写作及提交准备。新的证据或审查意见可能要求返回相关步骤。

普通操作沿用已有授权；会改变科学方向的选择或无法绕过的输入缺口需要研究者
处理。已有问题、结果或稿件可从对应步骤开始，不要求逐项重做或每个步骤重新确认。

需要实际采样、实验设备或外部访问的工作由研究者或获授权的工具完成。
只有 idea 而没有所需证据时，当前交付会是选题与验证方案；数据或分析不足会被
标明，并据此收窄主张或补充研究。综述等文章使用适合该类型的文献证据和方法。

### 最终交付与“投稿级别”的含义

面向指定期刊，目标交付包括完整正文、与结果一致的图件和图注、已核验参考文献，
以及适用的补充材料、投稿信、数据/代码可用性和作者声明。分析脚本、证据定位与
检查记录单独保存，正式稿保持干净。

“投稿级别”是需要实际验收的目标：研究问题与贡献清楚，方法和比较能支持主张，
结果可核查，引用有依据，正文与图件一致，适用提交要求得到满足。最后由作者确认
研究质量和投稿材料；发表决定取决于期刊评审，技能安装或文字生成本身不能保证。

## 已有研究可以直接使用

如果已经有部分成果，直接说明当前任务及可修改范围：

```text
调用 Research agent，基于这份已确认的大纲修改引言，保持研究问题和引用不变。
调用 Research agent，只润色这段已有文本，保留论证结构和科学含义。
调用 Research agent，检查这个分析结果能支持什么结论，先只读。
调用 Research agent，用这份已核验数据绘制多面板图，交付可编辑矢量文件。
调用 Research agent，依据学校模板和已有初稿完善开题报告。
调用 Research agent，检查这份审稿回复与修改后的正文是否一致。
```

## 项目上下文与证据治理

项目事实和已确认决定保留在研究项目中。现有 `.agent/NEXT.md`、
`STATE.md` 等文件承担跨会话恢复，原始资料和分析结果承担证据权威。
任务内复用足够的记录，避免在提案、技能模板和工作包之间重复维护同一状态。

已接入 OpenSpec 1.12.0。对明确使用 OpenSpec 的任务，`research-task` 工作包
链接科学要求、实现步骤与实际验收证据；普通检索、润色等任务可以直接执行。
工作包完成或文件齐全不能代替科学验收。详见
[系统边界](docs/architecture.md)和[OpenSpec 科研使用说明](docs/openspec_usage.md)。

## 源码维护与安装

模型调用、权限和会话执行由现有 Codex 运行时提供。仓库 `skills/` 是维护源码，
实际使用需要将所需技能安装到运行时支持的目录，并绑定相应工具和数据环境。

维护脚本需要 Python 3.10+。在仓库目录运行：

```powershell
python -X utf8 -B scripts/harness.py validate
python -X utf8 -B -m unittest discover -s tests -v
python -X utf8 -B scripts/harness.py doctor
```

`validate` 检查源码结构、语法、声明及已知凭据模式；`doctor` 定位需要人工确认的
本机路径。各技能的文献服务、全文权限、知识库、文档软件和绘图环境按任务单独配置。

`git pull` 更新仓库源码，不会自动替换本机技能。迁移时先比较现有安装和源码，
保留有效本地增强，再安装所需技能及共享依赖，验证实际技能发现和目标任务。
详见[迁移与环境说明](docs/installation.md)。

Nature 底座来自本仓库已发布的 `b5b8e08` 本地增强快照，之后选择性吸收改进。
上游更新先比较和审阅，再验证、同步受影响文件。已授权的本机每周监测只读取
公开上游并准备审阅包，启动项与绑定保留在本地。详见
[更新方式](docs/installation.md#已授权的上游监测)。

## 当前验证与限制

2026-10-13 功能精简后，8 个重复入口已移除，28 个维护条目在本机原生发现中
启用；725 对源码/安装文件一致，125 条 manifest 资源路径和 168 个本地链接
检查通过。迁移的论文定位与作者导出脚本共 16 项相关测试通过，两项图件帮助
脚本可从新路径启动。只执行受影响的机械检查，没有新增模型调用或行为评估。
完整分工、合并去向与限制见[功能审查](docs/skill_function_audit.md)。

同日后续修正了合并模式的文本冲突：先选择交付物及模式，模式完成即返回；
卡片不继承完整 reader 流程，提示词/参考图任务不进入绘图验收，已有文本可直接
修辞修订，解释已有结果不默认重算。提供方误绑定、CNS 模式说明、查询复用和
既有回归定义一并更正。按既定维护政策执行受影响的机械检查，模型行为与科研
质量仍未实测。

截至 2026-10-12，已执行的维护验证包括：**51 项维护、接口与集成测试通过**，
源码检查通过，34 个技能目录下的 721 个源码文件与本机安装副本一致，
受影响技能的原生发现检查无错误。现有 OpenAlex HTTP 回退完成匿名检索 smoke；
真实认证请求尚未执行。

仓库保留 36 条维护回归定义，其中 2 条因缺少私有原始片段仍不可执行。
这些定义及结构检查不等于已经执行全部行为评估，也不证明科研判断、
写作质量、创新性或投稿水平提升。外部文献服务的覆盖和可用性随访问条件变化；
知识库、账户、Office 等本机依赖不随 GitHub 克隆自动配置。

## 持续优化与文档

从真实任务暴露的具体问题出发，修改对应技能的最小部分，保留可复核案例，
运行相关检查，并在需要判断行为变化时用相同材料比较现用版和候选版。
作者评估证据支撑、事实保留和修改负担，通过后更新受影响安装。

GitHub 保存技能源码和脱敏的改进材料。论文库、未公开研究、原始私有评估、
会话、凭据和本机绑定保留在仓库外或忽略的本地目录中。

- [系统边界与个人习惯](docs/architecture.md)
- [全部技能功能审查与本次精简](docs/skill_function_audit.md)
- [早期架构审查](docs/architecture_review.md)
- [科学发现建议与本地优化](docs/scientific_discovery_review.md)
- [参考项目比较与选择](docs/reference_projects.md)
- [行为评估方法](docs/behavioral_evaluation.md)
- [迭代与贡献](CONTRIBUTING.md)
- [优先级路线](docs/roadmap.md)
- [迁移验证记录](docs/validation.md)
- [第三方来源与许可](THIRD_PARTY_NOTICES.md)
