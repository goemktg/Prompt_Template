#!/usr/bin/env python3
"""Minimal cross-platform session gate MCP server for mediator-capable runtime flows."""

from __future__ import annotations

import json
import os
import tempfile
import threading
from pathlib import Path
from time import gmtime, strftime
from typing import Any

from mcp.server.fastmcp import FastMCP

VALID_PHASES = ("INIT", "ATOMIZE", "PLAN", "EXECUTE", "REPORT", "AWAIT", "FINALIZE")
ALLOWED_TRANSITIONS = {
    "INIT": {"ATOMIZE"},
    "ATOMIZE": {"PLAN", "ATOMIZE"},
    "PLAN": {"EXECUTE", "PLAN"},
    "EXECUTE": {"REPORT"},
    "REPORT": {"AWAIT"},
    "AWAIT": {"EXECUTE", "FINALIZE", "ATOMIZE"},
    "FINALIZE": set(),
}
_STATE_LOCK = threading.Lock()


def _now_iso() -> str:
    return strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())


def _resolve_base_dir() -> Path:
    configured = os.environ.get("SESSION_GATE_STATE_DIR", ".copilot-runtime/session-gate")
    expanded = Path(os.path.expanduser(configured))
    if not expanded.is_absolute():
        expanded = Path.cwd() / expanded
    expanded.mkdir(parents=True, exist_ok=True)
    return expanded


def _session_id() -> str:
    return os.environ.get("SESSION_GATE_SESSION_ID", "default").strip() or "default"


def _state_file() -> Path:
    return _resolve_base_dir() / f"{_session_id()}.json"


def _default_state() -> dict[str, Any]:
    return {
        "session_id": _session_id(),
        "current_phase": "INIT",
        "history": [],
        "pending_gates": {},
        "updated_at": _now_iso(),
    }


def _write_state(state: dict[str, Any]) -> None:
    target = _state_file()
    target.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = _now_iso()
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=target.parent, delete=False) as handle:
        json.dump(state, handle, indent=2)
        handle.write("\n")
        temp_name = handle.name
    os.replace(temp_name, target)


def _load_state() -> dict[str, Any]:
    target = _state_file()
    with _STATE_LOCK:
        if target.exists():
            try:
                data = json.loads(target.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                data = _default_state()
            if isinstance(data, dict) and data.get("session_id") == _session_id():
                data.setdefault("history", [])
                data.setdefault("pending_gates", {})
                data.setdefault("current_phase", "INIT")
                data.setdefault("updated_at", _now_iso())
                return data
        data = _default_state()
        _write_state(data)
        return data


def _save_state(state: dict[str, Any]) -> None:
    with _STATE_LOCK:
        _write_state(state)


def _required_gate_actions(from_phase: str, to_phase: str, pending_gates: dict[str, Any]) -> list[str]:
    actions: list[str] = []
    if from_phase == "PLAN" and to_phase == "EXECUTE" and not pending_gates.get("plan_approved"):
        actions.append("PLAN -> EXECUTE requires plan_approved=true.")
    if from_phase == "REPORT" and to_phase == "AWAIT":
        if not pending_gates.get("ask_user_called"):
            actions.append("REPORT -> AWAIT requires ask_user_called=true.")
        if not pending_gates.get("user_approved"):
            actions.append("REPORT -> AWAIT requires user_approved=true.")
    if from_phase == "AWAIT" and to_phase == "EXECUTE" and not pending_gates.get("await_user_confirmed"):
        actions.append("AWAIT -> EXECUTE requires await_user_confirmed=true.")
    if from_phase == "AWAIT" and to_phase == "FINALIZE" and not pending_gates.get("user_approved"):
        actions.append("AWAIT -> FINALIZE requires user_approved=true.")
    return actions


mcp = FastMCP(
    "session-gate",
    instructions=(
        "Lifecycle phase gate for orchestrator-style runtime loops. "
        "Use validate_transition before phase_transition when a caller needs a dry run."
    ),
)


@mcp.tool()
def get_session_state() -> dict[str, Any]:
    """Return the persisted lifecycle state for the current session id."""
    return _load_state()


@mcp.tool()
def set_gate_flag(name: str, value: bool = True) -> dict[str, Any]:
    """Set or clear a named gate flag in the current session state."""
    state = _load_state()
    state.setdefault("pending_gates", {})[name] = value
    _save_state(state)
    return {
        "success": True,
        "current_phase": state["current_phase"],
        "pending_gates": state["pending_gates"],
    }


@mcp.tool()
def validate_transition(from_phase: str, to_phase: str) -> dict[str, Any]:
    """Check whether a phase change is allowed and which gate actions are still required."""
    state = _load_state()
    normalized_from = from_phase.upper().strip()
    normalized_to = to_phase.upper().strip()

    if normalized_from not in VALID_PHASES:
        return {"success": False, "error": f"Invalid from_phase: {from_phase}", "current_phase": state["current_phase"]}
    if normalized_to not in VALID_PHASES:
        return {"success": False, "error": f"Invalid to_phase: {to_phase}", "current_phase": state["current_phase"]}

    allowed = normalized_to in ALLOWED_TRANSITIONS.get(normalized_from, set())
    gate_actions = _required_gate_actions(normalized_from, normalized_to, state.get("pending_gates", {}))
    return {
        "success": True,
        "current_phase": state["current_phase"],
        "allowed": allowed,
        "gate_satisfied": not gate_actions,
        "required_actions": gate_actions,
    }


@mcp.tool()
def phase_transition(from_phase: str, to_phase: str, reason: str) -> dict[str, Any]:
    """Apply a validated lifecycle phase change and record the transition reason in history."""
    state = _load_state()
    normalized_from = from_phase.upper().strip()
    normalized_to = to_phase.upper().strip()

    if normalized_from not in VALID_PHASES or normalized_to not in VALID_PHASES:
        return {"success": False, "error": "Invalid phase value.", "current_phase": state["current_phase"]}
    if state["current_phase"] != normalized_from:
        return {
            "success": False,
            "error": f"Phase mismatch: current phase is {state['current_phase']}",
            "current_phase": state["current_phase"],
        }
    if normalized_to not in ALLOWED_TRANSITIONS.get(normalized_from, set()):
        return {
            "success": False,
            "error": f"Transition {normalized_from} -> {normalized_to} is not allowed.",
            "current_phase": state["current_phase"],
        }

    gate_actions = _required_gate_actions(normalized_from, normalized_to, state.get("pending_gates", {}))
    if gate_actions:
        return {
            "success": False,
            "error": "Transition blocked by pending gates.",
            "required_actions": gate_actions,
            "current_phase": state["current_phase"],
        }

    state.setdefault("history", []).append(
        {
            "from": normalized_from,
            "to": normalized_to,
            "reason": reason.strip() or "unspecified",
            "timestamp": _now_iso(),
        }
    )
    state["current_phase"] = normalized_to
    state["pending_gates"] = {}
    _save_state(state)
    return {
        "success": True,
        "current_phase": state["current_phase"],
        "history_length": len(state["history"]),
    }


@mcp.tool()
def reset_session(reason: str = "manual reset") -> dict[str, Any]:
    """Reset the current session state to INIT and append a reset entry to history."""
    state = _default_state()
    state["history"].append(
        {
            "from": "UNKNOWN",
            "to": "INIT",
            "reason": f"RESET: {reason}",
            "timestamp": _now_iso(),
        }
    )
    _save_state(state)
    return {"success": True, "current_phase": "INIT", "session_id": state["session_id"]}


if __name__ == "__main__":
    mcp.run(transport="stdio")