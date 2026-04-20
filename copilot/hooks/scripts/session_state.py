#!/usr/bin/env python3
"""Shared session-state resolution helpers for hooks and session-gate."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Mapping


def resolve_session_state_dir(environ: Mapping[str, str] | None = None) -> Path:
    """Resolve the active session-state directory with shared precedence.

    Priority order:
      1. SESSION_GATE_STATE_DIR env var (explicit override)
      2. COPILOT_SESSION_DIR env var
      3. ~/.copilot/session-state/<COPILOT_SESSION_ID> when session ID is set
      4. ~/.copilot/session-state (default shared directory)
    """
    env = environ or os.environ
    if env.get("SESSION_GATE_STATE_DIR"):
        return Path(str(env["SESSION_GATE_STATE_DIR"])).expanduser()
    if env.get("COPILOT_SESSION_DIR"):
        return Path(str(env["COPILOT_SESSION_DIR"])).expanduser()
    if env.get("COPILOT_SESSION_ID"):
        return (
            Path.home() / ".copilot" / "session-state" / str(env["COPILOT_SESSION_ID"])
        ).expanduser()
    return (Path.home() / ".copilot" / "session-state").expanduser()


def derive_session_id(
    state_dir: Path | None = None, environ: Mapping[str, str] | None = None
) -> str | None:
    """Derive a session id from env, or from .../session-state/<id> directory shape.

    Returns None when no session id can be derived (single shared directory mode).
    """
    env = environ or os.environ
    env_session_id = env.get("COPILOT_SESSION_ID")
    if env_session_id:
        return str(env_session_id)

    resolved_dir = (state_dir or resolve_session_state_dir(env)).expanduser()
    parent = resolved_dir.parent
    if parent.name != "session-state":
        return None

    candidate = resolved_dir.name.strip()
    return candidate or None
