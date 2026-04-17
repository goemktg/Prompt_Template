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

This file governs upstream authoring workflow for `shared/**`. Mirror-side direct-edit guardrails belong in `runtime-mirrors.instructions.md`.
It may apply alongside narrower surface-specific instructions under `shared/`; use it as a workflow overlay for source-of-truth sync decisions.

## Repository Model

Treat these locations as the authoritative sources in this repository:

- `constitution.md` is the root source-of-truth for the constitution.
- `shared/copilot-instructions.md` is the source-of-truth policy file.
- `shared/instructions/` contains the source-of-truth instruction files.
- `.github/copilot-instructions.md` and `.github/instructions/` are runtime mirrors.

Do not treat runtime mirrors as the primary authoring target when the upstream source lives under `shared/`.

## Sync Decision

Not every `shared/**` edit maps to the same sync target, and some edits may not affect any mirror at all.

Before finishing a change under `shared/`, decide whether the edited asset affects a mirrored runtime surface:

1. If the edited file has a documented runtime mirror, refresh that mirror as part of the workflow.
2. If the edited file feeds a different deployment or sync path, use the matching target for that asset.
3. If the edited file has no runtime mirror, no `.github` sync is required.

Sync may require an explicit manual update of the matching mirror path as part of the same change. Do not assume the mirror updates automatically.

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
- If the change only affects a non-mirrored `shared/**` asset, avoid unnecessary `.github` updates.

## Authoring Checklist

- The edit was made in the source-of-truth file under `shared/`.
- The affected runtime mirror target, if any, was identified correctly.
- Required mirror refresh steps were performed or explicitly noted.
- No assumption was made that all `shared/**` edits share the same sync destination.