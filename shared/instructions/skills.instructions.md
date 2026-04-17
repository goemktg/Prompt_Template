---
name: 'Skill Asset Guardrails'
description: 'Authoring rules for shared/skills/**/SKILL.md files, including packaging criteria for repeatable non-interactive protocols.'
applyTo: 'shared/skills/**/SKILL.md'
---

<!-- TECHNIQUE: Principled Instructions (arXiv:2312.16171) -->

# Skill Authoring Guardrails

Use this file only for authoring `SKILL.md` assets under `shared/skills/`.

## Scope

- Own SKILL.md structure, trigger clarity, executable protocol design, and packaging fitness.
- Keep guidance local to skill authoring.
- Leave repository-wide governance, routing gates, approval policy, and global escalation rules in `shared/copilot-instructions.md` and `AGENTS.md`.

## Out Of Scope

- Do not duplicate `0-SKILL`, `0-INTENT`, `0-GATE`, delegation policy, or main-session governance here.
- Do not turn a skill into a generic documentation file or a substitute for agent definitions.
- Do not encode runtime MCP or hook configuration in SKILL.md unless the skill is specifically about authoring those assets.

## File And Frontmatter Rules

- Path must be `shared/skills/<skill-name>/SKILL.md`.
- Frontmatter `name` must match the folder name exactly.
- Required frontmatter:
  - `name`
  - `description`
- Wrap `description` in single quotes.
- Keep the description specific and activation-oriented so the skill can be discovered reliably.

## Recommended SKILL.md Shape

Preferred sections:

1. Usage
2. Responsibility
3. Required tools or prerequisites, if any
4. Protocol
5. Output contract
6. Exit criteria
7. Failure handling or escalation, when needed

Authoring rules:

- One skill should own one repeatable job.
- Protocol steps should be short, ordered, and directly executable.
- Put guardrails near the protocol they constrain.
- Use output contracts when downstream agents or users rely on structured results.
- Mention handoffs only when the next owner is explicit.

## Packaging Test: Is This A Good Skill?

Package the workflow as a skill only when most of these are true:

- The task recurs across sessions or repositories.
- The task follows a stable sequence of non-interactive steps.
- The same acceptance checks apply each time.
- The workflow benefits from bundled templates, examples, or checklists.
- The workflow can be executed without pausing for user negotiation in the middle.

Prefer another surface when:

- The guidance is always-on and broad: use instructions.
- The capability needs context isolation or specialist identity: use an agent.
- The task is a one-off command or narrow prompt: use a prompt file.

## Identifying Repeatable Non-Interactive Multi-Step Protocols

Good candidates for skill packaging usually have all of the following traits:

- The workflow has three or more steps that run in a predictable order.
- Each step transforms inputs into a defined intermediate or final output.
- Mid-protocol user approval is not required for normal execution.
- Failure modes can be described in advance.
- The same protocol can be reused without project-specific rewrites.

Signals that a protocol is not ready for packaging:

- The steps change substantially every time.
- Success depends on ad hoc judgment that is not written down.
- The workflow mostly routes to other tools without adding packaging value.
- The protocol is actually a global policy and belongs in `shared/copilot-instructions.md` instead.

## Protocol Writing Rules

- Start with the smallest executable sequence.
- Name each step by outcome, not by vague intention.
- Distinguish required steps from optional branches.
- If external content is involved, state sanitization or trust-boundary handling explicitly.
- If the workflow produces artifacts, name their expected paths or shapes.

## Authoring Checklist

- Folder name and frontmatter `name` match.
- The description contains concrete trigger phrases.
- The responsibility statement is single-purpose.
- The protocol is executable without hidden assumptions.
- Packaging value is clear: repeatable, non-interactive, and reusable.
- Global governance remains referenced, not copied.