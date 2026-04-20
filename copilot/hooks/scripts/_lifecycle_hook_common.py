#!/usr/bin/env python3
"""Shared helpers for hook payload resolution and session-gate file access."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


PLUGIN_ROOT = Path(__file__).resolve().parents[3]
COPILOT_SCRIPTS_DIR = PLUGIN_ROOT / "copilot" / "scripts"
_HOOK_SCRIPTS_DIR = Path(__file__).resolve().parent

if str(COPILOT_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(COPILOT_SCRIPTS_DIR))
if str(_HOOK_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_HOOK_SCRIPTS_DIR))

from runtime_root import find_plugin_root  # type: ignore  # noqa: E402
from session_state import resolve_session_state_dir  # noqa: E402


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


def resolve_session_gate_state_file() -> Path:
    """Return the gate-state.json path for the active session directory."""
    return resolve_session_state_dir() / "gate-state.json"
