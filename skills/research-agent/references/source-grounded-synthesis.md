# Source-grounded scientific synthesis

Evidence support for `ars-academic-writing`, not a separate writing owner.
Use for literature-supported manuscript arguments, not language-only edits.
This is a small local adaptation of research ideas, not an implementation of
OpenScholar or PaperQA2 and not a journal-style template.

Start from the question the reader needs answered. In the closest original
papers, recover the scientific problem, the finding that changed understanding,
how the evidence supports it, and the conditions under which it applies.
Method categories can help comparison but must not replace these relationships.

Use question-conditioned retrieval: seek evidence that distinguishes plausible
answers, including contrary and qualifying findings when relevant. A larger
corpus or a high retrieval score is not a stronger argument. Read beyond the
retrieved fragment when the necessary comparison or limitation is elsewhere.
Keep enough source context to avoid attributing a review's recommendation to
an empirical result.

Synthesize across studies before treating their statements as premises of the
manuscript. Explain which apparent differences arise from tasks, measurements,
data or study conditions; leave disagreements unresolved when the evidence
does not settle them. Distinguish established results, supported interpretation
and open questions. Do not fabricate a controversy to make a story dramatic.

Connect the author's actual evidence to the literature question. An Introduction
should make the question consequential and prepare the answer the Results can
support. For descriptive or evidence-mapping work, explain the knowledge gained
by the comparison without promising causal explanation, performance gains or
practical prescriptions that were not established.

When reviewing a draft, identify the particular claim, missing comparison or
unsupported inference that prevents the argument from working. Retrieve or
reread only what could resolve that defect, then revise the affected reasoning.
Do not run an open-ended self-critique loop or treat changing adjectives as
resolving a scientific objection. If no supported argument emerges, explain
the missing scientific premise separately; do not disguise it as finished prose.

Before delivery, check that the original sources support the attached claims
and that the literature motivation matches the author's results. Preserve
the author's scope and the uncertainty needed to interpret the findings.
There is no prescribed paragraph count, transition vocabulary, number of
citations or mandatory rhetorical escalation. Keep source checks out of the
clean manuscript unless they are part of its scientific content.

## Design sources and limits

- [OpenScholar official implementation](https://github.com/AkariAsai/OpenScholar):
  relevant-passage use, feedback-directed evidence retrieval and citation
  attribution. See `src/open_scholar.py` and `src/instructions.py`.
- [PaperQA2 official implementation](https://github.com/Future-House/paper-qa):
  question-conditioned evidence gathering and source-grounded answering. See
  the algorithm documentation and `src/paperqa/agents/tools.py`.

Other AI-for-Science systems are discussed in maintenance documentation, not
imported as writing requirements. An external benchmark score is neither a
local acceptance threshold nor proof that a mechanism has been implemented.
Traceability supports checking; it does not establish that the inference is valid.

OpenScholar/PaperQA2 design-source review: 2026-09-22. Scope corrected 2026-09-28.
Neither source establishes that these adapted instructions yield submission-grade
narratives. No external code, model, corpus or prompt text is imported. Keep the
existing local corpus and author-controlled evidence; external runtimes need a
separate installation and data-handling decision.
