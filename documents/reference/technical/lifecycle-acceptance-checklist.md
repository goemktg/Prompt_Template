# lifecycle-acceptance-checklist

## 목적

이 체크리스트는 현재 저장소에 이미 구현된 lifecycle slice를 빠르게 점검하기 위한 acceptance 및 smoke 절차다. 모든 항목은 현재 존재하는 script, hook, test 표면만 사용한다.

## 권장 실행 순서

1. 정적 wiring 확인
2. installer dry-run 확인
3. runtime refresh dry-run 확인
4. workspace sync self-check 확인
5. lifecycle/unit smoke 실행

공통 smoke 명령:

```powershell
python -m unittest discover -s tests -p "test_lifecycle_runtime_contract.py"
```

## 1. 정적 wiring 확인

확인 대상:

- `plugin.json`이 `copilot/hooks.json`과 `copilot/mcp.json`을 가리킨다.
- `copilot/hooks.json`에 `sessionStart`, `sessionEnd`, `preCompact`가 선언되어 있다.
- hook script 파일이 실제로 존재한다.

실행 명령: 위 공통 smoke 명령 사용

통과 기준:

- hook manifest shape 검증이 통과한다.
- orchestrator thin-contract 검증이 통과한다.
- `upgrade_state.json` 초기화 및 migration shape 검증이 통과한다.

## 2. Installer dry-run

VS Code 설정 파일을 실제로 수정하지 않고 registration 경로만 확인한다.

```powershell
python scripts/install_vscode_plugin.py --dry-run --settings-file C:\path\to\settings.json --no-refresh-runtime
```

통과 기준:

- 명령이 실패하지 않는다.
- 대상 settings 파일에 대해 `would update` 또는 `already current`가 출력된다.
- 실제 파일 쓰기나 process terminate가 발생하지 않는다.

## 3. Runtime refresh dry-run

stale local runtime process 탐지 범위를 확인한다.

```powershell
python scripts/refresh_mcp_runtime.py --dry-run
```

통과 기준:

- 명령이 실패하지 않는다.
- 결과에 plugin root가 맞게 해석된다.
- 매치가 없으면 `No stale runtime processes matched plugin root`가 출력된다.
- 매치가 있으면 대상 script가 `runtime_launcher.py`, `workspace_sync_server.py`, `start-memory.py` 범위로만 식별된다.

## 4. Workspace sync runtime/self-check

workspace sync server가 현재 plugin root와 upgrade entrypoint를 올바르게 찾는지 확인한다.

```powershell
python copilot/scripts/workspace_sync_server.py --self-check
```

통과 기준:

- JSON 출력에 `repo_root`, `upgrade_script`, `python_executable`, `marker_files`가 포함된다.
- `repo_root`가 현재 저장소 root를 가리킨다.
- `upgrade_script`가 `scripts/upgrade_ai.py`를 가리킨다.

## 5. Lifecycle persistence smoke

명시 phase write와 hook 기반 session lifecycle이 현재 스키마에 저장되는지 확인한다.

우선순위가 높은 기본 smoke는 위 공통 smoke 명령으로 실행한다.

선택적 수동 spot-check:

```powershell
python scripts/write_lifecycle_transition.py --workspace C:\path\to\workspace --phase PLAN --status active --active-task "smoke" --plan-hash "plan-smoke"
```

통과 기준:

- `lifecycle_state.current_phase`가 입력값과 일치한다.
- `AWAIT` 입력 시 `approval_pending`, `await_context`, `continuity.next_transition`이 함께 저장된다.
- `FINALIZE completed` 입력 시 상태가 `idle`로 정규화되고 `active_task`가 비워진다.

## 6. Hook/session lifecycle 확인

이 항목은 현재 unittest가 가장 신뢰도 높은 smoke 경로다. 아래 검증이 포함되어야 한다.

- `session_init.py` 실행 후 `INIT` / `active` / `continuity.last_event=sessionStart`
- `pre-compact.py` 실행 후 `compact_safe=true`, `last_compaction_checkpoint=true`
- `session_end.py` 실행 후 `FINALIZE` / `idle` / `continuity.last_event=sessionEnd`
- malformed payload에서도 hook가 fail-open으로 종료 코드 `0`을 유지

실행 명령: 위 공통 smoke 명령 사용

## 7. 상태 파일 확인 포인트

확인 파일: `.copilot-memory/upgrade_state.json`

최소 확인 항목:

- `schema_version`이 `2`다.
- `lifecycle_state`와 `runtime_state`가 모두 존재한다.
- runtime refresh 또는 sync 실행 후 해당 payload가 top-level 미러와 nested state에 함께 남는다.
- hook 또는 transition writer 실행 후 `lifecycle_state.updated_at`이 갱신된다.

## 실패 시 우선 확인

- plugin root 탐지가 실패하면 `copilot/scripts/runtime_root.py` marker set과 실제 경로를 먼저 확인한다.
- sync 관련 실패면 `workspace_sync_server.py --self-check` 결과와 `scripts/upgrade_ai.py` 경로를 함께 본다.
- lifecycle persistence가 비어 있으면 대상 workspace의 `.copilot-memory/upgrade_state.json` 생성 여부를 확인한다.
- hook 동작이 비어 있으면 `copilot/hooks.json` 경로, `cwd`, script 상대경로가 일치하는지 확인한다.
