# 安装、配置与更新

本工具集使用 Codex 的本地技能目录。安装器需要 Python 3.10+，没有额外 Python 包依赖；它不安装 Codex、不配置账户、不下载模型、不创建调度任务。

## 首次安装

先克隆仓库并验证源码：

~~~powershell
git clone https://github.com/CALEBY9/Research-harness.git
cd Research-harness
python -X utf8 -B scripts/harness.py validate
python -X utf8 -B scripts/harness.py list
~~~

推荐先查看安装计划，再显式安装到个人技能目录：

~~~powershell
python -X utf8 -B scripts/harness.py install --target ~/.agents/skills --dry-run
python -X utf8 -B scripts/harness.py install --target ~/.agents/skills
python -X utf8 -B scripts/harness.py check --target ~/.agents/skills
~~~

~ 由 Python 展开，因此上述 Python 命令同样适用于 PowerShell、Bash 和 zsh。安装器会创建目标父目录；任何待写入的同名文件或目录已存在时，整次安装在复制前停止。无关技能不会被修改。没有强制覆盖选项。

Codex 支持用户目录 ~/.agents/skills 和项目内 .agents/skills。技能未出现在选择器中时，重启会话，并检查是否存在同名技能。具体发现规则参见 [OpenAI Docs](https://learn.chatgpt.com/docs/build-skills)。

## 项目级或选择安装

例如只在你自己的项目目录中使用：

~~~powershell
python -X utf8 -B scripts/harness.py install --target ../my-research/.agents/skills
python -X utf8 -B scripts/harness.py check --target ../my-research/.agents/skills
~~~

随后从 my-research 项目启动 Codex，不要把私人研究材料放进本维护仓库。不要在个人和项目两处重复安装同名技能。

只安装某个能力时重复使用 --skill：

~~~powershell
python -X utf8 -B scripts/harness.py install --target ../my-research/.agents/skills --skill nature-reader --skill nature-polishing
python -X utf8 -B scripts/harness.py check --target ../my-research/.agents/skills --skill nature-reader --skill nature-polishing
~~~

选择安装会同时带上 nature-shared、shared-references 和许可文件。仅安装 research-agent 路由器不会自动安装其全部专业技能；需要完整研究工作流时使用默认安装。

[skills/catalog.json](../skills/catalog.json) 是启用目录的唯一分发清单。ars-academic-writing 是停用参考，安装器拒绝选择它。figures4papers 的未确认许可素材不分发。安装不包含本仓库 .agents 中的 OpenSpec 集成和实验候选，也不会启用历史写作链。

## 没有作者的知识库也能使用

用户提供的论文、数据、现有稿件及可访问公共文献可以作为研究输入。没有绑定本地库时，使用这些来源完成任务，并说明实际证据覆盖；不得声称已检索作者的库。

nature-literature-kb 是既有库的接入说明，不是随包提供的 RAG 服务。只有你拥有相应后端时，才配置：

PowerShell：

~~~powershell
$env:RESEARCH_AGENT_KB_ROOT = 'D:/my_research_library'
python -X utf8 -B scripts/harness.py doctor
~~~

Bash / zsh：

~~~bash
export RESEARCH_AGENT_KB_ROOT="$HOME/research_library"
python -X utf8 -B scripts/harness.py doctor
~~~

项目自己的配置和用户明确指定路径优先于环境变量；所有路径都要实际核验。doctor 只检查根目录和 papers/scripts/research_library.py 是否存在，不证明索引健康、检索质量或后端接口兼容。没有该后端时保持未配置，使用提供的原文与检索技能。不要把任意目录改名后当作兼容库。

历史作者安装路径与专题后端仅供原环境恢复，见 nature-literature-kb 中的独立说明；它们不是新用户的安装前提。

## 按任务配置工具

| 任务 | 配置方式与边界 |
|---|---|
| 文本规划、论文阅读、写作与润色 | 已能运行 Codex，并提供所需材料即可开始 |
| 外部文献检索与全文 | 选择实际可用的服务；API 配置和机构登录由自己提供 |
| 学术检索 MCP 后端 | 按 skills/nature-academic-search/mcp-server/requirements.txt 配置独立环境；install.sh 为历史 Claude Code 安装器，不用于本次 Codex 安装 |
| PDF 下载 | 技能工具按 skills/nature-downloader/requirements.txt 配置；仓库三层下载后端另用 scripts/pdf_download/requirements.txt；机构权限不由安装器提供 |
| 图片恢复为 PPT | 按 skills/nature-image2ppt/requirements.txt 和技能说明配置；需要模型时沿用自己的服务 |
| DOCX、PDF、PPT 与专业绘图 | 提供可用文档工具与相应依赖；Origin、Office、EditaPlot、Tabbit 需另行安装 |
| 定期文献追踪与通知 | 用户明确选择后，单独配置服务和调度；不会随安装自动运行 |

不为安装技能而一次性安装全部可选依赖。科研任务实际需要某项能力时，先验证该工具可用，再执行。

## 更新已有安装

git pull 只更新仓库，不会改变已安装技能。本工具不自动合并或覆盖用户修改。

1. 获取并审阅目标提交的差异及许可变化。
2. 运行 validate 和与变更相关的测试。
3. 暂存到一个新的非技能发现目录：

~~~powershell
python -X utf8 -B scripts/harness.py stage --target ./local_state/review_candidate
~~~

4. 比较候选与实际安装。保留有效的本地修改，先保存将被替换的原文件，再按已审阅范围手动更新；无差异的资源不必替换。
5. 用相同的 --skill 范围运行 check，刷新 Codex 的技能列表，并实际执行一条目标任务。check 报告你刻意保留的本地差异时，需人工确认其含义，不能把 FAIL 改写成已通过。

stage 默认带上全部启用技能、共享资源和许可。它拒绝已存在目录，也拒绝在 .agents、.codex 或 .claude 内暂存，以免审阅即激活技能。install 是单独的显式命令。

## 诊断

| 现象 | 处理 |
|---|---|
| Existing installation entries | 已有同名技能或共享文件；比较并按更新流程处理，不要删除不明来源的用户文件 |
| Unknown or inactive skill | 用 list 检查当前启用名字；退役入口不安装 |
| check 返回 missing / changed | 有文件缺失或与当前源码不同；检查本地修改或安装中断 |
| inactive_present 非空 | 安装目录还含停用写作入口；确认其用途后自行停用，不自动删除 |
| KB_RESOURCE_MISSING 等 | 只暂停依赖该库的动作；一般阅读、检索和写作可继续使用实际可用来源 |
| 示例中的本机路径不存在 | 示例或历史指针不是你的配置；绑定自己的工具与材料 |

文件检查通过以后仍需核验宿主发现和实际任务行为。语法、文件完整性和科研质量是不同验收项。

## 上游维护

Nature 底座保留本仓库记录的本地增强版本，不自动跟随上游覆盖。scripts/nature_upstream.py check / prepare / watch / monitor 供维护者按需审阅上游；普通安装不会注册启动项、执行监测或改变技能。来源与固定版本见 [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) 和 docs/nature_upstream.json。

## 许可与公开内容

原创贡献采用 Apache-2.0；第三方条款分别适用，尤其 ARS 为 CC BY-NC 4.0。安装器同时复制根 LICENSE、THIRD_PARTY_NOTICES.md、NATURE_LICENSE 和组件内许可。论文库、未公开研究、凭据、会话与机器绑定不分发。当前目录停止跟踪的参考文件仍可能存在于历史提交；本轮未改写 Git 历史。
