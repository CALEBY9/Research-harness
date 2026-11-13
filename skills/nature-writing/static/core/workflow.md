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

Reuse the project's established terms. For multi-section consistency, observed
drift or an explicit audit, maintain a compact Terminology Ledger in the existing
working notes. A short passage needs only an internal check against source
definitions. See `../../../nature-shared/core/terminology-ledger.md`.

When the source is development documentation, record internal shorthand as
source variants, not automatically as canonical manuscript terms. Resolve its
scientific meaning from the variable definitions, study protocol, or approved
methods, then select an established disciplinary term or a precise descriptive
phrase. Frequency in working notes alone does not establish the canonical term.
Reuse the existing ledger for recurring mappings; keep it outside the manuscript.

## 2. Learn the paper's story and choose section architecture

Use the relevant section guidance together with a suitable published local
exemplar or an existing source-linked distillation. Treat the paper as a connected
research work. Give priority to its Abstract, Introduction and Discussion,
reading them together with the Results/figures needed to understand the narrative.
Reuse sufficient previous reading; this is not a full-paper reread per citation.

For local sources not already adequately read, execute the verified context
route in `nature-literature-kb` automatically through its unified paper-library
entry, with bounded English query variants.
Read the returned source coverage and errors; a successful command or saved JSON
does not establish actual reading or claim support. Use connected `narrative` context
for whole-paper learning and Abstract/Introduction/Discussion framing, `results`
context for interpreting findings with method/figure candidates, and `section`
context for a specific supporting passage. The adapter owns commands and corpus
selection; the author need not choose the mode or run retrieval. Read the actual
source blocks, follow necessary continuations, and retain the selected run and
source version. Save large responses in the existing task evidence area and
inspect bounded passages so truncated tool output is never mistaken for reading.
Resolve missing sections or absent anchors through targeted section/original-PDF
reading before using the affected evidence; continue supported drafting when a
source remains unavailable. Candidate links and source coverage alone do not
establish scientific support. Keep recovery details in working notes.

Reconstruct what changes in the reader's understanding as the paper progresses:

- Abstract: which problem, central discovery, decisive evidence and implication
  survive compression; how the sentences form a complete scientific story.
- Introduction: how the opening creates a reason to care, prior knowledge leads
  to a precise unresolved issue, and the study's conceptual move becomes needed.
  Track paragraph functions, transitions and when the contribution is revealed.
- Discussion: how the paper answers its opening question, integrates findings,
  explains agreement or tension with prior work, and develops their broader
  meaning, limits and next questions.
- Across the paper: how the title and abstract express the same contribution,
  the Introduction motivates what the Results answer, and the Discussion
  changes the interpretation of those answers. Study design, methods, figures,
  analysis, sentence rhythm and other useful features as the current task needs.

Use these observations to shape the present manuscript's central message,
information order, emphasis and paragraph progression from its actual evidence.
When addressing "没有故事", "主线不清" or disconnected sections, repair the
requested narrative before sentence polishing. A language-only scope still
preserves the established argument. Keep useful source locators and adaptation
notes in existing working notes; the requested deliverable remains clean prose.
Reuse author-approved prose and corrections when available. An unaccepted
generated draft is not an author-style exemplar.

## 3. Give each paragraph a primary reasoning purpose

For literature-dependent sections, first distinguish the scientific evidence
needed for coverage from the smaller set of whole-paper writing exemplars.
Identify the claims, major research strands, nearest syntheses and contrary or
qualifying findings the section must address. Retrieve across those gaps and
synthesize their actual findings before drafting. Reusing a few familiar
papers does not establish coverage. Apply an explicit author/project citation
target to distinct sources, not repeated citation markers; do not create a
universal count or add irrelevant references. In delivery notes, distinguish
source checks, argument assessment and unresolved coverage. A mechanical
reference check or a self-reported judgment is not independent quality evidence.

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

Keep claims near their evidence. Lead with the research object and the strongest
supported finding or reasoning step. Attach a necessary boundary to the claim
it qualifies, avoiding repetition across paragraphs. Internal verification status
belongs in task notes unless it changes scientific interpretation. Match concrete
terminology and sentence rhythm to suitable published/author-approved examples.
Preserve uncertainty and adverse evidence without adding generic apologies or
hypothetical objections.

When drafting from development documents, data dictionaries, analysis notes, or
execution logs, treat them as evidence and provenance sources. Their convenient
engineering vocabulary may remain in those documents; manuscript prose requires
an explicit conversion from the underlying scientific meaning:

- Recover the research object, population, variable, operation, and evidence
  status behind each shorthand before writing the sentence. Use the mapped
  academic terms in a scientific argument; do not copy the working-document
  sentence structure or merely replace its nouns with scholarly-sounding words.
- Express substantive content as a method, finding, interpretation, or supported
  limitation. Describe necessary coding or computational procedures by their
  reproducible scientific operations in Methods or SI. Keep purely administrative
  status, scheduling, file handling, and revision history in working records.
- Make conversions context-specific: a ratio's "分母" can be expressed as the
  defined population or number of eligible observations; "UNKNOWN" can become
  "现有证据不足以判定" only when that is its documented meaning. These are not
  global replacements. Preserve counts, inclusion rules, missingness, variable
  definitions, uncertainty, and the strength of the original evidence.
- Resolve ambiguous meanings from the source before conversion; report any
  consequential unresolved ambiguity separately. Do not turn a completed review
  task into evidence of independent validation, or a tentative label into an
  established scientific category through academic wording.

## 5. Calibrate verbs to evidence strength

`show` / `demonstrate` need strong direct evidence. `suggest` / `indicate` are for trend-level or indirect evidence. `may` / `could` are for plausible but unverified mechanisms.

## 6. Remove unsupported novelty and universal claims

Sweep for `first`, `unique`, `unprecedented`, `comprehensive`, `complete`, `always`, `never`. Replace with bounded claims or delete.

## 7. Check paragraph flow and manuscript meaning

- One paragraph, one message.
- Make the paragraph's purpose clear; a topic sentence is useful, but a needed
  observation, comparison or transition may lead when it improves the argument.
- Each subsequent sentence has an explicit relation to the previous one (cause, comparison, restriction, example).

For full reverse-outlining, open `references/paragraph-flow.md`.

Before delivery, read the actual prose, headings, and captions as a scientific
reader without access to the project's working records:

- Keep sentences that explain the research question, method, finding,
  interpretation, or a limitation that changes what can be concluded.
- Remove internal work status, local file/version identifiers, and editing or
  verification narration from the manuscript; retain them in author notes only
  when needed. When a sentence mixes work status with a scientific limitation,
  keep the limitation and express its consequence directly. For example,
  "复核任务已结束，但分类准确性尚未经独立验证" becomes
  "分类准确性尚未经独立验证" when that limitation is supported.
- Preserve sample definitions, comparison populations, missing-data treatment,
  uncertainty, and reproducibility-critical methods. Decide by function, not a
  word blacklist: a denominator may need defining in Methods, but repeatedly
  invoking "分母" does not explain a study's contribution. State the population
  and comparison in reader-facing terms where possible, without changing the
  quantity being estimated. Place necessary implementation detail in Methods
  or SI according to its scientific role.

Revise the affected sentences and check their meaning against the evidence
before returning them. Numerical, citation, or file-consistency checks do not
establish that this manuscript check has passed.

## 8. Return the clean prose

Use `output-format.md`. Keep material unresolved issues and any requested
explanation or audit outside the manuscript; do not append routine planning
blocks to a prose request.

## 9. Revise by targeted edit, not full rewrite

Infer the revision scope from the user's feedback. A local correction calls for
a local edit; rejection of the overall premise or story may require the
authorized section to be rebuilt. Preserve accepted passages where compatible
with the requested change.

- For a local request, change the affected passages and necessary dependencies
  within scope; retain unrelated accepted prose.
- When restructuring is already requested, execute it within the authorized
  scope. Ask only if it requires an unresolved scientific decision or expansion
  beyond that scope, not for routine paragraph-order choices.
- Keep the Terminology Ledger (step 1b) stable across revisions unless the user changes a term; never let a revision reintroduce a variant of a locked term.
- After revising, re-run only the checks relevant to what changed (steps 5-7), not the whole workflow.
- If the user's redirection reveals the original premise was wrong, return to the confirmation gate (step 3b) instead of patching prose on a broken premise.
- Every proposed addition triggers the main-text deletion check: identify the
  new sentence's function, find existing text with the same function, and prefer
  replacement or compression before appending. Re-run the paragraph necessity
  and claim-repetition checks after the edit.
