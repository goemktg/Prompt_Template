# orchestrator-responsibility-split-map

## 목적

이 문서는 현재 lifecycle refactor 기준으로 어떤 책임이 prompt 자산에 남아 있고, 어떤 책임이 runtime 표면과 테스트로 내려갔는지 빠르게 보여주는 split map이다.

## 한눈에 보는 분리 원칙

- prompt-only: 규칙 선언, 경계 설명, routing narrative, operator-facing contract
- runtime-owned: sync 실행, process refresh, state write, hook event handling
- tests-owned: wiring shape, persistence shape, thin-contract regression 검증

## 표면별 책임

| 표면 | 현재 책임 | 성격 |
| --- | --- | --- |
| `copilot/agents/orchestrator.agent.md` | lifecycle phase vocabulary, orchestration boundary, session-once sync check 요구, delegation/TODO contract | prompt-only |
| `AGENTS.md` | agent catalog, skill routing, orchestrator를 언제 쓰는지에 대한 저장소 수준 설명 | prompt-only |
| `shared/copilot-instructions.md` | lifecycle-first operating model, tier/gate/delegation 정책, main-session과 subagent 경계 | prompt-only |
| `copilot/hooks.json` | `sessionStart`, `sessionEnd`, `preCompact` runtime event wiring | runtime-owned manifest |
| `copilot/hooks/scripts/*.py` | session lifecycle continuity marker 기록, fail-open hook 동작 | runtime-owned implementation |
| `copilot/scripts/runtime_root.py` | plugin root discovery contract | runtime-owned implementation |
| `copilot/scripts/runtime_launcher.py` | MCP mode dispatch | runtime-owned implementation |
| `scripts/install_vscode_plugin.py` | VS Code settings 등록, hook manifest 등록, stale refresh 호출 | runtime-owned implementation |
| `copilot/scripts/workspace_sync_server.py` | sync self-check, wrapper execution, sync result persistence | runtime-owned implementation |
| `scripts/refresh_mcp_runtime.py` | stale runtime process 탐지/종료와 refresh 결과 persistence | runtime-owned implementation |
| `scripts/write_lifecycle_transition.py` | explicit phase transition persistence | runtime-owned implementation |
| `copilot/scripts/upgrade_state.py` | `upgrade_state.json` schema migration, atomic save, nested state normalization | runtime-owned implementation |
| `tests/test_lifecycle_runtime_contract.py` | hook wiring, state shape, installer wiring, thin orchestrator contract regression | validation |

## prompt-only에 남긴 것

- 어떤 phase vocabulary를 쓸지
- orchestrator가 어디까지 조정자 역할만 해야 하는지
- direct-answer carveout, Tier 0/1/2, delegation gate 같은 정책 설명
- TODO title 형식과 orchestration plan 최소 shape

이 영역은 실행 로직이 아니라 operator와 agent가 따라야 할 계약이다.

## runtime-owned로 내려간 것

- plugin root 탐지와 settings 기반 plugin copy lookup
- stale runtime process refresh
- workspace sync 실행과 결과 기록
- session hook 이벤트 처리
- `lifecycle_state`, `runtime_state` persistence와 schema migration

즉, 실제 side effect와 상태 기록은 prompt에서 설명만 하지 않고 runtime script가 수행한다.

## 아직 prompt 자산에 남아 있지만 runtime으로 더 내릴 수 있는 영역

- session-once sync check의 호출 강제 수준
- approval wait와 resume를 자동 복원하는 상위 orchestration helper
- self-check 실패 시 richer operator guidance

현재는 정책 또는 계약으로는 분리됐지만, 완전한 runtime enforcement까지는 가지 않은 영역이다.

## 운영 판단 규칙

- 새로운 책임이 파일 쓰기, process 제어, settings 조회를 동반하면 runtime-owned 후보로 본다.
- 새로운 책임이 routing 설명, lifecycle 문법, 승인 정책을 다루면 prompt-only 후보로 본다.
- 새 변경이 thin orchestrator contract를 깨는지 여부는 unittest와 문서 둘 다에서 확인한다.

## 관련 문서

- `runtime-path-contract.md`: root resolution과 lookup 경로
- `runtime-refresh-runbook.md`: stale runtime refresh와 smoke
- `lifecycle-state-schema-guide.md`: 상태 스키마와 writer 표면
- `lifecycle-validation-guide.md`: 현재 validation surface와 남은 fixture 공백
