---
name: nature-research-discovery
description: Map an environmental-science field or discover source-grounded, testable candidate hypotheses. Use nature-scientific-insight for a standalone novelty verdict, scientific contribution comparison or research go/no-go decision.
---

Use subagents only when the user explicitly requests delegation; otherwise perform role checks locally.

Generate environment-science research ideas from: **$ARGUMENTS**

## Role in the Research Workflow

`nature-research-discovery` is the Discovery-stage orchestrator. It should produce a small set of defensible, data-grounded candidate ideas, not a finished method or paper.

Match the requested deliverable: a field map or candidate hypotheses, with the
closest-prior evidence needed to ground them. A standalone novelty assessment
uses `nature-scientific-insight`. A map-only request does not require generating or
ranking ideas; an author-selected question can go directly to `nature-method-design` or
`nature-experiment-plan` through the router.

`nature-scientific-insight` owns scientific recommendation criteria. For candidate
screening or ranking, read its
[judgment criteria](../nature-scientific-insight/references/judgment-criteria.md) and
reuse a sufficient prior assessment. A standalone novelty or research-continuation
verdict belongs there; this owner supplies the landscape, original-source
comparisons and new candidate hypotheses. These are responsibilities within the
requested task, not a required sequence of owner calls.

Ground the requested field map or candidate list in supplied evidence and targeted literature checks. Rank candidates when a shortlist is requested; do not automatically launch method design, experiment planning, or writing. For a supplied idea's value or novelty verdict, use `nature-scientific-insight` rather than starting a new candidate-generation cycle. Existing assessments are useful inputs, not required workflow dependencies.

SciDER-inspired principle: idea generation must be grounded in **killer prior work + residual delta + data characteristics + executable validation**, not only in abstract novelty language. The default stance is falsification-first: try to prove the idea is already done before generating candidates.

## Core Outputs

- One report or project equivalent — the requested field map, prior-work assessment, or ranked idea report; `IDEA_REPORT.md` is a suggested name for the latter
- Optional `idea.json` — machine-readable idea summary when requested or useful for an authorized handoff
- Optional `IDEA_CANDIDATES.md` — compact shortlist when the user requests a lightweight handoff

Reuse available literature coverage, closest prior-work comparisons, residual deltas, hypothesis notes, and data audits in any sufficient format. Missing legacy gate files do not block screening. Missing scientific evidence limits the recommendation and must be reported; do not invent it.

## Stage Gates

### G0 — Scientific Question Gate
Extract from the request and available context; ask only for unresolved, consequential choices:
- phenomenon/process of interest
- environmental system and spatial/temporal scale
- target variable or mechanism
- why the problem matters scientifically
- what kind of evidence could answer it

### G1 — Literature and Gap Gate
Use `nature-academic-search` for missing literature evidence and `nature-literature-kb` for a relevant verified local corpus. Choose sources by the question and actual tool availability; a tool name in a reference is not proof that it is mounted.
Extract:
- core-domain consensus
- unresolved scientific gaps
- source coverage, query families, de-duplication/ranking baseline, and missing or manual sources
- mature models or methods in the field
- top-journal papers worth reproducing or extending
- adjacent domains with transferable theories, data products, or methods
- closest prior work and what remains unverified

When a field map is requested or needed to clarify a broad direction, connect research objects, processes, scales, measures, and disciplinary perspectives to identifiable sources. Distinguish established relationships from proposed connections. An empty map cell or an unfamiliar combination is a search lead, not evidence of a scientific gap.

### G1.5 — Closest prior work and falsifiability

Build the source-located comparison across object, method, data and claim using
the core judgment criteria. Record relevant query families and coverage limits;
apply the closest-prior, residual-delta and method-contribution reasoning from
that reference rather than defining a separate novelty rule set here.

### G1.6 — Scientific hypothesis and evidence test

Develop a hypothesis and distinguishing observation under the core judgment
criteria for competing explanations, claim boundaries and feasibility. For
descriptive/resource candidates, explain the added knowledge without inventing
a causal mechanism. Unresolved interpretation of completed outputs belongs to
`nature-data-analysis`; a scientific choice across those interpretations belongs to
`nature-scientific-insight`.

### G2 — Data Grounding Gate
Before ranking ideas, identify the data reality behind each candidate:
- available observations, remote-sensing products, reanalysis, model outputs, field data, or derived datasets
- spatial/temporal coverage and resolution
- variables, units, semantics, and expected mechanism relevance
- obvious quality risks: missingness, bias, scale mismatch, uncertainty, licensing, reproducibility limits
- whether the idea can be minimally tested without inventing data

If no plausible data path exists, downgrade or reject the idea even if it sounds novel.

### G3 — Top-Paper Reproduction Gate
When the user provides a top-journal paper or asks for idea generation from existing work, identify:
- what can be reproduced directly
- what depends on unavailable data, code, software, or domain assumptions
- which limitation, dataset, region, mechanism, or method gap can become a new idea
- what data or experimental setup would make the extension falsifiable

### G4 — Candidate Idea Gate
Return a shortlist proportionate to the evidence and requested scope. Each recommended idea must include:
- scientific question
- hypothesis when an explanation is being tested, or the descriptive/resource question otherwise
- core novelty type: `problem`, `method`, `data`, or `finding`
- environmental domain and scale
- data grounding and data feasibility
- required data and mature baseline models
- possible cross-domain inspiration and transfer boundary
- experiment outline or minimal validation
- closest prior work hypothesis
- residual delta after closest prior work
- anti-novelty verdict: `SURVIVE`, `REFRAME`, or `DROP`
- editorial hypothesis verdict: `PROCEED`, `REFRAME`, `RETURN_TO_DATA_AUDIT`, or `ABANDON`
- central tension and killer figure
- qualitative overlap assessment and threat level; quantify only with a defined scoring basis
- novelty risk and feasibility risk
- what would falsify the novelty or scientific claim

### G5 — PI-style Critic Gate
Before recommending ideas, apply a PI-style critique:
use the core judgment criteria to identify the strongest objection, remaining
supported contribution, and evidence that would change the recommendation.
Keep the source comparisons and candidate-specific reasoning in the same report.

### G6 — Selection Gate
Rank candidates by:
- scientific importance
- novelty defensibility
- data availability and quality
- methodological feasibility
- paper story potential
- risk of being only "apply method X to domain Y"
- ability to survive the PI-style critic gate

Recommend the strongest supported candidates; the author chooses the research direction. Continue to another stage only when authorized.

## Output

Use one compact report with the direction, search/source trace and coverage gaps, and the requested map, prior-work assessment, or candidates with ranked recommendations. Apply the candidate fields above when recommending ideas. Include reproduction opportunities only when relevant. Keep missing evidence next to the affected recommendation; use `AUTHOR_INPUT_NEEDED` only for a scientific choice or input that cannot be recovered from available sources.

Do not repeat the same candidate fields across multiple mandatory tables. Produce `idea.json` when a machine-readable handoff is useful or requested; it does not authorize a downstream workflow.

For detailed execution, read [idea-discovery-workflow.md](references/idea-discovery-workflow.md). Use [idea-discovery-templates.md](references/idea-discovery-templates.md) only when a report structure is useful; reuse sufficient project records instead of duplicating them.

## `idea.json` Schema

```json
{
  "idea_id": "idea_001",
  "title": "",
  "scientific_question": "",
  "hypothesis": "",
  "novelty_type": "problem|method|data|finding",
  "environmental_domain": "",
  "scale": {"spatial": "", "temporal": ""},
  "data_grounding": "",
  "data_requirements": [],
  "baseline_models": [],
  "killer_prior_work": [],
  "overlap_score": null,
  "residual_delta": "",
  "anti_novelty_verdict": "SURVIVE|REFRAME|DROP",
  "editorial_hypothesis_verdict": "PROCEED|REFRAME|RETURN_TO_DATA_AUDIT|ABANDON",
  "central_tension": "",
  "killer_figure": "",
  "journal_ceiling": "",
  "closest_prior_work_to_check": [],
  "cross_domain_inspiration": [],
  "transfer_boundary": "",
  "minimal_validation": "",
  "falsifier": "",
  "reviewer_attack": "",
  "next_skill": null
}
```

## Key Rules

- Do not skip literature grounding.
- Use the core judgment criteria to screen a broad or top-journal-oriented recommendation; a requested field map does not require an editorial verdict.
- Do not describe an idea as novel without documented search coverage, closest prior work, a falsifier, an overlap assessment, and a residual delta.
- Kill or reframe high-overlap ideas instead of rescuing them with new wording.
- Do not expand topic labels; establish the added knowledge and a feasible decisive comparison appropriate to the contribution type before recommending an idea.
- Do not generate ideas that cannot be tested with plausible data.
- Do not treat cross-domain borrowing as novelty unless the transfer boundary is explicit.
- Do not let a method idea replace the environmental science question.
- Prefer one sharp scientific question over a bundle of loosely connected improvements.
- Every recommended idea must include data grounding, a minimal validation route, and a closest-prior-work hypothesis.
- If evidence is insufficient, report the specific gap and complete the supported screening; do not invent a research story.
