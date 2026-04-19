#!/usr/bin/env python3
# Archived: this repository now relies on native Gemini access instead of a local Gemini MCP backend.
"""Archived Gemini MCP server implementation.

This is a minimal local port of the reference Gemini bridge. It keeps the
interface small and reviewable while remaining usable as a leaf proxy for the
mediator stack.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from typing import Any

from mcp.server.fastmcp import FastMCP

MAX_PROMPT_SIZE = 100_000
DEFAULT_TIMEOUT = int(os.environ.get("GEMINI_TIMEOUT_SECONDS", "120"))
DEFAULT_MODEL = os.environ.get("GEMINI_DEFAULT_MODEL", "").strip() or "gemini-2.5-pro"
KNOWN_MODELS = [
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-3.1-pro-preview",
]


def resolve_gemini_bin() -> str:
    env_bin = os.environ.get("GEMINI_BIN", "").strip()
    if env_bin:
        return env_bin
    for candidate in ("gemini", "gemini.cmd", "gemini.exe"):
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    return "gemini"


GEMINI_BIN = resolve_gemini_bin()


def strip_markdown_fences(text: str) -> str:
    if not text:
        return text
    normalized = text.replace("\r\n", "\n").strip()
    match = re.match(r"^```[\w+.-]*\n(.*?)```$", normalized, re.DOTALL)
    return match.group(1).strip() if match else text


def build_error(message: str) -> dict[str, Any]:
    return {
        "success": False,
        "response": None,
        "data": None,
        "parsed": False,
        "model": None,
        "tokens": None,
        "latency_ms": None,
        "error": message,
    }


def extract_stats(envelope: dict[str, Any]) -> tuple[str | None, dict[str, Any] | None, int | None]:
    stats = envelope.get("stats")
    if not isinstance(stats, dict):
        return None, None, None

    models = stats.get("models")
    if not isinstance(models, dict) or not models:
        return None, None, None

    model_name: str | None = None
    model_stats: dict[str, Any] | None = None
    for candidate_name, candidate_stats in models.items():
        if not isinstance(candidate_stats, dict):
            continue
        roles = candidate_stats.get("roles")
        if isinstance(roles, dict) and "main" in roles:
            model_name = candidate_name
            model_stats = candidate_stats
            break
    if model_name is None and len(models) == 1:
        model_name, model_stats = next(iter(models.items()))

    latency_ms = None
    if isinstance(model_stats, dict):
        api_stats = model_stats.get("api")
        if isinstance(api_stats, dict):
            raw_latency = api_stats.get("totalLatencyMs")
            if isinstance(raw_latency, int):
                latency_ms = raw_latency
    return model_name, model_stats, latency_ms


def run_gemini(
    prompt: str,
    model: str,
    json_mode: bool,
    sandbox: bool,
    timeout: int,
) -> dict[str, Any]:
    prompt_size = len(prompt.encode("utf-8"))
    if prompt_size > MAX_PROMPT_SIZE:
        return build_error(f"Prompt too large ({prompt_size} bytes, max {MAX_PROMPT_SIZE})")

    command = [
        GEMINI_BIN,
        "--output-format",
        "json",
        "--model",
        model,
        "--prompt",
        prompt,
    ]
    if sandbox:
        command.append("--sandbox")

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return build_error(f"Timeout after {timeout}s")
    except FileNotFoundError:
        return build_error(f"Gemini CLI not found: {GEMINI_BIN}")
    except OSError as exc:
        return build_error(f"Failed to execute Gemini CLI: {exc}")

    if result.returncode != 0:
        stderr = result.stderr.strip() if result.stderr else ""
        return build_error(f"Gemini CLI exited with code {result.returncode}: {stderr}")

    stdout = result.stdout.strip()
    if not stdout:
        return build_error("Gemini CLI returned empty output")

    try:
        envelope = json.loads(stdout)
    except json.JSONDecodeError as exc:
        return build_error(f"Failed to parse Gemini output: {exc}")

    response_text = strip_markdown_fences(str(envelope.get("response", "")))
    model_name, model_stats, latency_ms = extract_stats(envelope)
    tokens = None
    if isinstance(model_stats, dict):
        raw_tokens = model_stats.get("tokens")
        if isinstance(raw_tokens, dict):
            tokens = {
                "input": raw_tokens.get("input"),
                "output": raw_tokens.get("candidates"),
            }

    payload: dict[str, Any] = {
        "success": True,
        "response": response_text,
        "data": None,
        "parsed": False,
        "model": model_name or model,
        "tokens": tokens,
        "latency_ms": latency_ms,
        "warnings": result.stderr.strip() or None,
        "error": None,
    }

    if json_mode:
        try:
            payload["data"] = json.loads(response_text)
            payload["parsed"] = True
        except (json.JSONDecodeError, TypeError):
            payload["parsed"] = False

    return payload


mcp = FastMCP(
    "gemini",
    instructions=(
        "Gemini MCP server for mediator leaf calls. "
        "Use gemini_prompt to execute a prepared prompt and gemini_models to inspect known model ids."
    ),
)


@mcp.tool()
def gemini_prompt(
    prompt: str,
    model: str = "",
    json_mode: bool = False,
    sandbox: bool = False,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    effective_model = model.strip() if model.strip() else DEFAULT_MODEL
    return run_gemini(
        prompt=prompt,
        model=effective_model,
        json_mode=json_mode,
        sandbox=sandbox,
        timeout=timeout,
    )


@mcp.tool()
def gemini_models() -> dict[str, Any]:
    gemini_available = bool(shutil.which(GEMINI_BIN))
    if not gemini_available and os.path.isabs(GEMINI_BIN):
        gemini_available = os.path.exists(GEMINI_BIN)
    return {
        "models": list(KNOWN_MODELS),
        "default_model": DEFAULT_MODEL,
        "gemini_bin": GEMINI_BIN,
        "available": gemini_available,
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")