---
name: nature-literature-kb
description: Retrieve original evidence and published writing exemplars from the author's local paper corpora, prioritizing local sources for relevant research and manuscript work. Also inspect, build or maintain their verified indexes.
---

## Codex CLI Adaptation

This skill provides the local registered-paper-corpus adapter for Research Agent.

- Interpret Claude slash-command references such as `/nature-literature-kb` as the Codex skill name `nature-literature-kb`.
- Map Claude tools to Codex operations: `Read`/`Glob`/`Grep` to shell reads/searches, `Write`/`Edit` to local file edits, and `Bash` to PowerShell-compatible `shell_command`.
- Do not assume Claude Code hooks, settings, slash-command routing, or Claude-only frontmatter fields exist in Codex CLI.
- Use this skill only as local-document intelligence support; it does not replace `research-agent` for topic discovery.
- Follow `C:\Users\Administrator\AGENTS.md` and project-local `AGENTS.md`.

# nature-literature-kb

Use this skill when the user asks to build, refresh, inspect, or query the papers branch of the unified LLM knowledge-base project on D drive.

This is the first retrieval source for relevant literature-dependent research
and substantive manuscript writing. Infer the corpus from the topic, project
pointers and relevant index registries; do not wait for the author to name this
skill. Reuse sufficient evidence already read for the task. Supplement missing,
newer, closest-prior or contrary evidence through the search owner.

The author describes this library as curated published Q1-or-above literature.
For writing exemplars, prioritize relevant Nature/Science/Cell and field-leading
journals, matching study design, article type and section. The whole paper is
available for learning: concepts, research design, methods, analysis, figures,
interpretation, narrative and language. For narrative learning, retrieve a
paper as a connected work: read its Abstract, Introduction and Discussion
together, with the Results/figures needed to understand how its story is earned.
Return enough section context and original locators for the writing owner to
follow that progression; isolated search snippets are insufficient. Reuse
adequate source-linked distillations. Topic similarity alone does not select
an exemplar. Keep this preference
separate from claim support and unverified per-paper quartile metadata.
Preserve contrary findings and corpus coverage limits. Language-only edits
need no new literature search.

## Quick Trigger / Stop Card

- Use when: relevant research or substantive writing needs literature evidence or published exemplars, without an explicit KB request; also for requested corpus queries, inspection, building or maintenance.
- Do not use as the sole owner of open-ended discovery, closest-prior coverage, novelty judgment, or acquisition of papers outside the corpus; use the corresponding research or search owner.
- Required inputs: selected `corpus_id`, source/index boundary, intended action, and a verified backend/script path.
- Output / handoff: backend and run directory, corpus boundary, retrieval candidates with source locators, quality warnings, and next owner skill; add a Retrieval QA Dossier when multiple KB papers will feed manuscript prose.
- Return / stop conditions: missing script/index -> `KB_RESOURCE_MISSING`; documented interface drift -> `KB_RESOURCE_CONTRACT_DRIFT`; missing runtime dependency -> `KB_ENVIRONMENT_MISSING`; unresolved corpus/run boundary -> `KB_CORPUS_UNBOUND`; incomplete retrieval QA for a planned manuscript claim -> `KB_RETRIEVAL_QA_INCOMPLETE`; incomplete corpus coverage -> return to `research-agent` for field-level claims.
- Validation: `Test-Path`, script `--help` or AST/parser check, manifest/artifact readback, and a read-only query or explicitly scoped smoke build.

## Canonical Entry

Canonical unified LLM KB root:

```text
D:\03_Agent4Science\01_LLM-knowledge_base\research_wiki
```

Knowledge branches:

```text
papers\                               # original PDFs, article metadata, paper RAG indexes
wiki\sources\                         # academic paper archive cards and actual paper reading pages
external_materials\Official account\  # secondary articles/tool originals, app and historical indexes
external_materials\cards\             # external-source metadata cards, not reading notes
wiki\notes\                           # actual source-linked reading notes only
```

Project-specific paper indexes should live under:

```text
D:\03_Agent4Science\01_LLM-knowledge_base\research_wiki\papers\indexes\<corpus_id>
```

Public library names (storage/run names are internal provenance):

```text
research_papers    科研文献库: repaired main, supplement, Zotero, wind ecosystem, validated additions
research_notes     研究笔记库: actual author/agent reading notes with original-source packets
external_materials 外部资料库: secondary articles and methods/tool originals, separate from papers
figure_references  图件参考库: existing Nature figure owner and design-reference router
```


Unified PDF storage policy:

```text
D:\03_Agent4Science\01_LLM-knowledge_base\research_wiki\papers\sources\<corpus_id>\pdfs
```

Keep PDFs, derived chunks, metadata, QC artifacts, and generated indexes in separate sibling directories.

## Verified Backend Routes

Read `library_catalog.json` or run `python -B papers/scripts/research_library.py catalog`
at the KB root. Use these public names without asking the author to select an
extraction batch. Existing sources/runs retain their binding paths. Archived
green-certificate runs are not active sources. Backend extraction quality still
differs and must remain visible in each result.

### Research papers: automatic context reading (default)

For manuscript drafting or substantive revision, execute this route when local
literature is needed. The author need not ask for context recovery, run a shell
command, translate queries or select a reading mode. Reuse adequate source-linked
reading already available for the same task. Infer useful English scientific
terms and bounded query variants from the writing question.

The unified entry searches all catalogued paper sources and validated additions,
then reads original blocks from the selected version. Supply bounded English
scientific variants alongside a Chinese question. Repeated storage copies do not
earn extra fusion votes. Inspect `searches`, `errors` and `query_warnings`; zero
hits do not establish a field-wide gap. Follow `docs/research_library.md`.
For a concrete recall gap, retry with `--hybrid`: existing offline hybrid
candidates map to repaired pages only when PDF bytes are identical. Inspect
`unmapped_hybrid_candidates`; this is not a new dense index or a reranker.

Operational root is the canonical KB root above. Typical agent-internal call:

```powershell
python -B papers/scripts/research_library.py query "<writing question>" --query-variant "<English scientific terms>" --limit 3 --context-mode narrative --context-chars 24000
```

Choose the context mode from the writing intent:

| Writing use | Context mode |
|---|---|
| Whole-paper exemplars, central story, Abstract/Introduction/Discussion framing | `narrative` |
| Interpreting findings or comparing results with method/figure context | `results` |
| A specific supporting passage or local subsection | `section` |

`section` recovers the whole observed Introduction for its subsection hits;
`narrative` connects source-observed Abstract, Introduction, Methods, Results,
Discussion and Conclusion. Read `context.blocks`, not the navigation snippet.
Inspect `missing_components`, `structure`, `source_binding_status`, candidate
links and source warnings. Method/figure links need scientific interpretation;
an unavailable hierarchy or historical missing PDF hash remains uncertain.

For sources selected for the manuscript, inspect `status`, `anchor_included`,
`unread_ranges` and `continuation`. Follow the same run, chunk and context mode
until the needed sections and qualifications have been read. Use returned
`continuation.offset`; allow at least `minimum_chars_for_next_block` so the next
paragraph/table/formula fits intact. The adapter does not silently cut a source
block. Do not read every search candidate merely because it was returned.
`anchor_source_offset` can target the observed anchor before filling surrounding
conditions; native sources offer a text-matched block range when available,
otherwise only a page-start candidate. Their section hierarchy remains unverified. A targeted offset
does not mean earlier material or the whole narrative has been read.

The query adapter prioritizes a source anchor when reading from the start would
exhaust that paper's share of the text budget. Inspect `selection_strategy` and
`preceding_continuation`: for a selected paper, use its run/chunk/mode and offset
to read earlier conditions as needed, then follow the forward `continuation`.
`stop_before_offset` marks the already-reached source boundary; it is not a CLI
option. For connected narrative learning, recover the relevant preceding and
following sections in source order. If the anchor is still absent, use the
reported `minimum_chars_for_anchor` or next whole-block requirement for the next
bounded read. Never call a focused or PARTIAL read a complete Introduction.

When configured, local reranking follows fused recall and uses selected enriched
titles with their recorded status. Inspect `reranking`, errors and per-result
`rerank.token_coverage`; a ranking score is not evidence support. A reranker error
is explicit PARTIAL_FAILURE. `--no-rerank` is a troubleshooting fallback, not a
silent replacement for a failed model. Do not interpret model-trimmed ranking
input as the original evidence read; use the source-context reader above.
Front-matter hits (such as ARTICLEINFO/keywords) can be redirected to an observed
Abstract or Introduction chunk in the same paper and source run. Inspect
`reading_anchor` and `rerank.source_chunk_id`; retain the original recall locator
and use the reading anchor or returned continuation for source reading. A
`FRONT_MATTER_NAVIGATION_ONLY` passage is navigation, not scientific evidence.

```powershell
python -B papers/scripts/research_library.py read --run-dir "<source_run>" --chunk-id "<chunk_id>" --context-mode narrative --offset <continuation.offset> --max-chars <sufficient_text_budget>
python -B papers/scripts/research_library.py read --run-dir "<source_run>" --chunk-id "<chunk_id>" --list-sections
python -B papers/scripts/research_library.py read --run-dir "<source_run>" --chunk-id "<chunk_id>" --section-id "<observed_section_id>"
```

Save large JSON responses under the task's existing evidence/log location and
read bounded block ranges. Receiving a file or a truncated tool response does
not mean its contents were read. `COMPLETE` describes the selected source scope,
not whole-paper semantic completeness. Check missing sections and original PDF
pages when the claim needs them; do not infer absence from an unrecognized heading.
Keep different PDF versions separate and verify identity plus original locators
before citation. If needed support remains unavailable, hold that claim and
continue the supported prose, using external search for the specific gap.

Source-text budgets are shared across papers with unused capacity redistributed;
they are not model-token budgets. Large responses should use `--json-output`
under the task's evidence area, followed by bounded reading. Unread range lists
may be abbreviated, but continuations retain the exact block offset. Do not
classify `evidence_relation=UNASSESSED` as support. Reuse existing task notes to
connect actual claims with source locators, study conditions and qualifications.

For secondary articles or method/tool originals query `--library external_materials`
and inspect `external_results`. Actual source-linked reading notes use
`--library research_notes` and `note_results`; generated source cards are excluded.
`--library all` keeps papers, notes and external materials separate. Read a selected
material or reading note with `read --note-file "<source_file>"`; it is not verified
paper evidence. After actual reading and authorized writeback, publish a note under
`wiki/notes/` with its original read JSON; never count imported articles as completed notes. For a
selected figure/table/formula, `object --run-dir "<source_run>" --paper-id
"<paper_id>" --block-id "<block_id>"` returns the original object and available
image path. Inspect the image/PDF, headers, units, notes and definitions before
using scientific values. Design references continue through `nature-figure`.
If image files are missing or page layout matters, add `--render-page
"<new_task_page.png>"` to the object command and visually inspect the exported
original PDF page. Existing image files are preserved; export is not interpretation.
Explicit additions use `research_library.py add <supplied PDF/MD/TXT path>`;
no scheduled scan, watch service, automatic framework install or whole-corpus
rebuild is part of ordinary writing.

### DL-GEE: optional historical hybrid recall expansion

Operational root:

```powershell
cd "D:\03_Agent4Science\01_LLM-knowledge_base\research_wiki"
```

Read-only query of the hash-verified active hybrid `run_*` index:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File papers\scripts\query_dlgee_hybrid.ps1 "deep learning geospatial process extraction"
```

The launcher uses the pinned managed runtime, retrieval overlay, local model
snapshot, and offline Hugging Face cache. If any of those paths is unavailable,
return `KB_ENVIRONMENT_MISSING`; do not install or silently switch models. The
query verifies the registered manifest, health report, parent BM25 bindings,
and FAISS hash before loading the index. Use the lexical fallback explicitly
when dense retrieval is unavailable or a BM25 comparison is requested:

```powershell
python papers\scripts\query_dlgee_literature_index.py "deep learning geospatial process extraction"
```

Use this historical route for explicitly requested hybrid retrieval or a concrete
recall gap after the default writing route. It does not search the repaired
chunk namespace or manual additions. For multiple query variants use
`--queries-file <plan.json> --chunks-per-paper 3`. Its own historical chunks use
`python -B papers/scripts/read_dlgee_evidence.py --chunk-id <id> --neighbors 1`
to read complete chunks and hash-bound original PDF pages. Use its
`--paper-id <id> --list-sections` and `--section <heading>` options for needed
methods/results context. Keep its IDs and reader within that run; never send
repaired/incremental IDs to this historical reader or attach them to old vectors.
Resolve paper identity and source version before switching between routes.
Keep the writing owner and continue after checking support; neither a search hit
nor a successful PDF read licenses a claim.
This adds no automatic API call, reranker, index refresh or mandatory Paper Card.

An explicitly requested five-paper smoke build must stay under `smoke_runs` and must not replace the production index:

```powershell
python papers\scripts\build_dlgee_literature_index.py --limit 5 --output-root "papers\indexes\dl_gee_literature\smoke_runs" --smoke-query "deep learning geospatial process extraction"
```

### Green-certificate/carbon-power: archived hybrid backend

The executable currently lives at:

```text
D:\01_research\01_green certificate-carbon coupling\tools\literature_kb\literature_kb.py
```

The project is currently archive/read-only. Before build or refresh, read its project `AGENTS.md` and `STATUS.md`; do not reopen or modify the project/configuration unless the user explicitly asks. Its bundled `default_config.yaml` and README still contain pre-migration KB paths, so they are not current execution authority.

For a read-only query of the existing relocated index, preflight both resources and dependencies, then pass the current index path explicitly:

```powershell
$toolRoot = "D:\01_research\01_green certificate-carbon coupling\tools\literature_kb"
$kbDir = "D:\03_Agent4Science\01_LLM-knowledge_base\research_wiki\papers\indexes\green_certificate_carbon_power\run_20260605"
Test-Path -LiteralPath "$toolRoot\literature_kb.py"
Test-Path -LiteralPath "$kbDir\manifest.json"
python -c "import faiss, rank_bm25, pandas, numpy, fitz, yaml"
python "$toolRoot\literature_kb.py" query --kb-dir "$kbDir" --query "绿色证书 与 碳交易 电力市场联动"
```

If the dependency preflight fails, return `KB_ENVIRONMENT_MISSING`. Do not install packages or change the archived project automatically.

## Current Pipeline Contract

- Source corpus: shared KB PDFs under `D:\03_Agent4Science\01_LLM-knowledge_base\research_wiki\papers\sources\green_certificate_carbon_power\papers`.
- Output root: `D:\03_Agent4Science\01_LLM-knowledge_base\research_wiki\papers\indexes\green_certificate_carbon_power`.
- DL-GEE corpus: original PDFs, existing PDF chunks, metadata, extraction outputs, and QC artifacts are stored under `D:\03_Agent4Science\01_LLM-knowledge_base\research_wiki\papers\sources\dl_gee_literature`; treat this as a separate corpus and do not merge it into the green-certificate/carbon-power index.
- Before build/query, verify the canonical root and selected corpus/index path exist. Treat older roots only as provenance unless the user explicitly selects them.
- DL-GEE default manuscript route: `manage_dlgee_library.py query/read` searches the repaired main FTS run, supplement and healthy manual additions, then recovers source context. Read its reported runs and coverage; no dense update is implied. The historical hybrid remains registered in `papers/indexes/dl_gee_literature/active_run.json`: pinned Qwen3-Embedding-0.6B/FAISS plus the immutable parent SQLite FTS5/BM25 run, fused with RRF. Its BM25 parent is the historical lexical fallback; keep its chunk namespace separate.
- Green-certificate archived backend: MinerU/PyMuPDF extraction, semantic chunks, dense index + BM25 reciprocal-rank fusion, and section/short-chunk reranking. Its artifacts are `manifest.json`, `kb_stats.json`, `kb_quality_report.md`, `chunks.csv`, `papers.csv`, `dense.index`, and `bm25.pkl`.
- Report the selected backend and exact run directory. Do not describe the DL-GEE backend as reranked, and do not treat the archived green-certificate manifest as proof that its original source paths remain active.

## Research Workflow Integration

Use this adapter for local-PDF retrieval, corpus-supported writing or knowledge-base maintenance:

```text
research-agent -> nature-literature-kb -> original-source verification -> nature-writing (substantive prose)
Use nature-academic-search for coverage outside the corpus;
use nature-downloader for lawful retrieval of missing originals.
```

For requested writing from multiple corpus papers, load
`../shared-references/kb-to-manuscript-evidence-bridge.md`. This owner supplies
retrieval candidates; `research-agent` coordinates the task and
`nature-writing` owns substantive source-grounded synthesis and prose.
Use `nature-reader` for a requested or necessary deep read, and
`nature-literature-synthesis` for formal review/synthesis work. Continue the authorized task
without forcing a full Paper Card or a retired manuscript stage per citation.

Hard boundaries:

- Do not cite `chunk_id`, vector IDs, or the KB answer as evidence.
- Evidence must resolve back to DOI/title plus page, section, table, figure, equation, or snippet locator from the original paper.
- If the selected backend's quality artifact (`quality_report.md` or `kb_stats.json` / `kb_quality_report.md`) shows poor extraction quality, report the limitation before using retrieved results.
- If the local corpus has not been coverage-audited, do not use it to claim the state of the whole field.
- Keep MinerU optional; unavailable MinerU should degrade to PyMuPDF, not block ordinary literature work.

## Minimum Output

For build/refresh:

```text
KB directory:
Backend:
Papers indexed:
Chunks indexed:
Extractor used:
Quality warnings:
Next query command:
```

For a standalone query request:

```text
Question:
KB used:
Backend / run directory:
Retrieval summary:
Top evidence candidates:
Limitations:
Next handoff:
```

For KB-assisted manuscript writing, retain the following in the internal handoff
or existing task notes. Continue to the requested clean prose; do not substitute
a retrieval report or shell instructions for the manuscript:

```text
Writing intent / target section:
Corpus inclusion and coverage boundary:
Query IDs and scientific questions:
Retrieval method / settings / source-diversity control:
Original-paper locator completeness:
Answerability: answered / partial / not enough evidence
Residual source families or contradictions:
Bridge status / failure code:
Next owner: nature-writing (substantive prose) / nature-reader (deep reading) / nature-literature-synthesis (formal synthesis methods)
```
