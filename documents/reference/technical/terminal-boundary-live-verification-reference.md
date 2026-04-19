# terminal-boundary-live-verification-reference

## 문서 역할

이 문서는 terminal write 이후 다음 fresh session 경계에서 stale continuity가 되살아나지 않는지 확인하는 **단일 canonical operator runbook**이다.

이 문서가 canonical인 이유는 다음과 같다.

- 현재 저장소에서 이 경계를 직접 다루는 운영 절차, 테스트 근거, smoke, 증거 채집 기준을 한곳에 합쳤다.
- 동일 주제를 분산 설명하던 supporting reference는 유지하되, 이 문서가 operator follow path의 source of truth가 된다.
- broader lifecycle acceptance 전체를 다시 설명하지 않고, terminal -> next fresh session boundary proof에만 집중한다.

## 현재 상태 요약

2026-04-19 기준 이 문서 갱신 과정에서 수행한 authoring-session spot-check와 코드/테스트 근거를 함께 요약하면 아래와 같다.

| 항목 | 현재 상태 | 근거 |
| --- | --- | --- |
| automated contract suite | spot-check pass | 이 문서 갱신 중 `python -m unittest discover -s tests -p "test_lifecycle_runtime_contract.py"`를 실행해 `Ran 41 tests ... OK`를 관찰 |
| stale runtime process smoke | spot-check pass | 이 문서 갱신 중 `python scripts/refresh_mcp_runtime.py --dry-run`를 실행해 `No stale runtime processes matched plugin root`를 관찰 |
| workspace sync root self-check | spot-check pass | 이 문서 갱신 중 `python copilot/scripts/workspace_sync_server.py --self-check`를 실행해 현재 repo root와 `scripts/upgrade_ai.py` resolution을 관찰 |
| terminal write normalization | 구현 및 테스트 고정 | `scripts/write_lifecycle_transition.py`, `tests/test_lifecycle_runtime_contract.py` |
| fresh-session reset after terminal state | 구현 및 테스트 고정 | `copilot/hooks/scripts/session_init.py`, `tests/test_lifecycle_runtime_contract.py` |
| actual next fresh Copilot session boundary proof | 아직 operator manual step 필요 | 실제 새 Copilot 세션 진입은 unittest만으로 완전 대체되지 않음 |

위 spot-check는 현재 저장소 상태를 읽기 위한 참고 근거일 뿐이며, reusable operator acceptance evidence를 대체하지 않는다. reusable boundary evidence는 아래 절차에 따라 별도 before/after snapshot으로 다시 남겨야 한다.

요약하면, **코드 계약과 단위 테스트는 충분히 갖춰져 있고 이번 문서 갱신 시점의 smoke spot-check도 통과했지만, terminal 이후 실제 다음 fresh session이 열릴 때 stale continuity가 남지 않는지에 대한 마지막 boundary proof는 여전히 operator가 새 세션을 직접 열어 before/after snapshot을 채집해야 한다.**

## authoritative sources

이 주제에서 authoritative로 취급하는 근거는 아래 순서다.

| 분류 | source | 이 문서에서의 역할 |
| --- | --- | --- |
| runtime writer | `scripts/write_lifecycle_transition.py` | terminal write가 state file에 무엇을 남기는지 정의 |
| sessionStart hook | `copilot/hooks/scripts/session_init.py` | non-`AWAIT` fresh session에서 continuity reset이 어떻게 일어나는지 정의 |
| sessionEnd hook | `copilot/hooks/scripts/session_end.py` | terminal 성격의 종료 state와 bounded cleanup trigger를 정의 |
| regression suite | `tests/test_lifecycle_runtime_contract.py` | writer/hook 계약이 실제로 regression-protected인지 증명 |
| supporting validation guide | `documents/reference/technical/lifecycle-validation-guide.md` | 현재 자동 검증 표면과 아직 manual인 면을 설명 |
| supporting evidence runbook | `documents/reference/technical/lifecycle-evidence-capture-runbook.md` | snapshot 채집 순서와 보고 형식을 보조 설명 |
| supporting refresh guide | `documents/reference/technical/runtime-refresh-runbook.md` | smoke와 refresh가 어디까지 보장하는지 설명 |
| supporting cleanup policy | `documents/reference/technical/stale-cleanup-policy.md` | stale process cleanup과 artifact cleanup 책임 분리를 설명 |

## 무엇이 증명됐고 무엇이 아직 수동인가

### 자동으로 증명된 것

아래 항목은 코드와 테스트로 현재 고정돼 있다.

| 항목 | 실제로 증명된 내용 | 근거 |
| --- | --- | --- |
| hook wiring | `sessionStart`, `sessionEnd`, `preCompact`가 예상 script와 연결됨 | `test_hook_manifest_references_expected_scripts` |
| terminal hook state | `sessionEnd` 이후 `current_phase=FINALIZE`, `status=idle`, `active_task=null`, `current_plan_hash=null` | session lifecycle test block |
| terminal writer normalization | `FINALIZE completed` write 시 `status=idle`, `active_task=null`, `current_plan_hash=null`, `continuity.last_terminal_status=completed` | `test_write_lifecycle_transition_finalize_clears_active_task` |
| non-terminal cleanup | `FINALIZE` 이후 다른 phase로 쓰면 `last_terminal_status`가 continuity에서 제거됨 | `test_write_lifecycle_transition_non_terminal_phase_clears_terminal_status` |
| fresh session reset | non-`AWAIT` 상태에서 `sessionStart`가 `INIT` / `active`로 덮어쓰고 stale `resume_token`, stale `current_plan_hash`, `hydrated_from_previous_session`, `last_terminal_status`를 제거함 | `test_session_start_overwrites_non_await_state_with_init`, `test_session_start_overwrites_finalized_state_with_init_and_clears_terminal_residue` |
| `AWAIT` 예외 경로 | `AWAIT` 상태에서는 resume continuity가 hydrate되며 fresh reset과 동일하게 취급하지 않음 | `test_session_start_hydrates_existing_await_state`, `test_write_lifecycle_transition_leaving_await_clears_resume_only_state` |

### 아직 operator manual verification이 필요한 것

아래 항목은 문서/코드상으로는 예상 동작이 명확하지만, 실제 다음 fresh Copilot session 경계에서는 operator 관찰이 필요하다.

| 항목 | 왜 수동인가 |
| --- | --- |
| terminal write 직후 실제 state residue 관찰 | 실제 operator terminal에서 write한 결과와 local state file snapshot을 직접 남겨야 한다. |
| 같은 workspace에서 다음 fresh Copilot session 진입 | unittest는 hook payload를 시뮬레이션하지만 실제 editor session boundary 자체를 대신하지 못한다. |
| 새 세션이 `AWAIT` resume가 아니라 truly fresh path였는지 확인 | 실제 UI/session flow는 operator가 확인해야 한다. |
| post-sessionStart snapshot 비교 | 다음 세션 시작 후 state file을 읽어 stale continuity residue 부재를 최종 판정해야 한다. |

## canonical boundary definition

이 문서에서 말하는 terminal -> next fresh session boundary는 다음 두 관찰 지점 사이를 뜻한다.

1. terminal write 또는 `FINALIZE` 완료 직후, 다음 세션이 아직 시작되지 않은 pre-hook 상태
2. 같은 workspace에서 완전히 새로운 다음 Copilot session이 시작되어 `sessionStart` hook가 실행된 직후 상태

핵심 계약은 아래 한 문장으로 요약된다.

```text
terminal residue may exist before the next session starts, but it must not survive into the next fresh session continuity.
```

## supporting documents와 역할 분리

아래 문서는 유지하지만, 이 주제의 canonical operator 절차는 이 문서 하나로 본다.

| 문서 | 유지 여부 | 역할 |
| --- | --- | --- |
| `documents/reference/technical/terminal-boundary-live-verification-reference.md` | 유지 | **canonical operator runbook** |
| `documents/reference/technical/lifecycle-evidence-capture-runbook.md` | 유지 | supporting evidence template과 기록 포맷 reference |
| `documents/reference/technical/lifecycle-validation-guide.md` | 유지 | 자동 검증 표면과 한계 reference |
| `documents/reference/technical/runtime-refresh-runbook.md` | 유지 | preflight/smoke 및 runtime refresh 범위 reference |
| `documents/reference/technical/stale-cleanup-policy.md` | 유지 | stale cleanup 책임 분리 reference |

즉, operator는 이 문서를 따라 검증하고, 필요할 때만 supporting reference를 펼쳐 보면 된다.

## exact operator verification procedure

아래 절차는 terminal write부터 다음 fresh session boundary까지 operator가 그대로 따라야 하는 canonical 절차다.

### 1. workspace 경로 고정

```powershell
$Workspace = "C:\Users\samkt\workplace\0_active_projects\Visual_Studio_Code\Prompt_Template"
Set-Location $Workspace
```

### 2. optional preflight smoke 실행

이 단계는 boundary proof 자체는 아니지만, 현재 machine의 root resolution과 stale process surface를 먼저 확인하는 데 유용하다.

```powershell
python -m unittest discover -s tests -p "test_lifecycle_runtime_contract.py"
python scripts/refresh_mcp_runtime.py --dry-run
python copilot/scripts/workspace_sync_server.py --self-check
```

이 문서 갱신 시점 spot-check에서 관찰한 결과는 아래와 같다. 이 블록은 reusable operator evidence가 아니라, 현재 runbook 내용이 코드/환경과 모순되지 않는지 확인한 authoring note다.

- unittest: `Ran 41 tests ... OK`
- refresh dry-run: `No stale runtime processes matched plugin root`
- self-check: 현재 repo root와 `scripts/upgrade_ai.py`를 정확히 보고

### 3. baseline snapshot을 읽는다

```powershell
Get-Content .copilot-memory\upgrade_state.json
```

기록할 최소 항목은 아래와 같다.

- `lifecycle_state.current_phase`
- `lifecycle_state.status`
- `lifecycle_state.current_plan_hash`
- `lifecycle_state.active_task`
- `lifecycle_state.continuity.last_terminal_status`
- `lifecycle_state.await_context`
- `lifecycle_state.updated_at`

### 4. terminal state를 명시적으로 쓴다

canonical write command는 아래다.

```powershell
python scripts/write_lifecycle_transition.py --workspace $Workspace --phase FINALIZE --status completed
```

이 command가 현재 코드상에서 보장하는 내용은 다음과 같다.

- `current_phase=FINALIZE`
- `status=idle`
- `active_task=null`
- `current_plan_hash=null`
- `continuity.last_terminal_status=completed`
- 기존 `continuity.next_transition` 제거

### 5. pre-hook snapshot을 저장한다

```powershell
Get-Content .copilot-memory\upgrade_state.json
```

이 snapshot은 **다음 세션이 시작되기 전** 상태여야 한다. 이 시점에는 terminal residue가 잠시 존재해도 된다.

기록할 핵심 판정값:

- `current_phase=FINALIZE` 여부
- `status=idle` 여부
- `current_plan_hash`가 `null` 또는 부재인지
- `active_task`가 `null` 또는 부재인지
- `continuity.last_terminal_status=completed`가 남아 있는지
- `updated_at` 시각

### 6. 같은 workspace에서 다음 fresh session을 시작한다

이 단계는 현재도 manual이다.

operator action:

- 기존 Copilot session을 종료한다.
- 같은 workspace에서 새 Copilot session을 시작한다.
- 자동 `AWAIT` resume가 아니라 **fresh session**으로 들어가도록 한다.

주의 사항:

- 이 단계에서 `AWAIT` resume로 들어가면 본 검증은 invalid다.
- 같은 workspace state file을 사용하는 세션이어야 한다.
- 다른 workspace 또는 수동 state 편집이 섞이면 증거력이 떨어진다.

### 7. post-sessionStart snapshot을 다시 읽는다

```powershell
Get-Content .copilot-memory\upgrade_state.json
```

다음 항목을 확인한다.

- `current_phase=INIT`
- `status=active`
- `current_plan_hash` 부재 또는 `null`
- `lifecycle_state.continuity.last_terminal_status` 부재
- `lifecycle_state.continuity.hydrated_from_previous_session` 부재
- `lifecycle_state.continuity.resume_token` 부재
- `lifecycle_state.continuity.next_transition` 부재
- 기타 stale continuity clue 부재

### 8. pass/fail을 판정한다

아래 세 조건을 모두 만족하면 pass다.

1. 다음 fresh session snapshot에 stale continuity key가 없다.
2. 다음 fresh session snapshot에 stale `current_plan_hash`가 없다.
3. terminal 단계에서 잠시 존재했을 수 있는 `last_terminal_status`가 다음 fresh session continuity로 carry-over되지 않는다.

## pass/fail criteria

### pass

아래 조건을 모두 만족하면 pass다.

| 확인 항목 | pass 기준 |
| --- | --- |
| pre-hook terminal write | `FINALIZE` / `idle`가 관찰된다. |
| pre-hook residue scope | `active_task`와 `current_plan_hash`는 정리되고, `last_terminal_status`만 terminal marker로 남을 수 있다. |
| next fresh session phase | `INIT` / `active`가 관찰된다. |
| stale continuity key | `lifecycle_state.await_context`, `lifecycle_state.continuity.resume_token`, `lifecycle_state.continuity.next_transition`, `lifecycle_state.continuity.hydrated_from_previous_session`가 없다. |
| stale plan linkage | stale `current_plan_hash`가 없다. |
| terminal carry-over | `continuity.last_terminal_status`가 없다. |

권장 기록 문구:

```text
PASS: pre-hook에서는 FINALIZE / idle 및 terminal residue가 관찰됐고, 다음 fresh session에서는 INIT / active로 reset되며 stale continuity key, stale current_plan_hash, unintended last_terminal_status carry-over가 모두 부재했다.
```

### fail

아래 중 하나라도 관찰되면 fail이다.

- 다음 fresh session state에 `resume_token`, `await_context`, `continuity.next_transition`, `hydrated_from_previous_session` 같은 stale resume clue가 남아 있다.
- 다음 fresh session state에 stale `current_plan_hash`가 남아 있다.
- 다음 fresh session state에 `continuity.last_terminal_status`가 그대로 남아 있다.
- phase가 `INIT`로 보이더라도 continuity payload가 이전 세션을 암시한다.
- operator가 실제로 fresh session이 아닌 `AWAIT` resume path로 들어갔다.

권장 기록 문구:

```text
FAIL: next fresh session snapshot에서 reset 이후 없어야 할 continuity residue가 관찰됐다. phase 값만으로 pass 처리하지 않는다.
```

## diagnostics와 smoke commands

권장 smoke는 아래 세 가지다.

```powershell
python -m unittest discover -s tests -p "test_lifecycle_runtime_contract.py"
python scripts/refresh_mcp_runtime.py --dry-run
python copilot/scripts/workspace_sync_server.py --self-check
```

해석 규칙은 아래와 같다.

| 명령 | 통과 시 의미 | 주의점 |
| --- | --- | --- |
| unittest | hook wiring, writer normalization, session reset contract가 regression-protected 상태임을 뜻함 | 실제 editor boundary 자체를 대신하지는 않음 |
| `refresh_mcp_runtime.py --dry-run` | 현재 plugin root 기준 stale runtime process 탐지 범위를 확인 | process clean이라는 뜻이지 fresh-session proof라는 뜻은 아님 |
| `workspace_sync_server.py --self-check` | 현재 repo root, marker, `upgrade_script` resolution이 올바름을 확인 | sync wiring 확인이지 boundary pass/fail 자체는 아님 |

추가 진단 포인트:

- `sessionEnd` hook는 `FINALIZE` / `idle` state와 bounded artifact cleanup trigger를 담당한다.
- `sessionStart` hook는 non-`AWAIT` fresh path에서 continuity를 reset한다.
- `AWAIT` 상태는 예외 경로이므로, boundary smoke에서 fresh path와 섞어 해석하면 안 된다.

## evidence capture guidance

증거는 최소한 아래 순서로 남긴다.

1. baseline snapshot
2. terminal write command 문자열과 실행 시각
3. pre-hook snapshot
4. next fresh session 시작 시각과 operator note
5. post-sessionStart snapshot
6. pass/fail 판정 메모

권장 저장 위치는 아래와 같다.

- 요약 보고: `documents/drafts/<date>-terminal-boundary-evidence.md`
- 구조화 로그: `results/lifecycle/<timestamp>_terminal-boundary.json`

`results/lifecycle/`가 없으면 operator가 먼저 디렉터리를 만든 뒤 저장한다. 간단한 1회 검증이면 `documents/drafts/<date>-terminal-boundary-evidence.md`만 사용해도 된다.

각 snapshot마다 기록할 최소 필드는 아래와 같다.

- `lifecycle_state.current_phase`
- `lifecycle_state.status`
- `lifecycle_state.current_plan_hash`
- `lifecycle_state.active_task`
- `lifecycle_state.continuity.last_terminal_status`
- `lifecycle_state.await_context`
- `lifecycle_state.continuity.hydrated_from_previous_session`
- `lifecycle_state.updated_at`

보고 메모 예시는 아래 형식을 쓴다.

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

## failure buckets

| 버킷 | 의미 | 대표 징후 |
| --- | --- | --- |
| boundary-reset failure | fresh-session reset이 경계에서 실패 | `INIT` 이후에도 stale continuity key가 남음 |
| writer-normalization failure | terminal write가 남기면 안 되는 필드를 남김 | pre-hook snapshot에 불필요한 stale plan/continuity residue가 과다하게 존재 |
| unintended resume-path entry | 새 세션이 아니라 resume 경로로 들어감 | `hydrated_from_previous_session=true`, `await_context` 유지 |
| observation gap | 필요한 before/after snapshot이 빠짐 | pre-hook 또는 post-sessionStart 기록 부재 |
| environment contamination | 다른 workspace, 수동 편집, 손상된 state가 섞임 | `updated_at` 순서 불일치, workspace 혼선 |

## cleanup proposal for duplicate or stale docs

아래 정리안은 **제안만** 하며, 이번 변경에서는 적용하지 않는다.

| 대상 | 현재 판단 | 제안 |
| --- | --- | --- |
| `documents/reference/technical/lifecycle-evidence-capture-runbook.md` | 본 주제와 높은 중복이 있으나 증거 템플릿 가치가 있음 | 유지하되, 후속 변경에서 "supporting reference" 배너를 상단에 추가하고 operator step은 이 canonical 문서로 링크하도록 축약 |
| `documents/reference/technical/lifecycle-validation-guide.md` | 중복이 아니라 validation surface 설명 문서 | 유지 |
| `documents/reference/technical/runtime-refresh-runbook.md` | preflight/smoke 문서로 유효 | 유지 |
| `documents/reference/technical/stale-cleanup-policy.md` | cleanup scope policy 문서로 유효 | 유지 |
| `documents/drafts/temple-run-analysis.md` | 이 주제의 canonical 문서가 아님 | 이 boundary 주제와 무관하거나 historical draft라면 archive 또는 explicit non-canonical 표시 검토 |
| `documents/drafts/temple-run-adoption-blueprint-final.md` | 이 주제의 canonical 문서가 아님 | 이 boundary 주제와 무관하거나 historical draft라면 archive 또는 explicit non-canonical 표시 검토 |

## operator notes

- phase 값만 `INIT`라고 해서 pass 처리하지 않는다.
- `AWAIT` resume 예외는 control sample로는 유용하지만, fresh-session boundary pass/fail을 대신하지 않는다.
- refresh나 self-check가 통과해도 실제 next fresh session snapshot 비교가 빠지면 boundary proof는 완료되지 않는다.
