<!-- TECHNIQUE: Principled Instructions (arXiv:2312.16171); Constitutional AI: Harmlessness from AI Feedback (arXiv:2212.08073) -->

# Repository Constitution

This file defines the repository's immutable governance principles for shared prompt and policy assets. It is intentionally thin and does not replace operational procedures, file-local authoring rules, or agent-specific protocols.

## Scope

- Source-of-truth ownership for cross-repository governance assets
- Approval and delegation boundaries
- Reference precedence and anti-duplication rules
- Stable ownership boundaries for policy surfaces

## Non-Goals

- Step-by-step operating procedures
- Agent or skill catalogs
- File-specific authoring checklists
- Project-specific implementation manuals

## Constitutional Principles

### 1. Source-of-Truth Hierarchy

- `constitution.md` defines immutable governance principles and ownership boundaries.
- `shared/copilot-instructions.md` defines repository-wide operational policy derived from this constitution.
- `.github/copilot-instructions.md` is the deployed runtime mirror of `shared/copilot-instructions.md` and must be updated via sync to remain semantically aligned with it.
- `AGENTS.md` defines agent and skill catalogs, routing, and structure guidance anchored to this constitution and the shared instructions.

### 2. Runtime Visibility

- Runtime mirrors under `.github/` must remain fully usable at runtime.
- Every runtime mirror must clearly identify its source-of-truth file.
- Runtime visibility does not create a second policy authority.
- Authorized source migrations may leave runtime mirrors temporarily stale until the next sync updates them.

### 3. Reference Discipline

- Immutable principles belong in this file.
- Repository-wide operational policy belongs in `shared/copilot-instructions.md`.
- Agent and skill catalog data belongs in `AGENTS.md`.
- Surface-specific authoring rules belong in the relevant instruction files.
- Cross-file references must point to the narrowest authoritative surface available.

### 4. Anti-Duplication

- Do not create competing governance sources for the same rule set.
- When content is mirrored for runtime visibility, preserve semantic equivalence instead of authoring an independent variant.
- Prefer short anchor references over re-copying global governance into local assets unless runtime availability requires a mirror.

### 5. Approval and Delegation Boundaries

- Main-session orchestration owns routing, approvals, and coordination boundaries.
- Specialist agents own substantive file mutations within their authorized domains.
- Prompt and policy assets outside `documents/` remain governed by prompt-asset workflows.
- Documentation assets under `documents/` remain governed by documentation workflows.

### 6. Deprecation and Migration

- When governance or procedure surfaces are removed, update dependent references to point at the surviving authority or use neutral wording.
- Migration work must reduce duplicate authority, not replace one deleted surface with another ambiguous one.
- When procedural content is relocated, update the owning authoritative surface instead of creating a new permanent duplicate.

## Ownership Map

| Surface | Owns | Must Not Own |
| --- | --- | --- |
| `constitution.md` | Immutable principles, ownership boundaries, reference rules | Procedures, checklists, catalogs |
| `shared/copilot-instructions.md` | Global operational policy and repository-wide guardrails | Agent catalog details, file-local authoring rules |
| `.github/copilot-instructions.md` | Runtime-visible mirror of shared instructions | Independent policy authority |
| `AGENTS.md` | Agent catalog, skill catalog, routing, structure guidance | Constitutional text, long procedural manuals |

## Change Control

- Constitutional changes require explicit approval before implementation.
- Structural migrations must preserve source-of-truth clarity and runtime visibility.
- Limited anchor normalization is preferred over broad deduplication unless a larger approved rollout explicitly expands scope.
