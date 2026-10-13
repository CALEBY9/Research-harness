# Research Harness maintenance

This repository owns the versioned Research Agent source. `skills/` contains
the imported, locally enhanced installation; it is not the live skill directory.
Read `docs/architecture.md` and `.agent/NEXT.md` when resuming maintenance.

- Edit the smallest owner of an observed failure. Keep `research-agent` a router.
- On 2026-10-13 the author selected `nature-scientific-insight` as the core scientific
  decision skill. It owns evidence-grounded recommendations; discovery, design,
  result interpretation and Nature writing retain their task deliverables.
  Routine settled execution and language edits do not require a new judgment pass.
- Preserve task boundaries, author-controlled scientific decisions,
  bilingual prose requirements, source authority and clean-final delivery.
- Research workflow skills use `nature-<capability>` with lowercase hyphenated names.
  Keep `research-agent` as the public entry and preserve upstream identifiers for
  independent general-purpose tools such as Humanizer and EditaPlot.
  Directory, frontmatter, invocation metadata and current owner references agree;
  see `docs/skill_naming.md`. Do not install duplicate legacy-name aliases.
- On 2026-10-13 the author requested a full functional cleanup. Eight overlapping
  entries are now conditional resource modes under five retained owners; see
  `docs/skill_function_audit.md`. Preserve their useful mechanics and constraints,
  but do not restore standalone aliases or nested SKILL.md entrypoints.
- Do not copy project manuscripts, corpora, session transcripts, credentials,
  global runtime configuration or private evaluation inputs into this repository.
- Keep machine paths and private evaluations in ignored `local_state/`.
- Source changes do not authorize replacing installed skills. Compare the source
  and installed version, show the affected files, then apply the authorized scope.
- Use the smallest mechanical checks relevant to the changed files. Reuse prior
  verification when its scope and assumptions remain valid; do not repeat the
  full suite for ordinary instruction edits. Use `python scripts/harness.py validate`
  and affected owner checks when changes affect package structure, routing or code.
  A structural PASS is not evidence of better writing or scientific judgment.
- On 2026-10-13 the author deferred standalone model benchmarks. Observe behavior
  during later authorized real-project tasks and reuse their outputs and traces.
  Updating Research Agent does not require a new A/B run, extra model calls or
  human review session. A demonstrated failure or material behavior change may
  justify targeted follow-up; independent costly runs still need authorization.
- On 2026-10-12 the author explicitly requested restoring Nature Skills from
  the published `b5b8e08` snapshot as the writing foundation. After the author's
  2026-10-13 duplicate-skill cleanup, preserve ARS only as archived/versioned
  reference outside live skill discovery; keep skill_evolve_workflow retired. Verify affected
  behavior from actual tasks; structural checks do not certify writing quality. Do not enable
  automatic self-editing, paid evaluations, schedules or subagents without explicit
  authorization. On 2026-10-12 the author authorized Nature upstream monitoring:
  the weekly watcher may read the public upstream and prepare ignored local reviews,
  but must not overwrite skills, call models or publish research materials.
- Keep `.agent/STATE.md` and `.agent/NEXT.md` local and concise after implementation.

OpenSpec uses the project-local `research-task` schema and the Research Agent
reference `skills/research-agent/references/openspec-research.md`. Follow existing
authorization through implementation; planning-only requests remain planning-only.
Verify the requirements linked from tasks.md even without delta specs. Artifact
presence or checked tasks alone are not acceptance evidence. Keep project-specific
science in its owning project; archive must not rewrite scientific definitions.
