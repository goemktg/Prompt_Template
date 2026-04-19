# lifecycle-acceptance-report-template

## 목적

이 템플릿은 현재 저장소의 lifecycle 변경을 점검한 뒤 결과를 짧게 남기기 위한 acceptance report 골격이다. 현재 구현된 검증 표면만 반영하며, pending scope는 반드시 별도 구역에 남긴다.

## 템플릿

~~~markdown
# Lifecycle Acceptance Report

## 기본 정보

- 대상 변경: [change summary]
- 작성일: [YYYY-MM-DD]
- 검증자: [name]
- 대상 workspace: [path]

## 실행 명령

```powershell
python -m unittest discover -s tests -p "test_lifecycle_runtime_contract.py"
python scripts/refresh_mcp_runtime.py --dry-run
python copilot/scripts/workspace_sync_server.py --self-check
```

필요 시 persistence 근거를 추가하려면 아래 명령을 별도로 실행한다.

```powershell
python scripts/refresh_mcp_runtime.py
python scripts/write_lifecycle_transition.py --workspace . --phase PLAN --status active --active-task "acceptance" --plan-hash "acceptance-plan"
```

## 판정 요약

| 항목 | 결과 | 근거 |
| --- | --- | --- |
| hook wiring | PASS / FAIL / PENDING | [short note] |
| lifecycle_state persistence | PASS / FAIL / PENDING | [short note] |
| runtime_state persistence | PASS / FAIL / PENDING | [short note] |
| stale runtime cleanup scope | PASS / FAIL / PENDING | [short note] |
| thin orchestrator contract | PASS / FAIL / PENDING | [short note] |

## 상태 파일 확인

- `schema_version`: [value]
- `lifecycle_state.current_phase`: [value]
- `runtime_state.updated_at`: [value]
- 확인한 파일: `[target_workspace]/.copilot-memory/upgrade_state.json` 또는 `[plugin_root]/.copilot-memory/upgrade_state.json`
- 주의: dry-run과 self-check만 실행했다면 `runtime_state` persistence 또는 stale cleanup 결과는 `PENDING`으로 남긴다.

## 차단 이슈

- [없으면 없음]

## pending scope

- [현재 구현되지 않은 항목만 기재]

## 최종 판정

- 최종 상태: ACCEPTED / CONDITIONAL / REJECTED
- 근거: [one paragraph]

## Review Validation Evidence

| 필드 | 값 |
| --- | --- |
| Verdict | APPROVED / CONDITIONAL / REJECTED |
| Reviewed Files | [comma-separated paths] |
| Review Attempts | [number] |
| Open Issues | [number or short note] |
| Blocking Issues | [none or short note] |

~~~

## 사용 규칙

- `PASS`는 현재 저장소의 구현과 테스트 또는 self-check 결과가 직접 뒷받침할 때만 사용한다.
- `runtime_state persistence`와 `stale runtime cleanup scope`는 non-dry-run 실행 또는 unittest 근거 없이 `PASS`로 올리지 않는다.
- 증거가 문서뿐이면 `PENDING`으로 남긴다.
- `pending scope` 구역은 비워 두지 않는다. 남은 구현 또는 fixture 공백을 명시한다.
