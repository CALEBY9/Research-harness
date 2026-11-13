# Section: Method (writing)

## Default structure

Choose the structure from the actual study design before applying a module
template. Observational, literature-analysis and evidence-synthesis studies
need population and selection, units and operational definitions, measurement
and missingness, reference/error evaluation, and comparisons or inference.
Explain which scientific question each comparison answers and what it cannot
identify. An algorithmic module/ablation structure applies only when the paper
actually introduces and tests such modules. Learn from empirical exemplars with
compatible designs; a conceptual Perspective is not an implementation model.

For an algorithmic contribution, a possible order is:
`task formulation -> overview (pipeline / system / approach) -> per-module detail -> implementation notes -> assumptions and boundary`.

## The three-element pattern (per module)

For studies that introduce and test modules, each module should answer:

1. **Motivation** — what problem this module addresses within the research question
2. **Mechanism** — what the module actually does, to a level a peer could re-implement
3. **Evidence / role** — how its contribution is assessed by comparisons actually performed

If any element is missing, the module reads as a black box. Flag the gap.

## Pre-writing checklist

Before drafting Method, read the author's materials for the following facts;
ask only for missing information that materially affects the section:

- Task formulation: inputs, outputs, scope.
- Overview figure / pipeline diagram: does one exist? It anchors the section.
- Notation: defined once and consistent.
- Reproducibility scope: code, weights, data — what will be released.

## Forbidden vague phrases

Never leave:

- `under standard conditions`
- `using routine methods`
- `data were analyzed statistically`
- `the method was validated`
- `samples were randomly assigned` (without saying how)

Replace with the actual reproducible information.

## Deeper reference

For module-motivation templates, three-elements examples, and overview-template patterns, open `references/method.md` and `references/examples/method/`.
