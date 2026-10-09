# Scientific writing rebase — 2026-09-22

The author explicitly requested removal of the entire Nature Skills suite and
then skill_evolve_workflow. This supersedes prior Nature-first and maintenance-
skill requirements. It is an author-directed architectural change, not a claim
that a model comparison established a better writing system.

## Applied scope

- Removed the 18 suite directories from both the live shared installation and
  maintained source, including nature-shared and researchwrite.
- Removed skill_evolve_workflow from the Codex installation, Claude installation
  and maintained source. Backups remain outside skill discovery, not executable
  dependencies. No research manuscript, corpus or analysis was removed.
- Research Agent now handles writing, language revision, source reading,
  citation work and correspondence directly, with existing local support tools.
  The legacy workflow and paper_* chain are not restored.
- Rebound support-skill handoffs, UI metadata and regression expectations;
  disabled removed-package import paths. Import hashes remain historical
  provenance, not an active inventory.
- Removed Claude's maintenance-skill dispatch. This is not a replacement of
  the separate Claude research workflow or proof of cross-CLI writing parity.

## External designs actually checked

Official repositories, README material and the relevant source were inspected.
No external repository was installed or executed, and no private papers were
uploaded. Repository metadata below is a 2026-09-22 snapshot, not a quality score.

| Project | Relevant mechanism | Decision and limits |
|---|---|---|
| [OpenScholar](https://github.com/AkariAsai/OpenScholar) | Source-grounded scientific responses, feedback-directed additional retrieval and attribution; verified in src/open_scholar.py and src/instructions.py | Use as a design reference for question-led literature synthesis. Apache-2.0; not archived; reported last push 2025-08-13. Its full retrieval/model stack is not installed; scientific QA is not manuscript-quality proof. |
| [PaperQA2](https://github.com/Future-House/paper-qa) | Search, question-conditioned evidence gathering and answering; verified in the algorithm description and src/paperqa/agents/tools.py | Use as an evidence-gathering reference while retaining the existing local KB. Apache-2.0; not archived; reported last push 2026-09-17. No package upgrade, reindexing or external-provider configuration is implied. |
| [STORM](https://github.com/stanford-oval/storm) | Perspective-guided questions and pre-writing knowledge curation | Not the manuscript foundation: the authors describe Wikipedia-like articles and expressly disclaim publication-ready output. MIT; not archived; reported last push 2025-09-30. |
| [AI Scientist v2](https://github.com/SakanaAI/AI-Scientist-v2) | Autonomous ML experiments and manuscript generation | Not installed: the current task is evidence synthesis and scientific narrative, not autonomous ML experimentation. Repository specifies Linux/NVIDIA execution and warns about executing generated code; custom license requires separate review before reuse. Not archived; reported last push 2025-12-19. |

The active adaptation is
`skills/research-agent/references/source-grounded-synthesis.md`. It contains
original local guidance, not copied upstream prompts or code. It does not
prescribe paragraph count, stock transitions, citation quotas or a mandatory
sequence of agents. Better narrative quality remains to be demonstrated on
the author's actual material.

## Validation

- `python -B scripts/harness.py validate`: PASS; 15 source skills, 10 parsed
  Python files, 36 regression definitions. No behavioral model execution.
- `python -B -m unittest discover -s tests -v`: 25/25 PASS.
- UTF-8 `quick_validate.py` on the live research-agent: PASS.
- `git diff --check`: PASS; existing line-ending warnings are informational.
- Two historical private writing fixtures remain missing and explicitly
  blocked; their cases were not executed. Scientific meaning constraints and
  adverse-evidence checks remain in the retained regression pack.

Use a fresh session to refresh discovered skills. Do not read archived copies
to satisfy a stale catalogue. Existing unrelated worktree edits were preserved;
no commit, push, provider change, automatic hook or new runtime was performed.
