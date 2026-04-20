#!/usr/bin/env python3
"""Unified preToolUse hook: INIT guard + safety check + loop detection.

Merges three separate hook scripts into one process to eliminate 2 Python
spawns per tool call. Execution phases are ordered for early exit:

  Phase 0: Parse stdin, extract tool name
  Phase 1: Exempt-tool gate (exit immediately for read-only tools)
  Phase 2: INIT-phase guard (deny mutating tools before ATOMIZE transition)
  Phase 2b: Completion guard (FINALIZE-only completion tools)
  Phase 2c: Session-gate mutation guard (EXECUTE phase)
  Phase 2d: REPORT-phase guard (block mutating tools in REPORT)
  Phase 2e: PLAN-phase guard (block execution tools in PLAN)
  Phase 2f: AWAIT-phase guard (block mutating tools in AWAIT)
  Phase 3: Safety regex check (shell tools only -- before any file I/O)
  Phase 4: Loop detection (single state file read/write)
"""
import json
import sys

# ---------------------------------------------------------------------------
# Phase 0: Parse input
# ---------------------------------------------------------------------------

def _load_input():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)
    if not isinstance(data, dict):
        sys.exit(0)
    return data

_INPUT = _load_input()
_TOOL_NAME = str(_INPUT.get("toolName") or _INPUT.get("tool_name") or "")


def _emit(decision, reason):
    print(json.dumps({
        "permissionDecision": decision,
        "permissionDecisionReason": reason,
    }))

# ---------------------------------------------------------------------------
# Phase 1: Exempt-tool early exit
# ---------------------------------------------------------------------------

EXEMPT_TOOLS = {
    "view", "glob", "grep", "rg",
    "read_bash", "list_bash",
    "read_agent", "list_agents",
    "report_intent", "think", "ask_user",
    "store_memory", "fetch_copilot_cli_documentation",
    "sql", "web_fetch",
    # session-gate read-only tools are exempt (no side effects).
    # Mutation tools remain subject to hook guards and loop detection.
    "session-gate-check_gate", "session-gate-get_session_state",
}
EXEMPT_PREFIXES = ("memory-", "context7-", "tavily-",
                   "arxiv-", "github-mcp-server-")

if _TOOL_NAME in EXEMPT_TOOLS or any(_TOOL_NAME.startswith(p) for p in EXEMPT_PREFIXES):
    sys.exit(0)

# ---------------------------------------------------------------------------
# Phase 2: INIT-phase guard (deny mutating tools before ATOMIZE)
# ---------------------------------------------------------------------------

import os as _os_early  # noqa: E402
import re as _re_early  # noqa: E402
from datetime import datetime as _datetime_early, timezone as _timezone_early  # noqa: E402
from pathlib import Path as _Path_early  # noqa: E402

try:
    import fcntl as _fcntl_early
    _HAS_FLOCK = True
except ImportError:
    _fcntl_early = None  # type: ignore[assignment]
    _HAS_FLOCK = False

_SCRIPTS_DIR_EARLY = _Path_early(__file__).resolve().parent
if str(_SCRIPTS_DIR_EARLY) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR_EARLY))

from session_state import (  # noqa: E402
    derive_session_id as _derive_session_id_early,
    resolve_session_state_dir as _resolve_state_dir_shared_early,
)

INIT_MUTATING_TOOLS = {"bash", "task", "apply_patch", "edit", "create", "shell",
                       "powershell", "execute", "write_bash"}

# Single-use INIT bootstrap lease allowlist when delegated_write_permitted is true.
INIT_BOOTSTRAP_TOOLS = {"apply_patch", "edit", "create"}
LEGACY_INIT_BOOTSTRAP_TOOLS = {"task", "apply_patch", "edit", "create"}


def _resolve_session_state_dir():
    return _resolve_state_dir_shared_early(_os_early.environ)


def _resolve_session_gate_state_file():
    return _resolve_session_state_dir() / "gate-state.json"


def _load_session_gate_state_unlocked(state_file):
    if not state_file.exists():
        return {"current_phase": "INIT", "_state_reason": "missing"}
    try:
        with state_file.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception:
        return {"current_phase": "INIT", "_state_reason": "unreadable"}
    if not isinstance(data, dict):
        return {"current_phase": "INIT", "_state_reason": "invalid"}
    expected_session_id = _derive_session_id_early(
        _resolve_session_state_dir(), _os_early.environ
    )
    actual_session_id = data.get("session_id")
    if expected_session_id:
        if not isinstance(actual_session_id, str) or not actual_session_id.strip():
            return {"current_phase": "INIT", "_state_reason": "missing_session_id"}
        if actual_session_id != expected_session_id:
            return {"current_phase": "INIT", "_state_reason": "session_mismatch"}
    return data


def _load_session_gate_state(state_file):
    lock_path = _Path_early(f"{state_file}.lock")
    try:
        _os_early.makedirs(lock_path.parent, exist_ok=True)
        with lock_path.open("a", encoding="utf-8") as lock_fh:
            if _HAS_FLOCK and _fcntl_early is not None:
                _fcntl_early.flock(lock_fh.fileno(), _fcntl_early.LOCK_SH)
            return _load_session_gate_state_unlocked(state_file)
    except Exception:
        return {"current_phase": "INIT", "_state_reason": "unreadable"}


def _now_iso_early():
    return _datetime_early.now(_timezone_early.utc).isoformat()


def _extract_bootstrap_path(tool_name, tool_args):
    try:
        payload = json.loads(tool_args) if isinstance(tool_args, str) else tool_args
    except Exception:
        payload = tool_args

    if isinstance(payload, dict):
        for key in ("path", "file_path", "target_file", "targetPath"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()

    if tool_name == "apply_patch" and isinstance(tool_args, str):
        match = _re_early.search(
            r"^\*\*\* (?:Update|Add|Delete) File: (.+)$",
            tool_args,
            _re_early.MULTILINE,
        )
        if match:
            return match.group(1).strip()

    return None


def _persist_consumed_bootstrap_lease(state_file, tool_name, tool_args):
    lock_path = _Path_early(f"{state_file}.lock")
    try:
        _os_early.makedirs(lock_path.parent, exist_ok=True)
        with lock_path.open("a", encoding="utf-8") as lock_fh:
            if _HAS_FLOCK and _fcntl_early is not None:
                _fcntl_early.flock(lock_fh.fileno(), _fcntl_early.LOCK_EX)

            gate = _load_session_gate_state_unlocked(state_file)
            pending = gate.setdefault("pending_gates", {})
            if not pending.get("delegated_write_permitted"):
                return False, None

            lease = pending.get("delegated_write_lease")
            if not isinstance(lease, dict):
                lease = {
                    "granted_at": gate.get("updated_at") or _now_iso_early(),
                    "consumed_at": None,
                    "consumed_by": None,
                }

            if lease.get("consumed_at"):
                return False, None

            lease["granted_at"] = (
                lease.get("granted_at") or gate.get("updated_at") or _now_iso_early()
            )
            lease["consumed_at"] = _now_iso_early()
            lease["consumed_by"] = tool_name
            consumed_path = _extract_bootstrap_path(tool_name, tool_args)
            if consumed_path:
                lease["consumed_path"] = consumed_path
            else:
                lease.pop("consumed_path", None)

            pending["delegated_write_permitted"] = False
            pending["delegated_write_lease"] = lease
            gate["updated_at"] = _now_iso_early()

            state_file.parent.mkdir(parents=True, exist_ok=True)
            with state_file.open("w", encoding="utf-8") as fh:
                json.dump(gate, fh, ensure_ascii=False, indent=2)
                fh.write("\n")

            return True, None
    except Exception as exc:
        return False, str(exc)


def _check_init_phase():
    if _TOOL_NAME not in INIT_MUTATING_TOOLS:
        return
    state_file = _resolve_session_gate_state_file()
    gate = _load_session_gate_state(state_file)
    if str(gate.get("current_phase", "INIT")).upper() == "INIT":
        pending = gate.get("pending_gates", {})
        bootstrap_tools = (
            INIT_BOOTSTRAP_TOOLS
            if isinstance(pending.get("delegated_write_lease"), dict)
            else LEGACY_INIT_BOOTSTRAP_TOOLS
        )
        if pending.get("delegated_write_permitted") and _TOOL_NAME in bootstrap_tools:
            consumed, error = _persist_consumed_bootstrap_lease(
                state_file,
                _TOOL_NAME,
                _INPUT.get("toolArgs", _INPUT.get("tool_input", {})),
            )
            if consumed:
                return
            if error:
                _emit(
                    "deny",
                    "[INIT GUARD] Delegated write lease could not be persisted during "
                    f"INIT bootstrap consumption; denying tool. Error: {error}",
                )
                sys.exit(0)
        state_reason = gate.get("_state_reason")
        state_hint = ""
        if state_reason == "missing":
            state_hint = " No session-gate state exists yet."
        elif state_reason in {"unreadable", "invalid"}:
            state_hint = " Session-gate state could not be read."
        elif state_reason in {"missing_session_id", "session_mismatch"}:
            state_hint = " Session-gate state did not match the active session."
        _emit(
            "deny",
            "[INIT GUARD] Session is still in INIT phase. Mutating tools are "
            "blocked until the orchestrator calls: session-gate "
            'phase_transition("INIT", "ATOMIZE", reason). '
            "To bootstrap one delegated repo-file write before ATOMIZE, set "
            "delegated_write_permitted=true via session-gate for edit/create/"
            f"apply_patch.{state_hint}",
        )
        sys.exit(0)


_check_init_phase()

# ---------------------------------------------------------------------------
# Phase 2b: Completion guard (FINALIZE-only completion tools)
# ---------------------------------------------------------------------------

COMPLETION_TOOLS = {"task_complete", "attempt_completion"}


def _check_completion_gate():
    if _TOOL_NAME not in COMPLETION_TOOLS:
        return
    gate = _load_session_gate_state(_resolve_session_gate_state_file())
    phase = str(gate.get("current_phase", "INIT")).upper()
    pending = gate.get("pending_gates", {})
    if phase == "FINALIZE":
        return
    _emit(
        "deny",
        "[COMPLETION GUARD] Completion tools are blocked unless the session "
        "is in FINALIZE. AWAIT is the resting state for new follow-up tasks "
        "and must not end the session. To end the session, explicitly "
        "transition AWAIT -> FINALIZE first. "
        f"Current phase: {phase}. Pending gates: {pending}",
    )
    sys.exit(0)


_check_completion_gate()

# ---------------------------------------------------------------------------
# Phase 2c: Session-gate mutation guard (EXECUTE phase)
# ---------------------------------------------------------------------------

SESSION_GATE_STATE_GUARD_TOOLS = {
    "session-gate-set_gate_flag",
    "session-gate-force_reset",
}


def _check_session_gate_mutation_guard():
    if _TOOL_NAME not in SESSION_GATE_STATE_GUARD_TOOLS:
        return
    gate = _load_session_gate_state(_resolve_session_gate_state_file())
    phase = str(gate.get("current_phase", "INIT")).upper()
    if phase == "EXECUTE":
        _emit(
            "deny",
            "[SESSION-GATE GUARD] session-gate approval-flag and reset tools are blocked "
            "during EXECUTE phase. Only the outer orchestrator may set gate flags or reset "
            "session state. Council subagents must return analytical payloads only and must "
            "not mutate session-gate state. "
            f"Current phase: {phase}. Tool: {_TOOL_NAME}.",
        )
        sys.exit(0)


_check_session_gate_mutation_guard()

# ---------------------------------------------------------------------------
# Phase 2d: REPORT-phase guard (block mutating tools in REPORT)
# ---------------------------------------------------------------------------

REPORT_BLOCKED_TOOLS = {
    "bash", "task", "apply_patch", "edit", "create",
    "shell", "powershell", "execute", "write_bash",
}


def _check_report_phase_guard():
    if _TOOL_NAME not in REPORT_BLOCKED_TOOLS:
        return
    gate = _load_session_gate_state(_resolve_session_gate_state_file())
    phase = str(gate.get("current_phase", "INIT")).upper()
    if phase != "REPORT":
        return
    _emit(
        "deny",
        "[REPORT GUARD] Mutating tools are blocked during REPORT phase. "
        "REPORT is an approval boundary -- present results via ask_user and "
        "wait for user approval. Set gate flags (ask_user_called, "
        "user_approved) then transition REPORT -> AWAIT to resume work. "
        f"Current phase: {phase}. Blocked tool: {_TOOL_NAME}.",
    )
    sys.exit(0)


_check_report_phase_guard()

# ---------------------------------------------------------------------------
# Phase 2e: PLAN-phase guard (block execution tools in PLAN)
# ---------------------------------------------------------------------------

PLAN_BLOCKED_TOOLS = {
    "bash", "shell", "powershell", "execute", "write_bash",
}


def _check_plan_phase_guard():
    if _TOOL_NAME not in PLAN_BLOCKED_TOOLS:
        return
    gate = _load_session_gate_state(_resolve_session_gate_state_file())
    phase = str(gate.get("current_phase", "INIT")).upper()
    if phase != "PLAN":
        return
    _emit(
        "deny",
        "[PLAN GUARD] Execution tools are blocked during PLAN phase. "
        "Build and present the plan via ask_user, receive plan approval, "
        "then set_gate_flag('plan_approved', true) and transition "
        "PLAN -> EXECUTE to begin work. "
        f"Current phase: {phase}. Blocked tool: {_TOOL_NAME}.",
    )
    sys.exit(0)


_check_plan_phase_guard()

# ---------------------------------------------------------------------------
# Phase 2f: AWAIT-phase guard (block mutating tools in AWAIT)
# ---------------------------------------------------------------------------

AWAIT_BLOCKED_TOOLS = {
    "bash", "task", "apply_patch", "edit", "create",
    "shell", "powershell", "execute", "write_bash",
}


def _check_await_phase_guard():
    if _TOOL_NAME not in AWAIT_BLOCKED_TOOLS:
        return
    gate = _load_session_gate_state(_resolve_session_gate_state_file())
    phase = str(gate.get("current_phase", "INIT")).upper()
    if phase != "AWAIT":
        return
    _emit(
        "deny",
        "[AWAIT GUARD] Mutating tools are blocked during AWAIT phase. "
        "AWAIT is a fully resting state -- transition AWAIT -> ATOMIZE "
        "before beginning work. Call: session-gate "
        'phase_transition("AWAIT", "ATOMIZE", reason). '
        f"Current phase: {phase}. Blocked tool: {_TOOL_NAME}.",
    )
    sys.exit(0)


_check_await_phase_guard()

# ---------------------------------------------------------------------------
# Phase 3: Safety check (shell tools only)
# ---------------------------------------------------------------------------

SHELL_TOOLS = {"bash", "shell", "powershell", "execute"}


def _extract_command(tool_args):
    try:
        payload = json.loads(tool_args) if isinstance(tool_args, str) else tool_args
    except Exception:
        payload = {}
    if isinstance(payload, dict):
        for key in ("command", "cmd"):
            value = payload.get(key)
            if isinstance(value, str):
                return value
    return tool_args if isinstance(tool_args, str) else ""


if _TOOL_NAME in SHELL_TOOLS:
    import re  # noqa: E402

    DENY_PATTERNS = [
        (re.compile(r"\brm\s+(-[a-zA-Z]*f[a-zA-Z]*\s+)?/"), "rm with absolute path detected."),
        (re.compile(r"\brm\s+-rf\s+~(?:/|\b)"), "Destructive home directory deletion detected."),
        (re.compile(r"\brm\s+-rf\b"), "Recursive force-remove detected."),
        (re.compile(r"\bgit\s+push\s+(--force|-f)\b"), "git push --force rewrites remote history."),
        (re.compile(r"\bgit\s+reset\s+--hard\b"), "git reset --hard discards uncommitted changes."),
        (re.compile(r"\bmkfs(?:\.\w+)?\b"), "Filesystem formatting command detected."),
        (re.compile(r"\bdd\s+if="), "Raw disk overwrite command detected."),
        (re.compile(r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:"), "Fork bomb detected."),
        (re.compile(r"\bchmod\s+(-R\s+)?777\s+/"), "Unsafe permission change on root detected."),
        (re.compile(r">\s*/dev/sd[a-z]\b"), "Direct disk device overwrite detected."),
        (re.compile(r"\bDROP\s+(TABLE|DATABASE)\b", re.IGNORECASE), "SQL DROP TABLE/DATABASE detected."),
        (re.compile(r"\bTRUNCATE\s+TABLE\b", re.IGNORECASE), "SQL TRUNCATE TABLE detected."),
        (re.compile(r"\bcurl\s+.*\|\s*(ba)?sh\b"), "curl pipe to shell detected."),
        (re.compile(r"\bwget\s+.*\|\s*(ba)?sh\b"), "wget pipe to shell detected."),
    ]
    ASK_PATTERNS = [
        (re.compile(r"\bsudo\b"), "Command requires elevated privileges."),
        (re.compile(r"\bgit\s+push\b"), "Command will push commits to a remote repository."),
        (re.compile(r"\bgit\s+rebase\b"), "Command rewrites git history."),
        (re.compile(r"\bgit\s+merge\b"), "Command merges branches -- verify target."),
        (re.compile(r"\bkill\s+-9\b"), "Forceful process termination detected."),
        (re.compile(r"\bnpm\s+publish\b"), "Command will publish a package."),
        (re.compile(r"\bdocker\s+(rm|rmi|system\s+prune)\b"), "Command removes Docker resources."),
        (re.compile(r"\bkubectl\s+delete\b"), "Command deletes Kubernetes resources."),
        (re.compile(r"\bchmod\s+777\b"), "Command grants world-writable permissions."),
    ]

    command = _extract_command(_INPUT.get("toolArgs", {}))
    if command:
        for pattern, reason in DENY_PATTERNS:
            if pattern.search(command):
                _emit("deny", f"{reason} Command: {command}")
                sys.exit(0)
        for pattern, reason in ASK_PATTERNS:
            if pattern.search(command):
                _emit("ask", f"{reason} Command: {command}")
                sys.exit(0)

# ---------------------------------------------------------------------------
# Phase 4: Loop detection (shared state I/O)
# ---------------------------------------------------------------------------

import hashlib    # noqa: E402
import os         # noqa: E402
from contextlib import contextmanager  # noqa: E402
from datetime import datetime, timezone  # noqa: E402
from pathlib import Path  # noqa: E402


def _get_session_dir():
    return Path(_resolve_session_state_dir())


SESSION_DIR = _get_session_dir()
STATE_FILE = SESSION_DIR / "unified-hook-state.json"
DECISIONS_FILE = SESSION_DIR / "unified-hook-decisions.jsonl"


@contextmanager
def _locked(path: Path):
    lock_path = Path(str(path) + ".lock")
    os.makedirs(lock_path.parent, exist_ok=True)
    with lock_path.open("a", encoding="utf-8") as fh:
        if _HAS_FLOCK and _fcntl_early is not None:
            _fcntl_early.flock(fh.fileno(), _fcntl_early.LOCK_EX)
        try:
            yield
        finally:
            if _HAS_FLOCK and _fcntl_early is not None:
                _fcntl_early.flock(fh.fileno(), _fcntl_early.LOCK_UN)


def _read_json(path, default):
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return default


def _write_json(path, data):
    os.makedirs(path.parent, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False)


def _append_jsonl(path, record):
    os.makedirs(path.parent, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _default_state():
    return {"loop_window": []}


WINDOW_SIZE = 10
LOOP_DENY_THRESHOLD = 7
LOOP_ASK_THRESHOLD = 5
OSCILLATION_LENGTH = 4


def _hash_call(tool_name, tool_args):
    normalized = json.dumps({"t": tool_name, "a": tool_args}, sort_keys=True)
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


def _trailing_repeat_count(window, current_hash):
    count = 0
    for entry in reversed(window):
        if entry.get("hash") == current_hash:
            count += 1
        else:
            break
    return count


def _trailing_oscillation_length(window):
    if len(window) < 4:
        return 0
    hashes = [e.get("hash", "") for e in window]
    for period in range(2, len(hashes) // 2 + 1):
        pattern = hashes[-period:]
        matched = 0
        for i in range(period, len(hashes)):
            if hashes[-(i + 1)] == pattern[-(((i - period) % period) + 1)]:
                matched += 1
            else:
                break
        if matched >= period:
            return matched + period
    return 0


def _check_loop(state, tool_args):
    current_hash = _hash_call(_TOOL_NAME, tool_args)
    window = state.get("loop_window", [])

    if len(window) < 2:
        window.append({"hash": current_hash, "tool": _TOOL_NAME})
        if len(window) > WINDOW_SIZE:
            window[:] = window[-WINDOW_SIZE:]
        state["loop_window"] = window
        return None, None

    repeat_count = _trailing_repeat_count(window, current_hash)
    oscillation_len = _trailing_oscillation_length(window)

    window.append({"hash": current_hash, "tool": _TOOL_NAME})
    if len(window) > WINDOW_SIZE:
        window[:] = window[-WINDOW_SIZE:]
    state["loop_window"] = window

    if repeat_count >= LOOP_DENY_THRESHOLD:
        return "deny", (
            f"Loop detected: {repeat_count + 1} consecutive identical "
            f"'{_TOOL_NAME}' calls. Try a different approach."
        )
    if repeat_count >= LOOP_ASK_THRESHOLD:
        return "ask", (
            f"Possible loop: {repeat_count + 1} consecutive identical "
            f"'{_TOOL_NAME}' calls. Consider changing strategy."
        )
    if oscillation_len >= OSCILLATION_LENGTH:
        return "ask", (
            f"Oscillation detected: {oscillation_len}-step repeating pattern "
            f"in tool calls. Consider a different approach."
        )

    return None, None


def main():
    tool_args = _INPUT.get("toolArgs", _INPUT.get("tool_input", {}))

    try:
        with _locked(STATE_FILE):
            raw_state = _read_json(STATE_FILE, _default_state())
            state = {
                "loop_window": raw_state.get("loop_window", [])
                if isinstance(raw_state, dict) else []
            }

            loop_decision, loop_reason = _check_loop(state, tool_args)
            _write_json(STATE_FILE, state)

        if loop_decision:
            _append_jsonl(DECISIONS_FILE, {
                "ts": _now_iso(),
                "tool": _TOOL_NAME,
                "decision": loop_decision,
                "source": "loop",
                "reason": loop_reason,
            })
            _emit(loop_decision, loop_reason)

    except Exception:
        pass  # Fail open -- never block the model due to hook errors


if __name__ == "__main__":
    main()
