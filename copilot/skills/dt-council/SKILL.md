---
name: dt-council
description: 'Mediator-first multi-perspective council protocol for disagreement surfacing and synthesis. Triggers: dt-council, model council, diverse perspectives, mediator redirect.'
---

# dt-council

## Usage

Use this skill when a task needs disagreement surfacing across distinct analytical lenses, or when `@deep-think-mediator` returns a council redirect.

This is a repository-fit council protocol surface for the active mediator stack. It is executed by `@dt-council-mediator` and stays inside the repository's lifecycle-first boundary.

## Responsibility

This skill owns council-local reasoning flow only:

- Normalize council intake and level selection.
- Select diverse participants from the active agent fleet.
- Sequence parallel analysis, critique, enrichment, and synthesis.
- Return a normalized council result to the orchestrator.

Out of scope:

- Lifecycle transitions, approval gates, and persistence.
- User-facing delivery.
- Independent Gemini vendor plumbing beyond the mediator's leaf boundary.
- Global orchestration beyond the council-local phase sequence.

## Active Repo Surfaces

Use these active repository surfaces:

- Council mediator: `@dt-council-mediator`
- Optional first-hop redirect source: `@deep-think-mediator`
- Optional Gemini runtime surface: host-provided native Gemini access outside the repo-owned runtime, when available
- Preferred participant pool: `@architect`, `@planner-gpt`, `@planner-gemini`, `@planner-claude`, `@research-gpt`, `@research-gemini`, `@research-claude`, `@validator`
- Optional runtime helpers when configured: `session-gate` and `context-manager`

## Levels

- `council`: 3 to 4 distinct participants, one enrichment round, one synthesis pass.
- `extended`: adds stronger critique and at least one additional enrichment round.
- `ultra`: reserved for the hardest decisions and only when the caller provides enough budget.

## Protocol

1. Normalize intake
- Require: objective, constraints, council level hint, budget hint, and expected output shape.
- If a protocol asset reference is provided, prefer that asset. Otherwise run this local repo-fit protocol.

2. Select participants
- Choose 3 to 4 participants with genuinely different lenses.
- Avoid duplicate participants unless a specific domain needs reinforcement.
- Use a Gemini-family runtime path only when it is explicitly required and the host environment provides native Gemini access outside the repo-owned runtime.

3. Run first-pass analysis
- Dispatch parallel first-pass analyses.
- Require each participant to state assumptions, strongest recommendation, and key uncertainty.

4. Critique and enrich
- Require a critique or destruction-test pass before synthesis.
- Share disagreement zones back across participants for one or more enrichment rounds depending on level.
- Preserve high-value disagreements rather than compressing them away.

5. Synthesize
- Produce one synthesis package.
- Name where the council agrees, where it disagrees, and why.
- If evidence is insufficient to resolve a disagreement, keep both positions in the output.

## Output Contract

Return one of these shapes:

```yaml
dt_council_mediator_result:
  status: complete
  level: council | extended | ultra
  summary: <short council outcome>
  final_payload:
    recommendation: <result>
    agreements: [<agreement>]
    disagreements: [<disagreement>]
    follow_ups: [<follow-up>]
  metadata:
    protocol_asset: local-repo-fit | <path>
    phases_completed: [selection, analysis, critique, enrichment, synthesis]
    participants: [<agent labels>]
```

```yaml
dt_council_mediator_result:
  status: blocked | error
  reason: <missing dependency or failure>
  partial_payload: <optional>
```

## Exit Criteria

- Council intake is normalized.
- Participant diversity is intentional.
- The final payload preserves meaningful disagreement.
- The result stays inside mediator and lifecycle boundaries.

## Failure Handling

- Missing council mediator context or inputs: return `blocked`.
- Required Gemini vendor path unavailable: return `blocked` or a degraded payload without vendor participation.
- Budget exhaustion before synthesis: return `error` with partial findings and unresolved disagreement zones.