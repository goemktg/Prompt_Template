# 프롬프트 엔지니어링 논문: 마스터 색인

> **최종 업데이트**: 2026-03-29
> **정책**: 각 카테고리의 목표는 논문 **100편**입니다. `@master-prompt-writer` 에이전트가
> 카테고리 파일을 월별 자동 업데이트하며, 100편 초과 시 최저 점수 논문부터 퇴출합니다.
> **관리자**: `@master-prompt-writer` 에이전트 — 30일 기한 이후 첫 실행 시 동작합니다.

---

## 카테고리 색인

| # | 카테고리 | 태그 | 파일 | 현재 | 목표 | 최종 업데이트 |
|---|----------|-----|------|---------|--------|-------------|
| 1 | Surveys & Overviews | `[SURVEY]` | [survey.md](categories/survey.md) | 50 | 100 | 2026-03-29 |
| 2 | Reasoning & Chain-of-Thought | `[REASONING]` | [reasoning.md](categories/reasoning.md) | 50 | 100 | 2026-03-29 |
| 3 | Automatic Prompt Optimization | `[AUTO-OPT]` | [auto-opt.md](categories/auto-opt.md) | 50 | 100 | 2026-03-29 |
| 4 | Agent & Multi-Step Prompting | `[AGENT]` | [agent.md](categories/agent.md) | 50 | 100 | 2026-03-29 |
| 5 | Structured Output & Format | `[STRUCTURE]` | [structure.md](categories/structure.md) | 50 | 100 | 2026-03-29 |
| 6 | Code & Program-Aided Prompting | `[CODE]` | [code.md](categories/code.md) | 50 | 100 | 2026-03-29 |
| 7 | Few-Shot & In-Context Learning | `[FEW-SHOT]` | [few-shot.md](categories/few-shot.md) | 50 | 100 | 2026-03-29 |
| 8 | RAG & Knowledge-Augmented | `[RAG]` | [rag.md](categories/rag.md) | 50 | 100 | 2026-03-29 |
| 9 | Safety & Robustness | `[SAFETY]` | [safety.md](categories/safety.md) | 50 | 100 | 2026-03-29 |
| 10 | Prompt Compression & Efficiency | `[COMPRESSION]` | [compression.md](categories/compression.md) | 50 | 100 | 2026-03-29 |
| 11 | Multimodal Prompting | `[MULTIMODAL]` | [multimodal.md](categories/multimodal.md) | 50 | 100 | 2026-03-29 |
| 12 | Role & Persona Prompting | `[ROLE]` | [role.md](categories/role.md) | 50 | 100 | 2026-03-29 |

**총계**: 전체 카테고리 1,200편 중 600편

---

## 점수 기준 (전체 카테고리)

| 필드 | 범위 | 설명 |
|-------|-------|-------------|
| **Novelty** | 1–100 | 기존 연구 대비 기여의 신규성 |
| **Impact** | 1–100 | 인용 횟수 + 실질적 채택 범위 |
| **Score** | 1–100 | `round((Novelty + Impact) / 2)` |

점수 기준:

- **80–100**: 핵심 정전 — 반드시 유지; 기법 선택 시 우선 참조
- **60–79**: 중요 — 관련 작업 유형에 포함
- **40–59**: 보조 — 틈새 또는 점진적 가치
- **1–39**: 퇴출 후보 (카테고리 100편 초과 시 우선 퇴출)

---

## 업데이트 절차

논문 카탈로그 업데이트 워크플로우는 전용 스킬로 관리됩니다:

- 스킬 이름: `paper-catalog-update`
- 스킬 정의 파일: `.github/skills/paper-catalog-update/SKILL.md`

최신 여부 확인, 점수 산정, 추가/퇴출 정책, 메타데이터 업데이트의 단일 정보 소스는 해당 스킬을 사용하세요.

---

## 상위 논문 빠른 참조 (점수 ≥ 90)

| 카테고리 | 제목 | 점수 |
|----------|-------|-------|
| `[FEW-SHOT]` | Language Models are Few-Shot Learners (GPT-3) | 99 |
| `[REASONING]` | Chain-of-Thought Prompting Elicits Reasoning in LLMs | 99 |
| `[ROLE]` | InstructGPT: Training LMs to Follow Instructions | 97 |
| `[RAG]` | Retrieval-Augmented Generation for NLP Tasks | 97 |
| `[MULTIMODAL]` | CLIP: Learning Transferable Visual Models | 97 |
| `[SURVEY]` | Pre-train, Prompt, and Predict | 95 |
| `[CODE]` | Evaluating LLMs Trained on Code (Codex / HumanEval) | 94 |
| `[MULTIMODAL]` | GPT-4V(ision) Technical Report | 94 |
| `[MULTIMODAL]` | Stable Diffusion: High-Resolution Image Synthesis | 94 |
| `[AUTO-OPT]` | Large Language Models as Optimizers (OPRO) | 91 |
| `[AGENT]` | ReAct: Synergizing Reasoning and Acting | 93 |
| `[SAFETY]` | Constitutional AI: Harmlessness from AI Feedback | 92 |
| `[REASONING]` | Self-Consistency Improves Chain of Thought | 92 |
| `[MULTIMODAL]` | Flamingo: Visual Language Few-Shot Learning | 91 |
| `[REASONING]` | Zero-shot CoT ("Let's think step by step") | 91 |

