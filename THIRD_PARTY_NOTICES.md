# Third-party provenance and licensing

This is initially a private maintenance repository for an existing local research
skill installation. There is no blanket license grant over all bundled material.
Retain original notices and review component-specific terms before redistribution.

## ARS writing adaptation

- `skills/ars-academic-writing/` is a local adaptation of selected argument,
  Introduction rhetoric and drafting guidance from academic-research-skills.
- Upstream copyright (c) 2026 Cheng-I Wu; CC BY-NC 4.0, not Apache or MIT.
- Commit, links, modifications, license and warranty notice are retained in
  `skills/ars-academic-writing/references/provenance.md`.
- This is not the full suite or an upstream-endorsed installation.

## Nature Skills

- The 18 directories below were retired on 2026-09-22 and restored on 2026-10-12
  at the author's explicit request, from this repository's published commit
  `b5b8e082522409aea0cb8db80a7afc2e5c086867`. They are current runtime dependencies.
- Source: https://github.com/Yuan1z0825/nature-skills
- License: Apache License 2.0; original root license copied to `skills/NATURE_LICENSE`.
- Scope: the 17 `nature-*` directories imported from the Nature installation,
  plus `researchwrite`. `nature-image2-prompt` is a separate local adapter.
- These are locally enhanced installed copies, not a pristine upstream release.
  See `docs/import_manifest.json` for the initial imported files.
- Embedded assets/tools may have additional LICENSE/NOTICE files; those remain
  in their original imported directories. Root Apache metadata alone does not
  establish rights for every image or embedded third-party example.
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

- English source: https://github.com/blader/humanizer
- MIT license retained at `skills/humanizer/LICENSE`.
- Chinese source: https://github.com/op7418/Humanizer-zh
- MIT license retained at `skills/humanizer-zh/LICENSE`.
- Current installed content and platform metadata are preserved. No upstream
  code update or fresh plugin compatibility certification is claimed.

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
`skills/anti-defensive-writing/references/provenance.md` describes independently
written guidance distilled from cited public designs.

A public redistribution license for the user's own contributions has not been
selected. Do not assume ownership of any referenced paper, image, font, tool,
or third-party text. Private research inputs and project data are not bundled.

## Reference projects

The projects in `docs/reference_projects.md` were inspected for design ideas.
Their runtimes, credentials, datasets and skill suites were not newly imported.
That document records observed license metadata and outstanding reuse questions.
