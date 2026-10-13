# Execute and finish a scientific figure

nature-data-analysis owns computation, plotting data and the figures delivered as part
of its analysis task, including rendering and in-scope visual repair.
nature-figure can directly render publication figures from verified results and
owns their design and review; do not create a second executor for the same plot.
nature-writing owns the paper argument; nature-data-analysis is needed only for unsettled
result interpretation. Reuse a sufficient approved
figure plan. Do not introduce a mandatory new spec or ask the author to perform
routine coding, layout or export decisions.

## Choose a visual comparison

Start with the reader's question, supported result and the quantity to compare.
Map it to a main panel that exposes that relation directly:

- magnitude or ordered comparison: aligned points/bars on a common scale;
- counts versus within-group rates: aligned panels with the same category order,
  separate explicit units and denominators; avoid ambiguous dual axes;
- conditional proportion: show the conditioning set and unresolved coverage,
  rather than presenting a selected denominator as full-population prevalence;
- change: comparable time coverage and baseline; distinguish cohort change from
  changing sample composition;
- effects with defensible uncertainty: estimates and labeled intervals with a
  meaningful reference; do not invent error bars from incomplete aggregates;
- spatial patterns: appropriate projection, extent, resolution and legend;
  a map does not itself identify spatial causation.

Use only supporting panels that clarify heterogeneity, comparison conditions or
robustness. Give the central comparison most visual space. A concept figure uses
an appropriate concept/vector workflow; quantitative values must come from code
and real data, not an image generator. An existing approved figure package stays
protected; render candidates separately.

## Encode scientific meaning

Keep category order, labels, units and colors consistent. Show missing/unknown
separately from zero/negative and label any excluded denominator. Comparable
panels need comparable scales or explicit reasons for a different scale. A nested
category's higher proportion is not greater quality; avoid maturation arrows or
red/green success signals without that scientific meaning.

Use restrained color for the decisive distinctions, redundant shapes/labels
where needed, legible type at the intended publication size and direct labels
when they reduce lookup. Avoid decorative 3-D, gradients and unnecessary grid
lines. Reuse the project's typography and palette; journal names are not styles.
Keep scientific conditions visible in the figure/legend and administrative
version/provenance in the separate companion.

## Render, inspect, repair

Use the existing working Python/R/GIS/Origin workflow. Do not introduce a new
dependency just for aesthetic polish. Keep source code and plotting data;
deliver editable vector output where appropriate plus a raster preview.
Text-as-text SVG or embedded PDF fonts aid editing, but editable raster/maps may
also require the project file and source layers. State what was actually checked.

Inspect the exported image at intended size, not only an interactive canvas.
Check clipping, collisions, panel hierarchy, labels, legend, numerical mapping,
line weights and necessary uncertainty. Independently inspect the vector export
for retained text/layers when promising editability. Correct observed defects
and render again; successful save or code review alone is not visual inspection.

Reconcile figure, legend and manuscript claims after changes. Deliver the actual
figure and a concise caption, with script/data provenance separately. When an
independent reader evaluation is available and authorized, ask what comparison,
finding and limits they infer. Agent visual inspection is not independent reader
validation, and attractive output alone is not evidence of scientific gain.
