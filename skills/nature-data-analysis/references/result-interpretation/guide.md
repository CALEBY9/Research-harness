# nature-data-analysis: result-interpretation mode

Use this mode only for its requested deliverable. Its owning skill is `nature-data-analysis`.
Resolve mode-local manifest, scripts, static fragments and references from
`MODE_DIR`, the directory containing this guide. Select only the needed
mode; this resource is not a separate skill or a mandatory next stage.

Use subagents only when the user explicitly requests delegation; otherwise perform role checks locally.

Analyze research results from: **$ARGUMENTS**

## Role in the Research Workflow

This completed-output mode is the evidence organizer within `nature-data-analysis`. It turns completed analysis outputs into paper-ready claim evidence, uncertainty notes, limitations, and figure/table plans.

This mode does not rerun primary cleaning, statistical models or rendering.
Complete the requested interpretation and return. Identify a missing calculation
explicitly; enter the computational branch only if that calculation is actually
requested or already authorized within a combined task, never as a self-handoff.

Complete the requested operation only. Use the corresponding owner for a needed handoff within the user's authorized scope; these skills are not a mandatory stage chain.

This owner organizes and interprets completed results. When the deliverable is
selection of a central claim, comparison of scientific interpretations or a
research-continuation decision, `nature-scientific-insight` owns the recommendation.
For claim-support notes, reuse its
[judgment criteria](../../../nature-scientific-insight/references/judgment-criteria.md) on
evidence strength and competing explanations; do not duplicate a completed
assessment or treat interpretation alone as author approval of a new mainline.

## Expected Inputs

Inspect available materials first:

- `refine-logs/FINAL_PROPOSAL.md`
- `refine-logs/EXPERIMENT_PLAN.md`
- `refine-logs/EXPERIMENT_TRACKER.md`
- `experiments/<timestamp>_<topic>_attempt_k>/`
- completed `nature-data-analysis` outputs such as `results/data_analysis/ANALYSIS_REPORT.md`, `DATA_AUDIT.md`, `STATISTICAL_DIAGNOSTICS.md`, `ANALYSIS_RUN_MANIFEST.md`, tables, figures, or scripts
- result CSV/JSON/NetCDF/GeoTIFF/statistical outputs
- model logs, analysis notebooks, map outputs, or figure drafts
- user-provided observation summaries or tables

If no usable result evidence exists, report the missing results rather than
inventing findings. Reuse any supported subset. Name the missing calculation
and required inputs; a calculation gap does not itself authorize computation
or another invocation of the parent skill.

## Workflow

### Step 1: Locate and Classify Evidence

Group files by:
- run or experiment block
- dataset / region / temporal period
- baseline or model variant
- metric or response variable
- figure/table target
- claim tested

### Step 2: Build Comparison Tables

For each relevant claim, organize:
- primary metric or environmental indicator
- baseline and comparator systems
- effect size, uncertainty, confidence interval, or variability where available
- spatial/temporal pattern
- sensitivity or robustness result
- missing or failed runs

### Step 3: Establish What the Result Adds

For every finding, separate:

1. **Observation** — what the data show, with numbers or file references
2. **Interpretation** — plausible scientific or methodological explanation
3. **Claim support** — which claim is supported, weakened, or unresolved
4. **Uncertainty** — data quality, scale mismatch, sampling, model assumptions, stochastic variance
5. **Next check** — follow-up analysis needed before paper writing

Do not upgrade correlation, map pattern, or model performance into mechanism unless the evidence supports it.

State the strongest useful conclusion that remains after the limitations, not
only what cannot be inferred. Relate it to the closest available comparison:
who can estimate, compare, understand or act more reliably, and why? A better
estimate, boundary or reusable resource can matter without reversing consensus.
When that added value is unresolved, identify the missing comparison instead of
adding generic importance language. Keep the observation-to-interpretation link
usable by nature-writing; manuscript prose belongs to the writing owner.

Preserve denominators and unknown states in downstream summaries. For nested
categories, set membership alone does not explain conditional proportions.
Neither observed proportions nor stress scenarios establish measurement-error
intervals, causal mechanisms or rankings of method quality.

### Step 4: Produce Figure and Table Readiness Notes

For each candidate figure/table:
- purpose in the paper argument
- data provenance path
- plot type or professional software workflow
- minimum annotation needed
- whether it is main-paper, supplementary, or not ready
- missing analysis before final plotting

### Step 5: Legacy Claim Matrix Migration

If an existing project already has an older claim table such as `| Claim | Evidence | Strength | Figure/Table | Missing Check | Risk |`, do not discard it. Upgrade it minimally before downstream writing, figure freeze, or reproducibility review:
- preserve the original claim and evidence wording
- add stable or provisional `Claim ID` values
- add `Evidence ID / Locator` only when a real source, row, file, page, figure, table, or output locator exists
- add `Source / Output Path`, `Analysis provenance path`, `Figure/Table target`, and `Boundary condition`
- mark missing locators, provenance paths, and boundary conditions as blockers instead of inventing them

The migrated matrix should match the canonical Claim Support Matrix structure below before `nature-evidence-audit` builds `ARTIFACT_MANIFEST.md`.

### Step 6: Reviewer-Style Evidence Gate

Check:
- Does the result answer the scientific question?
- Does each main claim have direct evidence?
- Are baselines and mature field standards sufficient?
- Are negative or ambiguous results acknowledged?
- Are uncertainty and limitations explicit?
- Does the interpretation clarify a flexible `So what?` significance layer rather than merely reporting an effect or significant change?
- Is cross-domain transfer validated or still assumed?

## Canonical Outputs

Reuse the project's existing evidence notes. For a bounded task, one concise
companion with result locators, supported claims and figure needs is sufficient;
do not require four new files before drafting or rendering. If separate files
are useful, write or propose them under `results/analysis/`:

```text
results/analysis/
├── ANALYSIS_SUMMARY.md
├── CLAIM_SUPPORT_MATRIX.md
├── FIGURE_TABLE_PLAN.md
└── LIMITATIONS_AND_UNCERTAINTY.md
```

Use this structure for `ANALYSIS_SUMMARY.md`:

```markdown
# Analysis Summary

## Inputs Reviewed

## Key Findings

## Claim Support Matrix
| Claim ID | Claim | Evidence ID / Locator | Source / Output Path | Analysis provenance path | Strength | Figure/Table target | Boundary condition | Missing check | Risk |
|----------|-------|-----------------------|----------------------|--------------------------|----------|---------------------|--------------------|---------------|------|

## Baseline / Comparator Summary

## Spatial and Temporal Patterns

## Uncertainty and Limitations

## Figure and Table Readiness

## Evidence Gaps Before `research-agent`
```

## Key Rules

- Do not fabricate results or statistical significance.
- Preserve data provenance paths and carry forward Claim ID / Evidence ID / Locator from `nature-experiment-plan` when available.
- Mark weak, ambiguous, or failed results explicitly.
- Separate observation from interpretation.
- Do not polish into manuscript prose here; `research-agent` handle paper structure and drafting.
- Prefer a compact set of paper-critical findings over exhaustive log summaries.
