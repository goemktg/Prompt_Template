# runtime-path-contract

## 목적

이 문서는 현재 저장소에서 plugin root를 어떻게 찾고, 그 root를 기준으로 MCP runtime과 installer가 어떤 표면을 해석하는지 빠르게 확인하기 위한 운영 참조다. 기준 구현은 `copilot/scripts/runtime_root.py`와 이를 호출하는 launcher, installer, sync wrapper다.

## 공통 계약

- authoritative plugin root는 `plugin.json`을 포함한 저장소 root다.
- 기본 lookup marker는 `plugin.json`과 `copilot/mcp.json`이다.
- workspace sync는 추가로 `scripts/upgrade_ai.py`까지 포함한 marker set을 사용해 sync 가능한 root만 허용한다.
- lookup 순서는 `start_path` 상향 탐색, VS Code `chat.pluginLocations`, VS Code `agentPlugins` bounded walk 순이다.
- JSONC settings는 comment 제거와 trailing comma 정리 후 읽는다.

## 표면별 해석 매트릭스

| 표면 | 시작점 | required marker | lookup 결과 사용처 |
| --- | --- | --- | --- |
| `plugin.json` | none | none | runtime assets 경로 선언: `copilot/hooks.json`, `copilot/mcp.json` |
| `copilot/mcp.json` | MCP process cwd | `plugin.json`, `copilot/mcp.json` | inline bootstrap가 `runtime_launcher.py`까지 진입할 root 결정 |
| `copilot/scripts/runtime_root.py` | caller 제공 `start_path` 또는 cwd | caller-defined | 공통 root resolution 유틸 |
| `copilot/scripts/runtime_launcher.py` | launcher 파일 위치 | `plugin.json`, `copilot/mcp.json` | memory server, workspace-sync server 실행 |
| `scripts/install_vscode_plugin.py` | 저장소 root | `plugin.json`, `copilot/mcp.json` | VS Code settings 등록, hook manifest 등록, stale runtime refresh |
| `copilot/scripts/workspace_sync_server.py` | wrapper 파일 위치 | `plugin.json`, `copilot/mcp.json`, `scripts/upgrade_ai.py` | sync 대상 workspace에 대해 `scripts/upgrade_ai.py` 실행 |

## source/workspace/plugin copy/settings 관점 요약

- source checkout: 저장소 내부에서 실행하면 상향 탐색만으로 root를 찾는 것이 우선 경로다.
- workspace target: `workspace_sync_server.py`는 현재 plugin root를 찾은 뒤, 별도 target workspace를 받아 `scripts/upgrade_ai.py`를 실행한다. target workspace가 plugin root일 필요는 없다.
- plugin copy: 현재 cwd가 plugin copy 내부가 아니어도 VS Code settings의 `chat.pluginLocations`와 `globalStorage/.../agentPlugins` 하위 bounded walk를 통해 root를 찾는다.
- settings lookup: `settings.json`은 Windows `APPDATA`, macOS `~/Library/Application Support`, Linux `~/.config` 순회 대상이다. `chat.pluginLocations` 값은 `dict`, `list`, `string`을 모두 허용한다.
- home-based plugin dirs: `globalStorage` 경로에 추가로 `~/.vscode/agent-plugins`와 `~/.vscode-insiders/agent-plugins`도 모든 플랫폼 공통으로 `agentPlugins` 탐색 대상에 포함된다 (상수 `VSCODE_HOME_PLUGIN_DIRS`). VS Code 설치 위치에 무관하게 user-home 기반 설치를 지원한다.

## 현재 동작 포인트

- `plugin.json`은 runtime manifest 진입점만 선언한다. 실제 root discovery는 하지 않는다.
- `runtime_launcher.py`는 mode별 실행만 담당하고, root discovery 자체는 `find_plugin_root()`에 위임한다.
- `install_vscode_plugin.py`는 VS Code settings에 plugin root와 `copilot/hooks.json`을 등록하고, 필요 시 `refresh_mcp_runtime.py`를 호출해 stale process를 내린다.
- `workspace_sync_server.py`는 self-check와 sync wrapper 역할만 하며, sync 결과를 `.copilot-memory/upgrade_state.json`에 기록한다.

## 운영 규칙

- 신규 runtime 표면이 plugin root를 직접 추론해야 한다면 `runtime_root.py`를 재사용한다.
- root lookup 실패 메시지는 start path 기준 실패로 보고되므로, 첫 확인 대상은 marker 파일 존재 여부다.
- sync wrapper처럼 추가 marker가 필요한 표면은 required marker를 늘릴 수 있지만, 기본 계약인 `plugin.json`과 `copilot/mcp.json`은 유지해야 한다.

## 빠른 확인

```powershell
python scripts/install_vscode_plugin.py --dry-run --settings-file C:\path\to\settings.json --no-refresh-runtime
python copilot/scripts/workspace_sync_server.py --self-check
```

위 두 명령이 각각 settings 등록 대상과 `repo_root`/`upgrade_script`를 올바르게 보여주면 현재 path contract는 대체로 정상이다.
