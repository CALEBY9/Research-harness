# Clean-Final Language Gate

Use this reference whenever a manuscript, figure/table caption, graphical abstract, response-package clean copy, or submission-ready DOCX is being reviewed, polished, formatted, or packaged.

## Purpose

Final scholarly artifacts must contain reader-facing academic prose only. They must not contain authoring-process language, reviewer-response language, before/after wording, internal workflow labels, local file names, tool names, parser names, runtime notes, or change-log phrasing.

This gate is not ordinary style polish. If it fails, the document is not clean-final.

## Generalization and locality boundary

Keep only cross-project risk families, decision rules, and acceptance tests in this shared gate. Do not add journal identifiers, local paths, manuscript-specific equation or table numbers, project variable names, dataset names, scenario labels, run labels, parameter values, or one project's internal codes.

Project-specific blocked terms belong in a project-local denylist stored with that project's QA records. Pass that file to the scanner at run time; do not copy its contents into this shared gate or an owner skill. A local observation may enter the shared workflow only after it has been rewritten as a domain-neutral failure condition, evidence requirement, acceptance test, or stop rule.

## Scope

Apply to:

- title, abstract, highlights, keywords
- manuscript body, Methods, Results, Discussion, Conclusions
- figure/table captions, table cells, figure text, axes, legends
- graphical abstract and submission package notes intended for readers
- clean manuscript versions in revision packages

Do not apply the same ban to response letters, marked copies, revision matrices, change logs, audit reports, code comments, artifact manifests, or supplementary reproducibility notes, as long as those files are not presented as the clean manuscript.

## Prohibited Phrase Families

### Revision and reviewer-response leakage

Search for and remove or relocate:

```text
reviewer-response
reviewers' concern
reviewer concern
reviewer questions
in response to the concern
according to the reviewer
as requested by the reviewer
revised audit
Revision implemented
was revised to
revised model
revised manuscript
new and revised
```

Allowed context: `revised policy`, `revised regulation`, or a cited official policy title may remain if it is the research object rather than the author's revision process.

### Before/after or original-to-final process framing

Search for and remove or recast:

```text
based on the original
original model
original formulation
original manuscript
legacy variable
original-to-calibrated
baseline-to-calibrated
are replaced by
is replaced by
replaces the original
retired from
newly introduced
introduced only
```

Preferred reader-facing replacements:

```text
pre-expansion policy scope
baseline calibration
calibrated model component
sector-specific accounting module
parameter bridge
model constraint
diagnostic traceability
```

Allowed context: `original data`, `original source`, or `original issuance scope` may remain only if it is a scholarly/policy object. Prefer `pre-expansion issuance scope` when contrasting policy stages.

### Tool, parser, runtime, and implementation leakage

Search for and remove or recast:

```text
implemented model
implementation-level
in implementation
active runtime model
runtime coverage
accepted runtime outputs
parser output
GUI export
script generated
workflow
workspace
Internal QA
artifact render
Word-native PDF QA
```

Preferred reader-facing replacements:

```text
the model specifies
the calibrated model sets
the model constraint is
reported model outputs
independent model-export checks
diagnostic checks
```

### Placeholders, internal codes, and local locators

Search for:

```text
TODO
TODO_CITE
remove before submission
before submission
Draft positioning
Provisional
machine-simulated
local file or path
internal field, stage, run, dataset, or version label
```

Any remaining author-side code must be mapped through a `Publication Terminology Map` before entering the clean manuscript. Use placeholders such as `{internal_code}` and `{reader_facing_term}` in the shared workflow; keep the actual mappings in the project record.

## Required Scan Protocol

1. Extract text from the full manuscript, including tables and captions. For DOCX, do not rely only on visible paragraph extraction if formulas, text boxes, or embedded figures may carry text.
2. Extract or OCR figure text, axes, legends, and table images when figures are final submission assets.
3. Run a high-risk phrase scan using the domain-neutral families above. Put project-specific terms discovered during review in a project-local denylist and load it at run time.
4. For DOCX clean copies, also check for residual Word comments and tracked-change structures. Any `<w:comment>`, `<w:commentReference>`, `<w:ins>`, `<w:del>`, `<w:moveFrom>`, or `<w:moveTo>` element is a clean-final blocker unless the file is explicitly a marked-up review copy.
5. Classify hits:
   - `REMOVE`: authoring/revision/process leakage.
   - `RECAST`: legitimate concept expressed with process wording.
   - `ALLOW_WITH_REASON`: phrase has a scholarly or policy meaning, not an author-process meaning.
6. Rewrite `REMOVE` and `RECAST` hits as final scholarly prose.
7. Re-scan. Clean manuscript and display items must have 0 unresolved high-risk hits.
8. Render or otherwise visually verify the edited artifact when it is a DOCX, figure, table, or submission package file.

## Runnable Scanner

Use the dependency-free scanner before declaring a clean manuscript, main display item, or submission package ready:

```powershell
python <skills-root>\shared-references\scripts\clean_final_scanner.py `
  <artifact-or-folder> `
  --extra-term-file <project-qa-folder>\clean_final_project_terms.txt `
  --out-csv <analysis-or-qa-folder>\clean_final_scan.csv `
  --out-md <analysis-or-qa-folder>\clean_final_scan_report.md
```

The scanner reads `.docx`, `.pptx`, `.xlsx`, `.txt`, `.md`, `.csv`, `.tsv`, `.tex`, `.svg`, `.xml`, `.html`, `.json`, `.yml`, and `.yaml` files with standard-library extractors. `--extra-term-file` accepts one literal project-local term per non-empty line; lines beginning with `#` are comments. Repeat `--extra-term` for ad hoc literal terms. The scanner returns exit code `2` when unresolved high-risk hits are found. Use `--no-fail` only for exploratory triage, not for submission readiness.

The scanner is a gate, not a substitute for judgment. Each hit still needs a decision:

- `REMOVE`: author-process, toolchain, local-path, or placeholder leakage.
- `RECAST`: legitimate concept written in process language.
- `ALLOW_WITH_REASON`: phrase is a policy/scientific object rather than author-process language.

## Completion Record

For submission-grade work, record a compact gate result:

```markdown
## Clean-Final Language Gate
- Artifact:
- Scope checked:
- High-risk hits before:
- High-risk hits after:
- Allowed-with-reason hits:
- Visual/render QA:
- Verdict: PASS / FAIL
```

Do not put this record inside the clean manuscript. Put it in a review report, revision matrix, submission checklist, or project analysis folder.
