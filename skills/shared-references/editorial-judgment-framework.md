# Editorial Judgment Framework — Top-Tier Journals (v1.0)

> 顶刊编辑在 desk 阶段(15-30 分钟)读稿的判断框架。本文件是 `paper_nature_template/SKILL.md` v3.0 §1 的独立扩展版,供 `paper_review` 与 `cover_letter` 调用。

---

## 编辑视角的 5 问

| # | 问题 | 答不上的后果 |
|---|---|---|
| Q1 | What is the **central tension**? | desk reject |
| Q2 | What does this paper **displace**? | desk reject 或下转子刊 |
| Q3 | **Why now?** | "interesting but not timely" |
| Q4 | Who is the **smallest community** that would care? | "scope too narrow" |
| Q5 | What is the **falsifiability test**? | "claim too soft or too broad" |

---

## Q1. Central Tension — 不是 gap

| 形态 | 判断 |
|---|---|
| "Top-down vs bottom-up estimates differ by factor of 2" | ✅ 真 tension |
| "Whether X causes Y is contested between hypotheses A and B" | ✅ 真 tension |
| "X has been understudied" | ❌ gap, 不是 tension |
| "X is important for Y" | ❌ importance claim, 不是 tension |
| "Effects of X on Y under conditions Z" | ❌ research question, 不是 tension |

**Polish 不能制造 tension** — 必须在 paper_outline 阶段就有。如果手稿真的没有 tension, 不要投顶刊,投专业期刊不丢人。

---

## Q2. Displacement — 不是 contribution

Displacement 强度梯度:

| 强度 | 描述 | 投稿档次 |
|---|---|---|
| **改写范式** | 推翻一个领域共识 | Nature/Science 主刊 |
| **重大精化** | factor-of-2 修正 IPCC/IPBES 关键参数 | Nature 子刊 |
| **机制 displacement** | 已知现象的 mechanism 被替换 | Nature 子刊 / NC |
| **边界 displacement** | 已知效应在新边界条件下不成立 | NC / 子刊 |
| **首次量化** | 第一份 X 的估计,但**无对照** | 专业期刊 |
| **方法改进** | 新方法但结论与旧方法一致 | 专业期刊 |
| **新应用** | 已知方法到新区域/对象 | 专业期刊 |

**误判后果**: 把"首次量化"当"重大精化"投 Nature → desk reject 后浪费 4-8 周。

---

## Q3. Why Now — 具体时间锚点

| 触发 | 强度 |
|---|---|
| 新观测平台首次可用 (Sentinel-6, NISAR, GFED-5) | 强 |
| IPCC AR cycle / COP / 重大政策事件 | 强 |
| 方法学突破让以前算不了的问题变得可算 | 强 |
| 领域刚出现公开争议,本研究提供裁判证据 | 强 |
| "近年来 X 受到越来越多关注" | **无** (扁平开头) |
| "随着 X 技术发展" | **无** |

---

## Q4. Smallest Community — 但不能太窄

强:**至少 2 个独立社群同时关心**
- 海上风电工程师 + 海洋生态学家 + 海洋空间规划政策制定者
- 古气候学家 + 大气化学家 + 行星科学家

弱:**单一社群 = scope mismatch**
- "海上风电研究者" → 投专业期刊
- "搞 CA-ABM 的人" → 投方法期刊

---

## Q5. Falsifiability — 一行可证伪

形式:
> "若数据呈 [specific pattern X],本研究 claim 不成立。"

例:
- "若 14 年中超过 4 年的尾迹效应方向与平均效应相反 → 我们的 fleet-scale 推断不成立"
- "若模型在保留出的 5 个站点上预测误差超过 30% → 不能扩展到全球"

**Polish 不能凭空生成**——必须在 paper_outline 阶段写好,作为 PAPER_PLAN.md 的固定字段。

---

## Editorial 视角的"不投"信号

收到投稿后,以下任何一条出现 = desk reject 高概率:

- ❌ Abstract 第一句可套到任何环境科学论文
- ❌ Introduction 是 paper-by-paper literature dump
- ❌ Claim 类型(见 `claim-typology-and-rivals.md`)与证据等级不匹配
- ❌ 没有 rival hypothesis 处理
- ❌ Display item 1 是研究区地图或流程图(不是 claim preview)
- ❌ Methods 含 "we first … then we …" 流水线叙述
- ❌ Discussion 收尾是 "Our findings have important implications for …"
- ❌ Cover letter 是 abstract 的复述

---

## Editorial 视角的"送审"信号

以下条件满足越多,送审概率越高:

- ✅ Abstract 第一句是 specific tension/displacement
- ✅ Introduction 综述按方法/问题族,不是按论文
- ✅ Claim 与证据级别匹配 + rival 已处理
- ✅ Display item 1 是 conceptual + claim preview
- ✅ Methods 子标题 functional
- ✅ Discussion 有 specific displacement claim
- ✅ Cover letter 回答 scope fit + why now + general interest 三问

---

## 编辑接到稿件后的内部流程(实证)

1. **Editor screening** (5-15 min): 读 cover letter + abstract + Fig 1 caption + skim conclusions
   - 判断:scope fit 与 general interest
   - 输出: desk reject / send to subordinate editor / send for review
2. **Subordinate editor full read** (30-60 min): 完整读 main text
   - 判断:technical soundness 初判 + 哪 3-5 个 reviewer
3. **Peer review** (4-10 周): 通常 3 位审稿人
4. **Editor decision** (审稿后): 综合 reviewer 意见 + editorial 判断
   - 选项: accept / minor / major / reject / transfer

**关键认识**: cover letter + abstract + Fig 1 决定能否进入步骤 2。这 3 件事必须是手稿最强的部分。

---

## 把这套框架接入工作流

- `paper_outline` Step 0 — 用 Q1-Q5 自检;答不上 → 不要进入 Step 1
- `paper_review` simulated peer review — 包含 Editor view, 用本框架
- `cover_letter` — 用 Q1/Q2/Q3 写 editorial pitch
- `paper_nature_template` — 是这套框架的入口
