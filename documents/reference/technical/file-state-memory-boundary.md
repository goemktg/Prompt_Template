# file-state-memory-boundary

## 목적

이 문서는 `.copilot-memory/upgrade_state.json`과 Memory MCP 사이의 authoritative boundary를 짧게 고정한다. 목표는 동일 정보를 두 군데에 중복 저장해 drift를 만드는 일을 줄이는 것이다.

## 기본 원칙

| 질문 | 정답 |
| --- | --- |
| runtime과 lifecycle의 authoritative state는 어디에 저장하는가 | file state |
| cross-agent summary와 handoff 메모는 어디에 저장하는가 | Memory MCP |
| 같은 phase/status를 둘 다에 상세 저장해도 되는가 | 아니오 |

## authoritative ownership

| 정보 종류 | 기본 저장소 | 예시 |
| --- | --- | --- |
| 현재 phase, status, await context | `.copilot-memory/upgrade_state.json` | `lifecycle_state.current_phase`, `await_context` |
| runtime refresh, sync, cleanup 결과 | `.copilot-memory/upgrade_state.json` | `runtime_state.last_sync`, `last_runtime_refresh` |
| schema migration과 compatibility mirror | `.copilot-memory/upgrade_state.json` | top-level `last_sync`, `sync_check` |
| cross-agent handoff summary | Memory MCP | step summary, decision note, failure context |
| long-running doc or review 기억 | Memory MCP | 문서 스타일 결정, handoff status |

## 중복 최소화 규칙

1. phase, status, plan hash, approval pending 같은 machine state는 file을 우선한다.
2. Memory MCP에는 그 state를 복제하지 말고 해석 요약만 남긴다.
3. Memory MCP에 저장할 때는 file의 필드값 자체보다 "왜 이 상태가 중요한지"를 요약한다.
4. 동일 사실을 양쪽에 써야 하면 file에는 원본 값, Memory MCP에는 참조 메모만 둔다.

## 권장 저장 예

| 상황 | file state | Memory MCP |
| --- | --- | --- |
| `AWAIT` 진입 | 필수 | 선택 |
| runtime refresh 결과 | 필수 | 보통 불필요 |
| cross-agent 전달용 plan 요약 | 선택 | 권장 |
| documentation session summary | 불필요 | 권장 |

## 현재 저장소 기준 해석

- `write_lifecycle_transition.py`, hook scripts, sync/refresh scripts는 file state writer다.
- `shared/copilot-instructions.md`가 말하는 step prompt, failure context, summary 저장은 Memory MCP 쪽 책임이다.
- 따라서 `upgrade_state.json`은 실행 상태, Memory MCP는 협업 문맥 요약이라는 경계를 유지해야 한다.

## 주의

- Memory MCP가 일시적으로 불가하더라도 runtime/lifecycle state는 file 기준으로 유지된다.
- 반대로 file state가 손상되면 Memory MCP summary만으로 machine resume를 대체하지 않는다.

## 관련 문서

- [lifecycle-state-schema-guide.md](./lifecycle-state-schema-guide.md)
- [lifecycle-save-resume-event-matrix.md](./lifecycle-save-resume-event-matrix.md)
- [orchestrator-responsibility-split-map.md](./orchestrator-responsibility-split-map.md)
