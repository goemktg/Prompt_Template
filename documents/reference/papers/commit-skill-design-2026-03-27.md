# COMMIT SKILL 설계 근거 정리

## 개요

이 문서는 `commit-skill` 설계 시 반영한 공식 문서와 최신 연구 근거를 정리합니다.
핵심 목표는 다음과 같습니다.

- 변경사항 기반 커밋 메시지 자동 생성
- 커밋 전 사용자 명시 승인 강제
- 오동작 시 안전한 중단과 재확인

## 공식 문서 근거

### 1. Agent Skills Specification

- 출처: [Agent Skills Specification](https://agentskills.io/specification)
- 반영 포인트:
  - `SKILL.md`의 Frontmatter(`name`, `description`)가 스킬 디스커버리 핵심
  - 설명(description)에 "무엇을/언제" 사용해야 하는지 명확히 작성
  - 필요 시 `scripts`, `references`, `assets` 등 확장 구조 사용 가능

### 2. VS Code Agent Skills 문서

- 출처: [VS Code Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- 반영 포인트:
  - 프로젝트 스킬 위치를 `.github/skills/<skill-name>/SKILL.md`로 구성
  - 스킬 본문은 호출 시 로드되는 실행 지침으로 작성

### 3. GitHub Copilot Agent Skills 문서

- 출처: [GitHub Copilot Agent Skills](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-skills)
- 반영 포인트:
  - 스킬은 "항상 적용되는 규칙"이 아니라 "특정 작업에서 호출되는 워크플로우"에 적합
  - 스킬 디렉토리의 리소스를 필요 시 참조하도록 설계

## 최신 연구 근거

### 1. ReAct (2023)

- 논문: ReAct: Synergizing Reasoning and Acting in Language Models
- 링크: [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
- 적용:
  - `Inspect -> Generate -> Confirm -> Execute` 4단계 워크플로우 설계
  - 행동 실행 전 추론/요약 단계를 명시해 신뢰성과 설명가능성 향상

### 2. ToolACE (2024)

- 논문: ToolACE: Winning the Points of LLM Function Calling
- 링크: [arXiv:2409.00920](https://arxiv.org/abs/2409.00920)
- 적용:
  - 도구 호출 전제 조건을 명확히 선언
  - 실패 처리와 재시도 의사결정을 분리
  - "확인 없이 commit 금지" 같은 하드 제약 포함

### 3. Human-In-the-Loop Software Development Agents (2024)

- 논문: Human-In-the-Loop Software Development Agents
- 링크: [arXiv:2411.12924](https://arxiv.org/abs/2411.12924)
- 적용:
  - 최종 상태 변경(`git commit`) 전 사용자 승인 게이트 필수화
  - 애매한 사용자 응답을 승인으로 간주하지 않고 재확인

## 설계 원칙

### 원칙 1. 명시 승인 게이트

커밋은 저장소 상태를 변경하므로, 사용자 명시 승인 없이 실행하지 않습니다.

### 원칙 2. 변경사항 기반 메시지 생성

마지막 커밋(`HEAD`) 이후 diff를 기반으로 Conventional Commits 형식 후보를 생성합니다.

### 원칙 3. 실패 안전성

변경사항 없음, 커밋 실패, 애매한 승인 응답 시 중단 후 재확인합니다.

## 구현 체크리스트

- [x] `.github/skills/commit-skill/SKILL.md` 생성
- [x] `name`/`description` 포함한 frontmatter 작성
- [x] "커밋 진행" 트리거 문구 반영
- [x] 승인 전 커밋 금지 규칙 포함
- [x] 에러/엣지케이스 처리 지침 포함

## 참고

본 문서는 스킬 설계 근거를 기록하기 위한 참조 문서입니다.
실제 실행 규칙은 `SKILL.md`를 기준으로 합니다.
