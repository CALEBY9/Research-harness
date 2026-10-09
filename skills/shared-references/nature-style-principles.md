# Nature/Science Portfolio Writing Principles — Environmental Science (v1.0)

> 本文件取代 `writing-principles.md` 在 Nature/Science 子刊环境科学场景下的位置。原文件针对 ML/CS 会议论文 (ICLR/NeurIPS/ICML),与 Nature 子刊的 letter/article 体裁差异显著。
>
> 配合 `paper_nature_template/SKILL.md` v3.0 (编辑判断框架) 与 `paper_polish/examples/english.md` v3.0 (真实学术段落 before/after) 使用。

---

## 1. Nature 风格的核心 — 不是"清晰",是"密度"

ML 会议论文教练 (Karpathy / Neel Nanda) 反复强调"clarity"——**短句、单一 claim、front-load contribution**。这在 8-10 页的 ICLR 论文里是对的。

但 Nature Letter **只有 1500 词正文 + 200 词 abstract**,在这个空间里要承载:

- field-level tension
- specific knowledge gap with stake
- novel approach (and why it works)
- headline finding with effect size + CI
- mechanism layer
- generalization boundary
- broader implication / displacement

**这是 7 个功能,200 词 abstract = 平均每句话承载 1.4-1.6 个功能。**

ML 写作训练出的"一句一意"在这里不够用。Nature 风格的写作核心是**句子密度**——每个从句、每个修饰语都在工作。

---

## 2. Layered Density — 单句承载多功能

### 反面例 (ML 风格 / 一句一意)

> *Coastal eutrophication is a major problem. It has been linked to nitrogen loading. Recent studies suggest phosphorus may also matter. We investigate this.*

(28 词,4 句,4 个功能位 — 密度 1.0 functions/sentence)

### 正面例 (Nature 风格 / layered)

> *Coastal eutrophication has long been attributed to nitrogen loading, yet recent meta-analyses suggest phosphorus limitation may be more widespread than current frameworks predict, with consequences for nutrient management policy that have not been quantified at coastal-ocean scale.*

(40 词,1 句,**5 个功能位**:历史共识 + 当前争议 + specific gap + scale + policy stake — 密度 5.0 functions/sentence)

差距是 5x。这就是为什么 Nature 投稿用 ML 写作风格读起来"扁平"。

---

## 3. Abstract Density Anatomy

200 词 Nature Letter abstract,合理的句数是 **5-7 句**,每句承担:

| 句 | 必备功能 | 可叠加功能 |
|---|---|---|
| 1 | 领域 tension / displacement target | 历史共识 + 当前争议 |
| 2 | specific knowledge gap | scale + stake |
| 3 | 本研究的方法 + 为什么这个方法适合 | 数据规模 + 时间窗 |
| 4 | headline finding | effect size + CI + n |
| 5 | mechanism layer | 边界条件 |
| 6 (可选) | broader implication | displacement direction |

每句 30-40 词,层叠功能。**反面**:每句一个功能 + 每句 15 词 → 7 句话才能装完 → 超 abstract 长度。

### Density audit 工具

写完 abstract 后,逐句标注**承担的功能数**。任何一句只承担 1 个功能 → 是否能与相邻句子合并?平均密度 < 1.5 functions/sentence → 改写。

---

## 4. Lead Pattern (Introduction 与 Abstract 的开篇)

ML 论文的开篇是 *problem-then-claim*。Nature 论文的开篇有 4 种典型 lead pattern,选哪种取决于你的 displacement 类型:

### Lead Type A — Paradox-then-resolution
适用:已发表证据相互冲突,本研究提供裁判证据。

> *X has been observed to do A in laboratory studies⁵⁻⁷ but B in field observations⁸⁻¹⁰. Whether this discrepancy reflects [scale / methodology / system identity] has remained unresolved …*

### Lead Type B — Consensus-then-displacement
适用:领域有强共识,本研究推翻或精化。

> *It is widely accepted that X drives Y¹⁻³. Here we show that this view is incomplete in [specific regime] where Z dominates …*

### Lead Type C — Convergence-then-tension
适用:多条独立证据指向同一现象,但 mechanism 不清。

> *Independent lines of evidence — including A⁵, B⁶, and C⁷ — point to phenomenon X. The mechanism, however, remains contested between hypotheses Y and Z …*

### Lead Type D — Scale-mismatch
适用:已知 process 在新尺度上需要重新评估。

> *The local-scale dynamics of X are well understood⁵⁻⁸, but the [aggregated / regional / global] response to scaled-up deployment of X has not been quantified …*

**Polish 阶段不能凭空生成 lead pattern**——必须在 paper_outline 阶段决定本研究的 displacement 类型。

---

## 5. Methods at the End — Nature 结构特殊性

Nature/Science portfolio 多数刊物 Methods 在主文末尾或作为 Methods Online。这与 ML 会议 (Method 在 Section 3,page 2-3) 完全相反。

写作含义:

- **Main text 不能假设读者已读 Methods**——需要 self-explanatory
- **Display item caption 必须自包含**——读者跳读图表时无 Methods 上下文
- **Abstract 不能展示 method 细节**——只展示 method 类型 (e.g., "satellite remote sensing combined with hydrodynamic modelling")

---

## 6. Display Item Choreography

Nature 风格的 figure 不是按类型 (map / bar / heatmap) 分,是按**论证功能**分。

- Fig 1: conceptual schematic + claim preview (in-data illustration of the central effect)
- Fig 2: dominant pattern (main effect)
- Fig 3: mechanism evidence (why Fig 2 is real causation, not coincidence)
- Fig 4: generalization boundary or counterfactual
- Extended Data Figs: robustness / sensitivity / reviewer pre-emption

详见 `paper_nature_template/SKILL.md` v3.0 §5。

---

## 7. Citation Style

Nature 子刊 default 是 **numeric superscript citation** (`[5]` 或 `⁵`)——不是 `(Author, Year)`。这影响写作:

- 句子节奏更紧凑 (citation 不打断 narrative)
- Related work 更难做 author-name-driven 综述 — 强制按方法/问题族组织
- 综述段落自然变成"two complementary approaches⁵⁻¹⁰ have dominated …"形式

---

## 8. 句长分布 (实证范围)

基于近 5 年 *Nature Climate Change* / *Nature Sustainability* / *Nature Communications* 环境科学 OA 论文样本:

| 章节 | 平均句长 (词) | 最长 (词) |
|---|---|---|
| Title | 12-16 | 22 |
| Abstract | 28-34 | 48 |
| Introduction | 24-30 | 42 |
| Results | 22-28 | 38 |
| Discussion | 26-32 | 45 |
| Methods | 18-24 | 32 |

**Polish 工具不应把超过这些范围的句子机械拆短**——多数情况下复合句承载了必要的条件、对照或定语限制。

---

## 9. Hedge 频率 (实证范围)

Nature 子刊环境科学论文,合法 hedge ("may", "suggest", "consistent with", "likely") 频率:

- Abstract: 1-3 次
- Introduction: 2-5 次
- Results: 3-8 次 (限制因果声明)
- Discussion: 5-12 次 (extrapolation 必须 hedge)

ML 写作教练 (Lipton 等) 反对 hedge,但 Nature 子刊环境科学的审稿人**期待 hedge**——因为单一研究证据不构成因果断言。Polish 把 Discussion 的 hedge 全删 → 审稿人立刻在 minor revision 里要求加回。

---

## 10. Pre-Submission Checklist (Nature 子刊环境科学专用)

### Narrative
- [ ] Central tension 用 1 句话写出来 (用 paper_nature_template Q1)
- [ ] Displacement 对象明确 (用 Q2)
- [ ] Why now 有具体时间锚点 (用 Q3)
- [ ] Falsifiability test 写得出来 (用 Q5)

### Density
- [ ] Abstract 平均句子功能 ≥ 1.5
- [ ] Lead pattern 选定 (A/B/C/D)
- [ ] Abstract 第一句不能套到任何环境科学论文上

### Structure
- [ ] Letter:1500 词正文 + 4 display items + Methods Online
- [ ] Article:3000-5000 词 + 4-6 figures + Extended Data 2-10 个
- [ ] Methods 自包含 (display item caption 不依赖 main text)

### Evidence
- [ ] 所有数字带 CI / SE / IQR / n
- [ ] Sensitivity tests 在 Extended Data
- [ ] Cross-domain transfer 有 legality 论证 (若用 ML/AI 方法)
- [ ] Generalization 边界明确

### Display Items
- [ ] Fig 1 是 conceptual + claim preview,不是研究区地图
- [ ] 每图 caption 自包含
- [ ] 至少一图是 mechanism evidence (不只是 main effect)
- [ ] 至少一图是 generalization 或 counterfactual

### Reference
- [ ] Citation style 与目标刊一致 (numeric superscript for most Nature pf.)
- [ ] Related work 按方法/问题族,不是 paper-by-paper
- [ ] Closest competing work (近 2-3 年) 显式定位

### Cover Letter (见 cover_letter/SKILL.md)
- [ ] 250-400 词
- [ ] 回答 scope fit / why now / general interest 三问
- [ ] 不重复 abstract — 是 editorial pitch 不是 research summary

---

## 11. 与原 ML 写作原则的差异速查

| 维度 | ML 会议风格 (`writing-principles.md`) | Nature 环境科学 (本文件) |
|---|---|---|
| 总长 | 8-10 页 two-column | 1500 (Letter) / 3000-5000 (Article) 词 |
| 句长 | 短 (15-20 词) | 中长 (24-32 词,abstract 可至 45) |
| 句密度 | 一句一 claim | 一句多功能 (1.5-2.0 functions/sentence) |
| Method 位置 | Section 3 (page 2-3) | 末尾或 Methods Online |
| Contribution bullets | 2-4 条 | 无 |
| Related Work section | 独立 section,1 页 | 无 — 综述融入 Introduction 后半段 |
| Hedge | 反对 | 期待 (尤其 Discussion) |
| Citation style | (Author, Year) — natbib | Numeric superscript |
| 开篇 | problem-then-claim | A/B/C/D 4 种 lead pattern |
| Display item 角色 | 主要作 evidence | conceptual + evidence + mechanism + generalization 多角色 |

---

## 12. 来源

- Joshua Schimel, *Writing Science* (Oxford UP, 2012) — 学术写作圣经,密度与叙事并重
- George Gopen & Judith Swan, *The Science of Scientific Writing* (American Scientist, 1990) — 经典短文,subject-verb-object 节奏
- Nature Briefing for Editors (内部指引,2023 年版本)
- 实证语料:近 5 年 *Nature Climate Change*, *Nature Sustainability*, *Nature Communications*, *Nature Energy*, *One Earth*, *Joule* 环境科学 OA 论文 (建议团队建立本地语料库作为风格 ground truth)
