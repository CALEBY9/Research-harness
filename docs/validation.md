# 验证记录

## 2026-11-13：可复用分发

本地环境：Windows 11，Python 3.13.9。以下记录分发与维护检查，不构成科研效果或宿主兼容性保证。

| 检查 | 实际结果 | 边界 |
|---|---|---|
| `python -X utf8 -B scripts/harness.py validate` | PASS；29 个启用技能，133 个 Python 文件可解析，59 条回归定义 | 含两个未执行的私有输入案例；模型执行数为 0 |
| `python -X utf8 -B -m unittest discover -s tests` | 73 项全部通过，无跳过 | 包含原有工具测试和新增分发测试；不代表全部技能的真实任务行为通过 |
| 隔离安装 CLI | 通过：源码副本、空白用户目录、Python `-I -S` 禁用第三方包；dry-run、install、check 与重复安装拒绝 | 不依赖作者配置、私有库或外部账户；没有启动 Codex 或调用模型 |
| 安装集合 | 启用入口与清单一致；共享资源及许可齐全；旧 ARS 写作入口与 figures4papers 缺席 | 是文件集合与内容检查，不是外部服务验收 |
| 受影响技能元信息 | Research Agent、文献库、图件三个技能检查通过 | 不证明输出质量提升 |
| 文档与配置 | 45 个当前文档本地链接可解析；工作流和问题表单 YAML 可解析；Git whitespace 检查通过 | 远端链接及 Actions 实际运行另行核验 |
| 许可未明确的参考集合 | 70 个文件停止 Git 跟踪，本机文件保留 | 当前分发排除；历史提交未改写 |

CI 配置包含 Windows、Linux、macOS 与 Python 3.10/3.13。此处记录的是本地验证，远端各平台是否通过应查看对应提交的 Actions 结果。私有知识库和独立软件集成仍须使用者自行配置并实测。

## 首次迁移历史

后续候选行为比较使用 [behavioral_evaluation.md](behavioral_evaluation.md)。
本页保留首次迁移的历史结果；结构 PASS 不等于行为改善。

日期：2026-09-08。

| 检查 | 实际结果 | 能证明什么 |
|---|---|---|
| 指定安装目录导入 | 34 技能、708 文件 | 已保留明确列入范围的现用源码与支持文件 |
| 导入与现用文件比对 | 708 文件与初始来源 SHA-256 一致；无差异 | 本次没有修改现用技能或丢失所导入文件的内容 |
| `python scripts/harness.py validate` | PASS；147 个 Python 文件通过语法解析；JSON/基本技能元信息/回归 owner 检查通过 | 源码结构与语法；不保证所有辅助工具运行成功 |
| `python -m unittest discover -s tests -v` | 10/10 PASS | 暂存不覆盖、错误输入可见失败、秘密模式输出不回显值、未执行案例标记 |
| `python scripts/harness.py doctor` | 49 处绝对路径，涉及 16 文件 | 本机依赖或示例的位置；尚未完成跨机器重绑定 |
| 已知凭据模式检查 | 未命中高风险 token/private-key/URL 凭据模式 | 有限模式扫描，不等于完整隐私或 secret 审计 |
| 额外长字符串赋值检查 | 1 项，位于凭据配置单元测试，已核对为测试伪值 | 已检查该项，未把伪值判作真实凭据 |
| 模型行为与科研效果 | 本次执行 0 条 | 没有在本次重跑 31 条模型回归，也没有新质量提升结论 |

Nature 原有示例 `figure_VIGIL/plot_ablation.py` 含 3 条 `\l` 无效转义
SyntaxWarning，无 Python 语法失败。本次保持上游/现用示例内容，不顺手修订。

两条需要私有输入的回归：`RA-QUALITY-01-WIND-LANGUAGE-ONLY` 和
`RA-QUALITY-02-METACOUPLING-RESTRUCTURE`。快照保留定义和历史指针；输入论文片段
没有导入。即便测试定义存在，也不得报告其执行通过。

本地详细路径检查和导入比对记录在被 Git 忽略的 `local_state/`。
正式稿、项目资料、会话、凭据和已有项目状态均未作为迁移输入。

外部项目仅做文档/局部源码设计核对，见 `reference_projects.md`。
未执行其安装脚本、启动服务、安装依赖或开展端到端研究实验。
