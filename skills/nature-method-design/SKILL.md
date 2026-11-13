---
name: nature-method-design
description: Design research methods or experiment and validation plans for selected questions. Use for 研究设计、方法方案、实验计划、对照与验证路线; not proposal-document writing or executing analyses.
---

# Research Design — 研究设计

Use the author's selected question and existing evidence. Choose the requested
deliverable before loading a mode; these are two depths of one design task.

| Requested deliverable | Read |
|---|---|
| Compare or refine implementable methods, data choices and assumptions | [Method proposal](references/method-proposal.md) |
| Specify experiments, baselines, validation blocks, run order and figure roadmap | [Experiment plan](references/experiment-plan.md) |

For a combined request, reuse the method decision and data audit when developing
the plan. Do not invoke this skill again or require both outputs for one mode.
Existing proposals can enter experiment-plan mode directly. Proposal/opening-report
documents belong to `nature-proposal-writer`; execution and interpretation belong
to `nature-data-analysis`. Scientific value and unresolved contribution choices
use `nature-scientific-insight` criteria, reusing sufficient prior judgments.

## Shared constraints

For model-assisted initial planning and refinement, use the plan-refiner roles in
[the collaboration policy](../nature-shared/core/model-collaboration.md). Reuse
the selected idea, source evidence and pilot results. Start with the decisive
comparison and a minimal pilot; use its outcome to refine the larger plan.
Additional models are optional support, not approval gates or proof of validity.

- Recover the approved question, study design, units, scales, comparators and
  constraints from the project's authority documents. Preserve their scientific
  meaning; recommend material changes for the author to decide.
- Reuse the existing data audit. Fill only relevant gaps in source/coverage,
  semantics/units, resolution, missingness, dependence, access and licensing.
  A missing legacy filename is not a reason to restart design or create files.
- A planning or review request does not authorize data acquisition. For marine
  co-location, identify missing bathymetry, environment, sea-use or engineering
  evidence; download or stage it only when needed and authorized. Record actual
  sources, access conditions and failures if acquisition is performed.
- Select evidence requirements for the research design. Algorithm baselines,
  ablations, random seeds and assisted-search checks apply only when relevant;
  literature, observational and scenario studies need their own validity checks.
- Missing data, untested assumptions and negative findings stay explicit. Do not
  invent availability, novelty, expected performance, results or citations.
- Use the existing project layout and records. Mode templates are optional ways
  to supply missing information, not mandatory parallel state systems.
- Deliver the requested design with supported choices, decisive comparisons,
  failure interpretations and feasible effort. Planning is not execution.
  Do not launch experiments, subagents or a new research stage by selecting a mode.
