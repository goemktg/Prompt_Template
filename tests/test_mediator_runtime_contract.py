import json
import py_compile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class MediatorRuntimeContractTests(unittest.TestCase):
    def _read_text(self, relative_path: str) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def _load_json(self, relative_path: str) -> dict:
        return json.loads(self._read_text(relative_path))

    def test_mediator_skills_exist_with_expected_frontmatter(self) -> None:
        expectations = {
            "copilot/skills/deep-think/SKILL.md": (
                "name: deep-think",
                "@deep-think-mediator",
                "@dt-council-mediator",
                "host-provided native Gemini access",
            ),
            "copilot/skills/dt-council/SKILL.md": (
                "name: dt-council",
                "@dt-council-mediator",
                "host-provided native Gemini access",
            ),
        }

        for relative_path, required_fragments in expectations.items():
            with self.subTest(relative_path=relative_path):
                content = self._read_text(relative_path)
                self.assertTrue(content.startswith("---\n"))
                for fragment in required_fragments:
                    self.assertIn(fragment, content)
                self.assertNotIn("@gemini-gateway", content)

    def test_mcp_config_preserves_existing_servers_and_repo_owned_mediator_runtime_servers(self) -> None:
        config = self._load_json("copilot/mcp.json")
        servers = config.get("mcpServers")
        self.assertIsInstance(servers, dict)

        for expected_server in ("context7", "memory", "workspace-sync", "sequentialthinking", "session-gate", "context-manager"):
            self.assertIn(expected_server, servers)

        session_gate = servers["session-gate"]
        self.assertIn("copilot/mcp-servers/session-gate/server.py", session_gate["args"])
        self.assertIn("SESSION_GATE_STATE_DIR", session_gate["env"])

        context_manager = servers["context-manager"]
        self.assertIn("copilot/mcp-servers/context-manager/server.py", context_manager["args"])
        self.assertIn("CONTEXT_MANAGER_BASE_DIR", context_manager["env"])

    def test_server_files_compile_and_export_expected_surfaces(self) -> None:
        expectations = {
            "copilot/mcp-servers/session-gate/server.py": ("def phase_transition(", "def validate_transition("),
            "copilot/mcp-servers/context-manager/server.py": ("def store_result(", "def retrieve_result("),
        }
        for relative_path, expected_fragments in expectations.items():
            with self.subTest(relative_path=relative_path):
                py_compile.compile(str(REPO_ROOT / relative_path), doraise=True)
                content = self._read_text(relative_path)
                for fragment in expected_fragments:
                    self.assertIn(fragment, content)

    def test_mediator_assets_do_not_claim_repo_owned_local_gemini_backend(self) -> None:
        for relative_path in (
            "copilot/agents/orchestrator.agent.md",
            "copilot/agents/deep-think-mediator.agent.md",
            "copilot/agents/dt-council-mediator.agent.md",
            "copilot/skills/deep-think/SKILL.md",
            "copilot/skills/dt-council/SKILL.md",
            "AGENTS.md",
            "README.md",
        ):
            with self.subTest(relative_path=relative_path):
                content = self._read_text(relative_path)
                self.assertNotIn("local Gemini MCP backend is configured", content)
                self.assertNotIn("`gemini` MCP server when configured in `copilot/mcp.json`", content)


if __name__ == "__main__":
    unittest.main()