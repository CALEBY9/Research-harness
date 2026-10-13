# From question to discriminating analysis

Use for paper-level comparisons, inference or unresolved measurement semantics.
The author's design remains authoritative. Complete authorized descriptive work
even when a stronger inference is unavailable; propose new analyses separately
when they change the approved question, sample, metric or protocol.

## Define the quantity before choosing a test

Recover the target population, independent unit, eligible denominator, contrast,
time/space window and intended interpretation. Distinguish counts, within-group
rates, composition among positives, and conditional proportions. A sum across
overlapping groups is not a population count; fractional attribution is not an
independent sample of that size. Record these meanings in the existing analysis
note or script, not a second scientific authority file.

Before a merge, establish the key and expected one-to-one/one-to-many relation;
reconcile unmatched keys and row multiplication. Before aggregation, check unit
conversion, duplicate observations and group/window membership. Keep unknown,
not applicable, absent and observed zero distinct through tables and figures.
Do not fill unknown labels as negative to make percentages sum neatly.

For spreadsheets, verify the source rows behind a decisive cached total or
formula: a nearby year/group label does not establish formula membership.
Reconstruct from eligible records when the aggregation is wrong; preserve the
source. Audit missingness separately inside and outside the selected window;
unrelated historical gaps do not require imputation or invalidate a complete
selected comparison. A derived table still inherits unresolved source identity.

## Select the comparison that answers the question

| Question | Necessary design decision | Common failure |
|---|---|---|
| Distribution or change | Comparable coverage, denominator, units and measurement across groups/time | Corpus growth presented as increasing adoption |
| Association or explanation | Plausible competing explanations, adjustment rationale and observable discriminating contrast | Significance or model fit presented as a mechanism |
| Prediction | Intended deployment shift, independent split, baseline and leakage controls | Random row split across repeated sites/subjects |
| Scenario comparison | Fixed baseline, changed assumptions and interacting policy/model components | Sequence differences treated as isolated component effects |
| Measurement validity | Independent reference, missingness and misclassification design | A rerun or source check described as expert validation |

Use the smallest scientifically adequate method. Select adjustment variables
from the scientific design; a long regression does not repair outcome-defined
predictors, post-treatment adjustment or unmeasured confounding. For a rival
explanation, state what it predicts too and which additional observation would
distinguish it. If none is available, report that inferential limit and the
useful descriptive result rather than manufacturing an explanatory model.

### When aggregate ratios drive the story

With matched numerator/denominator categories, a ratio of totals is a
denominator-weighted average of category ratios. Different composition can
therefore produce different aggregate ratios without any within-category
difference. Inspect the available category quantities before calling a regional
ratio efficiency or a marginal return. Standardization/decomposition needs
matched category-level quantities and a justified reference; aggregate totals
alone do not identify the composition contribution. Keep a proposed decomposition
separate when the required data or scientific authorization is absent.

### When a joint intervention is claimed to add value

Where two components can be varied independently, comparable neither/A/B/both
conditions can distinguish a joint result from component effects. On a fixed
outcome scale, the additive interaction is Y_both - Y_A - Y_B + Y_neither;
its sign means different things for benefits and costs and is scale-dependent.
Keep non-treatment assumptions, outcome accounting and the solution-selection
rule comparable. An infeasible cell or a changed constraint/selection rule may
prevent this interpretation. Optimization ranks or TOPSIS scores from different
candidate sets are not physical outcome effects. Do not run new scenarios merely
because this comparison would be useful; respect the authorized design.

## Match uncertainty to the evidence

Respect the independent sampling/assignment unit and dependence across space,
time and groups when resampling or fitting uncertainty. Document clustering,
blocking, weights and effective support when relevant. Aggregate counts alone
may not identify the correct sampling or measurement-error model.

Report effect magnitude in interpretable units with supported uncertainty.
Unknown-label scenarios are assumption-dependent sensitivity ranges, not
confidence intervals. Distinguish sampling variability, measurement error,
model/scenario uncertainty and incomplete coverage; do not use one as a proxy
for all four. A null test is not equivalence without an appropriate margin and
design. Diagnostics should address assumptions relevant to the actual method,
not require normality checks for every dataset.

## Make results usable and check the derivation

Bind each paper-facing value to the selected source rows and calculation. Check
a small decisive result independently (for example from counts rather than a
precomputed percentage), including its denominator and direction. Reconcile
exported plot data with the table and caption. Use a targeted perturbation or
alternative comparison only when it can change interpretation; mark exploratory
choices and retain failed or incompatible results when they affect the claim.

Handoff: state the observed contrast, the strongest supported interpretation,
the unresolved alternative and the evidence needed to discriminate it. A new
observation requiring production changes returns to the author/planning owner;
routine calculation repair within the authorized design should be completed.
