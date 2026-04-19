#!/usr/bin/env python3
"""Shared runtime entrypoint for MCP server launchers."""

from __future__ import annotations

import argparse
import os
import runpy
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from runtime_root import find_plugin_root


PLUGIN_MARKERS = (
    "plugin.json",
    os.path.join("copilot", "mcp.json"),
)


def _resolve_plugin_root() -> Path:
    return Path(
        find_plugin_root(
            start_path=Path(__file__).resolve().parent,
            required_markers=PLUGIN_MARKERS,
        )
    ).resolve()


def _run_memory() -> int:
    plugin_root = _resolve_plugin_root()
    memory_dir = plugin_root / ".copilot-memory"
    memory_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env.update(
        {
            "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec",
            "MCP_MEMORY_SQLITE_PATH": str(memory_dir / "memory.db"),
            "CUDA_VISIBLE_DEVICES": "",
            "MCP_MEMORY_USE_ONNX": "1",
        }
    )

    completed = subprocess.run(
        ["uv", "tool", "run", "--from", "mcp-memory-service", "memory", "server"],
        env=env,
        check=False,
    )
    return completed.returncode


def _run_workspace_sync(forwarded_args: list[str]) -> int:
    plugin_root = _resolve_plugin_root()
    script_path = plugin_root / "copilot" / "scripts" / "workspace_sync_server.py"
    sys.argv = [str(script_path), *forwarded_args]
    runpy.run_path(str(script_path), run_name="__main__")
    return 0


def _run_session_gate(forwarded_args: list[str]) -> int:
    plugin_root = _resolve_plugin_root()
    script_path = plugin_root / "copilot" / "mcp-servers" / "session-gate" / "server.py"
    sys.argv = [str(script_path), *forwarded_args]
    runpy.run_path(str(script_path), run_name="__main__")
    return 0


def _run_context_manager(forwarded_args: list[str]) -> int:
    plugin_root = _resolve_plugin_root()
    script_path = plugin_root / "copilot" / "mcp-servers" / "context-manager" / "server.py"
    sys.argv = [str(script_path), *forwarded_args]
    runpy.run_path(str(script_path), run_name="__main__")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Launch MCP runtime services.")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    subparsers.add_parser("memory", help="Start the memory MCP server.")

    subparsers.add_parser(
        "workspace-sync",
        help="Start the workspace-sync MCP server.",
    )

    subparsers.add_parser(
        "session-gate",
        help="Start the session-gate MCP server.",
    )

    subparsers.add_parser(
        "context-manager",
        help="Start the context-manager MCP server.",
    )

    parsed, extras = parser.parse_known_args(argv)

    if parsed.mode == "memory":
        if extras:
            parser.error(f"unrecognized arguments: {' '.join(extras)}")
        return _run_memory()
    if parsed.mode == "workspace-sync":
        return _run_workspace_sync(extras)
    if parsed.mode == "session-gate":
        return _run_session_gate(extras)
    if parsed.mode == "context-manager":
        return _run_context_manager(extras)
    raise RuntimeError(f"Unsupported runtime mode: {parsed.mode}")


if __name__ == "__main__":
    sys.exit(main())