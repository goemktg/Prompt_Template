---
name: 'Agent Asset Guardrails'
description: 'Authoring rules for copilot/agents/*.agent.md files. Use when creating or revising agent definitions.'
applyTo: 'copilot/agents/*.agent.md'
---

<!-- TECHNIQUE: Principled Instructions (arXiv:2312.16171) -->

# Agent Authoring Guardrails

Use this file only for authoring `copilot/agents/*.agent.md` assets.

## Scope

- Own structure, frontmatter quality, trigger clarity, and authoring hygiene for agent definition files.
- Keep rules local to the agent-file surface.
- Treat `shared/copilot-instructions.md` and `AGENTS.md` as the source of truth for global governance, routing, and repository-wide policies.

## Out Of Scope

- Do not restate or move `0-SKILL`, `0-INTENT`, `0-GATE`, approval boundaries, language policy, or other global governance into agent files.
- Do not turn an agent definition into a second orchestrator or a second policy manual.
- Do not use this file to define runtime configuration for MCP, hooks, or shell launch behavior.

## File And Naming Rules

- Path must be `copilot/agents/<agent-name>.agent.md`.
- The frontmatter `name` should match the filename stem and use lowercase hyphenated words.
- Keep one agent focused on one primary responsibility. If the file starts describing multiple unrelated jobs, split it.
- Write prose in English. Keep identifiers, tool names, and examples in their native syntax.

## Frontmatter Guardrails

Required frontmatter:

- `name`
- `description`

Optional frontmatter, only when justified:

- `tools`
- `argument-hint`
- `model`
- `target`
- `user-invocable`
- `disable-model-invocation`
- `agents`
- `handoffs`

Frontmatter rules:

- Wrap `description` in single quotes.
- Keep `description` specific enough to act as a discovery surface: include what the agent does and when to use it.
- Keep `tools` minimal and capability-based. Do not grant tools that the body never uses.
- Set `user-invocable: true` only for agents intended to be selected directly by users.
- Use `disable-model-invocation` only when the agent should not be callable as a subagent by other agents.
- Add `argument-hint` when the agent benefits from consistent invocation payloads.
- Add `agents` or `handoffs` only when the agent genuinely coordinates other agents or offers explicit next actions.

## Body Structure

Preferred structure:

1. Mission
2. Boundary or responsibility section
3. Operating protocol or decision process
4. Output expectations
5. Failure or escalation rules when needed

Authoring rules:

- State the agent's job in the first section with an explicit boundary.
- Define what the agent owns and what it must not own.
- Use ordered steps only for executable workflows.
- Keep examples short and representative.
- Avoid repeating repository-wide safety or delegation text unless the agent needs a local reminder that narrows its own role.

## Role-Boundary Checks

- If the file starts copying large sections from `shared/copilot-instructions.md`, stop and replace them with a short boundary reference.
- If the agent appears to make routing decisions outside its own specialty, narrow the scope.
- If the file mixes planning, implementation, and review into one role without a clear reason, split responsibilities.

## Authoring Checklist

- The filename, frontmatter `name`, and described role align.
- The description contains concrete trigger phrases.
- Optional frontmatter fields are present only when they change behavior.
- The body explains mission, limits, and execution shape without duplicating global governance.
- The agent remains understandable without relying on hidden assumptions.