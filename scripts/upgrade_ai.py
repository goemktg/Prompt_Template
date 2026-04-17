#!/usr/bin/env python3
"""
AI Template Workspace Sync Tool

Syncs updater-managed supplementary files from this plugin repository into a
target workspace.
- Uses this repository as the source plugin folder
- Uses copilot/deploy-manifest.json as the authoritative source manifest
- Syncs only supplementary deploy entries into the target workspace
"""

import argparse
import filecmp
import json
import shutil
import sys
from datetime import datetime
from fnmatch import fnmatch
from pathlib import Path
from pathlib import PurePosixPath
from typing import cast
from typing import Any, Dict, List, Optional, Set, Tuple


_SUPPLEMENTARY_MANIFEST_REL = Path("copilot") / "deploy-manifest.json"
_FORBIDDEN_SUPPLEMENTARY_TARGETS = (
    Path("README.md"),
    Path("plugin.json"),
    Path("copilot") / "mcp.json",
    Path("copilot") / "hooks.json",
)
_FORBIDDEN_SUPPLEMENTARY_PREFIXES = (
    Path("copilot") / "agents",
    Path("copilot") / "hooks",
    Path("shared") / "skills",
)


class TemplateUpgrader:
    """Manages local supplementary file sync into a target workspace."""

    def __init__(
        self,
        repo_root: Path,
        target_root: Optional[Path] = None,
        ignore_delay: bool = False,
    ):
        self.repo_root = repo_root.resolve()
        self.source_root = self.repo_root
        self.target_root = (target_root or Path.cwd()).resolve()
        self.supplementary_manifest = self.source_root / _SUPPLEMENTARY_MANIFEST_REL
        self.state_file = self.target_root / ".copilot-memory" / "upgrade_state.json"
        self.ignore_delay = ignore_delay

    def _ensure_state_dir(self) -> None:
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

    def _load_state(self) -> Dict[str, Any]:
        self._ensure_state_dir()
        if not self.state_file.exists():
            return {"schema_version": 1}
        try:
            with open(self.state_file, encoding="utf-8") as file_handle:
                data = cast(object, json.load(file_handle))
            if isinstance(data, dict):
                state = cast(Dict[str, Any], data)
                if "schema_version" not in state:
                    state["schema_version"] = 1
                return state
        except (OSError, json.JSONDecodeError):
            pass
        return {"schema_version": 1}

    def _save_state(self, state: Dict[str, Any]) -> None:
        self._ensure_state_dir()
        temp_file = self.state_file.with_suffix(".json.tmp")
        with open(temp_file, "w", encoding="utf-8") as file_handle:
            json.dump(state, file_handle, indent=2, sort_keys=True)
        temp_file.replace(self.state_file)

    def save_last_exit_code(self, code: int) -> None:
        state = self._load_state()
        state["last_exit_code"] = code
        if code == 0:
            state["last_success_ts"] = datetime.now().timestamp()
        self._save_state(state)

    def _resolve_target_relative_path(self, rel_path: str) -> Path:
        return self._resolve_relative_path(self.target_root, rel_path)

    def _resolve_relative_path(self, root: Path, rel_path: str) -> Path:
        candidate = (root / rel_path).resolve()
        candidate.relative_to(root.resolve())
        return candidate

    def _is_forbidden_supplementary_target(self, rel_path: Path) -> Optional[str]:
        normalized = Path(rel_path.as_posix())
        if normalized in _FORBIDDEN_SUPPLEMENTARY_TARGETS:
            return f"{normalized.as_posix()} is runtime-owned or explicitly excluded"
        for prefix in _FORBIDDEN_SUPPLEMENTARY_PREFIXES:
            if normalized == prefix or prefix in normalized.parents:
                return f"{normalized.as_posix()} is outside the supplementary deploy boundary"
        return None

    def _load_supplementary_manifest(self, manifest_path: Path) -> Optional[Dict[str, Any]]:
        try:
            with open(manifest_path, encoding="utf-8") as file_handle:
                manifest = cast(object, json.load(file_handle))
        except FileNotFoundError:
            print(f"ERROR: Supplementary deploy manifest not found: {manifest_path}")
            return None
        except (OSError, json.JSONDecodeError) as error:
            print(f"ERROR: Failed to load supplementary deploy manifest: {error}")
            return None

        if not isinstance(manifest, dict):
            print("ERROR: Supplementary deploy manifest must be a JSON object")
            return None
        manifest = cast(Dict[str, Any], manifest)
        if manifest.get("schemaVersion") != 1:
            print("ERROR: Supplementary deploy manifest schemaVersion must be 1")
            return None

        policy_obj = manifest.get("syncPolicy")
        if not isinstance(policy_obj, dict):
            print("ERROR: Supplementary deploy manifest must declare syncPolicy.overwrite = 'force'")
            return None
        policy = cast(Dict[str, Any], policy_obj)
        if policy.get("overwrite") != "force":
            print("ERROR: Supplementary deploy manifest must declare syncPolicy.overwrite = 'force'")
            return None

        entries_obj = manifest.get("entries")
        if not isinstance(entries_obj, list) or not entries_obj:
            print("ERROR: Supplementary deploy manifest entries must be a non-empty array")
            return None
        entries = cast(List[Any], entries_obj)

        entry_ids: Set[str] = set()
        for entry_obj in entries:
            if not isinstance(entry_obj, dict):
                print("ERROR: Each supplementary deploy manifest entry must be an object")
                return None
            entry = cast(Dict[str, Any], entry_obj)
            entry_id_obj = entry.get("id")
            kind_obj = entry.get("kind")
            source_obj = entry.get("source")
            target_obj = entry.get("target")
            if not all(
                isinstance(value, str) and value
                for value in (entry_id_obj, kind_obj, source_obj, target_obj)
            ):
                print(
                    "ERROR: Supplementary deploy entries require non-empty string id, kind, source, and target fields"
                )
                return None
            entry_id = cast(str, entry_id_obj)
            kind = cast(str, kind_obj)
            target = cast(str, target_obj)
            if entry_id in entry_ids:
                print(f"ERROR: Duplicate supplementary deploy entry id: {entry_id}")
                return None
            entry_ids.add(entry_id)
            if kind not in {"file", "directory"}:
                print(f"ERROR: Unsupported supplementary deploy entry kind: {kind}")
                return None
            forbidden_reason = self._is_forbidden_supplementary_target(Path(target))
            if forbidden_reason:
                print(f"ERROR: Invalid supplementary deploy target for {entry_id}: {forbidden_reason}")
                return None
            if kind == "directory":
                include_obj = entry.get("include")
                if include_obj is not None:
                    if not isinstance(include_obj, list) or not include_obj:
                        print(
                            f"ERROR: Directory supplementary deploy entry {entry_id} must use a non-empty include array"
                        )
                        return None
                    include_patterns = cast(List[Any], include_obj)
                    if not all(isinstance(pattern, str) and pattern for pattern in include_patterns):
                        print(
                            f"ERROR: Directory supplementary deploy entry {entry_id} must use a non-empty include array"
                        )
                        return None

        return manifest

    def _matches_manifest_patterns(self, rel_path: Path, patterns: List[str]) -> bool:
        rel_posix = rel_path.as_posix()
        pure_path = PurePosixPath(rel_posix)
        for pattern in patterns:
            if pure_path.match(pattern) or fnmatch(rel_posix, pattern):
                return True
            if pattern.startswith("**/") and pure_path.match(pattern[3:]):
                return True
        return False

    def _expand_manifest_entry(self, entry: Dict[str, Any], source_root: Path) -> List[Tuple[Path, Path]]:
        source = self._resolve_relative_path(source_root, entry["source"])
        target = self._resolve_target_relative_path(entry["target"])
        kind = entry["kind"]

        if kind == "file":
            if not source.is_file():
                raise FileNotFoundError(f"Supplementary deploy source file not found: {entry['source']}")
            return [(source, target)]

        if not source.is_dir():
            raise FileNotFoundError(f"Supplementary deploy source directory not found: {entry['source']}")

        patterns = entry.get("include") or ["**/*"]
        pairs: List[Tuple[Path, Path]] = []
        for src in sorted(source.rglob("*")):
            if not src.is_file():
                continue
            rel = src.relative_to(source)
            if not self._matches_manifest_patterns(rel, patterns):
                continue
            pairs.append((src, target / rel))
        return pairs

    def _cleanup_empty_parents(self, start: Path) -> None:
        current = start
        while current != self.target_root and current.exists():
            try:
                current.rmdir()
            except OSError:
                break
            current = current.parent

    def _sync_manifest_file(self, src: Path, dst: Path, backup_extension: str) -> str:
        if dst.exists() and dst.is_dir():
            raise IsADirectoryError(f"Supplementary deploy target is a directory: {dst}")

        if dst.exists() and filecmp.cmp(src, dst, shallow=False):
            return "unchanged"

        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            backup_path = dst.with_name(dst.name + backup_extension)
            shutil.copy2(dst, backup_path)
        shutil.copy2(src, dst)
        return "updated"

    def _sync_supplementary_deploy(self, manifest_path: Path, source_root: Path) -> bool:
        manifest = self._load_supplementary_manifest(manifest_path)
        if manifest is None:
            return False

        backup_extension = manifest["syncPolicy"].get("backupExtension", ".bak")
        state = self._load_state()
        previous = state.get("supplementary_deploy", {}).get("entries", {})
        next_entries: Dict[str, Any] = {}
        synced = unchanged = deleted = 0
        sync_started_at = datetime.now().timestamp()

        print("Syncing supplementary deploy targets...", end=" ")
        try:
            self.target_root.mkdir(parents=True, exist_ok=True)
            for entry in manifest["entries"]:
                entry_id = entry["id"]
                pairs = self._expand_manifest_entry(entry, source_root)
                for _, dst in pairs:
                    rel_dst = dst.relative_to(self.target_root)
                    forbidden_reason = self._is_forbidden_supplementary_target(rel_dst)
                    if forbidden_reason:
                        raise ValueError(
                            f"Expanded target {rel_dst.as_posix()} violates deploy boundary: {forbidden_reason}"
                        )

                current_targets: Set[str] = set()
                for src, dst in pairs:
                    rel_target = dst.relative_to(self.target_root).as_posix()
                    current_targets.add(rel_target)
                    result = self._sync_manifest_file(src, dst, backup_extension)
                    if result == "updated":
                        synced += 1
                    else:
                        unchanged += 1

                previous_targets = set(previous.get(entry_id, {}).get("targets", []))
                stale_targets = previous_targets - current_targets
                for rel_target in sorted(stale_targets):
                    stale_path = self._resolve_target_relative_path(rel_target)
                    if stale_path.exists() and stale_path.is_file():
                        shutil.copy2(stale_path, stale_path.with_name(stale_path.name + backup_extension))
                        stale_path.unlink()
                        deleted += 1
                        self._cleanup_empty_parents(stale_path.parent)

                next_entries[entry_id] = {
                    "targets": sorted(current_targets),
                    "updated_at": sync_started_at,
                }

            new_entry_ids = {entry["id"] for entry in manifest["entries"]}
            for orphan_id, orphan_info in previous.items():
                if orphan_id in new_entry_ids:
                    continue
                for rel_target in sorted(orphan_info.get("targets", [])):
                    stale_path = self._resolve_target_relative_path(rel_target)
                    if stale_path.exists() and stale_path.is_file():
                        shutil.copy2(stale_path, stale_path.with_name(stale_path.name + backup_extension))
                        stale_path.unlink()
                        deleted += 1
                        self._cleanup_empty_parents(stale_path.parent)
        except (FileNotFoundError, IsADirectoryError, OSError, ValueError) as error:
            print(f"ERROR: {error}")
            return False

        state["supplementary_deploy"] = {
            "schema_version": manifest["schemaVersion"],
            "manifest": manifest_path.relative_to(source_root).as_posix(),
            "last_run_ts": sync_started_at,
            "source_root": str(self.source_root),
            "sync_policy": manifest["syncPolicy"],
            "entries": next_entries,
        }
        self._save_state(state)
        print(f"Done ({synced} updated, {unchanged} unchanged, {deleted} deleted)")
        return True

    def _deploy_release_payload(self) -> bool:
        return self._sync_supplementary_deploy(self.supplementary_manifest, self.source_root)

    def upgrade(self) -> bool:
        print("=" * 60)
        print("AI Template Workspace Sync Tool")
        print("=" * 60)
        print(f"Source plugin folder: {self.source_root}")
        print(f"Target workspace: {self.target_root}")

        if not self._deploy_release_payload():
            return False

        print("=" * 60)
        print("Workspace sync completed successfully!")
        print("=" * 60)
        return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync AI Template supplementary files into a target workspace"
    )
    parser.add_argument(
        "target",
        nargs="?",
        help="Target workspace directory (defaults to the current working directory)",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent.resolve()
    target_root = Path(args.target).resolve() if args.target else Path.cwd().resolve()
    upgrader = TemplateUpgrader(repo_root, target_root=target_root)

    try:
        success = upgrader.upgrade()
        upgrader.save_last_exit_code(0 if success else 1)
        sys.exit(0 if success else 1)
    except Exception as error:
        print(f"ERROR: Unexpected error: {error}", file=sys.stderr)
        upgrader.save_last_exit_code(1)
        sys.exit(1)


if __name__ == "__main__":
    main()
