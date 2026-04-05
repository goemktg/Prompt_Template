# 프롬프트 인수인계 및 모니터링 가이드 (Prompt Handoff Monitoring Guide)

이 문서는 2-Step Handoff 프로세스에 기반하여 프롬프트 분석 결과물(`@master-prompt-writer`)이 최종 문서(`@doc-writer`)로 어떻게 인계되고 관리되는지 모니터링하는 운영 절차를 설명합니다.

## 1. 목적 (Overview)

프롬프트 거버넌스 및 에이전트 책무 분리에 따라 팩트 중심의 초안 생성과 문서 품질 검수가 개별적으로 이루어집니다. 본 가이드는 Handoff 프로세스 중 누락되거나 병목이 발생하는 구간을 식별하고 해결하기 위한 관리 지침입니다.

## 2. 모니터링 대상 (Monitored Artifacts)

- **초안 팩트 시트 (Draft Fact Sheet):** `documents/drafts/`에 생성되는 템플릿 기반 초안 팩트 시트
- **Memory MCP 인수인계 내역:** 생성, 갱신, 소비 시점에 기록되는 단일 진실 버퍼 기록
- **최종 문서 (Final Document):** 팩트가 번역되고 규격화되어 발행되는 최종 `documents/` 하위 파일

## 3. 상태 생명주기 (Status Lifecycle)

1. `draft`: `@master-prompt-writer` 작성 진행 중.
2. `ready-for-doc-writer`: 초안 발행 완료 및 검증 요청 대기 중.
3. `blocked`: 팩트가 부족하거나 외부 검증 실패로 처리가 지연됨.
4. `superseded`: 최신 팩트 시트로 교체됨.
5. `consumed`: `@doc-writer`에 의해 활용되어 최종 발행됨.

## 4. 장애 유형 및 알림 모드 (Failure Modes & Alerts)

- **Handoff Timeout:** `ready-for-doc-writer` 상태로 방치된 후 48시간 내 `consumed` 되지 않은 경우. (병목 발생 가능성)
- **Evidence Unverified:** 유효한 논문 근거가 결여되었음에도 발행 절차로 진입된 경우.
- **Lost Fact Sheet:** Memory MCP 에는 기록되었으나 `documents/drafts/` 에 파일이 없는 경우 경로 매핑 오류.

## 5. 정기 검수 체크리스트 (Daily/Weekly Review Checklist)

- [ ] Memory MCP의 `blocked` 항목 원인 분석 및 해결
- [ ] 72시간 경과한 `draft` 상태 폐기 또는 재할당
- [ ] 최종 문서 발간 누락 없이 `consumed` 상태 업데이트 확인
- [ ] 정기적으로 `documents/drafts/` 의 오래된 미사용 초안 일괄 정리 (2주일 초과)

## 6. 권장 핵심성과지표 (Minimal KPIs)

- **Handoff Latency:** 인계 상태 전환에 소요되는 평균 시간 (`ready` → `consumed`)
- **Blocked Rate:** 전체 Handoff 건수 중 `blocked` 상태가 되는 문서의 비율 (오류 비율 지표)
- **Superseded Rate:** 단일 분석 도중 여러 번 반복 작성되는 낭비 비율
- **Missing Citation Rate:** 인용구 누락으로 반환된 `unverified` 팩트 비율

## 7. 운영자 조치 사항 (Operator Actions)

`blocked` 나 `stale` 상태 등 문제가 발견될 경우 다음을 조치합니다.

1. `blocked`: 상태 사유를 분석하고, `@master-prompt-writer`에게 결측 데이터 보강이나 논문 재검증 지시. 필요 시 타 에이전트(예: `@research-gpt`) 투입.
2. `stale` (`ready` 지연): `@doc-writer`에게 수동 호출 지시. "Handoff 패키지 검증 후 최종 문서 발행 요망."
3. 반복적 `unverified`: 팩트 시트 템플릿의 Required 항목과 논문 카탈로그 이력 대조 (Paper Catalog Update 가이드 참조).
