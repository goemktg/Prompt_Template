#!/usr/bin/env python3
"""sessionStart hook: initialize session-gate-adjacent state for the current session."""

from __future__ import annotations

import json
import os
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from session_state import resolve_session_state_dir  # noqa: E402

try:
    import fcntl as _fcntl_mod
    _HAS_FLOCK = True
except ImportError:
    _fcntl_mod = None
    _HAS_FLOCK = False


def _get_session_dir() -> Path:
    return resolve_session_state_dir()


SESSION_DIR = _get_session_dir()
MEMORY_ROOT = Path.home() / ".copilot" / "memory"
SESSIONS_LOG = SESSION_DIR / "sessions.jsonl"
UNIFIED_STATE_FILE = SESSION_DIR / "unified-hook-state.json"
UNIFIED_DECISIONS_FILE = SESSION_DIR / "unified-hook-decisions.jsonl"


def load_input() -> dict:
    try:
        input_data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)
    if not isinstance(input_data, dict):
        sys.exit(0)
    return input_data


def to_iso(timestamp_ms: object) -> str:
    try:
        return datetime.fromtimestamp(
            float(timestamp_ms) / 1000.0, tz=timezone.utc  # type: ignore[arg-type]
        ).isoformat()
    except Exception:
        return datetime.now(timezone.utc).isoformat()


@contextmanager
def locked(path: Path):
    lock_path = Path(str(path) + ".lock")
    os.makedirs(lock_path.parent, exist_ok=True)
    with lock_path.open("a", encoding="utf-8") as lock_file:
        if _HAS_FLOCK and _fcntl_mod is not None:
            _fcntl_mod.flock(lock_file.fileno(), _fcntl_mod.LOCK_EX)
        try:
            yield
        finally:
            if _HAS_FLOCK and _fcntl_mod is not None:
                _fcntl_mod.flock(lock_file.fileno(), _fcntl_mod.LOCK_UN)


def write_json(path: Path, data: object) -> None:
    os.makedirs(path.parent, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False)


def append_jsonl(path: Path, record: object) -> None:
    os.makedirs(path.parent, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def truncate_file(path: Path) -> None:
    os.makedirs(path.parent, exist_ok=True)
    with path.open("w", encoding="utf-8"):
        pass


def find_git_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return current


def count_memories(memory_file: Path) -> int:
    try:
        content = memory_file.read_text(encoding="utf-8")
    except Exception:
        return 0
    return sum(1 for line in content.splitlines() if line.strip())


def main() -> int:
    try:
        input_data = load_input()
        cwd = Path(str(input_data.get("cwd", "."))).expanduser()
        project_root = find_git_root(cwd)
        project_name = project_root.name or "project"
        memory_file = MEMORY_ROOT / project_name / "MEMORY.md"
        memory_count = count_memories(memory_file) if memory_file.exists() else 0
        memory_message = ""
        if memory_file.exists():
            memory_message = f"Memory context available: {memory_count} memories"

        # Reset unified pre-hook state files so each session starts clean.
        with locked(UNIFIED_STATE_FILE):
            write_json(UNIFIED_STATE_FILE, {"loop_window": []})
        with locked(UNIFIED_DECISIONS_FILE):
            truncate_file(UNIFIED_DECISIONS_FILE)

        record: dict = {
            "event": "start",
            "ts": to_iso(input_data.get("timestamp")),
            "cwd": str(cwd),
            "source": input_data.get("source"),
            "initialPrompt": input_data.get("initialPrompt"),
            "project": project_name,
        }
        if memory_message:
            record["message"] = memory_message
            record["memory_count"] = memory_count

        with locked(SESSIONS_LOG):
            append_jsonl(SESSIONS_LOG, record)
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
