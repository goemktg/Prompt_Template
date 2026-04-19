# runtime-surface-inventory

## 목적

이 문서는 현재 저장소의 runtime-owned surface를 한 번에 확인하고, `plugin.json` 기준 누락 표면이 있는지 짧게 판정한다.

## manifest 기준 inventory

| 선언 위치 | 경로 | 실제 상태 | 메모 |
| --- | --- | --- | --- |
| `plugin.json` | `copilot/agents/` | 존재 | runtime-owned agent definitions |
| `plugin.json` | `copilot/skills/` | 존재 | runtime-owned skills |
| `plugin.json` | `copilot/hooks.json` | 존재 | hook manifest |
| `plugin.json` | `copilot/mcp.json` | 존재 | MCP manifest |

## 운영 표면 inventory

| 종류 | 표면 | 상태 |
| --- | --- | --- |
| hook manifest | `copilot/hooks.json` | 구현됨 |
| hook scripts | `copilot/hooks/scripts/session_init.py`, `copilot/hooks/scripts/session_end.py`, `copilot/hooks/pre-compact.py` | 구현됨 |
| runtime root | `copilot/scripts/runtime_root.py` | 구현됨 |
| launcher | `copilot/scripts/runtime_launcher.py` | 구현됨 |
| sync wrapper | `copilot/scripts/workspace_sync_server.py` | 구현됨 |
| state store | `copilot/scripts/upgrade_state.py` | 구현됨 |
| explicit transition writer | `scripts/write_lifecycle_transition.py` | 구현됨 |
| install registration | `scripts/install_vscode_plugin.py` | 구현됨 |
| activation verifier | `scripts/verify_runtime_activation.py` | 구현됨 |
| stale runtime refresh | `scripts/refresh_mcp_runtime.py` | 구현됨 |
| stale file cleanup | `scripts/cleanup_runtime_artifacts.py` | 구현됨 |

## missing-surface 판정

- `plugin.json`이 선언한 핵심 runtime surface 누락은 현재 없다.
- `copilot/hooks.json`이 가리키는 script도 현재 모두 존재한다.
- `copilot/mcp.json`이 기대하는 launcher 경로도 현재 존재한다.

즉, 현재 남은 이슈는 missing file이 아니라 아래 성격에 가깝다.

1. 일부 bootstrap logic이 중복돼 있다.
2. live orchestrator execution integration 증거가 아직 부족하다.
3. richer recovery guidance와 sync 범위 설명이 더 필요하다.

## 운영 결론

- missing runtime-owned surface 생성 태스크는 현재 기준으로 닫을 수 있다.
- 후속 작업은 새 파일 추가보다 proof 확대와 문서 정렬에 둔다.

## 관련 문서

- [runtime-path-contract.md](./runtime-path-contract.md)
- [orchestrator-responsibility-split-map.md](./orchestrator-responsibility-split-map.md)
- [lifecycle-validation-matrix.md](./lifecycle-validation-matrix.md)
