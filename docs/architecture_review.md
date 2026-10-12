# Research Harness 架构重叠审查

审查日期：2026-10-12。范围为仓库维护源码、项目级技能、相关文档与本机安装入口。
本轮目标是减少职责争抢和重复工作，不改变作者的 Nature 默认选择。

## 诊断结论

原建议识别了边界膨胀的风险，但部分判断把主题相关当成能力重复，或把已经停用的
候选当作默认运行入口。当前仓库维护 34 个技能源码目录，另有无独立入口的
`shared-references`；项目级安装包含六个 OpenSpec 技能和一个显式候选 vNext。
这些目录不是 41 个默认并行运行的 Agent。数量本身不足以证明应删除。

本机审查时，34 个技能的 721 个源码文件与对应安装文件一致。ARS 的技能配置为
`enabled=false`；项目 vNext 的 invocation policy 为 `allow_implicit_invocation=false`。
这些是本轮读取的状态，不依赖旧的私有仓库或 ARS 默认时期的记录。

| 原建议 | 当前证据与判断 | 本轮处置 |
|---|---|---|
| proposal 与论文写作切开 | `nature-writing` 与 `researchwrite` 描述已切开，但后者正文、QA 示例、README 和 manifest 仍接收论文 Discussion、独立综述及邮件 | 删除这些入口；背景综述限定为 proposal 内的章节 |
| polishing 仅允许语法级编辑 | LANGUAGE_ONLY 路径已存在，但 fuller route 仍把论证/证据重构列为自身模式，并有独立 LaTeX 排版入口 | 保留同论证句子改写、翻译与压缩；论证重构交给写作，排版交给格式 owner |
| figure 只设计、不绘图 | `nature-figure` 本身有已维护的 Python/R 后端、导出与图件检查；禁止绘图会削弱完整交付。真实冲突是所有定量渲染都强制加载 `data_analyze`，后者又宣称独占图件执行 | 图件 owner 可直接使用核验数据渲染；仅在有新计算缺口时加载分析支持，避免双执行器 |
| Evidence、Claim、Reviewer 合并 | `evidence_audit` 检查溯源/复现，`res_analyze` 解释完成结果，`nature-reviewer` 产出模拟审稿意见；没有另外的独立 Claim Validator 入口 | 保留职责，路由明确复用已有检查；不新增总验证 Agent，不削弱既有证据 closeout 与独立审稿要求 |
| 删除 ARS 默认入口 | 本机入口已经禁用，router 不自动混用 ARS；但 ARS 自身 frontmatter 仍自称 Research Agent 写作 owner | 改为停用参考说明；保留可回退源码，不删除目录或更改配置 |
| 所有任务统一进入 OpenSpec | router 与 OpenSpec reference 已限定为显式使用或既有项目；Research Code Spec 已允许复用 figure/analysis contract。真实重复风险是 researchwrite 默认新建 foundation 和 `state.json` | 保留可选 OpenSpec，proposal 复用现有科学文档与任务记录；模板按需补缺，不建立状态镜像 |
| 合并/删除重复写作技能 | `lit_synthesis` 接口说只负责方法和证据资产，但 frontmatter 与入口仍宣称起草综述手稿 | 收窄为综合方法 owner，明确写作/计算交接；移除固定论文写作模板，保留方法与证据交付清单 |
| 冻结分析扩展、避免自研 PDF/文献工具 | 本轮未发现可以等价替代后安全删除的具体实现及其调用链证据 | 不新增分析工具、PDF 工具、依赖或 runtime；不根据潜在重复删除有效实现 |

## 技能处置清单

以下清单按用户交付物分组，仅是文档说明，不是新增运行时 registry 或阶段链。

| 模块 | 处置 | 职责 |
|---|---|---|
| `research-agent` | 保留并调整路由 | 当前任务选择、已有产物复用与完成责任 |
| `nature-writing` | 保留 | 论文/学位论文正文及实质论证重构 |
| `researchwrite` | 保留、收窄入口 | proposal、开题和研究计划；复用项目约定 |
| `nature-polishing` | 保留、收窄入口 | 已有论证内的语言编辑、翻译与压缩 |
| `paper_format` | 保留、承接排版入口 | 学术材料的版式与格式检查；复用已有 LaTeX 技术参考 |
| `nature-figure` | 保留、去除强制分析交接 | 科研图件设计、后端渲染、导出与视觉审查 |
| `data_analyze` | 保留、澄清图件执行边界 | 数据转换、分析计算及该分析任务内的图表 |
| `res_analyze` | 保留 | 完成结果的解释、支持范围与未解决检查 |
| `evidence_audit` | 保留 | 证据、产物、代码和复现审计；既有最终 closeout 保留 |
| `nature-reviewer` | 保留 | 模拟审稿输出；不冒充真实审稿或已有审计的独立确认 |
| `nature-statistics` | 保留 | 统计报告的透明度与文本审查；计算按缺口交给分析 owner |
| `nature-data` | 保留 | 可用性声明、仓库/许可边界与数据引用 |
| `nature-response` | 保留 | 已有审稿意见的作者回复，与模拟审稿区分 |
| `lit_synthesis` | 保留、降为方法支持 | 系统综述协议、筛选/编码与跨论文综合资产 |
| `literature_kb` | 保留 | 已注册本地 corpus 的构建与查询；不与公共搜索合并 |
| `nature-academic-search` | 保留 | 多源检索、引文影响与参考文献管理 |
| `nature-citation` | 保留专项入口 | 仅针对明确 Nature/CNS 来源限制的引用支持 |
| `nature-ref-verifier` | 保留专项入口 | 文献元数据逐字段核验，与支持某个科学 claim 区分 |
| `nature-downloader` | 保留 | 合法全文与补充材料获取，不承担论文解读 |
| `nature-literature-pipeline` | 保留专项入口 | 用户明确要求的持续监测；不参与一次性检索默认链 |
| `nature-reader` | 保留 | 保持图表、公式与来源定位的全文双语 reader |
| `nature-paper-card` | 保留 | 单篇论文的证据与实验—主张卡片，非全文翻译 |
| `nature-paper2ppt` | 保留 | 从论文/笔记建立汇报故事与 PPT |
| `nature-image2ppt` | 保留 | 从图像重建对象级可编辑 PPT，与新写幻灯片区分 |
| `res_find` | 保留 | 可检验问题与 closest-prior 筛选 |
| `res_method` | 保留 | 作者已选问题的方法方案 |
| `res_plan` | 保留 | 已选问题/方法的实验与证据计划，非 proposal 文档写作 |
| `research-scholar-distiller` | 保留 | 公开学术材料的判断框架，不代表学者本人 |
| `nature-image2-prompt` | 保留 | 概念图的提示词交付，非定量图件执行 |
| `anti-defensive-writing` | 保留条件入口 | 起草后的特定修辞修复，不成为自动写作阶段 |
| `humanizer`、`humanizer-zh` | 保留条件入口 | 不同语言的显式文风编辑，不重选科学论证 |
| `nature-shared`、`shared-references` | 保留共享依赖 | 按 owner 需求加载参考；不创建独立用户 workflow |
| `ars-academic-writing` | 降为停用参考 | 对照与回退材料，退出默认任务选择 |
| 项目 `scientific-agent-vnext` | 保留显式候选 | 当前独立实验绑定，不进入全局默认写作 |
| 项目六个 `openspec-*` 技能 | 保留既有集成 | 已选工作包的机械操作，不再定义科学任务或额外阶段 |

## 修改与验收边界

修改集中在现有入口、manifest 的触发条件与必要的说明文件。没有新增 Agent、
dispatch 代码、状态库、hash gate、hook、依赖或工具。既有最终证据审查、受保护
产物约束、作者决策与多审稿人隔离要求均保留。没有删除技能目录。

验收包括仓库结构/JSON/Python 验证、现有维护测试、受影响入口 frontmatter 与
manifest 路径核验，以及源码与安装文件一致性检查。执行结果与安装备份在忽略的
`local_state/architecture_review_20261012/`；这份审查不把结构检查或路由说明当作
新会话行为、科研质量提升或维护成本下降的实测证据。
