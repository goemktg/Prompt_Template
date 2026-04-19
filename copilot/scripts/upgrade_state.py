#!/usr/bin/env python3
"""Shared helpers for lifecycle-aware workspace upgrade state."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Mapping


def _as_dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _copy_dict(value: Any) -> dict[str, Any]:
    return dict(_as_dict(value))


def _extract_timestamp(*values: Any) -> float | None:
    for value in values:
        if not isinstance(value, dict):
            continue
        for key in ("updated_at", "timestamp", "checked_at", "last_run_ts"):
            candidate = value.get(key)
            if isinstance(candidate, (int, float)):
                return float(candidate)
    return None


class UpgradeStateStore:
    """Read, migrate, and update .copilot-memory/upgrade_state.json."""

    SCHEMA_VERSION = 2

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root.resolve()
        self.state_path = self.workspace_root / ".copilot-memory" / "upgrade_state.json"

    def load(self) -> dict[str, Any]:
        if not self.state_path.exists():
            return self._migrate({})

        try:
            raw_data = json.loads(self.state_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return self._migrate({})

        if not isinstance(raw_data, dict):
            return self._migrate({})
        return self._migrate(dict(raw_data))

    def save(self, state: Mapping[str, Any]) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.state_path.with_suffix(".json.tmp")
        temp_path.write_text(
            json.dumps(dict(state), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temp_path.replace(self.state_path)

    def save_last_exit_code(self, code: int, timestamp: float | None = None) -> None:
        state = self.load()
        event_ts = float(timestamp if timestamp is not None else time.time())
        state["last_exit_code"] = code
        if code == 0:
            state["last_success_ts"] = event_ts
        self.save(state)

    def update_supplementary_deploy(
        self,
        supplementary_deploy: Mapping[str, Any],
    ) -> None:
        state = self.load()
        state["supplementary_deploy"] = dict(supplementary_deploy)
        self.save(state)

    def update_lifecycle_state(self, **fields: Any) -> None:
        state = self.load()
        lifecycle_state = _copy_dict(state.get("lifecycle_state"))
        lifecycle_state.update(fields)
        lifecycle_state["updated_at"] = float(time.time())
        state["lifecycle_state"] = self._normalize_lifecycle_state(state, lifecycle_state)
        self.save(state)

    def update_runtime_refresh(self, refresh: Mapping[str, Any]) -> None:
        self._update_runtime_section("last_runtime_refresh", dict(refresh), mirror_top_level=True)

    def update_runtime_cleanup(self, cleanup_result: Mapping[str, Any]) -> None:
        self._update_runtime_section("last_runtime_cleanup", dict(cleanup_result), mirror_top_level=True)

    def update_sync_result(self, sync_result: Mapping[str, Any]) -> None:
        state = self.load()
        runtime_state = _copy_dict(state.get("runtime_state"))
        payload = dict(sync_result)
        event_ts = payload.get("timestamp")
        if not isinstance(event_ts, (int, float)):
            event_ts = time.time()
            payload["timestamp"] = event_ts

        runtime_state["last_sync"] = payload
        runtime_state["updated_at"] = float(event_ts)
        state["runtime_state"] = self._normalize_runtime_state(state, runtime_state)
        state["last_sync"] = payload

        exit_code = payload.get("exit_code")
        if isinstance(exit_code, int):
            state["last_exit_code"] = exit_code
            if payload.get("success") is True:
                state["last_success_ts"] = float(event_ts)

        self.save(state)

    def update_sync_check(self, sync_check: Mapping[str, Any]) -> None:
        self._update_runtime_section("sync_check", dict(sync_check), mirror_top_level=True)

    def _update_runtime_section(
        self,
        field_name: str,
        payload: dict[str, Any],
        *,
        mirror_top_level: bool,
    ) -> None:
        state = self.load()
        runtime_state = _copy_dict(state.get("runtime_state"))
        event_ts = payload.get("timestamp")
        if not isinstance(event_ts, (int, float)):
            event_ts = time.time()
            payload["timestamp"] = event_ts

        runtime_state[field_name] = payload
        runtime_state["updated_at"] = float(event_ts)
        state["runtime_state"] = self._normalize_runtime_state(state, runtime_state)
        if mirror_top_level:
            state[field_name] = payload
        self.save(state)

    def _migrate(self, state: dict[str, Any]) -> dict[str, Any]:
        migrated = dict(state)
        migrated["schema_version"] = self.SCHEMA_VERSION
        migrated["lifecycle_state"] = self._normalize_lifecycle_state(migrated, migrated.get("lifecycle_state"))
        migrated["runtime_state"] = self._normalize_runtime_state(migrated, migrated.get("runtime_state"))
        return migrated

    def _normalize_lifecycle_state(
        self,
        state: Mapping[str, Any],
        lifecycle_state: Any,
    ) -> dict[str, Any]:
        current = _as_dict(lifecycle_state)
        await_context = current.get("await_context")
        continuity = current.get("continuity")
        updated_at = current.get("updated_at")
        if not isinstance(updated_at, (int, float)):
            updated_at = state.get("last_success_ts")

        return {
            "active_task": current.get("active_task"),
            "approval_pending": bool(current.get("approval_pending", False)),
            "await_context": dict(await_context) if isinstance(await_context, dict) else None,
            "continuity": dict(continuity) if isinstance(continuity, dict) else {},
            "current_phase": current.get("current_phase"),
            "current_plan_hash": current.get("current_plan_hash"),
            "status": current.get("status", "idle"),
            "updated_at": float(updated_at) if isinstance(updated_at, (int, float)) else None,
        }

    def _normalize_runtime_state(
        self,
        state: Mapping[str, Any],
        runtime_state: Any,
    ) -> dict[str, Any]:
        current = _as_dict(runtime_state)
        last_sync = _copy_dict(current.get("last_sync") or state.get("last_sync")) or None
        last_runtime_refresh = (
            _copy_dict(current.get("last_runtime_refresh") or state.get("last_runtime_refresh")) or None
        )
        last_runtime_cleanup = (
            _copy_dict(current.get("last_runtime_cleanup") or state.get("last_runtime_cleanup")) or None
        )
        sync_check = _copy_dict(current.get("sync_check") or state.get("sync_check")) or None
        updated_at = current.get("updated_at")
        if not isinstance(updated_at, (int, float)):
            updated_at = _extract_timestamp(last_runtime_cleanup, last_sync, last_runtime_refresh, sync_check)

        return {
            "last_runtime_refresh": last_runtime_refresh,
            "last_runtime_cleanup": last_runtime_cleanup,
            "last_sync": last_sync,
            "sync_check": sync_check,
            "updated_at": float(updated_at) if isinstance(updated_at, (int, float)) else None,
        }