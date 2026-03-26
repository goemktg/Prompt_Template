# 프롬프트 엔지니어링 감사 보고서

**날짜:** 2026-03-26
**최종 업데이트:** 2026-03-26
**대상:** `Prompt_Template` 리포지토리
**수신:** 프로젝트 관리자

## 1. 목적

이 보고서는 `Prompt_Template` 리포지토리의 현재 프롬프트 엔지니어링 성숙도를 최신 연구(2022–2026)와 비교 평가합니다. 에이전트 워크플로 내에서 구조적 비효율성, 컨텍스트 최적화 기회, 신뢰성 위험 요소를 식별하고 현대화를 위한 구체적인 로드맵을 제시합니다.

## 2. 분석 범위

감사는 다음 워크스페이스 자산을 대상으로 했습니다.

- **핵심 지침:** `.github/copilot-instructions.md`, `AGENTS.md`, `documents/AGENT_MANUAL.md`
- **에이전트 정의:** 22개의 활성 `.github/agents/*.agent.md` 파일
- **템플릿:** `documents/PROJECT.template.md`, `documents/CHANGELOG.template.md`, `documents/QUICKSTART.template.md`
- **누락된 자산:** `.github/prompts/*.prompt.md`, `.github/skills/*/SKILL.md`, `*.instructions.md` 파일의 부재가 명시적으로 확인됨.

## 3. 연구 참고 문헌

근거의 강도는 기초 기술과 최신 연구를 구분하기 위해 범주화되었습니다.

**강력한 / 기초적인 근거:**

- **Chain-of-Thought (CoT) Prompting** (Wei et al., 2022) — 복잡한 추론에 필수적임.
- **ReAct Framework** (Yao et al., 2022; Yao et al., 2023) — 추론과 행동의 인터리빙(Interleaved reasoning and acting).
- **Self-Refine** (Madaan et al., 2023) — 반복적인 출력 개선.
- **Chain-of-Verification (CoVe)** (Dhuliawala et al., 2023) — 검증을 통한 환각(hallucination) 감소.
- **Prompt Engineering Survey** (Zhou et al., 2024/2025 update, arXiv:2402.07927) — 프롬프트 기법의 체계적인 분류.
- **LLM-as-a-Judge reliability literature** (2024–2025 survey landscape) — 평가자 편향 및 메타 평가 우려 사항.

**최신 / 떠오르는 근거 (실험적):**

- **Evaluation-Driven Multi-Agent Optimization** (Purpura et al., 2026, arXiv:2601.03359) — 자동화된 지침 튜닝.
- **Layered Chain-of-Thought** (Sanwal, 2025, arXiv:2501.18645) — 멀티 에이전트 시스템을 위한 계층적 추론.
- **Automatic Prompt Optimization surveys** (2025 survey landscape) — 시스템 프롬프트의 알고리즘적 정제.

## 4. 핵심 원칙

문헌에서 도출된 네 가지 핵심 원칙이 이번 감사의 기준입니다.

1. **Context Parsimony:** 불필요한 토큰은 성능을 저하시킵니다 (Lost-in-the-Middle 현상). 지침은 단일 덩어리가 아니라 모듈화되어야 합니다.
2. **Explicit Decomposition:** 복잡한 작업은 한 번의 시도(one-shot)보다는 최종 사용자에게 보이지 않는 단계적 추론(CoT)이 필요합니다.
3. **Verification Loops:** 모든 생성 단계에는 별도의 검증 단계(CoVe/Self-Refine)가 필요합니다.
4. **Deterministic Tool Contracts:** 도구 정의는 구현 표면(surface)과 정확히 일치해야 환각 호출을 방지할 수 있습니다.

## 5. 범주별 결과

### A. 전역 지침 (`copilot-instructions.md`)

- **Token Overload:** 파일에 중복된 "MUST/MANDATORY" 지시어가 포함된 과도한 컨텍스트 부하가 있습니다. 최신 프롬프트 엔지니어링 조사 및 컨텍스트 윈도우 연구에 따르면, 동일한 운영 제약 조건은 한 번만 명시하고 지속적인 지침은 짧고 명확하며 반복을 줄이는 것이 좋습니다.
- **Subjectivity:** "very strong reasoner(매우 강력한 추론가)"와 같은 주관적인 규칙이 일부 존재하며, 이는 결정론적으로 강제하기 어렵습니다.
- **Broken Link:** 손상된 상대 링크가 포함되어 있습니다: `../../AGENTS.md#available-agents`.

### B. 아키텍처 및 우선순위

- **Ambiguity:** `.github/copilot-instructions.md`, `AGENTS.md`, `documents/AGENT_MANUAL.md` 간에 규칙 중복이 존재합니다. 충돌 발생 시(예: 운영 규칙 vs 코딩 규칙) 어떤 파일이 권한을 갖는지 불분명합니다.
- **Language Policy Boundary:** `documents/`는 한글, 그 외 운영 자산은 영어로 분리하는 정책은 이 저장소 구조에서는 실무적으로 허용 가능합니다. 다만 이 안전성은 `documents/`가 보관용·설명용 계층으로 남고, `.github/`의 운영 파일이 한글 문서를 필수 런타임 컨텍스트로 요구하지 않는다는 전제 위에서만 유지됩니다.

### C. 에이전트 정의

- **Standardization Gap:** 22개의 에이전트 파일에 표준화된 입력/출력 계약(contract)이 없으며, `AGENTS.md`에서의 선택 지원이 약합니다.
- **Boilerplate Inflation:** 많은 에이전트가 상태 비저장(stateless) 또는 원자적(atomic) 작업임에도 불구하고 길고 반복적인 지침 블록과 함께 *매 실행 시* `Memory MCP`를 의무화하고 있습니다. 이는 불필요하게 컨텍스트 윈도우를 소모합니다.
- **Tool Hallucination Risk:** 와일드카드 선언(예: `context7/*`, `memory/*`)이 사용됩니다. 이러한 "라지(lazy)" 정의는 설치된 런타임에 존재하지 않는 도구를 모델이 환각해낼 위험을 높입니다.

### D. 검증 및 품질

- **Unverifiable Rules:** 지침에 강제할 수 있는 훅(hook)이 없는 경우가 많습니다. 자동화된 린터(linter)나 프리커밋(pre-commit) 확인 없이는 "프로젝트 컨텍스트 확인"과 같은 규칙은 보장되기보다 희망 사항에 가깝습니다.

## 6. 우선순위 개선 권장 사항

다음 표는 결과를 해결하기 위한 고가치 조치 사항을 정리한 것입니다.

| Priority | Impact | Action Item | Target File(s) |
| :--- | :--- | :--- | :--- |
| **P0** | Critical | **언어 정책 경계 확정:** `documents/` 내부는 한글, 그 외 운영 자산은 영어로 고정하고 충돌 문구를 제거합니다. | `.github/copilot-instructions.md`, `documents/**/*.md` |
| **P0** | Critical | **깨진 링크 수정:** 탐색이 작동하도록 `AGENTS.md`에 대한 상대 경로를 수정합니다. | `.github/copilot-instructions.md` |
| **P1** | High | **핵심 규칙 중복 제거:** "3대 핵심 파일"을 엄격히 직교하는 구조(정책 vs 운영 vs 카탈로그)로 리팩터링합니다. | `copilot-instructions.md`, `AGENT_MANUAL.md` |
| **P1** | High | **에이전트 계약 표준화:** 결합성을 높이기 위해 22개 모든 에이전트에 대해 엄격한 입/출력 스키마를 정의합니다. | `.github/agents/*.agent.md` |
| **P2** | High | **도구 정의 최적화:** 환각을 줄이기 위해 와일드카드(`*`)를 명시적 도구 목록으로 대체합니다. | `.github/agents/*.agent.md` |
| **P2** | Medium | **메모리 지침 모듈화:** 반복적인 Memory MCP 상용구(boilerplate)를 전체 텍스트 포함 대신 공유 스킬이나 가벼운 참조로 이동합니다. | `.github/agents/*.agent.md` |
| **P2** | Medium | **CoT 분해 구현:** 복잡한 에이전트(예: `@architect`, `@research-claude`)가 내부적인 단계별 추론을 사용하도록 업데이트합니다. | `.github/agents/*.agent.md` |
| **P3** | Low | **프롬프트 자산 생성:** 빈번하고 반복적인 사용자 작업을 위해 `.github/prompts/*.prompt.md`를 도입합니다(현재 누락됨). | `.github/prompts/` |
| **P3** | Low | **SKILL.md 표준 채택:** 에이전트 파일의 복잡하고 반복적인 로직을 재사용 가능한 `.github/skills/`로 마이그레이션합니다. | `.github/skills/` |
| **P3** | Low | **규칙 검증 자동화:** 깨진 링크와 템플릿 준수 여부를 확인하는 린터를 생성합니다. | `scripts/validate_docs.py` |

## 7. 구현 로드맵

### 1단계: 위생 점검 (1주 차)

- **목표:** 치명적인 문제를 수정하고 일관성을 강제합니다.
- **성공 지표:** 핵심 문서 내 깨진 내부 링크 0개; `documents/` 내부 문서는 한글, 그 외 운영 자산은 영어로 정렬됨.

작업:

- `documents/` 내부 영어 문서를 한글로 변환합니다.
- `.github/copilot-instructions.md`의 언어 정책을 `documents/` 한글 / 그 외 영어로 갱신합니다.
- `copilot-instructions.md`의 깨진 링크를 수정합니다.
- 우선순위 계층 명확화: `copilot-instructions.md` (정책) > `AGENT_MANUAL.md` (프로세스) > `AGENTS.md` (카탈로그).

### 2단계: 최적화 (2주 차)

- **목표:** 토큰 사용량을 줄이고 신뢰성을 향상합니다.
- **성공 지표:** 상시 로드 지침 길이를 최소 20% 감소; 최우선 에이전트 파일에서 와일드카드 도구 선언 제거.

작업:

- 22개 모든 에이전트 감사: 와일드카드 도구 정의 제거.
- Memory MCP 지침을 간결한 참조 문자열(예: "전역 지침의 Memory 프로토콜 참조")로 리팩터링.
- 가장 많이 사용되는 상위 5개 에이전트에 대한 I/O 계약 정의.

### 3단계: 고급 워크플로 (3주 차 이상)

- **목표:** 연구 기반 추론 패턴을 구현합니다.
- **성공 지표:** 고복잡도 에이전트가 명시적인 단계별 워크플로를 사용; 최소 하나의 재사용 가능한 `.prompt.md` 또는 `.github/skills/` 패턴 채택 및 검증.

작업:

- 사용자에게 보이는 Chain-of-Thought(CoT) 공개 없이, 아키텍트 및 연구원 에이전트에 명시적 단계별 추론/분해 단계 도입.
- 공통 패턴(예: `documentation-writing`, `code-review`)을 위한 `SKILL` 파일 생성.
- 표준 사용자 쿼리를 위한 `.prompt.md` 템플릿 배포.

## 8. 위험 및 주의 사항

- **회귀(Regression):** 암시적 컨텍스트가 제거되면 전역 지침의 리팩터링으로 인해 일시적으로 에이전트 성능이 저하될 수 있습니다. A/B 테스트(또는 수동 현장 확인)가 필요합니다.
- **컨텍스트 윈도우:** 토큰 감소가 목표이긴 하지만, 과도한 최적화는 에이전트의 "성격"이나 미묘한 제약 조건을 잃게 할 수 있습니다. 간결함과 명확성 사이의 균형이 필요합니다.
- **언어 분리 정책의 한계:** `documents/` 한글 정책은 낮은 위험이지만, 운영 파일이 한글 문서를 필수 런타임 입력으로 참조하기 시작하면 검색 누락과 토큰 오버헤드가 빠르게 커질 수 있습니다.
- **모델 드리프트:** "Gemini 3 Pro"에 맞춰 튜닝된 에이전트는 다른 모델에서 다르게 동작할 수 있습니다. 프롬프트는 가능한 한 모델에 구애받지 않아야 하며, 모델별 오버라이드를 사용해야 합니다.
- **유지 보수:** `SKILL.md`와 `.prompt.md` 파일 도입은 유지 보수 범위를 증가시킵니다. `sanity_check` 스크립트가 이러한 새로운 파일 유형을 포함하는지 확인해야 합니다.
