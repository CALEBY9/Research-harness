# KB-to-Manuscript Evidence Bridge

Use this reference when the requested writing uses multiple papers from a
selected local corpus. It does not apply to wording-only edits, routine index
checks, or results supported entirely by the author's own data.

## Current owners and continuation

`literature_kb` selects the registered corpus/run and returns locatable
candidates. `research-agent` coordinates retrieval and source reading;
`nature-writing` owns substantive synthesis and manuscript drafting,
including checking the original passages that support its claims. Use
`nature-paper-card` when a paper needs a full deep read or a Paper Card, not
automatically for every citation. Use `lit_synthesis` for an actual systematic
review, meta-analysis or formal synthesis task.

A request to write from the corpus authorizes this bounded retrieval-to-writing
continuation. Reuse supplied verified evidence and proceed within that scope;
do not stop merely to obtain another handoff approval. Research Agent handles
lawful source retrieval and any needed search beyond the corpus. Neither adds
authority to rebuild an index, change
the research question, or publish/send material.

Research Agent distinguishes substantive review from wording-only revision.
Do not run the retired paper_*
owner chain or require separate outline, review and polishing stages for an
ordinary requested paragraph.

## Retrieval and original evidence

Keep the corpus/run, research question, actual query variants and residual
coverage gaps in the existing task notes or Retrieval QA Dossier. A ranking,
chunk ID, PDF hash or snippet alone does not establish claim support.

For each source actually used, read the necessary original page/section and
retain its identity, locator and supporting text. Expand beyond the first
retrieved fragment when methods, results or limitations needed for the claim
are elsewhere. Verify citation metadata against the original or authoritative
metadata; a journal header is not a paper title.

Reuse existing evidence IDs. When a structured `KB_EVIDENCE_PACK` is useful,
its minimal content is: paper identity, original locator, evidence, design and
scale, uncertainty, and relation to the proposed claim. Relations remain
`SUPPORTS`, `CONTRADICTS`, `QUALIFIES` or `CONTEXT_ONLY`.
`UNVERIFIED` evidence cannot license a factual assertion. A source-identity
or content conflict must be resolved; disagreement between verified studies can
itself support an accurately bounded account of that disagreement.

## Cross-paper synthesis and drafting

Organize the answer around the writing question, not a list of papers. Compare
what the studies establish, why findings may differ, which boundaries matter,
and what remains unanswered. Do not infer consensus or a field-wide gap from
paper count, retrieval rank, majority direction, or a search returning no hits.

For a formal synthesis or complex chapter, reuse or create only the needed
`CROSS_PAPER_SYNTHESIS_MATRIX` rows: question, recurring evidence, disagreement,
context/heterogeneity, evidence IDs, residual gap and manuscript role. Preserve
`CONSENSUS`, `CONTESTED`, `CONTEXT_DEPENDENT` and `INSUFFICIENT`
distinctions. An ordinary paragraph can keep the same trace in compact notes;
it does not require a new directory, ledger, full Paper Card per source or
fixed number of tables.

`nature-writing` drafts only the supported or explicitly bounded propositions.
Verify claim support against the original evidence and preserve author authority. Unsupported
central claims remain `HOLD_FOR_EVIDENCE` or `REJECT_OR_REMOVE`; continue
unaffected writing where possible rather than hiding uncertainty in fluent prose.

Keep evidence selection separate from style calibration. Follow the actual
journal/article type or thesis requirements, using relevant exemplars when
available. An unknown target journal does not block a scientific working draft.

## Verify the requested deliverable

Trace the central literature-dependent claims back to the original sources and
check citation attachment, study boundaries, numerical/causal wording and
cross-paragraph consistency. Review only what changed; keep evidence notes out
of the clean final. Retrieval relevance and model self-scores do not certify
scientific truth, publication quality or whole-corpus completeness.

Report a concrete unresolved gap using existing statuses where applicable:
`KB_CORPUS_UNBOUND`, `KB_RETRIEVAL_QA_INCOMPLETE`,
`KB_EVIDENCE_PACK_INCOMPLETE`, `KB_SYNTHESIS_UNRESOLVED`,
`KB_CLAIM_TRACE_BROKEN`, or `KB_STYLE_PROFILE_UNRESOLVED` for an explicitly
requested target-style claim. A missing process form is not itself missing
scientific evidence.
