---
name: nature-reader
description: Read one research paper as an evidence-grounded Paper Card or a full-text reader from PDF, DOI, arXiv, HTML or supplied text. Use for 单篇论文精读、文献卡片、读论文、全文翻译 or 中英文对照; choose the requested output and preserve source locators.
metadata:
  version: "2.1.1"
  author: Community contribution, refactored into static/dynamic layers
---

# Research Paper Reader — Router

## Choose the reading deliverable first

For single-paper deep reading, a Paper Card, experiment-to-claim analysis or
Chinese explanatory reading notes, use [paper-card mode](references/paper-card/guide.md).
Load its mode-local manifest, selected paper-type fragments and bundled source
preparation/audit tools. Reuse an existing source map; do not run full translation
merely to produce a card. Match the requested language and retain source locators.
Complete that mode and return; do not load the root full-reader manifest or
continue through the full-reader protocol below for a card-only request.

For explicitly requested full-text translation, bilingual reading or a complete
full-paper reader, use the full-reader route below. Its core and output contract
apply to that mode only. Preserve requested completeness and mark unavailable
material; a card does not replace full translation. Load both cores only when
the requested deliverable actually needs both outputs. Reuse one source
extraction/map, complete each requested output, then return without invoking
the reader again.

This skill is split into two layers:

- A **static layer** under `static/` that holds versioned, reusable content fragments (core principles, the reading workflow, the output contract, and per-source-format extraction guidance).
- A **dynamic layer** (this file plus `manifest.yaml`) that detects the request's source format and loads only the fragments needed for the current job.

Do not try to apply the reading logic from memory or from this router. Always load fragments from disk as described below.

## Full-reader protocol

These five steps apply only after selecting the full-reader deliverable.
The root manifest and its always_load list belong to this branch.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). It declares the `source_format` axis, the allowed values, and the file paths each value maps to.

Also read every file listed under `always_load`. These hold the core principles, the reading workflow, and the output contract that apply to the full-reader branch, plus the shared Terminology Ledger used to build the recurring-term table.

### 2. Detect the source format

Decide the `source_format` value using the manifest's `detect:` hint and the user's input:

- `pdf-text` — selectable-text PDF. Default.
- `scanned-pdf` — image-only or OCR-required PDF.
- `html` — publisher or preprint HTML page.
- `doi-arxiv` — a bare DOI or arXiv link that must be resolved first.
- `pasted-text` — pasted prose or notes with no retrievable original layout.

Keep the source-format selection internal unless a material ambiguity needs the user's input. A source may map to more than one value (for example a DOI that resolves to a PDF); load the resolution fragment first, then the fragment for the resolved artifact.

### 3. Load the matching fragment(s)

Read the file mapped for the detected `source_format`. Do **not** read every fragment in `static/`. Load only what step 2 selected.

### 4. Build the reader using the loaded material

Apply the loaded fragments in this priority order:

1. Core principles (`core/principles.md`) — bilingual reader by default, translate for meaning, never degrade to a summary, copyright caution.
2. Source-format fragment — how to extract text, figures, and tables for this input.
3. Reading workflow (`core/workflow.md`) — the six-step source-map-first process.
4. Output contract (`core/output-contract.md`) — required files and the pre-response verification checklist.

Build the Terminology Ledger as you translate (`../nature-shared/core/terminology-ledger.md`); it becomes the `paper.md` recurring-term table and the `source_map.json` glossary.

If constraints prevent full processing, still create a draft reader and label missing pages, figures, or low-confidence crops in `translation_notes.md`. Do not switch to summary mode.

### 5. Reach for references only when needed

The files under `references/` are deep references, not defaults. Open them on demand per the `references.on_demand` table in the manifest:

- detailed figure/table cropping and placement → `references/figure-extraction.md`.
- exact field schema for `paper.md` / `source_map.json` → `references/output-spec.md`.
- equations, mathematical expressions, chemical formulae, or image-only formulae → `references/equation-handling.md`.
- answering follow-up questions with source citations → `references/grounding-rules.md`.

## Why this split

- The static layer is versioned and reviewable. Adding a new source format is one new fragment plus one manifest line.
- The dynamic layer keeps each invocation cheap: only the fragment relevant to this input enters context.
- The router itself is short on purpose. Update fragments, not this file, when adding scope.
- This structure mirrors `nature-writing` and `nature-polishing` so shared content lives in `nature-shared/`.
