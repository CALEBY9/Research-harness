# Claim Typology, Rival Hypotheses, and Scoop Matrix (v1.0)

> Paper outline 阶段最容易出问题的地方:
> ① 把 correlation claim 写成 causation claim → 审稿人立刻挑刺
> ② 没列 rival hypotheses → 审稿人帮你列,然后reject
> ③ 不知道自己相对 closest competing work 在哪几个维度上有差异 → 被 scoop 或被认为 incremental
>
> 本文件提供这三个工具的精化版,补 `paper_outline/SKILL.md` 当前 claim-evidence matrix 太粗的问题。

---

## 1. Claim Typology — 6 类声明 + 触发的审稿质询

每条 claim 必须**先分类**,再决定证据要求。把弱类 claim 当强类写 = 顶刊最常见的 desk reject 原因。

### 类型 A — Descriptive Claim
**形式**: "X 在 Y 处呈现 Z 模式"
**例**: "近 30 年中国近海 chlorophyll 呈现南北分异趋势"
**证据要求**: 数据完备、统计显著
**审稿质询**: 数据代表性?探测限?季节偏差?
**Polish 注意**: 不要写成 "X 由 Y 引起" 的 causal 形式

### 类型 B — Comparative Claim
**形式**: "X 比 Y 更 Z" 或 "A 状态下 X > B 状态下 X"
**例**: "夏季尾迹效应是冬季的 3 倍"
**证据要求**: 双向比较 + 统计检验 + 配对/分层控制
**审稿质询**: 控制变量是否完整?confounder?selection bias?
**Polish 注意**: 比较要给出 effect size 与 CI,不只是 p-value

### 类型 C — Mechanistic Claim
**形式**: "X 通过 mechanism M 影响 Y"
**例**: "尾迹效应通过破坏温跃层将营养盐枯竭表层水带到光合层"
**证据要求**:
- 直接观测 mechanism 步骤 (不只是 inputs 与 outputs)
- 或:多个独立证据收敛指向同一 mechanism
- 或:控制实验排除替代 mechanism
**审稿质询**: 替代 mechanism?观测到的中间步骤?可证伪性?
**Polish 注意**: "is consistent with mechanism M" ≠ "M is the cause" — 措辞精确

### 类型 D — Causal Claim
**形式**: "X 引起 Y 变化"
**例**: "海上风电安装导致区域 chlorophyll 下降 12%"
**证据要求**(从弱到强):
- D1 (弱): 时间序列 + 安装时间点的断点回归
- D2 (中): 处理-对照设计 + 多个处理组
- D3 (强): 准实验 + 多种 identification strategy + falsification tests
- D4 (最强): RCT (环境科学罕见)
**审稿质询**: confounder?reverse causality?selection on observables?
**Polish 注意**: causal claim 在没有 D2 以上证据时**必须** hedge ("consistent with", "may", "suggest")

### 类型 E — Predictive Claim
**形式**: "在 X 条件下 Y 会变化 Z"
**例**: "若 GW 级风电在北海全部部署,夏季表层 chlorophyll 累积下降 ~7%"
**证据要求**:
- 模型 + 输入 driver 的不确定性传播
- Cross-validation 在 hold-out set
- 已知偏差 (model bias) 的显式声明
**审稿质询**: out-of-sample 验证?不确定性传播?边界条件?
**Polish 注意**: 必须说 prediction 的有效域 (in-sample distribution),不能外推到完全不同的 regime

### 类型 F — Counterfactual / Projective Claim
**形式**: "若 X 没发生,Y 会是 Z"
**例**: "若 2010 年后未实施氮排放控制,渤海低氧区面积现已增加 X%"
**证据要求**:
- Counterfactual scenario 构造的合法性 (匹配什么、放任什么)
- Sensitivity 到 counterfactual 假设
- 同行已接受的 counterfactual 方法 (PSM, synthetic control, IV, etc.)
**审稿质询**: counterfactual 假设是否合理?
**Polish 注意**: 必须显式标注"counterfactual based on assumptions A, B, C"

### Anti-pattern — 类型混淆

| 混淆 | 后果 |
|---|---|
| 把 A 写成 D | "我们发现 X 与 Y 相关,因此 X 引起 Y" — 顶刊 desk reject |
| 把 C 写成 D | 没有直接观测 mechanism 步骤,但用了 "X causes Y via M" — major revision 至少 |
| 把 E 写成 F | 用 prediction 模型做 counterfactual 而无 baseline 论证 — major revision |
| 把 B 写成 A | "X 比 Y 高" 但未做统计检验 — minor revision 但显得不专业 |

---

## 2. Rival Hypothesis Matrix

每条 claim **至少列 2-3 个 rival hypothesis**,在 paper_outline 阶段就写好,不要等审稿人提出。

### 模板

```markdown
| Rival Hypothesis | Why plausible | Evidence to rule out / weaken | Residual concern |
|---|---|---|---|
| H1 (本研究的 claim) | (本研究的 mechanism) | (主证据) | (剩余不确定) |
| H2 (替代解释 1) | (它合理的理由) | (本研究排除/弱化它的证据) | (实在排除不了的部分) |
| H3 (替代解释 2) | (...) | (...) | (...) |
```

### 例 (海上风电对 chlorophyll 的影响)

| Rival | Why plausible | Evidence to weaken | Residual concern |
|---|---|---|---|
| H1: 尾迹效应破坏温跃层,枯竭表层营养盐 (本研究) | 物理机制成立;尾迹长度与影响范围匹配 | Fig 2: chlorophyll 下降空间分布与建模尾迹分布相关 (r=0.7);深度剖面显示温跃层加深 | 单一观测不能完全排除合并 driver |
| H2: 安装期施工扰动的临时效应 | 施工期沉积物再悬浮可能持续 1-2 年 | Fig 3: chlorophyll 下降在风场运营 5 年后仍存在,排除施工临时效应 | 施工累积效应不能完全分离 |
| H3: 可能是 ENSO/NAO 等气候模式的混淆 | 北海 chlorophyll 已知受 NAO 影响 | 控制 NAO 后效应仍显著 (Extended Data Fig 2) | NAO 与 wind farm 部署在某些时段共变,残留混淆可能 |
| H4: 风场区域被排除商业捕捞,捕食者结构变化导致 chlorophyll 变化 (top-down) | 北海部分风场区域捕捞被限制 | 仅在禁渔风场 vs 非禁渔风场,效应 size 相近 | 数据有限,需要更多 paired 比较 |

**Polish 阶段不能凭空生成这种表格**——必须在 paper_outline 阶段建好。

---

## 3. Falsifiability Test (单独写一行)

在 PAPER_PLAN.md 中,每条 main claim 旁边写一行 falsifiability test:

> "If the data showed X, then the claim would not hold."

例:
- Claim: 尾迹效应是 fleet-scale chlorophyll 下降的主要 driver
- Falsifiability: 若 chlorophyll 下降与尾迹覆盖范围空间相关 r < 0.3,或下降在风场停运期间无回升,则 claim 不成立

写不出 falsifiability → claim 太软或太大,回到 outline 重写。

---

## 4. Scoop Matrix — 相对 closest competing work 的差异坐标

paper_outline 阶段必须显式做这个矩阵,**不是引言里 vague 的"前人没做过"**。

### 模板

针对最近 2-3 年的 closest competing work (通常 2-5 篇),沿以下维度做对比:

```markdown
|  | Comp 1 (Author Year, Venue) | Comp 2 | Comp 3 | This study |
|---|---|---|---|---|
| **Question** | (他们问的具体问题) | | | (我们问的具体问题) |
| **Scale** | spatial / temporal | | | |
| **Method** | (主方法) | | | |
| **Data** | (数据源 + 时间窗) | | | |
| **Mechanism level** | descriptive / comparative / mechanistic / causal | | | |
| **Boundary condition** | (适用范围) | | | |
| **Conclusion** | (主结论) | | | |
| **Differential** | — | — | — | (本研究在哪个维度上 distinct) |
```

### 关键判断

填完矩阵后,**本研究的 differential 必须存在于 ≥ 2 个维度**,否则属于:

- ≤ 1 维度差异 → incremental 工作,投顶刊会被定为 "not sufficient advance"
- 2-3 维度差异 → 可投 NC / CommsEE / 子刊
- 4+ 维度差异 + 显著 displacement → 可投 Nature/Science 主刊

### 反面例 — vague positioning

> "前人主要研究单一风场。本研究研究 fleet-scale。"

**问题**:只在 scale 维度有差异。Method 是否新?Mechanism level 是否升级?Boundary condition 是否拓展?都没说清。审稿人立刻判断为 incremental scaling。

### 正面例 — precise positioning

| | Smith2023 (NCC) | Liu2024 (NS) | This study |
|---|---|---|---|
| Question | 单一风场 vs 无风场,chl 差异 | 多个风场 cumulative impact (无尾迹模型) | Fleet-scale 尾迹效应 + 与水产养殖空间冲突 |
| Scale | 1 farm × 5 yr | 12 farms × 8 yr (北海) | 38 yr × 247 stations × 全球沿海 |
| Method | RS + 描述性统计 | RS + spatial regression | RS + biogeochemical model + counterfactual |
| Mechanism level | comparative | causal (粗) | causal (D2) + mechanistic (温跃层观测) |
| Boundary condition | 单一近岸海域 | 北海 | 全球沿海 + 季节分层 |
| **Differential** | — | — | **方法 (model + counterfactual)、scale (全球 + 长时序)、mechanism level (mechanistic + causal)、policy stake (与 aquaculture 空间冲突)** |

→ 4 个维度差异 + 引入 policy stake → 可投 Nature Sustainability。

---

## 5. 把这 3 个工具集成进 paper_outline workflow

```
paper_outline 增量步骤(在原 Step 2 "Build Claims-Evidence Matrix" 之后加):

Step 2.1: Claim Typology — 每条 claim 标 A/B/C/D/E/F 类型
Step 2.2: Rival Hypothesis Matrix — 每条 claim 列 2-3 个 rival
Step 2.3: Falsifiability Test — 每条 claim 写一行
Step 2.4: Scoop Matrix — 相对 ≥ 2 篇 closest competing work
```

---

## 6. 与 paper_review 的对接

`paper_review` simulated peer review 模式应:

- 用 Claim Typology 检查每条 claim 的措辞与证据等级是否匹配
- 用 Rival Hypothesis Matrix 检查是否预先回应了主要替代解释
- 用 Falsifiability Test 检查 claim 是否过软或过大
- 用 Scoop Matrix 评估 differential 维度数 → 投稿档次建议

---

## 7. 模板文件

`paper_outline` 输出 `paper/PAPER_PLAN.md` 时,加入以下小节:

```markdown
## Claim Typology
| ID | Claim | Type (A-F) | Evidence Level | Notes |

## Rival Hypothesis Matrix
[如本文件 §2 表]

## Falsifiability Tests
- Claim 1 falsifiability: ...
- Claim 2 falsifiability: ...

## Scoop Matrix
[如本文件 §4 表]

## Differential Dimensions
- N dimensions distinct from closest competing work
- Recommended target tier: Nature / NCC / NC / specialty
```
