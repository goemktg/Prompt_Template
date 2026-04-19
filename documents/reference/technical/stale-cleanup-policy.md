# stale-cleanup-policy

> 참고: 이 문서는 supporting reference다. terminal-boundary lifecycle operator의 canonical runbook은 `documents/reference/technical/terminal-boundary-live-verification-reference.md`를 우선 기준으로 사용한다.

## 목적

이 문서는 현재 저장소에서 실제로 구현된 stale cleanup 범위와 운영 절차를 짧게 고정한다. 기준은 `scripts/refresh_mcp_runtime.py`, `scripts/cleanup_runtime_artifacts.py`, `scripts/install_vscode_plugin.py`, `copilot/hooks.json`, `<workspace>/.copilot-memory/upgrade_state.json`이다.

## 현재 authoritative policy

현재 stale cleanup은 두 표면으로 나뉜다.

- process cleanup authoritative surface: `scripts/refresh_mcp_runtime.py`
- artifact cleanup authoritative surface: `scripts/cleanup_runtime_artifacts.py`

둘은 같은 상태 파일을 갱신할 수 있지만, 책임은 분리된다. process cleanup은 현재 plugin root에 속한 stale Python runtime process만 탐지·종료하고, artifact cleanup은 target workspace 안의 bounded marker JSON과 deploy-manifest 관리 대상 `.bak`만 정리한다.

다만 stale deployed file은 위 두 script만으로 다 끝나지 않는다. deploy-manifest가 추적하는 managed target subset에 대해서만 `scripts/upgrade_ai.py` sync 경로가 stale deployed file 삭제를 담당한다.

| stale 범주 | 현재 상태 | authoritative surface | 정책 메모 |
| --- | --- | --- | --- |
| stale MCP/runtime process | 구현됨 | `scripts/refresh_mcp_runtime.py` | 현재 plugin root와 target script 이름 세트가 함께 매치될 때만 정리 대상이다. |
| stale managed deployed file | 부분 구현 | `scripts/upgrade_ai.py`, `copilot/deploy-manifest.json` | 이전 deploy state와 현재 manifest target 차집합인 file target만 backup 후 삭제한다. |
| stale unmanaged deployed surface | 미구현 | 없음 | manifest 밖 파일, 임의 backup, runtime-owned surface 밖 복사본은 자동 cleanup 대상이 아니다. |
| stale session/compact/lifecycle marker JSON | 구현됨 | `scripts/cleanup_runtime_artifacts.py`, `copilot/hooks/scripts/session_end.py` | prefix와 디렉터리 범위가 고정된 bounded cleanup이다. |
| deploy-manifest 관리 대상 stale `.bak` 누적 | 구현됨 | `scripts/cleanup_runtime_artifacts.py`, `copilot/deploy-manifest.json` | managed target에서 나온 `.bak`만 age 기준으로 정리한다. |
| sync failure rollback cleanup | 미구현 | 없음 | rollback은 수동 운영 절차로만 다룬다. |

현재 process cleanup 대상 script 이름은 아래 세 개로 제한된다.

- `runtime_launcher.py`
- `workspace_sync_server.py`
- `start-memory.py`

또한 command line 안에 현재 plugin root가 포함되어야 매치된다. 즉, 다른 plugin copy나 무관한 Python process는 정리 대상이 아니다.

현재 artifact cleanup 범위도 의도적으로 좁다.

- marker JSON: `.copilot-memory/` 및 `.copilot-memory/runtime/` 아래에서 `session-`, `compact-`, `lifecycle-` prefix를 가진 `.json`
- backup file: `copilot/deploy-manifest.json`의 managed target에 대응되는 `.bak`
- 기본 stale 기준: marker 24시간, backup 7일
- 기본 보존 수: newest managed backup 0개

즉, 임의의 `.bak`, 임의의 JSON, deploy-manifest 밖 파일은 자동 정리 대상이 아니다.

또한 stale deployed files라는 표현은 아래 둘을 반드시 구분해서 써야 한다.

- managed stale deployed file: deploy-manifest가 추적한 과거 target이며 현재 sync 대상에서는 빠진 file
- unmanaged stale deployed surface: deploy-manifest와 무관한 잔여 파일, 수동 복사본, runtime-owned surface 밖 산재물

현재 자동 삭제가 가능한 것은 첫 번째뿐이다.

## 실행 정책

### 1. 기본 실행 순서

1. 먼저 dry-run으로 탐지 범위를 확인한다.
2. plugin registration 직후에는 `scripts/install_vscode_plugin.py`의 기본 refresh를 사용할 수 있다.
3. install/update 후 supplementary deploy가 필요하면 `copilot/scripts/workspace_sync_server.py` 또는 `scripts/upgrade_ai.py`를 실행한다.
4. sync 성공 시 deploy-manifest 기준 stale managed deployed file 정리는 sync 내부에서 처리된다.
5. stale process 정리가 여전히 필요하면 `scripts/refresh_mcp_runtime.py`를 직접 실행한다.
6. workspace artifact 정리가 필요하면 `scripts/cleanup_runtime_artifacts.py --workspace <path>`를 사용한다.
7. `sessionEnd` hook는 payload에 `workspacePath`가 있을 때 artifact cleanup을 non-dry-run으로 호출한다.
8. 실행 후 `<workspace>/.copilot-memory/upgrade_state.json`의 `runtime_state.last_runtime_refresh`, `runtime_state.last_runtime_cleanup`, `runtime_state.last_sync`를 확인한다.

권장 명령:

```powershell
python scripts/refresh_mcp_runtime.py --dry-run
python scripts/refresh_mcp_runtime.py
python scripts/cleanup_runtime_artifacts.py --workspace <workspace-path> --dry-run
python scripts/cleanup_runtime_artifacts.py --workspace <workspace-path>
```

workspace sync 확인이 필요하면 아래를 추가한다.

```powershell
python copilot/scripts/workspace_sync_server.py --self-check
python scripts/upgrade_ai.py <workspace-path>
```

### 2. 세션 경계 정책

| 판단 | 조건 | 정책 |
| --- | --- | --- |
| 새 세션 필요 | VS Code settings의 plugin/hook activation 값이 새로 추가되거나 변경됨 | settings는 installer가 쓸 수 있지만, session lifecycle 재진입과 hook 재적용은 새 세션 기준으로 검증한다. |
| 새 세션 필요 | `sessionStart` hydrate 또는 `AWAIT` resume를 실제로 확인해야 함 | hook 기반 continuity는 새 세션이 authoritative entrypoint다. |
| hot refresh 허용 | 이미 활성화된 plugin copy에서 stale process만 정리함 | process refresh는 현재 세션 안에서 best-effort로 수행 가능하다. |
| hot refresh 허용 | managed marker / managed backup cleanup만 수행함 | bounded artifact cleanup은 새 세션이 필수는 아니다. |
| 새 세션 권장 | refresh/sync 이후에도 증상이 남거나 live orchestration 연동 proof가 필요함 | 현재 저장소는 이 경로의 완전한 hot reload 보장을 주장하지 않는다. |

### 3. cleanup order

현재 정책상 cleanup 순서는 아래처럼 해석한다.

1. preflight: dry-run 또는 self-check
2. install/update settings 반영과 activation verification
3. workspace sync
4. sync 내부의 managed stale deployed file delete 확인
5. stale process refresh
6. managed marker / managed backup cleanup
7. 필요 시 새 세션 재진입

이 순서를 쓰는 이유는 stale deployed file 정리가 sync 내부 동작이기 때문이다. 별도의 global deployed-file cleaner가 있는 것이 아니다.

### 4. rollback notes

- `scripts/upgrade_ai.py`는 managed file overwrite/delete 전에 `.bak`를 남기지만, automatic rollback transaction은 제공하지 않는다.
- sync 실패 시 cleanup script를 연쇄적으로 더 실행해서 상태를 "맞추려" 하지 않는다. 먼저 partial deploy 범위를 확인하고 필요한 target만 `.bak` 기준 수동 복구한다.
- `scripts/refresh_mcp_runtime.py`는 process terminate만 수행하며 undo는 없다. 복구는 새 process 기동 또는 새 세션 재시작으로 본다.
- `scripts/cleanup_runtime_artifacts.py`는 stale marker와 오래된 managed backup을 삭제하므로, 삭제 후 rollback이 필요하면 외부 백업에 의존해야 한다.
- unmanaged deployed surface는 rollback도 cleanup도 자동화 범위 밖이다.

## 안전 규칙

- dry-run 없이 바로 terminate하지 않는다.
- 예외: installer 기본 경로는 registration 직후 stale process를 즉시 정리하는 best-effort 흐름이므로 `dry_run=False` refresh를 바로 호출한다.
- plugin root가 예상과 다르면 cleanup을 중단하고 `copilot/scripts/workspace_sync_server.py --self-check`로 root를 재확인한다.
- terminate 실패는 즉시 치명적 오류로 간주하지 않는다. 먼저 새 세션에서 stale 증상이 실제로 남는지 smoke로 확인한다.
- artifact cleanup은 managed scope에만 적용한다. fresh backup, unmanaged backup, prefix 밖 marker는 보존 대상이다.
- `sessionEnd` hook는 `workspacePath`가 있을 때만 artifact cleanup을 호출한다. workspace 정보가 없으면 skip하며 임시 디렉터리에 상태 파일을 쓰지 않는다.
- `sessionStart`와 `preCompact`는 continuity 기록 담당이고, process cleanup은 여전히 hook가 아니라 refresh script 책임이다.

## 검증 포인트

| 확인 항목 | 통과 기준 |
| --- | --- |
| 탐지 범위 | 매치 대상이 현재 plugin root와 target script 세트로 제한된다. |
| process 상태 기록 | non-dry-run refresh 후 `runtime_state.last_runtime_refresh`가 갱신된다. |
| artifact 상태 기록 | cleanup 실행 후 `runtime_state.last_runtime_cleanup`와 top-level `last_runtime_cleanup` mirror가 갱신된다. |
| hook 분기 | `sessionEnd`는 `workspacePath`가 있으면 cleanup을 실행하고, 없으면 skip한다. |
| 운영 후속 확인 | 필요 시 `python -m unittest discover -s tests -p "test_lifecycle_runtime_contract.py"`가 통과한다. |

## pending scope

아래 항목만 현재도 truly pending이다.

- sync 실패 후 자동 rollback cleanup
- managed marker/managed backup 밖 stale deployed surface 전반 자동 cleanup
- cross-workspace runtime cache 일괄 청소
