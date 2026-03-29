# Prompt Engineering Papers: Agent & Multi-Step Prompting

> **Category**: `[AGENT]`
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
| 1 | ReAct: Synergizing Reasoning and Acting in LLMs | Yao et al. | 2022 | arXiv:2210.03629 | 92 | 94 | **93** | Interleaves Thought–Action–Observation loops; foundation for tool-using agent prompting. |
| 2 | Toolformer: Language Models Can Teach Themselves to Use Tools | Schick et al. | 2023 | arXiv:2302.04761 | 90 | 88 | **89** | Self-supervised API call insertion; models learn when/how to call tools from data. |
| 3 | HuggingGPT: Solving AI Tasks with ChatGPT and Models in HuggingFace | Shen et al. | 2023 | arXiv:2303.17580 | 85 | 82 | **84** | LLM as controller orchestrating specialized HuggingFace models via structured planning prompts. |
| 4 | Generative Agents: Interactive Simulacra of Human Behavior | Park et al. | 2023 | arXiv:2304.03442 | 90 | 92 | **91** | 25-agent sandbox with memory, reflection, planning prompts; foundational multi-agent simulation. |
| 5 | AutoGPT / BabyAGI-style Task Decomposition | Richards et al. | 2023 | Blog/GitHub | 82 | 90 | **86** | Recursive autonomous task creation and execution; popularized long-horizon agent prompting. |
| 6 | ToolBench: Facilitating LLMs to Master Tools via Tool Learning | Qin et al. | 2023 | arXiv:2307.16789 | 85 | 80 | **83** | 16,000+ real APIs; trains LLMs on tool-selection and multi-step API orchestration. |
| 7 | AgentBench: Evaluating LLMs as Agents | Liu et al. | 2023 | arXiv:2308.03688 | 78 | 80 | **79** | 8-environment benchmark; first comprehensive evaluation of LLM agent prompting strategies. |
| 8 | CAMEL: Communicative Agents for Mind Exploration | Li et al. | 2023 | arXiv:2303.17760 | 85 | 78 | **82** | Role-based dual-agent communication; systematic exploration of agent-agent interaction. |
| 9 | MetaGPT: Meta Programming for Multi-Agent Collaborative Framework | Hong et al. | 2023 | arXiv:2308.00352 | 85 | 82 | **84** | Assigns SOP-based roles to agents; structured multi-agent software development framework. |
| 10 | Voyager: An Open-Ended Embodied Agent with LLMs | Wang et al. | 2023 | arXiv:2305.16291 | 88 | 80 | **84** | Lifelong learning Minecraft agent; skill library grows via iterative prompting + code execution. |
| 11 | OpenAgents: An Open Platform for Language Agents in the Wild | Xie et al. | 2023 | arXiv:2310.10634 | 80 | 72 | **76** | Open-source agent platform; data, plugin, and web agents with natural conversation interface. |
| 12 | Ghost in the Minecraft: Generally Capable Agents | Zhu et al. | 2023 | arXiv:2305.17144 | 78 | 68 | **73** | Goal-directed agent prompting; sub-goal planning + goal verification in Minecraft. |
| 13 | Communicative Agents for Software Development (ChatDev) | Qian et al. | 2023 | arXiv:2307.07924 | 82 | 78 | **80** | Multi-agent waterfall: CEO → CTO → programmer → tester; prompt-driven software lifecycle. |
| 14 | AgentSims: An Open-Source Sandbox for LLM Agent Evaluation | Lin et al. | 2023 | arXiv:2308.04026 | 72 | 62 | **67** | Sandbox environment for agent behavior simulation and evaluation. |
| 15 | Cognitive Architectures for Language Agents | Sumers et al. | 2023 | arXiv:2309.02427 | 80 | 70 | **75** | Memory + action + decision-making framework; maps cognitive architecture patterns to LLM agent prompts. |
| 16 | Self-Debugging: Teaching Large Code Models to Self-Debug | Chen et al. | 2023 | arXiv:2304.05128 | 82 | 76 | **79** | LLM uses execution output to iteratively debug its own code; closed-loop agent prompting. |
| 17 | WebGPT: Browser-Assisted Question-Answering with Human Feedback | Nakano et al. | 2021 | arXiv:2112.09332 | 88 | 82 | **85** | Trains LLM to browse web; reward model from human preferences; early web-agent prompting. |
| 18 | WebAgent: A Real-world WebAgents with Planning, Long Context | Gur et al. | 2023 | arXiv:2307.12856 | 80 | 70 | **75** | HTML-understanding + planning prompts for real website task execution. |
| 19 | Agents: An Open-source Framework for Autonomous Language Agents | Zhou et al. | 2023 | arXiv:2309.07870 | 75 | 70 | **73** | Open framework standardizing agent loop: plan → observe → act → reflect. |
| 20 | LLM+P: Empowering LLMs with Classical Planners | Liu et al. | 2023 | arXiv:2304.11477 | 78 | 65 | **72** | Translates NL tasks to PDDL, solves with classical planner, translates back; hybrid agent. |
| 21 | Self-RAG: Learning to Retrieve, Generate, and Critique | Asai et al. | 2023 | arXiv:2310.11511 | 88 | 82 | **85** | Agentic retrieval with self-evaluation; reflection tokens guide when/what to retrieve. |
| 22 | CLIN: A Continually Learning Language Agent for Rapid Task Adaptation | Majumder et al. | 2023 | arXiv:2310.10134 | 78 | 62 | **70** | Memory-augmented agent that improves within and across episodes via causal hypothesis storage. |
| 23 | AgentTuning: Enabling Generalized Agent Abilities for LLMs | Zeng et al. | 2023 | arXiv:2310.12823 | 80 | 68 | **74** | Interleaved general + agent data fine-tuning; preserves general capability while adding agent skills. |
| 24 | Describe, Explain, Plan and Select (DEPS) | Wang et al. | 2023 | arXiv:2302.01560 | 76 | 64 | **70** | Structured plan generation with critic-guided selection; improves long-horizon planning. |
| 25 | AppAgent: Multimodal Agents as Smartphone Users | Yang et al. | 2023 | arXiv:2312.13771 | 80 | 68 | **74** | Vision-based GUI agent operating smartphones via touch; learns from exploration + docs. |
| 26 | OS-Copilot: Towards Generalist Computer Agents | Wu et al. | 2024 | arXiv:2402.07456 | 82 | 70 | **76** | OS-level agent integrating file, web, shell, and app tools; self-directed skill learning. |
| 27 | MemoryBank: Enhancing Large Language Models with Long-Term Memory | Zhong et al. | 2023 | arXiv:2305.10250 | 80 | 68 | **74** | Hierarchical memory for agents; episodic + semantic long-term storage with LLM retrieval. |
| 28 | TaskBench: Benchmarking LLMs in Task Automation | Shen et al. | 2023 | arXiv:2311.18760 | 72 | 62 | **67** | Multi-step tool orchestration benchmark; tests agent prompt planning accuracy. |
| 29 | Multi-Agent Debate Improves Reasoning Accuracy | Du et al. | 2023 | arXiv:2305.14325 | 82 | 72 | **77** | Multiple agents argue positions, then resolve; debate dynamics improve factual accuracy over single-agent. |
| 30 | OpenHands: An Open Platform for AI Software Agents | Various | 2024 | arXiv:2407.16741 | 80 | 72 | **76** | Full-stack open-source software agent platform; state-of-the-art on SWE-bench. |
| 31 | AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation | Wu et al. | 2023 | arXiv:2308.08155 | 88 | 85 | **87** | Multi-agent conversation framework; customizable agent interactions for complex tasks. |
| 32 | SWE-Agent: Agent-Computer Interfaces Enable LLMs as Software Engineers | Yang et al. | 2024 | arXiv:2405.15793 | 88 | 82 | **85** | Agent-Computer Interface design; structured command vocabulary for code tasks. |
| 33 | Cradle: Empowering Foundation Agents Towards General Computer Control | Zhang et al. | 2024 | arXiv:2403.03186 | 82 | 75 | **79** | General computer control agent; game-playing via visual-language prompting. |
| 34 | AgentGym: Evolving Large Language Model-based Agents across Diverse Environments | Xi et al. | 2024 | arXiv:2406.04151 | 78 | 70 | **74** | Unified agent training platform; cross-environment generalization via curriculum. |
| 35 | PC Agent: While You Sleep, AI Works | Li et al. | 2025 | arXiv:2501.15678 | 80 | 72 | **76** | Overnight computer agent; autonomous task execution with human review in morning. |
| 36 | Claude Computer Use | Anthropic | 2024 | Blog/Docs | 85 | 85 | **85** | Native computer use API; structured screenshot and action prompting for automation. |
| 37 | Browser Use: Web Browsing Agents via Prompting | Various | 2024 | arXiv:2406.18123 | 76 | 72 | **74** | Browser automation agents; DOM parsing and action selection via structured prompts. |
| 38 | Mixture-of-Agents Achieves GPT-4 Level Performance | Li et al. | 2024 | arXiv:2406.04692 | 85 | 78 | **82** | Mixture-of-Agents (MoA); combining multiple LLMs via layered agent prompting. |
| 39 | CrewAI: A Framework for Orchestrating Role-Playing Agents | Moura | 2024 | GitHub/Docs | 72 | 75 | **74** | Role-based multi-agent framework; task-focused agent crew composition. |
| 40 | LangGraph: Building Stateful, Multi-Actor LLM Applications | LangChain | 2024 | Documentation | 75 | 78 | **77** | Graph-based agent orchestration; state machine for complex multi-step agent workflows. |
| 41 | Agent Protocol: Standardizing LLM Agent Communication | Various | 2024 | GitHub | 68 | 72 | **70** | Standardized agent API; interoperability between different agent frameworks. |
| 42 | AgentScope: A Flexible yet Robust Multi-Agent Platform | Gao et al. | 2024 | arXiv:2402.14034 | 74 | 68 | **71** | Distributed multi-agent system; fault-tolerant agent coordination. |
| 43 | Internet Explorer: Targeted Representation Learning on the Internet | Shi et al. | 2024 | arXiv:2312.14652 | 75 | 68 | **72** | Web exploration agent; self-supervised learning from browsing trajectories. |
| 44 | WebArena: A Realistic Web Environment for Building Agents | Zhou et al. | 2023 | arXiv:2307.13854 | 82 | 78 | **80** | Real website agent benchmark; end-to-end web task completion evaluation. |
| 45 | OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks | Xie et al. | 2024 | arXiv:2404.07972 | 80 | 74 | **77** | Full OS environment benchmark; desktop application manipulation tasks. |
| 46 | Mind2Web: Towards a Generalist Web Agent | Deng et al. | 2024 | arXiv:2306.06070 | 78 | 74 | **76** | Large-scale web agent dataset; 2,000+ tasks across 137 websites. |
| 47 | OSCopilot: End-to-End GUI Agent for General Operating Systems | Wu et al. | 2024 | arXiv:2402.07456 | 80 | 72 | **76** | OS-level assistant; learns to use applications via interaction history. |
| 48 | Agent Hospital: A Simulacrum of Hospital with Evolvable Medical Agents | Li et al. | 2024 | arXiv:2405.02957 | 74 | 65 | **70** | Medical simulation via agents; evolving doctor-patient agent interactions. |
| 49 | WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks? | Drouin et al. | 2024 | arXiv:2403.07718 | 76 | 70 | **73** | Enterprise task benchmark; ServiceNow-based knowledge work evaluation. |
| 50 | AgentStudio: A Toolkit for Building General Virtual Agents | Zheng et al. | 2024 | arXiv:2403.17918 | 72 | 65 | **69** | GUI agent toolkit; observation and action space standardization. |

---

## Papers to Add (Priority Queue for Next Update)

Search targets:
- "Cradle: Empowering Foundation Agents" (2024) game agents
- "SWE-Agent: Agent-Computer Interfaces Enable LLMs as Software Engineering Agents" (2024)
- "Claude's Constitutional AI" as agent principle
- "AI Agents in Business Automation" (2025 papers)
- "LangChain / LangGraph architecture papers" (2024)
- "CrewAI multi-agent framework" evaluation papers
- "AutoGen: Enabling Next-Gen LLM Applications" (Wu et al., 2023, arXiv:2308.08155)
- "REACT + ToolBench integration" studies
- "Agent alignment and safety" (2024-2025)
- "Mixture-of-Agents" (MoA) — Li et al., 2024
- "AgentGym: Evolving LLM-based Agents" (2024)
- "PC Agent: While You Sleep" (2025) — computer use agents
- "Browser Use" and "Computer Use" API papers (Anthropic, 2024)
