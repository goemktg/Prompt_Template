# runtime-refresh-runbook

> 참고: 이 문서는 supporting reference다. terminal-boundary lifecycle operator의 canonical runbook은 `documents/reference/technical/terminal-boundary-live-verification-reference.md`를 우선 기준으로 사용한다.

## 목적

이 문서는 현재 구현된 stale runtime refresh 흐름과, 아직 의도적으로 자동화하지 않은 범위를 구분해 운영자가 빠르게 판단할 수 있게 만드는 runbook이다.

특히 WS2에서 남아 있던 세 가지 판단 기준을 현재 저장소 기준으로 명시한다.

- 어떤 표면을 stale surface로 보며 무엇이 자동 처리 범위인지
- install/update 직후 어떤 refresh 단계를 밟아야 하는지
- 언제 hot refresh로 충분하고, 언제 새 세션이 필요한지

## 현재 runtime 표면 범위

먼저 구분할 점은, refresh는 process/runtime 정리 담당이고 artifact cleanup은 별도 script와 `sessionEnd` hook가 담당한다는 것이다. 아래 목록은 현재 stale runtime refresh와 인접한 운영 표면을 함께 보여준다.

- stale Python runtime process 탐지 및 종료: `scripts/refresh_mcp_runtime.py`
- installer 이후 best-effort refresh: `scripts/install_vscode_plugin.py`
- refresh 결과 기록: `.copilot-memory/upgrade_state.json`의 `runtime_state.last_runtime_refresh`
- bounded stale marker / managed `.bak` cleanup: `scripts/cleanup_runtime_artifacts.py`
- artifact cleanup 결과 기록: `.copilot-memory/upgrade_state.json`의 `runtime_state.last_runtime_cleanup`
- session continuity marker 기록 및 `sessionEnd` cleanup trigger: `copilot/hooks/scripts/session_init.py`, `copilot/hooks/scripts/session_end.py`, `copilot/hooks/pre-compact.py`
- workspace sync 결과 기록: `copilot/scripts/workspace_sync_server.py`

현재 refresh는 plugin copy 기준 stale process 정리에 집중한다. 반면 artifact cleanup은 target workspace 기준 stale marker JSON과 managed `.bak` 정리에 집중한다.

## stale surface 범주

현재 저장소에서 stale surface는 아래처럼 다섯 범주로 나눠서 보는 것이 가장 정확하다.

| 범주 | 대표 표면 | 현재 처리 상태 | 운영 메모 |
| --- | --- | --- | --- |
| stale MCP/runtime process | `runtime_launcher.py`, `workspace_sync_server.py`, `start-memory.py`를 실행 중인 Python process | 구현됨 | 현재 plugin root가 command line에 포함된 process만 매치한다. |
| stale managed deployed file | `copilot/deploy-manifest.json`에 의해 이전 run에는 배포됐지만 현재 manifest target 집합에서는 빠진 file target | 부분 구현 | `scripts/upgrade_ai.py` sync 중 backup 후 삭제한다. 별도 전면 sweep는 없다. |
| stale unmanaged deployed surface | deploy-manifest 밖 파일, runtime-owned surface 밖 복사본, 임의 디렉터리 누적물 | 미구현 | 자동 cleanup 대상으로 주장하면 안 된다. 현재는 운영자 수동 판단 영역이다. |
| stale session/compact/lifecycle marker | `.copilot-memory/`, `.copilot-memory/runtime/` 아래 `session-`, `compact-`, `lifecycle-` prefix `.json` | 구현됨 | `scripts/cleanup_runtime_artifacts.py`와 `sessionEnd` hook가 bounded cleanup한다. |
| managed backup accumulation | deploy-manifest 관리 대상 target에 대응되는 `.bak` | 구현됨 | 오래된 managed backup만 age 기준으로 정리한다. |

핵심은 stale deployed surface 전체가 자동 정리되는 것이 아니라, deploy-manifest가 추적하는 managed target subset만 sync 과정에서 삭제까지 다룬다는 점이다.

## 표준 흐름

1. install/update 진입점에서는 `scripts/install_vscode_plugin.py`가 VS Code settings를 갱신한다.
2. installer는 `--no-refresh-runtime`가 아니면 stale runtime refresh를 best-effort로 수행한다.
3. installer는 이어서 `scripts/verify_runtime_activation.py`로 plugin root, hook manifest, custom hook activation 설정이 반영됐는지 검사한다.
4. workspace supplementary deploy가 필요하면 `copilot/scripts/workspace_sync_server.py` 또는 `scripts/upgrade_ai.py`가 deploy-manifest 기준 sync를 수행한다.
5. sync 중 manifest 기준으로 stale managed deployed file이 감지되면 `.bak`를 남긴 뒤 삭제한다.
6. 별도 artifact cleanup이 필요하면 `scripts/cleanup_runtime_artifacts.py --workspace <path>` 또는 `sessionEnd` hook를 사용한다.
7. 새 세션이 시작되면 `sessionStart` hook가 continuity와 `AWAIT` hydrate를 다시 기록한다.

즉, install/update 이후의 refresh는 settings 반영, stale process 정리, activation verification, workspace sync, bounded artifact cleanup, session lifecycle 재시작 여부 판단의 순서로 이해하는 편이 현재 구현과 가장 가깝다.

## 새 세션 필요 여부

현재 구현 기준으로는 아래 구분이 가장 안전하다.

| 판단 | 적용 조건 | 이유 |
| --- | --- | --- |
| 새 세션 필요 | `scripts/install_vscode_plugin.py`가 `chat.pluginLocations`, `chat.hookFilesLocations`, `chat.plugins.enabled`, `chat.useCustomAgentHooks`를 새로 쓰거나 바꾼 직후 | 설정 반영과 hook/session lifecycle 재진입은 현재 세션 안에서 완전히 증명된 hot reload contract가 아니다. |
| 새 세션 필요 | `sessionStart` hydrate, `AWAIT` resume, hook wiring 재검증이 목적일 때 | 이 동작은 session lifecycle 이벤트에 의존하므로 새 세션이 authoritative 재진입 지점이다. |
| 새 세션 권장 | refresh 이후에도 stale 증상, sync gate failure, live orchestrator 연동 이상이 남을 때 | 현재 저장소는 live subagent execution path의 end-to-end proof가 아직 부족하다. |
| hot refresh 허용 | plugin registration과 hook activation 상태가 이미 current이고, 목표가 stale Python runtime process 종료뿐일 때 | `scripts/refresh_mcp_runtime.py`는 process slice만 다루며 현재 세션 전체 재기동을 전제하지 않는다. |
| hot refresh 허용 | workspace supplementary deploy sync 후, session lifecycle 재진입 없이 파일 반영과 self-check만 확인하면 충분할 때 | `scripts/upgrade_ai.py`와 `workspace_sync_server.py`는 file sync와 state 기록을 담당한다. |
| hot refresh 허용 | managed marker JSON / managed `.bak` cleanup만 추가로 실행할 때 | `scripts/cleanup_runtime_artifacts.py`는 bounded file cleanup이며 sessionStart 재호출이 필수는 아니다. |

여기서 hot refresh 허용은 "동작할 수 있음"이지 "새 세션과 동등하게 보장됨"을 뜻하지 않는다. session lifecycle 재진입이 목적이면 새 세션을 기준으로 삼는다.

## hook/session 상호작용

- `sessionStart`: `INIT`, `active`, `last_event=sessionStart` 기록
- `preCompact`: `compact_safe=true`, `last_compaction_checkpoint=true` 기록
- `sessionEnd`: `FINALIZE`, `idle`, `last_event=sessionEnd`를 기록하고, payload에 `workspacePath`가 있으면 artifact cleanup도 호출
- refresh script는 hook 상태를 직접 만지지 않는다. process refresh, artifact cleanup, continuity hook는 같은 상태 파일을 쓸 수 있지만 책임이 다르다.

정리하면, refresh는 process/runtime 정리 담당이고, `sessionEnd`는 continuity 기록에 더해 workspace-scoped artifact cleanup을 트리거할 수 있다.

## cleanup 순서와 rollback 메모

현재 구현 기준 운영 순서는 아래처럼 보수적으로 잡는다.

1. `--dry-run` 또는 `--self-check`로 현재 root와 대상 범위를 먼저 확인한다.
2. install/update 경로라면 settings 반영과 activation verification을 먼저 끝낸다.
3. workspace sync가 필요하면 `workspace_sync_server.py` 또는 `upgrade_ai.py`를 실행한다.
4. sync가 성공한 뒤에만 결과 state와 deploy-manifest 기준 stale managed target 삭제 여부를 확인한다.
5. stale process가 남았거나 installer refresh를 건너뛰었다면 `refresh_mcp_runtime.py`를 실행한다.
6. 마지막에 managed marker JSON과 managed `.bak` 정리가 필요할 때만 `cleanup_runtime_artifacts.py`를 실행한다.
7. hook 재진입 또는 `AWAIT` hydrate 확인이 필요하면 새 세션으로 마무리한다.

rollback 메모도 좁게 이해해야 한다.

- managed deploy target overwrite/delete에는 `.bak`가 남지만 transaction rollback은 없다.
- sync 실패 시 자동 rollback은 없다. partial sync 또는 partial delete가 의심되면 즉시 중단하고 `.bak`와 manifest target 목록을 기준으로 수동 복구한다.
- process refresh에는 rollback 개념이 사실상 없고, 필요하면 새 runtime process를 다시 시작하는 방식으로만 복구한다.
- marker cleanup은 stale marker 삭제이므로, 삭제 후 되돌리려면 별도 백업이나 외부 복사본이 필요하다.

## 의도적으로 아직 안 하는 것

- sync 실패 시 자동 rollback
- managed marker/managed `.bak` 밖 stale deployed surface 전반 자동 cleanup
- hook 미실행 환경에 대한 별도 대체 trigger 강제
- cross-workspace runtime cache 일괄 청소

이 영역은 아직 운영 판단 또는 후속 구현 항목으로 남아 있다.

## 실패 playbook

### 1. refresh 명령 자체가 실패함

- `python scripts/refresh_mcp_runtime.py --dry-run`으로 먼저 root resolution이 되는지 본다.
- PowerShell process query 오류면 Windows 권한 또는 shell availability를 확인한다.
- plugin root가 이상하면 `runtime-path-contract.md` 기준으로 marker와 settings 등록 상태를 점검한다.

### 2. matched는 되는데 terminate가 실패함

- 출력의 `pid`와 `error`를 확인한다.
- 동일 PID가 이미 종료된 race인지, 권한 문제인지 구분한다.
- 즉시 치명적 실패로 보지 말고 새 세션에서 실제 stale 증상이 남는지 smoke를 다시 돈다.

### 3. refresh 후에도 sync 또는 memory runtime이 이상함

- `python copilot/scripts/workspace_sync_server.py --self-check`로 현재 root와 `upgrade_script`를 본다.
- `.copilot-memory/upgrade_state.json`에서 `runtime_state.last_runtime_refresh`와 `runtime_state.last_sync`가 최신으로 갱신됐는지 확인한다.
- 새 VS Code session을 열어 hook 기반 continuity가 다시 기록되는지 본다.

## smoke steps

```powershell
python scripts/refresh_mcp_runtime.py --dry-run
python copilot/scripts/workspace_sync_server.py --self-check
python -m unittest discover -s tests -p "test_lifecycle_runtime_contract.py"
```

통과 기준:

- refresh dry-run이 실패하지 않는다.
- self-check가 현재 `repo_root`와 `scripts/upgrade_ai.py`를 가리킨다.
- unittest가 hook wiring, state persistence, thin orchestrator contract를 통과한다.

## 운영 메모

- refresh는 best-effort다. 일부 process terminate 실패가 곧바로 lifecycle failure를 뜻하지는 않는다.
- authoritative 확인 지점은 상태 파일과 smoke 결과다.
- 수동 점검 시에는 stale process 정리와 state continuity 기록을 분리해서 판단하는 편이 안전하다.
