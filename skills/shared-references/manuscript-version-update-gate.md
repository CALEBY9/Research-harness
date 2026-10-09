# Manuscript Version Update / Story Rebase Gate

Use this gate when a task creates the next manuscript version, updates a versioned abstract or Introduction, merges or compares manuscript versions, synchronizes new evidence into a draft, or rebuilds the story of an existing manuscript. Do not use it for a first draft with no prior manuscript, a formatting-only task, or an exact-span proof/minor/R&R correction already governed by `paper_revision`.

## 1. Freeze the version boundary

Before prose mutation, record:

```text
Update mode: LOCAL_PATCH / EVIDENCE_SYNC / STORY_REBASE / TARGET_PROFILE_REBASE
Canonical fact base: path + SHA-256 when file-backed
Canonical plan: path + SHA-256 or revision marker
Plan freshness: CURRENT / STALE / CONFLICTING
Narrative base, if any: path + role
Style benchmark, if any: exact journal/article type + access date
Parent version: path + SHA-256
Output path: new path only
Output path state: ABSENT / COLLISION
Editable surfaces:
Protected surfaces:
Dominant claim:
Supporting claim roles:
Required review and format handoff:
```

Keep source roles separate:

- `FACT_BASE`: the current verified evidence, results, figures, tables, claim ledger, and boundaries. Only this role may supply manuscript facts.
- `NARRATIVE_BASE`: an optional earlier version used only for paragraph function, story order, or reader flow. It cannot override the fact base.
- `STYLE_BENCHMARK`: current target-journal guidance or comparable articles used for functional calibration, never as evidence or reusable wording.

If these roles are mixed or the canonical version is unclear, return `CANONICAL_VERSION_UNRESOLVED` before drafting.

## 2. Check plan freshness

Compare the canonical plan's scientific question, dominant claim, evidence states, cohort/sample/design facts, result boundaries, figure roles, and target profile against the current fact base.

- If they agree, mark `CURRENT`.
- If verified evidence changed but the plan can be deterministically updated, mark `STALE` and return to `paper_outline` before prose.
- If artifacts disagree or the intended scientific choice is not uniquely determined, mark `CONFLICTING` and request the resolving artifact or author decision.

Use `PLAN_ARTIFACT_DRIFT` for stale or conflicting plans. Do not patch prose first and repair the plan afterward.

## 3. Select one update mode

| Mode | Use when | Required route |
|---|---|---|
| `LOCAL_PATCH` | The scientific story and evidence are stable; only named spans need correction. | `paper_revision -> scoped owner skill -> paper_review verification` |
| `EVIDENCE_SYNC` | New or corrected evidence changes admitted facts, numbers, boundaries, figures, or limited claim wording without changing the paper's central story. | update claim/evidence ledger and plan -> revise affected locations only -> `paper_review` / `evidence_audit` |
| `STORY_REBASE` | The dominant claim, paragraph architecture, section order, or information economy is weak; incremental editing would preserve accumulated bloat. | `paper_outline` rebuilds the story contract from the fact base -> `paper_write` regenerates only authorized surfaces -> `paper_review` |
| `TARGET_PROFILE_REBASE` | The exact journal/article type changed while science remains stable. | existing `submit_guide -> paper_outline TARGET_PROFILE_REBASE` route |

Do not combine modes silently. If more than one is needed, order them explicitly: evidence sync first, then story or target-profile rebase. Return `UPDATE_MODE_UNRESOLVED` when the route cannot be selected safely.

## 4. Story-rebase admission

`STORY_REBASE` requires:

- one dominant claim stated in one author-side sentence;
- supporting claims that test, explain, bound, or generalize that claim rather than compete with it;
- a current claim-evidence ledger and red thread;
- explicit keep / drop / move decisions for material inherited from prior versions;
- distinct paragraph functions for the abstract and Introduction;
- authorization for the surfaces to be regenerated.

If several independent results remain equally central, return `DOMINANT_CLAIM_UNRESOLVED` to `paper_outline`; consider splitting, demoting, or moving material rather than listing everything in the abstract.

Do not merge prose from all prior versions. Reconstruct authorized reader-facing text from the current plan and fact base; use prior wording only when it remains accurate, necessary, and functionally superior.

## 5. Abstract and Introduction controls

The locked writing profile and exact target-journal benchmark control length and move structure. Across profiles:

- make the dominant claim and belief-changing result visible before a full method inventory;
- include only design details needed to interpret the main result;
- do not give every analysis, service, subgroup, robustness check, and caveat equal abstract weight;
- preserve boundaries needed to prevent material misreading, while moving audit rationale to author-side notes, Methods, Discussion, or limitations;
- assign every Introduction paragraph one necessary function and make the next paragraph answer the question created by the previous one.

Use `ABSTRACT_CATALOGUE_FAILURE` when the abstract is a list of independent methods/results/boundaries rather than one argument. This blocks polish.

## 6. Immutable output and QA binding

- A version-named output path is immutable. If it already exists, return `VERSION_PATH_COLLISION`; create a new version path or explicitly enter a controlled overwrite workflow with backup and revalidation.
- Bind review and QA claims to the exact artifact hash. If a reviewed or QA-bound artifact hash changes, return `POST_QA_ARTIFACT_DRIFT` and invalidate the old verdict.
- Never call a later filename the better or canonical version merely because its number or modification time is newer.
- For DOCX or multi-version deliverables, hand off to `paper_format` for lifecycle separation, output index/version ledger, save/reopen, rendering, and final delivery QA.

## 7. Verification before handoff

`paper_review` must compare the candidate against the version-update contract and, when a parent exists, the parent version:

```text
plan/artifact consistency
dominant-claim visibility
claim/evidence fidelity
paragraph-function distinctness
method and boundary load versus reader need
new repetition or catalogue behavior
promised keep/drop/move decisions
version path and QA hash integrity
target-profile fit without evidence inflation
```

Mechanical length or similarity counts may flag risk but cannot establish writing quality. For high-stakes story rebases, use a blind or side-by-side human review against a predeclared rubric before calling the candidate improved.

## Failure codes

`CANONICAL_VERSION_UNRESOLVED`, `PLAN_ARTIFACT_DRIFT`, `UPDATE_MODE_UNRESOLVED`, `DOMINANT_CLAIM_UNRESOLVED`, `ABSTRACT_CATALOGUE_FAILURE`, `VERSION_PATH_COLLISION`, and `POST_QA_ARTIFACT_DRIFT`.
