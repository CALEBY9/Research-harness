# nature-figure: figure-corpus mode

Use this mode only for its requested deliverable. Its owning skill is `nature-figure`.
Resolve mode-local manifest, scripts, static fragments and references from
`MODE_DIR`, the directory containing this guide. Select only the needed
mode; this resource is not a separate skill or a mandatory next stage.

# NCS Figure Corpus Builder

## Purpose

Use this mode for requested reference inventory, extraction, staged intake or promotion. If the existing corpus is sufficient, continue with the requested figure work without an intake pass.

The corpus is a design-learning layer, not an asset library. Its job is to convert reference figures into reusable, copyright-safe design knowledge:

- figure archetypes;
- panel choreography;
- visual hierarchy;
- caption logic;
- style tokens;
- transferable layout rules;
- do-not-copy boundaries.

It must not copy, trace, redraw, or reuse published figure artwork.

## Inputs

Accept one or more of:

- a local folder of screenshots or figure images;
- paper PDFs or figure screenshots supplied by the user;
- paper URLs, DOI lists, or curated GitHub/website galleries;
- target venue family: Nature, Cell, Science, Nature Communications, Nature Sustainability, One Earth, PNAS, or a field-leading journal;
- an existing project figure set needing style benchmarking.

If the image source, article title, venue, year, or figure ID is unknown, mark it `UNVERIFIED` or `PROVISIONAL`; do not invent metadata.

## Shared NCS Corpus Intake Contract

Canonical shared root and active manifest:

```text
D:\03_claude research\01_LLM-knowledge_base\NCS figureCorpus\
└── 02_index\REFERENCE_FIGURE_MANIFEST.csv
```

Shared intake is optional and append-only. Use it only when the user explicitly authorizes persistent addition to the shared corpus. A request to inspect, compare, or temporarily learn from a PDF/screenshot/reference image is not write authorization; keep that material in a project/session-local provisional inventory instead.

Before any shared write:

1. Read the nearest `AGENTS.md`, `.agent/NEXT.md`, `.agent/STATE.md`, the corpus `README.md`, `02_index/CLASSIFICATION_RULES.md`, and the most recent relevant QC/report artifact.
2. Snapshot the active manifest path, schema, row count, SHA-256, registered path set, filesystem image set, duplicate paths/names, and protected-template paths. If the documented active-set invariant is already violated, return `SHARED_CORPUS_DRIFT` and do not promote new material.
3. Create a versioned staging run; never overwrite, delete, rename, or silently reclassify existing active assets or rows.

Recommended staging layout:

```text
NCS figureCorpus/qc/reference_intake/run_<timestamp>/
├── raw_inputs/                 # only when the user's rights/local-use boundary permits a copy
├── candidate_figures/          # extracted or normalized candidates; not active corpus assets
├── INTAKE_MANIFEST.csv         # provenance, extraction, classification, rights, and review state
├── DUPLICATE_CHECK.csv         # SHA-256 and collision decisions
├── PROMOTION_DECISIONS.csv     # APPROVE / REJECT / HOLD with reviewer and reason
└── INTAKE_QA.md
```

PDFs are source containers: extract candidate figures into staging and review them individually; never auto-promote every page image. Screenshots and reference images also enter as candidates. If copying the raw source is not permitted, retain a verified source locator and only the allowed derivative/metadata. Record, when available, source path/URL, source PDF path, paper title, DOI, venue/year, figure/page identifier, caption, extraction method/quality, figure role/type, metadata status, license/local-use boundary, and do-not-copy notes. Unknown values remain `PROVISIONAL` or `UNVERIFIED`.

Run exact SHA-256 deduplication against both active registered assets and the current staging run, plus filename/destination collision checks. Treat perceptual or near-duplicate matches as a review queue, not an automatic deletion or merge. A duplicate may be linked in the intake ledger but is not appended again.

Promotion requires explicit decisions and a transactional apply:

1. Require `APPROVE` for design value, dominant visible `figure_type`, provenance, extraction quality, and rights/local-use boundary; unresolved candidates remain staged.
2. Copy each approved candidate to a collision-safe path under `01_Figures/<figure_type>/` and append only its new row to the active manifest. Do not silently change the active manifest schema; return `SCHEMA_MIGRATION_REQUIRED` with a versioned proposal if new columns are necessary.
3. Re-run invariants: manifest row count equals the registered active image set, every manifest path exists, manifest paths and filenames are unique, each parent folder matches `figure_type`, counts/run metadata agree where maintained, and all protected-template paths and hashes are unchanged.
4. On any failed invariant, do not claim promotion complete; roll back the current run's additions from the pre-write snapshot and preserve the staging/QC evidence.

Stop codes include `SHARED_CORPUS_WRITE_AUTH_REQUIRED`, `SHARED_CORPUS_DRIFT`, `SOURCE_PROVENANCE_REQUIRED`, `RIGHTS_BOUNDARY_REQUIRED`, `DUPLICATE_REFERENCE`, `PROMOTION_REVIEW_REQUIRED`, and `SCHEMA_MIGRATION_REQUIRED`.

## Workflow

Select only the steps needed for the requested inventory, design extraction or
intake. Inventory-only work ends after inventory/metadata and returns; it does
not require design-token libraries, benchmarking or shared promotion.

1. Build an inventory. Use `MODE_DIR/scripts/build_manifest.py` by its resolved path when a local image folder is available.
2. Record source metadata: source path/URL, paper title, DOI/URL, venue, year, article type, figure ID, license/permission status, and verification state.
3. Classify each figure by role and archetype: graphical abstract, mechanism map, pipeline/workflow, killer relationship, spatial-temporal decomposition, uncertainty audit, robustness/generalization, threshold/regime shift, causal contrast, Pareto frontier, model architecture, or multi-panel hero figure.
4. Extract design tokens without copying content: canvas ratio, panel grid, information flow, typography scale, line-weight hierarchy, color semantics, legend strategy, annotation density, whitespace discipline, and caption function.
5. Write a `DO_NOT_COPY.md` boundary for every source family: exact layout, icons, labels, data shapes, color combinations, visual metaphors, and caption phrasing that must not be reused.
6. Promote only generalized patterns into `STYLE_TOKEN_LIBRARY.yml` and `FIGURE_ARCHETYPE_LIBRARY.md`.
7. Use selected benchmark cards in the figure-benchmark mode when transfer rules are requested, then continue the current figure task.

## Copyright And Integrity Rules

- Reference figures are evidence for design analysis only.
- Do not reuse published artwork, icons, images, panel layouts, data patterns, or captions.
- Do not train a generative model on copyrighted images unless the user has confirmed rights and the workflow records that permission.
- Do not infer data values or scientific findings from a reference figure for the user's manuscript.
- If a reference image is from a paywalled or copyrighted article, store only metadata and analysis notes unless the user confirms the local-use boundary.
- When in doubt, keep the raw image outside project submission artifacts and preserve only the design card.

## Output Contract

Default to proposing artifacts in the response. Write files only when the user authorizes project artifact writes.

Recommended project-local corpus layout:

```text
paper/figures/ncs_corpus/
├── raw_refs/                         # user-managed reference images; not submission assets
├── REFERENCE_FIGURE_MANIFEST.csv
├── FIGURE_ARCHETYPE_LIBRARY.md
├── DESIGN_TOKEN_CARDS.md
├── STYLE_TOKEN_LIBRARY.yml
├── TRANSFER_RULES.md
├── DO_NOT_COPY.md
└── CORPUS_QA.md
```

Minimum manifest fields:

```csv
reference_id,local_path,source_url,paper_title,doi,venue,year,article_type,figure_id,figure_role,archetype,license_status,metadata_status,notes
```

Minimum design card:

```markdown
# Design Token Card: [reference_id]

## Source Metadata
- Local path / URL:
- Paper / venue / year:
- Figure ID:
- Metadata status: VERIFIED / PROVISIONAL / UNVERIFIED
- License / permission status:

## Figure Role
- Paper role:
- Scientific question:
- Main visual tension:
- Killer panel / sequence:

## Transferable Design Logic
| Layer | Observed logic | Transferable rule | Do not copy |
|-------|----------------|-------------------|-------------|
| Layout |  |  |  |
| Panel choreography |  |  |  |
| Visual hierarchy |  |  |  |
| Color semantics |  |  |  |
| Caption logic |  |  |  |
```

## Script

Use the bundled manifest helper for local folders:

```powershell
python "MODE_DIR/scripts/build_manifest.py" `
  --input "paper/figures/ncs_corpus/raw_refs" `
  --output "paper/figures/ncs_corpus/REFERENCE_FIGURE_MANIFEST.csv"
```

The script only creates a project/local inventory skeleton. It does not analyze image content, verify metadata, deduplicate assets, or promote rows into the shared active manifest; never point it at the shared active manifest as a replacement operation.

## Delivery and reuse

- Return the requested inventory/intake assets and their actual verification status. The listed manifest, design cards, style tokens and do-not-copy notes apply only to the selected intake scope.
- Reuse generalized style tokens only after copyright and do-not-copy boundaries are explicit.
- If applying those rules to a figure is also requested, continue in the current owner's plotting branch with the existing workflow and its rendering and visual checks; do not reinvoke the owner or use a raw reference image as the final figure base. Otherwise finish the inventory/intake result and return.
