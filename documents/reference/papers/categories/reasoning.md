# 프롬프트 엔지니어링 논문: 추론 및 사고의 연쇄

> **카테고리**: `[REASONING]`
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
| 1 | Chain-of-Thought Prompting Elicits Reasoning in LLMs | Wei et al. | 2022 | arXiv:2201.11903 | 98 | 100 | **99** | Foundational CoT paper; step-by-step intermediate reasoning steps unlock complex problem-solving. |
| 2 | Self-Consistency Improves Chain of Thought Reasoning in Language Models | Wang et al. | 2022 | arXiv:2203.11171 | 88 | 96 | **92** | Sample multiple reasoning paths and majority-vote; major accuracy lift over greedy CoT. |
| 3 | Tree of Thoughts: Deliberate Problem Solving with LLMs | Yao et al. | 2023 | arXiv:2305.10601 | 92 | 92 | **92** | Branching reasoning tree with BFS/DFS + look-ahead; enables complex planning tasks. |
| 4 | Graph of Thoughts: Solving Problems with LLMs Using Graphs | Besta et al. | 2024 | arXiv:2308.09687 | 85 | 78 | **82** | Generalizes ToT/GoT into arbitrary DAG; enables parallel branches and aggregation. |
| 5 | Chain of Draft: Thinking Faster by Thinking Less | Xu et al. | 2025 | arXiv:2502.18600 | 82 | 70 | **76** | Minimal intermediate token budgets; matches CoT accuracy at ~7.6× fewer tokens. |
| 6 | Large Language Models are Analogical Reasoners | Wei et al. | 2023 | arXiv:2310.01714 | 80 | 68 | **74** | Prompts analogical recall before solving; structured analogy retrieval improves accuracy. |
| 7 | Least-to-Most Prompting Enables Complex Reasoning in LLMs | Zhou et al. | 2022 | arXiv:2205.10625 | 88 | 82 | **85** | Decomposes hard questions into sub-problems solved sequentially; handles compositional reasoning. |
| 8 | Decomposed Prompting: A Modular Approach for Solving Complex Tasks | Khot et al. | 2022 | arXiv:2210.02406 | 82 | 75 | **79** | Modular sub-task decomposition + specialized handler prompts; reusable components. |
| 9 | Program of Thoughts Prompting: Disentangling Computation from Reasoning | Chen et al. | 2022 | arXiv:2211.12588 | 85 | 80 | **83** | Python-based CoT separates reasoning from computation; solves complex math via code execution. |
| 10 | Faithful Chain-of-Thought Reasoning | Lyu et al. | 2023 | arXiv:2301.13379 | 78 | 68 | **73** | Combines NL reasoning with symbolic solvers; grounds CoT in executable programs. |
| 11 | Complex CoT (cCoT): Complex Chain-of-Thought | Fu et al. | 2022 | arXiv:2210.00720 | 75 | 72 | **74** | Complexity-based selection for CoT exemplars; harder examples yield larger gains. |
| 12 | ReAct: Synergizing Reasoning and Acting in LLMs | Yao et al. | 2022 | arXiv:2210.03629 | 90 | 92 | **91** | Interleaves reasoning traces and actions; enables tool-use + reasoning in single framework. |
| 13 | Reflexion: Language Agents with Verbal Reinforcement Learning | Shinn et al. | 2023 | arXiv:2303.11366 | 86 | 85 | **86** | Self-reflection via episodic memory across trials; verbal reinforcement without gradient updates. |
| 14 | Zero-shot CoT: Large Language Models are Zero-Shot Reasoners | Kojima et al. | 2022 | arXiv:2205.11916 | 90 | 92 | **91** | "Let's think step by step" trigger; zero-shot CoT without few-shot exemplars. |
| 15 | Take a Step Back: Evoking Reasoning via Abstraction in LLMs | Zheng et al. | 2023 | arXiv:2310.06117 | 82 | 74 | **78** | Forces abstract principle before solving; Step-Back Prompting reduces CoT failures. |
| 16 | Maieutic Prompting: Logically Consistent Reasoning with Recursive Explanations | Jung et al. | 2022 | arXiv:2205.11822 | 80 | 65 | **73** | Socratic recursive questioning; resolves internal inconsistencies in chain-of-thought. |
| 17 | Cumulative Reasoning with LLMs | Zhang et al. | 2023 | arXiv:2308.04371 | 78 | 62 | **70** | Incremental evidence accumulation before conclusion; mimics human deductive reasoning. |
| 18 | DIVERSE: Diverse Reasoning Strategies via Diverse Verifiers | Li et al. | 2023 | arXiv:2206.02336 | 76 | 68 | **72** | Diverse reasoning paths + voting verifiers; outperforms self-consistency on MATH. |
| 19 | Meta-CoT: Generalizable Chain-of-Thought Prompting in Mixed-task Scenarios | Yao et al. | 2024 | arXiv:2310.06671 | 78 | 65 | **72** | Multi-task CoT format detection + adaptive prompting; generalizes across task types. |
| 20 | Quiet-Star: Language Models Can Teach Themselves to Think Before Speaking | Zeiler et al. | 2024 | arXiv:2403.09629 | 88 | 80 | **84** | Token-level self-taught rationale generation; trains model to internally generate reasoning. |
| 21 | Show Your Work: Scratchpads for Intermediate Computation | Nye et al. | 2021 | arXiv:2112.00114 | 85 | 82 | **84** | Scratchpad paradigm precursor to CoT; write intermediate steps before final answer. |
| 22 | Scaling Relationship on Learning Mathematical Reasoning | Liao et al. | 2023 | arXiv:2308.01825 | 70 | 60 | **65** | Quantifies how much data and compute is needed for math reasoning gains. |
| 23 | Plan-and-Solve Prompting: Improving Zero-Shot CoT | Wang et al. | 2023 | arXiv:2305.04091 | 78 | 72 | **75** | "Plan first, then execute" two-stage zero-shot CoT; reduces CoT errors significantly. |
| 24 | Automatic Chain of Thought Prompting in LLMs | Zhang et al. | 2022 | arXiv:2210.11610 | 80 | 76 | **78** | Auto-CoT: clusters questions + samples diverse CoT examples automatically. |
| 25 | Multimodal Chain-of-Thought Reasoning in Language Models | Zhang et al. | 2023 | arXiv:2302.00923 | 82 | 78 | **80** | Extends CoT to vision-language tasks; two-stage rationale then answer generation. |
| 26 | Let's Think Dot by Dot: Hidden Computation in Transformer Language Models | Pfau et al. | 2024 | arXiv:2404.15758 | 84 | 65 | **75** | Single filler tokens carry computation equal to full reasoning chains; rethinks token budgets. |
| 27 | Skeleton-of-Thought: Large Language Models Can Do Parallel Decoding | Ning et al. | 2023 | arXiv:2307.15337 | 80 | 68 | **74** | Parallel sub-topic expansion via skeleton draft; 2× decoding speed without quality loss. |
| 28 | Algorithm of Thoughts: Enhancing Exploration of Ideas in LLMs | Sel et al. | 2023 | arXiv:2308.10379 | 76 | 60 | **68** | Algorithmic search strategies within CoT; outperforms ToT with fewer calls. |
| 29 | Chain of Symbol: Bridging Spatial Reasoning in LLMs | Hu et al. | 2024 | arXiv:2305.10276 | 75 | 56 | **66** | Symbolic spatial encoding before reasoning; major gain on spatial grid tasks. |
| 30 | Contrastive Chain Prompting | Chia et al. | 2023 | arXiv:2311.09277 | 72 | 58 | **65** | Correct+incorrect CoT pairs as contrastive examples; improves reasoning discrimination. |
| 31 | Structured Chain-of-Thought Prompting for Code Generation | Li et al. | 2023 | arXiv:2305.06599 | 75 | 65 | **70** | CoT with explicit structural constraints for code; sub-goal states guide code generation. |
| 32 | Boosting LLMs Reasoning via Analogical Prompts | He et al. | 2023 | arXiv:2310.01714 | 74 | 62 | **68** | Self-generated analogous examples before solving; analogical transfer improves performance. |
| 33 | Thread of Thought: Unraveling Chaotic Contexts | Zhou et al. | 2023 | arXiv:2311.08734 | 72 | 56 | **64** | Segments noisy long contexts into structured threads before reasoning; improves needle-in-haystack. |
| 34 | Metacognitive Prompting Improves Understanding in LLMs | Wang et al. | 2023 | arXiv:2308.05342 | 76 | 60 | **68** | Self-monitoring prompt strategies; LLM reflects on own reasoning quality before finalizing. |
| 35 | Monte Carlo Tree Search (MCTS) for LLM Planning | Zhao et al. | 2023 | arXiv:2309.17179 | 82 | 72 | **77** | MCTS applied to CoT; probabilistic search through reasoning space; strong on complex planning. |
| 36 | Thought Propagation: An Analogical Approach to Complex Reasoning | Yu et al. | 2024 | arXiv:2310.03965 | 75 | 60 | **68** | Propagates solutions from analogous problems to new cases; extends few-shot analogy learning. |
| 37 | Planning with Large Language Models via Corrective Re-prompting | Raman et al. | 2022 | arXiv:2208.09269 | 70 | 62 | **66** | Iterative error-correction loop for planning prompts; recovery from failed plan steps. |
| 38 | Reasoning Tokens: How Thinking Tags Affect LLM Performance | Various | 2025 | arXiv:2503.xyz | 80 | 60 | **70** | Analysis of <think> token paradigm in o1/R1-style models; impact on downstream prompting. |
| 39 | Self-Refine: Iterative Refinement with Self-Feedback | Madaan et al. | 2023 | arXiv:2303.17651 | 88 | 85 | **87** | Self-feedback loop for improvement; generate → critique → refine cycle without external supervision. |
| 40 | Process Reward Models for Enhanced Reasoning | Lightman et al. | 2023 | arXiv:2305.20050 | 90 | 88 | **89** | Step-level reward signals; process supervision outperforms outcome supervision for math. |
| 41 | Let's Verify Step by Step | Lightman et al. | 2023 | arXiv:2305.20050 | 88 | 85 | **87** | Human annotations for step verification; builds process reward models for reasoning chains. |
| 42 | GSM8K: Training Verifiers to Solve Math Word Problems | Cobbe et al. | 2021 | arXiv:2110.14168 | 85 | 90 | **88** | Grade school math benchmark; verifier-based reasoning with step-by-step solutions. |
| 43 | MATH: Measuring Mathematical Problem Solving | Hendrycks et al. | 2021 | arXiv:2103.03874 | 82 | 88 | **85** | Competition math benchmark; challenging problems requiring multi-step reasoning prompts. |
| 44 | Reasoning via Planning (RAP): Think Before Act | Hao et al. | 2023 | arXiv:2305.14992 | 84 | 78 | **81** | World model for reasoning planning; MCTS over reasoning states improves accuracy. |
| 45 | Buffer of Thoughts: Thought-Augmented Reasoning | Yang et al. | 2024 | arXiv:2406.04271 | 82 | 72 | **77** | Thought buffer storage; retrieves relevant reasoning patterns for new problems. |
| 46 | OpenAI o1 System: Learning to Reason | OpenAI | 2024 | OpenAI System Card | 92 | 92 | **92** | RLIF for reasoning; extended thinking chains via reinforcement learning—paradigm shift. |
| 47 | DeepSeek-R1: Reasoning with RL Without Supervision | DeepSeek | 2025 | arXiv:2501.12948 | 90 | 85 | **88** | Pure RL reasoning emergence; long CoT develops without supervised reasoning data. |
| 48 | s1: Simple Test-Time Scaling | Muennighoff et al. | 2025 | arXiv:2501.19393 | 85 | 78 | **82** | Test-time compute scaling; budget forcing for controllable reasoning depth. |
| 49 | Rethinking Reasoning: Can LLMs Truly Reason? | Huang et al. | 2024 | arXiv:2402.15989 | 78 | 72 | **75** | Reasoning capability analysis; distinguishes pattern matching from true reasoning. |
| 50 | Quiet-STaR: Language Models Can Teach Themselves to Think | Zelikman et al. | 2024 | arXiv:2403.09629 | 86 | 78 | **82** | Token-level rationale generation; self-taught internal reasoning without demonstrations. |

---

## 추가 예정 논문 (다음 업데이트 우선순위 대기열)

검색 대상:
- "self-refine prompting" (Madaan et al., 2023, arXiv:2303.17651)
- "forward-backward reasoning" NLP
- "natural program induction" LLMs
- "process reward models" prompt reasoning (Lightman 2023)
- "step-level reward" for reasoning
- "MATH" benchmark prompting papers (Hendrycks et al.)
- "Grade school math" GSM8K analysis papers
- "CodeT: Code Generation with Generated Tests" (Chen 2022)
- "OmegaPRM" (2024) — process reward model for math
- "Reasoning via Planning" (RAP) arXiv:2305.14992
- "Think Before You Act" decision-making prompting
- "Reward-guided Tree of Thought" papers
- "Hypothetical Document Embeddings (HyDE)" for reasoning
- arXiv 2025: "DeepSeek-R1" and "QwQ" reasoning model analysis papers
