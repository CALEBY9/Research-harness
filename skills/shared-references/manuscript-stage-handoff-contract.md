# Manuscript Stage Handoff Contract

## Purpose

Use this contract when substantive manuscript work crosses `paper_outline`, `paper_write`, `paper_review`, or `paper_polish`. It transfers the minimum governing state without copying whole skill bodies, long review reports, retrieval dossiers, or source prose into the next generation context.

This contract does not replace the canonical paper plan, evidence assets, manuscript, or review report. It points to them and freezes the subset needed by the next owner.

## Context discipline

1. Do not preload the full four-owner chain. Load the current owner only.
2. At a stage boundary, write one compact handoff record and bind it to the exact source artifact or plan hash when file-backed.
3. The next stage loads its own owner, this handoff, and only the referenced evidence/profile slices needed for its decision. Do not reread an upstream owner merely to reconstruct its reasoning.
4. Treat upstream instructions as completed-stage provenance, not as additional governing prompts for prose generation.
5. If an actual context reset is required for a long manuscript, resume the next owner in a fresh run or turn from the handoff locator. A handoff can reduce carried instructions and copied material; it cannot erase tokens already loaded in the same model context.
6. Keep every handoff author-side. Never paste route labels, IDs, hashes, review notes, or failure codes into clean manuscript prose.

## Common envelope

```text
Handoff ID:
From owner -> To owner:
Writing Profile Lock and profile reference:
Section / editable surface:
Canonical plan or artifact locator + SHA-256 / revision marker:
Section question:
Dominant claim and supporting roles:
Admitted Claim IDs -> Evidence IDs/states/locators:
Paragraph functions / order:
Required boundaries and hedges:
Terminology-map locator:
Protected spans / immutable surfaces:
Unresolved blockers or failure codes:
Next-stage stop condition:
```

Use locators rather than embedding whole evidence cards, PDFs, KB answers, or prior drafts. Include short excerpts only when the next decision cannot be made safely from the locator and label them as evidence, not prose to reuse.

## `DRAFT_HANDOFF` — outline to write

Add:

```text
Red thread / one-sentence defensible answer:
Section-specific prose contract:
Claim order and required comparisons:
Figure/table callouts and role:
KB Synthesis IDs, when triggered:
Excluded, deferred, or supplement-only material:
Output path and collision state, when file-backed:
```

`paper_write` may dereference only the claims, evidence rows, figures, and terminology needed for the target section. A missing claim state, locator, paragraph function, or boundary returns to `paper_outline`; it must not be filled with plausible prose.

## `REVIEW_HANDOFF` — write to review

Add:

```text
Draft locator + exact hash / inline text boundary:
Drafted section and intentionally unchanged surfaces:
Claim-to-paragraph map:
Known weak points and deferred issues:
Representative KB claim traces requested, when triggered:
Checks already run and their evidence:
```

`paper_review` evaluates the manuscript and locators, not the prose-generation rationale. Return a delta-oriented action matrix plus a `POLISH_HANDOFF`; do not make the next stage carry the full review report unless a specific blocker requires it.

## `POLISH_HANDOFF` — review to polish

Add:

```text
Review verdict: PASS_FOR_POLISH / RETURN_UPSTREAM
Scientific and structural blockers: NONE / listed
Authorized language/style surface:
Facts, numbers, units, citations, hedges, equations, and claims to preserve:
Remaining reader-facing defects:
Target/generic profile pointer:
Artifact/scanner requirements, if any:
```

`paper_polish` consumes the clean draft plus this record. It does not need the full `paper_outline`, `paper_write`, or `paper_review` instruction bodies. If the verdict is `RETURN_UPSTREAM`, do not polish around the blocker.

## Completion check

A handoff passes when the next owner can identify what may change, what must remain fixed, what evidence supports each claim, what section logic to execute, and when to stop without reconstructing the upstream stage. Use `MANUSCRIPT_HANDOFF_INCOMPLETE` when any required field is missing or contradictory.
