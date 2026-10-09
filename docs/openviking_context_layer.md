# OpenViking 作为只读 Context sidecar 的接入边界与试验协议

评估日期：2026-09-19，对 2026-09-17 初评按上游文档复核并细化。
结论不变：OpenViking 只作为 Research Agent 的 Context 检索 sidecar 候选，
不进入权威链，不替代 literature_kb，不改变 `.agent/` 权威。

## 已核验事实（来源见文末）

- 主体：volcengine/OpenViking，自我描述为 "Self-evolving Context Database
  for AI Agents"；`viking://` 虚拟文件系统统一 Resource/Memory/Skill，
  L0/L1/L2 分层加载。
- 许可：主项目 AGPL-3.0；`crates/ov_cli` 与 examples 为 Apache-2.0。
  因此只以独立 server + MCP/HTTP 接入，禁止把其源码复制或子模块引入本仓库。
- MCP：单端点 `http://<server>:1933/mcp`，15 个工具：
  `find, search, read, list, tree, remember, write, edit, add_resource,
  list_watches, cancel_watch, grep, glob, forget, health`。
  只读子集＝`find/search/read/list/tree/grep/glob`（另 `health`）；
  其余一律按写入口对待。
- Codex 插件：SessionStart 注入 profile，UserPromptSubmit 逐 prompt 检索注入，
  Stop/PreCompact/SessionEnd 提交会话（SessionEnd 需 Codex ≥0.145 且优雅退出），
  PreToolUse(Bash) 识别 `viking://` URI。控制项：
  `OPENVIKING_NO_AUTO_INJECT`（默认 false）、`OPENVIKING_RECALL_QUERY_FILTERS`、
  `OPENVIKING_CAPTURE_FILTERS`（CSV、sed 式替换规则）。
- 关键陷阱：idle-TTL（默认约 30 分钟）清扫会把非优雅退出的会话在下一次
  SessionStart 补提交。"关窗即不采集"不成立；真正的控制是 capture filter
  与"在污染敏感上下文不安装插件"。
- 模型面：embedding 支持 `local`（GGUF）与 `ollama` 等本地路线；L0/L1 语义层
  依赖 VLM（volcengine/openai/openai-codex/kimi/glm/litellm 等），未配置 VLM 时
  L0/L1 退化为内容直生成（语义较弱）。`processing_mode="vectors_only"` 是
  `add_resource` 的参数（只向量化、跳过 VLM 语义理解、不生成
  `.abstract.md`/`.overview.md`），不是全局配置键；官方配置文档无此键。

## 对外部输入的更正与未核验项

- `vectors_only` 的位置写错：是 `add_resource` 参数，不是配置项。
- 以下未能独立核验（本机到 GitHub 的直连持续重置）：版本时间线
  （v0.4.20、2026-09-14、95 commits、约 3.8 万 star、建仓时间）、Qasper
  基准数字（60 query / recall≈0.614 / F1≈0.293）、L1 目录 32-children 采样、
  `memory_diff.json` 细节。决策不依赖这些数字：接口高速演进已按高风险处理，
  任何接入都必须能整体摘除。
- 遗漏点：workspace 记忆按 git origin URL 派生；跨项目/非 git 目录下的
  隔离行为需在 Phase 1 实测后再信任。

## 边界（与 docs/architecture.md、docs/roadmap.md、nature-shared
evidence-authority 一致）

1. 权威不变：项目 `.agent/NEXT.md`、`STATE.md` 与原文件仍是唯一事实源；
   OpenViking 索引只是检索面，不是第二权威，不参与验收或完成判断。
2. 证据链不变：检索命中只提供 candidate evidence；claim 支持必须回到
   DOI/页码/section/table/figure/equation locator（literature_kb 契约保留，
   OpenViking 不承担论文证据检索）。
3. 保护数据禁入：selected 800 身份清单、FROZEN120、盲审包、机器答案、
   专家材料、未发表稿正文不进入索引。项目 `.agent/` 与含生产数字/待作者
   裁决内容的文档，仅在本地 VLM 或无 VLM 配置下、且作者点名该项目时考虑。
4. AGPL 隔离：独立 server、MCP 通信；不复制源码进 harness。
5. 泄露控制：任何云端 VLM/embedding provider 不得接触未发表内容；默认
   `local`/`ollama` embedding，L0/L1 用本地 VLM 或接受无 VLM 降级。

## 分阶段试验协议

- Phase 1（只读 sidecar）：MCP 只暴露白名单工具
  `find/search/read/list/tree/grep/glob`；不装 Codex 插件、不启 hooks、
  不调用 `add_resource` 写会话记忆。索引对象＝本仓库公开文档 + 单一项目
  公开层。验收：能定位"某决定记录在哪个文件"，全程无写调用。
- Phase 2（单项目低风险 context）：导入一个项目的公开文档与 notes，用
  20–30 个真实历史恢复问题回测；对照组＝直接读 `.agent/` 的现有流程。
  指标：定位耗时、找错版本、漏找关键决定；不建通用评分器。
- Phase 3（插件 recall 受控试验）：以 `OPENVIKING_NO_AUTO_INJECT=true`
  起步（保留逐 prompt recall、关闭固定注入）；recall/capture filter 先用
  样例 diff 人工核验语义（替换式规则，不是丢弃式）；怀疑污染即停并卸载
  插件。默认不依赖 SessionEnd/idle 清扫类采集。
- Phase 4（experiences，最后）：仅限"Research Agent 如何工作"的程序性经验
  （工具失败恢复、canonical binding、检索顺序、artifact validation）；
  科学结论、研究假设、方法选择、论文 claim 永不进入自动学习；
  author control contract 优先级最高。

试验产物与日志放 `local_state/`（不进仓库）。任一阶段出现越权写入、
污染召回或绕过证据回源，即回退该阶段并记录失败场景。

来源：repo README、`docs/en/guides/06-mcp-integration.md`、
`docs/en/agent-integrations/04-codex.md`、docs.openviking.ai 配置页
（2026-09-19 抓取）。
