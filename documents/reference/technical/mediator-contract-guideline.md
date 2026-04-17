# 중재자 에이전트 계약 및 규약 (Mediator Contract Guideline)

**작성일:** 2026-04-16
**상태:** Active
**관련 스펙:** [temple-run-instruction-mediator-implementation.md](../../drafts/temple-run-instruction-mediator-implementation.md)

## 1. 문서 목적

본 문서는 환경 내 비대화형 다단계 프로토콜을 처리하기 위한 **얇은 중재자(Thin/Protocol Mediator) 에이전트**의 입력, 출력, 권한 경계 및 예외 처리 규약을 정의합니다.

## 2. 권한 경계 (Authority Boundaries)

### 허용된 권한 (In-Scope)

* **단일 프로토콜 내의 정규화**: 복잡한 출력을 파싱하거나 형식을 맞추는 데이터 정규화(Output normalization).
* **사전 조건 검사 (Local preflight)**: 주어진 입력 페이로드가 해당 중재자가 처리할 수 있는 유효한 형식인지 검사.
* **컨텍스트 축소 (Context trimming)**: 오케스트레이터에게 필요한 핵심 요약 정보와 정형화된 응답만 반환.

### 금지된 권한 (Out-of-Scope)

* **섀도우 오케스트레이션 (Shadow Orchestration)**: `runSubagent`를 호출하여 다른 서브에이전트에게 작업을 위임하는 행위.
* **글로벌 게이트 통제**: `0-SKILL`, `0-INTENT`, `0-GATE` 등의 평가 및 라우팅 결정.
* **사용자 직접 대화**: `ask_user`, `vscode_askQuestions` 등 대화형 사용자 질문 도구를 활용하거나 사용자에게 직접 입력을 요구하는 행위 (절대 금지).
* **영구 정책 수정**: `.github/copilot-instructions.md` 등 글로벌 거버넌스 파일 임의 수정.

## 3. 입력 계약 (Input Contract)

Mediator를 호출하는 오케스트레이터는 다음의 구조화된 입력을 제공해야 합니다.

* **명시적 목표**: 처리해야 할 단일 로직 (예: "Extract metrics from output").
* **제한된 컨텍스트**: 전체 대화 기록이 아닌, 처리에 필요한 특정 파일 경로 또는 원시 텍스트.
* **재개 식별자**: (필요시) Memory MCP에서 상태를 조회할 수 있는 Tag 목록 또는 Session ID.

## 4. 출력 계약 (Output Contract)

처리 완료 후, Mediator는 항상 명확하고 파싱 가능한 구조로 오케스트레이터에게 반환해야 합니다. 대화형 설명문이나 인사말을 포함해서는 안 됩니다.

### 성공 시 (SUCCESS)

```json
{
  "status": "SUCCESS",
  "data": {
    "normalized_key": "normalized_value"
  }
}
```

### 실패 시 (FAIL)

```json
{
  "status": "FAIL",
  "error": {
    "code": "PARSE_ERROR",
    "reason": "실패 원인에 대한 구체적인 설명",
    "retryable": true
  }
}
```

에러 코드는 반드시 단일 문자열(`INVALID_INPUT`, `LOCAL_PREFLIGHT_FAIL`, `PARSE_ERROR` 등) 중 하나를 반환해야 합니다.

## 5. 정규화 및 에러 처리 기대 수준

* **노이즈 제거**: LLM 응답에 섞인 부가 설명이나 Markdown 포맷 오류를 제거하고 완벽하게 정규화된 형태(주로 strict JSON)로 가공해야 합니다.
* **구조화된 에러 반환**: 데이터 누락이나 로컬 조건 위반 시, 짐작해서 결과를 만들지 말고 명시적인 `FAIL` 상태와 실패 사유를 담은 구조체를 오케스트레이터에게 반환하여 재시도나 판단을 위임합니다.

## 6. 안티패턴 (Anti-patterns)

1. **상태 가로채기**: 오케스트레이터를 거치지 않고 독자적으로 Memory MCP의 진행률을 100%로 명시해버리거나 세션을 임의로 종료하는 행위.
2. **지시어 남용**: 특정 프로토콜 전용 Mediator가 다른 템플릿(예: 프롬프트 논문 등)을 무단으로 로드하여 글로벌 공간에 간섭하는 행위.
3. **대화형 반환문**: 사람을 대하듯 "~진행했습니다", "다음은 결과입니다" 등의 서술부를 출력하는 행위. 반드시 간결한 구조체만 리턴해야 합니다.
