# AI4Science 能力评审与首轮路由进化（2026-09-20）

作者指令：锐评本地 Research agent 的 AI4Science 能力，自行检测、自行调用多
agent 评估、自行进化。本文是评审记录与已应用改动的验收证据；不是行为质量
提升证明（本轮全部为静态证据，`behavioral_evaluations_executed: 0`）。

## 方法

5 个独立只读评审 agent（文献证据链 / 研究设计创新链 / 代码实验复现 / 统计
推断 / 治理与自进化），各自通读路由器与相关 owner SKILL.md，对 20+ 条
AI4Science 典型任务做静态路由探针，输出带 file:line 证据的评分与缺口。
主维护线程同时跑确定性检测（`harness.py validate`、unittest 25/25、
回归包清点、源-安装 diff）。评审 agent 不改文件、不联网。

## 评分与锐评

| 维度 | 分 | 一句话锐评 |
|---|---|---|
| 文献获取与证据链 | 3.5/5 | 单体 owner 专业水准高，但跨 owner 契约在仓库层断链、引用验证双头管辖、prior-art 检索无路由归属 |
| 研究设计与创新链 | 3.5/5 | 证伪优先的反 novelty 筛选是一流约束，但 novelty/hypothesis 在路由器层"没有门牌"，样本量/对照/功效在设计链无词 |
| 代码实验与复现 | 2.5/5 | 事后法医一流，事前实验台是空的：全库 34 skill 无一承担复现/训练/第三方环境执行；`evidence_audit` 前身叫 code_repro，执行职责在演进中丢失 |
| 统计推断与稳健性 | 3.5/5 | 稿件报告侧接近最佳实践（效应量优先、伪复制 P0、因果语言双闸），执行侧统计三向歧义、seed 方差无阶段契约、UNKNOWN/分母无 owner |
| 治理与自进化 | 4/5 | 防自我晋级的结构设计在个人 harness 里属第一梯队，但整套机制零真实执行、19/35 skill 零回归覆盖，是把从未开过刃的刀 |

总评：这是一台**"读科学、写科学、审科学"一流的机器，"动手做科学"的
执行层刻意缺席**。对以文献综述+测量管线（人写代码、agent 审计）为主的
当前主项目是正确取舍；对 AI4Science 全谱（复现、训练、benchmark 执行）
则是明确短板。治理层（作者控制、证据权威、防作弊晋级）是最强资产。

## 静态探针证实的关键缺口（改动依据）

1. novelty/prior-art 请求（"评估这个方法的新颖性，最接近 3 篇 prior
   work"）在路由器无行，能力深埋在 `res_find` G1.5 gate 内不可达。
2. 可证伪假设→检验路线图请求无行；`res_plan` 行只写 "a mature method"。
3. 执行侧统计（检验/效应量/seed 方差）三向歧义 data_analyze /
   nature-statistics / res_analyze，路由表无触发词。
4. 6 条 AI4Science 执行类探针 3 条无 owner（复现论文代码、复现图、
   搭第三方环境）；`research-code-spec.md:84-86` 禁止未批准装包，但
   没有任何文本告诉入口"如实报告无 owner + 单独请求授权"。
5. `evidence_audit:215-217`、`paper_format:129,223,342`、
   `lit_synthesis:239`、`literature_kb:169` 引用的 `../shared-references/`
   契约目录（含 2 个 gate 脚本）不在维护仓库，跨 owner 证据桥接在
   Git 层不可审计；live `.codex` 安装中实际存在 17 个文件。
6. `CONTRIBUTING.md:32` 写"现有 31 条"，实际（改动前）32 条，计数漂移。

## 已应用改动（APPLY_APPROVED_PATCH，最小集）

失败归因：1–4 = `SKILL_DEFECT`（静态探针可复现的路由文本缺失）；
5 = 导入遗漏（修复导入，不改任何行为）；6 = 文档计数漂移。

| # | 文件 | 改动 |
|---|---|---|
| 1 | `skills/research-agent/SKILL.md` | Local gaps 表 4 处：res_find 行 +novelty/closest-prior；res_plan 行 +falsifiable hypothesis；data_analyze 行 +检验/效应量/CI/seed 方差；新增诚实 no-owner 行（复现/第三方执行→受控实施任务+装包单独授权+evidence_audit manifest） |
| 2 | `skills/research-agent/references/copilot-regression.json` | +4 用例：RA-ROUTE-07-NOVELTY-PRIOR-ART、RA-ROUTE-08-HYPOTHESIS-ROADMAP、RA-ROUTE-09-ABLATION-STATS、RA-AI4S-01-REPRO-NO-OWNER（期望=如实报告无 owner+请求授权），32→36 条 |
| 3 | `skills/shared-references/`（新） | 从 live `.codex` 安装整体导入 17 文件（15 契约 md + 2 脚本，剔除 `__pycache__`），`docs/import_manifest.json` +17 条 hash 条目；四 owner 的 `../shared-references/` 引用全部可解析 |
| 4 | `CONTRIBUTING.md` | 31→36 条计数修正 |
| 5 | `docs/roadmap.md` | 候选表 +1 行"论文代码复现/第三方实验执行 owner"（记录缺口与触发条件，不新增 skill） |

语义选择门：记录 `NOT_APPLICABLE`——本轮全部为措辞级路由澄清、注册导入
与文档修正，无新 skill、无新依赖、无行为语义扩张；若后续把复现做成真正
owner，须走完整冻结三臂门。

## 验证（实际执行）

- `python -c json.load`：回归包 36 条，4 条新用例 ID 在位。
- `python -m unittest discover -s tests`：25/25 OK。
- `python scripts/harness.py validate`：PASS，skills 34、
  python_parsed 152（150→152 = 新导入的 2 个 gate 脚本）、
  regression_definitions 36、errors 空。
- 路由污染 grep：既有行（nature-academic-search:18、literature_kb:24、
  nature-statistics:26）逐字未动；"novelty" 在路由器全文仅出现 1 次
  （res_find 行内）。
- shared-references 解析检查：5 个被引用路径（bridge、equation gate、
  clean-final gate、2 脚本）全部存在。
- 语义 dry-run（grep/readback 层）：RA-ROUTE-07/08/09 与新增行逐一
  对应；RA-AI4S-01 的期望行为与 no-owner 行及 `references/research-code-spec.md`
  授权条款一致。未执行任何模型调用；路由改善是文本层判断，不是行为证据。

## Cross-CLI Sync Ledger

| Item | Codex path | Claude path | Sync status | Reason | Validation |
|---|---|---|---|---|---|
| research-agent SKILL.md | `.codex/skills/research-agent/SKILL.md` | 无对应安装（Claude 侧入口为 claude-code-research-workflow） | SYNCED (Codex-only owner) | research-agent 是 Codex 侧路由器 | 拷贝后 diff 为空 |
| copilot-regression.json | `.codex/skills/research-agent/references/` | 同上 | SYNCED (Codex-only owner) | 维护回归包随源码 | 拷贝后 diff 为空 |
| shared-references | `.codex/skills/shared-references/` | `.agents/skills/` 侧另有 nature-shared | SYNCED（导入方向 live→repo） | 修复仓库断链，live 未动 | 17 文件 hash 记入 manifest |

同步前源-安装 diff 为空（唯一增量即本轮改动）；live 覆盖前的旧字节可由
本仓库 Git 历史与 `.codex` 侧无版本现状下的本记录回溯（本轮覆盖仅 2 个
文件，均为措辞级路由澄清）。

## 暂缓未应用（记录为候选，需作者或后续迭代）

1. `data_analyze` Step 5 增加 seed 方差/UNKNOWN≠NO/分母显式报告规则——
   owner 级行为改动，需真实失败案例或行为评估后再入（Agent D 建议）。
2. 设计链样本量/统计功效/对照组规则——涉及科学定义，属作者决定。
3. res_find/res_method 的环境科学域硬编码（`res_method:80-85` 数据源
   清单）——范围决策，非维护侧可改。
4. 引用验证双头管辖（nature-ref-verifier vs nature-academic-search
   wf2 两套分类不对齐）——需先裁决 owner 边界。
5. 治理层首条真实行为闭环（RA-STRAT-01 冻结材料已在，缺审定 adapter）
   ——roadmap 既有优先项，本轮不重复。
6. 19/35 skill 零回归覆盖——按真实失败逐步补，不一次性铺开。

## 边界确认

本轮未：改任何 owner 行为语义、新增 skill/依赖/hook/CI、执行付费模型
调用、宣称行为或科研质量提升、触碰 protected 产物。改动范围 =
作者"自行进化"指令 + 上述 6 条静态证据。
