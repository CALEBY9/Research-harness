# Workflow 1: Multi-Source Literature Search

**Purpose:** Search multiple academic databases in parallel, deduplicate, merge, and rank results.

**Prerequisites:** Relevant mounted search tools or the standalone HTTP fallback in [routing and operations](../../static/core/routing-and-ops.md#no-mcp-fallback-standalone-search). Check actual availability before calling a named tool.

**Uses:** [Dedup Engine](../dedup-engine.md) — deduplication and merge preference logic.

## Procedure

1. **Analyze topic** — identify domain, consult [source routing](../search-strategy.md#source-selection).
2. **Select sources by tier** — follow [Source Tiers](../source-tiers.md). Always try T1 first; escalate to T2 only if T1 insufficient; use T3 as last resort with explicit user warning.
3. **Search in parallel** — call all relevant MCP search tools simultaneously:
   - Biomedical → `pubmed_search_articles`
   - Cross-disciplinary → `search_crossref`
   - Preprints → `search_arxiv` / `search_biorxiv` / `search_medrxiv`
   - Exhaustive → add `search_semantic_scholar` / `search_webofscience` / `search_scopus`
4. **Deduplicate** — apply [Dedup Engine](../dedup-engine.md) to merged result list.
5. **Merge and rank** — follow the user's relevance/date/citation preference. For claim-support work, keep relevance, evidence type and original-source access separate: an inaccessible direct study remains relevant but unverified; an accessible peripheral paper is not equivalent support. See [Result Ranking](../search-strategy.md#result-ranking).
6. **Complete the requested search** — bibliographic discovery ends with its requested records. For claim support, map each material claim to the checked original passage and its scope, or mark the specific unresolved gap. A fixed paper count, DOI match or accessible full text alone does not establish adequate support. Do not replace the research question to fit available papers. Continue useful supported work within scope, and preserve important blocked candidates and lawful fallback attempts in the result.
7. **Present results** — include source labels and verification status; for claim support also give evidence type, locator and limits. A short table is sufficient; do not require a new workflow artifact for a simple lookup.

## Adaptive search for a consequential evidence gap

For a novelty assessment or claim-bearing synthesis, revisit the search only
when a specific unresolved proposition could change the answer. A simple
bibliographic lookup can finish at the requested records.

1. Name the unresolved proposition: closest precedent, rival explanation,
   contradictory result, missing population/scale or inaccessible pivotal study.
2. Choose the next query to address that gap. Use synonyms or adjacent fields,
   opposing/null findings, or a selective backward/forward citation lead from a
   pivotal paper. Use available index tools or checked reference lists; do not
   require a new citation-graph service or repeat every source in every round.
3. Verify the relevant original passage. Before calling findings contradictory,
   compare definitions, populations, scales, methods and data provenance;
   shared underlying data do not provide independent corroboration. Retrieval
   rank, model confidence and citation counts do not certify scientific quality.
4. Stop when the material proposition has adequate scoped evidence and the
   relevant competing findings have been considered, or when access, source
   coverage or the authorized effort limit prevents resolution. Report what
   remains unresolved and its effect on the answer. No hits means an incomplete
   search result, not proof that nobody has done the work.

Keep queries, citation leads, original locators and unresolved limits in the
same result report or existing project record. This loop gathers evidence;
`res_find` owns the novelty/hypothesis judgment and the author selects the
research direction. Literature disagreement alone does not generate a validated
new mechanism.

## Output Format

```
**Title**: [Paper Title]
**Authors**: [Author list]
**Journal**: [Journal name]
**Year**: [Year]  |  **DOI**: [DOI]  |  **PMID**: [PMID]
**Citations**: [count if available]
**Abstract**: [First 200 characters...]
```

## Error Modes

- **MCP tool unavailable:** report specific failure, continue with remaining tools.
- **No results:** broaden terms per [Query Construction](../search-strategy.md#query-construction), try alternative sources, suggest user refine query.
- **All sources empty:** suggest MeSH strategy (Workflow 3) or manual query refinement.
