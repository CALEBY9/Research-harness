# Equation Semantic Integrity Gate

This shared contract applies to formula-bearing manuscripts during revision, verification, submission QA, and production proofing. It prevents equation objects, adjacent definitions, notation tables, executable models, supplements, and proof output from drifting apart.

## Core rule

Do not use prose similarity or visual rendering as evidence that an equation is correct. Exact symbol identity, first-use definition, numbering, units, source-model mapping, and artifact freshness must be checked separately. A formula or definition that cannot be parsed or verified is `MANUAL_REQUIRED`, never an automatic pass.

The division of responsibility is:

- deterministic checks decide whether symbols, numbers, locators, and hashes match;
- the language model diagnoses a flagged mismatch and drafts the smallest correction;
- the author or model owner decides scientific forks, parameter choices, and changes that may affect results;
- the editor/publisher decides post-acceptance scientific corrections that exceed obvious proof repair.

## Required frozen inputs

For a submission-grade revision or proof audit, freeze the exact paths and SHA-256 values of every in-scope artifact:

- current editable manuscript or accepted author source;
- production proof PDF/HTML when available;
- supplement/Appendix;
- executable model, code, configuration, or algorithm source when equations describe implementation;
- equation ledger and symbol registry;
- figures/tables whose labels, time axes, or values depend on the equations.

Conflicting canonical paths or a stale artifact hash are `BLOCK`.

## Equation ledger contract

Use one ledger row per displayed equation, including auxiliary displays and sub-equations. The machine-readable JSON contract is enforced by `scripts/equation_semantic_gate.py`.

Minimum fields:

| Field | Requirement |
|---|---|
| `id` | Unique printed equation number such as `16`, `17b`, or `A3` |
| `display_index` | Physical order in the artifact, contiguous from 1 |
| `formula_symbols` | Exact canonical variables, parameters, indices, and sets used in the equation; omit operators/functions |
| `local_definitions` | Symbols actually defined in the immediately associated explanatory text |
| `definition_exemptions` | Exceptional first-use definitions located elsewhere, each with a reason and exact locator; forbidden in strict-local mode |
| `formula_locator` / `definition_locator` | Page, paragraph, bookmark, XML/object, or other stable source locator |
| `formula_text` or `formula_sha256` | Audited formula content or its normalized fingerprint |
| `definition_text` or `definition_sha256` | Audited explanatory content or its normalized fingerprint |
| `model_bound` / `model_locator` | Whether the equation describes executable behavior and, if so, the exact code/model/config locator |
| `parse_status` | `PARSED` or `MANUAL_REQUIRED` |

The symbol registry must give every canonical symbol one meaning and one non-empty unit/dimension entry, including `dimensionless` where appropriate. Deprecated spellings belong only in `aliases`; an alias appearing in a formula or definition is `BLOCK`.

## Deterministic acceptance rules

For equations in physical order:

1. Display count equals the expected count; every display has one unique number and one unique physical index.
2. Every formula symbol resolves to the canonical symbol registry.
3. Every symbol at first appearance is defined immediately after that equation. A project may disable strict-local mode only with an exact alternative locator and reason.
4. The local definition block contains no symbol absent from the associated equation.
5. Repeated definitions, when retained, cannot contradict the registered meaning or unit.
6. Every executable/model-bound equation has an exact model/code/config locator; a semantic mismatch is `BLOCK`, even if the equation renders correctly.
7. Every equation cross-reference resolves to a declared equation ID.
8. Any change to a formula, adjacent definition, notation table, equation number, executable model, or accepted-source hash invalidates the prior equation-ledger pass and requires re-audit.
9. Word/MathType/OMML/OLE extraction counts and PDF rendering are structural evidence only; they cannot substitute for this semantic gate.

Verdicts are `PASS`, `BLOCK`, or `MANUAL_REQUIRED`. Do not downgrade missing definitions, extra local symbols, deprecated aliases, unnumbered displays, invalid cross-references, stale hashes, or model contradictions to stylistic warnings.

## Production proof correction mode

Once a manuscript is accepted or in production proof, first classify each proposed correction:

| Class | Definition | Default action |
|---|---|---|
| `PUBLISHER_ERROR` | Accepted author source is correct but production changed, dropped, substituted, or damaged it | Restore the accepted source and document the source/proof difference |
| `OBVIOUS_AUTHOR_ERROR` | A unique correction is fixed by the accepted equation, locked model, notation registry, or undisputed source and does not change model behavior or reported results | Apply the smallest local correction and disclose it to production/editorial staff |
| `CLARITY_CORRECTION` | Adds a missing first-use definition, expands an abbreviation, fixes a locator, or removes an equation-external explanation without changing scientific meaning | Apply narrowly; do not add new evidence or claims |
| `SCIENTIFIC_DECISION_REQUIRED` | Two or more scientifically plausible definitions exist, or manuscript/source/model disagree about the intended mechanism | Do not silently choose; request author decision and editor approval |
| `MODEL_OR_RESULTS_CHANGE` | Correction would alter parameters, equations, simulation behavior, analysis, figures, tables, or conclusions | Hold; rerun and resynchronize only with explicit editorial authorization |

An “obvious” proof correction must have one authoritative basis, be local, preserve model/results, and introduce no new evidence. If any condition fails, it is not obvious.

Proof mode must compare the accepted source with the exact production artifact. A source-source hash match does not prove scientific correctness, and a visual proof inspection does not prove mathematical identity.

## Proof-stage boundaries

Allowed narrow corrections include restoring a missing multiplication sign, correcting a uniquely determined variable name, defining a symbol at first use, removing stale aliases from the wrong `where` block, fixing an unambiguous equation/citation/date reference, removing production placeholders, and calibrating a validation statement to the already reported metric.

Do not silently use proofing to choose between competing model equations, change a policy parameter, recalibrate a model, remove an unfavorable validation metric, replace results, or redraw a substantive figure. Mark these `SCIENTIFIC_DECISION_REQUIRED` or `MODEL_OR_RESULTS_CHANGE` and escalate.

## Required handoff

A formula-bearing manuscript may proceed only when:

- all displayed equations are represented in the ledger;
- unresolved missing/extra/alias/numbering/cross-reference/model mismatches are zero;
- the ledger hashes match the current frozen artifacts;
- all `MANUAL_REQUIRED` rows have an author-side inspection record;
- proof corrections are classified, and no scientific-decision/model-results item is silently marked `APPLY`.
