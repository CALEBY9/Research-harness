---
name: nature-figure
description: >-
  Create, revise, audit and export scientific figures, prepare conceptual-image
  prompts, and inspect or organize figure references when requested. Use for
  论文配图、科研绘图、机制图提示词、参考图分析 or 图件语料整理; raw-data
  calculation and generic image editing keep their own tools.
---

# Nature Figure Making — Router

This skill is split into two layers:

- A **static layer** under `static/` that holds versioned, reusable content fragments (the figure contract and default stance, plus a per-backend quick-start for Python and R).
- A **dynamic layer** that first selects the requested deliverable. Plotting uses `manifest.yaml` to resolve its backend; other modes use their own guidance. The large design, API, pattern, and QA material lives in on-demand references.

Do not try to apply the figure logic from memory or from this router. Always load fragments from disk as described below.

## Select the requested deliverable first

Choose the applicable branch before loading a plotting manifest or backend.
Non-plotting branches finish with their requested output and return; the plotting
protocol below does not apply to them. For an explicitly combined task, reuse
the shared scientific specification and execute only the requested parts.

| Deliverable | Selected resources and stopping point |
|---|---|
| Scientific plot or manuscript figure assembly | Use the plotting protocol below; resolve Python/R only when rendering or a plotting-source edit requires it. |
| Figure planning or audit only | Read the scientific-design sections of [figure contract](static/core/contract.md) and the existing specification; for supplied figures, use the applicable [QA checks](references/qa-contract.md). Return the plan or findings without starting rendering. |
| Conceptual-image prompt or prompt audit | Read [conceptual-prompts mode](references/conceptual-prompts/guide.md); return the requested prompt/audit without an image call or plotting preflight. |
| Reference-figure comparison/design rules | Read [figure-benchmark mode](references/figure-benchmark/guide.md); return the benchmark/transfer findings, without plot/PDF QA. |
| Reference inventory or corpus intake | Read [figure-corpus mode](references/figure-corpus/guide.md); return the inventory or authorized intake result, without plotting. |
| Requested conceptual-image generation/edit | Use the conceptual-prompt contract and the available authorized image capability; perform the actual-image checks, then return. |

Read the `User-facing privacy rule` section of `static/core/stance.md` for every
branch; its other plotting stance and backend rules apply only to plotting.
Preserve protected scientific content, author approval, copyright, data integrity
and shared-write boundaries in the selected resources. Resolve mode helpers
under MODE_DIR. Inspection or prompt preparation does not authorize shared
intake, generation, external upload, or canonical promotion.

For a new or substantively redesigned conceptual figure, use
`references/conceptual-handoff.md` only for missing fields required by the selected
prompt contract. Reuse a sufficient existing specification; planning does not
grant scientific or visual approval.

For an AI-assisted graphical abstract, read
[AI graphical-abstract guidance](references/ai-graphical-abstract-workflow.md)
and apply only the steps relevant to planning, prompting, generation or audit.
Preserve the approved semantic graph and selected visual direction. Verify the
exact journal's policy when submission eligibility is at issue; an internal
draft is not certified for submission.

Honor a user-specified provider. Otherwise use the current available authorized
image capability and follow its instructions. A generic Image 2 or AI-image
request does not select OpenRouter. Read
[OpenRouter generation guidance](references/openrouter-image-generation.md)
and use `scripts/generate_openrouter_schematic.py` only when OpenRouter was
explicitly selected for the task or already bound by its authorized project
workflow. If that provider is unavailable, report the blocker rather than
silently switching services or uploading unpublished material.

## Plotting and figure-assembly protocol

These steps apply to the selected plotting/assembly branch. Planning-only or
audit-only work uses the needed design/verification sections and returns without
loading a rendering backend, calling renderers, or creating missing exports.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). It declares the `backend` axis, the allowed values, and the file paths each value maps to.

Read the `always_load` files (`static/core/contract.md` and
`static/core/stance.md`) only for plotting/assembly. Their backend and export
requirements do not become defaults for prompt or reference modes.

### 2. Resolve the backend for rendering or plotting-source edits

If the request stops at planning/audit, skip backend setup. Otherwise use the backend-selection rules in `static/core/contract.md`: current explicit choice, existing project workflow, saved preference, then the supported local default. This is a technical choice, not a mandatory approval checkpoint. Read `references/backend-selection.md` only when comparing backends is material to the task. The selected backend remains exclusive throughout rendering and visual QA.

### 3. Load the matching backend fragment

When a backend is needed and resolved, read the mapped fragment (`static/fragments/backend/python.md` or `static/fragments/backend/r.md`). It carries the backend-only execution rule and the publication quick-start (rcParams/theme and export helper). Do **not** load the other backend's fragment.

### 4. Build the figure using the loaded material

For revision of an existing figure, a protected/accepted figure package, or a
claim-bearing figure-readiness decision, first load
`../nature-shared/core/evidence-authority.md`. Bind the exact source and working
copy. Freeze the estimand, data layers, units, statistics, topology or arrow
direction, captions, numbering, and manuscript references unless the author
explicitly approves changing them. A successful render or visual QA pass does
not by itself promote a draft to canonical or license a stronger scientific
claim.

Apply the loaded material in this order:

1. Figure contract (`core/contract.md`) — write the core conclusion, map the evidence chain, classify the archetype, set the journal/export contract, before any code.
2. Multi-panel evidence architecture — when planning, restructuring, or auditing a labelled multi-panel figure, load `references/multipanel-evidence-architecture.md`. Make the figure answer one Results-level scientific question; assign panels different inferential roles, not merely different metrics. When figure order must follow the manuscript argument, also load `../nature-shared/core/nature-results-discussion.md`.
3. Default stance (`core/stance.md`) — archetype-first composition, hero panel, restrained palette, statistics/integrity as part of the figure.
4. Backend fragment — the exclusive Python or R quick-start and execution rule.
5. Template adaptation — when reusing built-in original examples, licensed external material, or user-provided plotting code, load `references/asset-adaptation.md` before mapping data or changing the script.
6. Delivery preflight — for a rendered plot/assembly, load `references/qa-contract.md`. Validate the actual plotting source when present and audit the actual exported PDF when present, then inspect the delivered figure at final size. A requested PDF export must exist and pass its checks; an artifact that the task neither requests nor produces does not become a prerequisite. For planning/audit-only work, check the supplied material and report unassessable rendered properties without creating exports. Automated checks do not replace visual inspection.

For rendering from verified plotting data, use the selected backend and existing
project code directly; no analysis-owner handoff is required. When new aggregation,
joins, uncertainty estimates or statistical comparisons are needed, resolve
`nature-data-analysis` from the installed catalogue and use its analytical-design support.
Keep one rendering executor: an analysis-owned task may render its own plots;
reuse those outputs for figure design/review instead of regenerating them in a
second pipeline. `nature-figure` retains publication design and review ownership.
Do not recompute results to suit a layout. Report unresolved numerics separately
and continue unaffected design work.

When the target is the flagship journal Nature, also load
`references/nature-article-requirements.md`. It separates initial-review files
from accepted-in-principle main and Extended Data production contracts and owns
the flagship legend limit.

When the target is Nature Machine Intelligence, instead load
`../nature-shared/journal-formats/nature-machine-intelligence.md`. Apply its
combined six-item main display budget, ten-item Extended Data maximum,
initial-versus-production boundary, 300-dpi/180-mm production checks and source-
data contract. NMI's current live pages do not assign a standalone per-legend
number, but its official 2018 brief guide set a historical advisory ceiling of
fewer than 300 English words per complete figure legend. Count the whole legend,
not each panel; aim for 150–250 words and keep it below 300 unless the live
submission system or editor gives a newer instruction. Do not import flagship
Nature's limit.

The chart serves the scientific logic; aesthetic polish is subordinate to making the core conclusion clear, defensible, and reviewable.

### 5. Reach for references only when needed

The files under `references/` are deep references, not defaults. Open them on demand per the `references.on_demand` table in the manifest — for example `references/figure-contract.md` to build the contract, `references/multipanel-evidence-architecture.md` to turn one Results-level question into complementary panel roles and a claim-escalating figure sequence, `references/asset-adaptation.md` to reuse a plotting template safely, `references/template-catalog.md` for validated Python CSV templates, `references/api.md` for the Python palette and numerical/layout safety helpers, `references/r-workflow.md` for R, `references/design-theory.md` for color/typography/export rationale, `references/common-patterns.md` and `references/chart-types.md` for layout/chart recipes, `references/nature-2026-observations.md` for real Nature page archetypes, `references/qa-contract.md` before final delivery, `references/nature-article-requirements.md` for exact flagship Nature stage and upload rules, `../nature-shared/journal-formats/nature-machine-intelligence.md` for exact NMI figure rules, `references/ai-graphical-abstract-workflow.md` for AI-assisted graphical-abstract planning, policy gating, human verification, and provenance, and `references/tutorials.md` / `references/demos.md` for worked examples.

Do not infer flagship Nature or NMI requirements from a Nature Communications
corpus or from the visual-style examples in this skill.

## Why this split

- The static layer is versioned and reviewable. The backend gate is now explicit in the manifest rather than buried in prose.
- The dynamic layer loads the selected mode's resources. A backend quick-start enters context only when plotting requires it; deeper references load only when needed.
- The router itself is short on purpose. Update fragments and references, not this file, when adding scope.
- This structure mirrors `nature-writing`, `nature-polishing`, `nature-reader`, and `nature-paper2ppt`.
