# 源码维护、暂存与安装

## 现有机器

2026-09-08 初次导入采用 34 个实际已安装技能作为来源。Nature 源仓库的 HEAD 为
`54144dcf6376b034716bd70edd40ad2cf407943e`，工作树存在本地增强，因此不能
用该 commit 或最新上游版本替代本次实际安装快照。

2026-10-12 按作者明确请求，从本仓库已发布的
`b5b8e082522409aea0cb8db80a7afc2e5c086867` 恢复 17 个 Nature 目录及
`nature-proposal-writer`（当时安装名 `researchwrite`）。它们仍是当时的本地增强版本，不是最新上游发行版。
实质写作由 `nature-writing` 承担，ARS 文件与增强保留为非默认备选；
`skill_evolve_workflow` 继续退役。[ARS 采用记录](ars_writing_adoption.md)
保留历史身份，不作为当前默认路由。

本机 Nature / nature-proposal-writer 位于用户级 `.agents/skills`，Research Agent
及既有分析、知识库工具位于历史 `.codex/skills`。2026-10-13 按作者要求
删除 25 个重复的旧技能安装目录，包括旧 `paper_*` 写作链及 ARS 入口；
ARS 仅保留发现目录之外的备份和版本化参考源码。图件语料库、知识库及
研究设计等独立能力保留。三层下载不在当时删除的 25 个目录中，随后发现的
后端缺失已从可追溯修订记录恢复。实现作为工具代码维护于
[PDF 下载后端](../scripts/pdf_download/three_layer_pdf_downloader.py)，本机安装在
用户工具目录，通过无 `SKILL.md` 的目录联接满足既有桥的路径；未恢复技能入口。
8 项源码测试与 6 项实际 CLI 本地夹具检查通过，机构登录和外部出版商下载未复测。
源码、安装与发现须分别核验；CLI 帮助可加载不代表后端可执行。

同日按作者要求新增核心科学判断技能，随后按工作单元边界优化为
`nature-scientific-insight`（科研洞察与判断），承接核心科学判断及旧
`res_novelty` 的有价值细则；不恢复旧技能链。vNext 的 ARS 对照绑定指向
版本化参考源码，保留其明确选择的上游写作配置。知识库绑定路径已重新核验，
路径存在不表示查询、健康或科学证据已通过验证。

原 `research-judgment` 已更名，源码、安装目录、frontmatter、界面元数据和当前
owner 引用保持一致；不保留第二个公开别名。更名不等于已验证调用准确率提高。

2026-10-13 按作者要求统一科研流程技能名称为 `nature-<capability>`；完整
更名表与安装根目录见[技能命名](skill_naming.md)。`research-agent` 入口保留。
目录、调用元数据、owner 引用及上游映射同步修正，原有项目资源与调用策略保留。

`docs/import_manifest.json` 记录逐文件初次导入校验值，供迁移证据使用。
它不是今后禁止修改技能的冻结门槛。`scripts/import_local_skills.py` 是
一次性导入工具；目标已经存在时拒绝覆盖。正常维护使用文件 diff。

原安装保持在本机既有技能目录。本仓库不复制全局 AGENTS、运行时配置、
插件缓存、论文库、会话、项目状态或归档候选。

## Nature 上游审阅式更新

`docs/nature_upstream.json` 记录来源、已选择的目录映射和本轮两个局部导入。
它不表示整个 Nature 套件已经更新。历史原仓库 HEAD `54144dc...` 在公开
仓库读取返回 404，原因未确认；不能用本仓库的 `b5b8e08` 本地增强快照
冒充上游原版，也不能在找不到原版时自动三方合并。

先只读检查：

```powershell
python -X utf8 -B scripts/nature_upstream.py check
```

按输出的完整提交 SHA，为明确选定的技能生成一个新审阅目录，例如：

```powershell
python -X utf8 -B scripts/nature_upstream.py prepare --commit e605b35611ab2849af46d0cf7831aefdcf85be07 --target .\local_state\nature_upstream_review_20261012 --skill nature-writing
```

工具会连带暂存 `nature-shared`，保留本地与上游原文件，记录新增、删除和
内容差异。目录已经存在时拒绝覆盖，不向源码或实际安装路径写入。已确认
可靠的上游原版可用 `--base <完整SHA>` 加入比较；无原版时所有差异标明需
人工比较。`review.diff` 是本地与上游的显示差异，不是自动应用的合并补丁。
新目录保留原始 Git 来源供复查，不进入技能发现。失败不会生成成功报告；
如失败目录需要保留，换一个新目录重试并保留失败原因。

审阅时保留本地中文 `zh`、学位论文 `thesis`、作者科学决定与交付规则，
核对条件加载和共享依赖，区分脚本修复与写作行为变化。先把接受的变更
合并到本仓库源码，按受影响的结构、引用或代码做必要机械检查，复用范围仍
适用的验证；行为表现结合后续真实项目观察，不要求每次更新另跑模型基准。
再按已授权文件范围同步安装。工具没有自动合并、安装或启用
入口；普通 skills 更新器也没有登记本次恢复的 Nature 目录。

2026-10-12 本轮只导入固定 `e605b35` 的 Discussion 参考和 retry-zero 修复，
并补充本地科学定位、证据迁移和图件交接方法。没有用上游 router/manifest
替换本地路由。Discovery 或结构测试不能证明新方法实际加载或稿件增益。

### 已授权的上游监测

作者于 2026-10-12 授权同步版本并等待后续上游更新。维护命令新增一次检查：

```powershell
python -X utf8 -B scripts/nature_upstream.py watch
```

首次以 `watch_initial_commit` 为已观察版本；新提交出现时，为已采用的
Nature 目录和共享依赖生成隔离审阅包。检查结果和待处理目录指针保存在
`local_state/nature_upstream_watch/check_result.json`。同一提交不会重复暂存，
待审更新不会因随后一次无变更检查而消失；失败保留原观察状态并返回非零。
观察到某个提交不表示其内容已经安装。

本机 Windows Task Scheduler 注册被未提权进程的权限限制拒绝；未留下任务。
改用当前用户 Startup 快捷方式启动隐藏的 Python `monitor` 进程：每周一
09:00（本机时区）检查；本周已经检查过时，重新登录不重复检查，错过检查
时在登录或休眠恢复后补查。退出登录或关机时不运行。启动项、解释器及
执行记录保留本地，
不随 GitHub 克隆自动创建。后台命令为：

```powershell
pythonw -X utf8 -B scripts/nature_upstream.py monitor
```

`monitor_status.json` 记录后台 PID 和下次检查时间；`monitor.log` 保存成功及
失败日志。关闭监测时，停止该记录中经命令行核对属于本工具的 PID，并移除
用户 Startup 中的 `ResearchHarness Nature Upstream Check.lnk` 即可。

监测不调用付费模型、不向上游上传文件、不覆盖本地增强。上游 router 与
manifest 当前缺少本地中文及学位论文路径，旧原版基线也未证实；因此更新
必须审阅实际差异。后续维护任务沿用作者的同步授权，保留本地能力、检查
相关依赖并验证接受的修改，再同步源码与受影响安装；涉及科研定义或正式
主线改变仍由作者决定。记录已吸收及未采用的上游内容后，维护者清空
`watch_state.json` 的 `pending_review`，保留 `observed_commit`；此动作只表示
审阅结束，不表示整套安装。监测状态不是聊天通知，也不是自动安装结果。

## 通用隔离暂存

下面命令需要指定一个尚不存在的目录，可选择单个技能，也可省略 `--skill`
暂存全部技能。暂存仅方便审阅，不会替换任何当前安装。

```powershell
python scripts/harness.py stage --target .\local_state\trial_skills --skill research-agent
```

重跑时换一个新的目标目录。工具不提供覆盖现有目录的选项。

## 换机器或安装候选

1. 克隆指定分支/commit，运行 `validate` 和单元测试。
2. 运行 `doctor`。它列出含本机绝对路径的文件和行号，不会自动改写路径。
3. 按需要绑定 Nature 写作方法及共享参考、KB、文档工具等现用依赖。路径提示也可能来自示例，
   须检查调用语义；简单字符串替换不能证明可迁移。
4. 查看现有安装与候选 diff，保留现有有效本地修改，选择本次安装的技能集合。
5. 使用该运行时支持的安装方式，并验证实际技能发现与一条目标任务。核验用户目录
   与项目目录的完整发现列表：所选维护技能应启用，退役入口应缺席，额外入口须逐项
   解释用途；只核对源码或“改过的技能仍存在”不能发现残留。技能发现、脚本可加载
   和真实科研判断质量分别报告，不用结构检查替代科研验证。

Codex 当前官方文档支持仓库/用户级 `.agents/skills`，并说明同名技能不会
自动合并。本快照源自混合的 `.agents/skills` 与历史 `.codex/skills` 安装。
不要把所有快照目录再放进已含同名技能的发现目录。
[官方来源](https://learn.chatgpt.com/docs/build-skills)

`humanizer:humanizer` 是本机现有 English Humanizer 的名称约定；部分旧 adapter
含下划线。首版保留名称以避免破坏现有调用，不据此声称所有 Agent 都兼容。

## 公开发布

当前 GitHub 仓库为公开源码仓库。提交前需逐项核查本机路径、项目名称、私有
fixture 指针和第三方素材的再分发范围；密钥模式扫描不等于完整脱敏。
`.agent/`、`local_state/`、凭据及私有研究输入保持在本地忽略范围。
保留第三方 LICENSE 和 NOTICE，不能给整包第三方内容重新指定统一许可。
面向其他用户的一键安装/plugin 发布是后续独立工作。
