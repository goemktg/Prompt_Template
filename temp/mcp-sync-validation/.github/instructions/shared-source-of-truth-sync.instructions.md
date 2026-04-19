---
name: 'Shared Source-Of-Truth Sync'
description: 'Authoring rules for shared/** source-of-truth assets. Refresh affected runtime mirrors under .github when mirrored surfaces change.'
applyTo: 'shared/**'
---

<!-- TECHNIQUE: Principled Instructions (arXiv:2312.16171) -->

# Shared Source-Of-Truth Sync

Use this file when editing source-of-truth assets under `shared/`.

## Purpose

- Keep edits anchored in the repository's source-of-truth layer.
- Remind authors that some `shared/**` assets feed runtime mirrors under `.github/`.
- Ensure affected mirrors are refreshed when the upstream source changes.
- Keep lifecycle-first governance anchored in source-of-truth assets instead of spreading independent copies into runtime config surfaces.

This file governs upstream authoring workflow for `shared/**`. Mirror-side direct-edit guardrails belong in `runtime-mirrors.instructions.md`.
It may apply alongside narrower surface-specific instructions under `shared/`; use it as a workflow overlay for source-of-truth sync decisions.

## Repository Model

Treat these locations as the authoritative sources in this repository:

- `constitution.md` is the root source-of-truth for the constitution.
- `shared/copilot-instructions.md` is the source-of-truth policy file.
- `shared/instructions/` contains the source-of-truth instruction files.
- `AGENTS.md` and source agent assets under `copilot/agents/` define catalog and agent-side lifecycle wording.
- `.github/copilot-instructions.md` and `.github/instructions/` are runtime mirrors.

Do not treat runtime mirrors as the primary authoring target when the upstream source lives under `shared/`.

Lifecycle-first governance changes should be authored in these source-of-truth policy, catalog, and agent surfaces first. Runtime config files such as `copilot/mcp.json`, `plugin.json`, and `copilot/deploy-manifest.json` are not alternate homes for the same governance text.

## Sync Decision

Not every `shared/**` edit maps to the same sync target, and some edits may not affect any mirror at all.

Before finishing a change under `shared/`, decide whether the edited asset affects a mirrored runtime surface:

1. If the edited file has a documented runtime mirror, refresh that mirror as part of the workflow.
2. If the edited file feeds a different deployment or sync path, use the matching target for that asset.
3. If the edited file has no runtime mirror, no `.github` sync is required.

Sync may require an explicit manual update of the matching mirror path as part of the same change. Do not assume the mirror updates automatically.

When the upstream edit changes lifecycle-first wording in a mirrored source-of-truth asset, treat mirror refresh as part of the same implementation step. Do not respond to that kind of change by copying lifecycle governance into runtime configuration files that only need identifiers or integration metadata.

## Common Mirror Pairs

Practical examples in this repository model:

- `shared/copilot-instructions.md` -> `.github/copilot-instructions.md`
- `shared/instructions/*.instructions.md` -> `.github/instructions/*.instructions.md`

Apply the example by path, not by copy-paste habit. The correct sync target depends on which mirrored runtime surface is affected.

## Authoring Rules

- Edit the source-of-truth asset first.
- Check whether the change affects a mirrored runtime surface under `.github/`.
- Refresh the affected mirror when required, using the repository's explicit or manual sync workflow.
- Keep the source and mirror aligned after the change.
- If the upstream change is lifecycle-related, verify that the propagated text stays in source policy, agent, catalog, or instruction mirrors rather than expanding into runtime config surfaces.
- If the change only affects a non-mirrored `shared/**` asset, avoid unnecessary `.github` updates.

## Authoring Checklist

- The edit was made in the source-of-truth file under `shared/`.
- The affected runtime mirror target, if any, was identified correctly.
- Required mirror refresh steps were performed or explicitly noted.
- Lifecycle-first wording stayed anchored to source-of-truth and mirror surfaces instead of becoming duplicated runtime-config policy.
- No assumption was made that all `shared/**` edits share the same sync destination.