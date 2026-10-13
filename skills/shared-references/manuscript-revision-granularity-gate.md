# Manuscript Revision Granularity Gate

## Purpose

This gate prevents proof, minor-revision, reviewer-response, citation, and other targeted manuscript edits from being implemented as unnecessary paragraph- or field-level rewrites. It applies to clean manuscripts, marked copies, Word/DOCX Track Changes, LaTeX, Markdown, and plain-text revisions.

The governing rule is:

```text
Use the smallest defensible edit unit:
character/token -> phrase -> clause -> sentence -> paragraph -> section.
Escalate only when the smaller unit cannot correct the identified problem and the larger scope is authorized.
```

Providing a whole paragraph as context does not authorize replacing the whole paragraph.

## Revision-Mode Defaults

| Revision mode | Default edit unit | Maximum without additional approval | Paragraph/section rewrite |
|---|---|---|---|
| Production proof / author proof | character, token, or phrase | one locally determined sentence only when unavoidable | prohibited unless classified as a scientific decision and approved by the author/editor |
| Minimal / minor / editorial revision | token, phrase, or clause | the specifically identified sentence | requires explicit user authorization tied to a reviewer/editor request |
| Major / structural revision | sentence or paragraph | the declared editable surface | allowed only inside the declared structural scope |
| Explicit rewrite | paragraph or section | the explicitly authorized section | allowed, while all frozen material remains protected |

When the revision mode is not stated, infer the narrowest safe mode from the request. Existing accepted text, proof text, specific reviewer comments, named sentences, citation corrections, and metadata fixes default to local correction, not rewrite.

## Required Scope Contract

Before editing, record the smallest usable form of:

```text
Revision mode:
Canonical source:
Working artifact:
Reviewer/editor/issue ID, if any:
Target locator:
Target sentence(s), citation(s), field(s), or object(s):
Editable span:
Protected context:
Maximum edit unit:
Allowed collateral edits:
Track Changes / marked-copy requirement:
Citation-manager source of truth, if applicable:
Reference-manager linkage state: embedded / traveling-library-only / external-library-linked / plain-text / unknown
Stop condition:
```

For a short edit, this may be one compact line. For a paragraph with sentences `S1-S5` when only `S2` and `S4` are defective, `S2` and `S4` are editable; `S1`, `S3`, and `S5`, their order, citations, and formatting are protected.

## Editing Rules

- Use character-, token-, phrase-, clause-, or sentence-level patches inside the declared editable span.
- Preserve all non-target sentences verbatim unless a separately documented dependency makes a local bridging edit necessary.
- Do not send a whole paragraph for unconstrained regeneration when only selected sentences are editable. Full-paragraph context may be supplied only with explicit protected-span markers and a local-patch output contract.
- Do not improve nearby prose, terminology, transitions, citations, or formatting merely because it is visible.
- If the requested correction cannot be made within the maximum edit unit, stop and propose a scope escalation; do not silently rewrite the containing paragraph.
- A paragraph or section rewrite must have an explicit reason, linked reviewer/editor instruction or author decision, and a declared replacement boundary.

## Word / DOCX and Field-Aware Rules

- For Track Changes, apply deletions and insertions only to the exact changed range. Preserve the paragraph container, paragraph properties, unaffected runs, styles, bookmarks, hyperlinks, comments, equations, citations, and field codes.
- Do not replace `Paragraph.Range.Text`, `paragraph.text`, an entire `<w:p>`, a section range, or another enclosing block when the authorized change is smaller.
- Do not assign an entire citation or bibliography `Field.Result.Text` when only an author-year suffix, punctuation mark, volume, issue, page/article number, DOI, or other subfield is changing. Patch the exact visible span while preserving the field code.
- Before changing citation or bibliography metadata, freeze the reference-manager source of truth: embedded field code / Traveling Library, external EndNote library, verified export, or plain text. Do not relink, refresh, or reconstruct fields from an assumed, partial, or unavailable library.
- An EndNote or other reference-manager refresh may regenerate a complete citation or bibliography field. If the refresh produces coarse redlines, keep the reference-manager-linked clean master separate from a reviewer-facing granular marked copy, or obtain explicit approval for the broader field regeneration. Do not present a whole-field refresh as a token-level correction.
- After any field-aware change, verify field count/type, field-code identity, displayed result, citation-reference mapping, save/reopen behavior, and—when the authoritative library is available—one controlled refresh round trip. If the external library is unavailable, keep fields locked, record the limitation, and do not claim reference-manager round-trip integrity.
- Word Compare is a verification or marked-copy aid, not proof of acceptable revision granularity. A compare result that re-inserts unchanged sentences or whole paragraphs fails this gate.

## Track Changes Fidelity QA

Before delivering a marked manuscript:

1. Map every insertion and deletion to an authorized target locator.
2. Confirm protected sentences and protected objects are unchanged in accepted text and formatting.
3. Inspect whether any revision crosses a target-sentence boundary, contains a paragraph mark, or re-inserts unchanged text.
4. Confirm that citation/reference field codes and other protected Word objects remain intact when applicable.
5. Confirm the declared citation-manager source of truth and field linkage state; where the authoritative library is available, complete the controlled refresh/save/reopen round trip.
6. Confirm that formatting-only revisions are absent unless explicitly requested.
7. Open/read back the DOCX revision structure and, when layout or field behavior matters, verify it with Word or an equivalent real document engine.

The gate passes only when every substantive revision maps to an authorized editable span and no protected text is included in a deletion/insertion pair.

## Failure Codes

| Code | Meaning | Required action |
|---|---|---|
| `TARGET_SPAN_AMBIGUOUS` | The intended sentence/range cannot be uniquely located | stop and resolve the locator |
| `REVISION_SCOPE_DRIFT` | Accepted text or formatting changed outside the editable span | revert the out-of-scope change and reapply locally |
| `PARAGRAPH_REWRITE_NOT_AUTHORIZED` | A paragraph/section was replaced without the required scope authorization | reject the patch and redo at token/phrase/sentence level |
| `PROTECTED_SENTENCE_TOUCHED` | An unchanged sentence was included in tracked deletion/insertion | reject the marked copy and regenerate locally |
| `FIELD_RESULT_WHOLESALE_REPLACEMENT` | A whole citation/bibliography/Word field result was replaced for a subfield correction | patch the exact span or separate clean master from granular marked copy |
| `CITATION_SOURCE_OF_TRUTH_UNRESOLVED` | The authoritative embedded/external/plain-text citation source is unknown or conflicting | stop field refresh/relinking and resolve the source boundary |
| `REFERENCE_MANAGER_ROUNDTRIP_UNVERIFIED` | Field code/result/linkage was not checked through the available save/reopen/refresh path | run the controlled round trip or record the unavailable-library blocker |
| `WORD_REDLINE_COARSE` | Track Changes or Word Compare represents a local edit as broad replacement | do not deliver; regenerate the redline |
| `PROOF_SCOPE_ESCALATION_REQUIRED` | A proof correction would exceed local correction or change scientific content | obtain author/editor decision before editing |
| `TRACK_CHANGES_UNVERIFIED` | Revision structure was not inspected after DOCX editing | run revision-structure readback before delivery |

## Handoff Contract

When a reviewer-driven revision coordinated by `nature-response` needs `nature-writing`, `nature-polishing`, `nature-paper-format`, or a DOCX execution tool, pass the scope contract, editable spans, protected context, maximum edit unit, and any citation-manager source/linkage state. Downstream skills may return a scope-escalation proposal, but may not expand the editable surface or change the reference-manager source of truth themselves.
