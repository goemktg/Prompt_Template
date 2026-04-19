# lifecycle-save-resume-event-matrix

## 목적

이 문서는 현재 저장소에서 실제로 상태를 저장하는 lifecycle 이벤트와 resume 힌트를 한 표로 묶는다. 기준은 `copilot/hooks/scripts/*.py`, `scripts/write_lifecycle_transition.py`, `copilot/scripts/workspace_sync_server.py`, `scripts/refresh_mcp_runtime.py`다.

## 이벤트 매트릭스

| 이벤트 또는 명령 | writer | 저장 위치 | 핵심 필드 | resume 해석 |
| --- | --- | --- | --- | --- |
| session 시작 | `copilot/hooks/scripts/session_init.py` | `lifecycle_state` | 기존 `AWAIT`면 `hydrated_from_previous_session=true`, 아니면 `current_phase=INIT`, `status=active` | 이전 상태가 `AWAIT` 또는 `awaiting`이면 자동 hydrate, 아니면 새 `INIT` 시작 |
| compact 직전 | `copilot/hooks/pre-compact.py` | `lifecycle_state` | `continuity.last_event=preCompact`, `compact_safe=true`, `last_compaction_checkpoint=true` | compaction 이전 checkpoint 의미만 가진다. phase는 유지된다. |
| PLAN 기록 | `scripts/write_lifecycle_transition.py --phase PLAN` | `lifecycle_state` | `current_phase=PLAN`, `status`, `active_task`, `current_plan_hash` | 현재 plan 식별자와 작업명이 남는다. TODO hydrate는 pending scope다. |
| AWAIT 기록 | `scripts/write_lifecycle_transition.py --phase AWAIT` | `lifecycle_state` | `approval_pending`, `await_context`, `continuity.next_transition` | 현재 구현에서 가장 명시적인 resume 힌트다. 다음 전환 후보를 파일에 남긴다. |
| FINALIZE 기록 | `scripts/write_lifecycle_transition.py --phase FINALIZE` | `lifecycle_state` | `status=idle`, `active_task=null`, `continuity.last_terminal_status` | terminal 상태 정규화. 이후 resume보다 새 `INIT` 시작이 기본이다. |
| session 종료 | `copilot/hooks/scripts/session_end.py` | `lifecycle_state` | `current_phase=FINALIZE`, `status=idle`, `continuity.last_event=sessionEnd` | 세션 종료 흔적만 남긴다. 자동 session hydrate는 없다. |
| workspace sync 실행 | `copilot/scripts/workspace_sync_server.py` | `runtime_state` | `last_sync`, `exit_code`, `success`, `target_workspace`, `upgrade_script` | runtime surface 최신성 판단 근거다. lifecycle phase resume를 직접 수행하지는 않는다. |
| stale runtime refresh | `scripts/refresh_mcp_runtime.py` | `runtime_state` | `last_runtime_refresh`, `matched_count`, `terminated_count`, `failed` | stale process 정리 결과를 남긴다. lifecycle_state를 되살리지는 않는다. |

## 현재 minimum resume 규칙

1. `lifecycle_state`는 현재 phase와 continuity 힌트를 남긴다.
2. `runtime_state`는 sync와 refresh 결과를 남긴다.
3. 자동 hydrate는 `sessionStart`에서 `AWAIT` 또는 `awaiting` 상태에만 적용된다.
4. `AWAIT`는 `await_context`와 `continuity.next_transition`이 있으면 guided resume 후보로 해석한다.
5. `PLAN`, `EXECUTE`, `REPORT` 등 비대기 상태는 session restart 시 자동 복원하지 않고 새 `INIT`로 다시 시작한다.
6. `FINALIZE` 또는 `sessionEnd` 이후에는 기본값을 resume보다 새 `INIT` 시작으로 본다.

## restart/hydrate 프로토콜

| 이전 종료 상태 | 다음 `sessionStart` 동작 |
| --- | --- |
| `AWAIT` 또는 `awaiting` | 기존 phase, `await_context`, `current_plan_hash`, continuity를 유지한 채 hydrate |
| 그 외 lifecycle 상태 | `INIT` / `active`로 초기화 |
| 손상된 state 파일 | migration 후 기본 shape로 복구하고 새 `INIT` 시작 |

## 현재 한계

- 자동 hydrate는 `sessionStart` hook 경로에서만 증명됐다.
- 실제 orchestrator execution path가 항상 `write_lifecycle_transition.py`를 호출하는지에 대한 live integration 증거는 아직 없다.
- delegated step prompt reference와 todo snapshot 복원은 아직 pending scope다.

## 운영 체크

| 상황 | 먼저 볼 필드 |
| --- | --- |
| approval 대기 재개 | `lifecycle_state.await_context`, `lifecycle_state.approval_pending` |
| plan continuity 확인 | `lifecycle_state.current_plan_hash`, `lifecycle_state.active_task` |
| runtime 최신성 확인 | `runtime_state.last_sync`, `runtime_state.last_runtime_refresh` |
| compact 직전 상태 확인 | `lifecycle_state.continuity.compact_safe`, `last_compaction_checkpoint` |

## pending scope

- 실제 orchestrator execution path와 writer 연동 증명
- delegated step prompt reference 복원
- todo snapshot 저장
- restart vs guided resume 자동 판정
