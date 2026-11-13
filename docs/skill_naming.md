# Research Agent 技能命名

2026-10-23 本轮功能精简：29 个相关安装条目减为 27 个（含内部共享依赖）。
`nature-experiment-plan` 已并入 `nature-method-design` 的 experiment-plan 模式；
`academic-humanizer` 已并入 `nature-polishing` 的 academic-humanization 模式。
旧目录移出技能发现范围，不留别名；正文、许可和例子保留在对应模式及本地恢复副本。
模拟审稿默认单份报告；多份隔离审稿仅按明确请求使用。保留证据、权限及科学主张边界。
以下较早日期的数量和分工只作历史记录，以本段及当前入口为准。

本页记录命名迁移。同日后续功能审查已将 8 个独立入口合并为现有技能的按需模式；
下面更名表不是当前完整入口清单。当前功能分工和全部合并去向见
[技能功能审查](skill_function_audit.md)。例如 `res_analyze` 的结果解释现为
`nature-data-analysis` 的 result-interpretation 模式，图件扩展成为
`nature-figure` 的条件资源，不再有独立调用入口。

2026-10-13 按作者要求，科研流程技能统一使用 `nature-<capability>`：小写英文、
连字符分词、完整功能名称，目录名与 `SKILL.md` 的 `name` 一致。
本地扩展采用相同命名空间以便与现有 Nature 技能配合；这不表示它们来自上游。

`research-agent` 保留为公开协调入口。Humanizer、EditaPlot 等独立通用工具
保留其上游身份。原有 `nature-*` 技能继续沿用既有名称。

| 原名称 | 命名迁移时名称 | 工作单元 |
|---|---|---|
| scientific-insight | nature-scientific-insight | 科研洞察与判断（核心） |
| res_find | nature-research-discovery | 领域梳理与候选问题发现 |
| res_method | nature-method-design | 已选问题的方法设计 |
| res_plan | nature-experiment-plan | 实验、分析及验证计划 |
| res_analyze | nature-result-interpretation | 已完成结果的科学解释 |
| data_analyze | nature-data-analysis | 可复现数据分析与统计计算 |
| evidence_audit | nature-evidence-audit | 证据溯源与可复现性审计 |
| literature_kb | nature-literature-kb | 已注册本地论文库查询与维护 |
| lit_synthesis | nature-literature-synthesis | 系统综述方法与跨论文证据综合 |
| paper_format | nature-paper-format | 学术材料排版与格式检查 |
| researchwrite | nature-proposal-writer | 项目书、开题与研究计划文档 |
| research-scholar-distiller | nature-scholar-distiller | 公开学术材料的判断框架蒸馏 |
| anti-defensive-writing | nature-anti-defensive-writing | 起草后的特定修辞修订 |
| figure_benchmark_library | nature-figure-benchmark | 参考图件筛选与设计规则提取 |
| ncs_figure_corpus_builder | nature-figure-corpus | 图件参考语料整理与授权入库 |

命名迁移时前 13 项在本仓库维护源码，后两项为既有本机扩展。
后续功能精简将两项图件扩展的有用指导与脚本并入 figure 模式资源，
仅在所请求的参考图任务中加载，不作为普通绘图的默认阶段。

## 安装与引用

2026-10-23 按作者要求，Research Agent 的相关研究技能、Humanizer、EditaPlot
及共享依赖统一到用户级 `.agents/skills/`。这取代更名时保留双安装根目录的安排；
不保留旧目录别名或重复安装。运行时仍应从实际技能清单定位。

目录、frontmatter、界面调用提示、当前路由、跨技能资源链接及上游映射共同更新。
旧名称不保留重复安装或目录别名。自然语言仍可通过“调用 Research agent，……”
表达任务；显式 `$skill-name` 调用采用新名称。客户端缓存旧清单时需刷新或新建会话。

更名不迁移知识库后端、项目产物或归档目录，不改绑定文件的内部 schema key。
历史导入清单、旧维护报告及 release 记录保留原始名称；其名称不能作为当前入口。
`nature-proposal-writer` 与 Nature 上游的 `skills/nature-proposal-writer` 直接对应。
任务职责、科学判断细则与既有权限边界保持原有定义。

本次只核验名称、引用、安装同步与原生发现；不执行独立模型评测，
不将结构检查视为自然路由准确率或科研判断质量提升的证据。

## ARS 选择性安装补充（2026-10-25）

按作者要求，ARS 精选规划版保留上游标识 `academic-research-suite`，只增加
这一个发现入口；它不更名为 Nature 技能，也不安装多份同义别名。
`research-agent` 继续协调任务，Nature 命名与已合并模式保持不变。
职责边界见 [ARS 与 Nature 协作](ars_nature_workflow.md)。
