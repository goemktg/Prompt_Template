# Prompt Engineering Papers: Master Index

> **Last Updated**: 2026-03-29
> **Policy**: Each category targets **100 papers**. The `@prompt-master` agent auto-updates
> category files monthly — retiring the lowest-scoring entries when a category exceeds 100.
> **Curator**: `@prompt-master` agent — run on first invocation after 30-day deadline.

---

## Category Index

| # | Category | Tag | File | Current | Target | Last Updated |
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

**Total**: 600 / 1,200 papers across all categories

---

## Scoring Rubric (All Categories)

| Field | Range | Description |
|-------|-------|-------------|
| **Novelty** | 1–100 | How novel the contribution is relative to existing work |
| **Impact** | 1–100 | Citation count signal + practical adoption breadth |
| **Score** | 1–100 | `round((Novelty + Impact) / 2)` |

Score thresholds:

- **80–100**: Core canon — must keep; reference first in technique selection
- **60–79**: Important — include for relevant task types
- **40–59**: Supplementary — niche or incremental value
- **1–39**: Retirement candidates (retire first when category exceeds 100)

---

## Update Procedure

Paper catalog update workflow is managed by the dedicated skill:

- Skill name: `paper-catalog-update`
- Skill definition file: `.github/skills/paper-catalog-update/SKILL.md`

Use that skill as the single source of truth for stale-check, scoring, add/retire policy, and metadata updates.

---

## Top Papers Quick Reference (Score ≥ 90)

| Category | Title | Score |
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

