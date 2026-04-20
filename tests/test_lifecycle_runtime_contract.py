import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
COPILOT_SCRIPTS_DIR = REPO_ROOT / "copilot" / "scripts"
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures"

for candidate in (REPO_ROOT, SCRIPTS_DIR, COPILOT_SCRIPTS_DIR):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)


import refresh_mcp_runtime
import cleanup_runtime_artifacts
import install_vscode_plugin
import runtime_root
import upgrade_state
import verify_runtime_activation
import workspace_sync_server


class LifecycleRuntimeContractTests(unittest.TestCase):
    def _copy_fixture_tree(self, fixture_name: str, destination: Path) -> Path:
        shutil.copytree(FIXTURES_DIR / fixture_name, destination)
        return destination

    def _copy_fixture_file(self, fixture_name: str, destination: Path) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(FIXTURES_DIR / fixture_name, destination)
        return destination

    def _load_process_fixture(self, fixture_name: str, **tokens: str) -> list[dict[str, object]]:
        fixture_path = FIXTURES_DIR / fixture_name
        rows = json.loads(fixture_path.read_text(encoding="utf-8"))
        processes: list[dict[str, object]] = []
        for row in rows:
            self.assertIsInstance(row, dict)
            command_line_template = row.get("command_line_template")
            self.assertIsInstance(command_line_template, str)
            processes.append(
                {
                    "pid": row["pid"],
                    "name": row["name"],
                    "command_line": command_line_template.format(**tokens),
                }
            )
        return processes

    def _write_text(self, path: Path, content: str = "data") -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def _set_file_age_hours(self, path: Path, hours: float) -> None:
        modified_at = time.time() - (hours * 3600.0)
        os.utime(path, (modified_at, modified_at))

    def _run_hook(self, script_path: Path, payload: dict | str) -> subprocess.CompletedProcess[str]:
        stdin_data = payload if isinstance(payload, str) else json.dumps(payload)
        return subprocess.run(
            [sys.executable, str(script_path)],
            input=stdin_data,
            text=True,
            capture_output=True,
            check=False,
            cwd=str(REPO_ROOT),
        )

    def _run_script(self, script_path: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script_path), *args],
            text=True,
            capture_output=True,
            check=False,
            cwd=str(REPO_ROOT),
        )

    def _read_state_file(self, workspace_root: Path) -> dict:
        state_path = workspace_root / ".copilot-memory" / "upgrade_state.json"
        return json.loads(state_path.read_text(encoding="utf-8"))

    def test_hook_manifest_references_expected_scripts(self) -> None:
        hooks_path = REPO_ROOT / "copilot" / "hooks.json"
        hooks_json = json.loads(hooks_path.read_text(encoding="utf-8"))

        self.assertEqual(hooks_json.get("version"), 1)
        hooks = hooks_json.get("hooks")
        self.assertIsInstance(hooks, dict)
        self.assertEqual(set(hooks), {"sessionStart", "sessionEnd", "preCompact", "preToolUse"})

        expected_commands = {
            "sessionStart": "python scripts/session_init.py",
            "sessionEnd": "python scripts/session_end.py",
            "preCompact": "python pre-compact.py",
            "preToolUse": "python scripts/unified-pre-hook.py",
        }
        expected_paths = {
            "sessionStart": REPO_ROOT / "copilot" / "hooks" / "scripts" / "session_init.py",
            "sessionEnd": REPO_ROOT / "copilot" / "hooks" / "scripts" / "session_end.py",
            "preCompact": REPO_ROOT / "copilot" / "hooks" / "pre-compact.py",
            "preToolUse": REPO_ROOT / "copilot" / "hooks" / "scripts" / "unified-pre-hook.py",
        }

        for event_name, expected_command in expected_commands.items():
            entries = hooks.get(event_name)
            self.assertIsInstance(entries, list)
            self.assertEqual(len(entries), 1)
            entry = entries[0]
            self.assertEqual(entry.get("type"), "command")
            self.assertEqual(entry.get("bash"), expected_command)
            self.assertEqual(entry.get("cwd"), "copilot/hooks")
            self.assertTrue(expected_paths[event_name].is_file())

    def test_find_plugin_root_resolves_copied_minimal_plugin_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_root = self._copy_fixture_tree(
                "minimal_plugin_tree",
                Path(tmpdir) / "plugin-copy",
            )

            resolved = runtime_root.find_plugin_root(
                start_path=fixture_root / "workspace" / "deep" / "anchor.txt",
            )

            self.assertEqual(Path(resolved), fixture_root.resolve())

    def test_find_plugin_root_raises_for_broken_plugin_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_root = self._copy_fixture_tree(
                "broken_plugin_tree",
                Path(tmpdir) / "broken-plugin-copy",
            )

            with (
                mock.patch.object(runtime_root, "_iter_plugin_location_bases", return_value=()),
                mock.patch.object(runtime_root, "_iter_agent_plugin_bases", return_value=()),
            ):
                with self.assertRaisesRegex(RuntimeError, "Unable to resolve plugin root"):
                    runtime_root.find_plugin_root(
                        start_path=fixture_root / "workspace" / "deep" / "anchor.txt",
                    )

    def test_upgrade_state_load_initializes_schema_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            store = upgrade_state.UpgradeStateStore(workspace_root)

            state = store.load()

            self.assertEqual(state["schema_version"], upgrade_state.UpgradeStateStore.SCHEMA_VERSION)
            self.assertEqual(
                state["lifecycle_state"],
                {
                    "active_task": None,
                    "approval_pending": False,
                    "await_context": None,
                    "continuity": {},
                    "current_phase": None,
                    "current_plan_hash": None,
                    "status": "idle",
                    "updated_at": None,
                },
            )
            self.assertEqual(
                state["runtime_state"],
                {
                    "last_runtime_refresh": None,
                    "last_runtime_cleanup": None,
                    "last_sync": None,
                    "sync_check": None,
                    "updated_at": None,
                },
            )

    def test_upgrade_state_migrates_top_level_runtime_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            state_path = workspace_root / ".copilot-memory" / "upgrade_state.json"
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state_path.write_text(
                json.dumps(
                    {
                        "last_success_ts": 12.5,
                        "last_runtime_refresh": {
                            "timestamp": 21.0,
                            "matched_count": 1,
                        },
                        "last_sync": {
                            "timestamp": 34.0,
                            "success": True,
                        },
                        "last_runtime_cleanup": {
                            "timestamp": 44.0,
                            "deleted_count": 1,
                        },
                        "sync_check": {
                            "timestamp": 55.0,
                            "status": "ok",
                        },
                    }
                ),
                encoding="utf-8",
            )
            store = upgrade_state.UpgradeStateStore(workspace_root)

            state = store.load()

            self.assertEqual(state["schema_version"], upgrade_state.UpgradeStateStore.SCHEMA_VERSION)
            self.assertEqual(state["lifecycle_state"]["status"], "idle")
            self.assertEqual(state["lifecycle_state"]["updated_at"], 12.5)
            self.assertEqual(
                state["runtime_state"]["last_runtime_refresh"],
                {"timestamp": 21.0, "matched_count": 1},
            )
            self.assertEqual(
                state["runtime_state"]["last_sync"],
                {"timestamp": 34.0, "success": True},
            )
            self.assertEqual(
                state["runtime_state"]["last_runtime_cleanup"],
                {"timestamp": 44.0, "deleted_count": 1},
            )
            self.assertEqual(
                state["runtime_state"]["sync_check"],
                {"timestamp": 55.0, "status": "ok"},
            )
            self.assertEqual(state["runtime_state"]["updated_at"], 44.0)

    def test_upgrade_state_recovers_from_corrupted_state_fixtures(self) -> None:
        for fixture_name in (
            "corrupted_state/invalid-json.json",
            "corrupted_state/non-dict.json",
        ):
            with self.subTest(fixture_name=fixture_name):
                with tempfile.TemporaryDirectory() as tmpdir:
                    workspace_root = Path(tmpdir)
                    state_path = workspace_root / ".copilot-memory" / "upgrade_state.json"
                    self._copy_fixture_file(fixture_name, state_path)
                    store = upgrade_state.UpgradeStateStore(workspace_root)

                    recovered = store.load()

                    self.assertEqual(
                        recovered["schema_version"],
                        upgrade_state.UpgradeStateStore.SCHEMA_VERSION,
                    )
                    self.assertEqual(recovered["lifecycle_state"]["status"], "idle")
                    self.assertIsNone(recovered["runtime_state"]["last_sync"])

                    store.update_lifecycle_state(
                        current_phase="INIT",
                        status="active",
                        active_task="recover corrupted state",
                    )
                    stored = self._read_state_file(workspace_root)
                    self.assertEqual(stored["lifecycle_state"]["current_phase"], "INIT")
                    self.assertEqual(stored["lifecycle_state"]["status"], "active")

    def test_runtime_refresh_write_shape_updates_runtime_state_and_top_level(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            store = upgrade_state.UpgradeStateStore(workspace_root)
            payload = {
                "timestamp": 123.25,
                "plugin_root": str(workspace_root),
                "dry_run": False,
                "matched_count": 2,
                "terminated_count": 1,
                "terminated_pids": [101],
                "failed": [],
                "target_scripts": ["runtime_launcher.py"],
            }

            store.update_runtime_refresh(payload)
            stored = self._read_state_file(workspace_root)

            self.assertEqual(stored["last_runtime_refresh"], payload)
            self.assertEqual(stored["runtime_state"]["last_runtime_refresh"], payload)
            self.assertEqual(stored["runtime_state"]["updated_at"], payload["timestamp"])
            self.assertEqual(stored["schema_version"], upgrade_state.UpgradeStateStore.SCHEMA_VERSION)

    def test_refresh_runtime_processes_dry_run_matches_only_target_plugin_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_root = self._copy_fixture_tree(
                "minimal_plugin_tree",
                Path(tmpdir) / "plugin-copy",
            )
            processes = self._load_process_fixture(
                "stale_runtime/dry_run_processes.json",
                plugin_root=plugin_root.as_posix(),
                tmpdir=Path(tmpdir).as_posix(),
            )
            matching_process = processes[0]
            nonmatching_processes = processes[1:]

            with (
                mock.patch.object(
                    refresh_mcp_runtime,
                    "_list_processes",
                    return_value=[matching_process, *nonmatching_processes],
                ),
                mock.patch.object(refresh_mcp_runtime, "_terminate_process") as terminate_process,
                mock.patch.object(refresh_mcp_runtime.os, "getpid", return_value=999999),
            ):
                result = refresh_mcp_runtime.refresh_runtime_processes(
                    plugin_root=plugin_root,
                    dry_run=True,
                    write_state=False,
                )

            self.assertEqual(result["matched_count"], 1)
            self.assertEqual(result["terminated_count"], 0)
            self.assertEqual(result["terminated_pids"], [])
            self.assertEqual(result["failed"], [])
            self.assertEqual(result["matched"], [matching_process])
            terminate_process.assert_not_called()
            self.assertFalse((plugin_root / ".copilot-memory" / "upgrade_state.json").exists())

    def test_refresh_runtime_processes_terminates_matches_and_records_runtime_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            plugin_root = self._copy_fixture_tree(
                "minimal_plugin_tree",
                Path(tmpdir) / "plugin-copy",
            )
            processes = self._load_process_fixture(
                "stale_runtime/terminate_processes.json",
                plugin_root=plugin_root.as_posix(),
            )
            matching_process = processes[0]
            ignored_process = processes[1]

            with (
                mock.patch.object(
                    refresh_mcp_runtime,
                    "_list_processes",
                    return_value=[matching_process, ignored_process],
                ),
                mock.patch.object(refresh_mcp_runtime, "_terminate_process") as terminate_process,
                mock.patch.object(refresh_mcp_runtime.os, "getpid", return_value=999999),
                mock.patch.object(refresh_mcp_runtime.time, "time", return_value=789.5),
            ):
                result = refresh_mcp_runtime.refresh_runtime_processes(
                    plugin_root=plugin_root,
                    dry_run=False,
                    write_state=True,
                )

            terminate_process.assert_called_once_with(3501)
            self.assertEqual(result["matched_count"], 1)
            self.assertEqual(result["terminated_count"], 1)
            self.assertEqual(result["terminated_pids"], [3501])
            self.assertEqual(result["matched"], [matching_process])
            self.assertEqual(result["failed"], [])

            stored = self._read_state_file(plugin_root)
            recorded_refresh = stored["runtime_state"]["last_runtime_refresh"]
            self.assertEqual(recorded_refresh["timestamp"], 789.5)
            self.assertEqual(recorded_refresh["plugin_root"], str(plugin_root.resolve()))
            self.assertIs(recorded_refresh["dry_run"], False)
            self.assertEqual(recorded_refresh["matched_count"], 1)
            self.assertEqual(recorded_refresh["terminated_count"], 1)
            self.assertEqual(recorded_refresh["terminated_pids"], [3501])
            self.assertEqual(
                recorded_refresh["target_scripts"],
                list(refresh_mcp_runtime.TARGET_SCRIPT_NAMES),
            )

    def test_runtime_cleanup_write_shape_updates_runtime_state_and_top_level(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            store = upgrade_state.UpgradeStateStore(workspace_root)
            payload = {
                "timestamp": 223.5,
                "workspace_root": str(workspace_root),
                "dry_run": False,
                "candidate_counts": {"backup_files": 1, "marker_files": 1, "total": 2},
                "deleted": ["AGENTS.md.bak"],
                "deleted_count": 1,
                "failed": [],
            }

            store.update_runtime_cleanup(payload)
            stored = self._read_state_file(workspace_root)

            self.assertEqual(stored["last_runtime_cleanup"], payload)
            self.assertEqual(stored["runtime_state"]["last_runtime_cleanup"], payload)
            self.assertEqual(stored["runtime_state"]["updated_at"], payload["timestamp"])

    def test_record_sync_result_writes_wrapper_sync_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            runtime_info = {
                "repo_root": str(REPO_ROOT),
                "upgrade_script": str(REPO_ROOT / "scripts" / "upgrade_ai.py"),
            }

            with mock.patch.object(workspace_sync_server.time, "time", return_value=456.5):
                workspace_sync_server._record_sync_result(
                    workspace_root,
                    runtime_info,
                    exit_code=0,
                    success=True,
                    timed_out=False,
                )

            stored = self._read_state_file(workspace_root)
            expected_sync = {
                "timestamp": 456.5,
                "target_workspace": str(workspace_root),
                "exit_code": 0,
                "success": True,
                "timeout": False,
                "repo_root": runtime_info["repo_root"],
                "upgrade_script": runtime_info["upgrade_script"],
                "wrapper": "workspace_sync_server",
            }

            self.assertEqual(stored["last_sync"], expected_sync)
            self.assertEqual(stored["runtime_state"]["last_sync"], expected_sync)
            self.assertEqual(stored["runtime_state"]["updated_at"], 456.5)
            self.assertEqual(stored["last_exit_code"], 0)
            self.assertEqual(stored["last_success_ts"], 456.5)

    def test_workspace_sync_server_bootstraps_mcp_with_uv_when_missing(self) -> None:
        missing_mcp_error = ModuleNotFoundError("No module named 'mcp'", name="mcp")
        completed = subprocess.CompletedProcess(args=["uv"], returncode=0)

        with (
            mock.patch.object(workspace_sync_server, "import_module", side_effect=missing_mcp_error),
            mock.patch.object(workspace_sync_server.subprocess, "run", return_value=completed) as run_mock,
            mock.patch.dict(workspace_sync_server.os.environ, {}, clear=True),
            mock.patch.object(workspace_sync_server.sys, "argv", ["workspace_sync_server.py"]),
        ):
            with self.assertRaises(SystemExit) as exit_info:
                workspace_sync_server._build_mcp_server()

        self.assertEqual(exit_info.exception.code, 0)
        command = run_mock.call_args.args[0]
        env = run_mock.call_args.kwargs["env"]

        self.assertEqual(command[:5], ["uv", "run", "--with", "mcp", "python"])
        self.assertEqual(Path(command[5]), COPILOT_SCRIPTS_DIR / "workspace_sync_server.py")
        self.assertEqual(env[workspace_sync_server.MCP_BOOTSTRAP_ENV_VAR], "1")

    def test_workspace_sync_server_raises_if_bootstrap_already_attempted(self) -> None:
        missing_mcp_error = ModuleNotFoundError("No module named 'mcp'", name="mcp")

        with (
            mock.patch.object(workspace_sync_server, "import_module", side_effect=missing_mcp_error),
            mock.patch.dict(
                workspace_sync_server.os.environ,
                {workspace_sync_server.MCP_BOOTSTRAP_ENV_VAR: "1"},
                clear=True,
            ),
        ):
            with self.assertRaisesRegex(RuntimeError, "automatic uv bootstrap"):
                workspace_sync_server._build_mcp_server()

    def test_workspace_sync_server_runs_in_process_and_records_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)

            result = workspace_sync_server._run_sync(str(workspace_root))

            self.assertTrue(result["success"], result["stderr"])
            self.assertEqual(result["exit_code"], 0)
            self.assertEqual(result["target_workspace"], str(workspace_root.resolve()))
            self.assertEqual(result["repo_root"], str(REPO_ROOT.resolve()))
            self.assertEqual(
                result["command"],
                [
                    sys.executable,
                    str(REPO_ROOT / "scripts" / "upgrade_ai.py"),
                    str(workspace_root.resolve()),
                ],
            )
            self.assertEqual(
                result["upgrade_script"],
                str((REPO_ROOT / "scripts" / "upgrade_ai.py").resolve()),
            )
            self.assertIn("Workspace sync completed successfully!", result["stdout"])
            self.assertEqual(result["stderr"], "")

            self.assertTrue((workspace_root / "AGENTS.md").is_file())
            self.assertTrue((workspace_root / "constitution.md").is_file())
            self.assertTrue((workspace_root / ".github" / "copilot-instructions.md").is_file())
            self.assertTrue((workspace_root / ".github" / "instructions").is_dir())

            stored = self._read_state_file(workspace_root)
            self.assertEqual(stored["last_sync"]["wrapper"], "workspace_sync_server")
            self.assertIs(stored["last_sync"]["success"], True)
            self.assertEqual(stored["last_sync"]["target_workspace"], str(workspace_root.resolve()))
            self.assertEqual(stored["last_exit_code"], 0)

    def test_runtime_launcher_runpy_workspace_sync_self_check_from_non_repo_cwd(self) -> None:
        launcher_path = COPILOT_SCRIPTS_DIR / "runtime_launcher.py"
        workspace_sync_path = COPILOT_SCRIPTS_DIR / "workspace_sync_server.py"
        command = [
            sys.executable,
            "-c",
            (
                "import runpy, sys; "
                f"sys.argv = {[str(launcher_path), 'workspace-sync', '--self-check']!r}; "
                f"runpy.run_path({str(launcher_path)!r}, run_name='__main__')"
            ),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            env = os.environ.copy()
            env["PYTHONPATH"] = ""

            completed = subprocess.run(
                command,
                text=True,
                capture_output=True,
                check=False,
                cwd=tmpdir,
                env=env,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        runtime_info = json.loads(completed.stdout)

        self.assertEqual(runtime_info["cwd"], str(Path(tmpdir).resolve()))
        self.assertEqual(runtime_info["script_path"], str(workspace_sync_path.resolve()))
        self.assertEqual(runtime_info["argv"], [str(workspace_sync_path), "--self-check"])
        self.assertEqual(runtime_info["repo_root"], str(REPO_ROOT.resolve()))

    def test_session_hooks_fail_open_on_malformed_payload(self) -> None:
        session_init = REPO_ROOT / "copilot" / "hooks" / "scripts" / "session_init.py"
        result = self._run_hook(session_init, "{not-json")
        self.assertEqual(result.returncode, 0)

    def test_installer_settings_enable_hook_manifest_and_custom_hooks(self) -> None:
        settings: dict[str, object] = {
            "chat.pluginLocations": [],
            "chat.hookFilesLocations": [],
            "chat.plugins.enabled": False,
            "chat.useCustomAgentHooks": False,
        }
        plugin_root = str(REPO_ROOT)
        expected_hook_manifest = str((REPO_ROOT / "copilot" / "hooks.json").resolve())

        changed = install_vscode_plugin._update_settings(settings, plugin_root)

        self.assertTrue(changed)
        self.assertEqual(settings["chat.pluginLocations"], {plugin_root: True})
        self.assertEqual(
            settings["chat.hookFilesLocations"],
            {expected_hook_manifest: True},
        )
        self.assertIs(settings["chat.plugins.enabled"], True)
        self.assertIs(settings["chat.useCustomAgentHooks"], True)

    def test_runtime_activation_verifier_accepts_explicit_settings_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_path = Path(tmpdir) / "settings.json"
            plugin_root = REPO_ROOT.resolve()
            hook_manifest = str((plugin_root / "copilot" / "hooks.json").resolve())
            settings_path.write_text(
                json.dumps(
                    {
                        "chat.pluginLocations": {str(plugin_root): True},
                        "chat.hookFilesLocations": {hook_manifest: True},
                        "chat.plugins.enabled": True,
                        "chat.useCustomAgentHooks": True,
                    }
                ),
                encoding="utf-8",
            )

            result = verify_runtime_activation.verify_runtime_activation(
                settings_files=[str(settings_path)],
                plugin_root=plugin_root,
            )

            self.assertTrue(result["ok"])
            self.assertEqual(result["manifest_issues"], [])
            self.assertEqual(len(result["target_results"]), 1)
            self.assertTrue(result["target_results"][0]["ok"])
            self.assertEqual(result["target_results"][0]["issues"], [])

    def test_runtime_activation_verifier_reports_missing_settings_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_path = Path(tmpdir) / "settings.json"
            settings_path.write_text("{}\n", encoding="utf-8")

            result = verify_runtime_activation.verify_runtime_activation(
                settings_files=[str(settings_path)],
                plugin_root=REPO_ROOT,
            )

            self.assertFalse(result["ok"])
            self.assertEqual(result["manifest_issues"], [])
            self.assertEqual(len(result["target_results"]), 1)
            self.assertFalse(result["target_results"][0]["ok"])
            self.assertEqual(
                result["target_results"][0]["issues"],
                [
                    "chat.pluginLocations missing plugin root",
                    "chat.hookFilesLocations missing hook manifest",
                    "chat.useCustomAgentHooks is not true",
                    "chat.plugins.enabled is not true",
                ],
            )

    def test_installer_main_runs_post_install_verification(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_path = Path(tmpdir) / "settings.json"
            stdout_buffer = StringIO()
            stderr_buffer = StringIO()

            with (
                mock.patch.object(
                    install_vscode_plugin,
                    "parse_args",
                    return_value=argparse.Namespace(
                        settings_files=[str(settings_path)],
                        dry_run=False,
                        no_refresh_runtime=True,
                    ),
                ),
                redirect_stdout(stdout_buffer),
                redirect_stderr(stderr_buffer),
            ):
                exit_code = install_vscode_plugin.main()

            settings = json.loads(settings_path.read_text(encoding="utf-8"))
            self.assertEqual(exit_code, 0)
            self.assertIn("post-install verification passed", stdout_buffer.getvalue())
            self.assertEqual(stderr_buffer.getvalue(), "")
            self.assertTrue(settings["chat.pluginLocations"][str(REPO_ROOT.resolve())])
            self.assertTrue(settings["chat.plugins.enabled"])
            self.assertTrue(settings["chat.useCustomAgentHooks"])

    def test_installer_main_skips_post_install_verification_in_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_path = Path(tmpdir) / "settings.json"
            stdout_buffer = StringIO()
            stderr_buffer = StringIO()

            with (
                mock.patch.object(
                    install_vscode_plugin,
                    "parse_args",
                    return_value=argparse.Namespace(
                        settings_files=[str(settings_path)],
                        dry_run=True,
                        no_refresh_runtime=True,
                    ),
                ),
                mock.patch(
                    "scripts.verify_runtime_activation.verify_runtime_activation",
                    side_effect=AssertionError("dry-run should not verify runtime activation"),
                ),
                redirect_stdout(stdout_buffer),
                redirect_stderr(stderr_buffer),
            ):
                exit_code = install_vscode_plugin.main()

            self.assertEqual(exit_code, 0)
            self.assertIn("would update", stdout_buffer.getvalue())
            self.assertEqual(stderr_buffer.getvalue(), "")
            self.assertFalse(settings_path.exists())

    def test_installer_main_returns_non_zero_when_verification_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_path = Path(tmpdir) / "settings.json"
            stdout_buffer = StringIO()
            stderr_buffer = StringIO()
            verification_result = {
                "ok": False,
                "plugin_root": str(REPO_ROOT.resolve()),
                "manifest_issues": [],
                "target_results": [
                    {
                        "settings_file": str(settings_path),
                        "ok": False,
                        "issues": ["chat.plugins.enabled is not true"],
                    }
                ],
            }

            with (
                mock.patch.object(
                    install_vscode_plugin,
                    "parse_args",
                    return_value=argparse.Namespace(
                        settings_files=[str(settings_path)],
                        dry_run=False,
                        no_refresh_runtime=True,
                    ),
                ),
                mock.patch(
                    "scripts.verify_runtime_activation.verify_runtime_activation",
                    return_value=verification_result,
                ),
                redirect_stdout(stdout_buffer),
                redirect_stderr(stderr_buffer),
            ):
                exit_code = install_vscode_plugin.main()

            self.assertEqual(exit_code, 1)
            self.assertIn(
                f"post-install verification missing activation state: {settings_path}",
                stderr_buffer.getvalue(),
            )
            self.assertIn("  - chat.plugins.enabled is not true", stderr_buffer.getvalue())
            self.assertIn("post-install verification failed", stderr_buffer.getvalue())

    def test_runtime_activation_verifier_uses_default_settings_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_path = Path(tmpdir) / "settings.json"
            plugin_root = REPO_ROOT.resolve()
            hook_manifest = str((plugin_root / "copilot" / "hooks.json").resolve())
            settings_path.write_text(
                json.dumps(
                    {
                        "chat.pluginLocations": [str(plugin_root)],
                        "chat.hookFilesLocations": [hook_manifest],
                        "chat.plugins.enabled": True,
                        "chat.useCustomAgentHooks": True,
                    }
                ),
                encoding="utf-8",
            )

            with mock.patch.object(
                verify_runtime_activation,
                "_iter_default_settings_paths",
                return_value=[settings_path],
            ):
                result = verify_runtime_activation.verify_runtime_activation(plugin_root=plugin_root)

            self.assertTrue(result["ok"])
            self.assertEqual(result["target_results"][0]["settings_file"], str(settings_path))

    def test_orchestrator_agent_matches_thin_contract_guard(self) -> None:
        orchestrator_path = REPO_ROOT / "copilot" / "agents" / "orchestrator.agent.md"
        content = orchestrator_path.read_text(encoding="utf-8")

        self.assertIn("# ORCHESTRATOR AGENT", content)
        self.assertIn("## Mission", content)
        self.assertIn("## Boundary", content)
        self.assertIn("## Session-Once Sync Check", content)
        self.assertIn("## Lifecycle Protocol", content)
        self.assertIn("## Phase-Boundary State Writes", content)
        self.assertIn("## Planning And Output Contract", content)
        self.assertIn("INIT -> ATOMIZE -> PLAN -> EXECUTE -> REPORT -> AWAIT -> FINALIZE", content)
        self.assertIn("INIT`, `PLAN`, `REPORT`, `AWAIT`, and `FINALIZE`", content)

        self.assertNotIn("Strategic Modes", content)
        self.assertNotIn("Workflow Recipes", content)
        self.assertNotIn("Agent Registry & Routing", content)

    def test_runtime_artifact_cleanup_dry_run_finds_stale_backup_without_deleting(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            stale_backup = self._write_text(workspace_root / "AGENTS.md.bak")
            fresh_backup = self._write_text(workspace_root / "constitution.md.bak")
            self._set_file_age_hours(stale_backup, 24.0 * 8.0)
            self._set_file_age_hours(fresh_backup, 2.0)

            result = cleanup_runtime_artifacts.cleanup_runtime_artifacts(
                workspace_root=workspace_root,
                dry_run=True,
            )

            self.assertTrue(stale_backup.exists())
            self.assertTrue(fresh_backup.exists())
            self.assertEqual(result["candidate_counts"]["backup_files"], 1)
            self.assertEqual(result["candidate_counts"]["marker_files"], 0)
            self.assertEqual(result["deleted_count"], 0)
            self.assertIn("AGENTS.md.bak", result["candidates"])

            stored = self._read_state_file(workspace_root)
            self.assertTrue(stored["runtime_state"]["last_runtime_cleanup"]["dry_run"])
            self.assertEqual(stored["runtime_state"]["last_runtime_cleanup"]["deleted_count"], 0)

    def test_runtime_artifact_cleanup_real_run_deletes_stale_candidates_and_records_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            stale_backup = self._write_text(workspace_root / ".github" / "copilot-instructions.md.bak")
            stale_session_marker = self._write_text(
                workspace_root / ".copilot-memory" / "runtime" / "session-test.json",
                content="{}",
            )
            stale_compact_marker = self._write_text(
                workspace_root / ".copilot-memory" / "compact-test.json",
                content="{}",
            )
            self._set_file_age_hours(stale_backup, 24.0 * 8.0)
            self._set_file_age_hours(stale_session_marker, 48.0)
            self._set_file_age_hours(stale_compact_marker, 48.0)

            result = cleanup_runtime_artifacts.cleanup_runtime_artifacts(
                workspace_root=workspace_root,
                dry_run=False,
            )

            self.assertFalse(stale_backup.exists())
            self.assertFalse(stale_session_marker.exists())
            self.assertFalse(stale_compact_marker.exists())
            self.assertEqual(result["deleted_count"], 3)
            self.assertEqual(result["candidate_counts"]["total"], 3)
            self.assertEqual(result["failed"], [])

            stored = self._read_state_file(workspace_root)
            cleanup_state = stored["runtime_state"]["last_runtime_cleanup"]
            self.assertFalse(cleanup_state["dry_run"])
            self.assertEqual(cleanup_state["deleted_count"], 3)
            self.assertCountEqual(
                cleanup_state["deleted"],
                [
                    ".github/copilot-instructions.md.bak",
                    ".copilot-memory/runtime/session-test.json",
                    ".copilot-memory/compact-test.json",
                ],
            )

    def test_runtime_artifact_cleanup_preserves_non_stale_and_unmanaged_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            fresh_backup = self._write_text(workspace_root / "AGENTS.md.bak")
            fresh_marker = self._write_text(
                workspace_root / ".copilot-memory" / "runtime" / "lifecycle-current.json",
                content="{}",
            )
            unmanaged_backup = self._write_text(
                workspace_root / "notes" / "ignored.txt.bak",
                content="ignore",
            )
            self._set_file_age_hours(fresh_backup, 2.0)
            self._set_file_age_hours(fresh_marker, 2.0)
            self._set_file_age_hours(unmanaged_backup, 24.0 * 30.0)

            result = cleanup_runtime_artifacts.cleanup_runtime_artifacts(
                workspace_root=workspace_root,
                dry_run=False,
            )

            self.assertTrue(fresh_backup.exists())
            self.assertTrue(fresh_marker.exists())
            self.assertTrue(unmanaged_backup.exists())
            self.assertEqual(result["candidate_counts"]["total"], 0)
            self.assertEqual(result["deleted_count"], 0)

    def test_runtime_artifact_cleanup_is_idempotent_for_copied_fixture_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = self._copy_fixture_tree(
                "cleanup_workspace",
                Path(tmpdir) / "workspace",
            )

            stale_backups = [
                workspace_root / "AGENTS.md.bak",
                workspace_root / ".github" / "copilot-instructions.md.bak",
            ]
            stale_markers = [
                workspace_root / ".copilot-memory" / "compact-fixture.json",
                workspace_root / ".copilot-memory" / "runtime" / "session-fixture.json",
            ]
            fresh_marker = workspace_root / ".copilot-memory" / "runtime" / "lifecycle-fresh.json"
            unmanaged_backup = workspace_root / "notes" / "ignored.txt.bak"

            for path in stale_backups:
                self._set_file_age_hours(path, 24.0 * 8.0)
            for path in stale_markers:
                self._set_file_age_hours(path, 48.0)
            self._set_file_age_hours(fresh_marker, 2.0)
            self._set_file_age_hours(unmanaged_backup, 24.0 * 30.0)

            first_result = cleanup_runtime_artifacts.cleanup_runtime_artifacts(
                workspace_root=workspace_root,
                dry_run=False,
            )
            second_result = cleanup_runtime_artifacts.cleanup_runtime_artifacts(
                workspace_root=workspace_root,
                dry_run=False,
            )

            self.assertEqual(first_result["deleted_count"], 4)
            self.assertEqual(first_result["candidate_counts"]["total"], 4)
            self.assertEqual(second_result["candidate_counts"]["total"], 0)
            self.assertEqual(second_result["deleted_count"], 0)
            self.assertEqual(second_result["failed"], [])
            self.assertTrue(fresh_marker.exists())
            self.assertTrue(unmanaged_backup.exists())

            stored = self._read_state_file(workspace_root)
            cleanup_state = stored["runtime_state"]["last_runtime_cleanup"]
            self.assertFalse(cleanup_state["dry_run"])
            self.assertEqual(cleanup_state["candidate_counts"]["total"], 0)
            self.assertEqual(cleanup_state["deleted_count"], 0)

    def test_session_end_triggers_cleanup_when_workspace_in_payload(self) -> None:
        session_end = REPO_ROOT / "copilot" / "hooks" / "scripts" / "session_end.py"

        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            stale_marker = self._write_text(
                workspace_root / ".copilot-memory" / "session-stale.json",
                content="{}",
            )
            self._set_file_age_hours(stale_marker, 48.0)
            payload = {
                "workspacePath": str(workspace_root),
                "timestamp": 1_713_456_789_000,
                "source": "unit-test",
            }

            result = self._run_hook(session_end, payload)
            self.assertEqual(result.returncode, 0, result.stderr)

            self.assertFalse(stale_marker.exists())

    def test_session_end_skips_cleanup_when_no_workspace_in_payload(self) -> None:
        session_end = REPO_ROOT / "copilot" / "hooks" / "scripts" / "session_end.py"

        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            payload = {
                "timestamp": 1_713_456_789_000,
                "source": "unit-test",
            }

            result = self._run_hook(session_end, payload)
            self.assertEqual(result.returncode, 0, result.stderr)

            state_path = workspace_root / ".copilot-memory" / "upgrade_state.json"
            self.assertFalse(
                state_path.exists(),
                "cleanup must not have written state into temp dir when no workspace in payload",
            )


if __name__ == "__main__":
    unittest.main()