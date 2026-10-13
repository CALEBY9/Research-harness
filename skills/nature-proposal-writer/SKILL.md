---
name: nature-proposal-writer
description: |
  Compose, revise, or audit evidence-grounded research proposals, opening reports, and research plans in compose/revise/hybrid modes with structured QA. Use for 科研项目书、开题报告、研究计划, or proposal writing; not for manuscript drafting.
license: MIT
metadata:
  hermes:
    tags: [research, writing, proposal, revision, qa, multi-agent]
    related_skills: [brainstorming, professor, avoid-ai-writing, docx]
---

# nature-proposal-writer — proposal-first 科研写作 pipeline

受 autonovel（状态机+打分）、professor（动态专家）、brainstorming（入口追问）、anti-AI-writing（语言清理）启发的科研写作状态机。**不是通用"帮我写论文"prompt。**

`nature-proposal-writer` 是本机技能与源码目录名，上游对应 `nature-proposal-writer`。
需要初始化模板、
按条件加载参考资料或执行导出脚本时，先读取 `manifest.yaml`，只加载与当前条件匹配的路径。

## 产物边界

负责 proposal、开题报告和研究计划文档，包括其中的背景与文献综述章节。
论文、学位论文章节及独立综述论文正文交给 `nature-writing`，模拟论文审稿交给
`nature-reviewer`，语言-only 编辑交给 `nature-polishing`；普通邮件不触发本技能。
输入出现 Introduction、Discussion 或“综述”时，先按目标文档区分，不按章节词抢占任务。

## 核心原则

1. **证据先于文字** — 起草前必须建立或读取 `research_canon` 和 `evidence_table`
2. **论证先于章节** — 写正文前必须完成 `argument_map`
3. **契约先于段落** — 每节需要 purpose / allowed claims / forbidden claims / inputs / validation
4. **范围先于完备** — 如果是分阶段写作，先锁定阶段边界
5. **按问题检查** — 默认由当前代理检查；只有明确获准 delegation 时使用可用专家适配器
6. **内容先于语言** — 诊断科学逻辑后再做 anti-slop / 语言打磨
7. **不自动升级事实** — 永远不把 "may indicate" 改成 "proves"，除非有证据支撑
8. **删除胜于解释** — 当某主张不可行，直接删除。正文干净，解释留给答辩
9. **停止与继续** — 统一按 `references/stopping-rules.md` 判断
10. **作者控制科学主线** — 研究问题、dominant claim、rivals、falsifier、负结果解释和
    story rebase 由作者决定；agent 只负责整理、比较和压力测试选项
11. **证据状态与主张许可分离** — claim-bearing 工作读取
    `../nature-shared/core/evidence-authority.md`；缺失/未核验用
    `HOLD_FOR_EVIDENCE`，已有反证用 `REJECT_OR_REMOVE`

## 模式分派

| 输入 | 模式 |
|---|---|
| 题目、方向、模糊想法 | `compose` — 加载 `references/compose-mode.md` |
| 已有段落/章节/完整 proposal | `revise` — 加载 `references/revise-mode.md` |
| 已有草稿 + 扩写/补写/重构 | `hybrid` — 加载 `references/hybrid-mode.md` |

模糊时推断默认模式。只在选择会改变工作流时才问用户。

## 项目结构

先复用项目已有的任务范围、事实表、证据表、提纲和章节要求。它们可以直接满足
下述 foundation 字段，不必复制为一套新文件。已有 OpenSpec 工作包记录实施状态，
`.agent/` 记录恢复指针；不另建 `state.json` 镜像。
独立新 proposal 没有目录约定时，在项目指定的交付目录按需使用
`references/project-structure.md` 和 manifest 模板。只建立本次需要的文件，
不为段落修订预建完整目录树。已有 nature-proposal-writer 项目可继续使用原文件结构。

## Reference 文件索引

完整 reference 按任务需要加载，不要一次性注入全部文件：

| Reference | 加载时机 |
|---|---|
| `references/compose-mode.md` | 模式 = compose（9 步流程） |
| `references/revise-mode.md` | 模式 = revise（9 步流程） |
| `references/hybrid-mode.md` | 模式 = hybrid |
| `references/evaluation-rubric.md` | 使用 8 维 × 4 锚点评分体系时 |
| `references/research-anti-slop.md` | 清理中文 proposal 的模板化和空泛表达时 |
| `references/chinese-review-writing-style.md` | proposal 背景中的文献综合需要此参考时；不是综述论文入口 |
| `references/stopping-rules.md` | 判断继续迭代、拆分范围或停止时 |
| `references/professor-dispatch.md` | 按失败模式分派动态专家时 |
| `references/foundation-files.md` | 建立或修复 foundation 五文件时 |
| `references/project-structure.md` | 无既有约定的新 proposal，或维护已存在的 nature-proposal-writer 文件时 |
| `references/export-archive.md` | 导出和归档 `.md` / `.docx` 时 |
| `references/partial-proposal-scope.md` | 分阶段写作并防止范围蔓延时 |
| `references/ref-renumbering-cascade.md` | 处理参考文献增删和编号级联时 |
| `references/review-paper-framework.md` | proposal 拟开展综述研究，需说明其问题与证据设计时 |
| `references/review-critique-methodology.md` | proposal 文献背景需要证据比较方法时 |
| `references/validation-checklist.md` | 自动检查主张、引用、编号和可复现性时 |
| `references/gpt-handoff-revision-brief.md` | 生成跨 agent 修订交接简报时 |
| `references/within-approved-proposal.md` | 在已批准的 proposal 框架内扩写时 |
| `references/worked-example-quaternary-proposal.md` | 需要查看完整 foundation 文件填写示例时 |
| `references/降承诺提案模式.md` | 证据不足，需要降低承诺强度时 |

## 运行交付

交付用户要求的正文、文件或审查报告。修改理由、未解决证据缺口和验证情况另列；
内部评分与状态不进入正文，也不作为每次调用的必需输出。

## QA Mode — 四层质量保障 Pipeline

`professor`、其他专家 skill 或子代理都是可选适配器，不是默认依赖。只有这些能力已
安装、用户明确授权 delegation、且当前 instruction 允许时才调用；否则由当前代理按
同一 rubric 本地完成检查，并明确无法保证的独立性。不得为凑齐专家池自动安装服务、
创建 agent 或扩大任务范围。

当用户说"审查这段/跑 QA/检查方案/过 pipeline"时，进入 QA 模式。

### 情境挡位

| 挡位 | 适用场景 | 阈值 |
|------|---------|------|
| `proposal` | 研究方案/开题 | 7.0 |
| `quick` | 当前 proposal 的局部检查 | 无 |

### Pipeline 顺序（先内容后语言）

```
Gate 2: 内容检查（当前代理，按具体缺口检查可行性与创新依据）
  │
  ▼
Gate 1: 语言检查（复用本技能的 research-anti-slop 参考）
  │
  ▼
Gate 3: auto-validation（格式/完整性层）
  └── 每个 claim 有 citation？方法可复现？编号连续？
  │
  ▼
Gate 4: 评分阈值（分维度打分）
  ├── 总分≥阈值 → 通过 ✅
  └── 总分<阈值 → 按低分维度定向回退（不超过 3 轮）
```

**Gate 2 在 Gate 1 之前** — 避免改了句子后被专家打回重写。

### 使用方法

```
用户: "用 nature-proposal-writer 审查这段开题报告的方法方案"
  → 在请求范围内检查内容、语言、完整性与评分
  → 返回审查报告 + 定向修改建议

用户: "快速检查开题报告这段是否符合已确认的研究范围"
  → 只检查该段与既有范围，不启动完整方案审查
```

## 配置你的研究域

从当前材料与已确认的项目背景获取领域约束；不因首次使用自动创建领域专家或知识文件。
