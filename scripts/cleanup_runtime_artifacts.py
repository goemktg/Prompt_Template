#!/usr/bin/env python3
"""Clean bounded stale runtime artifacts for a target workspace.

Managed cleanup scope is intentionally narrow:
- backup files ending in .bak for deploy-manifest managed targets
- marker JSON files under .copilot-memory/ or .copilot-memory/runtime/
  with names starting with session-, compact-, or lifecycle-
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from copilot.scripts.upgrade_state import UpgradeStateStore


BACKUP_EXTENSION = ".bak"
DEFAULT_BACKUP_MAX_AGE_HOURS = 24.0 * 7.0
DEFAULT_MARKER_MAX_AGE_HOURS = 24.0
DEFAULT_KEEP_NEWEST_BACKUPS = 0
MARKER_PREFIXES = (
    "session-",
    "compact-",
    "lifecycle-",
)
MARKER_DIRECTORIES = (
    ".copilot-memory",
    ".copilot-memory/runtime",
)


def _resolve_workspace_root(raw_path: str) -> Path:
    return Path(raw_path).expanduser().resolve(strict=False)


def _load_deploy_manifest() -> dict[str, Any]:
    manifest_path = REPO_ROOT / "copilot" / "deploy-manifest.json"
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def _iter_managed_backup_paths(workspace_root: Path) -> Iterable[Path]:
    manifest = _load_deploy_manifest()
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        return

    seen: set[Path] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        raw_target = entry.get("target")
        kind = entry.get("kind")
        if not isinstance(raw_target, str) or not raw_target:
            continue
        target_path = workspace_root / raw_target
        if kind == "file":
            backup_path = target_path.with_name(target_path.name + BACKUP_EXTENSION)
            if backup_path.is_file() and backup_path not in seen:
                seen.add(backup_path)
                yield backup_path
            continue
        if kind != "directory" or not target_path.is_dir():
            continue
        for backup_path in target_path.rglob(f"*{BACKUP_EXTENSION}"):
            if not backup_path.is_file() or backup_path in seen:
                continue
            seen.add(backup_path)
            yield backup_path


def _iter_managed_marker_paths(workspace_root: Path) -> Iterable[Path]:
    for relative_dir in MARKER_DIRECTORIES:
        marker_dir = workspace_root / relative_dir
        if not marker_dir.is_dir():
            continue
        for candidate in marker_dir.glob("*.json"):
            if candidate.name.startswith(MARKER_PREFIXES):
                yield candidate


def _is_stale(path: Path, now: float, max_age_hours: float) -> bool:
    try:
        modified_at = path.stat().st_mtime
    except OSError:
        return False
    return modified_at <= now - (max_age_hours * 3600.0)


def _relative_path(path: Path, workspace_root: Path) -> str:
    return path.relative_to(workspace_root).as_posix()


def cleanup_runtime_artifacts(
    *,
    workspace_root: Path,
    dry_run: bool = False,
    backup_max_age_hours: float = DEFAULT_BACKUP_MAX_AGE_HOURS,
    marker_max_age_hours: float = DEFAULT_MARKER_MAX_AGE_HOURS,
    keep_newest_backups: int = DEFAULT_KEEP_NEWEST_BACKUPS,
    write_state: bool = True,
) -> dict[str, Any]:
    resolved_workspace = workspace_root.resolve(strict=False)
    now = time.time()

    backup_paths = sorted(
        _iter_managed_backup_paths(resolved_workspace),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    marker_paths = sorted(_iter_managed_marker_paths(resolved_workspace))
    kept_backups = {path for path in backup_paths[: max(keep_newest_backups, 0)]}

    stale_backups = [
        path
        for path in backup_paths
        if path not in kept_backups and _is_stale(path, now, backup_max_age_hours)
    ]
    stale_markers = [path for path in marker_paths if _is_stale(path, now, marker_max_age_hours)]

    deleted: list[str] = []
    failed: list[dict[str, str]] = []
    for candidate in [*stale_backups, *stale_markers]:
        relative_path = _relative_path(candidate, resolved_workspace)
        if dry_run:
            continue
        try:
            candidate.unlink()
        except OSError as error:
            failed.append({"path": relative_path, "error": str(error)})
            continue
        deleted.append(relative_path)

    result = {
        "timestamp": now,
        "workspace_root": str(resolved_workspace),
        "dry_run": dry_run,
        "backup_max_age_hours": float(backup_max_age_hours),
        "marker_max_age_hours": float(marker_max_age_hours),
        "keep_newest_backups": max(int(keep_newest_backups), 0),
        "scanned_counts": {
            "backup_files": len(backup_paths),
            "marker_files": len(marker_paths),
        },
        "candidate_counts": {
            "backup_files": len(stale_backups),
            "marker_files": len(stale_markers),
            "total": len(stale_backups) + len(stale_markers),
        },
        "candidates": [
            _relative_path(path, resolved_workspace) for path in [*stale_backups, *stale_markers]
        ],
        "deleted": deleted,
        "deleted_count": len(deleted),
        "failed": failed,
    }

    if write_state:
        UpgradeStateStore(resolved_workspace).update_runtime_cleanup(result)

    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Remove bounded stale runtime artifacts from a target workspace.",
    )
    parser.add_argument("--workspace", required=True, help="Target workspace root path.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report stale candidates without deleting them.",
    )
    parser.add_argument(
        "--backup-max-age-hours",
        type=float,
        default=DEFAULT_BACKUP_MAX_AGE_HOURS,
        help="Delete managed .bak files older than this many hours.",
    )
    parser.add_argument(
        "--marker-max-age-hours",
        type=float,
        default=DEFAULT_MARKER_MAX_AGE_HOURS,
        help="Delete managed marker JSON files older than this many hours.",
    )
    parser.add_argument(
        "--keep-newest-backups",
        type=int,
        default=DEFAULT_KEEP_NEWEST_BACKUPS,
        help="Always preserve this many newest managed backups.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    result = cleanup_runtime_artifacts(
        workspace_root=_resolve_workspace_root(args.workspace),
        dry_run=args.dry_run,
        backup_max_age_hours=args.backup_max_age_hours,
        marker_max_age_hours=args.marker_max_age_hours,
        keep_newest_backups=args.keep_newest_backups,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())