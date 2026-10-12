# Work package

## Source and scope

- Objective and selected owner: 恢复作者选择的 Nature 写作底座；Research Agent 继续负责轻量路由。
- Author-confirmed source: 本轮作者明确要求从其 GitHub 历史恢复；来源为本仓库 `b5b8e082522409aea0cb8db80a7afc2e5c086867` 的 Nature 目录与 researchwrite。当前 HEAD 为 `3da946e`，现有未提交增强先保留。
- Authorized actions: 备份、恢复方法文件、切换默认路由、同步本机安装及必要的技能启用设置、纠正冲突说明、运行离线与发现检查。
- Existing checks: `scripts/harness.py validate`、既有单元测试、skill-creator 验证工具、Codex app-server 技能发现。
- Invariants: 不改项目手稿、科研数据、知识库、模型路由、凭据；不恢复自动演化；不启动模型质量评测、不推送 GitHub。
- Unresolved author decisions: 无；此次明确授权取代此前 Nature 退役决定。
- Recovery: 本地忽略目录中的恢复前源码、已安装入口和安全技能配置备份；精确回滚说明随安装报告交付。

## 1. Tasks

- [x] 1.1 核对 GitHub 历史与本机差异；备份现有源码、ARS 和已安装入口，恢复 18 个来源目录。
- [x] 1.2 切换 Research Agent 路由、配套说明和本机入口；Nature 方法与来源逐字节一致，ARS 文件保留且默认入口禁用。
- [x] 1.3 验证共享依赖、结构与既有测试；通过独立 Codex app-server 读取实际发现结果。
- [x] 1.4 完成安装、回滚与验证记录，明确发现验证与写作质量验证的边界。

## Acceptance evidence

| Requirement/source | Implementation/artifact | Check and expected observation | Actual result/evidence locator | Status |
|---|---|---|---|---|
| 作者指定 GitHub 原版本 | Nature 17 目录 + researchwrite | 来自 b5b8e08，原方法不重写 | Git、源码、安装 666 文件一致；265 条引用存在 | PASS |
| 默认写作底座切换 | research-agent 与 Codex 技能配置 | Nature 可发现启用，ARS 禁用 | 独立 Codex 0.162.1 skills/list 在两处工作目录确认，无发现错误 | PASS |
| 保留现有研究能力与改动 | 本地备份、KB/分析与 ARS | 非目标源码及安装不变 | 64 个非目标源文件及完整已安装 ARS 一致；非技能配置一致；五处配套交接只改 owner 指向 | PASS |
| 验证边界 | 安装报告 | 离线检查不宣称顶刊质量或行为增益 | 零模型调用 | RECORDED |

## Review and handoff

- 安装证据和机器路径保存在忽略的本地记录中，不发布私有科研材料。
- 已更新既有 `.agent/NEXT.md` 与 `.agent/STATE.md`。安装报告在忽略的 `local_state/nature_restore_20261012/completion_report.md`。
- 已执行 harness validate、25 项仓库测试、10 项 Nature Figure 测试、5 项 Nature Shared 测试；五个主要入口在 UTF-8 模式通过 quick_validate。
- Windows 默认 GBK 读取使首轮四个 quick_validate 报解码错误；改用 Python `-X utf8` 后通过，未改方法文件。原始图件示例仍有三处转义警告，不影响结构解析；未以机械验证代替真实写作效果评估。
