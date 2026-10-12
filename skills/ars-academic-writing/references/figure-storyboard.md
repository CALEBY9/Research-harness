# Figure storyboard

Use for paper-level figure planning or a substantive visual-argument redesign.
For a local label, palette or layout edit, preserve the approved figure and use
the relevant editor directly. This reference plans the argument; it does not
generate data or establish a new plotting owner.

## Extend the existing figure plan

Reuse `res_analyze`'s `FIGURE_TABLE_PLAN` or the project's existing figure spec.
It already covers purpose, provenance, software, annotations, readiness and
missing analysis. Add only the missing information needed to answer:

- What one scientific question should the reader answer from this figure?
- Which supported comparison answers it, and which main panel makes that
  comparison easiest to see? Name the associated Results claim or passage.
- What does each supporting panel add: a comparator, heterogeneity, an
  alternative explanation, or a sensitivity check? Remove redundant panels
  from the proposal without deleting approved assets.
- What should the reader understand next, and how does the next figure advance
  the paper? Do not prescribe a fixed figure count or force every study into a
  mechanism diagram followed by performance plots.

If evidence is missing, mark that panel as proposed. An attractive layout is not
permission to estimate missing values or upgrade a historical result. Where
the author has frozen the figure package, propose changes separately.

## Match visual comparisons to scientific comparisons

Retain the authoritative data version, population, unit, denominator, weighting
and validation status. Check whether panels are actually comparable before
sharing scales, rankings or effect labels. Counts, adoption rates and conditional
composition answer different questions. An unknown-label stress range is not a
confidence interval or an independently validated measurement-error bound.

Separate conceptual relations from measured effects. Specify arrow meanings;
layout proximity, line thickness and icon size must not imply an unmeasured
causal relation, prevalence or maturity ordering. Show necessary uncertainty
and alternative explanations without relegating a decisive limitation to small
print. A planned mechanism belongs in a hypothesis diagram, not a Results panel.

Give the decisive comparison most of the visual area. Use consistent category
order, names, colors, units and uncertainty notation across the manuscript where
their meanings match. Select charts from the relationship to be read, not from
a journal-style keyword. Keep essential comparison conditions visible; place
supporting methodological detail in the legend or Methods.

Make the claimed relationship directly readable in one panel or aligned panels.
For example, a contrast between research volume and within-task use cannot be
read from task counts alone; do not make readers reconstruct it across unrelated
tables or heatmaps. This does not authorize adding an uncomputed comparison.

## Hand off to a working renderer

For quantitative figures, use the project's existing Python/R/GIS or other
verified plotting workflow through `data_analyze`; use `editaplot` only when
available and its Origin runtime has been checked. Do not use image generation
to invent or render quantitative results. Preserve editable source and the
project's provenance requirements.

When rendering is part of the authorized task, the executing owner reads
[figure execution](../../data_analyze/references/figure-execution.md), completes
the data mapping, exports the actual figure, inspects it and repairs observed
defects. Do not end at this storyboard or send routine layout decisions back to
the author. Missing scientific comparisons remain proposals, not invented panels.

For conceptual prompts, `nature-image2-prompt` consumes a complete logic
wireframe and visual specification. A storyboard alone does not satisfy its
node/edge semantics, selected direction, prompt preflight or author-approval
requirements. Prepare missing planning information within the authorized scope;
do not mark it approved, waive a check or restore a retired owner chain.
An existing approved project spec can supply the contract. The prompt owner
checks it irrespective of which currently available tool prepared it.

Check actual callable capabilities before promising a rendering or QA handoff.
A directory on disk, a referenced skill name or an importable plotting package
does not demonstrate a functioning end-to-end renderer. Report the specific
missing capability and complete the usable plan; do not install tools silently.

## Verify the delivered figure, when rendering is authorized

Check the plotted values and transformations against the source separately from
visual inspection. Render at the intended display or publication size and inspect
the actual image for clipping, label readability, panel hierarchy, meaningful
color contrast and legend coverage. Verify any promised editable export, then
check the figure, legend and manuscript for agreement. Do not claim visual QA
from source code or successful file creation alone.

For a figure-reading evaluation, show only the figure and legend to an authorized
reader and record the finding, comparison and limiting conditions they infer.
Compare these with the intended claim. Identify whether feedback came from the
author, another reader or a model; self-review is not independent validation.
This is an evaluation option, not a compulsory extra model call or a substitute
for delivering the requested figure.
