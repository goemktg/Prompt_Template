#!/usr/bin/env python3
"""sessionEnd hook: audit session state and run runtime cleanup."""

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

_REPO_ROOT = Path(__file__).resolve().parents[3]
_REPO_SCRIPTS_DIR = _REPO_ROOT / "scripts"
if str(_REPO_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_REPO_SCRIPTS_DIR))

from session_state import resolve_session_state_dir  # noqa: E402
from cleanup_runtime_artifacts import cleanup_runtime_artifacts  # noqa: E402

try:
    import fcntl as _fcntl_mod
    _HAS_FLOCK = True
except ImportError:
    _fcntl_mod = None
    _HAS_FLOCK = False


def _get_session_dir() -> Path:
    return resolve_session_state_dir()


SESSION_DIR = _get_session_dir()
SESSIONS_LOG = SESSION_DIR / "sessions.jsonl"
SUMMARY_FILE = SESSION_DIR / "session-summary.json"
TRACKER_STATS_FILE = SESSION_DIR / "tool-tracker-stats.json"
PROMPT_STATS_FILE = SESSION_DIR / "prompt-stats.json"
ERROR_STATE_FILE = SESSION_DIR / "error-state.json"
CHANGED_FILES_FILE = SESSION_DIR / "changed-files.json"


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


def read_json(path: Path, default: object) -> object:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return default


def write_json(path: Path, data: object) -> None:
    os.makedirs(path.parent, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)


def append_jsonl(path: Path, record: object) -> None:
    os.makedirs(path.parent, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def _workspace_from_payload(payload: dict) -> Path | None:
    for key in ("cwd", "workspace", "workspacePath", "workspace_root"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            candidate = Path(value).expanduser()
            if candidate.is_file():
                candidate = candidate.parent
            return candidate.resolve(strict=False)
    return None


def main() -> int:
    try:
        input_data = load_input()

        # Read available state files gracefully; these may not exist if
        # the individual tool-tracker or prompt-logger hooks are absent.
        with locked(TRACKER_STATS_FILE):
            tracker_stats = read_json(
                TRACKER_STATS_FILE,
                {"total_calls": 0, "file_mutations": 0, "cumulative_result_size_chars": 0},
            )
        prompt_stats = read_json(PROMPT_STATS_FILE, {"count": 0})
        error_state = read_json(ERROR_STATE_FILE, {"recent": [], "session_count": 0})
        changed_files = read_json(CHANGED_FILES_FILE, [])
        if not isinstance(changed_files, list):
            changed_files = []

        summary = {
            "session_end": to_iso(input_data.get("timestamp")),
            "reason": input_data.get("reason"),
            "stats": {
                "total_tool_calls": int(tracker_stats.get("total_calls", 0)),  # type: ignore[union-attr]
                "file_mutations": int(tracker_stats.get("file_mutations", 0)),  # type: ignore[union-attr]
                "prompts": int(prompt_stats.get("count", 0)),  # type: ignore[union-attr]
                "errors": int(error_state.get("session_count", 0)),  # type: ignore[union-attr]
            },
            "changed_files": changed_files,
        }

        with locked(SUMMARY_FILE):
            write_json(SUMMARY_FILE, summary)

        with locked(SESSIONS_LOG):
            append_jsonl(
                SESSIONS_LOG,
                {
                    "event": "end",
                    "ts": summary["session_end"],
                    "reason": input_data.get("reason"),
                    "stats": summary["stats"],
                },
            )

        # Runtime cleanup for stale backup and marker files.
        # write_state=False avoids writing cleanup results to UpgradeStateStore.
        workspace_root = _workspace_from_payload(input_data)
        if workspace_root is not None:
            cleanup_runtime_artifacts(
                workspace_root=workspace_root, dry_run=False, write_state=False
            )
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
