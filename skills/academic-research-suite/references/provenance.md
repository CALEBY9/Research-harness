# ARS 精选适配来源

Installed scope: research-question development, literature investigation and
research/paper framework planning. This is a local selective adaptation, not
the full ARS-Codex package or a claim of upstream behavioral equivalence.

## Inspected source

- Repository: [Imbad0202/academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex).
- Exact inspected commit: `8d6a1f856ee3da9d3a5e2b7f292b3dfe72b592c5`, fetched 2026-10-25.
- Adapter version recorded by upstream: `3.23.1`.
- Vendored original suite: [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills),
  commit `4c5449017f46eb64d112a301d4817d22c7c9f3d9`, as identified in the inspected adapter manifest.
- Paths below are relative to `skills/academic-research-suite/ars/` at the inspected Codex commit.

| Selected source methods | Local carrier |
|---|---|
| `deep-research/agents/research_question_agent.md`: question types, FINER, scope and sub-question inheritance | `question-framing.md` |
| `deep-research/references/socratic_mode_protocol.md` and `socratic_questioning_framework.md`: guided questioning and question authorship | `question-framing.md` |
| `deep-research/agents/bibliography_agent.md` and `academic-paper/agents/literature_strategist_agent.md`: queries, search records and source curation | `literature-survey.md` |
| `deep-research/agents/synthesis_agent.md`: thematic, narrative, framework and critical synthesis; conflicting evidence | `literature-survey.md` |
| `deep-research/templates/literature_matrix_template.md`: source-by-theme evidence organization | `literature-survey.md` |
| `deep-research/agents/research_architect_agent.md`: question–method–data coherence | `framework-planning.md` |
| `academic-paper/agents/structure_architect_agent.md` and `references/paper_structure_patterns.md`: evidence-to-section mapping and structure families | `framework-planning.md` |
| `academic-paper/agents/argument_builder_agent.md`: claim–evidence–reasoning, counterarguments and logical progression | `framework-planning.md` |

## Local modifications and exclusions

The selected methods are rewritten in Chinese and combined into three
task-loaded references. The upstream agent files and workflow entrypoints are
not installed as independently executable agents. FINER remains a qualitative
decision aid; fixed question/source/round quotas, numerical self-score gates,
paper-count voting and a universal clinical evidence pyramid are not adopted.
These choices preserve source tracing, counterevidence, uncertainty and author
control while fitting the existing research workspace and environmental work.

Upstream drafting, abstracts, manuscript review, revision, formatting, full
pipelines, study screening, meta-analysis execution and experiment workflows
are not installed. Nature owns those applicable deliverables. Upstream hooks,
scripts, model routing, subagent topology, Material Passport/ledger machinery,
automatic updates and optional runtime dependencies are not activated or bundled.
This adaptation does not weaken any existing project, source-integrity,
privacy, permission or institutional approval requirements.

Only one public ARS skill is installed: `academic-research-suite`. The older
local `ars-academic-writing` source remains archived outside live discovery.
The installed skill is not registered with an automatic upstream updater.
Structural/discovery checks do not establish research quality, retrieval
coverage, source-coding accuracy or productivity improvement.

## License and attribution

Copyright (c) 2026 Cheng-I Wu. Selected upstream methods and this local
adaptation are provided under Creative Commons Attribution-NonCommercial
4.0 International. The upstream license is retained verbatim as
[LICENSE](../LICENSE). Local adaptation and selective scope are identified above;
no upstream endorsement is implied. The license does not cover the user's
manuscripts, private data or cited third-party papers.
