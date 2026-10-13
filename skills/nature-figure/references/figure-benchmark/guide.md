# nature-figure: figure-benchmark mode

Use this mode only for its requested deliverable. Its owning skill is `nature-figure`.
Resolve mode-local manifest, scripts, static fragments and references from
`MODE_DIR`, the directory containing this guide. Select only the needed
mode; this resource is not a separate skill or a mandatory next stage.

## Codex CLI Adaptation

This skill is part of the Codex-side Research workflow.

- Use Codex file, shell, web, image, and editing capabilities available in the current session.
- If benchmark papers, images, PDFs, or screenshots are supplied locally, inspect only what is needed for the current figure task.
- If the user asks for latest or exact target-journal benchmarks, verify metadata with `nature-academic-search` or web lookup before treating them as current.
- Respect `C:\Users\Administrator\AGENTS.md` and any project-local `AGENTS.md`.

# Figure Benchmark Library

## Purpose

Use this skill when the user wants to learn from Nature, Science, Nature Communications, Nature Sustainability, One Earth, PNAS, or comparable top-journal figures, especially when they provide reference images.

The goal is not to copy a published figure. The goal is to extract figure logic:

- what scientific claim the figure carries;
- how panels create an argument;
- what the reader sees in five seconds;
- how uncertainty, comparator, scale, and evidence density are encoded;
- which visual principles can be transferred to the user's own data.

Use the `Top-Journal Figure Learning Loop` when the user gradually supplies high-quality figures, target-journal screenshots, paper PDFs, or links and wants future data-to-publication figures to improve over time. The loop promotes only reusable design knowledge into benchmark cards, style tokens, and transfer rules; raw reference images remain analysis inputs, not submission assets.

## Inputs

Accept one or more of:

- target journal or venue family;
- shared corpus manifest: `D:\03_claude research\01_LLM-knowledge_base\NCS figureCorpus\02_index\REFERENCE_FIGURE_MANIFEST.csv`;
- `paper/figures/ncs_corpus/REFERENCE_FIGURE_MANIFEST.csv`;
- `paper/figures/ncs_corpus/DESIGN_TOKEN_CARDS.md`;
- `paper/figures/ncs_corpus/STYLE_TOKEN_LIBRARY.yml`;
- `paper/figures/ncs_corpus/DO_NOT_COPY.md`;
- user-provided Nature-level figure screenshots, PDFs, paper links, or local images;
- `paper/figures/FIGURE_ARGUMENT_MAP.md`;
- `paper/figures/KILLER_FIGURE_BRIEF.md`;
- `paper/figures/FIGURE_CHOREOGRAPHY.md`;
- `paper/figures/VISUAL_ENCODING_SPEC.md`;
- an existing figure draft that needs benchmarking.

If the source, article identity, or figure role is unknown, mark the benchmark as `PROVISIONAL` instead of inventing metadata.

## Shared Corpus Boundary And Selection Contract

The shared NCS corpus is an optional candidate-locator pool, not an approved benchmark set, scientific evidence source, image-generation training set, or reusable asset library. Default integration is manifest-backed filtered retrieval plus source verification and benchmark-card generation; it requires no model training. Do not add embeddings, a multimodal reranker, or fine-tuning as a default dependency unless a curated subset and frozen retrieval evaluation demonstrate a concrete gain. Before using it:

1. Confirm the shared root and manifest exist; read the root `README.md`, `02_index/CLASSIFICATION_RULES.md`, and the most recent relevant report/QC artifact under `02_index/` or `qc/`.
2. Select candidates by the user's claim, data structure, figure role, comparator, uncertainty task, target venue, and production route. Do not retrieve on visual similarity or journal label alone.
3. Check that each selected `local_path` exists and inspect `metadata_status`, `classification_status`, `extraction_quality`, `license_status`, provenance fields, and do-not-copy notes. A manifest hit remains `PROVISIONAL` until the paper/figure identity and design-relevant interpretation are verified against the source layer.
4. Exclude unresolved, low-quality, missing-path, rights-incompatible, or structurally mismatched candidates from transferable rules. Record why each retained or rejected candidate was chosen.
5. Write only project-local benchmark cards, style tokens, and transfer rules. Link to the shared `reference_id`/manifest row; do not duplicate shared raw images.

## Figure Corpus Retrieval And Consumption Gate

Activate this gate only when the current figure task uses a shared/project corpus or supplied references. Freeze the retrieval intent before opening candidates:

- figure ID and Claim ID / claim role;
- data structure, manifest `data_type` / `data_analysis_type` when available,
  and intended figure role/archetype;
- comparator and uncertainty task;
- target venue family and target width;
- production route, query terms, and excluded visual patterns.

Then:

1. For a CSV manifest, run `MODE_DIR/scripts/select_figure_benchmarks.py` by its resolved path. Use repeatable/comma-separated `--data-type` and `--data-analysis-type` for exact controlled-vocabulary filtering, then use `--term` only for soft claim, comparator, uncertainty, or caption matching. Example: `python "MODE_DIR/scripts/select_figure_benchmarks.py" --manifest "<manifest.csv>" --figure-type conceptual_mechanism_diagram --data-type environmental_science_conceptual_reference --data-analysis-type "conceptual synthesis and mechanism communication" --venue-family ncs --term feedback --term boundary --limit 12 --output-json "<figure-dir>/benchmark/FIGURE_CORPUS_QUERY.json" --output-csv "<figure-dir>/benchmark/FIGURE_CORPUS_CANDIDATES.csv"`. If Python is unavailable, reproduce the same manifest filters and output fields manually and document the limitation; do not skip the retrieval record.
2. Treat selector output as `CANDIDATES_ONLY_NOT_APPROVED`. Inspect the actual image for every retained candidate and verify its paper/figure identity, source locator, local path, rights boundary, figure role, and design-relevant interpretation.
3. Compare candidates to the current claim, data structure, comparator/uncertainty need, reader path, target width, and production route. Journal family or surface resemblance alone is not a match.
4. Record selected and rejected candidates with reasons. A selected reference must yield at least one explicit `TRANSFER` or `ADAPT` rule and at least one relevant `REJECT` or `DO_NOT_COPY` boundary; otherwise it was viewed but not consumed.
5. Write `paper/figures/<figure_id>/benchmark/BENCHMARK_CONSUMPTION.md`. Link to candidate artifacts and shared `reference_id` values; do not copy raw corpus images into the project.

Fail closed:

- corpus/reference branch is active but the frozen query or candidate artifact is absent -> `CORPUS_SELECTION_REQUIRED`;
- a selected candidate lacks source/local-path/metadata/design-interpretation verification -> `BENCHMARK_SOURCE_UNVERIFIED`;
- no retained candidate structurally matches the current claim and data -> `BENCHMARK_MATCH_WEAK`; request better references or record an explicit user waiver instead of claiming corpus benefit;
- selected references have no rule-level implementation/exclusion mapping -> `BENCHMARK_CONSUMPTION_REQUIRED`.

When requested intake involves new PDFs, screenshots or reference images, use the figure-corpus mode. Persistent shared-corpus intake requires explicit user authorization; otherwise use a provisional project/session-local inventory.

## Workflow

1. Build a reference inventory. Record source, paper, venue, year, figure ID, local path or URL, article type, and whether metadata was verified.
2. If an NCS corpus exists, apply the Shared Corpus Boundary And Selection Contract before selecting benchmark figures; existing design cards and style tokens are hypotheses to re-check against the current claim and data structure.
3. Classify figure archetypes: mechanism map, killer relationship, spatial-temporal decomposition, uncertainty audit, robustness/generalization, threshold/regime shift, causal contrast, Pareto frontier, method schematic, or multi-panel hero figure.
4. Extract figure argument logic: panel order, claim density, killer panel, comparator, uncertainty, boundary condition, and caption function.
5. Extract production logic: target width, panel grid, typography, line weight, legend strategy, color semantics, whitespace, annotation density, and export format cues.
6. Run the Top-Journal Figure Learning Loop: map each transferable pattern to the user's data type, claim role, and production route; reject patterns that would require copying the benchmark's exact composition, artwork, data geometry, labels, or caption phrasing.
7. Write transfer rules. Separate `Transfer`, `Adapt`, `Reject`, and `Do not copy`.
8. Return the benchmark cards and transfer rules. If figure production is also requested, reuse them in the current owner's plotting branch without another owner invocation; otherwise stop here.

## Copyright And Integrity Rules

- Do not reproduce, redraw, trace, or closely imitate a published figure.
- Do not copy exact panel composition, icons, labels, colors, data patterns, or caption wording.
- User-provided screenshots and published figures are analysis inputs, not reusable figure assets.
- Benchmark figures cannot supply data, results, claims, labels, or statistics for the user's manuscript.
- If the benchmark conflicts with the user's evidence, the user's evidence and claim boundary win.

## Output Contract

Default to proposing artifacts in the response. Write files only when the user authorizes project artifact writes.

Recommended artifacts:

```text
paper/figures/benchmark/REFERENCE_FIGURE_MANIFEST.csv
paper/figures/benchmark/FIGURE_ARCHETYPE_LIBRARY.md
paper/figures/benchmark/BENCHMARK_DESIGN_CARDS.md
paper/figures/benchmark/TOP_JOURNAL_FIGURE_LEARNING.md
paper/figures/benchmark/TRANSFER_RULES.md
paper/figures/benchmark/STYLE_TOKENS.yml
paper/figures/benchmark/DO_NOT_COPY.md
paper/figures/<figure_id>/benchmark/FIGURE_CORPUS_QUERY.json
paper/figures/<figure_id>/benchmark/FIGURE_CORPUS_CANDIDATES.csv
paper/figures/<figure_id>/benchmark/BENCHMARK_CONSUMPTION.md
```

When `nature-figure` has already produced `paper/figures/ncs_corpus/`, or the shared corpus is used, do not duplicate raw reference images. Link to the relevant corpus manifest and write only benchmark-specific cards and transfer rules.

Minimum benchmark card:

```markdown
# Figure Benchmark Card

## Source
- Paper:
- Venue / year:
- Figure:
- Metadata status: VERIFIED / PROVISIONAL

## Figure Logic
- Figure role:
- Scientific tension:
- Killer panel / sequence:
- Panel choreography:
- Comparator / baseline:
- Uncertainty / scale / sample-size handling:
- Caption function:

## Transfer Rules
| Element | Transfer / Adapt / Reject / Do not copy | Reason |
|---------|------------------------------------------|--------|

## Data Match
| User data type / claim | Applicable benchmark pattern | Required adaptation | Risk if copied literally |
|------------------------|------------------------------|---------------------|--------------------------|

## Style Tokens
| Token | Observed pattern | Usable rule for our data |
|-------|------------------|--------------------------|
```

Minimum benchmark-consumption record:

```markdown
# Benchmark Consumption: [Figure ID]
- Status: VERIFIED_CONSUMED / MATCH_WEAK / USER_WAIVED
- Query artifact:
- Candidate artifact:
- Claim / data / comparator / uncertainty / target-width contract:

| Reference ID | Source and local-path verification | Structural match | Decision | Reason |
|--------------|------------------------------------|------------------|----------|--------|

| Rule ID | Source reference IDs | TRANSFER / ADAPT / REJECT / DO_NOT_COPY | Implementation or exclusion in our figure | Verification target |
|---------|----------------------|------------------------------------------|-------------------------------------------|---------------------|
```

## Delivery and reuse

- Return benchmark cards and transfer rules as the requested deliverable.
- When the corpus/reference branch is active, include the selector artifacts, `BENCHMARK_CONSUMPTION.md`, `STYLE_TOKENS.yml`, and figure-specific transfer rules in the existing figure specification.
- If a requested benchmark is missing, return `BENCHMARK_REQUIRED` instead of proceeding to production.
