# Minimal ARS writing adoption

Current status, 2026-10-12: the author chose to restore Nature as the default
writing foundation from this repository's `b5b8e08` snapshot. ARS source and
local refinements are retained as an inactive alternative; the record below
describes the earlier adoption and is not the current default routing policy.

## Targeted narrative refinement, 2026-09-28

The author requested diagnosis and targeted ARS optimization. The existing
writing guidance already contained CARS, CER, counterarguments and source checks;
this was not treated as a missing-framework problem. Three existing references
were refined to distinguish source facts from cross-paper inference, make the
scientific value of descriptive comparisons explicit, and expand beyond a
convenient review-heavy evidence pack when a key premise needs original studies.
The short ARS entrypoint, upstream pin, license and author authority are unchanged.

The evidence reference no longer presents external benchmark results as local
acceptance criteria or conceptual similarities as implemented mechanisms. The
newer AI-for-Science sources remain background, not runtime dependencies:
[AstaBench](https://github.com/allenai/asta-bench),
[Kosmos](https://arxiv.org/html/2511.02824v2),
[Co-Scientist](https://www.nature.com/articles/s41586-026-10644-y), and
[Agent Laboratory](https://agentlaboratory.github.io/).
None establishes quality of this ARS adaptation. In particular, the previously
added approximately 99% citation claim was not substantiated by the cited Kosmos
paper, and its performance figures do not define acceptable manuscript errors.

KB handoff text now distinguishes Research Agent coordination/source work from
ARS substantive drafting. Eight paired files were brought to the approved target;
the already-identical ARS entrypoint was retained. Codex live/source parity was
checked, along with the same files through existing ZCode links. Editing a ZCode
junction edits its Codex target; it is not a separate installation or independent
behavioral evaluation. The earlier live-only changelog is retained as history
with a correction notice rather than loaded as guidance.

Validation: harness PASS (16 skills, 36 definitions, zero behavioral executions),
25 maintenance unit tests passed; ARS and Research Agent quick_validate passed.
The generic validator rejected the unchanged legacy `literature_kb` name because
it requires hyphen-case; the repository explicitly preserves that name and its
native validator passed. No naming migration was performed to hide the mismatch.

One complete Introduction application trial and separate evidence/diagnosis notes
were produced in ignored local state. This was a same-session application exercise,
not a fresh-context or blinded comparison: the writer had seen earlier drafts and
edited the guidance. It checked source roles, cross-paper transitions, fair
acknowledgment of prior syntheses and problem/design alignment, but cannot prove
better or stable submission-grade writing. Author acceptance remains unmeasured.
Private inputs and precise machine paths are kept out of this versioned document.
No accepted manuscript, KB index, production pipeline, model or hook was changed.

## Current supplement: writing depth retained, 2026-09-22

The author approved correcting excessive compression. Three task-loaded Chinese
references now retain detailed literature-to-argument synthesis, Introduction
narrative and substantive revision diagnostics, including decision criteria and
clearly hypothetical examples. `SKILL.md` explicitly routes relevant tasks to
them before the work they guide. This is not a second orchestrator or new skill.

The expanded provenance maps retained upstream functions to their local carriers
and explains omitted machinery. Citation identity/support, contrary evidence,
author authority and meaning preservation remain; fixed quotas, self-scoring,
full-suite passports and automatic delegation remain outside the adaptation.
The same upstream commit is used, with Writing Quality Check added as a source.

Current checks: quick_validate and harness structure validation passed;
`python -X utf8 -B -m unittest discover -s tests` reran all 25 maintenance tests
successfully (28.845 seconds). These are not manuscript-quality evaluations. All five
Markdown files match between installation and versioned source, and local links
resolve. The original 36 route definitions and sixteen-skill count are unchanged.
No new manuscript-writing trial was performed for this supplement. The earlier
three-Perspective sample below predates it and cannot establish its quality.
No accepted manuscript, KB, project data, model configuration or hook was changed.

2026-09-22: the author approved replacing the default writing foundation with
selected academic-research-skills guidance after reviewing an improved Introduction.
This is a local adaptation, not installation or certification of the full suite.
Upstream commit, selected sources and CC BY-NC 4.0 notices are retained in
`skills/ars-academic-writing/references/provenance.md`.

## Implemented scope

- Added one owner, `ars-academic-writing`, for substantive section drafting,
  argument reconstruction, abstracts, theses and proposals.
- Updated Research Agent's route; retained its evidence reference as support,
  not a competing writing owner. Existing language-only, citation-only, analysis
  and formatting routes remain. Local workspace instructions agree with the route.
- Synchronized installed and versioned skill files. Updated six existing writing
  regression owner declarations; all other thirty cases remain unchanged.
- Corrected four obsolete handoff metadata strings and the corresponding guide
  bullet in the separate local KB project. Retrieval algorithms, indices, source
  assets and past dossiers were not changed. This was a behavior-preserving
  mechanical edit for research-code-spec purposes; no scientific schema changed.
- No full ARS pipeline, runtime, dependency, model change, hook, schedule or
  automatic delegation was installed. No accepted manuscript was overwritten.

## Checks actually executed

- `quick_validate.py` on installed `ars-academic-writing` and `research-agent`:
  both valid.
- `python -X utf8 scripts/harness.py validate`: PASS, 16 skills, 36 case
  definitions, zero structural errors. This command executes no behavioral cases.
- `python -X utf8 -B -m unittest discover -s tests -v`: 25 tests passed.
- Five affected live/source files byte-identical; ten route declarations and
  negative controls inspected; six owner-only changes and thirty unchanged cases.
- KB scripts: exact before/after comparison allowed only the four named string
  substitutions; Python AST parsing passed. No costly query/index run needed.
- `git diff --check`: passed; pre-existing unrelated changes were preserved.

## Independent writing trial and limits

One user-approved fresh-context subagent received only a real project question
and three local original-source readings, not the accepted Introduction or an
expected answer. It followed the new writing route and produced a discussion
section plus separate argument/source notes in the research project, not here.
No ongoing multiagent workflow was enabled.

Source review found one Perspective-based passage phrased too much like a direct
empirical result; the passage was corrected to attribute the argument to its
authors. The clean heading and final scientific-use sentence were also tightened.
The prose progressed from the complementary roles of knowledge and learning to
use-dependent validation, without inventing the project's results. These are
observations from one revised sample, not a controlled comparison or evidence
of reliable submission-grade writing. Three Perspectives do not test broad
empirical synthesis. Final scientific and narrative acceptance remains the author’s.
