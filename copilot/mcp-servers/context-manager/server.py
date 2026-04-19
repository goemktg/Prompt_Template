#!/usr/bin/env python3
"""Minimal context-manager MCP server for storing and paging large intermediate results."""

from __future__ import annotations

import json
import os
import re
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

MAX_RESULT_SIZE_CHARS = 50_000
PREVIEW_SIZE_BYTES = 2_000
IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9._-]+$")
DEFAULT_BASE_DIR = ".copilot-runtime/context-manager"
RESULTS_DIRNAME = "tool-results"


def _base_dir() -> Path:
    configured = os.environ.get("CONTEXT_MANAGER_BASE_DIR", DEFAULT_BASE_DIR)
    expanded = Path(os.path.expanduser(configured))
    if not expanded.is_absolute():
        expanded = Path.cwd() / expanded
    expanded.mkdir(parents=True, exist_ok=True)
    return expanded


def _normalize_identifier(value: str, field_name: str) -> str:
    if not value or not IDENTIFIER_RE.fullmatch(value):
        raise ValueError(f"{field_name} must contain only letters, numbers, dot, underscore, or hyphen")
    return value


def _session_id(session_id: str | None) -> str:
    candidate = session_id or "default"
    return _normalize_identifier(candidate, "session_id")


def _session_results_dir(session_id: str | None) -> Path:
    target = _base_dir() / _session_id(session_id) / RESULTS_DIRNAME
    target.mkdir(parents=True, exist_ok=True)
    return target


def _result_paths(result_id: str, session_id: str | None) -> tuple[Path, Path]:
    normalized_id = _normalize_identifier(result_id, "result_id")
    results_dir = _session_results_dir(session_id)
    return results_dir / f"{normalized_id}.txt", results_dir / f"{normalized_id}.meta.json"


def _make_preview(content: str) -> str:
    raw = content.encode("utf-8")
    if len(raw) <= PREVIEW_SIZE_BYTES:
        return content
    preview = raw[:PREVIEW_SIZE_BYTES]
    last_newline = preview.rfind(b"\n")
    if last_newline > 0:
        preview = preview[: last_newline + 1]
    return preview.decode("utf-8", errors="ignore")


def _slice_lines(content: str, start_line: int | None, end_line: int | None) -> tuple[str, int, list[int]]:
    lines = content.splitlines()
    total_lines = len(lines)

    if start_line is None and end_line is None:
        return content, total_lines, [1, total_lines] if total_lines else [0, 0]

    start = 1 if start_line is None else start_line
    end = total_lines if end_line is None else end_line
    if start < 1:
        raise ValueError("start_line must be >= 1")
    if end < start:
        raise ValueError("end_line must be >= start_line")

    bounded_start = min(start, total_lines + 1)
    bounded_end = min(end, total_lines)
    if total_lines == 0 or bounded_start > bounded_end:
        return "", total_lines, [bounded_start, bounded_end]

    selected = "\n".join(lines[bounded_start - 1 : bounded_end])
    if content.endswith("\n") and bounded_end == total_lines:
        selected += "\n"
    return selected, total_lines, [bounded_start, bounded_end]


def _read_metadata(meta_path: Path) -> dict[str, Any]:
    if not meta_path.exists():
        return {}
    return json.loads(meta_path.read_text(encoding="utf-8"))


mcp = FastMCP(
    "context-manager",
    instructions=(
        "Store and page large tool outputs for mediator-style workflows. "
        "Use store_result for full payloads, then retrieve_result for ranged reads."
    ),
)


@mcp.tool()
def store_result(tool_name: str, content: str, session_id: str | None = None) -> dict[str, Any]:
    results_dir = _session_results_dir(session_id)
    result_id = uuid.uuid4().hex[:8]
    result_path = results_dir / f"{result_id}.txt"
    meta_path = results_dir / f"{result_id}.meta.json"

    result_path.write_text(content, encoding="utf-8")
    meta_path.write_text(
        json.dumps(
            {
                "tool_name": tool_name,
                "size_chars": len(content),
                "created_at": datetime.now(timezone.utc).isoformat(),
            },
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    return {
        "result_id": result_id,
        "path": str(result_path),
        "size_chars": len(content),
        "preview": _make_preview(content),
    }


@mcp.tool()
def retrieve_result(
    result_id: str,
    start_line: int | None = None,
    end_line: int | None = None,
    session_id: str | None = None,
) -> dict[str, Any]:
    result_path, _meta_path = _result_paths(result_id, session_id)
    if not result_path.exists():
        return {"error": f"Result not found: {result_id}"}

    content = result_path.read_text(encoding="utf-8")
    selected, total_lines, returned_range = _slice_lines(content, start_line, end_line)
    response: dict[str, Any] = {
        "result_id": _normalize_identifier(result_id, "result_id"),
        "content": selected,
        "total_lines": total_lines,
        "returned_lines_range": returned_range,
    }
    if start_line is None and end_line is None and len(selected) > MAX_RESULT_SIZE_CHARS:
        truncated = selected[:MAX_RESULT_SIZE_CHARS]
        last_newline = truncated.rfind("\n")
        if last_newline > MAX_RESULT_SIZE_CHARS * 0.8:
            truncated = truncated[:last_newline]
        response["content"] = truncated
        response["truncated"] = True
        response["warning"] = (
            f"Output truncated at {MAX_RESULT_SIZE_CHARS:,} characters. "
            "Use retrieve_result with start_line/end_line for range access."
        )
    return response


@mcp.tool()
def list_results(session_id: str | None = None) -> dict[str, Any]:
    results_dir = _session_results_dir(session_id)
    results = []
    total_size_chars = 0
    for meta_path in sorted(results_dir.glob("*.meta.json")):
        result_id = meta_path.name[: -len(".meta.json")]
        metadata = _read_metadata(meta_path)
        size_chars = int(metadata.get("size_chars", 0))
        total_size_chars += size_chars
        results.append(
            {
                "result_id": result_id,
                "tool_name": metadata.get("tool_name", "unknown"),
                "size_chars": size_chars,
                "created_at": metadata.get("created_at"),
            }
        )
    return {
        "results": results,
        "total_count": len(results),
        "total_size_chars": total_size_chars,
    }


@mcp.tool()
def session_stats(session_id: str | None = None) -> dict[str, Any]:
    results_dir = _session_results_dir(session_id)
    results = []
    tool_counter: Counter[str] = Counter()
    for meta_path in sorted(results_dir.glob("*.meta.json")):
        result_id = meta_path.name[: -len(".meta.json")]
        metadata = _read_metadata(meta_path)
        tool_name = str(metadata.get("tool_name", "unknown"))
        size_chars = int(metadata.get("size_chars", 0))
        tool_counter[tool_name] += 1
        results.append(
            {
                "result_id": result_id,
                "tool_name": tool_name,
                "size_chars": size_chars,
                "created_at": metadata.get("created_at"),
            }
        )
    largest_result = max(results, key=lambda item: item["size_chars"], default=None)
    total_size_chars = sum(item["size_chars"] for item in results)
    return {
        "total_results": len(results),
        "total_size_chars": total_size_chars,
        "largest_result": largest_result,
        "results_by_tool": dict(tool_counter),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")