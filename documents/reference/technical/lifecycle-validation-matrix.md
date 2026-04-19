# lifecycle-validation-matrix

## 목적

이 문서는 현재 lifecycle refactor에서 무엇이 어떤 근거로 검증되는지 한 표로 요약한다. 구현된 검증과 pending scope를 분리해 과장 없이 읽을 수 있게 하는 것이 목적이다.

## 현재 validation matrix

| 검증 대상 | 현재 근거 | 실행 경로 | 통과 기준 | 상태 |
| --- | --- | --- | --- | --- |
| hook manifest wiring | `tests/test_lifecycle_runtime_contract.py` | `python -m unittest discover -s tests -p "test_lifecycle_runtime_contract.py"` | `copilot/hooks.json`이 `sessionStart`, `sessionEnd`, `preCompact`와 대응 script를 가진다. | 구현됨 |
| plugin root resolution success | 같은 unittest + `tests/fixtures/minimal_plugin_tree` | 같은 명령 | copied minimal plugin tree에서 `runtime_root.find_plugin_root()`가 fixture root를 반환한다. | 구현됨 |
| plugin root resolution failure | 같은 unittest + `tests/fixtures/broken_plugin_tree` | 같은 명령 | marker가 일부 누락된 broken plugin tree에서 `Unable to resolve plugin root`가 발생한다. | 구현됨 |
| `lifecycle_state` 기본 shape | 같은 unittest | 같은 명령 | 빈 workspace에서도 `schema_version: 2`, `lifecycle_state`, `runtime_state`가 생성된다. | 구현됨 |
| 구버전 runtime field migration | 같은 unittest | 같은 명령 | top-level `last_sync`, `last_runtime_refresh`, `sync_check`가 nested `runtime_state`로 정규화된다. | 구현됨 |
| runtime refresh 기록 | 같은 unittest + `scripts/refresh_mcp_runtime.py` | unittest 또는 `python scripts/refresh_mcp_runtime.py --dry-run` | refresh payload shape가 정의돼 있고 non-dry-run이면 상태에 기록된다. | 구현됨 |
| stale runtime matching false-positive avoidance | 같은 unittest | 같은 명령 | dry-run refresh가 현재 plugin copy의 대상 script만 매칭하고 다른 plugin copy, 비대상 script, 비대상 실행기는 제외한다. | 구현됨 |
| workspace sync self-check와 root discovery | `copilot/scripts/workspace_sync_server.py` + 관련 unittest | `python copilot/scripts/workspace_sync_server.py --self-check` | `repo_root`, `upgrade_script`, `marker_files`가 현재 저장소와 일치한다. | 구현됨 |
| workspace sync 결과 기록 | `tests/test_lifecycle_runtime_contract.py` | `python -m unittest discover -s tests -p "test_lifecycle_runtime_contract.py"` | wrapper가 `last_sync` payload shape를 `runtime_state`와 top-level 미러에 기록한다. | 구현됨 |
| `AWAIT` persistence | 같은 unittest | 같은 명령 | `approval_pending`, `await_context`, `continuity.next_transition`이 함께 기록된다. | 구현됨 |
| `FINALIZE` normalization | 같은 unittest | 같은 명령 | `FINALIZE completed`가 `status=idle`, `active_task=null`로 정규화된다. | 구현됨 |
| session continuity marker | 같은 unittest | 같은 명령 | `sessionStart`, `preCompact`, `sessionEnd`가 `lifecycle_state.continuity`를 갱신한다. | 구현됨 |
| installer wiring | 같은 unittest + installer dry-run | `python scripts/install_vscode_plugin.py --dry-run --settings-file C:\path\to\settings.json --no-refresh-runtime` | `chat.pluginLocations`, `chat.hookFilesLocations`, `chat.plugins.enabled`, `chat.useCustomAgentHooks`가 맞게 구성된다. | 구현됨 |
| thin orchestrator contract | 같은 unittest + 문서 비교 | 같은 unittest | `orchestrator.agent.md`가 thin contract 섹션을 유지하고 구형 비대 섹션을 포함하지 않는다. | 구현됨 |
| stale cleanup false-positive avoidance | 같은 unittest | 같은 명령 | fresh backup, fresh marker, unmanaged backup은 삭제하지 않는다. | 구현됨 |
| stale cleanup idempotency | 같은 unittest + `tests/fixtures/cleanup_workspace` | 같은 명령 | copied cleanup fixture에서 첫 실행 후 재실행 시 추가 candidate/deletion 없이 종료된다. | 구현됨 |
| end-to-end resume hydrate | 문서만 있음 | 없음 | `PLAN -> AWAIT -> EXECUTE` 자동 재개를 fixture와 실제 writer 체인으로 증명해야 한다. | pending scope |
| live stale runtime fixture | 문서만 있음 | 없음 | 실제 프로세스를 세운 상태에서 terminate 권한과 race handling까지 검증해야 한다. | pending scope |
| corrupted state fixture 다양화 | 문서만 있음 | 없음 | JSON 손상, partial write, mixed shape를 여러 fixture로 검증해야 한다. | pending scope |
| live orchestrator phase transition integration | 문서만 있음 | 없음 | 실제 orchestrator execution path에서 writer 호출과 state 반영을 end-to-end로 증명해야 한다. | pending scope |

## 운영용 최소 명령 세트

```powershell
python -m unittest discover -s tests -p "test_lifecycle_runtime_contract.py"
python scripts/refresh_mcp_runtime.py --dry-run
python copilot/scripts/workspace_sync_server.py --self-check
```

## 해석 규칙

- unittest 통과는 contract regression 방어선으로 해석한다.
- dry-run과 self-check는 현재 machine의 runtime-owned surfaces 확인으로 해석한다.
- self-check는 root discovery 증거이지 실제 sync result persistence 증거는 아니다.
- stale runtime matching 검증은 mocked process 목록 기준 근거이며, live process integration 증거는 아니다.
- fixture가 없는 항목은 문서에 적혀 있어도 구현 완료로 판정하지 않는다.

## pending scope

- deploy copy와 source checkout 분리 fixture
- automatic guided resume 검증
- live stale runtime process integration 검증
- live orchestrator phase transition writer integration 검증
- acceptance report를 실제 런 결과와 묶는 반복 가능한 파이프라인
