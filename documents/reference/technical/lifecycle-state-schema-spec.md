# lifecycle-state-schema-spec

## 목적

이 문서는 현재 `.copilot-memory/upgrade_state.json`의 `schema_version: 2`를 구현 기준으로 간단히 고정하는 명세다. 기준 구현은 `copilot/scripts/upgrade_state.py`의 `UpgradeStateStore`이며, deep validation이 아니라 현재 writer들이 실제로 의존하는 최소 shape를 설명한다.

## 스키마 보장 범위

현재 구현이 기계적으로 보장하는 것은 아래 세 가지뿐이다.

| 필드 | 보장 내용 | 근거 |
| --- | --- | --- |
| `schema_version` | 항상 `2`로 정규화된다. | `UpgradeStateStore._migrate()` |
| `lifecycle_state` | 항상 객체로 존재하고, 정해진 key 집합으로 정규화된다. | `UpgradeStateStore._normalize_lifecycle_state()` |
| `runtime_state` | 항상 객체로 존재하고, 정해진 key 집합으로 정규화된다. | `UpgradeStateStore._normalize_runtime_state()` |

즉, 현재 구현은 top-level 전체 JSON을 엄격하게 검증하지 않는다. writer가 넣은 payload 내부 shape는 대부분 그대로 저장되며, 필수 container와 핵심 key만 정규화한다.

## Machine-Enforced 필드

아래 필드는 `load()` 또는 각 update 메서드를 거치면 shape가 강제된다.

### 1. Top-level 필수 필드

| 필드 | 타입 | 비고 |
| --- | --- | --- |
| `schema_version` | number | 현재 값은 `2` |
| `lifecycle_state` | object | 하위 key가 정규화된다. |
| `runtime_state` | object | 하위 key가 정규화된다. |

### 2. `lifecycle_state`

| 필드 | 타입 | 기본값 | enforcement 수준 |
| --- | --- | --- | --- |
| `active_task` | string or `null` | `null` | key 존재 보장 |
| `approval_pending` | boolean | `false` | `bool(...)`로 정규화 |
| `await_context` | object or `null` | `null` | dict가 아니면 `null` |
| `continuity` | object | `{}` | dict가 아니면 빈 객체 |
| `current_phase` | string or `null` | `null` | 값 자체의 phase 유효성 검증은 writer 책임 |
| `current_plan_hash` | string or `null` | `null` | key 존재 보장 |
| `status` | string | `idle` | 값 자체의 status 유효성 검증은 writer 책임 |
| `updated_at` | number or `null` | `last_success_ts` 또는 `null` | 숫자면 float로 정규화 |

주의할 점은 `current_phase`와 `status`의 허용값 검증이 `UpgradeStateStore` 내부가 아니라 writer 쪽에 있다는 것이다. 예를 들어 `scripts/write_lifecycle_transition.py`는 CLI parser에서 phase/status를 검증하지만, store 자체는 임의 문자열을 막지 않는다.

### 3. `runtime_state`

| 필드 | 타입 | 기본값 | enforcement 수준 |
| --- | --- | --- | --- |
| `last_runtime_refresh` | object or `null` | `null` | dict면 저장, 아니면 `null` |
| `last_runtime_cleanup` | object or `null` | `null` | dict면 저장, 아니면 `null` |
| `last_sync` | object or `null` | `null` | dict면 저장, 아니면 `null` |
| `sync_check` | object or `null` | `null` | dict면 저장, 아니면 `null` |
| `updated_at` | number or `null` | payload timestamp 추론값 또는 `null` | 숫자면 float로 정규화 |

`runtime_state.updated_at`은 `last_runtime_cleanup`, `last_sync`, `last_runtime_refresh`, `sync_check`에서 timestamp 계열 key를 추론해 채운다. payload 내부 필드 이름 전체를 검증하지는 않는다.

## Human-Readable 또는 Debug 성격 필드

아래 필드는 현재 구현에서 호환성 미러, 운영 로그, 또는 사람이 빠르게 읽기 위한 성격이 강하다. 새 자동화는 가능하면 이 필드들보다 `lifecycle_state`와 `runtime_state`를 우선 참조하는 편이 안전하다.

| 필드 | 성격 | 이유 |
| --- | --- | --- |
| `last_sync` | top-level mirror | authoritative 값은 `runtime_state.last_sync` |
| `last_runtime_refresh` | top-level mirror | authoritative 값은 `runtime_state.last_runtime_refresh` |
| `last_runtime_cleanup` | top-level mirror | authoritative 값은 `runtime_state.last_runtime_cleanup` |
| `sync_check` | top-level mirror | authoritative 값은 `runtime_state.sync_check` |
| `last_exit_code` | debug/ops summary | lifecycle phase를 직접 구동하지 않음 |
| `last_success_ts` | debug/ops summary | recovery 기본 timestamp로만 재사용 |
| `supplementary_deploy` | install/runtime 운영 정보 | lifecycle resume 판단의 핵심 입력은 아님 |

또한 `continuity`와 각 runtime payload 내부 세부 key는 현재 writer들이 쓰는 관례는 있지만 공통 schema validator로 강제되지는 않는다. 예를 들어 `continuity.next_transition`, `continuity.resume_token`, `last_sync.wrapper`는 현재 구현상 유용한 힌트이지만, strict schema registry로 관리되지는 않는다.

## 현재 writer 표면

| writer | 기록 위치 | 현재 역할 |
| --- | --- | --- |
| `copilot/scripts/upgrade_state.py` | 전체 파일 | load, migrate, atomic save의 단일 저장 표면 |
| `scripts/write_lifecycle_transition.py` | `lifecycle_state` | `PLAN`, `AWAIT`, `FINALIZE` 등 explicit transition 기록 |
| `copilot/hooks/scripts/session_init.py` | `lifecycle_state` | session start 시 `INIT`, `active_task`, `continuity.last_event` 기록 |
| `copilot/hooks/pre-compact.py` | `lifecycle_state` | `compact_safe`, `last_compaction_checkpoint` 기록 |
| `copilot/hooks/scripts/session_end.py` | `lifecycle_state` | session end 시 `FINALIZE`, `idle` 기록 |
| `copilot/scripts/workspace_sync_server.py` | `runtime_state.last_sync` | sync 결과와 top-level `last_sync` mirror 기록 |
| `scripts/refresh_mcp_runtime.py` | `runtime_state.last_runtime_refresh` | stale runtime process refresh 결과 기록 |
| `scripts/cleanup_runtime_artifacts.py` | `runtime_state.last_runtime_cleanup` | managed backup/marker cleanup 결과 기록 |
| `scripts/upgrade_ai.py` | `supplementary_deploy`, `last_exit_code`, `last_success_ts` | install/update 결과 요약 기록 |

## 검증 근거

현재 명세와 직접 연결되는 테스트는 아래 파일에 모여 있다.

| 테스트 | 확인 내용 |
| --- | --- |
| `tests/test_lifecycle_runtime_contract.py::test_upgrade_state_load_initializes_schema_sections` | 기본 `schema_version: 2`, `lifecycle_state`, `runtime_state` shape 초기화 |
| `tests/test_lifecycle_runtime_contract.py::test_upgrade_state_migrates_top_level_runtime_fields` | top-level runtime mirror를 `runtime_state`로 마이그레이션 |
| `tests/test_lifecycle_runtime_contract.py::test_upgrade_state_recovers_from_corrupted_state_fixtures` | 손상된 JSON에서 기본 shape 복구 |
| `tests/test_lifecycle_runtime_contract.py::test_runtime_refresh_write_shape_updates_runtime_state_and_top_level` | refresh payload와 top-level mirror 동기화 |
| `tests/test_lifecycle_runtime_contract.py::test_runtime_cleanup_write_shape_updates_runtime_state_and_top_level` | cleanup payload와 top-level mirror 동기화 |
| `tests/test_lifecycle_runtime_contract.py::test_record_sync_result_writes_wrapper_sync_shape` | sync 결과 wrapper payload 저장 |
| `tests/test_lifecycle_runtime_contract.py::test_session_hooks_update_lifecycle_state_for_workspace_payload` | hook 기반 `INIT`, `preCompact`, `FINALIZE` 상태 기록 |
| `tests/test_lifecycle_runtime_contract.py::test_write_lifecycle_transition_writes_plan_state` | `PLAN` 상태 저장 |
| `tests/test_lifecycle_runtime_contract.py::test_write_lifecycle_transition_writes_await_state` | `AWAIT`와 `await_context`, `next_transition` 저장 |
| `tests/test_lifecycle_runtime_contract.py::test_write_lifecycle_transition_await_preserves_resume_adjacent_fields` | `AWAIT` 진입 시 plan-hash와 continuity 일부 보존 |
| `tests/test_lifecycle_runtime_contract.py::test_write_lifecycle_transition_finalize_clears_active_task` | `FINALIZE`에서 terminal 정규화 |

## 구현상 유의점

1. atomic write는 `upgrade_state.json.tmp`에 먼저 쓴 뒤 replace하는 방식이다.
2. corruption recovery는 손상된 세부 필드를 복원하는 것이 아니라 최소 shape로 재정규화하는 수준이다.
3. 자동 resume/hydrate는 아직 없다. 파일은 continuity 힌트를 남기지만, 재개 판단은 현재 사람 또는 상위 orchestration이 수행한다.

## See Also

- [lifecycle-state-schema-guide](./lifecycle-state-schema-guide.md)
- [lifecycle-save-resume-event-matrix](./lifecycle-save-resume-event-matrix.md)
- [lifecycle-corruption-recovery-checklist](./lifecycle-corruption-recovery-checklist.md)
