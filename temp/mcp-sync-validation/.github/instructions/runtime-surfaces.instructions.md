---
name: 'Runtime Surface Guardrails'
description: 'Authoring rules for runtime configuration surfaces, initially scoped to copilot/mcp.json.'
applyTo: 'copilot/mcp.json'
---

<!-- TECHNIQUE: Principled Instructions (arXiv:2312.16171) -->

# Runtime Surface Authoring Guardrails

Use this file only when authoring runtime-surface configuration files. Initial scope is `copilot/mcp.json`.

## Scope

- Own authoring quality for runtime-surface configuration files.
- Focus on configuration shape, naming clarity, environment hygiene, and comments or notes about intent.
- Treat this as a local authoring aid, not as operational policy.

## Current Target

- Active `applyTo` target: `copilot/mcp.json`

## Planned Expansion

Future authoring coverage may extend to these existing or future surfaces when the repository explicitly activates them via additional `applyTo` patterns:

- `plugin.json`
- `copilot/deploy-manifest.json`
- `copilot/hooks.json`
- `copilot/hooks/*.py`
- `copilot/hooks/**/*.py`

Keep this file authoring-focused even after expansion.

## Out Of Scope

- Do not define global routing, approval, or delegation rules here.
- Do not move runtime governance from `shared/copilot-instructions.md` into runtime-surface files.
- Do not duplicate lifecycle-first governance from policy, agent, catalog, or source instruction surfaces into runtime config files.
- Do not describe hook lifecycle policy or MCP operational procedures in full unless the target file needs a local authoring note.

## Lifecycle Boundary For Runtime Surfaces

Treat runtime surfaces as integration descriptors, not as a second governance layer.

- Lifecycle-first behavior is defined upstream in source-of-truth policy, agent, catalog, and instruction assets.
- Runtime surfaces may carry local integration points such as identifiers, server definitions, commands, paths, or activation metadata.
- Runtime surfaces may include a short local note that explains how a runtime field connects to the upstream lifecycle model.
- Runtime surfaces must not restate the full lifecycle phase machine, approval semantics, delegation rules, or repository-wide governance contracts.

If a lifecycle wording change occurs upstream, update this file only when the boundary or allowed local metadata needs clarification. Do not propagate the same governance text into `copilot/mcp.json`, `plugin.json`, or `copilot/deploy-manifest.json` unless a concrete integration field needs that clarification.

## MCP Configuration Guardrails

When editing `copilot/mcp.json`:

- Preserve valid JSON structure and keep formatting consistent.
- Add servers only when the command, args, and environment are all intentional and minimal.
- Prefer workspace-relative storage paths for local state when persistence is required.
- Keep environment variables explicit; avoid hidden defaults that make local debugging harder.
- Use stable server keys that reflect the actual service purpose.
- Do not add duplicate servers with overlapping responsibility unless the distinction is documented.

## Authoring Rules For Runtime Surfaces

- Document intent with short, local explanations outside the JSON file when needed; keep raw config uncluttered.
- Separate configuration concerns by surface: MCP config, hook manifest, and hook scripts should not absorb each other's rules.
- Treat shell commands, environment variables, and file paths as part of the interface contract. Edit them cautiously.
- Keep lifecycle references narrow and interface-level; prefer linking the concept back to the upstream policy surface instead of copying governance prose.
- Prefer additive, reviewable changes over broad rewrites.

## Expansion Rules For Future Hook Surfaces

If this instruction file later expands to `plugin.json`, `copilot/hooks.json`, or hook scripts:

- Add narrow `applyTo` patterns instead of switching to a catch-all glob.
- Keep per-surface guidance local to the file type being edited.
- Avoid turning hook authoring notes into a second copy of runtime governance.

## Authoring Checklist

- The instruction remains local to runtime-surface authoring.
- The active target stays limited to `copilot/mcp.json` for now.
- Guidance improves config clarity without dictating repository-wide policy.
- Runtime surfaces are allowed to carry integration metadata, but not a second copy of lifecycle governance.
- Future-surface references are clearly marked as inactive until explicit `applyTo` expansion is added.