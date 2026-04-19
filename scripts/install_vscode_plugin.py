#!/usr/bin/env python3
"""Register this repository as a VS Code Copilot chat plugin location."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from copilot.scripts.runtime_root import find_plugin_root
from scripts.refresh_mcp_runtime import refresh_runtime_processes


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


def _load_settings(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}

    raw_text = path.read_text(encoding="utf-8")
    cleaned = _strip_jsonc_comments(raw_text)
    cleaned = re.sub(r",(\s*[}\]])", r"\1", cleaned)
    data = json.loads(cleaned)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return data


def _iter_default_settings_paths() -> list[Path]:
    paths: list[Path] = []
    home = Path.home()
    appdata = os.environ.get("APPDATA")

    if appdata:
        paths.append(Path(appdata) / "Code" / "User" / "settings.json")
        insiders_path = Path(appdata) / "Code - Insiders" / "User" / "settings.json"
        if insiders_path.exists():
            paths.append(insiders_path)
        return paths

    if sys.platform == "darwin":
        paths.append(home / "Library" / "Application Support" / "Code" / "User" / "settings.json")
        insiders_path = home / "Library" / "Application Support" / "Code - Insiders" / "User" / "settings.json"
        if insiders_path.exists():
            paths.append(insiders_path)
        return paths

    paths.append(home / ".config" / "Code" / "User" / "settings.json")
    insiders_path = home / ".config" / "Code - Insiders" / "User" / "settings.json"
    if insiders_path.exists():
        paths.append(insiders_path)
    return paths


def _normalize_plugin_locations(value: Any) -> dict[str, bool]:
    if isinstance(value, dict):
        return {
            str(path): enabled is not False
            for path, enabled in value.items()
            if isinstance(path, str) and path.strip()
        }
    if isinstance(value, list):
        return {str(path): True for path in value if isinstance(path, str) and path.strip()}
    if isinstance(value, str) and value.strip():
        return {value: True}
    return {}


def _normalize_location_map(value: Any) -> dict[str, bool]:
    if isinstance(value, dict):
        return {
            str(path): enabled is not False
            for path, enabled in value.items()
            if isinstance(path, str) and path.strip()
        }
    if isinstance(value, list):
        return {str(path): True for path in value if isinstance(path, str) and path.strip()}
    if isinstance(value, str) and value.strip():
        return {value: True}
    return {}


def _update_settings(settings: dict[str, Any], plugin_root: str) -> bool:
    changed = False
    plugin_locations = _normalize_plugin_locations(settings.get("chat.pluginLocations"))
    hook_manifest_path = str((Path(plugin_root) / "copilot" / "hooks.json").resolve())
    hook_locations = _normalize_location_map(settings.get("chat.hookFilesLocations"))

    if plugin_locations.get(plugin_root) is not True:
        plugin_locations[plugin_root] = True
        changed = True

    normalized_locations = dict(sorted(plugin_locations.items()))
    if settings.get("chat.pluginLocations") != normalized_locations:
        settings["chat.pluginLocations"] = normalized_locations
        changed = True

    if settings.get("chat.plugins.enabled") is not True:
        settings["chat.plugins.enabled"] = True
        changed = True

    if hook_locations.get(hook_manifest_path) is not True:
        hook_locations[hook_manifest_path] = True
        changed = True

    normalized_hook_locations = dict(sorted(hook_locations.items()))
    if settings.get("chat.hookFilesLocations") != normalized_hook_locations:
        settings["chat.hookFilesLocations"] = normalized_hook_locations
        changed = True

    if settings.get("chat.useCustomAgentHooks") is not True:
        settings["chat.useCustomAgentHooks"] = True
        changed = True

    return changed


def _write_settings(path: Path, settings: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(settings, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _report_verification_result(result: dict[str, Any]) -> bool:
    if result["ok"]:
        print("post-install verification passed")
        return True

    for issue in result["manifest_issues"]:
        print(f"post-install verification missing: {issue}", file=sys.stderr)

    for target_result in result["target_results"]:
        target_path = target_result["settings_file"]
        if target_result["ok"]:
            continue

        print(f"post-install verification missing activation state: {target_path}", file=sys.stderr)
        for issue in target_result["issues"]:
            print(f"  - {issue}", file=sys.stderr)

    print("post-install verification failed", file=sys.stderr)
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Register this repository root in VS Code user settings chat.pluginLocations.",
    )
    parser.add_argument(
        "--settings-file",
        action="append",
        dest="settings_files",
        default=[],
        help="Explicit VS Code settings.json target. Can be provided multiple times.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the settings files that would be updated without writing them.",
    )
    parser.add_argument(
        "--no-refresh-runtime",
        action="store_true",
        help="Skip the best-effort stale runtime process refresh after registration.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plugin_root = Path(find_plugin_root(start_path=REPO_ROOT)).resolve()
    targets = [Path(path).expanduser() for path in args.settings_files] or _iter_default_settings_paths()

    if not targets:
        print("No VS Code settings targets were resolved.", file=sys.stderr)
        return 1

    wrote_any = False
    for target in targets:
        settings = _load_settings(target)
        changed = _update_settings(settings, str(plugin_root))

        if args.dry_run:
            action = "would update" if changed else "already current"
            print(f"{action}: {target}")
            continue

        if changed:
            _write_settings(target, settings)
            wrote_any = True
            print(f"updated: {target}")
        else:
            print(f"unchanged: {target}")

    if not args.dry_run and not wrote_any:
        print("VS Code plugin registration was already current.")

    if not args.dry_run and not args.no_refresh_runtime:
        try:
            refresh_result = refresh_runtime_processes(plugin_root=plugin_root, dry_run=False, write_state=True)
        except Exception as error:
            print(f"WARNING: runtime refresh failed: {error}", file=sys.stderr)
        else:
            if refresh_result["matched_count"] == 0:
                print("runtime refresh: no stale processes matched this plugin copy")
            else:
                print(
                    "runtime refresh: "
                    f"matched={refresh_result['matched_count']} "
                    f"terminated={refresh_result['terminated_count']}"
                )
                for failure in refresh_result["failed"]:
                    print(
                        f"runtime refresh warning: pid={failure['pid']} error={failure['error']}",
                        file=sys.stderr,
                    )

    if not args.dry_run:
        from scripts.verify_runtime_activation import verify_runtime_activation

        verification_result = verify_runtime_activation(
            settings_files=[str(target) for target in targets],
            plugin_root=plugin_root,
        )
        if not _report_verification_result(verification_result):
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())