#!/usr/bin/env python3
"""Retired Gemini backend tombstone.

The live repository no longer owns an active Gemini MCP backend.
The archived implementation is preserved under:
archive/copilot/mcp-servers/gemini/
"""

from __future__ import annotations

import sys


def main() -> int:
    sys.stderr.write(
        "The repo-owned Gemini backend has been retired. "
        "Use the archived copy under archive/copilot/mcp-servers/gemini/ if historical reference is needed.\n"
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())