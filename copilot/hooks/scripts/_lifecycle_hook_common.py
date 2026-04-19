#!/usr/bin/env python3
"""Shared helpers for minimal lifecycle hook state updates."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


PLUGIN_ROOT = Path(__file__).resolve().parents[3]
COPILOT_SCRIPTS_DIR = PLUGIN_ROOT / "copilot" / "scripts"

if str(COPILOT_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(COPILOT_SCRIPTS_DIR))

from runtime_root import find_plugin_root  # type: ignore  # noqa: E402
from upgrade_state import UpgradeStateStore  # type: ignore  # noqa: E402


WORKSPACE_KEYS = (
    "workspace",
    "workspacePath",
    "workspace_path",
    "workspaceRoot",
    "workspace_root",
    "workspaceFolder",
    "workspace_folder",
    "cwd",
    "rootPath",
    "root_path",
    "target_workspace",
    "targetWorkspace",
)
IDENTIFIER_KEYS = (
    "sessionId",
    "session_id",
    "conversationId",
    "conversation_id",
    "threadId",
    "thread_id",
    "requestId",
    "request_id",
    "traceId",
    "trace_id",
)
UNCHANGED = object()


def load_payload() -> dict[str, Any]:
    try:
        raw_payload = sys.stdin.read()
    except OSError:
        return {}

    if not raw_payload.strip():
        return {}

    try:
        parsed = json.loads(raw_payload)
    except json.JSONDecodeError:
        return {}

    return dict(parsed) if isinstance(parsed, dict) else {}


def normalize_timestamp(raw_value: Any) -> float | None:
    if not isinstance(raw_value, (int, float)):
        return None

    timestamp = float(raw_value)
    if timestamp > 10_000_000_000:
        timestamp /= 1000.0
    return timestamp


def _iter_candidate_values(payload: dict[str, Any]) -> list[str]:
    values: list[str] = []
    queue: list[Any] = [payload]

    while queue:
        current = queue.pop(0)
        if not isinstance(current, dict):
            continue

        for key in WORKSPACE_KEYS:
            candidate = current.get(key)
            if isinstance(candidate, str) and candidate.strip():
                values.append(candidate)

        for nested_key in ("workspace", "context", "metadata", "session", "repo"):
            nested = current.get(nested_key)
            if isinstance(nested, dict):
                queue.append(nested)

    return values


def resolve_plugin_root() -> Path:
    resolved = find_plugin_root(
        start_path=Path(__file__).resolve().parent,
        required_markers=("plugin.json", "copilot/mcp.json"),
    )
    return Path(resolved).resolve()


def resolve_workspace_root(payload: dict[str, Any]) -> Path:
    plugin_root = resolve_plugin_root()
    for raw_candidate in _iter_candidate_values(payload):
        candidate = Path(raw_candidate).expanduser()
        if candidate.suffix and not candidate.exists():
            candidate = candidate.parent
        elif candidate.is_file():
            candidate = candidate.parent
        return candidate.resolve(strict=False)
    return plugin_root


def resolve_workspace_root_from_payload(payload: dict[str, Any]) -> Path | None:
    """Return workspace root resolved from payload keys only; None when no workspace key present."""
    for raw_candidate in _iter_candidate_values(payload):
        candidate = Path(raw_candidate).expanduser()
        if candidate.suffix and not candidate.exists():
            candidate = candidate.parent
        elif candidate.is_file():
            candidate = candidate.parent
        return candidate.resolve(strict=False)
    return None


def current_continuity(store: UpgradeStateStore) -> dict[str, Any]:
    state = store.load()
    lifecycle_state = state.get("lifecycle_state")
    if not isinstance(lifecycle_state, dict):
        return {}
    continuity = lifecycle_state.get("continuity")
    return dict(continuity) if isinstance(continuity, dict) else {}


def extract_metadata(payload: dict[str, Any], workspace_root: Path) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "workspace_root": str(workspace_root),
    }

    timestamp = normalize_timestamp(payload.get("timestamp"))
    if timestamp is not None:
        metadata["event_timestamp"] = timestamp

    for key in ("source", "hookEvent", "eventName", "event"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            metadata[key] = value

    for key in IDENTIFIER_KEYS:
        value = payload.get(key)
        if isinstance(value, (str, int, float)):
            metadata[key] = value

    return metadata


def update_lifecycle_state(
    payload: dict[str, Any],
    *,
    current_phase: str | None | object,
    status: str | object,
    active_task: str | None | object,
    continuity_updates: dict[str, Any],
    reset_continuity: bool = False,
) -> Path:
    workspace_root = resolve_workspace_root(payload)
    store = UpgradeStateStore(workspace_root)
    state = store.load()
    lifecycle_state = state.get("lifecycle_state")
    current_state = dict(lifecycle_state) if isinstance(lifecycle_state, dict) else {}
    continuity = {} if reset_continuity else current_continuity(store)
    continuity.update(continuity_updates)
    continuity.update(extract_metadata(payload, workspace_root))
    store.update_lifecycle_state(
        active_task=current_state.get("active_task") if active_task is UNCHANGED else active_task,
        approval_pending=False,
        await_context=None,
        continuity=continuity,
        current_phase=current_state.get("current_phase") if current_phase is UNCHANGED else current_phase,
        current_plan_hash=None,
        status=current_state.get("status", "idle") if status is UNCHANGED else status,
    )
    return workspace_root