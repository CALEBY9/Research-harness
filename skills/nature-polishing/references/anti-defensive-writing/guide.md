# nature-polishing: anti-defensive-writing mode

Use this mode only for its requested deliverable. Its owning skill is `nature-polishing`.
Resolve mode-local manifest, scripts, static fragments and references from
`MODE_DIR`, the directory containing this guide. Select only the needed
mode; this resource is not a separate skill or a mandatory next stage.

# Anti-Defensive Academic Writing

This is a conditional repair of an existing manuscript passage. It improves
rhetorical posture without changing the scientific result or deciding what
the paper should claim.

## Required input and position

Accept supplied author prose directly; no preceding drafting call is required.
For a combined drafting-and-repair request, repair the requested draft after
the writing owner has produced it. Reuse the available claim, evidence, scope,
section and genre boundaries; do not start a second independent edit cycle.
For revision correspondence, apply this mode only to the manuscript passage,
not the reviewer-facing letter. It is not mandatory for every draft.

The parent's selected editing boundary controls this reference. In LANGUAGE_ONLY,
keep modality, hedges, paragraph roles and order locked: repair rhetorical
wording only where those invariants hold. Reordering a lead or consolidating
evidence qualifications is allowed only within an authorized bounded rewrite.
Preserve the affected wording and flag a real boundary conflict rather than
using this mode to widen the task. Return clean prose to the caller.

## Protected scientific content

Preserve facts, numbers, units, terminology, citations, comparison sets,
measured quantities, sample and population definitions, time and spatial
bounds, evidence status, causal direction and claim strength. The evidence
ceiling is a limit, not permission to change the passage's certainty.

Never hide or neutralize a negative finding, contradiction, rival explanation,
failure condition, ethical constraint, method limitation, or mandatory
disclosure that changes interpretation. Do not switch metrics, baselines,
subgroups, outcomes, or comparison frames because another framing looks more
favourable. Do not restructure the dominant story or choose a new main claim
without an explicit author decision.

## Sentence-function pass

Classify each suspected defensive passage by function before editing:

| Function | Action |
|---|---|
| `RHETORICAL_DEFENCE` | Remove apology, self-deprecation, or an answer to a hypothetical objection that adds no scientific information. |
| `DUPLICATE_QUALIFICATION` | Keep the qualification once beside the claim it bounds; delete only the redundant repetition. |
| `POSITIVE_SCOPE_CANDIDATE` | Restate a negative disclaimer as the exact positive study scope only when the two formulations are semantically equivalent. |
| `EVIDENCE_QUALIFICATION` | Preserve the uncertainty and, when its source is already known, state that source directly instead of stacking vague modal hedges. |
| `NEGATIVE_OR_RIVAL_EVIDENCE` | Preserve it and give it the placement required by its effect on the conclusion. Do not recast it as a favourable trade-off without evidence. |
| `METHOD_ETHICS_OR_GENRE_LIMIT` | Preserve it in the section and form required for valid interpretation, transparency, ethics, or journal compliance. |

A cue word is never an edit decision. Do not globally delete `may`, `might`,
`could`, `only`, `limited`, `however`, `although`, `可能`, `仅`, `局限`, or
similar terms. Determine what the sentence does in context.

## Revision priorities

Apply only the smallest changes permitted by the selected editing boundary:

1. Lead the paragraph with its strongest supported proposition.
2. Remove work-log chronology when the scientific argument, not the process,
   is the relevant content.
3. Replace negative self-description with a precise positive scope statement
   only when meaning and evidentiary strength remain unchanged.
4. Consolidate redundant hedges; retain the modality required by the evidence.
5. Keep each paragraph focused on one analytical job.

Do not add a stronger verb merely to sound confident. In particular, do not
upgrade association to causation, trend to significance, observation to
mechanism, planned work to completed work, or bounded performance to general
superiority.

## Final verification

Before returning the clean prose, check every material edit:

- claim strength and its evidence ceiling remain unchanged;
- every conclusion-changing boundary or adverse result remains visible;
- citations retain the same claim-support function;
- no new mechanism, explanation, evidence, limitation, or superiority claim
  was invented;
- removable rhetorical defence has been repaired within the selected boundary;
  a sentence that cannot be repaired without changing a locked scientific
  property remains intact, with the boundary conflict reported separately.

If the requested edit requires choosing the dominant claim, suppressing
material evidence, changing a comparison frame, or resolving a real scientific
ambiguity, preserve the affected passage and return that decision to the author.
Otherwise return only
the clean revised prose unless the user explicitly requests an audit or change
map.

Maintenance provenance is recorded in
[references/provenance.md](references/provenance.md); do not load it during an
ordinary manuscript pass.
