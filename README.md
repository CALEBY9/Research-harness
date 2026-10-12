# Research Harness

**面向环境科学、地理科学、海洋科学的 AI Research Partner。**

Research Harness 维护本地 Research Agent 的技能源码、工具、项目上下文约定与评估方法。
研究者决定科学问题、方法取舍和核心主张，Agent 根据当前任务协调文献、数据、分析、
写作与审查，完成可审阅、可复核的交付物。可以从选题开始，也可以直接处理已有数据、
稿件或审稿意见。

当前公开入口是 [`research-agent`](skills/research-agent/SKILL.md)。仓库维护
**34 个技能与共享参考目录**，采用 Nature Skills 作为默认写作底座，并保留本地
知识库、研究设计、数据分析和证据审计能力。模型调用、权限和会话执行由现有 Codex
运行时提供；仓库 `skills/` 是维护源码，实际使用还需要本机技能安装及相应工具绑定。

## 能力与分工

按当前交付物选择一个主要负责技能，再按证据缺口使用支持工具。

| 任务 | 内容 | 主要技能 |
|---|---|---|
| 科学发现与选题 | 有来源的领域地图、最接近的先行研究、残余贡献、可检验假设、数据可行性与风险比较 | [res_find](skills/res_find/SKILL.md) |
| 方法与实验设计 | 细化作者选定的问题，比较方法与竞争解释，设计对照、区分性观测和验证路线 | [res_method](skills/res_method/SKILL.md)、[res_plan](skills/res_plan/SKILL.md) |
| 学术判断框架 | 从学者公开研究中提取对象定义、创新逻辑、机制链和证据标准 | [research-scholar-distiller](skills/research-scholar-distiller/SKILL.md) |
| 文献检索与引文核验 | 多源检索、按证据缺口继续搜索、选择性引文追踪、参考文献核验与导出；明确要求 CNS 来源时单独限制 | [nature-academic-search](skills/nature-academic-search/SKILL.md)、[nature-ref-verifier](skills/nature-ref-verifier/SKILL.md)、[nature-citation](skills/nature-citation/SKILL.md) |
| 全文获取与论文阅读 | 合法获取全文，制作保留定位信息的双语 reader，或整理单篇论文证据卡 | [nature-downloader](skills/nature-downloader/SKILL.md)、[nature-reader](skills/nature-reader/SKILL.md)、[nature-paper-card](skills/nature-paper-card/SKILL.md) |
| 知识库与证据综合 | 查询已核验的本地论文库；制定系统综述、筛选、编码与跨论文综合方法 | [literature_kb](skills/literature_kb/SKILL.md)、[lit_synthesis](skills/lit_synthesis/SKILL.md) |
| 数据分析与结果解释 | 执行可复现计算，形成脚本、表图和诊断；解释已完成结果及其可支持的结论 | [data_analyze](skills/data_analyze/SKILL.md)、[res_analyze](skills/res_analyze/SKILL.md) |
| 论文与学位论文写作 | 基于作者证据规划、起草和重构摘要、引言、方法、结果、讨论及学位论文章节 | [nature-writing](skills/nature-writing/SKILL.md) |
| 学术润色与文风修订 | 保持论证、科学含义和主张强度，润色、翻译或压缩已有文本；按需修订公式化或防御性表达 | [nature-polishing](skills/nature-polishing/SKILL.md)、[humanizer-zh](skills/humanizer-zh/SKILL.md)、[Humanizer](skills/humanizer/SKILL.md)、[anti-defensive-writing](skills/anti-defensive-writing/SKILL.md) |
| 开题与研究计划 | 按已确认题目、学校或项目模板撰写开题报告、项目书与研究计划 | [researchwrite](skills/researchwrite/SKILL.md) |
| 科研图件 | 图件叙事、多面板设计、核验数据绘制、投稿格式导出与审查；机制图提示词另有支持 | [nature-figure](skills/nature-figure/SKILL.md)、[nature-image2-prompt](skills/nature-image2-prompt/SKILL.md) |
| 证据与投稿前审查 | 溯源和可复现性审计、审稿人视角评估、统计报告检查、数据可用性说明 | [evidence_audit](skills/evidence_audit/SKILL.md)、[nature-reviewer](skills/nature-reviewer/SKILL.md)、[nature-statistics](skills/nature-statistics/SKILL.md)、[nature-data](skills/nature-data/SKILL.md) |
| 审稿回复 | 按审稿人分别组织回复、返修信与修改片段，保持正文和回复内容一致 | [nature-response](skills/nature-response/SKILL.md) |
| 格式与汇报材料 | 修订论文排版，制作论文汇报 PPT，或把图片、扫描页面重建为可编辑幻灯片 | [paper_format](skills/paper_format/SKILL.md)、[nature-paper2ppt](skills/nature-paper2ppt/SKILL.md)、[nature-image2ppt](skills/nature-image2ppt/SKILL.md) |
| 周期文献追踪 | 在明确授权的来源、频率和交付渠道内发现、筛选、阅读和归档文献 | [nature-literature-pipeline](skills/nature-literature-pipeline/SKILL.md) |

Nature 技能按需使用 [nature-shared](skills/nature-shared/SKILL.md) 的共享参考，
它承担参考支持。ARS 保留为停用的备选材料；本机独立 `scientific-agent-vnext`
候选仅供明确选择的任务使用。默认写作使用 Nature，不自动混用其他写作体系。

## 工作原则

- **作者掌握科学方向。** Agent 提供证据、比较和建议；研究问题、关键方法取舍、
  核心主张和受保护产物的改变由作者决定。
- **证据定位到原文。** 检索命中、知识库片段、引文数和模型评分提供线索。
  重要主张回到原论文、数据或结果，并保留来源、定位及适用范围。
- **职责围绕交付物。** 写作负责论证，润色保持既有论证；核验数据可直接绘图，
  新计算由分析技能承担。复用已有有效结果，按具体缺口补充检查。
- **从用户指定阶段开始。** 领域地图、想法审查、实验设计、写作或润色均可单独完成。
  不默认启动完整阶段链、多代理、日程或自我修改。
- **科研假说可被否定。** 区分观察与解释，考虑竞争机制、负结果和反向结果。
  检索空白或图谱空格不能单独证明创新，相关性或模拟收益不能单独证明因果。
- **保持连续性与干净交付。** 复用项目已有背景、决定和状态记录。
  正式正文与提纲、证据说明、修改记录分开。

## 使用示例

在已安装本地技能的会话中，用自然语言说明任务、输入材料和约束：

```text
调用 Research agent，围绕这个方向做领域地图，核查最接近的先行研究，比较可检验的假设。
调用 Research agent，比较这两个方法的数据需求和验证能力，我来决定采用哪个。
调用 Research agent，基于这份已确认的大纲修改引言，保持研究问题和引用不变。
调用 Research agent，只润色这段已有文本，保留论证结构和科学含义。
调用 Research agent，检查这个分析结果能支持什么结论，先只读。
调用 Research agent，用这份已核验数据绘制多面板图，交付可编辑矢量文件。
调用 Research agent，依据学校模板和已有初稿完善开题报告。
调用 Research agent，检查这份审稿回复与修改后的正文是否一致。
```

已有稿件、数据、提纲和项目约定是相应任务的输入权威。说明哪些材料已经确认、
哪些可以修改，以及期望的交付物，有助于缩小检索和修改范围。

## 项目上下文与证据治理

项目事实和已确认决定保留在研究项目中。现有 `.agent/NEXT.md`、
`STATE.md` 等文件承担跨会话恢复，原始资料和分析结果承担证据权威。
任务内复用足够的记录，避免在提案、技能模板和工作包之间重复维护同一状态。

已接入 OpenSpec 1.12.0。对明确使用 OpenSpec 的任务，`research-task` 工作包
链接科学要求、实现步骤与实际验收证据；普通检索、润色等任务可以直接执行。
工作包完成或文件齐全不能代替科学验收。详见
[系统边界](docs/architecture.md)和[OpenSpec 科研使用说明](docs/openspec_usage.md)。

## 源码维护与安装

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
- [技能重叠与精简审查](docs/architecture_review.md)
- [科学发现建议与本地优化](docs/scientific_discovery_review.md)
- [参考项目比较与选择](docs/reference_projects.md)
- [行为评估方法](docs/behavioral_evaluation.md)
- [迭代与贡献](CONTRIBUTING.md)
- [优先级路线](docs/roadmap.md)
- [迁移验证记录](docs/validation.md)
- [第三方来源与许可](THIRD_PARTY_NOTICES.md)
