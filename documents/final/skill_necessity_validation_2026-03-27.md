# 스킬 재작성 및 필요성 재검증 보고서 (2026-03-27)

## 1. 목적

`reference/`에 제공된 레퍼런스 스킬들을 기준으로, 현재 프로젝트 템플릿에 맞는 실행형 스킬 세트를 재구성하고 각 스킬의 필요성을 다시 검증한다.

## 2. 검토 범위

- 기준 문서
  - `reference/documentation/SKILL.md`
  - `reference/code-review/SKILL.md`
  - `reference/deep-research/SKILL.md`
  - `reference/data-analysis/SKILL.md`
  - `reference/skill-extension/SKILL.md`
  - `reference/external-skill-generation/SKILL.md`
  - `documents/reference/papers/commit-skill-design-2026-03-27.md`
- 프로젝트 정책
  - `.github/copilot-instructions.md`
  - `documents/AGENT_MANUAL.md`
  - `AGENTS.md`

## 3. 재작성 결과

신규/개정 반영된 스킬 파일:

- `.github/skills/commit-skill/SKILL.md` (개정)
- `.github/skills/documentation/SKILL.md` (신규)
- `.github/skills/code-review/SKILL.md` (신규)
- `.github/skills/deep-research/SKILL.md` (신규)
- `.github/skills/data-analysis/SKILL.md` (신규)
- `.github/skills/skill-extension/SKILL.md` (신규)
- `.github/skills/external-skill-generation/SKILL.md` (신규)

연결 자산:

- `.github/skills/external-skill-generation/templates/skill_seekers_unified.example.json`
- `.github/skills/external-skill-generation/templates/mcp.skill-seekers.example.json`
- `.github/skills/external-skill-generation/templates/review_checklist.md`

## 4. 스킬별 필요성 검증

### 4.1 commit-skill

- 판정: **필수 유지**
- 근거:
  - 저장소 상태를 변경하는 `git commit`은 승인 게이트가 없으면 사고 비용이 높다.
  - 검사 스크립트 기반 워크플로우를 강제하면 에이전트별 실행 편차를 줄일 수 있다.
  - Conventional Commits 규칙을 통해 변경 추적성과 릴리즈 가독성을 확보한다.
- 중복/대체 가능성: 낮음 (직접 대체 가능한 스킬 없음)

### 4.2 documentation

- 판정: **필수 유지**
- 근거:
  - 본 템플릿은 `documents/drafts -> documents/final` 파이프라인을 전제로 한다.
  - `documents/` 한국어, 운영 자산 영어 정책을 문서 작성 단계에서 강제해야 일관성이 유지된다.
  - 다양한 프로젝트 유형에서 재사용 가능한 문서 표준이 필요하다.
- 중복/대체 가능성: 낮음

### 4.3 code-review

- 판정: **필수 유지**
- 근거:
  - 템플릿 레포는 정책/카탈로그/운영 문서가 분리되어 있어 회귀 리스크 탐지 체계가 중요하다.
  - 단순 문법 검사가 아닌 위험도 기반 리뷰 프로토콜이 필요하다.
  - PR/커밋 전 품질 게이트 역할로 직접적인 효용이 있다.
- 중복/대체 가능성: 낮음

### 4.4 deep-research

- 판정: **조건부 필수 (연구형/아키텍처형 작업에서 필수)**
- 근거:
  - 복합 질문(근거 요구, 다중 출처 비교)에서 ad-hoc 검색은 품질 편차가 크다.
  - 출처 수집/검증/합성 단계를 강제하면 문서 신뢰성과 재현성이 향상된다.
  - 레퍼런스/최종 보고 축적 구조와 잘 맞는다.
- 중복/대체 가능성: 중간 (단순 질의에는 오버헤드 가능)

### 4.5 data-analysis

- 판정: **조건부 유지 (실험/측정 작업에서 필수)**
- 근거:
  - 결과 비교/시각화/해석 규칙이 없으면 의사결정의 근거가 약해진다.
  - 베이스라인, 지표 정의, 시각화 품질을 정형화할 필요가 있다.
  - `results/`, `documents/final/` 연계 산출물 작성에 직접 사용 가능하다.
- 중복/대체 가능성: 중간 (일반 개발 태스크에서는 사용 빈도 낮음)

### 4.6 skill-extension

- 판정: **필수 유지**
- 근거:
  - 템플릿의 핵심 산출물인 스킬 파일의 생성/수정 품질을 직접 통제한다.
  - frontmatter 규칙(name/description), 경로 규칙, 단일 책임 원칙을 강제한다.
  - 향후 커스텀 스킬 추가 시 기준점 역할을 한다.
- 중복/대체 가능성: 낮음

### 4.7 external-skill-generation

- 판정: **선택 유지 (보안 통제 하에 사용)**
- 근거:
  - 외부 문서 기반 스킬 생성은 생산성이 높지만 보안/저작권/품질 리스크가 있다.
  - 본 스킬은 격리 경로(`temp/`) 및 수동 검증 게이트를 강제해 리스크를 낮춘다.
  - 템플릿 자산(JSON 예시, 체크리스트) 포함으로 안전한 반복 사용이 가능하다.
- 중복/대체 가능성: 중간 (외부 소스 미사용 시 불필요)

## 5. 결론

- 현재 프로젝트 기준 핵심 상시 스킬: `commit-skill`, `documentation`, `code-review`, `skill-extension`
- 상황 의존 스킬: `deep-research`, `data-analysis`, `external-skill-generation`
- 권장 운영: 상시 스킬은 기본 활성 문맥으로 유지하고, 상황 의존 스킬은 트리거 기반으로 호출

## 6. 후속 제안

1. `AGENTS.md`의 Available Skills 표에 `Priority` 또는 `Usage Scope` 열 추가
2. 스킬별 예제 태스크 1개씩을 `temp/skill_examples/`에 샘플로 관리
3. 분기별로 스킬 사용 로그를 점검해 사용 빈도 낮은 스킬을 축소/통합
