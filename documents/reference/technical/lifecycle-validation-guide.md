# lifecycle-validation-guide

> 참고: 이 문서는 supporting reference다. terminal-boundary lifecycle operator의 canonical runbook은 `documents/reference/technical/terminal-boundary-live-verification-reference.md`를 우선 기준으로 사용한다.

## 목적

이 문서는 현재 lifecycle refactor의 검증 표면이 어디까지 구현됐는지, 무엇을 신뢰할 수 있고 무엇이 아직 비어 있는지 정리한 운영 가이드다.

## 현재 검증 표면

핵심 자동 검증은 아래 unittest 한 파일에 모여 있다.

```powershell
python -m unittest discover -s tests -p "test_lifecycle_runtime_contract.py"
```

현재 이 스위트는 다음을 검증한다.

| 범주 | 현재 검증 내용 |
| --- | --- |
| hook wiring | `copilot/hooks.json` shape, script path, event 이름 |
| path resolution | copied minimal plugin tree 성공 경로와 broken plugin tree 실패 경로 |
| state schema | `UpgradeStateStore` 기본 shape, migration shape, nested runtime/lifecycle state |
| runtime refresh | refresh 결과 payload가 `runtime_state`와 top-level 미러에 함께 기록되는지, target plugin copy만 매칭하고 다른 plugin copy/비대상 script를 제외하는지 |
| workspace sync | sync 결과 payload shape와 wrapper 기록 형식 |
| session lifecycle | `sessionStart`/`preCompact`/`sessionEnd`가 state를 올바르게 갱신하는지 |
| explicit transition | `PLAN`, `AWAIT`, `FINALIZE` write 규칙과 invalid phase rejection |
| installer wiring | settings에 plugin root, hook manifest, custom hooks enable이 함께 기록되는지 |
| cleanup boundary | stale candidate 삭제, fresh/unmanaged file 보존, copied fixture 재실행 idempotency |
| orchestrator slim contract | `orchestrator.agent.md`가 thin contract 섹션을 유지하고 과거 비대 구조를 포함하지 않는지 |

## 현재 핵심 invariant

- 상태 파일은 `schema_version: 2`로 정규화된다.
- `lifecycle_state`와 `runtime_state`는 항상 존재한다.
- copied minimal plugin tree에서는 plugin root resolution이 성공하고, broken plugin tree에서는 표준 오류로 실패한다.
- runtime 결과는 nested state와 top-level compatibility field에 함께 남는다.
- stale runtime refresh dry-run은 현재 plugin copy의 대상 script만 매칭하고 다른 plugin copy, 비대상 script, 비대상 실행기는 제외한다.
- `FINALIZE completed`는 `status=idle`, `active_task=null`로 정규화된다.
- `AWAIT` write는 `approval_pending`, `await_context`, `continuity.next_transition`을 함께 남긴다.
- cleanup은 fresh backup, fresh marker, unmanaged `.bak` 파일을 보존하고 fixture 재실행 시 추가 삭제 없이 종료된다.
- hook는 malformed payload에서도 fail-open으로 종료 코드 `0`을 유지한다.
- orchestrator는 coordination contract만 남기고 runtime sync/state enforcement를 직접 소유하지 않는다.

## 수동 검증이 필요한 면

- 실제 VS Code session에서 hook가 항상 기대 시점에 호출되는지
- 실제 stale process가 존재할 때 terminate 권한과 race handling이 안정적인지
- `chat.pluginLocations` 또는 plugin copy 환경이 다양한 실제 사용자 머신에서 동일하게 동작하는지
- `scripts/upgrade_ai.py`와 sync wrapper의 end-to-end supplementary deploy 결과
- 실제 orchestrator execution path에서 phase transition writer가 항상 호출되는지

즉, 현재 검증은 contract와 payload shape에는 강하지만, 실제 multi-environment 운영 리허설은 아직 얕다.

## 아직 부족한 fixture와 테스트

- corrupted state fixture: 더 다양한 JSON 손상 및 partial write 상황
- live stale runtime fixture: 실제 matching process를 세워 놓고 refresh를 검증하는 통합 테스트
- workspace fixture: source checkout과 deployed plugin copy를 분리한 sync 시나리오
- resume fixture: `PLAN -> AWAIT -> EXECUTE` 재개를 end-to-end로 검증하는 상태 샘플
- negative installer fixture: settings가 `dict`, `list`, `string` 각각일 때 더 넓은 regression 세트

## 권장 추가 순서

1. path/root fixture를 먼저 늘린다.
2. stale runtime 통합 fixture를 추가한다.
3. `AWAIT` resume 시나리오 fixture를 넣는다.
4. deploy copy와 source checkout 분리 환경에서 sync 통합 테스트를 보강한다.

## smoke 보조 절차

자동 테스트 외에 아래 두 명령을 같이 보면 운영 신뢰도가 올라간다.

```powershell
python scripts/refresh_mcp_runtime.py --dry-run
python copilot/scripts/workspace_sync_server.py --self-check
```

이 조합은 unittest가 다루지 못하는 현재 machine의 root lookup과 runtime visibility를 빠르게 점검한다.

## 결론

현재 validation surface는 lifecycle contract regression을 막는 최소 방어선으로는 충분하다. 특히 broken-path path resolution, stale runtime 매칭 회피, stale cleanup 보존/재실행 보장은 테스트로 고정됐다. 다만 실제 deployed-copy 통합 검증과 live orchestrator execution 연동 증명은 아직 후속 작업으로 남아 있다.
