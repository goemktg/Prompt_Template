# Memory MCP 태그 및 스키마 기반 구조: 특수 중재자 (Memory MCP Tag & Schema Guide)

**작성일:** 2026-04-16
**상태:** Active
**적용 대상:** `Memory MCP`를 활용하는 오케스트레이터 및 향후 도입될 Mediator 에이전트

## 1. 문서 목적

본 문서는 향후 도입될 Mediator 에이전트의 작업 재개(Resume), 상태 개체(State objects) 관리 및 게이트(Gate) 통제 경계를 지원하기 위한 **Memory MCP 태그 및 스키마 기반 구조**를 정의합니다. 지원되지 않는 런타임 제어나 섀도우 오케스트레이션(Shadow orchestration)을 방지하고 얇은(Thin) 상태 전이만을 목적에 둡니다.

## 2. 기본 원칙

* **오케스트레이터 권위 존중**: 상태 전이의 주체는 오케스트레이터이며, Mediator는 주어진 상태를 확인하고 부분 업데이트(Partial update)만 수행합니다.
* **단순성**: 깊게 중첩된 객체를 피하고 평탄화된 상태 스키마를 지향합니다. `metadata.tags` 및 `metadata.type` 등 기본 필드를 활용하며, 결과 요약은 `content` 영역에 서술합니다.

## 3. Tagging 구조

상태 및 이력을 추적하기 위한 Tag 규약입니다. 쿼리 시 이 태그 조합을 사용하여 특정 런타임 컨텍스트를 복원합니다.

* `mediator-state`: Mediator 상태 객체임을 나타내는 필수 루트 태그
* `session:[SessionID]`: 고유 세션 식별자
* `protocol:[ProtocolName]`: 실행 중인 프로토콜 이름 (예: `governance-flow`, `catalog-update`)
* `status:[Status]`: 현재 진행 상태 (예: `status:pending`, `status:in-progress`, `status:blocked`, `status:completed`)

## 4. State Object 스키마 예시

작업 상태 보존 및 재개를 위한 표준 JSON 형태의 메타데이터 스키마입니다.

### 초기 상태 (Pending)

```json
{
  "content": "Protocol: catalog-update, Phase: extraction, Target: papers.md",
  "metadata": {
    "tags": ["mediator-state", "session:abc-123", "protocol:catalog-update", "status:pending"],
    "type": "mediator-resume-state"
  }
}
```

### 완료/전환 상태 (Completed / Handoff)

*주의: 기존 Pending 상태의 `content`를 변경하는 것이 불가능하므로, 아래 객체는 `status:completed` 태그를 달아 새로 저장된(store) 별도의 메모리 레코드 예시입니다.*

```json
{
  "content": "Protocol: catalog-update, Phase: extraction completed, Target: papers.md. Extracted 12 items. Validation passed.",
  "metadata": {
    "tags": ["mediator-state", "session:abc-123", "protocol:catalog-update", "status:completed"],
    "type": "mediator-resume-state"
  }
}
```

## 5. 상태 전이(Status Transitions) 및 경계

1. **초기화**: 오케스트레이터가 `status:pending` 상태 객체를 Memory MCP에 기록합니다.
2. **실행**: Mediator가 해당 객체를 읽어들이고, 작업 완료 후 `mcp_memory_memory_update` 도구를 통해 상태 태그를 수정합니다. 이때, 기존의 `status:pending` 태그는 반드시 제거하고 `status:completed` 또는 `status:blocked` 태그로 **교체(Replace)** 해야 합니다(`session` 및 `protocol` 등 다른 태그는 보존). 주의: 현재 업데이트 도구는 `content` 수정을 지원하지 않으므로 변경된 처리 결과가 필요한 경우, 갱신이 아닌 새로운 메모리로 저장(store)하고 참조해야 합니다.
3. **복귀**: 오케스트레이터는 `status:completed` 태그를 폴링하거나 보고받고 다음 단계를 진행합니다.
4. **금지 사항**: Mediator는 새로운 `session` 태그를 생성하거나, 다른 서브에이전트의 상태 태그를 임의로 조작해서는 안 됩니다.
