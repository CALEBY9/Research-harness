# Production Proof Integrity Gate

This shared contract applies when an accepted manuscript has entered publisher production and the author is checking a PDF, HTML, or portal proof. It complements the equation-specific gate by auditing the complete proof surface: production deltas, equations, tables and metrics, citations, cross-artifact coherence, claims, disclosures, and page-level presentation.

## Core rule

A production proof is a new artifact, not a visually equivalent copy of the accepted manuscript. Freeze it, compare it with the exact accepted source, and revalidate every high-risk surface touched by production. Successful rendering, editable Word objects, matching source-copy hashes, or a small correction count do not establish proof integrity.

Default to `READ_ONLY_AUDIT`. Apply a proof correction only when the user has authorized edits and the correction class permits it. Never use proofing to hide a scientific fork, post-hoc metric selection, model recalibration, or result replacement.

## Generalization and locality boundary

Keep only cross-project failure patterns and acceptance rules in this shared gate. Appropriate reusable content includes artifact-version freezing, source-to-proof delta review, equation/definition parity, table-construct and rounding provenance, citation identity closure, cross-artifact coherence, correction classification, clean-final checks, and returned-proof verification.

Do not add any of the following to this shared gate or the Research workflow entry point:

- journal, manuscript, submission, reviewer, or production identifiers;
- local project paths, filenames, hashes, page locators, or portal query numbers;
- concrete equation, table, figure, section, or Appendix numbers from one paper;
- project-specific variables, parameter names or values, scenario labels, policy names, datasets, metrics, thresholds, or numerical results;
- one manuscript's preferred scientific correction, editor comment, wording replacement, or unresolved author decision;
- a project-specific workaround that has not been abstracted into a falsifiable cross-project rule.

Project details belong in the project `AGENTS.md` / `CLAUDE.md`, project state, audit report, correction ledger, change log, or response package. A project observation may motivate a shared rule only after it has been rewritten as a domain-neutral failure condition, required evidence, acceptance test, or stop rule. Use placeholders rather than copying the originating paper's symbols or values.

## Required frozen evidence

Record exact paths and SHA-256 values for every in-scope artifact that exists:

- production proof PDF, HTML export, or portal snapshot;
- accepted author manuscript and accepted supplement/Appendix;
- current editable correction source, if different from the accepted source;
- executable model, code, configuration, data, and run outputs supporting equations, tables, or figures;
- figure source data and plotting scripts;
- final reference metadata or reference-manager export;
- prior proof version and correction list when this is a re-proof.

Conflicting canonical paths, an unknown accepted source, or an artifact changed after audit is `PROOF_VERSION_BOUNDARY_BLOCK`.

## Proof correction classes

Use the same five classes across equations, tables, citations, figures, and prose:

| Class | Meaning | Default action |
|---|---|---|
| `PUBLISHER_ERROR` | Production changed, dropped, substituted, or damaged correct accepted content | Restore the accepted content and request re-proof |
| `OBVIOUS_AUTHOR_ERROR` | One authoritative source uniquely determines a local correction that preserves model behavior and reported results | Apply the smallest correction and disclose it |
| `CLARITY_CORRECTION` | A local definition, abbreviation, locator, unit label, or reader-facing explanation can be repaired without changing scientific meaning | Apply narrowly |
| `SCIENTIFIC_DECISION_REQUIRED` | Two or more plausible scientific definitions exist, or accepted source, model, supplement, and results disagree | Hold and request author decision plus editor approval |
| `MODEL_OR_RESULTS_CHANGE` | The correction changes equations, parameters, execution, analysis, figures, tables, or conclusions | Hold; rerun and resynchronize only with explicit editorial authorization |

Every correction row needs a proof locator, accepted-source locator, authoritative basis, class, proposed action, affected artifacts, disposition, and re-proof status. An unattributed production change is not automatically a publisher error.

## Audit workstreams

### 1. Production-delta inventory

Compare the exact accepted source with the exact production artifact. Inventory additions, deletions, substitutions, reordered content, equation/object conversions, reference-manager changes, table transformations, figure replacements, and publisher queries.

Each material delta must be one of:

```text
EXPECTED_PRODUCTION_CHANGE
PUBLISHER_ERROR
AUTHOR_CORRECTION_REQUEST
MANUAL_REQUIRED
UNEXPLAINED_DELTA
```

`UNEXPLAINED_DELTA` is blocking. A visual skim cannot substitute for a text/object inventory, and text extraction cannot substitute for rendered-page inspection.

### 2. Equations and notation

For any displayed equation or model notation, load `equation-semantic-integrity-gate.md` and use its machine-readable ledger. The proof audit must cover every physical display, including auxiliary formulas and sub-equations, and must verify:

- exact symbol identity and first-use local definitions;
- absence of equation-external symbols in the adjacent `where` block;
- unique numbering and resolved cross-references;
- canonical aliases, units, dimensions, guards, lags, initial conditions, and stock-flow semantics;
- parity with the frozen executable model/code/config when the equation describes implementation;
- accepted-source-to-proof operator integrity, including multiplication signs, minus signs, delimiters, subscripts, superscripts, and Greek symbols.

Extraction counts, MathType/OMML/OLE presence, and successful PDF rendering are structural evidence only.

### 3. Tables, metrics, and validation constructs

Use one ledger row per reported table value or summary metric when the table supports a scientific claim. Record:

```text
table / cell locator
indicator label and scientific construct
source variable or calculation
population / scenario / period / aggregation window
unit and scaling
error or summary-metric formula
unrounded source values
display precision and rounding rule
independence status: independent holdout / external benchmark / historical fit / internal diagnostic / post-hoc diagnostic
source artifact / script / run locator
recalculation verdict
```

Hard rules:

- Recompute errors and summary metrics from frozen unrounded values. If displayed values cannot reproduce the reported error, state that the error uses unrounded values or increase the displayed precision.
- Distinguish signed percentage error, absolute percentage error, MAE, MAPE, RMSE, and other metrics by formula, not by label similarity.
- A changed indicator name must preserve the same construct. If its numerator, denominator, cap, residual, aggregation, independence, or scientific meaning changes, classify it as a scientific correction even when model dynamics and headline results remain unchanged.
- Do not remove a failed metric, relabel a tuned/post-hoc diagnostic as holdout validation, or choose a lower-error proxy after seeing the results without explicit disclosure and editor approval.
- Internal accounting invariants, sensitivity tests, plausibility checks, historical fit, external benchmarks, and independent validation must remain separate evidence classes.

### 4. Citations and reference identity

Run bidirectional closure after the publisher has produced the final author-year suffixes or numerical ordering:

- every body citation resolves to exactly one reference entry;
- every retained reference entry is cited or explicitly justified;
- author names, title, year, suffix, journal, volume/article number, and DOI/URL identify the same work;
- suffix corrections are bound to full reference identity, never guessed from `a`/`b` alone;
- publisher `uncited reference` and `missing reference` queries are resolved;
- title/author parsing damage and duplicated policy/report titles are corrected without changing valid identifiers;
- high-risk claims still have claim-level support, not merely topic-relevant references.

Reference-manager reinsertion may repair a broken field, but the re-proof still requires identity and body-list closure. A search miss is not evidence that an entry is absent unless the complete proof text and reference section were both checked.

### 5. Cross-artifact and version coherence

Build a compact parity matrix across main text, supplement/Appendix, executable source, results, figures, tables, captions, and response/change records where relevant. Check:

- parameter values, variable names, units, and scenario definitions;
- equation, table, figure, Appendix, and section cross-references;
- time origin, time-step, aggregation window, endpoint, and axis labels;
- figure source-data version, plotting script, panel definition, and caption wording;
- validation indicator definition and reported values;
- abbreviations and reader-facing terminology;
- current versus superseded artifacts.

A main-text/Appendix/model conflict cannot be waived because one location contains a notation table or because net results happen to be similar. Any artifact changed after parity review invalidates the affected rows.

### 6. Claims, disclosures, and reader-facing language

Recheck claims whose strength depends on proof-stage corrections:

- validation, prediction, causality, mechanism, hypothesis support, policy effect, and measurement language;
- `holdout`, `benchmark`, `historical fit`, `diagnostic`, and `post-hoc` labels;
- data/code availability and reproducibility statements;
- generative-AI declaration, tool identity, use scope, and human oversight, which remain author-owned factual disclosures;
- model-estimated or scenario-simulated results that must not be described as observed or measured.

Use `clean-final-language-gate.md` and `scripts/clean_final_scanner.py` for process-language leakage. Internal canonical-state labels, local paths, run names, parser names, audit history, or revision narration may appear in author-side ledgers but not in reader-facing prose unless they are genuine scientific objects and are explicitly allowed with reason. Load project-specific labels from a project-local denylist rather than adding them to this shared gate.

### 7. Production and page-level QA

Inspect the rendered proof, not only extracted text. Check every changed page and then the complete article surface for:

- publisher placeholders, unresolved queries, copyright placeholders, duplicated headings, missing images, and replacement notices;
- figure/table/caption separation, panel labels, legends, colorbars, axis units, line styles, and final-size readability;
- table indentation, alignment, border style, pagination, header repetition, decimal alignment, and notes;
- equations clipped, wrapped, renumbered, or separated from definitions;
- scientific typography: subscripts, superscripts, minus signs, multiplication signs, Greek symbols, chemical formulae, `CO2`-style indices, and inverse units such as `month^-1`;
- broken spaces, apostrophes, hyphenation, cross-references, abbreviations at first use, and special characters.

OCR or text extraction can flag candidates but cannot clear visual layout. Page QA evidence must record the proof version and inspected page or portal locator.

## Required author-side outputs

For a substantial proof audit, produce or maintain the equivalent of:

```text
PROOF_VERSION_MANIFEST
PROOF_DELTA_LEDGER
PROOF_CORRECTION_LIST
EQUATION_LEDGER and equation-gate report when applicable
TABLE_METRIC_LEDGER
CITATION_REFERENCE_CLOSURE
CROSS_ARTIFACT_PARITY_MATRIX
FINAL_PAGE_QA_RECORD
```

These may be compact tables in one audit report; do not create empty files merely to satisfy names. Separate publisher/typesetting errors from author-origin scientific corrections so the editor can route them correctly.

## Acceptance and stop rules

A proof may be labelled `READY_TO_APPROVE` only when all applicable conditions hold:

1. the frozen proof and accepted-source versions are unambiguous;
2. unexplained production deltas are zero;
3. equation-gate `BLOCK` and unresolved `MANUAL_REQUIRED` rows are zero;
4. every claim-bearing table metric is reproducible from frozen unrounded sources with correct construct, unit, period, formula, and label;
5. body-citation-to-reference and reference-to-body closure is complete;
6. main text, Appendix, model/code, results, figures, captions, and cross-references have no unresolved material conflict;
7. process-language, placeholder, typography, special-character, and page-layout findings are resolved and verified in the returned proof;
8. no `SCIENTIFIC_DECISION_REQUIRED`, `MODEL_OR_RESULTS_CHANGE`, or editor-approval request remains unresolved.

Otherwise return `HOLD_PROOF`, identify blocking versus non-blocking items, and state the smallest permitted next action. Do not say `ready`, `complete`, or `fixed` before inspecting the returned re-proof.

## Failure codes

```text
PROOF_VERSION_BOUNDARY_BLOCK
UNEXPLAINED_PRODUCTION_DELTA
EQUATION_GATE_BLOCK
TABLE_CONSTRUCT_MISMATCH
TABLE_RECALCULATION_FAIL
ROUNDING_PROVENANCE_MISSING
VALIDATION_LABEL_OVERCLAIM
CITATION_IDENTITY_MISMATCH
CITATION_CLOSURE_FAIL
CROSS_ARTIFACT_DRIFT
FIGURE_TIME_OR_UNIT_MISMATCH
PROCESS_LANGUAGE_LEAK
PRODUCTION_PLACEHOLDER
TYPOGRAPHY_OR_SPECIAL_CHARACTER_FAIL
MANUAL_PAGE_QA_REQUIRED
SCIENTIFIC_DECISION_REQUIRED
MODEL_OR_RESULTS_CHANGE
REPROOF_NOT_VERIFIED
```

## Handoff

The default proof route is:

```text
paper_revision (scope, correction classification, ledgers)
-> paper_review (scientific and reader-risk verification)
-> nature-evidence-audit (numbers, constructs, implementation, provenance)
-> nature-paper-format (rendered production and typography QA)
-> editor/publisher re-proof
-> final read-only verification
```

Only insert `paper_polish` for narrowly authorized wording corrections after scientific meaning and notation are frozen. A substantive model, analysis, or figure change returns to the owning analysis/figure workflow and cannot be closed inside proof mode.
