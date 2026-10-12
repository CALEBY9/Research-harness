# Source routing and operations

## Source routing

See [Source Tiers & Reliability](../../references/source-tiers.md) for the complete reliability classification and fallback routing rules. The T1→T2→T3 fallback chain is the standard execution order across all workflows.

Quick guide:

| User need | Primary (T1) | Secondary (T2) | Last Resort (T3) |
|-----------|-------------|-----------------|-------------------|
| Medical / clinical | PubMed | Semantic Scholar | Google Scholar |
| Cross-disciplinary | CrossRef | Semantic Scholar | Scopus |
| Preprints / CS / physics | arXiv | bioRxiv / medRxiv | — |
| Exhaustive review | PubMed + CrossRef + arXiv | Semantic Scholar + bioRxiv/medRxiv | WoS / Scopus |
| Citation count sensitive | Semantic Scholar | CrossRef | — |
| Chinese literature | — | — | CNKI / 万方 (manual) |

## Environment setup

### API keys (optional but recommended)

| Service | Env Var | Register At | Free Tier |
|---------|---------|-------------|-----------|
| Semantic Scholar | `SEMANTIC_SCHOLAR_API_KEY` | [api.semanticscholar.org](https://api.semanticscholar.org/) | Check current service/account quota |
| OpenAlex HTTP fallback | `OPENALEX_API_KEY` | [OpenAlex authentication](https://help.openalex.org/api/authentication/) | Anonymous basic use; key/account budget for larger searches |
| NCBI E-utilities | `NCBI_API_KEY` | [ncbi.nlm.nih.gov/account](https://www.ncbi.nlm.nih.gov/account/) | 10 req/s with key (3/s without) |
| Elsevier / Scopus / ScienceDirect | pybliometrics config | [dev.elsevier.com](https://dev.elsevier.com/) | Depends on API entitlement |

Set Semantic Scholar / NCBI keys via `export` or `.env` file. Elsevier keys are read from the local pybliometrics config, normally `~/.config/pybliometrics.cfg`; do not copy API keys into this plugin.

### Proxy (if behind firewall)

```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
```

### Pre-flight check

```bash
python scripts/preflight.py
```

Run before batch operations to verify API endpoints are reachable.

### Format converter dependencies

The format converter (`scripts/format-converter.py`) uses Python stdlib only — no extra dependencies. Run `python scripts/format-converter.py --test` to verify the conversion pipeline.

### No-MCP fallback (standalone search)

When the MCP server is not mounted (plain CLI use, skill auto-discovery, CI), the search workflow still runs via two stdlib-only scripts that hit public HTTP APIs directly — the same pattern `nature-citation/scripts/nature_citation.py` uses for CrossRef:

- **Discovery** — `scripts/academic_search.py` queries OpenAlex for keyword/author search, with relevance re-ranking and author disambiguation (`--affiliation` / `--orcid` / `--list-authors`). Returns ranked JSON (title, DOI, authors, year, citations, abstract). It supports anonymous basic use and an optional `OPENALEX_API_KEY` sent as a bearer header. Keep credentials in the runtime environment; do not put them in command arguments, URLs, reports or this plugin.
- **Download / convert** — `scripts/format-converter.py` turns the chosen DOIs/PMIDs/arXiv IDs into `.ris`/`.bib`/`.enw`/`.nbib` (CrossRef + PubMed + arXiv, also stdlib-only).

```bash
# discover, then export the picks
python scripts/academic_search.py "graph neural network potentials" --limit 10 --sort cited_by_count --mailto you@example.com
python scripts/format-converter.py --doi 10.1103/physrevlett.120.143001 --format ris
```

`--mailto` / `OPENALEX_MAILTO` / `CROSSREF_MAILTO` retain contact compatibility; they do not raise the API budget. Consult the current [authentication](https://help.openalex.org/api/authentication/) and [deprecation](https://help.openalex.org/api/deprecations/) guidance rather than assuming a permanent anonymous quota. HTTP failures remain visible and exit non-zero; do not silently retry an authenticated failure as anonymous. OpenAlex is one index, so its records are not independent verification by CrossRef, PubMed and arXiv. Use available original sources or independent providers where the requested evidence requires them. For field classification, OpenAlex Topics replaces deprecated Concepts; classification labels alone do not establish a research gap.

### MCP server runtime

Use uv to start the MCP server in an isolated dependency environment:

```bash
uv run --no-project --directory <mcp-server> --with "mcp>=1.0.0,<2.0.0" --with "requests>=2.28.0,<3.0.0" --with "toml>=0.10.2,<2.0.0" --with "lxml>=4.9.0,<6.0.0" --with "pybliometrics>=4.4.1,<5.0.0" python academic_search_server.py
```

`search_papers` defaults to CrossRef, PubMed, and arXiv. Scopus / ScienceDirect are opt-in providers: include `scopus` / `sciencedirect` in `sources`, or call their dedicated tools. These calls use the local pybliometrics config at `~/.config/pybliometrics.cfg` and may consume Elsevier API quota.

## Error handling

- **MCP tool unavailable**: report specific failure, continue with remaining tools. If the whole MCP server is absent, switch to the No-MCP fallback (`scripts/academic_search.py` + `scripts/format-converter.py`) above.
- **No results**: broaden terms, try alternative sources, suggest user refine query.
- **Script failure (2x)**: fall back to manual generation from MCP-fetched metadata.

## Limitations

- Google Scholar and Semantic Scholar are scraped (not API-backed) — results may vary.
- Chinese literature (CNKI / 万方) not indexed by CrossRef or PubMed.
- Citation counts may be delayed (CrossRef updates monthly).
