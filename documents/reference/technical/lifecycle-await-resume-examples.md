# lifecycle-await-resume-examples

## 목적

이 문서는 현재 구현과 현재 vocabulary 기준으로 `AWAIT` 및 resume를 어떻게 읽어야 하는지 concrete scenario로 설명한다. 핵심은 이미 구현된 저장 동작과 아직 자동화되지 않은 hydrate 동작을 분리해서 보는 것이다.

## 공통 전제

현재 저장소에서 자동으로 저장되는 것은 `upgrade_state.json`의 state snapshot이다. 자동으로 수행되지 않는 것은 snapshot을 읽고 다음 행동을 결정하는 resume automation이다.

| 구분 | 현재 상태 |
| --- | --- |
| explicit phase 저장 | 구현됨 |
| `await_context` 저장 | 구현됨 |
| `continuity.next_transition` 저장 | 구현됨 |
| hook 기반 session start / pre-compact / session end 기록 | 구현됨 |
| `AWAIT -> EXECUTE` 자동 재개 | 미구현 |
| todo hydrate, delegated prompt 복원 | 미구현 |
| restart vs guided resume 자동 판정 | 미구현 |

## 시나리오 1. 승인 대기 후 `EXECUTE`로 재개

### 시나리오 1 상황

사용자 승인이 필요한 작업에서 orchestrator가 `PLAN -> AWAIT`로 진입한다.

### 시나리오 1에서 실제로 기록되는 것

`scripts/write_lifecycle_transition.py`는 아래와 같은 정보를 남긴다.

```json
{
  "lifecycle_state": {
    "current_phase": "AWAIT",
    "status": "awaiting",
    "active_task": "wait for approval",
    "approval_pending": true,
    "await_context": {
      "approval_pending": true,
      "next_transition": "EXECUTE",
      "reason": "Need explicit user approval before EXECUTE"
    },
    "continuity": {
      "next_transition": "EXECUTE",
      "workspace_root": "..."
    }
  }
}
```

이 shape는 `tests/test_lifecycle_runtime_contract.py::test_write_lifecycle_transition_writes_await_state`에서 검증된다.

### 시나리오 1에서 이미 구현된 부분

- `AWAIT` phase와 `await_context.reason` 저장
- `approval_pending=true` 저장
- 다음 후보 전환인 `continuity.next_transition=EXECUTE` 저장

### 시나리오 1에서 아직 자동화되지 않은 부분

- 승인 응답을 받아 자동으로 `EXECUTE`를 호출하는 동작
- `await_context.reason`를 읽어 사용자에게 자동 프롬프트를 재구성하는 동작

### 시나리오 1의 현재 수동 resume 해석

1. `lifecycle_state.current_phase == AWAIT`인지 확인한다.
2. `approval_pending == true`인지 확인한다.
3. `await_context.next_transition == EXECUTE`면 승인 후 다음 목표를 `EXECUTE`로 본다.
4. 실제 전환은 사람이 `write_lifecycle_transition.py` 또는 상위 orchestration으로 다시 기록해야 한다.

## 시나리오 2. plan hash를 유지한 채 `AWAIT`로 멈췄다가 재개

### 시나리오 2 상황

이미 `PLAN`이 기록된 상태에서, 같은 작업이 승인 대기 때문에 잠시 멈춘다. 이때 plan continuity를 잃지 않는 것이 중요하다.

### 시나리오 2에서 실제로 기록되는 것

현재 테스트는 먼저 `PLAN` 상태를 기록한 뒤, continuity에 `resume_token`을 넣고, 다시 `AWAIT`로 전환한다. 결과적으로 아래 성격의 값이 유지된다.

| 필드 | 기대값 |
| --- | --- |
| `current_phase` | `AWAIT` |
| `status` | `awaiting` |
| `active_task` | 기존 작업명 유지 |
| `current_plan_hash` | 기존 plan hash 유지 |
| `continuity.resume_token` | 기존 값 유지 |
| `continuity.next_transition` | 새 값으로 추가 |

이 동작은 `tests/test_lifecycle_runtime_contract.py::test_write_lifecycle_transition_await_preserves_resume_adjacent_fields`가 검증한다.

### 시나리오 2에서 이미 구현된 부분

- `AWAIT` 전환 시 기존 `active_task`와 `current_plan_hash` 유지
- continuity 내부의 기존 key 일부 보존
- `next_transition`만 추가 또는 갱신

### 시나리오 2에서 아직 자동화되지 않은 부분

- `current_plan_hash`를 사용해 TODO 목록이나 delegated step prompt를 자동 hydrate
- `resume_token`을 이용해 Memory MCP handoff를 자동 조회

### 시나리오 2의 현재 수동 resume 해석

이 경우 resume의 최소 입력은 `active_task`, `current_plan_hash`, `continuity.resume_token`, `continuity.next_transition`이다. 즉, 현재 파일은 “어떤 계획을 재개해야 하는가”까지는 힌트를 남기지만, “그 계획의 다음 step artifact를 어떻게 복원할 것인가”는 아직 자동화하지 않는다.

## 시나리오 3. `AWAIT` 또는 active state에서 compaction 직전 checkpoint를 남기는 경우

### 시나리오 3 상황

세션이 compact되기 직전, 현재 상태를 완전히 종료하지 않고 checkpoint만 남기고 싶다.

### 시나리오 3에서 실제로 기록되는 것

`copilot/hooks/pre-compact.py`는 `_lifecycle_hook_common.update_lifecycle_state()`를 통해 현재 phase와 status를 유지하면서 continuity에 다음 힌트를 추가한다.

| continuity key | 의미 |
| --- | --- |
| `last_event=preCompact` | 마지막 lifecycle 이벤트 |
| `compact_safe=true` | compact-safe 상태 표시 |
| `last_compaction_checkpoint=true` | compaction 직전 checkpoint 존재 |

이 동작은 `tests/test_lifecycle_runtime_contract.py::test_session_hooks_update_lifecycle_state_for_workspace_payload`에서 검증된다.

### 시나리오 3에서 이미 구현된 부분

- compact 이전 checkpoint 흔적 저장
- 기존 lifecycle 상태를 유지한 채 continuity만 확장

### 시나리오 3에서 아직 자동화되지 않은 부분

- 다음 세션 시작 시 `compact_safe`를 보고 자동으로 guided resume를 제안하는 동작
- compaction 전후 memory handoff와 file state를 교차 검증하는 동작

### 시나리오 3의 현재 수동 resume 해석

`current_phase`가 그대로 남아 있고 `compact_safe=true`라면, 최소한 “state file은 compaction 전에 끊기지 않고 저장되었다”는 힌트로 볼 수 있다. 다만 이것만으로 자동 resume를 수행하지는 않으며, 여전히 사람이 `active_task`, `await_context`, `runtime_state`를 함께 확인해야 한다.

## 시나리오 4. runtime refresh 또는 cleanup 이후 resume 가능 여부를 판단하는 경우

### 시나리오 4 상황

`AWAIT` 상태는 남아 있지만, 그 사이에 stale process refresh나 runtime artifact cleanup이 수행되었다. 이때 단순히 `lifecycle_state`만 보면 충분하지 않다.

### 시나리오 4에서 실제로 기록되는 것

| writer | 남기는 필드 | 테스트 근거 |
| --- | --- | --- |
| `scripts/refresh_mcp_runtime.py` | `runtime_state.last_runtime_refresh` | `test_runtime_refresh_write_shape_updates_runtime_state_and_top_level` |
| `scripts/cleanup_runtime_artifacts.py` | `runtime_state.last_runtime_cleanup` | `test_runtime_cleanup_write_shape_updates_runtime_state_and_top_level` |
| `copilot/scripts/workspace_sync_server.py` | `runtime_state.last_sync` | `test_record_sync_result_writes_wrapper_sync_shape` |

### 시나리오 4에서 이미 구현된 부분

- refresh, cleanup, sync 결과를 `runtime_state`에 누적 기록
- top-level mirror도 함께 갱신

### 시나리오 4에서 아직 자동화되지 않은 부분

- runtime refresh 실패나 cleanup 실패를 근거로 resume를 자동 차단하는 정책
- `last_sync.success`와 `last_runtime_refresh.failed`를 종합해 다음 phase를 자동 선택하는 정책

### 시나리오 4의 현재 수동 resume 해석

1. `lifecycle_state`로 본래의 phase와 task를 확인한다.
2. `runtime_state.last_sync`로 현재 workspace copy가 최신인지 본다.
3. `runtime_state.last_runtime_refresh`와 `last_runtime_cleanup`에서 실패가 있었는지 확인한다.
4. runtime이 불안정하면 `EXECUTE`보다 `PLAN` 또는 새 `INIT`를 택하는 것이 안전하다.

## 요약 규칙

1. 현재 구현은 `AWAIT`를 파일에 명시적으로 남긴다.
2. 현재 구현은 resume 힌트도 일부 남긴다. 대표 예시는 `await_context`와 `continuity.next_transition`이다.
3. 현재 구현은 runtime 최신성 정보도 별도 구역에 남긴다.
4. 그러나 “어떻게 재개할지 결정하는 자동화”는 아직 없다.
5. 따라서 현재의 resume는 automated resume가 아니라 guided manual resume에 가깝다.

## See Also

- [lifecycle-save-resume-event-matrix](./lifecycle-save-resume-event-matrix.md)
- [lifecycle-state-schema-spec](./lifecycle-state-schema-spec.md)
- [lifecycle-validation-guide](./lifecycle-validation-guide.md)
