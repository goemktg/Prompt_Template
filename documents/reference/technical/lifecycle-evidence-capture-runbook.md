# lifecycle-evidence-capture-runbook

> 참고: 이 문서는 supporting reference다. terminal-boundary lifecycle operator의 canonical runbook은 `documents/reference/technical/terminal-boundary-live-verification-reference.md`를 우선 기준으로 사용한다.

## 목적

이 runbook은 terminal -> next fresh session 경계에서 lifecycle evidence를 일관된 순서로 채집하기 위한 운영 절차다. 목적은 설명이 아니라 재현 가능한 기록이다.

사용 대상은 orchestrator/runtime maintainers와 lifecycle verification operator다.

## 적용 범위

이 runbook은 아래 상황에만 적용한다.

- `FINALIZE` 또는 terminal cleanup 이후 다음 fresh `sessionStart` reset 증거 채집
- stale continuity key 부재, stale `current_plan_hash` 부재, `last_terminal_status` carry-over 부재 판정
- 문서, 이슈, 검증 보고서에 붙일 before/after snapshot 정리

`AWAIT` hydrate 품질 검증, 전체 acceptance, 손상 복구 절차는 본 runbook의 주 범위가 아니다.

## 사전 준비

- 대상 workspace 경로를 알고 있어야 한다.
- `.copilot-memory/upgrade_state.json`을 읽을 수 있어야 한다.
- `scripts/write_lifecycle_transition.py`를 실행할 수 있어야 한다.
- 다음 fresh session을 실제로 시작할 수 있어야 한다.
- 관찰 기록을 남길 기본 문서 위치가 준비돼 있어야 한다.

권장 기본 저장 위치:

- 요약 보고: `documents/drafts/<date>-terminal-boundary-evidence.md`
- 구조화 로그: `results/lifecycle/<timestamp>_terminal-boundary.json`

권장 준비 명령:

```powershell
$Workspace = "C:\Users\samkt\workplace\0_active_projects\Visual_Studio_Code\Prompt_Template"
Set-Location $Workspace
```

## 증거 채집 순서

증거 채집 순서는 반드시 아래 순서를 따른다.

1. baseline 확인
2. terminal write 실행
3. pre-hook snapshot 채집
4. 다음 fresh session 시작
5. post-sessionStart snapshot 채집
6. pass/fail 판정
7. failure bucket 분류

순서를 바꾸면 pre-hook 상태와 post-sessionStart 상태가 섞여 증거력이 떨어진다.

## 정확한 관찰 지점

| 순서 | 관찰 지점 | 언제 기록하는가 | 기록 위치 |
| --- | --- | --- | --- |
| 1 | baseline state | terminal write 전 | `.copilot-memory/upgrade_state.json` |
| 2 | terminal write result | `FINALIZE` write 직후 | command output + state file |
| 3 | pre-hook snapshot | 다음 세션 시작 전 | `.copilot-memory/upgrade_state.json` |
| 4 | next fresh session trigger | 새 세션 시작 직후 | operator action log |
| 5 | post-sessionStart snapshot | `sessionStart` hook 완료 후 | `.copilot-memory/upgrade_state.json` |
| 6 | 판정 메모 | before/after 비교 직후 | `documents/drafts/<date>-terminal-boundary-evidence.md` 또는 `results/lifecycle/<timestamp>_terminal-boundary.json` |

## 기록할 값

각 snapshot마다 최소한 아래 값을 기록한다.

| 필드 | 기록 이유 |
| --- | --- |
| `lifecycle_state.current_phase` | phase reset 여부 판단 |
| `lifecycle_state.status` | `active` / `idle` 구분 |
| `lifecycle_state.current_plan_hash` | stale plan hash carry-over 판정 |
| `lifecycle_state.active_task` | terminal residue 최소화 확인 |
| `lifecycle_state.continuity.last_terminal_status` | terminal marker의 다음 세션 carry-over 판정 |
| `lifecycle_state.await_context` | 잘못된 resume 진입 탐지 |
| `lifecycle_state.hydrated_from_previous_session` | fresh session인데 hydrate marker가 남는지 확인 |
| `lifecycle_state.updated_at` | snapshot 순서 검증 |

추가로 stale continuity clue가 있으면 이름과 값을 그대로 적는다. 예시는 `resume_token`, `continuity.next_transition`, 이전 delegated step clue다.

## 전후 snapshot 체크리스트

### before checklist

- [ ] workspace 경로를 기록했다.
- [ ] baseline snapshot 시각을 기록했다.
- [ ] terminal write 명령 전체를 기록했다.
- [ ] pre-hook snapshot에서 `FINALIZE` / `idle` 여부를 기록했다.
- [ ] pre-hook snapshot에서 `current_plan_hash` 값 또는 부재를 기록했다.
- [ ] pre-hook snapshot에서 `last_terminal_status` 값 또는 부재를 기록했다.

### after checklist

- [ ] 다음 fresh session 시작 시각을 기록했다.
- [ ] post-sessionStart snapshot 시각을 기록했다.
- [ ] post-sessionStart snapshot에서 `INIT` / `active` 여부를 기록했다.
- [ ] stale continuity key 부재 여부를 기록했다.
- [ ] stale `current_plan_hash` 부재 여부를 기록했다.
- [ ] unintended `last_terminal_status` carry-over 부재 여부를 기록했다.
- [ ] `hydrated_from_previous_session` 부재 여부를 기록했다.

## 실행 절차

### 1. baseline snapshot 읽기

```powershell
Get-Content .copilot-memory\upgrade_state.json
```

baseline에서 중요한 점은 이후 관찰값과 혼동되지 않도록 시각과 핵심 필드를 먼저 적어 두는 것이다.

### 2. terminal write 실행

```powershell
python scripts/write_lifecycle_transition.py --workspace $Workspace --phase FINALIZE --status completed
```

기록 항목:

- 실행 시각
- 명령 전체 문자열
- 종료 코드

### 3. pre-hook snapshot 채집

```powershell
Get-Content .copilot-memory\upgrade_state.json
```

기록 항목:

- `current_phase=FINALIZE` 여부
- `status=idle` 여부
- `current_plan_hash`
- `active_task`
- `continuity.last_terminal_status`

### 4. 다음 fresh session 시작

operator action:

- 기존 세션을 닫는다.
- 같은 workspace에서 새 Copilot 세션을 시작한다.
- 자동 resume가 아니라 새 `sessionStart`가 실행되도록 한다.

기록 항목:

- 세션 시작 시각
- workspace가 동일한지 여부
- `AWAIT` resume로 들어가지 않았다는 확인 메모

### 5. post-sessionStart snapshot 채집

```powershell
Get-Content .copilot-memory\upgrade_state.json
```

기록 항목:

- `current_phase=INIT` 여부
- `status=active` 여부
- `current_plan_hash` 부재 또는 `null`
- `continuity.last_terminal_status` 부재
- `hydrated_from_previous_session` 부재
- stale continuity clue 부재

## 실패 분류 버킷

실패는 아래 버킷으로 분류한다.

| 버킷 | 의미 | 대표 징후 |
| --- | --- | --- |
| boundary-reset failure | fresh-session reset이 경계에서 실패 | `INIT` 이후에도 stale continuity key가 남음 |
| writer-normalization failure | terminal write가 남기면 안 되는 필드를 남김 | pre-hook snapshot에 불필요한 plan/continuity residue가 과다하게 존재 |
| unintended resume-path entry | 새 세션이 아니라 resume 경로로 들어감 | `hydrated_from_previous_session=true`, `await_context` 유지 |
| observation gap | 필요한 before/after snapshot이 빠짐 | pre-hook 또는 post-sessionStart 기록 부재 |
| environment contamination | 다른 workspace, 수동 편집, 손상된 state가 섞임 | `updated_at` 순서 불일치, workspace 혼선 |

## 판정 규칙

아래를 모두 만족하면 pass로 기록한다.

- post-sessionStart snapshot에서 stale continuity key가 없다.
- post-sessionStart snapshot에서 stale `current_plan_hash`가 없다.
- post-sessionStart snapshot에서 unintended `last_terminal_status` carry-over가 없다.

하나라도 만족하지 못하면 fail로 기록하고 위 버킷 중 하나 이상으로 분류한다.

## 간단 보고 템플릿

아래 템플릿은 현재 저장소의 lifecycle verification 보고 스타일에 맞춘 짧은 보고 형식이다.

```text
검증 대상: terminal -> next fresh session boundary
실행 일시: 2026-04-19T00:00:00Z
workspace: C:\Users\samkt\workplace\0_active_projects\Visual_Studio_Code\Prompt_Template

사전 상태 요약:
- pre-hook phase/status: FINALIZE / idle
- pre-hook current_plan_hash: null
- pre-hook last_terminal_status: completed

사후 상태 요약:
- post-sessionStart phase/status: INIT / active
- stale continuity key: absent
- stale current_plan_hash: absent
- unintended last_terminal_status carry-over: absent
- hydrated_from_previous_session: absent

판정: PASS
실패 분류: none
메모: terminal residue는 pre-hook에서만 관찰됐고 다음 fresh session continuity에는 남지 않았다.
```

## 운영 메모

- phase 값만 `INIT`라고 해서 pass 처리하지 않는다.
- before/after snapshot이 모두 없으면 검증이 아니라 진술에 그친다.
- `AWAIT` resume 예외는 control sample로는 유용하지만, 본 runbook의 pass/fail 판정 기준을 대신하지 않는다.
