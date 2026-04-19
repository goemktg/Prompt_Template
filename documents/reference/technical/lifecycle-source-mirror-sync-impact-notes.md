# lifecycle-source-mirror-sync-impact-notes

## 목적

이 문서는 lifecycle wording 변경이 source-of-truth와 runtime mirror에 어떤 영향을 주는지 짧게 고정한다.

## 기본 모델

| 종류 | 현재 소유 경로 | mirror 여부 |
| --- | --- | --- |
| 전역 정책 | `shared/copilot-instructions.md` | `.github/copilot-instructions.md` mirror 존재 |
| instruction 자산 | `shared/instructions/*.instructions.md` | `.github/instructions/*.instructions.md` mirror 존재 |
| agent catalog | `AGENTS.md` | mirror 아님 |
| runtime config | `plugin.json`, `copilot/mcp.json`, `copilot/hooks.json` | mirror 아님 |
| 기술 문서 | `documents/reference/technical/*.md` | mirror 아님 |

## lifecycle 변경 시 영향 규칙

1. lifecycle 정책 문구를 바꾸면 먼저 source-of-truth를 수정한다.
2. 해당 자산이 mirror를 가지면 같은 변경 안에서 `.github` mirror도 갱신한다.
3. runtime config 파일에는 정책 문장을 복제하지 않고 identifier와 integration metadata만 둔다.
4. `documents/` 아래 기술 문서는 설명 문서이므로 mirror sync 대상이 아니다.

## 자주 헷갈리는 경우

| 변경 대상 | 필요한 sync |
| --- | --- |
| `shared/copilot-instructions.md`의 lifecycle wording | `.github/copilot-instructions.md` 갱신 필요 |
| `shared/instructions/*.instructions.md`의 lifecycle wording | 대응 `.github/instructions/*.instructions.md` 갱신 필요 |
| `AGENTS.md`의 lifecycle 설명 | `.github` mirror 갱신 불필요 |
| `plugin.json` 또는 `copilot/mcp.json`의 경로/manifest 변경 | source mirror sync 불필요 |
| `documents/reference/technical/*.md` 보완 | source mirror sync 불필요 |

## 운영 메모

- mirror는 runtime-visible copy이지 새로운 정책 작성 위치가 아니다.
- mirror가 stale해 보이면 mirror를 직접 고치기보다 upstream source를 먼저 확인한다.
- lifecycle refactor 중 wording을 넓히더라도 runtime config에 정책 설명을 복제하지 않는다.

## 관련 문서

- [runtime-path-contract.md](./runtime-path-contract.md)
- [orchestrator-responsibility-split-map.md](./orchestrator-responsibility-split-map.md)
