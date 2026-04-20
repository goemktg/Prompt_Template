#!/usr/bin/env python3
"""Session Gate MCP server -- enforces orchestrator work-loop phase transitions.

State machine:
  INIT -> ATOMIZE -> PLAN -> EXECUTE -> REPORT -> AWAIT -> FINALIZE

Provides tools for transition validation, gate checking, checkpoint recording,
session introspection, and emergency reset.  Persists state to disk so sessions
survive reconnects.  State file: <SESSION_GATE_STATE_DIR>/gate-state.json.
"""

# ---------------------------------------------------------------------------
# Tool alias note
# ---------------------------------------------------------------------------
# The ``ask_user`` tool (CLI / Copilot agent) and ``askQuestions`` (VS Code
# extension) are the same tool -- they both present a question to the human
# operator and return their response.
#
# All documentation in this server uses ``ask_user`` as the canonical name.
# The session-gate checks for the ``ask_user_called`` gate flag regardless of
# which concrete tool name was invoked by the orchestrator.
# ---------------------------------------------------------------------------

import json
import os
import sys
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

from mcp.server.fastmcp import FastMCP

_HOOK_SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "hooks" / "scripts"
if str(_HOOK_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_HOOK_SCRIPTS_DIR))

from session_state import derive_session_id, resolve_session_state_dir  # noqa: E402

try:
    import fcntl as _fcntl_mod
    _HAS_FLOCK = True
except ImportError:
    _fcntl_mod = None  # type: ignore[assignment]
    _HAS_FLOCK = False

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_FALLBACK_SESSION_ID = str(uuid.uuid4())
SESSION_ID = ""
STATE_DIR = Path(".")
STATE_FILE = Path("gate-state.json")

# ---------------------------------------------------------------------------
# State-machine definition
# ---------------------------------------------------------------------------

VALID_PHASES = {"INIT", "ATOMIZE", "PLAN", "EXECUTE", "REPORT", "AWAIT", "FINALIZE"}
DELEGATED_WRITE_LEASE_KEY = "delegated_write_lease"

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "INIT": {"ATOMIZE"},
    "ATOMIZE": {"PLAN", "ATOMIZE"},
    "PLAN": {"EXECUTE", "PLAN"},
    "EXECUTE": {"REPORT"},
    "REPORT": {"AWAIT"},
    "AWAIT": {"EXECUTE", "FINALIZE", "ATOMIZE"},
    "FINALIZE": set(),
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _log(msg: str) -> None:
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    print(f"[session-gate {ts}] {msg}", file=sys.stderr, flush=True)


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _resolve_state_binding() -> tuple[Path, str]:
    state_dir = resolve_session_state_dir(os.environ)
    derived_session_id = derive_session_id(state_dir, os.environ)
    return state_dir, derived_session_id or _FALLBACK_SESSION_ID


def _transition_required_actions(from_phase: str, to_phase: str, pending_gates: dict) -> list[str]:
    required_actions: list[str] = []

    if from_phase == "PLAN" and to_phase == "EXECUTE":
        if not pending_gates.get("plan_approved"):
            required_actions.append(
                "PLAN -> EXECUTE requires plan_approved=true. "
                "Present the plan via ask_user, receive plan approval, "
                "then set_gate_flag('plan_approved', true). "
                "For L0 tasks that skip plan presentation, self-approve by "
                "calling set_gate_flag('plan_approved', true) directly."
            )

    if from_phase == "REPORT" and to_phase == "AWAIT":
        if not pending_gates.get("ask_user_called"):
            required_actions.append(
                "REPORT -> AWAIT requires ask_user_called=true. "
                "Call ask_user, then set_gate_flag('ask_user_called', true)."
            )
        if not pending_gates.get("user_approved"):
            required_actions.append(
                "REPORT -> AWAIT requires user_approved=true. "
                "Receive explicit completion approval, then set_gate_flag('user_approved', true)."
            )

    if from_phase == "AWAIT" and to_phase == "EXECUTE":
        if not pending_gates.get("await_user_confirmed"):
            required_actions.append(
                "AWAIT -> EXECUTE requires await_user_confirmed=true. "
                "Call ask_user to confirm the follow-up task, then "
                "set_gate_flag('await_user_confirmed', true)."
            )

    if from_phase == "AWAIT" and to_phase == "FINALIZE":
        if not pending_gates.get("user_approved"):
            required_actions.append(
                f"AWAIT -> {to_phase} requires user_approved=true. "
                "Receive explicit user approval, then set_gate_flag('user_approved', true)."
            )

    return required_actions


def _transition_gate_summary(from_phase: str, to_phase: str, pending_gates: dict) -> dict:
    required_actions = _transition_required_actions(from_phase, to_phase, pending_gates)
    ask_user_required = False
    if from_phase == "PLAN" and to_phase == "EXECUTE":
        ask_user_required = not pending_gates.get("plan_approved")
    elif from_phase == "REPORT" and to_phase == "AWAIT":
        ask_user_required = not pending_gates.get("ask_user_called")
    elif from_phase == "AWAIT" and to_phase == "EXECUTE":
        ask_user_required = not pending_gates.get("await_user_confirmed")

    return {
        "from_phase": from_phase,
        "to_phase": to_phase,
        "required_actions": required_actions,
        "ask_user_required": ask_user_required,
        "gate_satisfied": not required_actions,
    }


# ---------------------------------------------------------------------------
# Session state management
# ---------------------------------------------------------------------------


class SessionState:
    """In-memory session state with JSON file persistence."""

    def __init__(self, state_file: Path, session_id: str) -> None:
        self.state_file = state_file
        self.session_id = session_id
        self._data: dict = {}
        self._load()

    # -- persistence -------------------------------------------------------

    def _blank_state(self) -> dict:
        return {
            "session_id": self.session_id,
            "current_phase": "INIT",
            "history": [],
            "checkpoints": [],
            "pending_gates": {},
            "report_state": {
                "active_checkpoint_id": None,
                "canonical_checkpoint_id": None,
            },
            "created_at": _now_iso(),
            "updated_at": _now_iso(),
        }

    @contextmanager
    def _locked_file(self):
        lock_path = Path(str(self.state_file) + ".lock")
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        with lock_path.open("a", encoding="utf-8") as lock_file:
            if _HAS_FLOCK and _fcntl_mod is not None:
                _fcntl_mod.flock(lock_file.fileno(), _fcntl_mod.LOCK_EX)
            try:
                yield
            finally:
                if _HAS_FLOCK and _fcntl_mod is not None:
                    _fcntl_mod.flock(lock_file.fileno(), _fcntl_mod.LOCK_UN)

    def _read_state_unlocked(self) -> dict | None:
        if not self.state_file.exists():
            return None
        try:
            data = json.loads(self.state_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, TypeError):
            return None
        return data if isinstance(data, dict) else None

    def _write_state_unlocked(self) -> None:
        self._data["updated_at"] = _now_iso()
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps(self._data, indent=2) + "\n", encoding="utf-8")

    def _load(self) -> None:
        with self._locked_file():
            data = self._read_state_unlocked()
            if data and data.get("session_id") == self.session_id:
                self._data = data
                _log(f"Resumed session {self.session_id} in phase {self.current_phase}")
                return
            self._data = self._blank_state()
            self._write_state_unlocked()
        _log(f"Initialised new session {self.session_id}")

    def refresh_from_disk(self) -> None:
        with self._locked_file():
            data = self._read_state_unlocked()
            if data and data.get("session_id") == self.session_id:
                self._data = data
                return
            self._data = self._blank_state()
            self._write_state_unlocked()

    def _save(self) -> None:
        with self._locked_file():
            self._write_state_unlocked()

    # -- accessors ---------------------------------------------------------

    @property
    def current_phase(self) -> str:
        return self._data["current_phase"]

    @current_phase.setter
    def current_phase(self, value: str) -> None:
        self._data["current_phase"] = value

    @property
    def history(self) -> list[dict]:
        return self._data["history"]

    @property
    def checkpoints(self) -> list[dict]:
        return self._data["checkpoints"]

    @property
    def pending_gates(self) -> dict:
        return self._data["pending_gates"]

    @property
    def report_state(self) -> dict:
        return self._data.setdefault("report_state", {
            "active_checkpoint_id": None,
            "canonical_checkpoint_id": None,
        })

    # -- mutations ---------------------------------------------------------

    def record_transition(self, from_phase: str, to_phase: str, reason: str) -> None:
        entry = {
            "from": from_phase,
            "to": to_phase,
            "reason": reason,
            "timestamp": _now_iso(),
            "gate_flags_at_transition": dict(self._data.get("pending_gates", {})),
        }
        self.history.append(entry)
        self.current_phase = to_phase
        self._data["pending_gates"] = {}
        if from_phase == "REPORT" and to_phase == "AWAIT":
            rs = self.report_state
            active_id = rs.get("active_checkpoint_id")
            if active_id:
                for cp in self.checkpoints:
                    if cp.get("checkpoint_id") == active_id:
                        cp["status"] = "canonical"
                        break
                rs["canonical_checkpoint_id"] = active_id
                rs["active_checkpoint_id"] = None
        self._save()

    def add_checkpoint(self, checkpoint: dict) -> None:
        if checkpoint.get("phase") == "REPORT":
            rs = self.report_state
            prev_active = rs.get("active_checkpoint_id")
            if prev_active:
                for cp in self.checkpoints:
                    if cp.get("checkpoint_id") == prev_active:
                        cp["status"] = "superseded"
                        break
            checkpoint["status"] = "candidate"
            rs["active_checkpoint_id"] = checkpoint["checkpoint_id"]
        self.checkpoints.append(checkpoint)
        self._save()

    def set_gate(self, key: str, value: object) -> None:
        self.pending_gates[key] = value
        if key == "delegated_write_permitted" and value is True:
            self.pending_gates[DELEGATED_WRITE_LEASE_KEY] = {
                "granted_at": _now_iso(),
                "consumed_at": None,
                "consumed_by": None,
            }
        self._save()

    def reset(self, reason: str) -> None:
        old = self._data.copy()
        self._data = self._blank_state()
        self._data["history"] = old.get("history", [])
        self._data["history"].append({
            "from": old.get("current_phase", "UNKNOWN"),
            "to": "INIT",
            "reason": f"FORCE_RESET: {reason}",
            "timestamp": _now_iso(),
        })
        self._save()

    def snapshot(self) -> dict:
        return dict(self._data)


# ---------------------------------------------------------------------------
# Instantiate global state + MCP server
# ---------------------------------------------------------------------------

state: SessionState | None = None


def _ensure_state(refresh: bool = True) -> SessionState:
    global state, SESSION_ID, STATE_DIR, STATE_FILE
    resolved_dir, resolved_session_id = _resolve_state_binding()
    resolved_state_file = resolved_dir / "gate-state.json"

    if (
        state is None
        or state.state_file != resolved_state_file
        or state.session_id != resolved_session_id
    ):
        SESSION_ID = resolved_session_id
        STATE_DIR = resolved_dir
        STATE_FILE = resolved_state_file
        state = SessionState(STATE_FILE, SESSION_ID)
    elif refresh:
        state.refresh_from_disk()

    return state


state = _ensure_state(refresh=False)
mcp = FastMCP("session-gate")

# ---------------------------------------------------------------------------
# MCP tools
# ---------------------------------------------------------------------------


@mcp.tool()
def phase_transition(from_phase: str, to_phase: str, reason: str) -> dict:
    """Validate and execute a phase transition in the orchestrator work loop.

    Args:
        from_phase: The phase the caller believes the session is in.
        to_phase:   The target phase to transition to.
        reason:     Human-readable explanation for the transition.

    Returns:
        dict with ``success``, ``current_phase``, and contextual info.
    """
    st = _ensure_state()
    from_phase = from_phase.upper().strip()
    to_phase = to_phase.upper().strip()

    if from_phase not in VALID_PHASES:
        return {
            "success": False,
            "error": f"Invalid from_phase '{from_phase}'. Must be one of: {sorted(VALID_PHASES)}",
            "current_phase": st.current_phase,
        }

    if to_phase not in VALID_PHASES:
        return {
            "success": False,
            "error": f"Invalid to_phase '{to_phase}'. Must be one of: {sorted(VALID_PHASES)}",
            "current_phase": st.current_phase,
        }

    if not reason or not reason.strip():
        return {
            "success": False,
            "error": "A non-empty reason is required for every transition.",
            "current_phase": st.current_phase,
        }

    if st.current_phase != from_phase:
        return {
            "success": False,
            "error": (
                f"Phase mismatch: session is in '{st.current_phase}', "
                f"but from_phase='{from_phase}' was provided."
            ),
            "current_phase": st.current_phase,
        }

    allowed = ALLOWED_TRANSITIONS.get(from_phase, set())
    if to_phase not in allowed:
        return {
            "success": False,
            "error": (
                f"Transition '{from_phase}' -> '{to_phase}' is not allowed. "
                f"Allowed targets from '{from_phase}': "
                f"{sorted(allowed) if allowed else '(none -- terminal state)'}."
            ),
            "current_phase": st.current_phase,
        }

    transition_gate = _transition_gate_summary(from_phase, to_phase, dict(st.pending_gates))
    if not transition_gate["gate_satisfied"]:
        required = " ".join(transition_gate["required_actions"])
        return {
            "success": False,
            "error": f"Gate violation for transition {from_phase} -> {to_phase}: {required}",
            "current_phase": st.current_phase,
            "pending_gates": dict(st.pending_gates),
            "required_actions": transition_gate["required_actions"],
        }

    st.record_transition(from_phase, to_phase, reason.strip())
    _log(f"Transition: {from_phase} -> {to_phase} | {reason.strip()}")

    return {
        "success": True,
        "previous_phase": from_phase,
        "current_phase": st.current_phase,
        "reason": reason.strip(),
        "timestamp": st.history[-1]["timestamp"],
        "session_id": st.session_id,
    }


@mcp.tool()
def check_gate(current_phase: str, next_phase: str | None = None) -> dict:
    """Check the gate requirements for the current phase.

    Args:
        current_phase: The phase the caller believes the session is in.
        next_phase: Optional target phase for transition-specific gate checks.

    Returns:
        dict with phase info, required actions, and whether ask_user is needed.
    """
    st = _ensure_state()
    current_phase = current_phase.upper().strip()
    normalized_next = next_phase.upper().strip() if isinstance(next_phase, str) else None

    if current_phase not in VALID_PHASES:
        return {
            "success": False,
            "error": f"Invalid phase '{current_phase}'. Must be one of: {sorted(VALID_PHASES)}",
        }

    if st.current_phase != current_phase:
        return {
            "success": False,
            "error": (
                f"Phase mismatch: session is in '{st.current_phase}', "
                f"but current_phase='{current_phase}' was provided."
            ),
            "current_phase": st.current_phase,
        }

    allowed_targets = sorted(ALLOWED_TRANSITIONS.get(current_phase, set()))
    if normalized_next is not None:
        if normalized_next not in VALID_PHASES:
            return {
                "success": False,
                "error": (
                    f"Invalid next_phase '{normalized_next}'. "
                    f"Must be one of: {sorted(VALID_PHASES)}"
                ),
                "current_phase": st.current_phase,
            }
        if normalized_next not in ALLOWED_TRANSITIONS.get(current_phase, set()):
            return {
                "success": False,
                "error": (
                    f"Transition '{current_phase}' -> '{normalized_next}' is not allowed. "
                    f"Allowed targets from '{current_phase}': "
                    f"{allowed_targets if allowed_targets else '(none -- terminal state)'}."
                ),
                "current_phase": st.current_phase,
            }

    targets_to_check = [normalized_next] if normalized_next else allowed_targets
    transition_requirements: dict[str, dict] = {}
    collected_required_actions: list[str] = []
    ask_user_required = False
    notes: list[str] = []

    for target in targets_to_check:
        summary = _transition_gate_summary(current_phase, target, dict(st.pending_gates))
        key = f"{current_phase}->{target}"
        transition_requirements[key] = summary
        collected_required_actions.extend(summary["required_actions"])
        ask_user_required = ask_user_required or summary["ask_user_required"]

    if normalized_next is not None:
        required_actions = list(dict.fromkeys(collected_required_actions))
    else:
        required_actions = []

    if current_phase == "FINALIZE":
        notes.append("Terminal state -- no further transitions allowed.")
    elif current_phase == "AWAIT" and normalized_next is None:
        notes.append(
            "AWAIT is a clean waiting state after REPORT -> AWAIT clears gate flags; "
            "AWAIT -> ATOMIZE is available without gating, "
            "AWAIT -> EXECUTE requires await_user_confirmed, "
            "and AWAIT -> FINALIZE requires user_approved."
        )
    elif normalized_next is None and collected_required_actions:
        notes.append(
            "Overview mode does not include transition-specific required_actions; "
            "inspect transition_requirements or pass next_phase for precise gating."
        )

    if normalized_next is not None:
        gate_key = f"{current_phase}->{normalized_next}"
        gate_satisfied = transition_requirements[gate_key]["gate_satisfied"]
    else:
        gate_satisfied = True if not targets_to_check else any(
            t["gate_satisfied"] for t in transition_requirements.values()
        )

    return {
        "success": True,
        "current_phase": st.current_phase,
        "next_phase": normalized_next,
        "allowed_transitions": allowed_targets,
        "transition_requirements": transition_requirements,
        "required_actions": required_actions,
        "ask_user_required": ask_user_required,
        "gate_satisfied": gate_satisfied,
        "notes": notes,
        "pending_gates": dict(st.pending_gates),
        "session_id": st.session_id,
    }


@mcp.tool()
def get_session_state() -> dict:
    """Return the full session state for introspection.

    Returns:
        dict with current phase, full transition history, checkpoints,
        pending gate flags, and session metadata.
    """
    st = _ensure_state()
    snapshot = st.snapshot()
    snapshot["checkpoint_count"] = len(st.checkpoints)
    snapshot["transition_count"] = len(st.history)
    snapshot["report_state"] = dict(st.report_state)
    return snapshot


@mcp.tool()
def record_checkpoint(phase: str, summary: str, key_decisions: list[str]) -> dict:
    """Record a checkpoint for the current work-loop phase.

    Args:
        phase:          The phase this checkpoint belongs to.
        summary:        Human-readable summary of progress at this point.
        key_decisions:  List of significant decisions made so far.

    Returns:
        dict with the checkpoint ID and confirmation.
    """
    st = _ensure_state()
    phase = phase.upper().strip()

    if phase not in VALID_PHASES:
        return {
            "success": False,
            "error": f"Invalid phase '{phase}'. Must be one of: {sorted(VALID_PHASES)}",
        }

    if not summary or not summary.strip():
        return {"success": False, "error": "A non-empty summary is required."}

    if not isinstance(key_decisions, list):
        return {"success": False, "error": "key_decisions must be a list of strings."}

    checkpoint_id = f"cp-{len(st.checkpoints) + 1:04d}"
    checkpoint = {
        "checkpoint_id": checkpoint_id,
        "phase": phase,
        "summary": summary.strip(),
        "key_decisions": [str(d).strip() for d in key_decisions if str(d).strip()],
        "timestamp": _now_iso(),
        "session_id": st.session_id,
    }

    st.add_checkpoint(checkpoint)
    _log(f"Checkpoint {checkpoint_id} recorded in phase {phase}")

    return {
        "success": True,
        "checkpoint_id": checkpoint_id,
        "phase": phase,
        "checkpoint_count": len(st.checkpoints),
        "timestamp": checkpoint["timestamp"],
        "session_id": st.session_id,
    }


@mcp.tool()
def set_gate_flag(flag: str, value: bool) -> dict:
    """Set a gate flag on the current phase.

    Allowed flags: ask_user_called, user_approved, await_user_confirmed,
    delegated_write_permitted, plan_approved.

    Args:
        flag:  Name of the gate flag to set.
        value: Boolean value for the flag.

    Returns:
        dict confirming the flag was set.
    """
    st = _ensure_state()
    allowed_flags = {
        "ask_user_called", "user_approved", "await_user_confirmed",
        "delegated_write_permitted", "plan_approved",
    }

    if flag not in allowed_flags:
        return {
            "success": False,
            "error": f"Unknown gate flag '{flag}'. Allowed flags: {sorted(allowed_flags)}",
            "current_phase": st.current_phase,
        }

    if not isinstance(value, bool):
        return {
            "success": False,
            "error": "value must be a boolean (true/false).",
            "current_phase": st.current_phase,
        }

    st.set_gate(flag, value)
    _log(f"Gate flag set: {flag}={value} in phase {st.current_phase}")

    return {
        "success": True,
        "flag": flag,
        "value": value,
        "current_phase": st.current_phase,
        "pending_gates": dict(st.pending_gates),
        "session_id": st.session_id,
    }


@mcp.tool()
def force_reset(reason: str, confirm: str) -> dict:
    """Emergency reset: return the session to INIT with a full audit trail.

    Args:
        reason:  Explanation for why the reset is necessary.
        confirm: Must be exactly ``"CONFIRM_RESET"`` to proceed.

    Returns:
        dict confirming the reset with audit information.
    """
    st = _ensure_state()
    if confirm != "CONFIRM_RESET":
        return {
            "success": False,
            "error": "Safety check: pass confirm='CONFIRM_RESET' to force reset. This is irreversible.",
        }

    if not reason or not reason.strip():
        return {
            "success": False,
            "error": "A non-empty reason is required for a force reset.",
        }

    previous_phase = st.current_phase
    st.reset(reason.strip())
    _log(f"FORCE RESET from {previous_phase}: {reason.strip()}")

    return {
        "success": True,
        "previous_phase": previous_phase,
        "current_phase": st.current_phase,
        "reason": reason.strip(),
        "timestamp": _now_iso(),
        "transition_count": len(st.history),
        "session_id": st.session_id,
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    _log(f"Starting session-gate server (session={SESSION_ID})")
    mcp.run(transport="stdio")
