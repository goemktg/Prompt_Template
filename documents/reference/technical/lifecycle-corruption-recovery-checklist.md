# lifecycle-corruption-recovery-checklist

## 목적

이 체크리스트는 `<target_workspace>/.copilot-memory/upgrade_state.json`이 손상되었거나 비정상 shape로 보일 때 현재 구현 기준으로 무엇을 확인하고 어떻게 복구할지 정리한다.

## 현재 자동 복구가 실제로 하는 일

`copilot/scripts/upgrade_state.py`의 `UpgradeStateStore.load()`는 아래 상황에서 상태를 `schema_version: 2` 기본 shape로 정규화한다.

- 파일이 없음
- JSON 파싱 실패
- top-level 객체가 아님
- 구버전 top-level runtime field만 있는 상태

중요: 현재 구현은 손상 파일을 자동 백업하거나 세밀하게 복원하지 않는다. 읽기 실패 시 기본 구조로 재정규화하는 fail-open 전략에 가깝다.

## 복구 체크리스트

### 1. 증상 확인

- hook 실행 후 `lifecycle_state`가 비어 있다.
- sync 또는 refresh 이후 `runtime_state`가 갱신되지 않는다.
- 상태 파일이 JSON으로 열리지 않는다.
- `schema_version`, `lifecycle_state`, `runtime_state` 중 하나가 없다.

### 2. 현재 파일 보존

자동 복구 전에 현재 파일을 별도 이름으로 복사해 둔다. 현재 구현은 quarantine copy를 자동 생성하지 않으므로 수동 보존이 안전하다.

예시:

```powershell
Copy-Item .copilot-memory\upgrade_state.json .copilot-memory\upgrade_state.corrupted.json -ErrorAction SilentlyContinue
```

### 3. 기본 self-check 실행

```powershell
python copilot/scripts/workspace_sync_server.py --self-check
python -m unittest discover -s tests -p "test_lifecycle_runtime_contract.py"
```

판단 기준:

- self-check가 현재 `repo_root`와 `scripts/upgrade_ai.py`를 찾으면 runtime root는 정상 후보다.
- unittest가 통과하면 schema normalization과 writer contract는 정상 후보다.

### 4. 상태 파일 재생성 또는 재정규화

아래 둘 중 하나를 선택한다.

1. 상태 파일을 제거한 뒤 writer를 다시 실행한다.
2. 상태 파일을 유지한 채 writer를 실행해 `schema_version: 2` shape로 재정규화한다.

가장 빠른 재생성 예시:

```powershell
python scripts/write_lifecycle_transition.py --workspace . --phase INIT --status active --active-task "recovery"
```

### 5. 최소 정상 shape 확인

복구 후 아래 필드는 반드시 보여야 한다.

| 필드 | 기대값 |
| --- | --- |
| `schema_version` | `2` |
| `lifecycle_state` | 객체 |
| `runtime_state` | 객체 |
| `lifecycle_state.updated_at` | 숫자 또는 `null` |
| `runtime_state.updated_at` | 숫자 또는 `null` |

### 6. 필요한 상태 다시 기록

현재 구현은 자동 resume를 제공하지 않으므로, 복구 뒤 필요한 상태를 다시 기록한다.

- 세션 시작 상태가 필요하면 hook 또는 `INIT` write를 다시 실행한다.
- approval 대기가 필요하면 아래처럼 required 인자를 모두 포함해 다시 기록한다.

```powershell
python scripts/write_lifecycle_transition.py --workspace . --phase AWAIT --status awaiting --active-task "await recovery" --approval-pending --await-reason "Recover approval boundary" --next-transition EXECUTE
```

- runtime 최신성 근거가 필요하면 sync 또는 refresh를 다시 실행한다.

## 복구 후 판정

- `lifecycle_state`와 `runtime_state`가 모두 존재한다.
- 새 write 후 `updated_at`이 갱신된다.
- 필요한 최소 phase가 다시 기록된다.
- smoke 명령이 통과한다.

## pending scope

- 손상 파일 자동 quarantine backup
- checksum 또는 partial write 감지
- 손상 전 `lifecycle_state` 세부 필드 자동 복원
- saved todo snapshot 자동 재구성
