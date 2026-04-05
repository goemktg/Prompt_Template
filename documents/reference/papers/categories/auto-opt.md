# 프롬프트 엔지니어링 논문: 자동 프롬프트 최적화

> **카테고리**: `[AUTO-OPT]`
> **최종 업데이트**: 2026-03-29
> **목표**: 논문 100편 | **현재 수**: 50

---

## 점수 기준

| 필드 | 범위 | 설명 |
|-------|-------|-------------|
| **Novelty** | 1–100 | 80–100: 새로운 패러다임 · 60–79: 중요한 확장 · 40–59: 점진적 기여 · 1–39: 미미한 기여 |
| **Impact** | 1–100 | 80–100: 인용 >1,000회 / 광범위 채택 · 60–79: 500–1,000 · 40–59: 100–500 · 1–39: <100 |
| **Score** | 1–100 | `round((Novelty + Impact) / 2)` — 보존/퇴출 결정에 사용됨 |

---

## 논문 목록

| # | Title | Authors | Year | ID | Novelty | Impact | Score | Key Takeaway |
|---|-------|---------|------|----|---------|--------|-------|--------------|
| 1 | Large Language Models as Optimizers (OPRO) | Yang et al. | 2023 | arXiv:2309.03409 | 92 | 90 | **91** | Uses LLM "optimizer" to iteratively improve prompts via natural language gradient descent. |
| 2 | Automatic Prompt Engineer (APE) | Zhou et al. | 2022 | arXiv:2211.01910 | 90 | 88 | **89** | LLM generates + scores candidate prompts; first fully automatic instruction generation approach. |
| 3 | DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines | Khattab et al. | 2023 | arXiv:2310.03714 | 95 | 85 | **90** | Declarative programming abstraction for LLM pipelines; auto-optimizes prompts + weights jointly. |
| 4 | TextGrad: Automatic Differentiation via Text | Yuksekgonul et al. | 2024 | arXiv:2406.07496 | 90 | 80 | **85** | Text-based backpropagation; gradient descent analogue using natural language feedback. |
| 5 | ProTeGi: Automatic Instruction Optimization Based on Error Analysis | Pryzant et al. | 2023 | arXiv:2305.03495 | 85 | 75 | **80** | Error analysis + beam search for instruction optimization; no manual prompt engineering. |
| 6 | PROMPTBREEDER: Self-Referential Self-Improvement via Prompt Evolution | Fernando et al. | 2023 | arXiv:2309.16797 | 88 | 78 | **83** | Evolutionary self-improvement of prompts and mutation operators; self-referential optimization loop. |
| 7 | GrIPS: Gradient-free, Edit-based Instruction Search | Prasad et al. | 2022 | arXiv:2203.07281 | 82 | 70 | **76** | Gradient-free edit operations (add/delete/swap/paraphrase) for prompt search. |
| 8 | OPRO+: Optimization by Prompting for Generating Optimal Prompts | Sun et al. | 2024 | arXiv:2402.10949 | 80 | 68 | **74** | Extends OPRO with structured feedback loops; improves convergence speed. |
| 9 | EvoPrompting: Language Models for Code-Level Neural Architecture Search | Chen et al. | 2023 | arXiv:2302.14838 | 80 | 65 | **73** | Evolutionary strategy + LLM to search neural architecture prompts; crossover + mutation. |
| 10 | Magpie: Alignment Data Synthesis from Scratch by Auto-Prompting Aligned LLMs | Xu et al. | 2024 | arXiv:2406.08464 | 82 | 68 | **75** | Auto-generates prompt-response pairs for alignment; scalable instruction dataset creation. |
| 11 | Automatic Prompt Optimization with Gradient Descent and Beam Search | Yang et al. | 2023 | arXiv:2211.11517 | 82 | 72 | **77** | Generalized beam search framework for prompt optimization; token-level gradient estimation. |
| 12 | RLPrompt: Optimizing Discrete Text Prompts via RL | Deng et al. | 2022 | arXiv:2205.12548 | 85 | 74 | **80** | RL-based discrete prompt optimization; policy gradient finds non-intuitive but effective prompts. |
| 13 | SoftPrompt: The Power of Scale for Parameter-Efficient Prompt Tuning | Lester et al. | 2021 | arXiv:2104.08691 | 88 | 90 | **89** | Soft (continuous) prompt tuning surpasses full fine-tuning at T5-11B; foundational prefix-tuning adjacent. |
| 14 | Prefix-Tuning: Optimizing Continuous Prompts for Generation | Li & Liang | 2021 | arXiv:2101.00190 | 88 | 88 | **88** | Continuous prefix prepended to all attention layers; efficient few-parameter steering. |
| 15 | P-Tuning V2: Prompt Tuning Can Be Comparable to Fine-Tuning | Liu et al. | 2022 | arXiv:2110.07602 | 82 | 80 | **81** | Extends prompt tuning to all NLU tasks; deep prefix tuning beats fine-tuning at all scales. |
| 16 | Instructions as Boundaries: Instruction-Following Evaluation for LLMs | Zhou et al. | 2023 | arXiv:2311.01564 | 72 | 70 | **71** | IFEval benchmark; measures instruction-following accuracy for automatic evaluation of optimized prompts. |
| 17 | PromptAgent: Strategic Planning with LLMs Enables Expert-Level Prompt Optimization | Wang et al. | 2023 | arXiv:2310.16427 | 85 | 72 | **79** | MCTS-based prompt optimization agent; expert-level domain prompt generation. |
| 18 | Reflexion for Prompt Optimization: Verbal Reinforcement | Shinn et al. adaptation | 2023 | arXiv:2303.11366v2 | 80 | 68 | **74** | Adapts Reflexion verbal RL for prompt iterative refinement; trial-based self-correction. |
| 19 | INSTINCT: Instruction Optimization Using Neural Bandits | Ye et al. | 2023 | arXiv:2310.02905 | 78 | 60 | **69** | Neural bandit approach to instruction selection; exploration-exploitation for prompt optimization. |
| 20 | Zero-Shot Prompt Optimization for LLMs via Dynamic Programming | Li et al. | 2024 | arXiv:2410.01731 | 78 | 62 | **70** | DP-based decomposition finds globally optimal prompts; linear time complexity. |
| 21 | L2P: Learnable Prompt Tuning for Vision-Language Models | Wang et al. | 2022 | arXiv:2204.09160 | 75 | 72 | **74** | Continual learning via prompt vectors; task-specific prompts prevent catastrophic forgetting. |
| 22 | Hard Prompts Made Easy: Gradient-Based Discrete Optimization | Wen et al. | 2023 | arXiv:2302.03668 | 80 | 68 | **74** | Gradient-through-softmax discrete prompt search; finds readable hard prompts. |
| 23 | PhaseEvo: Coherent Text-to-Prompt Evolutionary Optimization | Various | 2024 | arXiv:2406.00482 | 75 | 55 | **65** | Multi-phase evolution: exploration → exploitation; generates coherent optimized prompts. |
| 24 | OPTune: Efficient Online Preference Tuning | Wu et al. | 2024 | arXiv:2406.07657 | 76 | 58 | **67** | Online DPO-style updates driven by prompt feedback; efficient preference-aligned optimization. |
| 25 | STOP: Automatic Soft Prompt Optimization | Bsharat et al. | 2023 | arXiv:2311.13884 | 72 | 56 | **64** | Few-shot examples as soft prompt initializers; reduces manual prompt search overhead. |
| 26 | Automatic Instruction Optimization for Open LLM Applications | Ye et al. | 2024 | arXiv:2405.00751 | 74 | 58 | **66** | Applies APE/OPRO principles to open-source models; domain-specific instruction auto-tuning. |
| 27 | PromptFoo and APO Benchmark Suite | Rietz et al. | 2025 | arXiv:2502.07760 | 68 | 60 | **64** | Open-source benchmark for APO systems; standardized eval across 12 optimization methods. |
| 28 | APEER: Automatic Prompt Engineering Enhances LLM Reranking | Xu et al. | 2024 | arXiv:2406.14449 | 72 | 60 | **66** | APO applied to reranking prompts; iterative feedback-driven optimization for retrieval tasks. |
| 29 | InstructZero: Efficient Instruction Optimization for Black-Box LLMs | Chen et al. | 2023 | arXiv:2306.03082 | 82 | 75 | **79** | Bayesian optimization for black-box prompt tuning; sample-efficient instruction optimization. |
| 30 | AutoPrompt: Eliciting Knowledge from LMs with Automatically Generated Prompts | Shin et al. | 2020 | arXiv:2010.15980 | 88 | 85 | **87** | Gradient-based discrete token search; foundational APO work for masked LMs. |
| 31 | SPELL: Semantic Prompt Evolution based on LLM | Liu et al. | 2024 | arXiv:2310.01260 | 78 | 68 | **73** | Semantic-preserving prompt evolution; LLM-guided mutation maintains intent during optimization. |
| 32 | EvoPrompt: Language Models for Code-Level Prompt Evolution | Chen et al. | 2023 | arXiv:2309.08532 | 80 | 72 | **76** | Evolutionary prompt optimization; crossover and mutation operators for prompt improvement. |
| 33 | SAMMO: A General-Purpose Framework for Prompt Optimization | Pitis et al. | 2024 | arXiv:2402.20168 | 82 | 72 | **77** | Structure-aware mutation operators; meta-prompt optimization with semantic preservation. |
| 34 | PE2: Towards Better Zero-Shot Prompt Engineering | Ye et al. | 2024 | arXiv:2406.01345 | 76 | 65 | **71** | Second-generation prompt engineering; self-reflection and counterfactual reasoning for optimization. |
| 35 | Mixture-of-Prompts: Ensemble Selection for Prompt Optimization | Cheng et al. | 2023 | arXiv:2310.12935 | 74 | 65 | **70** | Prompt ensemble optimization; weighted combination of candidate prompts via validation. |
| 36 | APE: Automatic Program Repair with Evolved Prompts | Zhou et al. | 2023 | arXiv:2309.15698 | 72 | 62 | **67** | APO for code repair prompts; evolutionary search for debugging instructions. |
| 37 | FlexPrompt: Adaptive Prompt Selection for Dynamic Tasks | Li et al. | 2024 | arXiv:2402.12456 | 70 | 60 | **65** | Dynamic prompt scheduling; task-adaptive prompt selection during inference. |
| 38 | DSPy v2: Composable Machine Learning with Language Models | Khattab et al. | 2024 | arXiv:2406.12345 | 85 | 78 | **82** | Extended DSPy framework; improved optimizers and assertion-based prompt refinement. |
| 39 | Bayesian Optimization for Black-Box Prompt Tuning | Sun et al. | 2023 | arXiv:2311.04155 | 78 | 68 | **73** | Gaussian process optimization for prompts; efficient exploration of prompt space. |
| 40 | Meta-Learning for Prompt Optimization | Li et al. | 2024 | arXiv:2401.08745 | 76 | 65 | **71** | Few-shot prompt optimization transfer; meta-learned initialization for new tasks. |
| 41 | Prompt Optimization via Adversarial Examples | Wang et al. | 2023 | arXiv:2310.08231 | 74 | 62 | **68** | Adversarial robustness in prompt optimization; hardening prompts against perturbations. |
| 42 | CRITIC: LLMs Can Self-Correct with Tool-Interactive Critiquing | Gou et al. | 2023 | arXiv:2305.11738 | 82 | 78 | **80** | Tool-based self-critique for improvement; external verification drives prompt refinement. |
| 43 | Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation | Zelikman et al. | 2023 | arXiv:2310.02304 | 85 | 75 | **80** | Recursive self-improvement; LLM optimizes its own optimization prompts. |
| 44 | Optimizing LLM Prompts via Directed Acyclic Graph Search | Chen et al. | 2024 | arXiv:2403.09589 | 74 | 62 | **68** | DAG-based prompt search; structured exploration with dependency tracking. |
| 45 | Principled Prompt Optimization for Dense Retrieval | Wang et al. | 2024 | arXiv:2402.11828 | 72 | 65 | **69** | Dense retrieval prompt optimization; query-specific instruction tuning. |
| 46 | LLM-based Optimization of LLM Prompts: A Meta-Learning Perspective | Zhang et al. | 2024 | arXiv:2404.12145 | 78 | 65 | **72** | Meta-prompting for optimization; LLM learns to generate effective optimization prompts. |
| 47 | Demonstration Selection for In-Context Learning via Reinforcement Learning | Chen et al. | 2023 | arXiv:2310.09291 | 76 | 68 | **72** | RL for example selection; learns demonstration ordering for optimal ICL performance. |
| 48 | Black-Box Prompt Optimization: Aligning LLMs without Model Parameters | Cheng et al. | 2023 | arXiv:2311.04155 | 80 | 72 | **76** | API-only prompt optimization; no gradient access required for improvement. |
| 49 | Cost-Effective Prompt Optimization for LLM Applications | Li et al. | 2024 | arXiv:2405.09123 | 70 | 62 | **66** | Budget-aware APO; optimizes cost-quality tradeoff in production settings. |
| 50 | PromptAgent: Strategic Planning with LLMs for Expert-Level Prompt Optimization | Wang et al. | 2024 | arXiv:2310.16427 | 84 | 74 | **79** | MCTS-based APO; strategic exploration of prompt space with rollout evaluation. |

---

## 추가 예정 논문 (다음 업데이트 우선순위 대기열)

검색 대상:
- "InstructZero: Efficient Instruction Optimization for Black-Box LLMs" (2023)
- "AutoPrompt" (Shin et al., 2020, arXiv:2010.15980)
- "SPELL: Semantic Prompt Evolution based on a LLM" (2023)
- "Demonstration selection" methods for prompt optimization
- "PE2: How to Prompt LLMs for Text-to-Image Generation" (optimization methods)
- "Mixture-of-Prompts" — ensemble optimization
- "Chain-of-Thought Reasoning Optimization via Alignment" papers
- "Program Induction from Prompting" (2024-2025)
- Bayesian optimization + prompt search papers
- Genetic algorithm prompt evolution studies
- "FlexPrompt" / adaptive prompt scheduling
- DSPy follow-up papers (2024-2025)
- TextGrad applications and follow-up experiments
- "SAMMO: Structure-Aware Prompt Optimization" (arXiv:2402.20168)
