#!/usr/bin/env python3
"""Verify that this plugin copy is activated in VS Code settings."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.install_vscode_plugin import (  # noqa: E402
    _iter_default_settings_paths,
    _load_settings,
    _normalize_location_map,
    _normalize_plugin_locations,
)


def _resolve_settings_targets(settings_files: list[str]) -> list[Path]:
    if settings_files:
        return [Path(path).expanduser() for path in settings_files]
    return _iter_default_settings_paths()


def _collect_target_issues(settings: dict[str, Any], plugin_root: Path) -> list[str]:
    issues: list[str] = []
    plugin_root_str = str(plugin_root.resolve())
    hook_manifest_path = str((plugin_root / "copilot" / "hooks.json").resolve())

    plugin_locations = _normalize_plugin_locations(settings.get("chat.pluginLocations"))
    if plugin_locations.get(plugin_root_str) is not True:
        issues.append("chat.pluginLocations missing plugin root")

    hook_locations = _normalize_location_map(settings.get("chat.hookFilesLocations"))
    if hook_locations.get(hook_manifest_path) is not True:
        issues.append("chat.hookFilesLocations missing hook manifest")

    if settings.get("chat.useCustomAgentHooks") is not True:
        issues.append("chat.useCustomAgentHooks is not true")

    if settings.get("chat.plugins.enabled") is not True:
        issues.append("chat.plugins.enabled is not true")

    return issues


def verify_runtime_activation(
    settings_files: list[str] | None = None,
    plugin_root: Path | None = None,
) -> dict[str, Any]:
    resolved_plugin_root = (plugin_root or REPO_ROOT).resolve()
    plugin_manifest = resolved_plugin_root / "plugin.json"
    hook_manifest = resolved_plugin_root / "copilot" / "hooks.json"
    targets = _resolve_settings_targets(settings_files or [])

    target_results: list[dict[str, Any]] = []
    for target in targets:
        settings = _load_settings(target)
        issues = _collect_target_issues(settings, resolved_plugin_root)
        target_results.append(
            {
                "settings_file": str(target),
                "ok": not issues,
                "issues": issues,
            }
        )

    manifest_issues: list[str] = []
    if not plugin_manifest.is_file():
        manifest_issues.append("plugin.json is missing")
    if not hook_manifest.is_file():
        manifest_issues.append("copilot/hooks.json is missing")
    if not targets:
        manifest_issues.append("no VS Code settings targets were resolved")

    activation_ok = any(result["ok"] for result in target_results)
    overall_ok = not manifest_issues and activation_ok

    return {
        "ok": overall_ok,
        "plugin_root": str(resolved_plugin_root),
        "manifest_issues": manifest_issues,
        "target_results": target_results,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify that this repository is activated as a VS Code Copilot plugin.",
    )
    parser.add_argument(
        "--settings-file",
        action="append",
        dest="settings_files",
        default=[],
        help="Explicit VS Code settings.json target. Can be provided multiple times.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = verify_runtime_activation(settings_files=args.settings_files)

    for issue in result["manifest_issues"]:
        print(f"missing: {issue}", file=sys.stderr)

    for target_result in result["target_results"]:
        target_path = target_result["settings_file"]
        if target_result["ok"]:
            print(f"ok: {target_path}")
            continue

        print(f"missing activation state: {target_path}", file=sys.stderr)
        for issue in target_result["issues"]:
            print(f"  - {issue}", file=sys.stderr)

    if result["ok"]:
        print("runtime activation verification passed")
        return 0

    print("runtime activation verification failed", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())