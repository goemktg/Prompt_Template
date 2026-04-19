# bootstrap-duplication-debt-and-recovery

## 목적

이 문서는 `copilot/mcp.json` bootstrap snippet 중복 상태를 accepted debt로 기록하고, path resolution 또는 activation 실패 시 표준 recovery 메시지를 짧게 고정한다.

## duplication status

현재 `copilot/mcp.json`의 `memory`와 `workspace-sync`는 거의 같은 inline bootstrap을 각각 가진다.

| 항목 | 현재 상태 | 판정 |
| --- | --- | --- |
| root discovery 코드 | 두 server entry에 중복 존재 | accepted debt |
| settings lookup 코드 | 두 server entry에 중복 존재 | accepted debt |
| bounded walk / marker 검사 | 두 server entry에 중복 존재 | accepted debt |

현재는 아래 이유로 즉시 제거하지 않는다.

1. MCP manifest 안에서 각 server가 독립적으로 self-bootstrap해야 한다.
2. 현재 테스트와 운영 문서는 이 중복 구조를 전제로 이미 안정화돼 있다.
3. 남은 우선순위는 duplication 제거보다 live proof와 운영 검증 보강이다.

## 지금 닫을 수 있는 결정

- 중복은 존재한다.
- 중복 축소의 구현은 아직 하지 않았다.
- 대신 중복 축소 방안은 "공통 launcher helper로 외부화하되 `copilot/mcp.json` entry contract를 유지한다"는 수준으로 설계만 기록한다.

## 축소 방안 스케치

1. root discovery를 외부 helper 또는 launcher mode로 더 밀어 넣는다.
2. `copilot/mcp.json`은 최소 command/args만 유지한다.
3. 다만 manifest portability와 copied plugin tree 동작을 깨지 않는 회귀 증거가 있을 때만 적용한다.

현재는 설계 기록만 종료 조건으로 삼고, 구현 태스크는 별도로 보류한다.

## recovery messaging

### 1. root resolution 실패

증상:

```text
Unable to resolve plugin root
```

우선 확인:

1. `plugin.json`이 있는 root에서 실행 중인지 확인한다.
2. `copilot/mcp.json`, `copilot/scripts/runtime_launcher.py`가 실제로 존재하는지 확인한다.
3. VS Code `settings.json`의 `chat.pluginLocations`가 현재 plugin copy를 가리키는지 확인한다.

### 2. post-install activation 실패

증상:

```text
post-install verification missing activation state
post-install verification failed
```

우선 확인:

1. `chat.pluginLocations`에 현재 plugin root가 들어 있는지 확인한다.
2. `chat.hookFilesLocations`에 `copilot/hooks.json` 절대 경로가 들어 있는지 확인한다.
3. `chat.plugins.enabled=true`, `chat.useCustomAgentHooks=true`인지 확인한다.
4. 필요하면 `python scripts/install_vscode_plugin.py --settings-file <path>`를 다시 실행한다.

### 3. refresh 경로 점검

```powershell
python scripts/refresh_mcp_runtime.py --dry-run
python copilot/scripts/workspace_sync_server.py --self-check
```

위 두 명령이 실패하지 않으면 root discovery와 runtime visibility는 대체로 정상으로 본다.

## 관련 문서

- [install-update-entrypoint-decision.md](./install-update-entrypoint-decision.md)
- [runtime-refresh-runbook.md](./runtime-refresh-runbook.md)
- [lifecycle-acceptance-checklist.md](./lifecycle-acceptance-checklist.md)
