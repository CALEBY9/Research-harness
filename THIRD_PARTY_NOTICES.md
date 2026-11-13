# Third-party provenance and licensing

Research Harness contains original adapters and separately licensed upstream
components. Original contributions are licensed under Apache-2.0 (see `LICENSE`),
as selected by the maintainer on 2026-11-13. This grant does not relicense any
third-party component, paper, image or example. Retain component notices.

The active distribution is declared in `skills/catalog.json`. ARS components
retain CC BY-NC 4.0 terms, so the entire bundle must not be advertised as an
unrestricted Apache-2.0 package. Review the selected components before reuse.

## ARS writing adaptation

- The former `skills/ars-academic-writing/` was a local adaptation of selected argument,
  Introduction rhetoric and drafting guidance from academic-research-skills.
- Upstream copyright (c) 2026 Cheng-I Wu; CC BY-NC 4.0, not Apache or MIT.
- Redundant source files were removed on 2026-11-13. Commit, links,
  modifications, license and warranty notice remain in the
  [historical provenance](https://github.com/CALEBY9/Research-harness/blob/d9fcb8cbf52f3a8e569d849c66bcf9ca5a17d4bc/skills/ars-academic-writing/references/provenance.md).
- This is not the full suite or an upstream-endorsed installation.

## ARS selective research planning

- `skills/academic-research-suite/` is a local Chinese adaptation of selected
  question-development, literature-investigation, synthesis and framework
  methods from `Imbad0202/academic-research-skills-codex` at commit
  `8d6a1f856ee3da9d3a5e2b7f292b3dfe72b592c5` (inspected 2026-10-25).
- That adapter identifies vendored ARS 3.23.1 from `Imbad0202/academic-research-skills`
  at `4c5449017f46eb64d112a301d4817d22c7c9f3d9`.
- Copyright (c) 2026 Cheng-I Wu; CC BY-NC 4.0. The original license is preserved
  as `skills/academic-research-suite/LICENSE`. Selected source paths and local
  changes are mapped in `references/provenance.md` under that skill.
- Only the selective planning entry is active. Upstream writing/review/full
  pipeline workflows, scripts, hooks and optional runtime are not bundled or
  activated; the earlier `ars-academic-writing` adaptation is removed from the
  current tree and remains inactive.

## Nature Skills

- The 18 directories below were retired on 2026-09-22 and restored on 2026-10-12
  at the author's explicit request, from this repository's published commit
  `b5b8e082522409aea0cb8db80a7afc2e5c086867`. They are current runtime dependencies.
- Source: https://github.com/Yuan1z0825/nature-skills
- License: Apache License 2.0; original root license copied to `skills/NATURE_LICENSE`.
- Scope: the initial 17 `nature-*` directories imported from the Nature installation,
  plus `nature-proposal-writer` (originally `researchwrite`). Three imported modules
  are now conditional resources under retained owners; see `docs/nature_upstream.json`.
  The conceptual-prompts mode under `nature-figure` is a separate local adapter.
- These are locally enhanced installed copies, not a pristine upstream release.
  See `docs/import_manifest.json` for the initial imported files.
- Embedded assets/tools may have additional LICENSE/NOTICE files; those remain
  in their original imported directories. Root Apache metadata alone does not
  establish rights for every image or embedded third-party example.
- The `nature-figure/assets/figures4papers` reference collection has no confirmed
  redistribution license in the retained upstream notice. It is excluded from
  installation and no longer tracked in the current source tree. Existing local
  files are retained; older Git history has not been rewritten. This repository
  grants no rights over that collection.
- On 2026-10-12, scoped updates from upstream commit
  `e605b35611ab2849af46d0cf7831aefdcf85be07` imported
  `nature-shared/core/discussion-argument-language.md` verbatim and applied the
  `nature-academic-search/scripts/format-converter.py` retry-zero correction.
  Local router, language/thesis support and other adaptations were preserved.
  This does not claim adoption of that entire upstream release.
- Scientific-positioning and conceptual-handoff references are local behavior
  guidance for observed integration gaps; they do not import the complete ARS
  method text or change the separate ARS component's CC BY-NC license.

## Humanizer

- Academic source: https://github.com/AIScientists-Dev/academic-humanizer
- Installed on 2026-10-14 at commit `94b88b23703bed7df507acae7d6d5876209a0cdf`
  (0.3.3), with MIT license retained at `skills/nature-polishing/references/academic-humanization/LICENSE`.
  README, examples and assets retain upstream provenance; local metadata,
  bilingual task routing and meaning-preserving constraints are documented in
  `docs/humanizer_task_routing.md`. Examples do not supply manuscript evidence.

- English source: https://github.com/blader/humanizer
- The independent English skill was retired on 2026-10-14 at the author's request.
  Its reused catalog's MIT notice is retained at
  `skills/nature-polishing/references/academic-humanization/HUMANIZER_LICENSE`; recovery copies remain local.
- Chinese source: https://github.com/op7418/Humanizer-zh
- MIT license retained at `skills/humanizer-zh/LICENSE`.
- On 2026-10-12, English prompt/docs were updated from
  `225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8` (3.1.0), and Chinese prompt/docs/tests
  from `f4518a8eab97b8bfebc66a89d34320a89bef6930` (2026-09-23 revision).
  Local academic boundaries, clean-final delivery and installed platform metadata
  are retained. Chinese `allowed-tools` is omitted and MIT metadata retained for
  Codex compatibility. This is an adapted prompt update, not a plugin installation
  or independent writing-quality certification. See `docs/humanizer_upstream.md`.

## OpenSpec

- Official package: `@fission-ai/openspec` version `1.12.0`.
- Source: https://github.com/Fission-AI/OpenSpec/tree/v1.12.0
- License: MIT; retained at `openspec/OPENSPEC_LICENSE`.
- `.agents/skills/openspec-*` are upstream-generated project integrations. Bodies
  and notices are retained; compatibility moved into metadata and Bash-only
  allowed-tools removed for local Codex validation/shell compatibility. The CLI
  is installed separately, not vendored.
- `openspec/schemas/research-task` and Research Agent's OpenSpec reference are
  local research adaptations; they are not upstream scientific validation claims.

## Local adapter terms

Local research adapters and the router come from the user's existing installation.
Their source/provenance notes remain where supplied. In particular,
`skills/nature-polishing/references/anti-defensive-writing/references/provenance.md` describes independently
written guidance distilled from cited public designs.

The maintainer's original contributions use the root Apache-2.0 license.
Adaptations of third-party works remain subject to their original terms; the
root license is not a replacement for them. Private research inputs, corpora,
credentials and project data are not bundled.

## Reference projects

The projects in `docs/reference_projects.md` were inspected for design ideas.
Their runtimes, credentials, datasets and skill suites were not newly imported.
That document records observed license metadata and outstanding reuse questions.
