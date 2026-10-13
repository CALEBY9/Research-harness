# Research Agent 全部技能功能审查

2026-10-13 按作者要求审查更名后的本机技能，并实施精简。检查对象是维护源码、
实际安装、技能触发描述、任务产物、共享引用和相关脚本；不是仅比较名称。
共覆盖 37 个相关已安装条目：34 个仓库维护条目、2 个本机图件扩展、EditaPlot。
ARS 已不在本机技能发现目录，仅检查其现有版本化参考引用，不恢复入口。
系统、插件及非科研工具不属于本轮删除范围。

移除 **8 个重叠的独立入口**，其必要内容并入 **5 个现有技能的按需模式**。
精简后保留 29 个相关已安装条目，其中 28 个在本仓库维护，另一个是独立
EditaPlot。28 个维护条目包含协调入口、25 个 Nature 条目及 2 个 Humanizer；
`nature-shared` 是内部依赖，不承担用户工作流。

## 删除的独立入口与功能去向

| 原入口 | 审查判断 | 保留位置与调用方式 |
|---|---|---|
| `nature-citation` | 特定期刊来源限制是检索模式；独立入口与检索、核验和导出重复 | [nature-academic-search / cns-citation](../skills/nature-academic-search/references/cns-citation/guide.md)：明确要求 CNS 来源时使用；保留期刊范围、主张级来源和作者完整导出脚本 |
| `nature-ref-verifier` | 参考文献核验已经是 academic-search 工作流，原独立入口又做同一次查询 | [nature-academic-search / reference-verification](../skills/nature-academic-search/references/reference-verification/guide.md)：保留作者顺序、DOI/标题、卷期页及版本差异核验，复用查询记录 |
| `nature-paper-card` | 单篇深读与全文 reader 使用同一文献源，差别是交付深度和格式 | [nature-reader / paper-card](../skills/nature-reader/references/paper-card/guide.md)：保留卡片结构、论文类型、原文定位状态及准备/审计脚本；无需先完成全文翻译 |
| `nature-anti-defensive-writing` | 特定修辞问题属于既有文本润色，不需要第二个后处理入口 | [nature-polishing / anti-defensive-writing](../skills/nature-polishing/references/anti-defensive-writing/guide.md)：按问题加载，保留负结果、不确定性、因果边界及作者主张 |
| `nature-image2-prompt` | 机制图提示词是图件产出的一种模式，与 figure 规划和语义交接重复 | [nature-figure / conceptual-prompts](../skills/nature-figure/references/conceptual-prompts/guide.md)：保留线框、可见文字、已选视觉方向、作者批准及提示词审查；只请求提示词时不启动生成 |
| `nature-figure-benchmark` | 参考图件筛选和设计规则属于 figure 的条件性辅助模式 | [nature-figure / figure-benchmark](../skills/nature-figure/references/figure-benchmark/guide.md)：保留候选检索、来源核验、转用/拒绝规则及选择脚本；不作为普通绘图的必经阶段 |
| `nature-figure-corpus` | 参考材料整理与图件基准共用同一资源；无需单独发现入口 | [nature-figure / figure-corpus](../skills/nature-figure/references/figure-corpus/guide.md)：保留清单脚本、暂存审核、版权、共享写入授权及回滚约束 |
| `nature-result-interpretation` | 解释输出与分析技能已有的诊断/报告交付重叠 | [nature-data-analysis / result-interpretation](../skills/nature-data-analysis/references/result-interpretation/guide.md)：只需解释时复用已完成计算；主张选择仍交给核心判断技能 |

上述模式只含 `guide.md` 及支持资源，不含嵌套 `SKILL.md` 或独立调用元数据。
旧目录移出发现范围，无旧名别名。删除入口没有删除上述必要能力，也不会默认
加载全部模式。迁移的 Python 帮助脚本及其测试保留原实现。

## 保留的条目及独立职责

| 条目 | 核查后的职责 | 保留依据及边界 |
|---|---|---|
| [research-agent](../skills/research-agent/SKILL.md) | 按用户交付物协调实际可用技能 | 公开协调入口；不重复实施各专业技能、不强制整条阶段链 |
| [nature-scientific-insight](../skills/nature-scientific-insight/SKILL.md) | 研究价值、先行研究重合、残余贡献、解释与主张选择、下一步科学取舍 | 核心科研判断；作者保留方向和核心主张决定，未知与反证分开 |
| [nature-research-discovery](../skills/nature-research-discovery/SKILL.md) | 建立领域地图、发现有来源的可检验候选问题 | 产物是新候选及比较；已有想法的独立价值判断使用核心技能 |
| [nature-method-design](../skills/nature-method-design/SKILL.md) | 把作者选定的问题细化为数据可得、可实施的方法方案 | 方法选择与问题/数据约束；不自动进入完整实验或分析执行 |
| [nature-experiment-plan](../skills/nature-experiment-plan/SKILL.md) | 已选问题的对照、基线、数据、实验/分析、验证及图表路线 | 完整执行计划不同于方法提案；不把计划写成已完成结果 |
| [nature-scholar-distiller](../skills/nature-scholar-distiller/SKILL.md) | 从学者公开原始研究提取可复核的研究判断框架 | 用户明确需要的专门产物；不代表学者本人或声称其授权认可 |
| [nature-academic-search](../skills/nature-academic-search/SKILL.md) | 一次性文献检索、引用语境/严格他引、元数据核验和参考文献文件 | 合并一般检索、CNS 限制及字段核验；元数据正确不等于支持论文主张 |
| [nature-downloader](../skills/nature-downloader/SKILL.md) | 合法获取全文、补充材料及机构访问路径 | 全文访问、权限与下载不同于理解内容；不保证每个服务当前可用 |
| [nature-reader](../skills/nature-reader/SKILL.md) | 单篇证据卡、中文解释性深读或明确要求的完整/双语 reader | 按交付深度选模式；保留图表、方程、源定位和材料缺失说明 |
| [nature-literature-kb](../skills/nature-literature-kb/SKILL.md) | 已注册本地语料后端的构建、检查与查询 | 语料/后端/索引实际绑定不同于外部检索；命中不是主张已核实 |
| [nature-literature-synthesis](../skills/nature-literature-synthesis/SKILL.md) | 系统综述协议、筛选编码、跨论文综合及元分析方法 | 可复核综合资产不同于单篇阅读或临时检索；数值计算与正文各有 owner |
| [nature-literature-pipeline](../skills/nature-literature-pipeline/SKILL.md) | 明确授权的周期检索、筛选、阅读、交付和归档 | 调度、去重及持续归档是独立需求；不因安装技能自动建任务或发消息 |
| [nature-data-analysis](../skills/nature-data-analysis/SKILL.md) | 可复现计算、诊断、表图及完成结果解释 | 区分新计算与解释已有结果；不替作者选论文核心主张 |
| [nature-statistics](../skills/nature-statistics/SKILL.md) | 样本/重复、效应量、CI、假设、多重比较及稿件统计报告 | 报告/审查交付不同于运行数值分析；不默认重算全部统计 |
| [nature-evidence-audit](../skills/nature-evidence-audit/SKILL.md) | 来源、数据/代码/数字、可复现性及提交证据核验 | 审计可靠性不同于选题价值或正式模拟审稿；脚本通过不能证明科学主张 |
| [nature-writing](../skills/nature-writing/SKILL.md) | 论文、学位论文章节及实质论证重构 | 主张与段落结构的写作 owner；保留已确认对象、提纲、证据和 clean final |
| [nature-polishing](../skills/nature-polishing/SKILL.md) | 同论证润色、翻译、压缩及特定修辞修订 | 不另选故事或提升主张强度；专项修辞修订不强制成为第二遍检查 |
| [nature-proposal-writer](../skills/nature-proposal-writer/SKILL.md) | 项目书、开题和研究计划文档 | 学校/资助模板、计划性语言不同于完成研究的论文正文 |
| [nature-figure](../skills/nature-figure/SKILL.md) | 图件叙事、绘制/导出/审查、概念提示词及按需参考图模式 | 数据图与概念图按需处理；共享语料入库权限、原始数据及作者批准继续有效 |
| [nature-data](../skills/nature-data/SKILL.md) | 数据可用性、仓库/编号、限制共享、数据引用及 FAIR/source-data 包 | 实际共享与声明是独立投稿交付；不同于计算或内部溯源审计 |
| [nature-reviewer](../skills/nature-reviewer/SKILL.md) | 审稿人视角的投稿前 Major/Minor concerns 和阻断项 | 正式审稿报告不同于核心研究取舍或来源核验；不自动成为所有任务的终点 |
| [nature-response](../skills/nature-response/SKILL.md) | 按审稿人分隔的返修回复、rebuttal 和相关修订材料 | 有收到的评论、回复定位及跨文件一致性约束；不同于投稿前 review |
| [nature-paper-format](../skills/nature-paper-format/SKILL.md) | DOCX/LaTeX/Markdown 等的版式、模板和页面检查 | 格式修改不重写科学内容；与语言润色、论证重构分开 |
| [nature-paper2ppt](../skills/nature-paper2ppt/SKILL.md) | 从论文/阅读笔记编写完整学术汇报 PPT | 创建汇报故事与讲稿，区别于恢复已有图片幻灯片 |
| [nature-image2ppt](../skills/nature-image2ppt/SKILL.md) | 截图、扫描或图片幻灯片恢复为对象级可编辑 PPT | 原版重建、对象可编辑性及渲染验收不同于新写演示文稿 |
| [nature-shared](../skills/nature-shared/SKILL.md) | 科学证据、术语、写作与期刊的共享参考 | 现有多个技能的必需依赖；仅加载调用方明确需要的文件 |
| [humanizer](../skills/humanizer/SKILL.md) | 一般英文表达的文风修订 | 独立通用工具，可用于非科研文字；不成为科研判断或写作默认 owner |
| [humanizer-zh](../skills/humanizer-zh/SKILL.md) | 一般中文文字的空话、重复和模板表达修订 | 独立中文通用工具，保留事实、确定程度和作者声音 |
| EditaPlot（本机独立工具） | Origin/OriginPro 的对象级可编辑图表及其运行环境 | OPJU、Origin 实例与回读是具体工具能力；不与 figure 默认同时渲染同一图 |

## 同步修正的真实问题

- Reader 原描述排除 Paper Card，正常路由要求全文输出；现在先选择深读卡片或
  明确要求的完整 reader，避免无关全文翻译及同时加载两套核心。
- Polishing 快速路径排除全部按需资源，与专项修辞修订相冲突；现在只在该问题
  被请求或实际出现时加载对应指导，不捕获普通语言润色任务。
- 图件参考模式的帮助脚本与概念图交接路径改为实际模式目录，移除合并后产生的
  “先调用自己、再调用自己”表述；原语义、版权、共享写入与回滚约束保留。
- 参考核验原指导把 Crossref 404 当成 DOI 错误，又承认覆盖缺口；现在区分端点
  未命中、访问失败、版本差异和已核实的错误。DOI 字符串不用于推断出版年份，
  合规的 et al./等不判为作者遗漏，出版方与聚合元数据冲突显式报告。
- 周期文献技能的无依据本机“production-tested”表述移除。配置准备、实际激活及
  成功交付分开，既有显式自动化授权不变。
- 当前路由、调用元数据、相对资源链接、导入名单、上游活动映射及维护回归定义
  同步。回归定义区分 owner 与 mode，不能把禁止“新计算”误变成禁止解释 owner。

## 合并后的文本冲突修正

首次精简消除了独立入口重叠，但未完全解决父级通用流程与模式局部规则的
冲突。后续文本审查发现四类残留，2026-10-13 已在源码与本机安装副本中修正：

| 冲突 | 当前执行边界 |
|---|---|
| Paper Card 已选定，后文仍要求每次执行完整 reader 流程 | 卡片模式使用自己的 manifest，完成即返回；完整 reader 的核心和格式轴只用于完整输出。明确同时请求两种输出时复用原文提取与定位。 |
| 仅需提示词、参考图分析或清单，仍进入绘图后端及 PDF 验收 | 先按交付物选模式；非绘图模式完成即返回。仅规划/审查不启动渲染；实际源码和 PDF 才执行对应检查，明确要求的缺失文件仍属交付缺口。 |
| 用户已有文本，专项修辞指南却要求先起草；语言修订可能被扩大 | 接受已有原文直接修订；仅在同时请求起草时后置处理。LANGUAGE_ONLY 保留 hedge、主张强度、段落功能与顺序；科学含义或论证变化仍由写作 owner 和适用的作者/证据约束控制。 |
| 仅解释完成结果，后文仍要求计算或交接给自己 | 解释模式复用已有输出并完成返回；缺少计算明确报告，仅对实际请求或已有授权的计算进入计算分支，不重新调用自身。 |

相关修正包括：泛指 Image 2 不再绑定 OpenRouter，服务选择服从用户或已授权的
项目配置；已批准的概念图语义与视觉方向不重新探索；CNS 子模式的“无内容轴”
不再误述为父技能没有工作流轴；检索、核验和导出复用已有记录，局部文件转换
不默认触发远程查询。参考图子模式的自交接和遗漏的帮助脚本旧路径也已修正；
仅清点素材不进入设计提取或共享入库。调用元数据及既有回归定义同步修正，未增加新的独立入口、
自动阶段链、依赖、提供方配置或模型评测。

这些修正落实了文本分支边界，不能证明模型在实际任务中不会误选或漏执行。
自然调用准确率与科研判断质量继续留待真实项目观察。

## 安装、来源与验证边界

本机源码与安装同时维护；保留实际 `.codex/skills/` 与 `.agents/skills/` 根目录。
8 个旧入口和 6 个对应源码目录移出发现范围，备份放在忽略的本轮维护记录中。
不恢复旧 paper_* / Research workflow / ARS 默认入口，不改独立工具或私人后端。

[Nature 上游映射](nature_upstream.json)只监测仍存在的 15 个活动 Nature 条目。
合并的 3 个上游独立模块保留原始来源路径和本地资源位置，属于本地按需资源；
其后续上游差异需选择性审阅，监测不会自动恢复旧独立入口。两项图件扩展的
帮助脚本本轮首次作为模式资源纳入源码，保留原实现及本机路径边界。

本轮验证文件同步、资源引用、迁移脚本的相关测试和 Codex 原生技能发现，
不调用模型，不执行独立行为基准或完整测试套件。精简可确认发现目录更少、
维护绑定有效；自然调用准确率与科研判断质量仍应在后续真实项目观察。
文献服务、机构权限、共享语料、Office/Origin 等外部依赖没有因本轮审查而得到
端到端可用性认证。历史测试和旧名称迁移报告保留其日期与范围。
