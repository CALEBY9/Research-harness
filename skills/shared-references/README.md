# `shared-references/` — Skill 之间的共享参考资料

## 这是什么

**不是 skill。** 没有 SKILL.md 入口,**不能被独立调用**。

是被多个 skill 共同引用的参考资料库——类似软件工程中的 shared library / common module。Skill 之间避免重复内容,把通用的方法学/标准/框架抽到这里。

## 当前内容

| 文件 | 作用 | 被哪些 skill 引用 |
|---|---|---|
| `editorial-judgment-framework.md` | 顶刊编辑读稿 5 问 (Q1-Q5) + desk reject 信号 | `paper_outline` Step 0 / `paper_review` Tier 0 / `paper_nature_template` / `cover_letter` / `lit_synthesis` |
| `claim-typology-and-rivals.md` | Claim 类型学 (A-F) + Rival hypothesis matrix + Falsifiability + Scoop matrix | `paper_outline` Step 2.1-2.4 / `paper_review` Tier 1 |
| `nature-style-principles.md` | Nature 子刊环境科学写作原则 (layered density, lead patterns, 句长/hedge 分布) | `paper_write` Step 1, 5.1 / `lit_synthesis` Step 5 |
| `nature-portfolio-checklists.md` | Nature/Science/PNAS/Cell Press 系列各刊 specs + 通用投稿前 checklist | `paper_nature_template` / `cover_letter` / `lit_synthesis` |
| `citation-discipline.md` | 引用规范与诚信 | `paper_write` / `paper_review` / `lit_synthesis` |
| `kb-to-manuscript-evidence-bridge.md` | 本地文献候选的原文核验、跨文献综合和写作引用追溯；按任务复用证据记录 | `literature_kb` / `research-agent` / `lit_synthesis` |
| `clean-final-language-gate.md` + `scripts/clean_final_scanner.py` | 成品稿/图表/投稿包过程语言泄漏门控、禁词族与可执行扫描器 | `codex-research-workflow` / `paper_review` / `paper_polish` / `paper_format` / `paper_revision` / `submit_guide` |
| `equation-semantic-integrity-gate.md` + `scripts/equation_semantic_gate.py` | 逐公式符号—定义—编号—模型—版本一致性门控，以及 production proof 更正分类 | Research workflow entry / `paper_revision` / `paper_review` / `paper_polish` / `evidence_audit` |
| `production-proof-integrity-gate.md` | production proof 的差异清点、公式、表格指标、引用闭合、跨文件版本、声明与逐页 QA 总门控 | Research workflow entry / `paper_revision`; delegates to `paper_review` / `evidence_audit` / `paper_format` |
| `manuscript-revision-granularity-gate.md` | proof、小修、返修和 marked DOCX 的最小修订单元、editable/protected span、Track Changes 粒度、EndNote/reference-manager source-of-truth 与 round-trip 失败码 | Research workflow entry / `paper_revision` / `paper_polish` / `paper_format`; handed to DOCX execution when marked output is required |

## 为什么这样组织

如果不抽到 shared-references,以下问题会出现:

- 编辑 5 问会同时出现在 `paper_outline` / `paper_review` / `cover_letter` / `paper_nature_template` 里 → 修订时要改 4 处
- Nature 子刊各刊 specs 会同时出现在 `cover_letter` / `paper_nature_template` / `lit_synthesis` 里 → 内容漂移
- 单一 skill 文件膨胀到难以维护

抽到 shared-references 后:

- 每个文件有**唯一 source of truth**
- Skill 引用即可: `参见 ../shared-references/editorial-judgment-framework.md`
- 修订时改一处,所有引用 skill 自动获益

## 与 skill 的差异(明确边界)

| 维度 | skill (`paper_*/`) | shared-references/ |
|---|---|---|
| 调用方式 | 用户主动触发(`paper_outline`) | 不能独立调用 |
| 含 SKILL.md | 是 | 否 |
| 含 workflow / steps | 是 | 否 |
| 含 reference 内容 | 主体是 workflow | 主体是 reference |
| 类比 | 函数 / 命令 | 配置 / 数据 / 标准 |

## v4.1 清理记录

下列文件在 v4.1 删除(被新文件取代,且无 skill 引用残留):

- ~~`writing-principles.md`~~ — 旧 ML 会议风格,被 `nature-style-principles.md` 取代
- ~~`venue-checklists.md`~~ — 旧 ML 会议清单,被 `nature-portfolio-checklists.md` 取代

下列内容在 v4.1 从 `nature-portfolio-checklists.md` 剥离(项目特定,移到 `_project_notes/`):

- 海上风电 + 海水养殖耦合系统投稿决策树 → `_project_notes/offshore_wind_aquaculture/submission_strategy.md`
