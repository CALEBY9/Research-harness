# Optional foundation models and scored search

Load only for the explicit triggers below. Existing package, account, private-data,
license and compute authorizations still apply. This is not an ordinary analysis
prerequisite.

#### Small-Tabular Foundation Baseline Gate

For supervised classification or regression on a single flat table, consider a tabular foundation model such as TabPFN only as an optional rapid baseline, not as a default dependency or replacement for mature field baselines.

Run this eligibility gate before recommending or using such a model:

```markdown
| Dataset | Rows | Features | Task | TabPFN eligible? | Required baselines | Leakage / split risk | Decision |
|---------|------|----------|------|------------------|--------------------|----------------------|----------|
```

Eligibility requirements:

- the task is supervised classification or regression on structured tabular data;
- row count, feature count, class count, and hardware fit the selected checkpoint's documented limits;
- the train/test or cross-validation split is scientifically valid, with spatial, temporal, grouped, subject-level, or site-level leakage handled before model comparison;
- the analysis goal is quick feasibility screening, a strong small-data baseline, or model comparison, not causal identification or mechanism proof;
- XGBoost, CatBoost, LightGBM, random forest, linear/statistical, or other mature domain baselines remain planned when the result may support a paper claim.

If the model is actually run, record it like any other method:

```markdown
| Method | Version / checkpoint | Device | Split / CV | Metric | Runtime | Result locator | Caveat |
|--------|----------------------|--------|------------|--------|---------|----------------|--------|
```

Rules:

- Do not install `tabpfn`, use a hosted API, download model checkpoints, cache authentication tokens, or accept model licenses without explicit user approval.
- Treat TabPFN-style results as a baseline or exploratory signal until `res_analyze` and `evidence_audit` verify claim fit, leakage controls, environment, checkpoint, commands, and output locators.
- Do not generalize Nature / vendor benchmark claims beyond their stated dataset-size, task, hardware, and evaluation boundaries.
- For large tables, real-time inference, production latency, multi-table relational data, unstructured inputs, time-series dependence, spatial prediction, or causal claims, prefer the existing method-selection and diagnostic gates unless a project-specific validation justifies otherwise.

#### Candidate Search / Scored Iteration Ledger

Use this ledger when `res_plan` marks an analysis block as a scorable task, or when the user asks for automated method search, repeated code/model improvement, hyperparameter or architecture search, candidate recombination, LLM-assisted code generation, or score-driven optimization.

The ledger is not required for ordinary one-shot statistics, EDA, baseline fitting, or deterministic data cleaning.

```markdown
| Candidate ID | Parent / source idea | Intervention type | Code / config locator | Application status / proof | Dataset split | Quality score | Baseline delta | Runtime / total cost | Failure or warning | Next action |
|--------------|----------------------|-------------------|-----------------------|----------------------------|---------------|---------------|----------------|----------------------|--------------------|-------------|
```

Rules:
- Record failed, excluded, and low-scoring candidates when they affect the interpretation of the winning result.
- Classify `Intervention type` as `parameter/config`, `search-mechanism/control-flow`, `metric/evaluator`, or `environment/tool`. Repeated proposals, no new evidence, parameter fixation, or metric saturation require cause diagnosis before another search round; they do not automatically justify a mechanism-level change.
- A mechanism-level candidate is eligible only when the metric/evaluator and immutable artifacts are frozen, the baseline is reproducible, and a rollback target exists. Generated code, prompts, skills, or patches count as applied only when a diff/hash/snapshot/load log proves activation before the scored result; otherwise mark them reverted or invalid.
- Keep search/training, validation, and holdout scores separate; never select on a holdout set and then report it as independent evidence.
- Do not treat a score gain as a mechanism, causal, or general scientific claim until `res_analyze` and `evidence_audit` check the evidence boundary.
- If candidates are recombined from prior methods or literature summaries, record their parent/source idea and hand the provenance to `evidence_audit`.
- For tree search, UCB/PUCT-style selection, beam search, best-of-N, retry loops, or other branch-and-score procedures, record the search policy, parent-selection rationale, recombination parent(s), manual filtering, and saturation or stop rule; do not report only the winning candidate.
- Report total search cost when material, including runtime, compute, LLM/API use, and human filtering. Equal inner-evaluation counts do not establish equal total compute or efficiency.
- Stop or return to `res_plan` if the metric is unstable, leaks future/label information, rewards a shortcut, or lacks a meaningful baseline.

### `CANDIDATE_SEARCH_LEDGER.md`

Create this only for scorable-task or score-driven candidate-search analyses:

```markdown
# Candidate Search Ledger

## Search Boundary
- Claim / block:
- Metric:
- Search split:
- Validation split:
- Holdout boundary:
- Budget / stop rule:
- Stagnation / saturation criterion:
- Fixed evaluator / immutable artifacts:
- Allowed intervention levels:
- Search policy / parent-selection rule:
- Recombination or branch-source rule:

| Candidate ID | Parent / source idea | Intervention type | Code / config locator | Application status / proof | Dataset split | Quality score | Baseline delta | Runtime / total cost | Failure or warning | Next action |
|--------------|----------------------|-------------------|-----------------------|----------------------------|---------------|---------------|----------------|----------------------|--------------------|-------------|

## Selection Note
- Selected candidate:
- Why selected:
- Application-integrity evidence:
- Absolute baseline / final metric, uncertainty, and total search cost:
- Why this does not by itself prove a mechanism or broad scientific discovery:
```
