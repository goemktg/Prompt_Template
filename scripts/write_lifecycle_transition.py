#!/usr/bin/env python3
"""Write explicit lifecycle transitions into upgrade_state.json for a workspace."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from copilot.scripts.upgrade_state import UpgradeStateStore


VALID_PHASES = (
    "INIT",
    "ATOMIZE",
    "PLAN",
    "EXECUTE",
    "REPORT",
    "AWAIT",
    "FINALIZE",
)
VALID_STATUSES = (
    "idle",
    "active",
    "awaiting",
    "completed",
    "failed",
)


def _phase_value(raw_value: str) -> str:
    value = raw_value.strip().upper()
    if value not in VALID_PHASES:
        allowed = ", ".join(VALID_PHASES)
        raise argparse.ArgumentTypeError(f"invalid phase '{raw_value}'. Expected one of: {allowed}")
    return value


def _status_value(raw_value: str) -> str:
    value = raw_value.strip().lower()
    if value not in VALID_STATUSES:
        allowed = ", ".join(VALID_STATUSES)
        raise argparse.ArgumentTypeError(f"invalid status '{raw_value}'. Expected one of: {allowed}")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Persist an explicit lifecycle transition for a target workspace.",
    )
    parser.add_argument("--workspace", required=True, help="Target workspace root path.")
    parser.add_argument("--phase", required=True, type=_phase_value, help="Lifecycle phase to write.")
    parser.add_argument("--status", required=True, type=_status_value, help="Lifecycle status to write.")
    parser.add_argument("--active-task", help="Active task text for the lifecycle state.")
    parser.add_argument(
        "--approval-pending",
        action="store_true",
        help="Mark the written state as awaiting approval.",
    )
    parser.add_argument("--plan-hash", help="Optional plan hash for continuity and resume.")
    parser.add_argument("--await-reason", help="Optional reason for entering the AWAIT phase.")
    parser.add_argument(
        "--next-transition",
        type=_phase_value,
        help="Optional next lifecycle transition hint.",
    )
    return parser


def _resolve_workspace_root(raw_path: str) -> Path:
    candidate = Path(raw_path).expanduser()
    return candidate.resolve(strict=False)


def _merged_continuity(
    current_continuity: Any,
    *,
    workspace_root: Path,
    next_transition: str | None,
    leaving_await: bool,
    phase: str,
    requested_status: str,
) -> dict[str, Any]:
    continuity = dict(current_continuity) if isinstance(current_continuity, dict) else {}
    continuity["workspace_root"] = str(workspace_root)

    if phase != "FINALIZE":
        continuity.pop("last_terminal_status", None)

    if leaving_await:
        continuity.pop("hydrated_from_previous_session", None)
        continuity.pop("next_transition", None)
        continuity.pop("resume_token", None)

    if next_transition is not None:
        continuity["next_transition"] = next_transition
    elif phase == "FINALIZE":
        continuity.pop("next_transition", None)

    if phase == "FINALIZE":
        continuity["last_terminal_status"] = requested_status

    return continuity


def _await_context(
    *,
    phase: str,
    approval_pending: bool,
    await_reason: str | None,
    next_transition: str | None,
) -> dict[str, Any] | None:
    if phase != "AWAIT":
        return None

    context: dict[str, Any] = {}
    if await_reason:
        context["reason"] = await_reason
    if approval_pending:
        context["approval_pending"] = True
    if next_transition is not None:
        context["next_transition"] = next_transition
    return context or {}


def write_lifecycle_transition(
    *,
    workspace_root: Path,
    phase: str,
    status: str,
    active_task: str | None = None,
    approval_pending: bool = False,
    plan_hash: str | None = None,
    await_reason: str | None = None,
    next_transition: str | None = None,
) -> dict[str, Any]:
    store = UpgradeStateStore(workspace_root)
    state = store.load()
    lifecycle_state = state.get("lifecycle_state")
    current_state = dict(lifecycle_state) if isinstance(lifecycle_state, dict) else {}
    leaving_await = (
        current_state.get("current_phase") == "AWAIT"
        or current_state.get("status") == "awaiting"
    ) and phase != "AWAIT"

    effective_status = "idle" if phase == "FINALIZE" and status == "completed" else status
    effective_active_task = None if phase == "FINALIZE" else current_state.get("active_task")
    if phase != "FINALIZE" and active_task is not None:
        effective_active_task = active_task
    effective_plan_hash = plan_hash if plan_hash is not None else current_state.get("current_plan_hash")
    if phase == "FINALIZE" and status == "completed":
        effective_plan_hash = None
    elif leaving_await and plan_hash is None:
        effective_plan_hash = None

    store.update_lifecycle_state(
        active_task=effective_active_task,
        approval_pending=approval_pending if phase == "AWAIT" else False,
        await_context=_await_context(
            phase=phase,
            approval_pending=approval_pending,
            await_reason=await_reason,
            next_transition=next_transition,
        ),
        continuity=_merged_continuity(
            current_state.get("continuity"),
            workspace_root=workspace_root,
            next_transition=next_transition,
            leaving_await=leaving_await,
            phase=phase,
            requested_status=status,
        ),
        current_phase=phase,
        current_plan_hash=effective_plan_hash,
        status=effective_status,
    )
    return store.load()


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    write_lifecycle_transition(
        workspace_root=_resolve_workspace_root(args.workspace),
        phase=args.phase,
        status=args.status,
        active_task=args.active_task,
        approval_pending=args.approval_pending,
        plan_hash=args.plan_hash,
        await_reason=args.await_reason,
        next_transition=args.next_transition,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())