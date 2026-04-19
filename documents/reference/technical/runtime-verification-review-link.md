# runtime-verification-review-link

## 목적

이 문서는 runtime verification checklist와 documentation review checklist를 한 번에 묶어, lifecycle 관련 문서를 갱신할 때 무엇을 같이 확인해야 하는지 고정한다.

## 두 체크리스트의 역할

| 체크리스트 | 목적 |
| --- | --- |
| runtime verification | 문서가 설명하는 runtime 표면과 명령이 실제 구현과 맞는지 확인 |
| documentation review | 문서가 과장 없이 읽히고 링크, 용어, pending scope가 정확한지 확인 |

## 연결 규칙

1. lifecycle 문서가 runtime command를 언급하면 최소 하나의 verification 근거를 함께 적는다.
2. verification이 unittest인지, dry-run인지, self-check인지 문서에서 명시한다.
3. 문서 review는 "정확성" 항목에서 pending scope를 완료처럼 쓰지 않았는지 확인한다.
4. live integration 증거가 없으면 doc-review 단계에서 반드시 pending으로 남긴다.

## 실무용 묶음 절차

### 1. runtime 확인

- [lifecycle-acceptance-checklist.md](./lifecycle-acceptance-checklist.md)의 관련 명령을 확인한다.
- [lifecycle-validation-matrix.md](./lifecycle-validation-matrix.md)에서 자동 검증인지 수동 확인인지 구분한다.

### 2. documentation review 확인

- 명령 예제가 실제 파일 경로와 일치하는지 본다.
- 관련 문서 링크가 열리는지 본다.
- `구현됨`, `pending scope`, `resolved/N/A` 표기가 근거와 맞는지 본다.
- live orchestrator integration처럼 미증명 항목이 완료로 표기되지 않았는지 본다.

## lifecycle 문서 수정 시 최소 교차 점검표

| 문서 변경 종류 | 같이 확인할 verification 근거 |
| --- | --- |
| hook 또는 state 저장 규칙 | unittest의 hook/state 관련 항목 |
| install/update entrypoint 설명 | installer dry-run, activation verifier 관련 테스트 |
| refresh/cleanup 설명 | refresh dry-run, cleanup 관련 테스트 |
| resume/hydrate 설명 | `sessionStart` hydrate, `AWAIT` persistence 테스트 |
| mediator/no-go 설명 | thin orchestrator contract와 responsibility split 문서 |

## 결론

runtime verification checklist와 documentation review checklist는 분리된 절차가 아니라 한 세트다. lifecycle 문서는 두 체크를 모두 통과해야 완료로 본다.

## 관련 문서

- [lifecycle-acceptance-checklist.md](./lifecycle-acceptance-checklist.md)
- [lifecycle-validation-guide.md](./lifecycle-validation-guide.md)
- [lifecycle-validation-matrix.md](./lifecycle-validation-matrix.md)
