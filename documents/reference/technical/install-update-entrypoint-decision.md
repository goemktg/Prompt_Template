# install-update-entrypoint-decision

## 목적

이 문서는 현재 저장소에서 install/update 진입점을 어떻게 해석할지 짧게 고정한다. 핵심 질문은 `scripts/install_vscode_plugin.py`가 표준 진입점인지, 아니면 별도 all-in-one installer가 더 필요한지다.

## 현재 결정

| 표면 | 현재 역할 | 표준 진입점 여부 |
| --- | --- | --- |
| `scripts/install_vscode_plugin.cmd` | Windows 사용자를 위한 launcher shim | 아니오 |
| `scripts/install_vscode_plugin.py` | VS Code settings 등록, hook manifest 등록, stale runtime refresh, post-install verification 실행 | 예. Windows 기준 plugin registration entrypoint |
| `scripts/upgrade_ai.py` | workspace sync와 supplementary deploy worker | 아니오. user-facing installer가 아니라 runtime worker |
| `copilot/scripts/workspace_sync_server.py` | runtime self-check와 sync wrapper | 아니오. install 진입점이 아니라 runtime execution 표면 |

결론은 다음과 같다.

1. 현재 저장소에는 `templerun`식 단일 install/update orchestrator를 추가하지 않는다.
2. Windows에서 plugin 등록의 표준 진입점은 `scripts/install_vscode_plugin.py`다.
3. `scripts/install_vscode_plugin.cmd`는 Python 탐색만 담당하는 편의 wrapper이므로 표준 로직 진입점으로 보지 않는다.
4. update 작업은 하나의 installer로 합치지 않고 `workspace_sync_server.py`와 `upgrade_ai.py` 경로로 분리 유지한다.

## 이유

- `install_vscode_plugin.py`는 실제 side effect를 모두 묶고 있다.
- 같은 스크립트가 `verify_runtime_activation.py`까지 호출하므로 등록과 검증이 한 경로에서 끝난다.
- unittest가 settings registration과 hook activation branch를 이미 고정한다.
- 반면 `upgrade_ai.py`는 target workspace를 받아 실행되는 worker라서 plugin registration의 표준 진입점으로 쓰기 어렵다.
- 현재 남은 공백은 install entrypoint 부재보다 live sync proof와 richer recovery 문서에 가깝다.

## accepted boundary

- 표준 install entrypoint는 있다.
- 표준 all-in-one update entrypoint는 없다.
- 이 부재는 현재 허용된 구조적 선택이며, 새로운 script 추가 없이 운영 가능하다고 본다.

## 재검토 조건

아래 둘이 함께 생길 때만 단일 install/update entrypoint를 다시 검토한다.

1. `install_vscode_plugin.py`와 `upgrade_ai.py` 사이 수동 단계가 운영 오류의 주원인이 된다.
2. 하나의 user-facing command로 registration, sync, refresh, verification을 묶어야 할 명시 근거가 생긴다.

## 관련 문서

- [runtime-path-contract.md](./runtime-path-contract.md)
- [runtime-refresh-runbook.md](./runtime-refresh-runbook.md)
- [lifecycle-acceptance-checklist.md](./lifecycle-acceptance-checklist.md)
