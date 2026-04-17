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
- `copilot/hooks.json`
- `copilot/hooks/*.py`
- `copilot/hooks/**/*.py`

Keep this file authoring-focused even after expansion.

## Out Of Scope

- Do not define global routing, approval, or delegation rules here.
- Do not move runtime governance from `shared/copilot-instructions.md` into runtime-surface files.
- Do not describe hook lifecycle policy or MCP operational procedures in full unless the target file needs a local authoring note.

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
- Future-surface references are clearly marked as inactive until explicit `applyTo` expansion is added.