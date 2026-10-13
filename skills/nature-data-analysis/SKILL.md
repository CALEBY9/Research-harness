---
name: nature-data-analysis
description: Analyze research datasets or interpret completed outputs into auditable tables, figures, diagnostics, supported claims and uncertainty notes. Use for 数据分析、统计计算 or 已有结果解释; reuse completed computation when only interpretation is requested.
---

Use subagents only when the user explicitly requests delegation; otherwise perform role checks locally.

# Research Data Analysis — Reproducible, Evidence-Oriented

Analyze research data from: **$ARGUMENTS**

## Role in the Research Workflow

`nature-data-analysis` is the execution-stage data analysis skill. It turns raw, interim, or processed datasets into auditable analysis outputs: data audits, cleaning notes, exploratory summaries, statistical/model diagnostics, result tables, figures, scripts, and analysis reports.

Complete the requested operation only. Use the corresponding owner for a needed handoff within the user's authorized scope; these skills are not a mandatory stage chain.

Boundary:

- `nature-experiment-plan` designs what evidence is needed.
- `nature-data-analysis` reads, checks, transforms, analyzes, visualizes, and reports the data.
- Its completed-output mode interprets existing results as claim evidence, uncertainty, limitations and figure/table readiness without new computation.
- `nature-evidence-audit` checks that data, scripts, commands, figures, tables, and claims are traceable and rerunnable.

Read [analytical design](references/analytical-design.md) for inferential,
conditional or paper-level comparisons, or when units/denominators are uncertain.
Read [figure execution](references/figure-execution.md) when a rendered scientific
figure is requested. Simple summaries and local figure edits do not require a
new study-design exercise. Optional model/search guidance is loaded only by its
specific triggers below.

## When to Use

Use `nature-data-analysis` when the user asks to:

- analyze a CSV, Excel, Parquet, NetCDF, GeoTIFF, vector GIS file, model output, metrics table, or scenario result;
- inspect data quality, missingness, outliers, variable semantics, units, spatial/temporal extent, or sample structure;
- run or plan EDA, statistical tests, regression, GLM/GAM, mixed effects, time-series analysis, spatial analysis, optimization comparison, scenario comparison, sensitivity, uncertainty, or power/sample-size sanity checks;
- generate reproducible analysis scripts, tables, figures, diagnostics, and an analysis report;
- compare layouts, treatments, scenarios, baselines, models, methods, regions, periods, or ecological/energy/economic indicators.

For interpretation of completed results, select
[result-interpretation mode](references/result-interpretation/guide.md), reuse
the existing outputs, complete that mode and return. Do not enter the
computational workflow below or rerun cleaning/statistics for that request.
Select computation only for a requested new calculation, data audit or rendering
operation. A combined analysis-and-interpretation task uses each needed part
once, reusing the same evidence without calling this skill again.
Choosing a dominant claim, judging research value or comparing scientific
interpretations belongs to `nature-scientific-insight`; manuscript drafting and
polishing retain their writing owners.

## Expected Inputs

Inspect available materials first:

- data paths or directories;
- research question, hypothesis, or comparison target;
- response variable, predictors, grouping variables, spatial unit, temporal unit, and units when available;
- existing notebooks, scripts, logs, model outputs, figures, or tables;
- constraints such as Python/R preference, no heavy dependencies, GIS software, remote-sensing workflow, privacy, licensed data, or runtime budget.

If the data path, schema, or analysis target is missing, produce a compact `AUTHOR_INPUT_NEEDED` checklist rather than inventing data or conclusions.

First recover missing inputs from supplied files and project authority pointers.
Ask only for information that cannot be recovered and changes the analysis;
continue independent supported work when one comparison is blocked.

## Computational workflow

Use only the steps needed by the requested computational operation; completed
interpretation-only work does not enter this branch.

### Step 1: Data Intake and Audit

Identify:

- file format, row/column count, variables, data types, coordinate reference system, temporal range, and units when available;
- raw/interim/processed status and whether raw data must remain immutable;
- missing values, duplicated records, obvious impossible values, outliers, quality flags, class imbalance, spatial/temporal gaps, and license or access limits;
- whether the dataset can answer the stated question at the requested scale.

Stop or reframe when data are unreadable, schema is unclear, units are missing for key variables, or sample size/coverage cannot support the requested inference.

### Step 2: Cleaning and Preprocessing Plan

Specify or implement only necessary transformations:

- type conversion, unit harmonization, filtering, joins, aggregation, resampling, reprojection, normalization, feature construction, or missing-data handling;
- separation of raw, interim, processed, and derived outputs;
- provenance for every nontrivial transformation.

Never overwrite raw data. Do not silently drop records; record exclusion rules and counts.

### Step 3: Exploratory Data Analysis

Produce method-appropriate summaries:

- descriptive statistics, distributions, group summaries, trends, maps, correlations, pairwise relationships, and anomaly checks;
- sample size by group/region/period;
- preliminary plots that reveal data structure, not just publication graphics.

Mark EDA as exploratory unless a confirmatory design was specified before looking at the data.

### Step 4: Method Selection

Choose analysis methods from the data structure and question, not from keywords alone. Consider:

- tool selection: use the existing local environment first; use `pandas` for small/ordinary tables, optional `polars` lazy/streaming for large CSV/Parquet or multi-file ETL when installed or approved, and optional `statsmodels` when the question requires coefficient inference, OLS/GLM/discrete/mixed/time-series models, robust standard errors, residual diagnostics, or publication-ready statistical tables;
- group comparison: t-test, ANOVA, nonparametric alternatives, paired/repeated designs, multiple-comparison control;
- association and prediction: correlation, regression, GLM/GAM, regularized models, tree/boosting methods when justified;
- hierarchical data: mixed effects or clustered/blocked analysis;
- time series: autocorrelation, trend, seasonality, intervention, or forecasting diagnostics;
- spatial/GIS/remote sensing: CRS, scale mismatch, spatial autocorrelation, zonal statistics, raster/vector alignment, spatial cross-validation;
- scenario, layout, or optimization studies: baseline definition, objective functions, constraints, sensitivity, Pareto trade-offs, and robustness;
- Bayesian analysis only when priors, likelihood, diagnostics, and reporting boundaries can be stated.

If assumptions fail, propose or run an appropriate alternative instead of forcing a preferred test.

Do not install `polars`, `statsmodels`, or optional accelerators as hidden requirements. If they are absent and the analysis can proceed with existing tools, continue and record the tradeoff; if their absence changes correctness or feasibility, ask for approval or return `METHOD_NOT_IDENTIFIED`.

#### Optional model and search tasks

For an explicitly relevant small-tabular foundation-model baseline, automated
candidate search or score-driven iteration, read
[optional model/search guidance](references/optional-model-search.md).
It retains eligibility, authorization, leakage, budget and search-record rules;
do not load it for ordinary summaries, statistical analysis or plotting.

### Step 5: Diagnostics, Effect, and Uncertainty

Where applicable, check and report:

- normality, variance homogeneity, independence, residual patterns, leverage/influence, multicollinearity, autocorrelation, spatial autocorrelation, missingness mechanism, and model convergence;
- effect size or magnitude, confidence/credible intervals, variability, uncertainty bands, and sensitivity to thresholds or preprocessing choices;
- power or sample-size sanity check when null results, small samples, or underpowered comparisons would affect interpretation.

Avoid presenting p-values without effect magnitude and uncertainty when the claim depends on practical or ecological importance.

### Step 6: Generate Tables, Figures, Scripts, and Report

Reuse the project's output convention. Deliver the requested result with the
smallest sufficient script, table, figure and explanation. A bounded task can
use one report; the following is an optional structure for a substantial study,
not a mandatory packet or a reason to stop at planning:

```text
results/data_analysis/
├── DATA_AUDIT.md
├── ANALYSIS_PLAN.md
├── ANALYSIS_REPORT.md
├── STATISTICAL_DIAGNOSTICS.md
├── ANALYSIS_RUN_MANIFEST.md
├── tables/
├── figures/
├── scripts/
└── logs/
```

Use lightweight scripts or notebooks as appropriate, but paper-critical results should have a rerunnable script, command, or frozen notebook with documented environment assumptions.

## Computational output examples

Use these only for requested computational outputs. Interpretation-only work
uses its mode guide and does not create this packet as a prerequisite.

### `DATA_AUDIT.md`

```markdown
# Data Audit

## Inputs Reviewed
| Path | Format | Role | Rows / Size | Key Variables | Notes |
|------|--------|------|-------------|---------------|-------|

## Schema and Semantics
| Variable | Type | Unit | Meaning | Missing | Quality Issue |
|----------|------|------|---------|---------|---------------|

## Fitness for Question
- Question:
- Supported scale:
- Unsupported scale or claim:
- Decision: PROCEED / REFRAME / AUTHOR_INPUT_NEEDED / STOP
```

### `ANALYSIS_PLAN.md`

```markdown
# Analysis Plan

| Step | Purpose | Input | Method / Tool | Output | Decision Gate |
|------|---------|-------|---------------|--------|---------------|
```

### `STATISTICAL_DIAGNOSTICS.md`

```markdown
# Statistical and Model Diagnostics

| Analysis | Assumption / Diagnostic | Result | Decision | Alternative if Failed |
|----------|-------------------------|--------|----------|-----------------------|
```

### `ANALYSIS_RUN_MANIFEST.md`

```markdown
# Analysis Run Manifest

| Step | Input | Script / Command | Output | Status | Notes |
|------|-------|------------------|--------|--------|-------|
```

### `ANALYSIS_REPORT.md`

```markdown
# Analysis Report

## Question and Data

## Data Quality and Preprocessing

## Exploratory Findings

## Methods Used and Why

## Results
| Result ID | Output | Statistic / Metric | Effect / Uncertainty | Table / Figure | Script / Command |
|-----------|--------|--------------------|----------------------|----------------|------------------|

## Diagnostics and Robustness

## Supported Interpretation and Limits

## Claim-Evidence Notes
| Evidence ID / Locator | Output Path | Candidate Claim | Boundary Condition | Missing Check |
|-----------------------|-------------|-----------------|--------------------|---------------|
```

## Failure Codes

Use explicit failure or return codes:

- `DATA_NOT_READABLE`
- `DATA_SCHEMA_UNCLEAR`
- `AUTHOR_INPUT_NEEDED`
- `INSUFFICIENT_SAMPLE_SIZE`
- `METHOD_NOT_IDENTIFIED`
- `TABPFN_NOT_ELIGIBLE`
- `OPTIONAL_DEP_NOT_APPROVED`
- `LICENSE_OR_LOGIN_BOUNDARY`
- `LEAKAGE_RISK_UNRESOLVED`
- `SCORABLE_TASK_NOT_ELIGIBLE`
- `SEARCH_METRIC_UNSTABLE`
- `SEARCH_STAGNATION_UNDIAGNOSED`
- `MECHANISM_APPLICATION_UNVERIFIED`
- `SEARCH_COST_BOUNDARY_MISSING`
- `HOLDOUT_CONTAMINATION_RISK`
- `CANDIDATE_LEDGER_MISSING`
- `BASELINE_COMPARISON_INCOMPLETE`
- `ASSUMPTION_FAILED_NEEDS_ALTERNATIVE`
- `RESULT_NOT_REPRODUCIBLE`
- `CLAIM_INTERPRETATION_REQUIRED` — resolve within result-interpretation mode, without a self-handoff
- `EXPERIMENT_PLAN_REQUIRED` — identify the design gap for `nature-experiment-plan`; do not launch a new stage automatically

## Key Rules

- Do not fabricate data, rows, statistics, p-values, effect sizes, maps, model outputs, or significance.
- Do not overwrite raw data; write derived outputs separately.
- Prefer the smallest analysis that answers the question; do not add Airflow, Kedro, DVC, MLflow, Spark, or cloud infrastructure as default requirements.
- Use heavy tools only when the dataset or project already requires them and the user accepts the dependency.
- Do not install packages, upload data to external services, or use cloud/agent-based processing for private, licensed, or sensitive datasets without explicit user approval. Prefer existing local environments and record any dependency changes.
- Treat tabular foundation models as optional baselines with explicit eligibility, leakage, license, checkpoint, device, and reproducibility records; never make them hidden defaults.
- Keep exploratory and confirmatory analysis distinct.
- Preserve paths, commands, and assumptions so `nature-evidence-audit` can audit them.
- Include claim-evidence interpretation when it is part of the requested deliverable, reusing the completed outputs within this skill. A scientific claim-selection decision uses `nature-scientific-insight`; no mandatory self-handoff precedes writing.
