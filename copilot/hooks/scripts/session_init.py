#!/usr/bin/env python3
"""sessionStart hook: initialize lifecycle persistence for the current session."""

from __future__ import annotations

import sys

from _lifecycle_hook_common import (
    UpgradeStateStore,
    current_continuity,
    extract_metadata,
    load_payload,
    resolve_workspace_root,
    update_lifecycle_state,
)


RESUME_CONTINUITY_KEYS = (
    "next_transition",
    "resume_token",
    "workspace_root",
)


def _initial_active_task(payload: dict[str, object]) -> str:
    for key in ("activeTask", "active_task", "task", "prompt"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return "session"


def _resume_candidate(lifecycle_state: dict[str, object]) -> bool:
    current_phase = lifecycle_state.get("current_phase")
    status = lifecycle_state.get("status")
    return current_phase == "AWAIT" or status == "awaiting"


def _resume_continuity(store: UpgradeStateStore) -> dict[str, object]:
    continuity = current_continuity(store)
    return {
        key: continuity[key]
        for key in RESUME_CONTINUITY_KEYS
        if key in continuity
    }


def _hydrate_previous_session(payload: dict[str, object]) -> bool:
    workspace_root = resolve_workspace_root(payload)
    store = UpgradeStateStore(workspace_root)
    state = store.load()
    lifecycle_state = state.get("lifecycle_state")
    if not isinstance(lifecycle_state, dict) or not _resume_candidate(lifecycle_state):
        return False

    continuity = _resume_continuity(store)
    continuity.update(extract_metadata(payload, workspace_root))
    continuity["hydrated_from_previous_session"] = True
    continuity["last_event"] = "sessionStart"
    continuity["last_session_start"] = True
    continuity["compact_safe"] = False

    await_context = lifecycle_state.get("await_context")
    store.update_lifecycle_state(
        active_task=lifecycle_state.get("active_task"),
        approval_pending=bool(lifecycle_state.get("approval_pending", False)),
        await_context=dict(await_context) if isinstance(await_context, dict) else None,
        continuity=continuity,
        current_phase=lifecycle_state.get("current_phase"),
        current_plan_hash=lifecycle_state.get("current_plan_hash"),
        status=lifecycle_state.get("status", "idle"),
    )
    return True


def main() -> int:
    try:
        payload = load_payload()
        if _hydrate_previous_session(payload):
            return 0
        update_lifecycle_state(
            payload,
            current_phase="INIT",
            status="active",
            active_task=_initial_active_task(payload),
            continuity_updates={
                "last_event": "sessionStart",
                "last_session_start": True,
                "compact_safe": False,
            },
            reset_continuity=True,
        )
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())