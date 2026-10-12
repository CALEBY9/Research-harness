# 科学发现建议审查与本地优化

审查日期：2026-10-12。依据当前技能源码、安装副本、工具可用性、公开项目文档
和实际 HTTP 返回。外部建议是待检验的输入，不作为本地能力或科学主张的证据。

## 结论与真实缺口

“本地缺少科学发现层”与现有文件不符。`res_find` 已有最近先行研究筛查、
残余贡献、可证伪假设、机制与数据可行性；`res_method` 已有竞争方法与区分性
观测；`res_plan` 已有对照、负结果和验证路线。这证明已有职责与指令，尚不证明
其科学判断表现达到任何外部项目或领域专家的水平。

实际可修复的问题是指令漂移与执行指导不足：发现阶段参考文件仍调用退役的
`lit_search`、`res_novelty`，要求五份日志和固定候选数量，并安排无条件确认；
文献检索没有明确围绕未解决命题选择下一轮检索及停止；OpenAlex 脚本缺少可选
认证支持，说明仍把 `mailto` 当作配额机制，并把单一索引覆盖误写成多源替代。

## 建议处置

| 建议或判断 | 本地证据与问题 | 本次处置 |
|---|---|---|
| 科学发现是完全缺失的最大层 | `res_find` 已覆盖新颖性、假设和可证伪性；缺少实测质量证据 | 修复和补充现有 owner，不另建层 |
| PaperQA2 风格多轮检索 | 检索 owner 已有多源、去重、原文证据边界；反馈式检索和停止指导不足 | 在现有搜索流程增加按证据缺口继续检索、竞争证据与停止指导 |
| 引文遍历 | 已有相关文献与引文审查能力；并非所有任务需要网络构建 | 允许针对关键论文按需向前/向后追踪，复用现有工具和参考文献 |
| 自动矛盾检测 | 结果差异可能来自尺度、定义、样本和数据来源 | 检查原文与可比性后报告分歧；不把检索差异直接命名为科学矛盾 |
| evidence_quality_score | 检索排序分与引文数不能校准证据质量 | 保留证据类型、原文定位和限制，不新增无依据分数 |
| STORM 研究地图 | 可借鉴多视角组织；目录空白不证明知识断裂 | `res_find` 支持有来源的对象—过程—尺度—指标关系图，标明待验证连接 |
| Owl / Novelty Critic | 与现有 closest-prior-work 筛查重叠 | 在 `res_find` 完成单个想法审查，不创建独立 Agent |
| 异常发现 | 检索和解释异常不同；数据错误也可产生异常 | 先查测量、定义、抽样和尺度；已有输出解释由 `res_analyze` 承担 |
| Hypothesis Generator / Theory Connector | 假设与机制链已有；竞争解释可以更清晰 | 明确观察与假说、竞争解释、区分性比较及否定/反向结果 |
| 新 Experiment Designer / Reviewer Simulator | `res_method`、`res_plan`、`nature-reviewer` 已承担 | 复用原 owner，不自动串联 |
| 五层、多个 Agent、新 prompts/schemas | 会复制路由、证据记录和任务状态，未证明新的执行缺口 | 不新增 runtime、技能目录或第二套任务记录 |
| Semantic Scholar / OpenAlex / Crossref / PubMed 全部必须 | 领域和可用性不同；当前会话未提供这些专用 MCP 搜索工具 | 按任务与实际访问选择；验证现有 OpenAlex HTTP 回退，不宣称所有服务在线 |
| OpenAlex Concepts / 新知识图谱 | Concepts 已被 Topics 替代；分类标签不等于机制证据 | 修正使用说明，不部署图谱库 |
| 示例论文数量及风渔协同假说 | 原建议无查询、分页、去重、原文或因果识别证据 | 仅作为示例，不导入为项目事实、已证实 gap 或科学结论 |
| 接近 AI 副 PI / 科研操作系统 | 是定位愿景，无法从技能数量或静态检查推出 | 保持研究者决定科学方向，报告未验证的能力边界 |

## 外部来源核验

FutureHouse 将完整 AI Scientist 描述为问题、假设、实验、分析和知识产出的闭环，
并表示其定义下尚无系统完整满足要求。这支持保留能力边界，不能推导本机最缺哪层。
见 [FutureHouse AI Scientist](https://www.futurehouse.org/ai-scientist)。

PaperQA2 的迭代查询、证据汇集和引用回答值得借鉴；README 同时说明内部研究工具、
引文遍历及全文访问条件与公开代码存在差异，不能把内部结果直接转移给本地实现。
见 [PaperQA README](https://github.com/Future-House/paper-qa)。
本次采用检索反馈思路，没有安装 PaperQA、增加向量库或调用其模型流程。

原建议引用的检索工程文章发表于 2024-09-19，其实验针对 LitQA2 等文献任务；
这不是本机环境科学发现能力的评估。
见 [FutureHouse 工程文章](https://www.futurehouse.org/research/engineering-blog-journey-to-superhuman-performance-on-scientific-tasks)。
Crow、Falcon、Owl、Phoenix 的角色说明来自 2025-05-01 平台发布文章，不能单凭该
历史页面称作 2026 年最新完整产品清单。
见 [FutureHouse 平台发布](https://www.futurehouse.org/news/launching-futurehouse-platform-ai-agents)。

STORM 主要研究带引用的百科长文，其前置研究组织视角和提纲；Co-STORM 支持协作
探索及思维图。可以借鉴组织问题的方式，但这不证明某个地图空白是研究空白。
见 [STORM 官方仓库](https://github.com/stanford-oval/storm)。

OpenAlex 当前认证说明支持匿名基础查询和 bearer header；弃用说明已替换 Concepts，
并取消 `mailto` 的旧配额用途。
见 [认证说明](https://help.openalex.org/api/authentication/)及
[弃用说明](https://help.openalex.org/api/deprecations/)。
两页对无 key 使用的表述存在不一致；认证页的 `per_page=100` 上限也与本次 HTTP
实际接受 200 的结果不同。本次保留可工作的分页逻辑，仅增加可选认证，避免根据
冲突文档强制注册、缩减召回或写死配额。服务可达性不是全文支持或检索完整性的证明。

## 修改与验收边界

修改四个已有 owner 的九个文件：`research-agent` 路由、`res_find` 主入口及两份
参考文件、`res_method` 的一处旧引用，以及 `nature-academic-search` 的入口、
搜索流程、操作说明和现有 HTTP 脚本。两份发现参考文件整体精简，保留科学证据
要求，取消重复模板、退役 owner 和无条件阶段链。没有新增技能或生产依赖。

OpenAlex 认证只读取运行时 `OPENALEX_API_KEY` 并放入 HTTP header，覆盖作品检索、
作者候选和 ORCID 查询；不写凭据、不加入 URL、不静默降级或隐藏请求失败。
`tests/test_academic_search.py` 检查匿名行为、三类认证请求、401/429 可见失败
和非 JSON 响应。真实已认证请求因本机未配置该 key 而未执行。

维护检查使用 `python -m unittest discover -s tests -v`、
`python scripts/harness.py validate`、`git diff --check`、技能入口验证和
源码/安装比较；HTTP smoke 仅检查公开索引通信与结果格式。安装备份、实际命令
结果及发现检查保存在忽略的 `local_state/discovery_review_20261012/`。

本轮 51 项维护/接口/集成测试通过，harness 检查通过；34 个 owner 的 721 个
源码文件与安装文件一致。两个工作目录的原生技能发现均读取到四个受影响 owner，
无发现错误，ARS 仍停用。匿名 HTTP 检索返回两条公开索引记录；这里只验收通信
及格式，不将元数据当作原文支持、完整综述或新颖性结论。

这些检查验证维护正确性、安装一致性与接口行为。没有进行配对科研任务或人类
科学判断评估，不据此宣称假设更创新、研究更可靠或达到外部项目的性能。
