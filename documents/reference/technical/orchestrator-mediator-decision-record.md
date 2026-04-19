# orchestrator-mediator-decision-record

## 목적

이 문서는 현재 저장소에서 mediator를 새로 도입할지 여부를 lifecycle refactor 기준으로 기록하는 decision record다.

## 현재 결정

- 결정: 지금은 별도 mediator를 추가하지 않는다.
- 상태: active decision
- 판단 기준일: 2026-04-18

현재 저장소는 아래 표면으로 이미 책임 분리가 이뤄져 있다.

| 책임 | 현재 표면 |
| --- | --- |
| lifecycle vocabulary와 orchestration boundary | `copilot/agents/orchestrator.agent.md`, `AGENTS.md`, `shared/copilot-instructions.md` |
| runtime-owned surfaces | `copilot/hooks.json`, `copilot/hooks/scripts/*.py`, `copilot/scripts/workspace_sync_server.py`, `scripts/refresh_mcp_runtime.py`, `scripts/write_lifecycle_transition.py` |
| state persistence | `copilot/scripts/upgrade_state.py` |
| regression guard | `tests/test_lifecycle_runtime_contract.py` |

즉, 현재 문제는 mediator 부재보다 pending automation과 fixture 부족에 더 가깝다.

## no-go 근거

1. hook, sync, refresh, state write가 이미 runtime-owned surfaces로 내려가 있다.
2. thin orchestrator contract는 unittest로 회귀 방어가 걸려 있다.
3. 현재 남은 공백은 live orchestrator integration proof, fixture 다양화, richer recovery 문서처럼 mediator 없이도 해결 가능한 항목이 많다.
4. mediator를 추가하면 새로운 routing surface와 문서 동기화 비용이 늘어난다.

## mediator를 다시 검토하는 조건

아래 두 조건이 함께 성립할 때만 재검토한다.

- instruction, skill, runtime-owned surfaces만으로는 lifecycle semantics를 안정적으로 유지할 수 없다.
- mediator가 context budget 절감 또는 protocol normalization에 명확한 이득을 준다.

## go 또는 no-go 판정표

| 질문 | 현재 답 |
| --- | --- |
| runtime-owned surface만으로 책임을 내릴 수 있는가 | 예 |
| mediator가 없어서 막힌 구현이 있는가 | 아니오 |
| mediator 도입이 context budget 또는 protocol normalization에 즉시 이득을 주는가 | 아직 아님 |
| 그래서 지금 introduction plan이 필요한가 | 아니오 |

현재 판정은 no-go이므로 mediator introduction plan을 추가로 작성하지 않는다.
재검토가 필요해지면 그때 별도 decision record 또는 implementation plan을 만든다.

## pending scope

- live orchestrator integration proof가 쌓인 뒤에도 mediator 필요성이 남는지 재평가
- context budget 절감 또는 protocol normalization의 계량 근거 수집
