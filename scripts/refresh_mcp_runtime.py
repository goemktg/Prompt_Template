#!/usr/bin/env python3
"""Detect and refresh stale local MCP/runtime Python processes for this plugin copy."""

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, TypedDict


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from copilot.scripts.runtime_root import find_plugin_root
from copilot.scripts.upgrade_state import UpgradeStateStore


TARGET_SCRIPT_NAMES = (
    "runtime_launcher.py",
    "workspace_sync_server.py",
    "start-memory.py",
)
INTERPRETER_HINTS = (
    "python",
    "python3",
    "py.exe",
    "\\py ",
    "/py ",
    " uv ",
    "uv.exe",
)


class ProcessCandidate(TypedDict):
    pid: int
    name: str
    command_line: str


class RefreshResult(TypedDict):
    plugin_root: str
    dry_run: bool
    matched_count: int
    terminated_count: int
    matched: list[ProcessCandidate]
    terminated_pids: list[int]
    failed: list[dict[str, Any]]


def _normalize_text(value: str | Path) -> str:
    return os.path.normcase(str(value)).replace("\\", "/")


def _record_refresh_result(plugin_root: Path, result: RefreshResult) -> None:
    UpgradeStateStore(plugin_root).update_runtime_refresh(
        {
            "timestamp": time.time(),
            "plugin_root": result["plugin_root"],
            "dry_run": result["dry_run"],
            "matched_count": result["matched_count"],
            "terminated_count": result["terminated_count"],
            "terminated_pids": result["terminated_pids"],
            "failed": result["failed"],
            "target_scripts": list(TARGET_SCRIPT_NAMES),
        }
    )


def _looks_like_runtime_process(command_line: str, plugin_root: Path) -> bool:
    normalized = _normalize_text(command_line)
    if _normalize_text(plugin_root) not in normalized:
        return False
    if not any(script_name in normalized for script_name in TARGET_SCRIPT_NAMES):
        return False
    return any(hint in normalized for hint in INTERPRETER_HINTS)


def _list_processes_windows() -> list[ProcessCandidate]:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        "Get-CimInstance Win32_Process | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress -Depth 3",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "PowerShell process query failed")

    stdout = completed.stdout.strip()
    if not stdout:
        return []

    decoded = json.loads(stdout)
    rows = decoded if isinstance(decoded, list) else [decoded]
    candidates: list[ProcessCandidate] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        process_id = row.get("ProcessId")
        if not isinstance(process_id, int):
            continue
        command_line = row.get("CommandLine")
        if not isinstance(command_line, str) or not command_line.strip():
            continue
        name = row.get("Name")
        candidates.append(
            {
                "pid": process_id,
                "name": name if isinstance(name, str) else "",
                "command_line": command_line,
            }
        )
    return candidates


def _list_processes_posix() -> list[ProcessCandidate]:
    completed = subprocess.run(
        ["ps", "-ax", "-o", "pid=,command="],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "ps process query failed")

    candidates: list[ProcessCandidate] = []
    for raw_line in completed.stdout.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            continue
        try:
            pid = int(parts[0])
        except ValueError:
            continue
        command_line = parts[1]
        name = Path(command_line.split()[0]).name if command_line.split() else ""
        candidates.append({"pid": pid, "name": name, "command_line": command_line})
    return candidates


def _list_processes() -> list[ProcessCandidate]:
    if os.name == "nt":
        return _list_processes_windows()
    return _list_processes_posix()


def _terminate_process(pid: int) -> None:
    if os.name == "nt":
        completed = subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "taskkill failed")
        return
    os.kill(pid, signal.SIGTERM)


def refresh_runtime_processes(
    plugin_root: Path | None = None,
    dry_run: bool = False,
    write_state: bool = True,
) -> RefreshResult:
    resolved_root = Path(plugin_root or find_plugin_root(start_path=REPO_ROOT)).resolve()
    matched: list[ProcessCandidate] = []
    terminated_pids: list[int] = []
    failures: list[dict[str, Any]] = []

    for candidate in _list_processes():
        if candidate["pid"] == os.getpid():
            continue
        if not _looks_like_runtime_process(candidate["command_line"], resolved_root):
            continue
        matched.append(candidate)
        if dry_run:
            continue
        try:
            _terminate_process(candidate["pid"])
        except OSError as error:
            failures.append({"pid": candidate["pid"], "error": str(error)})
            continue
        except RuntimeError as error:
            failures.append({"pid": candidate["pid"], "error": str(error)})
            continue
        terminated_pids.append(candidate["pid"])

    result: RefreshResult = {
        "plugin_root": str(resolved_root),
        "dry_run": dry_run,
        "matched_count": len(matched),
        "terminated_count": len(terminated_pids),
        "matched": matched,
        "terminated_pids": terminated_pids,
        "failed": failures,
    }

    if write_state and not dry_run:
        _record_refresh_result(resolved_root, result)

    return result


def _print_result(result: RefreshResult) -> None:
    action = "would terminate" if result["dry_run"] else "terminated"
    if result["matched_count"] == 0:
        print(f"No stale runtime processes matched plugin root: {result['plugin_root']}")
    else:
        for candidate in result["matched"]:
            script_name = next(
                (name for name in TARGET_SCRIPT_NAMES if name in _normalize_text(candidate["command_line"])),
                "runtime",
            )
            print(f"{action}: pid={candidate['pid']} script={script_name}")
        print(
            f"refresh summary: matched={result['matched_count']} {action.replace(' ', '_')}={result['terminated_count']}"
        )

    for failure in result["failed"]:
        print(
            f"refresh warning: pid={failure['pid']} error={failure['error']}",
            file=sys.stderr,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refresh stale local MCP/runtime Python processes for this plugin copy.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report matching processes without terminating them.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = refresh_runtime_processes(dry_run=args.dry_run, write_state=not args.dry_run)
    except Exception as error:
        print(f"ERROR: runtime refresh failed: {error}", file=sys.stderr)
        return 1

    _print_result(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())