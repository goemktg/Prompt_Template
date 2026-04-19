---
name: deep-think
description: 'Mediator-first deep reasoning protocol for high-difficulty tasks. Triggers: deep-think, multi-hypothesis reasoning, structured refinement, mediator triage.'
---

# deep-think

## Usage

Use this skill when a task needs more than a single direct specialist pass: novel architecture, ambiguous tradeoffs, high-cost mistakes, or deliberate multi-hypothesis reasoning.

This is a repository-fit protocol surface for the active mediator stack. It is executed by `@deep-think-mediator`, not by the orchestrator or a leaf specialist directly.

## Responsibility

This skill owns protocol-local reasoning flow only:

- Normalize the intake for `@deep-think-mediator`.
- Triage whether the task should stay in deep-think or redirect to `@dt-council-mediator`.
- Shape a bounded multi-hypothesis reasoning pass using the active agent fleet.
- Return a normalized payload back to the orchestrator.

Out of scope:

- Lifecycle writes, TODO ownership, and approval gates.
- User interaction and memory persistence.
- File editing or publication decisions.
- Direct vendor integration beyond the leaf-proxy boundary.

## Active Repo Surfaces

Use the active repository surfaces instead of assuming the full reference stack:

- First protocol hop: `@deep-think-mediator`
- Council redirect target: `@dt-council-mediator`
- Optional Gemini runtime surface: host-provided native Gemini access outside the repo-owned runtime, when available
- Candidate reasoning participants: `@architect`, `@planner-gpt`, `@planner-gemini`, `@planner-claude`, `@research-gpt`, `@research-gemini`, `@research-claude`, `@validator`
- Optional runtime helpers when configured: `session-gate` and `context-manager`

## Protocol

1. Normalize intake
- Require: objective, constraints, budget hint, and expected output shape.
- If a protocol asset reference is provided, prefer that asset. Otherwise run this local repo-fit protocol.

2. Run triage
- Classify difficulty as `lite`, `standard`, or `deep`.
- Classify diversity need as `low`, `medium`, or `high`.
- If diversity need is high enough that disagreement handling is the main value, return redirect metadata for `@dt-council-mediator` instead of forcing deep-think.

3. Build the reasoning set
- Choose 2 to 3 distinct reasoning participants from the active agent fleet.
- Prefer structural diversity over duplicated roles.
- Use a Gemini-family runtime path only if it is explicitly needed and the host environment provides native Gemini access outside the repo-owned runtime.

4. Generate and critique
- Produce parallel hypotheses.
- Require each hypothesis to receive a self-critique or cross-check before synthesis.
- Keep the protocol bounded. If the budget hint is tight, reduce branch count before reducing verification.

5. Synthesize
- Merge compatible findings.
- Preserve unresolved disagreements instead of flattening them.
- Return the best current answer plus explicit risks, weak points, and any redirect rationale.

## Output Contract

Return one of these shapes:

```yaml
deep_think_mediator_result:
  status: complete
  tier: lite | standard | deep
  summary: <short outcome>
  final_payload:
    recommendation: <result>
    risks: [<risk>]
    open_questions: [<question>]
  metadata:
    protocol_asset: local-repo-fit | <path>
    phases_completed: [triage, hypotheses, critique, synthesis]
    participants: [<agent labels>]
```

```yaml
deep_think_mediator_result:
  status: redirect
  suggested_redirect_target: dt-council-mediator
  reason: <why council routing is preferred>
  redirect_context: <handoff payload>
```

```yaml
deep_think_mediator_result:
  status: blocked | error
  reason: <missing dependency or failure>
  partial_payload: <optional>
```

## Exit Criteria

- Intake is normalized.
- A bounded deep-think pass or a clean council redirect is produced.
- The result respects lifecycle ownership boundaries.
- No leaf vendor path is assumed without host-provided runtime access.

## Failure Handling

- Missing mediator context or protocol inputs: return `blocked`.
- Required Gemini leaf path unavailable: return `blocked` or a degraded payload without vendor participation.
- Budget exhausted before critique and synthesis: return `error` with the best partial payload.