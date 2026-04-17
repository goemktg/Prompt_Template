#!/usr/bin/env python3

import json
import sys
import tempfile
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE_ROOT))

from scripts.upgrade_ai import TemplateUpgrader  # noqa: E402


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, content: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(content, indent=2), encoding="utf-8")


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def test_orphan_entry_cleanup() -> None:
    """Removed entry_id targets are deleted and backed up after sync."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        sandbox = Path(tmp_dir)
        source_root = sandbox / "plugin"
        target_root = sandbox / "workspace"

        manifest = {
            "schemaVersion": 1,
            "syncPolicy": {"overwrite": "force", "backupExtension": ".bak"},
            "entries": [
                {
                    "id": "workspace-agents-anchor",
                    "kind": "file",
                    "source": "AGENTS.md",
                    "target": "AGENTS.md",
                },
            ],
        }

        write_text(source_root / "AGENTS.md", "plugin agents\n")
        write_json(source_root / "copilot" / "deploy-manifest.json", manifest)

        write_text(target_root / "AGENTS.md", "workspace agents\n")
        write_text(target_root / ".github" / "orphan.md", "orphan content\n")
        write_json(
            target_root / ".copilot-memory" / "upgrade_state.json",
            {
                "schema_version": 1,
                "supplementary_deploy": {
                    "schema_version": 1,
                    "manifest": "copilot/deploy-manifest.json",
                    "entries": {
                        "workspace-agents-anchor": {"targets": ["AGENTS.md"]},
                        "old-entry": {"targets": [".github/orphan.md"]},
                    },
                },
            },
        )

        upgrader = TemplateUpgrader(source_root, target_root=target_root, ignore_delay=True)

        if not upgrader._deploy_release_payload():
            raise AssertionError("Sync failed unexpectedly in orphan cleanup test")

        assert not (target_root / ".github" / "orphan.md").exists()
        assert (target_root / ".github" / "orphan.md.bak").read_text(encoding="utf-8") == "orphan content\n"


def test_forbidden_target_expansion_fails() -> None:
    """Directory expansion resolving into a forbidden prefix must fail closed."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        sandbox = Path(tmp_dir)
        source_root = sandbox / "plugin"
        target_root = sandbox / "workspace"

        manifest = {
            "schemaVersion": 1,
            "syncPolicy": {"overwrite": "force", "backupExtension": ".bak"},
            "entries": [
                {
                    "id": "breach-attempt",
                    "kind": "directory",
                    "source": "payload",
                    "target": "copilot",
                    "include": ["**/*.md"],
                },
            ],
        }

        write_text(source_root / "payload" / "agents" / "evil.md", "malicious agent\n")
        write_json(source_root / "copilot" / "deploy-manifest.json", manifest)

        upgrader = TemplateUpgrader(source_root, target_root=target_root, ignore_delay=True)

        result = upgrader._deploy_release_payload()
        assert not result
        assert not (target_root / "copilot" / "agents" / "evil.md").exists()


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp_dir:
        sandbox = Path(tmp_dir)
        source_root = sandbox / "plugin"
        target_root = sandbox / "workspace"

        old_manifest = {
            "schemaVersion": 1,
            "syncPolicy": {"overwrite": "force", "backupExtension": ".bak"},
            "entries": [
                {
                    "id": "shared-instructions",
                    "kind": "directory",
                    "source": "shared/instructions",
                    "target": ".github/instructions",
                    "include": ["*.instructions.md", "**/*.instructions.md"],
                },
            ],
        }
        new_manifest = {
            "schemaVersion": 1,
            "syncPolicy": {"overwrite": "force", "backupExtension": ".bak"},
            "entries": [
                {
                    "id": "workspace-agents-anchor",
                    "kind": "file",
                    "source": "AGENTS.md",
                    "target": "AGENTS.md",
                },
                {
                    "id": "shared-instructions",
                    "kind": "directory",
                    "source": "shared/instructions",
                    "target": ".github/instructions",
                    "include": ["*.instructions.md", "**/*.instructions.md"],
                },
            ],
        }

        write_text(source_root / "AGENTS.md", "plugin agents\n")
        write_text(
            source_root / "shared" / "instructions" / "new.instructions.md",
            "new instruction\n",
        )
        write_text(source_root / "README.md", "plugin readme should not deploy\n")
        write_text(source_root / "plugin.json", '{"name": "plugin-source"}\n')
        write_json(source_root / "copilot" / "deploy-manifest.json", new_manifest)
        write_json(source_root / "LAST_VERSION.json", {"version": "2.0.0"})

        write_text(target_root / "README.md", "workspace readme\n")
        write_text(target_root / "plugin.json", '{"name": "workspace-plugin"}\n')
        write_text(target_root / "AGENTS.md", "workspace agents\n")
        write_text(target_root / ".github" / "copilot-instructions.md", "workspace instructions\n")
        write_text(target_root / ".github" / "instructions" / "old.instructions.md", "stale instruction\n")
        write_json(
            target_root / ".copilot-memory" / "upgrade_state.json",
            {
                "schema_version": 1,
                "supplementary_deploy": {
                    "schema_version": 1,
                    "manifest": "copilot/deploy-manifest.json",
                    "entries": {
                        "workspace-agents-anchor": {"targets": ["AGENTS.md"]},
                        "shared-instructions": {
                            "targets": [".github/instructions/old.instructions.md"]
                        },
                    },
                },
            },
        )

        upgrader = TemplateUpgrader(source_root, target_root=target_root, ignore_delay=True)

        if not upgrader.upgrade():
            raise AssertionError("Selective deployment failed")

        assert (target_root / "README.md").read_text(encoding="utf-8") == "workspace readme\n"
        assert (target_root / "plugin.json").read_text(encoding="utf-8") == '{"name": "workspace-plugin"}\n'
        assert (target_root / "AGENTS.md").read_text(encoding="utf-8") == "plugin agents\n"
        assert (target_root / "AGENTS.md.bak").read_text(encoding="utf-8") == "workspace agents\n"
        assert (
            (target_root / ".github" / "copilot-instructions.md").read_text(encoding="utf-8")
            == "workspace instructions\n"
        )
        assert (target_root / ".github" / "instructions" / "new.instructions.md").exists()
        assert not (target_root / ".github" / "instructions" / "old.instructions.md").exists()
        assert (
            (target_root / ".github" / "instructions" / "old.instructions.md.bak").read_text(
                encoding="utf-8"
            )
            == "stale instruction\n"
        )
        assert not (target_root / "copilot" / "deploy-manifest.json").exists()
        assert not (target_root / "LAST_VERSION.json").exists()

        state = read_json(target_root / ".copilot-memory" / "upgrade_state.json")
        deployed_targets = state["supplementary_deploy"]["entries"]
        assert state["supplementary_deploy"]["manifest"] == "copilot/deploy-manifest.json"
        assert deployed_targets["workspace-agents-anchor"]["targets"] == ["AGENTS.md"]
        assert deployed_targets["shared-instructions"]["targets"] == [
            ".github/instructions/new.instructions.md"
        ]

        write_json(source_root / "copilot" / "deploy-manifest.json", old_manifest)
        if not upgrader.upgrade():
            raise AssertionError("Second sync failed")

        assert not (target_root / "AGENTS.md").exists()
        assert (target_root / "AGENTS.md.bak").read_text(encoding="utf-8") == "plugin agents\n"

    test_orphan_entry_cleanup()
    test_forbidden_target_expansion_fails()
    print("All smoke tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())