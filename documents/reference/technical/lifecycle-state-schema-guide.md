# lifecycle-state-schema-guide

## 목적

이 문서는 현재 `.copilot-memory/upgrade_state.json`의 `schema_version: 2` 구조를 운영 관점에서 빠르게 확인하기 위한 참조다. 상세 구현은 `copilot/scripts/upgrade_state.py`가 단일 저장 표면으로 관리한다.

## 파일 개요

현재 상태 파일은 아래 성격의 데이터를 함께 저장한다.

| 구역 | 용도 |
| --- | --- |
| top-level 메타 | 마지막 실행 결과와 호환성 유지용 미러 필드 |
| `lifecycle_state` | 현재 lifecycle phase, 대기 상태, 연속성 정보 |
| `runtime_state` | sync, refresh, self-check 계열 runtime 결과 |
| `supplementary_deploy` | `upgrade_ai.py`가 관리하는 supplementary deploy 결과 |

대표 top-level 필드는 다음과 같다.

| 필드 | 의미 |
| --- | --- |
| `schema_version` | 현재 스키마 버전. 값은 `2` |
| `last_exit_code` | 마지막 관련 실행 종료 코드 |
| `last_success_ts` | 마지막 성공 시각 |
| `last_sync` | `runtime_state.last_sync`의 호환성 미러 |
| `last_runtime_refresh` | `runtime_state.last_runtime_refresh`의 호환성 미러 |
| `sync_check` | `runtime_state.sync_check`의 호환성 미러 |

## `lifecycle_state`

`lifecycle_state`는 session continuity와 explicit phase persistence를 담당한다.

| 필드 | 의미 |
| --- | --- |
| `active_task` | 현재 작업 설명. `FINALIZE`에서는 `null` 가능 |
| `approval_pending` | `AWAIT`에서 승인 대기 여부 |
| `await_context` | `AWAIT` 진입 이유와 다음 전환 힌트 |
| `continuity` | resume에 필요한 부가 상태 묶음 |
| `current_phase` | `INIT`, `PLAN`, `AWAIT`, `FINALIZE` 등 현재 phase |
| `current_plan_hash` | 현재 plan 식별자 |
| `status` | `idle`, `active`, `awaiting`, `completed`, `failed` 중 하나 |
| `updated_at` | 마지막 lifecycle write 시각 |

`continuity`에는 현재 구현 기준으로 다음 값들이 자주 들어간다.

| 키 | 주 기록자 | 의미 |
| --- | --- | --- |
| `workspace_root` | hook 공통 로직, transition writer | 대상 workspace root |
| `last_event` | hook scripts | `sessionStart`, `preCompact`, `sessionEnd` 등 마지막 lifecycle 이벤트 |
| `last_session_start` | `session_init.py` | 세션 시작 마커 |
| `last_session_end` | `session_end.py` | 세션 종료 마커 |
| `compact_safe` | `pre-compact.py`, `session_end.py` | compaction 이후 안전 상태 여부 |
| `last_compaction_checkpoint` | `pre-compact.py` | pre-compact checkpoint 기록 |
| `next_transition` | `write_lifecycle_transition.py` | 다음 허용 transition 힌트 |
| `last_terminal_status` | `write_lifecycle_transition.py` | `FINALIZE` 직전 terminal status |

## `runtime_state`

`runtime_state`는 runtime refresh와 workspace sync 결과를 모은다.

| 필드 | 의미 |
| --- | --- |
| `last_runtime_refresh` | stale local MCP/runtime process refresh 결과 |
| `last_sync` | `workspace_sync_server.py`가 기록한 sync 결과 |
| `sync_check` | 별도 self-check 또는 sync health 결과 저장 위치 |
| `updated_at` | runtime 관련 마지막 갱신 시각 |

현재 구현에서 자주 보이는 payload shape는 다음과 같다.

| 구역 | 핵심 필드 |
| --- | --- |
| `last_runtime_refresh` | `timestamp`, `plugin_root`, `dry_run`, `matched_count`, `terminated_count`, `terminated_pids`, `failed`, `target_scripts` |
| `last_sync` | `timestamp`, `target_workspace`, `exit_code`, `success`, `timeout`, `repo_root`, `upgrade_script`, `wrapper` |
| `sync_check` | caller-defined payload. `UpgradeStateStore.update_sync_check()`가 저장 |

## 현재 writer 표면

| writer | 기록 내용 |
| --- | --- |
| `scripts/upgrade_ai.py` | `supplementary_deploy`, `last_exit_code`, `last_success_ts` |
| `scripts/refresh_mcp_runtime.py` | `runtime_state.last_runtime_refresh`와 top-level 미러 |
| `copilot/scripts/workspace_sync_server.py` | `runtime_state.last_sync`와 top-level `last_sync` |
| `scripts/write_lifecycle_transition.py` | explicit `lifecycle_state` 전환, `await_context`, `continuity.next_transition` |
| `copilot/hooks/scripts/session_init.py` | `INIT`, `active`, session start continuity |
| `copilot/hooks/pre-compact.py` | compaction-safe continuity marker |
| `copilot/hooks/scripts/session_end.py` | `FINALIZE`, `idle`, session end continuity |

참고로 hook script와 CLI writer는 모두 `UpgradeStateStore`를 통해 저장하며, 저장 시 temp file write 후 replace 방식으로 원자적 갱신을 수행한다. 읽기 시 JSON 손상 또는 구버전 상태는 `schema_version: 2` 구조로 마이그레이션된다.

## 운영 메모

- lifecycle continuity의 authoritative file은 `.copilot-memory/upgrade_state.json`이다.
- runtime 결과를 빠르게 읽을 때는 top-level 미러를 볼 수 있지만, 신규 자동화는 `runtime_state`와 `lifecycle_state`를 기준으로 처리하는 편이 안전하다.
- `dry-run` 경로는 상태를 남기지 않는 경우가 있으므로, 실제 기록 확인이 필요하면 non-dry-run 실행 결과를 기준으로 본다.
