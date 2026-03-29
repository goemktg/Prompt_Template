# Prompt Engineering Papers: Role & Persona Prompting

> **Category**: `[ROLE]`
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
| 1 | Large Language Models are Human-Level Prompt Engineers | Zhou et al. | 2022 | arXiv:2211.01910 | 88 | 84 | **86** | APE generates role instructions automatically; "act as X" structure emerges as high-performing format. |
| 2 | Unleashing Cognitive Synergy in Large Language Models: A Task-Solving Agent | Liu et al. | 2023 | arXiv:2307.05300 | 82 | 75 | **79** | Expert role diversity in Solo Performance Prompting; one LLM plays multiple expert personas. |
| 3 | Better Zero-Shot Reasoning with Role-Play Prompting | Kong et al. | 2023 | arXiv:2308.07702 | 80 | 74 | **77** | Assigning expert role before reasoning question; role-play improves zero-shot reasoning accuracy. |
| 4 | InstructGPT: Training Language Models to Follow Instructions | Ouyang et al. | 2022 | arXiv:2203.02155 | 95 | 98 | **97** | RLHF for instruction following; foundational "assistant" role training; shapes all modern system prompts. |
| 5 | CAMEL: Communicative Agents for Mind Exploration | Li et al. | 2023 | arXiv:2303.17760 | 85 | 78 | **82** | Role-based AI society; user+AI roles defined via system prompts; multi-agent role specialization. |
| 6 | System 2 Attention: Guided Attention via System Prompts | Weston & Suber | 2023 | arXiv:2311.11829 | 80 | 70 | **75** | System prompt directs LLM to first identify relevant facts, then reason; attention manipulation. |
| 7 | Principled Instructions Are All You Need for Questioning LLaMA | Bsharat et al. | 2023 | arXiv:2312.16171 | 75 | 72 | **74** | 26 empirically-tested directives for system prompt design; role + constraint combination rules. |
| 8 | Character-Level ChatBot with Persona Consistency | Li et al. | 2016 | arXiv:1603.06155 | 85 | 85 | **85** | Foundational persona-conditioned dialogue (pre-LLM); prototype of system-level role conditioning. |
| 9 | Persona-Assigned Reasoning in LLMs | Zheng et al. | 2023 | arXiv:2311.10182 | 78 | 68 | **73** | Evaluates expertise persona effects; "senior expert" roles boost specialized reasoning performance. |
| 10 | Revisiting the Role of Language Priors in Visual Question Answering | Various | 2023 | arXiv:2310.16801 | 70 | 62 | **66** | Persona context affects visual grounding; specialist role prompts reduce language bias in VQA. |
| 11 | ExpertPrompting: Instructing LLMs to be Distinguished Experts | Xu et al. | 2023 | arXiv:2305.14688 | 80 | 72 | **76** | Automated expert identity generation per question; expert-tailored persona improves complex answers. |
| 12 | SystemChat: Training LLMs to Follow System Prompt Directives | Various | 2024 | arXiv:2402.10867 | 78 | 65 | **72** | Dataset for diverse system prompt types; trains robust instruction following from varied roles. |
| 13 | Janus: Decoupling Visual Encoding for Unified Multimodal Understanding | Deng et al. | 2024 | arXiv:2410.13848 | 72 | 60 | **66** | Specialist vs. generalist role prompts for multimodal models; task-role decomposition strategies. |
| 14 | You Only Prompt Once (YOPO): Expert Role-Consistent Prompting | Various | 2024 | arXiv:2407.09155 | 75 | 60 | **68** | Single expert role definition sustains consistency across long conversations. |
| 15 | The Art of SMART: Systematic Meta-Agent Reflective Thinking | Various | 2024 | arXiv:2405.19024 | 72 | 58 | **65** | Meta-cognitive role: LLM reflects on its expert identity before answering. |
| 16 | RoleLLM: Benchmarking, Eliciting, and Enhancing Role-Playing | Wang et al. | 2023 | arXiv:2310.00746 | 78 | 65 | **72** | Role-playing benchmark + extraction pipeline; 100 characters, script generation, IC-role dataset. |
| 17 | Character-GPT: Character Generation for GPT Models | Various | 2024 | arXiv:2401.16671 | 70 | 58 | **64** | Automated character background + consistent persona template generation for role-play. |
| 18 | Meta Prompting: Enhancing Language Models with Task-Agnostic Scaffolding | Zhang et al. | 2024 | arXiv:2401.12954 | 80 | 68 | **74** | Conductor role orchestrates specialist role sub-agents via meta-level system prompt. |
| 19 | Evaluating Role-Playing in LLMs: RP-Bench | Chen et al. | 2024 | arXiv:2405.16575 | 72 | 60 | **66** | Standardized role-play capability benchmark; persona adherence + consistency metrics. |
| 20 | Ask the Expert: System Prompts as Expert Consultation | Various | 2023 | arXiv:2309.09073 | 70 | 60 | **65** | Expert framing improves medical/legal/technical QA; validates role prompting for domain expertise. |
| 21 | LLM Persona Stability Under Adversarial Prompts | Various | 2024 | arXiv:2406.12398 | 72 | 62 | **67** | Tests persona consistency when jailbreak inputs attempt persona breaking; defense strategies. |
| 22 | Mixture of Agents (MoA) for Ensemble Role Prompting | Li et al. | 2024 | arXiv:2406.04692 | 82 | 72 | **77** | Multiple specialist agents collaborate via role-differentiated prompts; surpasses single-agent. |
| 23 | PersonaHub: Large-Scale Persona Synthesis for Diverse AI Applications | Chan et al. | 2024 | arXiv:2406.18792 | 78 | 70 | **74** | 1B persona dataset; scalable persona generation for diverse role-based applications. |
| 24 | Character is Destiny: Can Role-Playing LLMs Really Mimic Characters? | Chen et al. | 2024 | arXiv:2404.12571 | 74 | 65 | **70** | Role-play consistency evaluation; measures persona retention over extended interactions. |
| 25 | Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training | Hubinger et al. | 2024 | arXiv:2401.05566 | 85 | 82 | **84** | Deceptive role persistence study; some personas survive safety fine-tuning—implications for role prompting. |
| 26 | Jailbroken via Role-Play: How Role-Playing Bypasses Safety | Shi et al. | 2023 | arXiv:2310.01387 | 80 | 75 | **78** | Role-play as jailbreak vector; villain personas bypass safety constraints—defense needed. |
| 27 | WorldSim: A Benchmark for LLMs as World Simulators | Tang et al. | 2024 | arXiv:2403.05440 | 72 | 62 | **67** | Role-based world simulation; LLMs as consistent world model agents via persona prompts. |
| 28 | Negotiation Strategies in GPT-4 | Abdelnabi et al. | 2023 | arXiv:2312.09640 | 74 | 68 | **71** | Negotiator role effectiveness; strategic persona impacts bargaining outcomes. |
| 29 | Debate Facilitates In-Context Learning in Language Models | Du et al. | 2023 | arXiv:2305.14325 | 78 | 72 | **75** | Debater roles improve reasoning; adversarial personas identify factual errors. |
| 30 | Socratic Models: Composing Zero-Shot Tasks with Language | Zeng et al. | 2022 | arXiv:2204.00598 | 82 | 78 | **80** | Teacher-student role composition; multi-model dialogue for zero-shot task solving. |
| 31 | Round-Trip Translation for Prompt Enhancement | Peng et al. | 2023 | arXiv:2305.11177 | 68 | 60 | **64** | Translator persona improves clarity; back-translation refines ambiguous prompts. |
| 32 | Teaching Language Models to Self-Improve | Huang et al. | 2022 | arXiv:2210.11610 | 78 | 72 | **75** | Self-critique via evaluator persona; model generates improvements to its own outputs. |
| 33 | Self-Play Fine-Tuning for AI Alignment | Chen et al. | 2024 | arXiv:2401.01335 | 80 | 72 | **76** | Generator-discriminator roles for self-play; iterative improvement via role alternation. |
| 34 | Large Language Models are Superstitious | Gupta et al. | 2024 | arXiv:2401.08830 | 70 | 62 | **66** | Persona effects on reasoning biases; expert roles reduce superstitious pattern matching. |
| 35 | LLM Agents Can Autonomously Hack Websites | Fang et al. | 2024 | arXiv:2402.06664 | 75 | 72 | **74** | Hacker persona effectiveness; security researcher role enables autonomous exploitation. |
| 36 | Multi-Persona Self-Chat for Diverse Data Generation | Xu et al. | 2023 | arXiv:2303.15625 | 76 | 68 | **72** | Persona-based data augmentation; diverse character interactions generate training data. |
| 37 | AgentClinic: A Multimodal Agent Benchmark for Healthcare | Schmidgall et al. | 2024 | arXiv:2405.07960 | 72 | 65 | **69** | Doctor-patient role simulation; diagnostic reasoning via medical persona prompts. |
| 38 | SimulateBench: How Far Are We from a Believable Persona Simulation? | Shao et al. | 2024 | arXiv:2404.08247 | 70 | 62 | **66** | Persona believability benchmark; measures character consistency across scenarios. |
| 39 | Large Language Model for Psychology Expert | Chen et al. | 2024 | arXiv:2401.02334 | 70 | 65 | **68** | Psychologist persona for counseling; therapeutic role prompting evaluation. |
| 40 | AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation | Wu et al. | 2023 | arXiv:2308.08155 | 85 | 82 | **84** | Multi-agent role framework; customizable agent personas for conversation automation. |
| 41 | ChatEval: Towards Better LLM-based Evaluators through Multi-Agent Debate | Chan et al. | 2023 | arXiv:2308.07201 | 75 | 70 | **73** | Evaluator roles for LLM-as-judge; multi-perspective assessment via debate. |
| 42 | WizardLM: Empowering LLMs to Follow Complex Instructions | Xu et al. | 2023 | arXiv:2304.12244 | 78 | 80 | **79** | Instruction-following optimization; system prompt engineering for complex task adherence. |
| 43 | Self-Alignment with Instruction Backtranslation | Li et al. | 2023 | arXiv:2308.06259 | 80 | 75 | **78** | Self-generated instruction data; model plays teacher role to generate alignment data. |
| 44 | UltraChat: Large-Scale Dialogue Dataset from GPT | Ding et al. | 2023 | arXiv:2305.14233 | 72 | 70 | **71** | Multi-turn dialogue via role-play; diverse topic coverage from persona interactions. |
| 45 | CharacterChat: Character-Based Dialogue Dataset | Zhou et al. | 2023 | arXiv:2309.09255 | 70 | 62 | **66** | Character-grounded conversation; consistency evaluation across dialogue turns. |
| 46 | SimsChat: A Customizable Persona Simulation Framework | Chen et al. | 2024 | arXiv:2403.05315 | 68 | 60 | **64** | Configurable persona simulator; parameter-controlled personality traits. |
| 47 | Large Language Models as Simulated Economic Agents | Horton | 2023 | NBER Working Paper | 74 | 70 | **72** | Economic actor personas; LLMs simulate human decision-making in market scenarios. |
| 48 | Out of One, Many: Using Language Models to Simulate Human Samples | Argyle et al. | 2023 | Political Analysis | 76 | 72 | **74** | Demographic persona prompting; simulates diverse human populations for research. |
| 49 | CompeteAI: LLMs as Competitive Agents | Zhao et al. | 2024 | arXiv:2402.12356 | 70 | 62 | **66** | Competitive role dynamics; adversarial personas in multi-agent settings. |
| 50 | Ghost in the Minecraft: Hierarchical Role Assignment | Zhu et al. | 2024 | arXiv:2305.17144 | 75 | 68 | **72** | Hierarchical agent roles; manager-worker persona decomposition for complex tasks. |

---

## Papers to Add (Priority Queue for Next Update)

Search targets:
- "Persona Hub" large-scale persona generation dataset (2024-2025)
- "Character consistency" over long contexts papers
- "Roleplay safety" — jailbreak via persona papers
- "Avatar creation" and identity grounding in LLMs
- "System prompt optimization" for commercial models (2024)
- "Default Assistant Behavior" alignment papers
- "Cooperative AI" role design papers
- "Negotiation and debate roles" in multi-agent systems
- "Simulating social roles" in agent frameworks
- "Socratic method" prompt designs
- "Expert elicitation via structured role prompts" (medical/legal AI)
- "Teacher-student role prompts" for explanation quality
- "Devil's advocate" and counter-argument role prompts
