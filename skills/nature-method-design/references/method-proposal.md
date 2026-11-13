# Method proposal mode

Read the shared constraints in `../SKILL.md` first. This mode refines the method; load [experiment-plan.md](experiment-plan.md) only when an execution/validation plan is also requested.

For detailed method-refinement examples, consult [phase-details.md](phase-details.md) only when needed.

### Phase 0: Freeze the Problem Anchor

Define:
- environmental system
- spatial and temporal scale
- target variable, process, or mechanism
- scientific gap
- why the question matters
- minimum evidence needed to answer it

The problem anchor must remain stable through the refinement. Do not let method novelty replace the scientific question.

### Phase 1: Data feasibility

Reuse the shared data audit and inspect only unresolved feasibility assumptions. If the data cannot answer the approved question, report the gap instead of designing an unsupported method. Acquisition remains conditional on task authorization.

### Phase 2: Compare Method Routes

Compare viable routes when the method remains open or the user requests comparison. When the author has already chosen a method, refine it and its relevant baselines without forcing unrelated alternatives:

For a method-development task, compare mature field methods and any justified
borrowed or frontier route. For observational, literature, measurement or
scenario research, compare designs that answer the actual question: what is
measured, against which reference, under which assumptions, and which rival
explanation remains compatible. An algorithm family comparison is not mandatory.

For a material unresolved interpretation, identify the observation that would
distinguish it from its strongest competitor, whether the current data contain
it, and the smallest feasible addition if they do not. Avoid circular proxies
defined by the outcome. State how the decision changes if that observation is
absent, null or reversed; descriptive contributions need no invented mechanism.

For every borrowed or frontier component, state:
- what is transferred
- why transfer is valid
- what evidence would prove transfer legality
- where the transfer likely fails

### Phase 3: Build the Final Method Proposal

Specify:
- dominant contribution type: `problem`, `method`, `data`, or `finding`
- core method blocks and their roles
- data-processing workflow
- model/analysis workflow
- baseline comparison set
- uncertainty and sensitivity analysis needs
- figure implications
- implementation risks

Keep the method compact. Remove components that do not defend the main claim.

### Phase 4: PI-style Reviewer Gate

Check:
- Does the method answer the frozen scientific question?
- Is the novelty more than applying method X to domain Y?
- Are the data assumptions realistic after the Data Audit Gate?
- Are mature baselines included?
- Is cross-domain transfer justified?
- Are limitations and failure boundaries explicit?
- What is the strongest reviewer objection?
- What fatal flaw would make the project not worth running?
- Should the proposal proceed, be reframed, or stop before detailed experiment planning?

## Canonical Output

Use the existing proposal document. Without a project convention, `refine-logs/FINAL_PROPOSAL.md` is a fallback when saving is requested; adapt this outline to the task:

```markdown
# Final Proposal

## Problem Anchor

## Scientific Question

## Knowledge Gap

## Dominant Contribution

## Data Audit Gate
| Dimension | Finding | Risk | Required Action |
|-----------|---------|------|-----------------|
| Structure |  |  |  |
| Quality |  |  |  |
| Semantics |  |  |  |
| Dependency |  |  |  |
| Access / License |  |  |  |

## Data and Study System

## Mature Baselines and Field Standards

## Method Thesis

## Method Workflow

## Cross-Domain Inspiration and Transfer Boundary

## Claim Map
| Claim | Evidence Needed | Baseline / Comparator | Risk | Planned Validation |
|-------|-----------------|-----------------------|------|--------------------|

## Data Processing Plan

## Model / Analysis Plan

## Figure Implications

## Limitations and Failure Boundaries

## Next Step
If experiment planning is included in the request, continue in this skill's experiment-plan mode using the same data audit; otherwise deliver the method proposal.
```

Optionally write:
- `refine-logs/REVIEW_SUMMARY.md` — reviewer critique and response notes
- `refine-logs/REFINEMENT_REPORT.md` — summary of changes across refinement rounds

## Key Rules

- Verify novelty-critical prior work and retain explicit uncertainty where coverage remains incomplete; reuse sufficient evidence without requiring legacy artifact names.
- Do not invent data availability, performance, results, or citations.
- Prefer the smallest adequate mechanism.
- Prefer strong baselines over padded comparisons.
- Make transfer legality explicit for every cross-domain or frontier component.
- Separate method design from experiment planning; load experiment-plan mode for a requested detailed run order.
