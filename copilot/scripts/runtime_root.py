#!/usr/bin/env python3
"""Shared plugin root discovery helpers for MCP runtime launchers."""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Any, Iterable

DEFAULT_SKIP_DIRS = {"AppData", ".git", "node_modules", ".venv", "__pycache__"}
WINDOWS_VSCODE_PRODUCTS = ("Code", "Code - Insiders")
MACOS_VSCODE_PRODUCTS = ("Code", "Code - Insiders")
LINUX_VSCODE_PRODUCTS = ("Code", "Code - Insiders")
VSCODE_HOME_PLUGIN_DIRS = (".vscode/agent-plugins", ".vscode-insiders/agent-plugins")


def _has_markers(path: str, required_markers: tuple[str, ...]) -> bool:
    return all(os.path.isfile(os.path.join(path, marker)) for marker in required_markers)


def _ascend_find(start_path: str, required_markers: tuple[str, ...], max_levels: int = 20) -> str | None:
    current = os.path.abspath(start_path)
    for _ in range(max_levels):
        if _has_markers(current, required_markers):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return None


def _walk_find(
    base_path: str,
    required_markers: tuple[str, ...],
    deadline: float,
    skip_dirs: set[str],
    max_descent: int,
    max_dirs: int,
) -> str | None:
    if not base_path or not os.path.isdir(base_path):
        return None

    base = os.path.abspath(base_path)
    base_depth = base.rstrip(os.sep).count(os.sep)
    seen = 0

    for current, dirs, _files in os.walk(base):
        seen += 1
        if seen > max_dirs or time.monotonic() > deadline:
            return None

        depth = current.rstrip(os.sep).count(os.sep) - base_depth
        dirs[:] = [name for name in dirs if name not in skip_dirs]
        if depth >= max_descent:
            dirs[:] = []

        if _has_markers(current, required_markers):
            return current
    return None


def _strip_jsonc_comments(text: str) -> str:
    result: list[str] = []
    index = 0
    in_string = False
    escaping = False
    length = len(text)

    while index < length:
        char = text[index]
        next_char = text[index + 1] if index + 1 < length else ""

        if in_string:
            result.append(char)
            if escaping:
                escaping = False
            elif char == "\\":
                escaping = True
            elif char == '"':
                in_string = False
            index += 1
            continue

        if char == '"':
            in_string = True
            result.append(char)
            index += 1
            continue

        if char == "/" and next_char == "/":
            index += 2
            while index < length and text[index] not in "\r\n":
                index += 1
            continue

        if char == "/" and next_char == "*":
            index += 2
            while index + 1 < length and not (text[index] == "*" and text[index + 1] == "/"):
                index += 1
            index += 2
            continue

        result.append(char)
        index += 1

    return "".join(result)


def _load_jsonc_file(path: str | Path) -> Any | None:
    try:
        raw_text = Path(path).read_text(encoding="utf-8")
    except OSError:
        return None

    cleaned = _strip_jsonc_comments(raw_text)
    cleaned = re.sub(r",(\s*[}\]])", r"\1", cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return None


def _iter_settings_paths() -> tuple[str, ...]:
    candidates: list[str] = []
    appdata = os.environ.get("APPDATA")
    home = os.path.expanduser("~")

    if appdata:
        for product in WINDOWS_VSCODE_PRODUCTS:
            candidates.append(os.path.join(appdata, product, "User", "settings.json"))

    macos_base = os.path.join(home, "Library", "Application Support")
    for product in MACOS_VSCODE_PRODUCTS:
        candidates.append(os.path.join(macos_base, product, "User", "settings.json"))

    linux_base = os.path.join(home, ".config")
    for product in LINUX_VSCODE_PRODUCTS:
        candidates.append(os.path.join(linux_base, product, "User", "settings.json"))

    return tuple(dict.fromkeys(os.path.abspath(path) for path in candidates))


def _iter_plugin_location_bases() -> tuple[str, ...]:
    bases: list[str] = []

    for settings_path in _iter_settings_paths():
        settings = _load_jsonc_file(settings_path)
        if not isinstance(settings, dict):
            continue

        locations = settings.get("chat.pluginLocations")
        if isinstance(locations, dict):
            for path, enabled in locations.items():
                if enabled is not False and isinstance(path, str) and path.strip():
                    bases.append(path)
        elif isinstance(locations, list):
            for entry in locations:
                if isinstance(entry, str) and entry.strip():
                    bases.append(entry)
        elif isinstance(locations, str) and locations.strip():
            bases.append(locations)

    return tuple(dict.fromkeys(os.path.abspath(os.path.expanduser(path)) for path in bases))


def _iter_agent_plugin_bases() -> tuple[str, ...]:
    candidates: list[str] = []
    appdata = os.environ.get("APPDATA")
    home = os.path.expanduser("~")

    if appdata:
        for product in WINDOWS_VSCODE_PRODUCTS:
            candidates.append(
                os.path.join(
                    appdata,
                    product,
                    "User",
                    "globalStorage",
                    "github.copilot-chat",
                    "agentPlugins",
                )
            )

    macos_base = os.path.join(home, "Library", "Application Support")
    for product in MACOS_VSCODE_PRODUCTS:
        candidates.append(
            os.path.join(
                macos_base,
                product,
                "User",
                "globalStorage",
                "github.copilot-chat",
                "agentPlugins",
            )
        )

    linux_base = os.path.join(home, ".config")
    for product in LINUX_VSCODE_PRODUCTS:
        candidates.append(
            os.path.join(
                linux_base,
                product,
                "User",
                "globalStorage",
                "github.copilot-chat",
                "agentPlugins",
            )
        )

    # Home-based agent-plugins directories (Windows, macOS, Linux)
    for rel in VSCODE_HOME_PLUGIN_DIRS:
        candidates.append(os.path.join(home, rel))

    return tuple(dict.fromkeys(os.path.abspath(path) for path in candidates))


def find_plugin_root(
    start_path: str | Path | None = None,
    required_markers: Iterable[str] = (
        "plugin.json",
        os.path.join("copilot", "mcp.json"),
    ),
    search_timeout_seconds: float = 12.0,
    max_descent: int = 6,
    max_dirs: int = 12000,
    skip_dirs: set[str] | None = None,
) -> str:
    """Find the plugin root from a start path using bounded search.

    Search order:
    1) Ascend parents from start_path
    2) Inspect chat.pluginLocations from VS Code user settings
    3) Inspect standard VS Code agentPlugins bases with bounded walk
    """

    markers = tuple(required_markers)
    if not markers:
        raise RuntimeError("required_markers must not be empty")

    start = os.path.abspath(str(start_path or os.getcwd()))
    root = _ascend_find(start, markers)
    if root is not None:
        return root

    deadline = time.monotonic() + search_timeout_seconds
    seen_bases: set[str] = set()
    skip = set(skip_dirs or DEFAULT_SKIP_DIRS)

    for base_group in (_iter_plugin_location_bases(), _iter_agent_plugin_bases()):
        for base in base_group:
            base = os.path.abspath(base)
            if base in seen_bases:
                continue
            seen_bases.add(base)
            root = _walk_find(base, markers, deadline, skip, max_descent, max_dirs)
            if root is not None:
                return root

    raise RuntimeError(f"Unable to resolve plugin root from start path: {start}")
