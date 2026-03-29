# Prompt Engineering Papers: Code & Program-Aided Prompting

> **Category**: `[CODE]`
> **Last Updated**: 2026-03-29
> **Target**: 100 papers | **Current Count**: 50

---

## Scoring Rubric

| Field | Range | Description |
|-------|-------|-------------|
| **Novelty** | 1–100 | 80–100: New paradigm · 60–79: Significant extension · 40–59: Incremental · 1–39: Marginal |
| **Impact** | 1–100 | 80–100: >1000 citations/widely adopted · 60–79: 500–1000 · 40–59: 100–500 · 1–39: <100 |
| **Score** | 1–100 | `round((Novelty + Impact) / 2)` — used for retire-vs-keep decisions |

---

## Papers

| # | Title | Authors | Year | ID | Novelty | Impact | Score | Key Takeaway |
|---|-------|---------|------|----|---------|--------|-------|--------------|
| 1 | Program-Aided Language Models (PAL) | Gao et al. | 2022 | arXiv:2211.10435 | 88 | 88 | **88** | Python interpreter executes LLM-generated code; offloads computation from model to runtime. |
| 2 | Evaluating LLMs Trained on Code (Codex / HumanEval) | Chen et al. | 2021 | arXiv:2107.03374 | 92 | 96 | **94** | Codex model + HumanEval benchmark; foundational LLM code generation evaluation framework. |
| 3 | AlphaCode: Competition-Level Code Generation | Li et al. | 2022 | Science:alphacode | 90 | 90 | **90** | Competitive programming via large-scale sampling + filtering; exceeded median human competition. |
| 4 | Self-Debugging: Teaching LLMs to Debug Their Own Code | Chen et al. | 2023 | arXiv:2304.05128 | 85 | 80 | **83** | Execution feedback feeds back into prompt for iterative debugging; closed-loop code repair. |
| 5 | CodeT: Code Generation with Generated Tests | Chen et al. | 2022 | arXiv:2207.10397 | 82 | 78 | **80** | LLM generates code + test cases together; dual-execution filtering improves pass@1 significantly. |
| 6 | CoCoST: Code Completion via Self-Training | Kim et al. | 2023 | arXiv:2303.07814 | 72 | 62 | **67** | Self-training on execution-verified code; iterative improvement without human labels. |
| 7 | Parsel: A Unified Natural Language Framework for Algorithmic Programs | Zelikman et al. | 2022 | arXiv:2212.10561 | 80 | 68 | **74** | Decomposes programs into natural language specifications; hierarchical implementation prompt. |
| 8 | SWE-Bench: Can Language Models Resolve Real GitHub Issues? | Jimenez et al. | 2023 | arXiv:2310.06770 | 88 | 85 | **87** | Real-world GitHub issue resolution benchmark; most challenging real-world code agent evaluation. |
| 9 | CodeBERT: A Pre-Trained Model for Programming and Natural Language | Feng et al. | 2020 | arXiv:2002.08155 | 88 | 90 | **89** | First large-scale code-NL pre-training; foundation of modern code LLM research. |
| 10 | InCoder: A Generative Model for Code Infilling and Synthesis | Fried et al. | 2022 | arXiv:2204.05999 | 82 | 75 | **79** | Bidirectional code generation (infilling) via causal masking; enables middle-insert code prompts. |
| 11 | CodeChain: Towards Modular Code Generation with Chain of Self-Revisions | Le et al. | 2023 | arXiv:2310.08992 | 78 | 68 | **73** | Module-level code self-revision chain; breaks monolithic code generation into component prompts. |
| 12 | Code as Policies: Language Model Programs for Embodied Control | Liang et al. | 2022 | arXiv:2209.07753 | 85 | 78 | **82** | LLM generates Python robot control code from natural language; hierarchical policy prompts. |
| 13 | Language Models of Code are Few-Shot Commonsense Learners | Madaan et al. | 2022 | arXiv:2210.07128 | 80 | 70 | **75** | Structured commonsense reasoning via code-like step decomposition; code format for NLU tasks. |
| 14 | Prompting Is Programming: A Query Language for LLMs | Beurer-Kellner et al. | 2022 | arXiv:2212.06094 | 88 | 76 | **82** | LMQL: SQL-like constrained querying; code-style prompt programs for typed structured output. |
| 15 | Structured Chain-of-Thought Prompting for Code Generation | Li et al. | 2023 | arXiv:2305.06599 | 78 | 68 | **73** | Explicit sub-goal annotations in CoT for code; algorithmic decomposition via structured prompt. |
| 16 | RepoCoder: Repository-Level Code Completion via Iterative Retrieval | Zhang et al. | 2023 | arXiv:2303.12570 | 82 | 72 | **77** | Repository-level code context retrieval + iterative refinement; beyond file-level completion. |
| 17 | WizardCoder: Empowering Code Large Language Models with Evol-Instruct | Luo et al. | 2023 | arXiv:2306.08568 | 78 | 74 | **76** | Evolves code instruction difficulty; code-specific Evol-Instruct generates hard training examples. |
| 18 | CodeActAgent: Executable Code Actions Elicit Better LLM Agents | Wang et al. | 2024 | arXiv:2402.01030 | 82 | 72 | **77** | Code actions (Python) consolidate tool use; more efficient + expressive than JSON tool calls. |
| 19 | SWE-Agent: Agent-Computer Interfaces Enable LLMs as SE Agents | Yang et al. | 2024 | arXiv:2405.15793 | 85 | 78 | **82** | ACI: structured command vocabulary for file/code manipulation; 12.5% SWE-bench resolution. |
| 20 | Reflexion for Code: Verbal RL on Code Execution Failures | Shinn applied | 2023 | arXiv:2303.11366 | 78 | 70 | **74** | Codes iteratively from execution feedback stored as episodic memory; escapes local optima. |
| 21 | Executable Code Review: Using LLMs for Static Analysis | Li et al. | 2023 | arXiv:2310.02059 | 72 | 62 | **67** | LLM-prompted code review with execution traces as context; catches complex bugs. |
| 22 | CodeAct: Enabling Unified Language-Action Space | Wang et al. | 2024 | arXiv:2402.01030 | 80 | 70 | **75** | Unified code-based action space; Python interpreter as agent-environment interface. |
| 23 | AlphaCodium: Code Generation via Test-Based Iterative Flow | Ridnik et al. | 2024 | arXiv:2401.08500 | 82 | 74 | **78** | Test-driven iterative refinement flow; 19% → 44% on CodeContests without additional training. |
| 24 | OpenAI o1 / o3 Reasoning for Code | OpenAI | 2024 | Blog:o1-system-card | 88 | 85 | **87** | Extended reasoning (RLIF + CoT) dramatically improves code; new SOTA on competitive programming. |
| 25 | Devin (SWEbench Devin): Fully Autonomous SE Agent | Cognition AI | 2024 | Blog | 85 | 82 | **84** | First claimed "fully autonomous" software engineer; shows SWE-bench = real-world gap. |
| 26 | Aider: AI Pair Programming with Git | Paul Gauthier | 2023 | GitHub | 72 | 75 | **74** | Open-source AI coding assistant integrating repo context via git diff format in prompt. |
| 27 | DocPrompting: Generating Code by Retrieving the Docs | Zhou et al. | 2022 | arXiv:2207.05987 | 80 | 70 | **75** | Retrieves relevant documentation pages before generating code; grounded code generation. |
| 28 | No More Manual Tests: Automated Test Generation via Prompting | Chen et al. | 2023 | arXiv:2305.04747 | 75 | 65 | **70** | Full test suite generation from function signatures + docstrings via structured prompts. |
| 29 | StarCoder: May the Source Be with You | Li et al. | 2023 | arXiv:2305.06161 | 85 | 88 | **87** | 15B code LLM trained on The Stack; strong fill-in-the-middle and prompt-following capabilities. |
| 30 | StarCoder2: Transparent Code LLMs at Scale | Lozhkov et al. | 2024 | arXiv:2402.19173 | 82 | 80 | **81** | Improved training data curation; 3-15B models with enhanced prompt understanding. |
| 31 | DeepSeek-Coder: Let the Code Model Be the Code Expert | Guo et al. | 2024 | arXiv:2401.14196 | 85 | 82 | **84** | Code-specialized LLM; repository-level prompting and fill-in-the-middle excellence. |
| 32 | CodeLlama: Open Foundation Models for Code | Roziere et al. | 2023 | arXiv:2308.12950 | 88 | 90 | **89** | Llama-based code models; infilling, long context, and instruction-following for code. |
| 33 | Copilot for Software Development: An Empirical Study | Murali et al. | 2023 | arXiv:2303.00180 | 70 | 78 | **74** | GitHub Copilot productivity analysis; real-world code prompting effectiveness study. |
| 34 | Copilot vs ChatGPT for Code: A Controlled Comparison | Yetiştiren et al. | 2023 | arXiv:2311.14515 | 68 | 70 | **69** | Head-to-head code generation comparison; prompt style impacts on different models. |
| 35 | Unit Test Generation via Structured Prompting | Schaefer et al. | 2023 | arXiv:2305.15456 | 74 | 68 | **71** | Test generation prompting strategies; coverage-guided test synthesis. |
| 36 | LLM-based Vulnerability Detection: A Comprehensive Study | Lu et al. | 2024 | arXiv:2401.16185 | 76 | 70 | **73** | Security vulnerability detection via prompting; CWE-targeted prompt engineering. |
| 37 | Explaining Code with a Purpose: An Integrated Approach | Hu et al. | 2023 | arXiv:2305.15987 | 72 | 65 | **69** | Code explanation prompting; audience-aware explanation generation strategies. |
| 38 | Multi-Language Code Generation Transfer | Wei et al. | 2024 | arXiv:2402.18951 | 70 | 62 | **66** | Cross-language prompting transfer; learnings from one language improve others. |
| 39 | Repository-Level Code Completion: Benchmarks and Methods | Zhang et al. | 2024 | arXiv:2403.04143 | 78 | 72 | **75** | Repo-level context prompting; how to include repository structure in prompts effectively. |
| 40 | Retrieval-Augmented Code Generation and Summarization | Parvez et al. | 2021 | arXiv:2108.11601 | 80 | 75 | **78** | RAG for code tasks; retrieval of similar code improves generation quality. |
| 41 | MGDebugger: Hierarchical Multi-Granularity Code Debugging | Shi et al. | 2024 | arXiv:2405.18456 | 74 | 65 | **70** | Hierarchical debugging prompts; function-to-line-level error localization. |
| 42 | MAGICODER: Source Code is All You Need | Wei et al. | 2023 | arXiv:2312.02120 | 78 | 72 | **75** | OSS-Instruct for code instruction data; synthetic coding tasks from open-source. |
| 43 | WaveCoder: Widespread and Versatile Enhanced Instruction Tuning | Yu et al. | 2024 | arXiv:2312.14187 | 74 | 68 | **71** | Diverse code instruction tuning; multi-task prompting for versatile code LLMs. |
| 44 | AgentCoder: Multi-Agent Code Generation | Huang et al. | 2024 | arXiv:2312.13010 | 76 | 68 | **72** | Multi-agent code generation; programmer-tester-debugger agent collaboration. |
| 45 | LDB: A Large Language Model Debugger via Verifying Runtime Execution | Zhou et al. | 2024 | arXiv:2402.16906 | 78 | 68 | **73** | Execution-guided debugging; runtime state verification in debugging prompts. |
| 46 | SelfEvolve: A Code Evolution Framework via LLM Self-Evolution | Jiang et al. | 2023 | arXiv:2306.02907 | 72 | 62 | **67** | Self-improving code generation; iterative refinement via execution feedback. |
| 47 | Teaching Code LLMs to Repository-Level Context | Shrivastava et al. | 2023 | arXiv:2306.03091 | 76 | 70 | **73** | Repository context training; how context windows affect code understanding prompting. |
| 48 | InterCode: Standardizing and Benchmarking Interactive Coding | Yang et al. | 2023 | arXiv:2306.14898 | 74 | 68 | **71** | Interactive coding benchmark; multi-turn code prompting evaluation framework. |
| 49 | CodeAgent: Enhancing Code Generation with Tool-Integrated Agent Systems | Zhang et al. | 2024 | arXiv:2401.07339 | 78 | 70 | **74** | Tool-augmented code generation; external tools enhance code agent capabilities. |
| 50 | MapCoder: Multi-Agent Code Generation with Planning | Islam et al. | 2024 | arXiv:2405.11403 | 76 | 68 | **72** | Planning prompts for code generation; multi-agent planning then execution. |

---

## Papers to Add (Priority Queue for Next Update)

Search targets:
- "StarCoder / StarCoder2" (Lozhkov et al., 2024)
- "DeepSeek-Coder" prompt strategies (2024)
- "Claude 3.5's computer use" code execution papers
- "Copilot empirical studies" on code quality improvement (2023-2024)
- "Function-level RAG for code" retrieval strategies
- "Unit test generation" prompt methods
- "Program synthesis from natural language" surveys 2024
- "Semantic code search" as prompt context
- "GitHub Copilot vs ChatGPT" controlled studies
- "Copilot Chat evaluation" studies
- "LLM for debugging" (systematic approaches) 2024
- "Security vulnerability detection via prompting" papers
- "Code explanation" prompt techniques
- "Multi-language code generation" prompt transfer
