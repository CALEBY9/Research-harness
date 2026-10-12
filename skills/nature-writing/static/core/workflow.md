# Writing workflow

Use this workflow for a new section or substantial argument reconstruction. For a title, one paragraph or a follow-up edit, reuse the settled framing and apply only the relevant steps. Planning supports the requested prose; it is not a separate deliverable unless requested.

This workflow does not apply to a supplied passage whose argument, evidence,
claim strength, and paragraph order must remain fixed. Route that
`LANGUAGE_ONLY` request to `nature-polishing`; do not require an argument plan,
confirmation gate, Terminology Ledger presentation, or claim-evidence map.

## 1. Build a one-sentence argument

> In [system/problem], we show [advance] using [approach], supported by [evidence], with [boundary].

Use this sentence to clarify the article's contribution, not to replace the author's question set. Several confirmed questions may support one contribution, and a thesis may have several chapter arguments. If a material scientific premise remains unresolved, identify the affected passage and continue the supported work.

## 1b. Build the Terminology Ledger

On first contact with the material, extract the recurring terms, abbreviations, notation, and proper names into a Terminology Ledger before drafting any prose. Lock the canonical forms and reuse them across every section. See `../../../nature-shared/core/terminology-ledger.md`.

## 2. Choose section architecture

Pick the section structure from the relevant `section/*.md` fragment and, if needed, deeper patterns from `references/article-architecture.md`.

## 3. Give each paragraph a primary reasoning purpose

Identify what the paragraph lets the reader understand. Context, comparison, evidence, explanation and qualification may work together toward that purpose; these are functions, not mutually exclusive paragraph types.

Split a paragraph when it contains unrelated conclusions or an unmanageable change of question. Keep the evidence-to-inference bridge and necessary boundary with the claim they explain. Do not split merely because two rhetorical functions occur together.

## 3a. Allocate Results evidence before drafting

When the task includes Results, a full manuscript, main-text compression, or
main-versus-SI placement, load
`../../../nature-shared/core/main-text-discipline.md`. Classify each result as
core discovery, necessary support, qualification, robustness, heterogeneity,
provenance detail, alternative inference, or edge case. Build the shortest
sufficient main-text evidence chain and record the destination of everything
else. Do not bury conclusion-changing evidence in SI.

## 3b. Confirmation gate — align before drafting

Resolve the core claim, evidence, and boundary from supplied materials and prior
author decisions; they need not be separately restated in the latest prompt.
When these support the requested draft without a material unresolved premise,
proceed to full prose. Do not invent missing evidence or choose a new dominant claim.

If an unresolved choice changes the scientific meaning or requested deliverable,
show the one-sentence argument, the specific uncertainty, and at most 2–3 focused
questions. Await the author's decision for the affected prose. If the author
requests a scaffold despite missing evidence, use explicit placeholders.

- **Depth dial**: deliver an outline first only when the user requests staged
  review or an outline is the requested deliverable.
- **Style, not substance**: if the user says the voice or style "is not mine", do not keep guessing — ask for one short sample of their own writing, then calibrate to it. From the sample, match: typical sentence length and rhythm, hedging level (`demonstrate` vs `may` / `could`), preferred connectives and transitions, person (first-person `we` vs passive), and terminology / abbreviation choices. Match the voice, not the content — never reuse the sample's claims or facts.

## 4. Draft from evidence outward

Keep claims near the data that support them. Do not stack claims at the top of a section then leave evidence at the bottom.

## 5. Calibrate verbs to evidence strength

`show` / `demonstrate` need strong direct evidence. `suggest` / `indicate` are for trend-level or indirect evidence. `may` / `could` are for plausible but unverified mechanisms.

## 6. Remove unsupported novelty and universal claims

Sweep for `first`, `unique`, `unprecedented`, `comprehensive`, `complete`, `always`, `never`. Replace with bounded claims or delete.

## 7. Run a paragraph-flow check

- One paragraph, one message.
- The first sentence is the topic / claim.
- Each subsequent sentence has an explicit relation to the previous one (cause, comparison, restriction, example).

For full reverse-outlining, open `references/paragraph-flow.md`.

## 8. Return prose plus notes

Output the draft together with explicit notes on assumptions, missing inputs, and where evidence is needed. See `output-format.md`.

## 9. Revise by targeted edit, not full rewrite

When the user reacts to a draft, "this is not what I meant" is usually local — a wrong claim, a mis-framed paragraph, the wrong result leading. Do not silently re-draft the whole section: a full rewrite breaks the paragraphs that were already right and forces the user to re-check everything.

- Change **only** the paragraphs or claims the user flagged; keep the rest verbatim.
- If a requested fix genuinely forces a structural change (reordering sections, moving a claim across paragraphs), say so and confirm the new structure before applying it, rather than restructuring silently.
- Keep the Terminology Ledger (step 1b) stable across revisions unless the user changes a term; never let a revision reintroduce a variant of a locked term.
- After revising, re-run only the checks relevant to what changed (steps 5-7), not the whole workflow.
- If the user's redirection reveals the original premise was wrong, return to the confirmation gate (step 3b) instead of patching prose on a broken premise.
- Every proposed addition triggers the main-text deletion check: identify the
  new sentence's function, find existing text with the same function, and prefer
  replacement or compression before appending. Re-run the paragraph necessity
  and claim-repetition checks after the edit.
