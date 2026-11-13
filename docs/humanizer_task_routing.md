# 学术润色与去AI味的任务路由

2026-10-23 按作者同意的功能精简，学术去AI味并入 `nature-polishing` 的
academic-humanization 模式；不再安装 `academic-humanizer` 独立入口。
一般中文文章继续使用 `humanizer-zh`，独立英文通用 Humanizer 继续退役。

| 任务 | 当前处理方式 |
|---|---|
| 中文通用文章、评论、技术或商务文档去AI味 | `humanizer-zh` |
| 中英文论文、学位论文、审稿回应、开题或基金计划去AI味 | `nature-polishing` 的 academic-humanization 模式 |
| 学术语言润色或翻译 | `nature-polishing` 的相应语言路径 |
| 学术润色与去AI味同时请求 | 一次整合编辑，最后统一对照原文与作者证据 |
| SCI 已润色，只要求去AI味 | 直接进入 academic-humanization 模式，不重跑普通润色 |

只加载当前模式或具体残留问题需要的语言指导。通顺文字可以不改，不自动追加
第二个 Humanizer、回译、检测服务、外部上传或额外模型轮次。

## 来源与保留内容

学术参考来自 [academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer)
提交 `94b88b23703bed7df507acae7d6d5876209a0cdf`（0.3.3）。本地适配后的指导、
示例与 MIT 许可保留在
`skills/nature-polishing/references/academic-humanization/`；原目录和展示素材
保留在发现目录之外的本轮恢复副本。没有恢复独立英文通用入口。

## 编辑边界

保留事实、术语、数字、单位、引用及其主张、直接引语、否定、条件、因果强度、
研究状态和段落功能。上游 before/after 仅为教学示例，不得为稿件添加证据。
改变科学主张或论证结构交给 `nature-writing` 及适用的作者决定。
有原稿时最终对照最初原稿；只有润色稿时保留其含义并说明核对范围。
作者样例可选，不从样例借用事实。AI降重只表示保留原意的编辑，不保证相似度
或 AI 检测结果。后续质量观察复用正常稿件任务及作者反馈，不另起评测项目。
