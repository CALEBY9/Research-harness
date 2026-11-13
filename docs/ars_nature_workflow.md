# ARS 与 Nature 的协作分工

2026-10-25 根据作者要求启用一个 ARS 精选入口 `academic-research-suite`。
Research Agent 继续负责按当前交付物选择技能，不建立新的总控流水线。

| 需要完成的事 | 默认技能 | 完成边界 |
|---|---|---|
| 找方向、收敛题目、提出候选问题 | ARS `academic-research-suite` | 可核对的先行工作、差异、数据路径与候选建议 |
| 从已有环境观测、数据条件或先行研究发展过程假设及区分性验证 | `nature-research-discovery` | 有依据的竞争假设、可区分的观测与最小验证，不展开完整实验方案 |
| 做领域/文献调研 | ARS `academic-research-suite` | 实际检索轨迹、证据矩阵、研究脉络、冲突与缺口 |
| 搭研究框架、初始论文大纲与论证骨架 | ARS `academic-research-suite` | 问题—证据—章节对应关系，不编造结果或先写正文 |
| 精读单篇、Paper Card、全文翻译 | `nature-reader` | 原文定位与指定深度的阅读产物 |
| 给已有主张补引用、书目核验、RIS/BibTeX | `nature-academic-search` | 按请求完成引用工作，不重做领域调研 |
| 已给定想法的价值、新颖性或证据判断 | `nature-scientific-insight` | 有依据的科学建议，作者保留决定 |
| 具体研究方法、实验与验证计划 | `nature-method-design` | 已选问题的可实施方案 |
| 正式系统综述、筛选编码或 meta-analysis 方法 | `nature-literature-synthesis` | 正式方法与证据资产，不将探索调研升格为完整系统综述 |
| 论文正文、学位论文与综述章节正文 | `nature-writing` | 复用已确认框架，完成实际正文 |
| 数据计算与结果解释 | `nature-data-analysis` | 实际计算或复用已有结果 |
| 科研图件 | `nature-figure` | 使用真实证据设计、绘制并验证图件 |
| 润色、翻译、压缩、学术去AI味 | `nature-polishing` | 保持事实、引用、论证与确定程度 |
| 首次投稿、审稿、返修、排版 | 对应 Nature 技能 | `nature-writing`、`nature-reviewer`、`nature-response`、`nature-paper-format` |
| 开题报告、项目书与正式研究计划 | `nature-proposal-writer` | 使用已确认问题与方案撰写文档 |

Research Agent 根据任务与材料自动识别领域并选择技能，无需作者确认学科或
指定技能。仅有环境科学主题的宽泛选题、调研或框架仍走 ARS；要求从已有
观测、数据条件或先行研究发展环境过程假设及区分性验证时，自动使用
`nature-research-discovery`。尊重作者已指定的技能，同一任务不重复运行
两套发现。必要的方法判断可以复用
`nature-scientific-insight` 的标准，不把它变成每次调研的强制预审。

## 本次实际选取的 ARS 内容

来源为 ARS-Codex `3.23.1` 的固定提交
`8d6a1f856ee3da9d3a5e2b7f292b3dfe72b592c5`。选择问题工程与 FINER、
苏格拉底提问、文献检索策略、证据矩阵、跨文献综合、研究架构、论文结构、
CER 论证与反证检查。它们适配为一个入口与三份按需参考，保留来源与
CC BY-NC 4.0 许可，详见
[来源说明](../skills/academic-research-suite/references/provenance.md)。

未安装上游完整写作、摘要、审稿、返修、排版、实验、研究筛选或端到端
流水线，也未安装其 runtime、scripts、hooks、模型分配、自动代理和更新器。
旧 `ars-academic-writing` 仍保留为非活跃历史源码。Nature 现有功能与已合并
模式保留，调整的是默认前期任务归属及其发现描述。

## 如何使用

- “调用 Research agent，调研海上风光养殖共址的研究脉络，找出有证据依据的候选问题。”
- “调用 Research agent，基于这份已确认的文献矩阵搭研究框架和论文大纲，先不要写正文。”
- “调用 Research agent，框架已经确认，按这些真实结果起草中文引言。”
- “调用 Research agent，精读这篇论文，然后按我指定的证据画图。”

也可直接调用 `$academic-research-suite`；界面名称为“ARS · 选题、调研与框架”。
本版理解 `ars-plan`、`ars-outline` 和 `ars-lit-review` 的文本意图，不新增
slash command 注册或其他 ARS 子技能入口。

## 交接与验证范围

ARS 向 Nature 提供已确认的问题与边界、文献矩阵及原文定位、研究/论文框架、
数据和结果状态、未解决的证据问题。复用项目已有权威报告和 `.agent/` 指针，
不强制新建护照、阶段目录、JSON 或评分台账。已完成的调研不因交接重跑。
用户明确要求组合任务时在授权范围内继续，单独的框架任务则在框架处结束。

安装检查应区分技能结构、源码与安装一致性、资源链接、原生技能发现以及
实际科研行为。前四类检查通过不能证明科学质量或效率提升；行为表现留待
已授权真实项目观察，不默认新增模型基准、A/B 或独立评审轮次。
