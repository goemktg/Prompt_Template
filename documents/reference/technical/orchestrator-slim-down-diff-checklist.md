# orchestrator-slim-down-diff-checklist

## 목적

이 체크리스트는 `copilot/agents/orchestrator.agent.md` 변경이 현재의 slim contract를 유지하는지 diff 기준으로 빠르게 검토하기 위한 것이다.

## 반드시 유지할 것

- `Mission`, `Boundary`, `Session-Once Sync Check`, `Lifecycle Protocol`, `Planning And Output Contract` 섹션이 남아 있어야 한다.
- lifecycle vocabulary는 `INIT`, `ATOMIZE`, `PLAN`, `EXECUTE`, `REPORT`, `AWAIT`, `FINALIZE`를 그대로 사용해야 한다.
- sync, refresh, state persistence는 runtime-owned surfaces 책임으로 남겨야 한다.
- orchestrator는 specialist 구현을 직접 소유하지 않는다고 명시해야 한다.

## diff 체크리스트

| 점검 질문 | 기대 답 |
| --- | --- |
| orchestrator가 runtime process 정리 로직을 직접 설명하거나 재구현하는가 | 아니오 |
| orchestrator가 `lifecycle_state` 또는 `runtime_state` write 절차를 직접 소유한다고 말하는가 | 아니오 |
| orchestrator가 대형 routing catalog 또는 workflow recipe를 다시 끌어오는가 | 아니오 |
| `Session-Once Sync Check`가 runtime-owned surfaces 사용을 요구하는가 | 예 |
| `AWAIT`를 실제 hold state로 유지하는가 | 예 |
| `REPORT -> AWAIT`, `PLAN -> AWAIT` 경계를 유지하는가 | 예 |

## reject 신호

- `Strategic Modes`, `Workflow Recipes`, `Agent Registry & Routing` 같은 구형 비대 섹션이 다시 등장한다.
- orchestrator가 settings 수정, process terminate, state schema migration 같은 side effect를 직접 책임진다고 서술한다.
- `AWAIT` 중에도 백그라운드 실행을 계속하는 서술이 들어간다.
- runtime-owned surfaces 대신 prompt 자산 안에 self-check 절차를 복제한다.

## 권장 review 순서

1. diff에서 section 제목 변화부터 확인한다.
2. `runtime-owned surfaces`, `lifecycle_state`, `runtime_state` 용어 사용이 유지되는지 본다.
3. `tests/test_lifecycle_runtime_contract.py`의 thin-contract assertion과 충돌하는 문구가 없는지 본다.
4. 필요하면 아래 smoke를 같이 실행한다.

```powershell
python -m unittest discover -s tests -p "test_lifecycle_runtime_contract.py"
```

## pending scope

- diff checklist를 자동 lint 또는 CI gate로 연결하는 작업
- orchestrator slim-down 이후 실제 token budget 개선 측정
