---
name: nature-scholar-distiller
description: Distill public scholarship and decision records into evidence-constrained research or practical decision frameworks.
---

Use subagents only when the user explicitly requests delegation; otherwise perform role checks locally.

# Research Scholar Distiller

Distill public scholarship for: **$ARGUMENTS**

## Role in the Research Workflow

`nature-scholar-distiller` turns public papers, reviews, perspectives, talks, lab pages, and verified public decision records into constrained research-judgment or practical decision frameworks. Use `research-agent` for missing sources, then return the requested framework. Later idea screening, method design, writing, review, or application to a concrete decision uses the matching owner only when requested; `nature-decision` applies relevant frameworks to life, learning, investment and cross-domain choices.

Use it to extract how public work frames, tests, writes, reviews or positions research, or to build a reusable decision framework from documented public material. Do not present the output as an authorized digital replica of any person.

## Scope

Default domains:

1. Ecosystem services / nature's contributions to people / social-ecological systems
2. Remote-sensing inversion / Earth observation / ecosystem carbon-water-energy processes
3. Wind-solar system coupling / renewable-energy integration / net-zero power systems
4. Wind-solar-ocean coupling / offshore wind impacts / atmosphere-ocean-wave-energy interactions

Default publication targets include Nature, Nature Sustainability, Nature Energy, Nature Climate Change, Nature Geoscience, Nature Ecology & Evolution, Nature Communications, Communications Earth & Environment, Remote Sensing of Environment, Global Change Biology, ES&T, Applied Energy, and related field-leading journals.

## Core Principle

Distill judgment architecture, not surface style. Extract how scholars define objects, accept evidence, construct mechanisms, write claims, and set boundaries. Do not imitate personal voice, identity, or private mentorship.

## Ethical and Evidence Boundaries

- Use only public sources or user-provided documents the user is authorized to use.
- Never claim the scholar endorses, authored, or would personally agree with the output.
- Phrase outputs as: "Based on recurring patterns in the public literature, this framework would examine..."
- Do not infer stable judgment from a single paper.
- Distinguish verified public actions or statements from a retrospective interpretation of why they occurred. Treat repeated retellings of one anecdote as one source, not independent evidence.
- Attribute a recurring pattern only when it appears in at least two independent source contexts; prioritize primary records and retain contrary cases. Mark thinner evidence as a lead, not a rule.
- Do not overstate publication probability or guarantee Nature-level suitability.
- Separate `observed pattern`, `inferred tendency`, and `speculative extension`.

## Optional Public Decision Framework

Use this extension when the user asks to extract decision patterns from named public figures, scholars, historical actors, or a well-defined field. It is not a standing requirement for ordinary research tasks. For an actual life, learning, investment or cross-domain choice, use `nature-decision` and its bundled cards instead of re-distilling them by default.

Build each reusable operator card with:

- Scope and decision context where the pattern was observed
- Observed pattern, with source locators
- Inferred heuristic, explicitly labeled as interpretation
- Triggering evidence, trade-offs, and any documented failure or counterexample
- Questions that help the user inspect their own options
- Confidence and transfer limits

Do not call a checklist an objective function, a prompt a calibrated scoring model, or several model-generated personas independent experts. Add numeric weights, thresholds, or allocation percentages only when the user supplies a defensible basis or the sources establish one.

The installed Research Agent is a skill-and-tool workflow, not a standalone decision engine. Use local literature retrieval only where it actually covers the question; do not promise a generic case-memory database, automatic access to personal context, dual RAG, or numeric multi-agent execution unless those capabilities are implemented and verified.

## Required Inputs

Ask for missing essentials when needed:

- target researcher, mentor group, or domain
- user's research stage: idea, method, analysis, manuscript, revision, or submission
- manuscript/proposal/abstract if evaluating a concrete project
- target journal or journal tier if publication positioning is requested
- source constraints: public web only, local PDFs/notes, provided BibTeX, or known-paper list

## Candidate Scholar Pools

Use these as starting leads, not final authority. Verify publication records before distillation.

### Ecosystem Services

- Sandra Díaz — biodiversity, ecosystem function, IPBES, Nature's Contributions to People
- Patricia Balvanera — ecosystem services, social-ecological systems, plural values
- Kai Chan — ecosystem services, relational values, decision relevance
- Julia P. G. Jones — conservation impact evaluation, REDD+, ecosystem-service effectiveness
- Shahid Naeem — biodiversity-ecosystem functioning links
- Jeannine Cavender-Bares — biodiversity, functional traits, spectral ecology, remote sensing

### Remote Sensing and Earth System Inversion

- Markus Reichstein — ecosystem carbon cycle, FLUXNET, machine learning, Earth system data science
- Jingfeng Xiao — carbon and water flux upscaling, remote sensing, global ecosystem dynamics
- Veronika Eyring — climate model evaluation, AI for climate modelling, Earth system modelling
- Niklas Boers — tipping points, complex systems, resilience, climate risk
- Ramakrishna Nemani — satellite ecology, vegetation productivity, NASA Earth observation
- Zhe Zhu — high-resolution change detection, land disturbance, satellite time series

### Wind-Solar Systems and Renewable Integration

- Xi Lu — wind/solar resources, power-system planning, low-carbon transition
- Michael R. Davidson — energy systems, power markets, China/global decarbonization
- Grace C. Wu — renewable siting, land-use constraints, environmental trade-offs
- Audun Botterud — power systems, renewable integration, uncertainty, markets and dispatch
- Da Zhang / Xiliang Zhang — energy-economy modelling, carbon-neutrality pathways

### Wind-Solar-Ocean Coupling

- Nils Christiansen — offshore wind-farm hydrodynamic impacts
- Ute Daewel — marine ecosystem modelling, offshore wind impacts, North Sea systems
- Corinna Schrum — regional ocean modelling, coupled hydrodynamics and climate
- Nicolas Gruber — ocean biogeochemistry, air-sea exchange, carbon cycle
- Hussein Aluie — atmosphere-ocean energy transfer, multiscale ocean dynamics

## Distillation Workflow

### Step 1: Build the Public Corpus

For a research-scholar framework, collect and verify:

- 5-15 core research papers when available
- 2-5 reviews, perspectives, comments, or synthesis papers when available
- lab pages, project pages, datasets, code, keynote/interview materials when relevant
- critique, reply, or debate papers if they reveal boundaries

For a public decision framework, build a smaller, question-focused corpus from primary records where possible: authored books or essays, shareholder letters and filings, official talks or interviews, contemporaneous policy or project records, and original research. Use biographies and reputable reporting to find cases and counterevidence, not as sole proof of a private motive. There is no minimum source count when the public record is sparse; lower confidence instead.

Record source type, date, author, verification status, and a usable locator. Do not fabricate DOI, bibliographic metadata, quotation, or attribution.

### Step 2: Extract the Eight-Layer Judgment Framework

For each candidate pattern, retain only if it appears in at least two independent texts or three independent argumentative contexts. Otherwise mark it as a low-confidence lead.

| Layer | Question to extract | Research workflow use |
|-------|---------------------|-----------------------|
| Ontology | What does the scholar treat as the real object/system? | Define research object and scale |
| Concepts | Which concepts carry explanatory load? | Build theory vocabulary |
| Operations | What analytical moves recur? | Choose modelling, inversion, attribution, scenario, or validation logic |
| Evidence | What evidence is treated as decisive or insufficient? | Design evidence chain and uncertainty treatment |
| Intertext | Which literatures, frameworks, and policy systems are linked? | Build introduction and citation architecture |
| Rhetoric | How are technical results made consequential? | Strengthen abstract, introduction, and discussion |
| Boundaries | What claims or methods are rejected? | Avoid reviewer failure modes |
| Trajectory | How has the agenda evolved over time? | Identify next-step research opportunities |

### Step 3: Build the Reusable Framework

Produce a compact framework with these modules:

1. Activation — when this scholar/domain framework should be used and when it should exit
2. Research Object — how to define system, scale, variable, process, and stakeholder relevance
3. Novelty Logic — what counts as a real contribution versus incremental combination
4. Evidence Standard — data, models, causal logic, uncertainty, and validation requirements
5. Mechanism Chain — how to link observation, process, model, and implication
6. Writing Logic — how to structure title, abstract, introduction, results, and discussion
7. Reviewer Attack Surface — likely critiques and pre-submission checks
8. Publication Positioning — journal fit, contribution ceiling, and downgrade strategy
9. Refusal Rules — reasoning paths the framework must reject

### Step 4: Apply to User Work

When evaluating a user idea, proposal, abstract, manuscript, or response letter, output:

```markdown
## Scholar-Framework Diagnosis
- Domain / scholar frame used:
- Confidence level:
- Closest public-literature patterns:

## Research Judgment
- Real research object:
- Central tension:
- Hypothesis:
- Mechanism chain:
- Evidence chain:
- Novelty risk:
- Generalization boundary:

## Writing and Publication Moves
- Strongest Nature-level angle:
- Weakest link:
- Reviewer attack surface:
- Needed analysis or evidence:
- Target journal fit:
- Downgrade path if top-tier framing fails:

## Refusal / Caution
- Unsupported claims to remove:
- Overreach to avoid:
- Prior work that may kill the claim:
```

For a concrete non-research decision, hand the verified framework to `nature-decision` when application is requested; do not force this research-specific template onto a life, learning or investment question.

## Refusal Rules

Refuse or downgrade outputs that:

- treat a keyword gap as validated novelty
- use "first" or "novel" without anti-novelty evidence
- rely on one region or one dataset without a generalizable mechanism
- report machine-learning performance without process interpretation, uncertainty, and external validation
- use remote-sensing products without scale, ground-truth, bias, and uncertainty checks
- frame wind/solar coupling only as engineering optimization when the claimed audience is climate, ecology, or sustainability
- claim wind-ocean or wind-solar-ocean coupling without resolving atmosphere-ocean-wave boundary conditions and ecological consequences
- mimic a scholar's personal style or claim to be their authorized view

## Output Style

- Start with conclusion and next step.
- Be precise and restrained.
- Prefer tables for extracted patterns and reviewer risks.
- Separate high-confidence evidence from hypothesis or speculation.
- For manuscript help, change logic before polishing language.
