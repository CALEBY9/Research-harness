# ARS 方法接入合同

本合同区分方法借用、完整上游工作流和运行时安装。使用某份角色文件不会自动创建代理；读取 ARS 参考不代表完整执行了 ARS 的全部流程。

## 可选写作配置

`bundled-candidate` 使用本包原创方法，不声称加载 ARS。`ars-local` 读取项目绑定中明确指定的 `local_baseline_entry` 及本次任务需要的参考文件，按 `local_baseline_kind` 区分实际安装与版本化参考，不猜测已移出的安装路径。`ars-upstream-slice` 读取固定版本 ARS-Codex 的写作内容，跳过其全流程编排、自动委派、阶段目录规定、自动更新及全局配置。

用户的当前科研边界与本任务权限优先。上游的证据核查、作者主张控制、文献来源及学术诚信约束应当保留。任何必要适配写入一次简短差异记录，不能一边移除上游约束，一边报告为“完整上游原样运行”。

## 上游文件依赖

先定位真实 checkout 或固定 commit 的只读文本快照。不要把维护仓库中的 `skills/` 自动等同于正在使用的安装目录。记录仓库 commit SHA；文件 blob SHA 只能标识一个文件。固定 commit 的 raw URL、逐文件哈希和来源清单可以标识文本快照；应明确它不是完整 checkout。若来源无法绑定 commit，则明确版本未完全固定。本机接入差异见 `local-integration.md`。

核查时用完整上游入口了解结构。实际写作按需读取以下路径，这些路径来自本次核查的 ARS-Codex 布局，未来版本若变更须重新定位：

```text
skills/academic-research-suite/ars/academic-paper/agents/argument_builder_agent.md
skills/academic-research-suite/ars/academic-paper/agents/draft_writer_agent.md
skills/academic-research-suite/ars/academic-paper/references/intro_title_rhetoric_guide.md
skills/academic-research-suite/ars/academic-paper/references/academic_writing_style.md
skills/academic-research-suite/ars/academic-paper/references/writing_quality_check.md
```

`argument_builder_agent.md` 与 `draft_writer_agent.md` 是本次直接读取过的文件。后三项在 draft writer 中被引用，部署时仍须确认它们存在、内容与版本一致。与所请求章节相关的其他方法依赖也要补全，例如 Discussion、综述、修订或引文表达。完整保留相关文件的论证步骤、实例与诊断标准，不再次压缩成一页泛泛原则。无需整包加载无关审稿、实验、筛选或多代理资源。

来源中的引用格式默认值、教学领域示例、繁体双语设置、固定代理数量与目录结构不构成用户学科要求。必须明确适配为实际任务：简体中文或指定英文、文章类型、目标期刊及当前作者已确认的范围。

## 上下文最小完整性

写作上下文应同时含有作者要回答的问题、当前结果与限制、可回查文献证据以及相关写作方法。避免只给模型论文卡片摘要，随后要求它综合自己没有读过的细节。也避免把三个月维护历史和所有技能描述塞进同一个写作回合。

一次只处理当前章节或作者授权的整稿任务。章节分开写时共享一份简短的全稿主线及术语表，整稿合并后另做一致性核对，不让每章自行定义新的中心贡献。

## 失效时

缺失某个 bound 文件，报告缺失的具体方法依赖。不要静默改用 Nature 或 bundled-candidate。可继续无须该依赖的证据整理，或在作者明确接受后按有名称的降级路径试写。对照试验中任何降级都使该轮不再属于原计划处理条件，必须标注。
