#!/usr/bin/env python3
"""MCP server for workspace sync operations."""

from __future__ import annotations

import io
import json
import os
import runpy
import subprocess
import sys
import time
from contextlib import redirect_stderr, redirect_stdout
from importlib import import_module
from pathlib import Path
from typing import Any, TypedDict

from runtime_root import find_plugin_root
from upgrade_state import UpgradeStateStore


class RuntimeInfo(TypedDict):
    cwd: str
    script_path: str
    argv: list[str]
    repo_root: str
    marker_source: str
    marker_files: list[str]
    upgrade_script: str
    python_executable: str
    pid: int


class SyncWorkspaceResult(TypedDict):
    success: bool
    exit_code: int
    target_workspace: str
    repo_root: str
    stdout: str
    stderr: str
    command: list[str]
    upgrade_script: str


SYNC_TIMEOUT_SECONDS = 120


MARKER_FILES = (
    "plugin.json",
    os.path.join("copilot", "mcp.json"),
    os.path.join("scripts", "upgrade_ai.py"),
)


MCP_BOOTSTRAP_ENV_VAR = "WORKSPACE_SYNC_MCP_BOOTSTRAPPED"


def _collect_runtime_info() -> RuntimeInfo:
    cwd = Path.cwd()
    script_path = Path(__file__).resolve()
    marker_source = str(script_path.parent)
    repo_root = Path(
        find_plugin_root(start_path=script_path.parent, required_markers=MARKER_FILES)
    )
    marker_files = [str(marker) for marker in MARKER_FILES]
    upgrade_script = repo_root / "scripts" / "upgrade_ai.py"

    return {
        "cwd": str(cwd),
        "script_path": str(script_path),
        "argv": sys.argv[:],
        "repo_root": str(repo_root),
        "marker_source": marker_source,
        "marker_files": marker_files,
        "upgrade_script": str(upgrade_script),
        "python_executable": sys.executable,
        "pid": os.getpid(),
    }


def _resolve_target_workspace(target_path: str | None) -> Path:
    if target_path:
        return Path(target_path).expanduser().resolve()
    return Path.cwd().resolve()


def _ensure_text(value: str | bytes | bytearray | memoryview | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, bytearray):
        return bytes(value).decode("utf-8", errors="replace")
    if isinstance(value, memoryview):
        return value.tobytes().decode("utf-8", errors="replace")
    return value


def _record_sync_result(
    target_workspace: Path,
    runtime_info: RuntimeInfo,
    exit_code: int,
    success: bool,
    timed_out: bool,
) -> None:
    try:
        UpgradeStateStore(target_workspace).update_sync_result(
            {
                "timestamp": time.time(),
                "target_workspace": str(target_workspace),
                "exit_code": exit_code,
                "success": success,
                "timeout": timed_out,
                "repo_root": runtime_info["repo_root"],
                "upgrade_script": runtime_info["upgrade_script"],
                "wrapper": "workspace_sync_server",
            }
        )
    except OSError as error:
        sys.stderr.write(
            f"[workspace-sync] state write warning target={target_workspace} error={error}\n"
        )
        sys.stderr.flush()


def _run_upgrade_in_process(upgrade_script: Path, target_workspace: Path) -> tuple[int, str, str]:
    command = [str(upgrade_script), str(target_workspace)]
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    previous_argv = sys.argv[:]
    previous_cwd = Path.cwd()

    try:
        sys.argv = command
        os.chdir(target_workspace)
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            try:
                runpy.run_path(str(upgrade_script), run_name="__main__")
                exit_code = 0
            except SystemExit as error:
                if error.code is None:
                    exit_code = 0
                elif isinstance(error.code, int):
                    exit_code = error.code
                else:
                    exit_code = 1
                    print(error.code, file=sys.stderr)
    finally:
        os.chdir(previous_cwd)
        sys.argv = previous_argv

    return exit_code, stdout_buffer.getvalue(), stderr_buffer.getvalue()


def _run_sync(target_path: str | None) -> SyncWorkspaceResult:
    runtime_info = _collect_runtime_info()
    target_workspace = _resolve_target_workspace(target_path)
    upgrade_script = Path(runtime_info["upgrade_script"])
    command = [sys.executable, str(upgrade_script), str(target_workspace)]
    sys.stderr.write(
        f"[workspace-sync] sync start target={target_workspace} timeout={SYNC_TIMEOUT_SECONDS}s\n"
    )
    sys.stderr.flush()

    completed_exit_code, completed_stdout, completed_stderr = _run_upgrade_in_process(
        upgrade_script,
        target_workspace,
    )

    sys.stderr.write(
        f"[workspace-sync] sync end target={target_workspace} exit_code={completed_exit_code}\n"
    )
    sys.stderr.flush()
    _record_sync_result(
        target_workspace,
        runtime_info,
        completed_exit_code,
        completed_exit_code == 0,
        False,
    )

    return {
        "success": completed_exit_code == 0,
        "exit_code": completed_exit_code,
        "target_workspace": str(target_workspace),
        "repo_root": runtime_info["repo_root"],
        "stdout": completed_stdout,
        "stderr": completed_stderr,
        "command": command,
        "upgrade_script": str(upgrade_script),
    }


def _log_runtime_info(runtime_info: RuntimeInfo) -> None:
    prefix = "[workspace-sync]"
    sys.stderr.write(f"{prefix} cwd={runtime_info['cwd']}\n")
    sys.stderr.write(f"{prefix} __file__={runtime_info['script_path']}\n")
    sys.stderr.write(f"{prefix} argv={json.dumps(runtime_info['argv'])}\n")
    sys.stderr.write(
        f"{prefix} repo_root={runtime_info['repo_root']} "
        f"source={runtime_info['marker_source']} markers={json.dumps(runtime_info['marker_files'])}\n"
    )
    sys.stderr.write(f"{prefix} upgrade_script={runtime_info['upgrade_script']}\n")
    sys.stderr.flush()


def get_runtime_info() -> RuntimeInfo:
    """Return runtime information for the workspace sync MCP server."""
    return _collect_runtime_info()


def sync_workspace(target_path: str | None = None) -> SyncWorkspaceResult:
    """Run the workspace sync script for the current or specified target workspace."""
    return _run_sync(target_path)


def _bootstrap_with_uv() -> None:
    if os.environ.get(MCP_BOOTSTRAP_ENV_VAR) == "1":
        raise RuntimeError(
            "workspace-sync requires the 'mcp' package, but automatic uv bootstrap did not make it available."
        )

    command = ["uv", "run", "--with", "mcp", "python", str(Path(__file__).resolve()), *sys.argv[1:]]
    env = os.environ.copy()
    env[MCP_BOOTSTRAP_ENV_VAR] = "1"

    sys.stderr.write("[workspace-sync] missing 'mcp'; re-launching with uv --with mcp\n")
    sys.stderr.flush()

    completed = subprocess.run(command, check=False, env=env)
    raise SystemExit(completed.returncode)


def _load_fastmcp() -> Any:
    try:
        return import_module("mcp.server.fastmcp")
    except ModuleNotFoundError as error:
        if error.name != "mcp":
            raise
        _bootstrap_with_uv()
        raise AssertionError("unreachable")


def _build_mcp_server() -> Any:
    server = _load_fastmcp().FastMCP("workspace-sync")
    server.tool()(get_runtime_info)
    server.tool()(sync_workspace)
    return server


def main() -> None:
    runtime_info = _collect_runtime_info()
    _log_runtime_info(runtime_info)

    if "--self-check" in sys.argv:
        sys.stdout.write(json.dumps(runtime_info, indent=2, sort_keys=True) + "\n")
        sys.stdout.flush()
        return

    _build_mcp_server().run()


if __name__ == "__main__":
    main()