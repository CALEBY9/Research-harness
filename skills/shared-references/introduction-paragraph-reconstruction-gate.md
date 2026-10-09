# Introduction Paragraph Reconstruction Gate

Use this gate whenever an Introduction paragraph is substantively planned, drafted, rebuilt, or reviewed. It is a scientific-scope and argument-structure gate before `paper_polish`; it does not impose one journal's rhetoric, a fixed number of paragraphs, or a fixed number of sentences. For an explicitly language-only exact-span correction whose scientific scope and paragraph function are already stable, preserve the existing `paper_polish` or `paper_revision` route and do not force a full reconstruction map.

## 1. Start from a study-addressable endpoint

Before drafting, record:

```text
Paragraph ID:
Reader question answered:
Study-addressable endpoint:
Downstream claim / result / design link:
Admitted evidence and citations:
Foregrounded objects or mechanisms:
Excluded or deferred material:
```

Write the endpoint first, then build backward. The endpoint must be a question, limitation, or transition that the current study can estimate, test, compare, explain, or bound. Do not make a larger unanalysed issue the paragraph's apparent target merely because it is important or rhetorically vivid.

## 2. Opening problem-paragraph functions

For the first problem-framing paragraph, use this default functional chain unless the locked writing profile or exact article type requires another justified structure:

```text
FIELD_STAKE
-> RESOLUTION_OR_KNOWLEDGE_LIMIT
-> NECESSARY_CONTEXT_OR_PROXY_LIMIT
-> STUDY_ADDRESSABLE_QUESTION
```

- `FIELD_STAKE`: establish the concrete scientific or environmental problem without a generic importance slogan.
- `RESOLUTION_OR_KNOWLEDGE_LIMIT`: state what existing assessment or evidence cannot directly resolve.
- `NECESSARY_CONTEXT_OR_PROXY_LIMIT`: explain only what the reader needs to understand why the common scale, proxy, or summary measure is insufficient.
- `STUDY_ADDRESSABLE_QUESTION`: end on the dimensions the study actually evaluates, such as range, magnitude, timing, mechanism, contrast, or boundary.

These are functions, not sentence templates. They may be merged or split when the target profile and evidence justify it. The paragraph must still progress toward one exact research need rather than display rhetorical complexity.

## 3. Study-scope admission test

Every foregrounded object, mechanism, subgroup, infrastructure component, statistic, or citation must satisfy at least one condition:

1. it is directly measured, analysed, controlled, stratified, or otherwise tested in the study;
2. it is necessary to define the exposure, design, proxy, interpretation, or evidence boundary; or
3. it is explicitly bounded as context and does not imply that the study decomposes or attributes its separate effect.

If a detail would reasonably make a reviewer expect an analysis the paper does not perform, de-centre it, generalize it to the supported level, move it to a better location, or cut it. Do not let a prominent contextual example redefine the study question.

## 4. Citation and statistic admission

A citation or statistic earns main-text space only when it performs one of these roles:

- `ESSENTIAL_PREMISE`
- `EXACT_GAP`
- `DESIGN_OR_PROXY_RATIONALE`
- `INTERPRETIVE_BOUNDARY`

Specificity, recency, or numerical vividness alone is insufficient. Retain a well-supported citation when it is necessary for the exact argument even if the cited study is not replicated here; otherwise move or cut it rather than building the paragraph around it.

## 5. Terminology-debt test

For a coined abstraction, metaphor, compressed label, or newly imported construct, ask:

1. Is it defined?
2. Is it analytically necessary?
3. Is it reused later?
4. Is it clearer than stating the relation directly?

If the answer is no, prefer direct scientific language. Established technical terms required by the field or target profile are not prohibited, but ornament must not substitute for a concrete limitation or question.

## 6. Reader propulsion and deletion test

Each sentence must change the reader's state by establishing a needed premise, narrowing the unresolved problem, explaining a necessary limitation, or creating the next unavoidable question. Apply this audit:

```markdown
| Sentence / unit | Function | Link to exact study question | Measured, necessary, or bounded? | Citation role | Terminology debt | Decision |
|---|---|---|---|---|---|---|
```

`Decision` must be `Keep`, `Rewrite`, `Merge`, `Move`, or `Cut`. If removing a sentence does not weaken the route to the exact research question or a necessary evidence boundary, it should not remain in that paragraph.

## 7. Failure and handoff

Return `INTRODUCTION_SCOPE_MISALIGNMENT` when the paragraph foregrounds an unanalysed object, implies an unsupported decomposition or attribution, ends on a question the study cannot answer, or uses citations and terminology that displace the exact study need.

- `paper_outline` repairs the paragraph question, function chain, admission decisions, and downstream claim link.
- `paper_write` reconstructs authorized clean prose from that map; it does not preserve a misaligned sentence merely because it is accurate in isolation.
- `paper_review` verifies the scope, citation function, terminology debt, deletion test, and reader propulsion before `paper_polish`.
