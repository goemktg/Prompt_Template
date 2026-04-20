#!/usr/bin/env python3
"""preCompact hook: write a compact-safe checkpoint marker to the session state directory."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from session_state import resolve_session_state_dir  # noqa: E402


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    try:
        session_dir = resolve_session_state_dir()
        compact_marker = session_dir / "compact-checkpoint.json"
        os.makedirs(session_dir, exist_ok=True)
        marker = {
            "event": "preCompact",
            "ts": _now_iso(),
            "compact_safe": True,
        }
        with compact_marker.open("w", encoding="utf-8") as fh:
            json.dump(marker, fh, ensure_ascii=False)
            fh.write("\n")
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
