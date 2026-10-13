# Conceptual figure handoff

Use when a new or substantially redesigned conceptual figure needs a generation
prompt. The conceptual-prompts mode intake contract controls the final prompt;
this reference supplies the missing planning interface, not another approval
system. Reuse the project's existing specification and complete relevant fields
there. Data-only plots and edits preserving an approved layout do not need it.

## Preserve scientific meaning

Record the objective and the logic status: `DRAFT`, `LOGIC_VALIDATED`,
`USER_APPROVED`, `USER_WAIVED` or a justified `NOT_APPLICABLE`. Model checking
can support `LOGIC_VALIDATED`, never author approval. An exploratory prototype
and a manuscript/submission figure have different existing approval requirements.
Follow `references/conceptual-prompts/guide.md` from the owning figure directory for those boundaries.

Record the mainline as ordered node IDs and the supporting branches with their
IDs, attachment points and scientific purposes. Populate the semantic tables:

| Node ID | Display label | Role | Input/precondition | Transformation/function | Output/effect | Evidence/source locator | Claim/novelty role |
|---|---|---|---|---|---|---|---|

| Source node | Target node | Semantic type | Display label | Evidence/source locator | must_not_imply |
|---|---|---|---|---|---|

Label arrows as sequence, association, transport, constraint or causation as
appropriate. A supported sequence cannot be upgraded to a causal edge for a
more compelling graphic. Preserve required nodes, edges and direction across
layout changes. An intermediate quantity need not become a peer module.

## Select the visible projection

Provide the fields consumed by the prompt owner:

- `selected_visual_direction`: selection status (`AGENT_RECOMMENDED`,
  `USER_SELECTED` or `USER_WAIVED`), direction ID, narrative strategy, layout,
  dominant spine, reader path, grouping/lanes, novelty anchor, density budget,
  caption burden and preserved traits. Keep unselected options out of the prompt.
- `visual_render_projection`: map the semantic graph into visible modules,
  edge/port labels, attached tags, caption-only content and any omitted display
  items. Include port sides and routing corridors when needed. Visual compression
  does not authorize deleting semantic content or changing topology.
- `visible_text_allowlist`: exact display labels grouped as nodes, edges/ports
  and legend terms. Control IDs and internal field names are not display text
  unless the scientific source explicitly defines them as symbols.
- `figure_caption_division`: what must be visible, what the legend supports and
  what can be caption-only. Essential relationships must be visible; a caption
  cannot repair an incorrect arrow or missing core step.
- `negative_visual_constraints`: prohibited scientific implications and visual
  encodings, including unsupported causal arrows and inappropriate quality scales.

For a high-stakes figure, unresolved selection stays `AGENT_RECOMMENDED` until
the author selects or waives it under the existing contract. Do not infer either
approval from an instruction to plan, a provider name or a saved specification.

## Record the actual preflight

Set `prompt_preflight` findings from inspection: semantic preservation, supported
arrows, visible required mechanisms, projection consistency, allowlisted text,
selected direction and caption division. Mark a failed check `BLOCKED` with the
specific issue; mark the preflight passing only when its applicable checks pass.
Do not assert a pass based on field presence or a Mermaid preview.

Return the completed specification or the exact remaining scientific/selection
choice. The prompt owner checks its intake before producing the final prompt;
rendering, journal policy and subsequent visual/scientific review remain required
for the delivered image. No raster is a source of quantitative research values.
