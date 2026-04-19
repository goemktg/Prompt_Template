#!/usr/bin/env python3
"""sessionEnd hook: persist a terminal lifecycle state without blocking the session."""

from __future__ import annotations

import sys
from pathlib import Path

from _lifecycle_hook_common import (
    load_payload,
    resolve_workspace_root_from_payload,
    update_lifecycle_state,
)

_REPO_ROOT = Path(__file__).resolve().parents[3]
_SCRIPTS_DIR = _REPO_ROOT / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from cleanup_runtime_artifacts import cleanup_runtime_artifacts  # noqa: E402


def main() -> int:
    try:
        payload = load_payload()
        update_lifecycle_state(
            payload,
            current_phase="FINALIZE",
            status="idle",
            active_task=None,
            continuity_updates={
                "last_event": "sessionEnd",
                "last_session_end": True,
                "compact_safe": True,
            },
        )
        workspace_root = resolve_workspace_root_from_payload(payload)
        if workspace_root is not None:
            cleanup_runtime_artifacts(
                workspace_root=workspace_root, dry_run=False, write_state=True
            )
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())