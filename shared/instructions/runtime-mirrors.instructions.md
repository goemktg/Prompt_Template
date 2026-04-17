---
name: 'Runtime Mirror Guardrails'
description: 'Authoring rules for .github runtime mirror files and other .github-owned assets. Prefer editing source-of-truth assets first, then syncing mirrors.'
applyTo: '.github/**'
---

<!-- TECHNIQUE: Principled Instructions (arXiv:2312.16171) -->

# Runtime Mirror Guardrails

Use this file when authoring assets under `.github/`.

## Purpose

- Prevent accidental direct edits to deployed or runtime mirror files under `.github/`.
- Preserve the repository's source-of-truth model:
  - `constitution.md`
  - `shared/copilot-instructions.md`
  - `shared/instructions/`
- Keep legitimate `.github`-native assets editable in place when no separate source-of-truth exists.

## Ownership Check Before Editing

Before changing a `.github/` file, decide which of these cases applies:

1. **Runtime mirror or deployed copy**
   - The file is generated, synced, or intentionally mirrored from a source-of-truth asset elsewhere in the repository.
   - Default action: edit the source-of-truth file, then sync so the `.github/` copy updates from that source.

2. **`.github`-native asset**
   - The file is genuinely owned in `.github/` and has no separate source-of-truth path.
   - Default action: edit the `.github/` file directly.

Do not treat every `.github/` file as a mirror. Determine ownership first.

## Runtime Mirror Rule

If a `.github/` file is a runtime mirror, do **not** make the mirror your primary edit target.

- Prefer the workflow: `edit source -> sync -> runtime mirror updates`.
- Keep mirrored files aligned with their upstream owner instead of applying one-off fixes directly in `.github/`.
- If you must inspect the runtime mirror, treat it as a verification surface unless the repository explicitly authorizes an emergency direct patch.

## Known Source-Of-Truth And Mirror Pairs

Examples in this repository model:

- `shared/copilot-instructions.md` -> `.github/copilot-instructions.md`
- `shared/instructions/*.instructions.md` -> `.github/instructions/*.instructions.md`
- `constitution.md` remains a source-of-truth asset and should not be re-authored through a `.github/` mirror.

When one of these upstream assets exists, edit the upstream file and sync the deployed copy.

## Direct-Edit Exceptions

Direct edits under `.github/` are still valid when the asset is owned there and no separate upstream source exists.

Examples of likely direct-edit exceptions:

- `.github/prompts/*.prompt.md` when the prompt file is authored and owned in place
- GitHub-native workflow or metadata files that exist only under `.github/`
- Repository-specific `.github` assets with no documented source in `shared/` or the repository root

If ownership is unclear, prefer checking for an upstream file before editing.

## Practical Authoring Rules

- Do not create a second source of truth by editing both the upstream asset and its deployed mirror independently.
- When a mirror looks stale or incorrect, fix the upstream asset first unless the task explicitly targets sync mechanics.
- If a direct `.github/` edit is necessary as a short-term exception, record that it should be reconciled back to the real source-of-truth path.
- Keep guidance practical: mirrors are usually not edited directly, but `.github`-native assets remain first-class edit targets.

## Authoring Checklist

- You identified whether the target `.github/` file is a mirror or a native asset.
- Mirrored/runtime files were edited through their upstream owner.
- `.github`-native assets were not blocked from legitimate direct edits.
- The expected workflow remained `source -> sync -> runtime mirror updates`.