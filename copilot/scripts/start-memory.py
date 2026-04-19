#!/usr/bin/env python3
"""Legacy launcher for mcp-memory-service.

SUPERSEDED: copilot/mcp.json now boots through copilot/scripts/runtime_launcher.py,
which acts as the shared runtime entrypoint for both memory and workspace-sync.
This file is retained for reference only.

Script location : copilot/scripts/start-memory.py
Workspace root  : two directory levels up from this file
Storage path    : <workspace_root>/.copilot-memory/memory.db
"""
import os
import subprocess
import sys

# Derive workspace root from this file's absolute location.
# __file__ is always resolved by Python regardless of the process CWD.
_here = os.path.dirname(os.path.abspath(__file__))          # copilot/scripts/
workspace_root = os.path.dirname(os.path.dirname(_here))    # <workspace>/

memory_dir = os.path.join(workspace_root, ".copilot-memory")
os.makedirs(memory_dir, exist_ok=True)

env = os.environ.copy()
env["MCP_MEMORY_STORAGE_BACKEND"] = "sqlite_vec"
env["MCP_MEMORY_SQLITE_PATH"] = os.path.join(memory_dir, "memory.db")
env["CUDA_VISIBLE_DEVICES"] = ""
env["MCP_MEMORY_USE_ONNX"] = "1"

result = subprocess.run(
    ["uv", "tool", "run", "--from", "mcp-memory-service", "memory", "server"],
    env=env,
)
sys.exit(result.returncode)
