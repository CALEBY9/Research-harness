# Humanizer 上游同步

2026-10-14 最终用途调整：作者主要处理 SCI 润色后去AI味，独立英文通用
humanizer 已从源码技能集合和本机发现目录移出，保留本地恢复副本与复用内容
的 MIT 声明。当前使用 academic-humanizer，中文通用适配 humanizer-zh 保留。
已润色稿直接去AI味，不重复润色、不再追加英文通用技能；当前规则见
[任务路由](humanizer_task_routing.md)。下文三技能记录是当日早先方案。

2026-10-14 后续作者澄清：要求三项 Humanizer 全部安装并自动按任务路由。
已新增 `AIScientists-Dev/academic-humanizer`，绑定提交
`94b88b23703bed7df507acae7d6d5876209a0cdf`（0.3.3），保留 LICENSE、README、
examples 与 assets，添加 Codex 界面元数据。版本/兼容信息放 metadata，去除
工具名称白名单；以本地编辑约束保护数据、引用和主张，示例不作为用户证据。
Research Agent 采用中文通用 / 英文通用 / 学术三路；学术“润色+AI降重”按需
组合 nature-polishing 与 academic-humanizer，并对照最初原稿验收。
这替代下文早先的“不安装 academic-humanizer”范围决定，Lynote 未安装。
完整安装及验证记录见 [三技能路由](humanizer_task_routing.md)。

2026-10-14 本地学术适配：两项现有技能增加论文/计划的证据、术语、段落功能和作者声音约束；英文修复新增反应、见词即改和禁止所有破折号的规则冲突。Research Agent 明确按语言选择一个适配器，普通学术润色仍由 nature-polishing 负责。不安装 academic-humanizer 或 Lynote，不采用回译与检测器闭环，不更新上游提交。来源诊断及采用边界见 [本次审查](humanizer_academic_review.md)。

2026-10-12 按作者授权同步两项技能，源码与实际安装同时更新。

| 技能 | 来源 | 已采用提交 | 版本 |
|---|---|---|---|
| humanizer-zh | https://github.com/op7418/Humanizer-zh | f4518a8eab97b8bfebc66a89d34320a89bef6930 | 2026-09-23 |
| humanizer | https://github.com/blader/humanizer | 225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8 | 3.1.0 |

采用上游 SKILL、README、CHANGELOG；保留原 MIT LICENSE。中文测试脚本及案例一并同步；英文维护指南、插件清单、既有包校验脚本和 CI 定义同步到同一版本，不安装或启用外部插件。实际安装位置沿用既有目录，不新增同名发现入口，不改 Research Agent 路由和默认写作 owner。

本地适配：中文移除运行时专属 `allowed-tools`，保留 MIT 元数据；两项 SKILL 记录 `upstream_commit`。学术事实、引用及其对应主张、因果方向、限定条件、段落功能和作者判断必须保留。模板、作者样例和必要的技术标记优先于通用风格偏好。英文粘贴模式默认只返回最终正文，不默认附草稿、诊断或评分。保留原 `agents/openai.yaml`，没有新增插件、模型调用或工具依赖。

本机旧安装内的 `.git` 元数据未重置；其 HEAD 不代表当前适配内容的上游版本。当前上游绑定以 `SKILL.md` 的 `metadata.upstream_commit` 和本记录为准。没有运行 `git reset`、全局安装器或 `npx skills update`，避免覆盖既有适配。

后续更新仍按固定上游提交审阅：核对当前源码与实际安装，备份受影响文件，将上游变化与本地适配比较，修改源码，执行 owner 检查，再同步批准的安装文件。`scripts/import_local_skills.py` 仍是一次性导入工具，不用于更新。Nature 监测器只负责其已映射套件，不监测这两个 Humanizer；本轮不扩大后台日程范围。

验证包括 Harness 结构校验、两项 Codex skill 校验、原始英文上游包校验、源/安装逐文件一致性及中文文件保护检查。18个中文短例和2个英文短例由同一会话实际改写并人工核对；不是独立、跨模型或盲测，不证明 AI 检测分数或稳定写作增益。新会话的实际发现与加载仍需在下一次调用确认。

任务级备份、原始上游仓库、逐项来源审计与测试记录保留在忽略目录 `local_state/humanizer_sync_20261012/`。没有修改论文文件、运行时配置或公开推送。
