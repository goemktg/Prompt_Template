---
name: lifecycle-runtime-ops
description: 'Run the non-interactive lifecycle runtime operations protocol: verify activation, inspect or hydrate workspace state, write explicit transitions, and perform bounded refresh or cleanup checks.'
---

<!-- TECHNIQUE: Principled Instructions (arXiv:2312.16171) -->

# lifecycle-runtime-ops

## Usage

Use this skill when a task needs the repeatable lifecycle runtime operations already implemented in this repository:

- verify runtime activation
- inspect or hydrate `.copilot-memory/upgrade_state.json`
- write explicit lifecycle transitions
- run bounded runtime refresh or cleanup checks

## Responsibility

This skill owns repo-local lifecycle runtime operations only:

- Scope: activation verification, lifecycle state inspection, resumable hydration checks, transition writes, and bounded refresh or cleanup evidence.
- Out of scope: repository-wide governance, new lifecycle design, or unrelated runtime debugging.

## Required Inputs

- target workspace root
- optional explicit VS Code settings file paths for activation verification
- requested lifecycle phase or maintenance action

## Canonical Surfaces

Use the existing runtime surfaces and state store as the source of truth:

- `scripts/verify_runtime_activation.py`
- `scripts/write_lifecycle_transition.py`
- `scripts/refresh_mcp_runtime.py`
- `scripts/cleanup_runtime_artifacts.py`
- `copilot/scripts/upgrade_state.py`
- `copilot/hooks/scripts/session_init.py`
- `.copilot-memory/upgrade_state.json`

## Protocol

1. Verify activation first
- Run activation verification before mutating lifecycle state.
- Confirm plugin and hook manifests exist and at least one VS Code settings target enables this plugin root, hook manifest, custom hooks, and plugin activation.
- If activation fails, stop and report the missing activation fields.

2. Load and inspect workspace state
- Read workspace state through `UpgradeStateStore.load()` semantics.
- Inspect `lifecycle_state.current_phase`, `status`, `active_task`, `current_plan_hash`, `approval_pending`, `await_context`, and `runtime_state` timestamps.
- If the state file is missing or malformed, use the normalized migrated schema as the baseline instead of treating it as a hard failure.

3. Hydrate resumable AWAIT state when present
- If the current lifecycle state is `AWAIT` or `awaiting`, preserve resume-adjacent fields such as `active_task`, `current_plan_hash`, `await_context`, and continuity metadata.
- If the current state is not resumable, continue with a fresh operation-specific update.

4. Write explicit lifecycle transitions when requested
- Use only the supported phases: `INIT`, `ATOMIZE`, `PLAN`, `EXECUTE`, `REPORT`, `AWAIT`, `FINALIZE`.
- Use only the supported statuses: `idle`, `active`, `awaiting`, `completed`, `failed`.
- For `AWAIT`, include `approval_pending`, optional `await_reason`, and optional `next_transition`.
- For `FINALIZE` with `completed`, clear stale active-task state rather than carrying it forward.

5. Run bounded runtime maintenance checks
- Prefer dry-run for refresh or cleanup checks before any destructive action.
- Runtime refresh only targets interpreter processes under this plugin root that match `runtime_launcher.py`, `workspace_sync_server.py`, or `start-memory.py`.
- Cleanup scope stays bounded to deploy-managed `.bak` files and marker JSON files with `session-`, `compact-`, or `lifecycle-` prefixes under `.copilot-memory/`.
- If a non-dry-run action is taken, record refresh or cleanup results back into runtime state.

6. Return an operations summary
- Report activation status, workspace root, resulting lifecycle phase and status, hydration or resume details, and any refresh or cleanup candidates or changes.
- Keep the summary limited to the runtime protocol outputs; do not restate broader repository policy.

## Output Contract

Every run should return a synthesized operations summary that normalizes the underlying script outputs into these fields when applicable:

- `activation_ok`
- `workspace_root`
- `lifecycle_phase`
- `lifecycle_status`
- `current_plan_hash`
- `approval_pending`
- `hydrated_from_previous_session` (derived from lifecycle continuity when hydrate logic applies)
- `runtime_refresh_summary`
- `runtime_cleanup_summary`
- `issues`

## Exit Criteria

The skill run is complete when:

- activation verification has run
- lifecycle state has been loaded and inspected
- the requested transition write has either completed or been skipped with a reason
- any refresh or cleanup action stayed within the bounded runtime scope
- the final report includes the resulting phase, status, and unresolved issues

## Failure Handling

- If activation verification fails, do not write a new lifecycle transition.
- If phase or status input is invalid, fail fast and report the allowed values.
- If refresh or cleanup fails, preserve inspection results and report the specific process or path errors.