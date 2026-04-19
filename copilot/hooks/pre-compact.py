#!/usr/bin/env python3
"""preCompact hook: persist a compact-safe continuity marker."""

from __future__ import annotations

import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from _lifecycle_hook_common import UNCHANGED, load_payload, update_lifecycle_state  # noqa: E402


def main() -> int:
    try:
        payload = load_payload()
        update_lifecycle_state(
            payload,
            current_phase=UNCHANGED,
            status=UNCHANGED,
            active_task=UNCHANGED,
            continuity_updates={
                "last_event": "preCompact",
                "last_compaction_checkpoint": True,
                "compact_safe": True,
            },
        )
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())