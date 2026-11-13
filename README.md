# Research Harness · Research Agent

[English](README.en.md) · [安装与配置](docs/installation.md) · [使用示例](examples/research_brief.md) · [贡献指南](CONTRIBUTING.md)

面向环境与地球科学的、研究者主导的科研技能工具集，覆盖水、土、气、生（water, soil, atmosphere and ecology）。一个 Research Agent 入口按任务协调选题、文献、方法、分析、图件、写作与返修；已有问题、数据或手稿可以直接进入相应任务。

研究者决定科学方向和核心主张。Agent 在授权范围内完成检索、实现、验证与交付，保留原文定位、数据依据、不确定性和反证。

## 快速开始

需要 Python 3.10+，以及能加载本地 Agent Skills 的 Codex 环境。安装脚本只使用 Python 标准库；模型访问由你自己的运行环境提供。

~~~powershell
git clone https://github.com/CALEBY9/Research-harness.git
cd Research-harness
python -X utf8 -B scripts/harness.py validate
python -X utf8 -B scripts/harness.py install --target ~/.agents/skills --dry-run
python -X utf8 -B scripts/harness.py install --target ~/.agents/skills
python -X utf8 -B scripts/harness.py check --target ~/.agents/skills
~~~

同一组 Python 命令可在 PowerShell、Bash 或 zsh 中使用。安装器展开 ~，默认安装目录已在命令中明确指定。已有同名文件或目录会使安装停止，不会覆盖你的技能、配置或研究材料。

在自己的研究项目目录中启动 Codex，确认技能列表包含 research-agent；未刷新时重启会话。然后输入：

> 调用 Research agent。请基于我提供的材料，先识别当前需要完成的研究任务，再在证据允许的范围内执行。保留我已确认的研究问题与主张；需要改变科学方向时给出依据和选项。

先尝试不需要私有知识库的[完整输入示例](examples/research_brief.md)。项目级安装、选择安装、更新与故障处理见[安装说明](docs/installation.md)。Codex 的发现位置与刷新行为参见 [OpenAI Docs](https://learn.chatgpt.com/docs/build-skills)。

## 能做什么

| 任务与交付物 | 主要技能 |
|---|---|
| 找方向、选题收敛、文献调研、初始研究或论文框架 | academic-research-suite（ARS 精选入口） |
| 研究价值、创新性、核心主张与研究去留判断 | nature-scientific-insight |
| 从已有环境观测发展过程假设与区分性验证 | nature-research-discovery |
| 研究设计、方法方案与完整实验计划 | nature-method-design |
| 文献检索、引文核验、全文获取与单篇精读 | nature-academic-search、nature-downloader、nature-reader |
| 数据分析、统计报告、证据审计与数据可用性 | nature-data-analysis、nature-statistics、nature-evidence-audit、nature-data |
| 科研图件、论文汇报、图片恢复为可编辑 PPT | nature-figure、nature-paper2ppt、nature-image2ppt |
| 论文正文与论证重构、润色与学术去 AI 味、格式整理 | nature-writing、nature-polishing、nature-paper-format |
| 开题与研究计划、模拟审稿、审稿回复 | nature-proposal-writer、nature-reviewer、nature-response |
| 本地文献库接入与周期文献追踪 | nature-literature-kb、nature-literature-pipeline（需配置相应服务） |
| 请求的怀疑性批评、跨领域决策、公开学者框架蒸馏 | ai-skeptic、nature-decision、nature-scholar-distiller |

完整分工见[技能功能说明](docs/skill_function_audit.md)，ARS 与 Nature 的边界见[协作说明](docs/ars_nature_workflow.md)。中文通用编辑由 humanizer-zh 提供；nature-shared 与 shared-references 提供共享资源。

其他学科可以复用检索、阅读、写作和审计模块；完整研究设计应结合该学科的对象、方法、代表文献和验证标准。跨学科适用性属于设计范围，不代表已完成各专业的实际效果验证。

## 科研协作原则

- 围绕新增知识组织研究：最接近的先行研究、残余贡献、可行数据与否定条件一起比较。
- 原始证据贯穿论证：检索命中只是候选；关键主张回到论文原文、数据与计算结果。
- 有可用本地论文库时优先利用；没有绑定时使用用户提供的论文或公共检索，不虚构本地检索结果。
- 学习已发表论文时看摘要、引言、结果与讨论共同构成的故事，而不只模仿句式。
- 正文、图件、引用与回复保持一致；正式稿与修改理由、检查记录分别交付。
- 按当前交付物组合技能，不默认运行从选题到投稿的自动流水线，不默认调用多个代理或付费评测。

## 安装包含什么

[分发目录清单](skills/catalog.json)明确列出 29 个启用技能，包括内部共享技能 nature-shared。默认还安装 shared-references，以及许可和来源说明。选择单个技能时，同样会带上共享资源。

旧 ars-academic-writing 仅保留为历史参考，不进入默认或选择安装。未确认再分发许可的 figures4papers 参考文件不进入当前分发；本机保留文件不受影响，历史 Git 提交未改写。

本仓库提供技能说明、参考资源和已有工具脚本。下列能力按需要另行配置：

| 能力 | 需要自行提供 |
|---|---|
| 模型与工具执行 | Codex 运行环境、自己的模型访问和工具权限 |
| 本地文献库 | 自己的语料、索引及兼容后端；作者的私有库和 research_library.py 后端不随仓库提供 |
| 外部文献与全文服务 | 相应网络、账户、API 配置或机构权限 |
| 文档、PDF、PPT 与专业绘图 | 相应文档工具和模块依赖；EditaPlot、Origin、Office、Tabbit 不在本包内 |
| 周期监测与通知 | 明确配置的调度器与通知服务；安装不会创建后台任务 |

不需要一次装齐所有可选软件。文本研究任务可从用户提供的材料开始；请求某项文件生成或工具操作时，再核对该项依赖。

## 验证与支持范围

~~~powershell
python -X utf8 -B scripts/harness.py validate
python -X utf8 -B -m unittest discover -s tests -v
python -X utf8 -B scripts/harness.py doctor
~~~

validate 检查源码结构、语法、启用清单和已知凭据模式；check 检查安装文件及共享资源；doctor 提示路径依赖和可选知识库绑定。它们不调用模型、不证明科研判断或论文质量。

[GitHub Actions](.github/workflows/validate.yml) 配置了 Windows、Linux、macOS 与 Python 3.10/3.13 的离线检查和安装测试。工作流配置不等于各平台已经通过；请以对应提交的 Actions 结果为准。维护测试中的可选外部工具缺失会明确跳过。

结构检查、真实任务行为和科研效果分开报告；历史记录见[验证记录](docs/validation.md)。当前没有跨模型性能排名或自主科研成功率承诺。

## 许可与贡献

原创贡献采用 [Apache-2.0](LICENSE)。第三方组件保留原许可：ARS 内容为 CC BY-NC 4.0，Humanizer 相关内容保留 MIT，Nature 组件保留其 Apache-2.0 及子组件声明。整包不能视为无条件的 Apache-2.0 授权；复用前阅读[第三方说明](THIRD_PARTY_NOTICES.md)。

欢迎提交可复核的问题、文档修正和聚焦的改进。提供最小脱敏输入、实际命令与错误，避免上传私有论文、账户或完整研究数据。参见[贡献指南](CONTRIBUTING.md)和[安全报告](SECURITY.md)。

- [系统边界](docs/architecture.md)
- [安装、配置与更新](docs/installation.md)
- [使用示例](examples/research_brief.md)
- [迭代路线](docs/roadmap.md)
- [参考项目及设计来源](docs/reference_projects.md)
