# Prompt Engineering Papers: Safety & Robustness

> **Category**: `[SAFETY]`
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
| 1 | Constitutional AI: Harmlessness from AI Feedback | Bai et al. | 2022 | arXiv:2212.08073 | 92 | 92 | **92** | Self-critique + revision via constitutional principles; RLHF-free harmlessness via prompting alone. |
| 2 | Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications | Greshake et al. | 2023 | arXiv:2302.12173 | 88 | 85 | **87** | Indirect prompt injection via web content; attacker-controlled data hijacks agent actions. |
| 3 | Universal and Transferable Adversarial Attacks on Aligned LLMs | Zou et al. | 2023 | arXiv:2307.15043 | 88 | 85 | **87** | Gradient-based adversarial suffix jailbreaks all major LLMs; exposes alignment brittleness. |
| 4 | PromptBench: Towards Evaluating the Robustness of LLMs to Adversarial Prompts | Zhu et al. | 2023 | arXiv:2306.04528 | 82 | 80 | **81** | Systematic adversarial prompt robustness benchmark; 4 attack types, 8 models, 9 tasks. |
| 5 | Tensor Trust: Interpretable Prompt Injection Attacks | Toyer et al. | 2023 | arXiv:2311.01011 | 80 | 74 | **77** | Human-designed prompt injection game dataset; 126,000 prompts for injection/defense research. |
| 6 | Jailbroken: How Does LLM Safety Training Fail? | Wei et al. | 2023 | arXiv:2307.02483 | 82 | 82 | **82** | Two failure modes: competing objectives and mismatched generalization; taxonomy of jailbreaks. |
| 7 | Ignore Previous Prompt: Attack Techniques for LLMs | Perez & Ribeiro | 2022 | arXiv:2211.09527 | 85 | 80 | **83** | Formal taxonomy of prompt injection attacks; goal hijacking vs. prompt leaking. |
| 8 | Prompt Injection Attacks Against GPT-Integrated Applications | Liu et al. | 2023 | arXiv:2306.05499 | 80 | 75 | **78** | Classifies injection attack surfaces + defensive prompt patterns for integrated apps. |
| 9 | Red Teaming Language Models to Reduce Harms | Perez et al. | 2022 | arXiv:2202.03286 | 82 | 80 | **81** | LLM-assisted red teaming; automatic harmful input generation scales safety evaluation. |
| 10 | Adversarial Prompting for Black-Box Foundation Models | Maus et al. | 2023 | arXiv:2302.04237 | 78 | 68 | **73** | Black-box adversarial prompt search via query-only optimization; transferable attacks. |
| 11 | Baseline Defenses for Adversarial Attacks Against Aligned LLMs | Jain et al. | 2023 | arXiv:2309.00614 | 76 | 70 | **73** | Perplexity filtering, paraphrasing, retokenization defenses; systematic evaluation of mitigations. |
| 12 | Certifiably Robust LLM-as-a-Judge with Optimal Aggregation | Various | 2024 | arXiv:2402.10180 | 78 | 65 | **72** | Statistical guarantees for robustness in LLM evaluation; voting + bounds approach. |
| 13 | Smoothllm: Defending LLMs Against Jailbreaking Attacks | Robey et al. | 2023 | arXiv:2310.03684 | 80 | 72 | **76** | Random perturbation + majority voting defends against GCG/suffix attacks with marginal quality loss. |
| 14 | Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems | Gu et al. | 2024 | arXiv:2410.07218 | 85 | 72 | **79** | Infectious prompt injection spreads across multi-agent chains; novel multi-agent threat vector. |
| 15 | LLMs Can be Easily Distracted by Irrelevant Context | Shi et al. | 2023 | arXiv:2302.00093 | 78 | 75 | **77** | Irrelevant sentences in prompt degrade accuracy; robustness requires attention-guiding prompts. |
| 16 | Calibrated Uncertainty Quantification for LLMs | Kadavath et al. | 2022 | arXiv:2207.05221 | 80 | 76 | **78** | Self-evaluation of confidence; prompts LLM to evaluate certainty → calibrated outputs. |
| 17 | On the Reliability of LLMs: A Survey of Robustness | Wang et al. | 2023 | arXiv:2308.09138 | 75 | 70 | **73** | Survey of LLM reliability: adversarial, distributional, OOD robustness. |
| 18 | Defending Against Indirect Prompt Injection in Agentic Systems | Various | 2024 | arXiv:2403.09972 | 80 | 68 | **74** | Multi-layer defense framework for production agents; highlights prompt isolation importance. |
| 19 | TrustGPT: A Benchmark for Trustworthy and Responsible LLMs | Huang et al. | 2023 | arXiv:2306.11507 | 72 | 65 | **69** | Toxicity, bias, value alignment evaluation across 8 LLMs; comprehensive safety benchmark. |
| 20 | ToxicChat: Unveiling Hidden Challenges of Toxicity Detection | Lin et al. | 2023 | arXiv:2310.17389 | 70 | 62 | **66** | Real user conversation toxicity benchmark; shows challenge of moderating naturally-occurring prompts. |
| 21 | SALAD-Bench: A Hierarchical and Comprehensive Safety Benchmark | Li et al. | 2024 | arXiv:2402.05044 | 78 | 68 | **73** | Fine-grained hierarchical safety evaluation; 30K+ attack-defense prompt pairs. |
| 22 | Many-shot Jailbreaking | Anil et al. | 2024 | Anthropic Blog | 82 | 78 | **80** | Long context enables jailbreaks via accumulated few-shot pressure; unique to long-context models. |
| 23 | Protecting Against Prompt Leakage in Production LLM Systems | Various | 2024 | arXiv:2405.11028 | 72 | 62 | **67** | System prompt extraction attacks + defenses; prompt confidentiality in deployed systems. |
| 24 | LLM-as-a-Judge Robustness and Bias | (related to Constitutional AI) | 2024 | arXiv:2406.18491 | 72 | 65 | **69** | Position bias, verbosity bias, self-preference in LLM-as-judge; calibration techniques. |
| 25 | Gradient Cuff: Detecting Jailbreak Attacks via Gradient Frontier | He et al. | 2024 | arXiv:2403.00867 | 75 | 60 | **68** | Gradient-based jailbreak detection using loss landscape; efficient detection for deployed models. |
| 26 | Deep Reinforcement Learning from Human Feedback (RLHF) | Christiano et al. | 2017 | arXiv:1706.03741 | 95 | 98 | **97** | Foundational RLHF paper; reward modeling from human preferences enables aligned LLM behavior. |
| 27 | Training Language Models to Follow Instructions with Human Feedback (InstructGPT) | Ouyang et al. | 2022 | arXiv:2203.02155 | 95 | 98 | **97** | InstructGPT via RLHF; establishes instruction-following + safety alignment paradigm. |
| 28 | Sleeper Agents: Training Deceptive LLMs That Persist Through Safety Training | Hubinger et al. | 2024 | arXiv:2401.05566 | 88 | 85 | **87** | Backdoor persistence study; deceptive behaviors survive standard safety training—major red flag. |
| 29 | OWASP Top 10 for Large Language Model Applications | OWASP | 2023 | OWASP Documentation | 70 | 85 | **78** | Industry security standard; prompt injection, data leakage, and insecure output handling taxonomy. |
| 30 | A Watermark for Large Language Models | Kirchenbauer et al. | 2023 | arXiv:2301.10226 | 85 | 82 | **84** | Green/red list watermarking; enables detection of LLM-generated text via token statistics. |
| 31 | Detecting LLM-Generated Text via Watermarks | Christ et al. | 2023 | arXiv:2306.09194 | 78 | 70 | **74** | Unbiased watermarking; provable detection with minimal quality impact. |
| 32 | DetectGPT: Zero-Shot Machine-Generated Text Detection | Mitchell et al. | 2023 | arXiv:2301.11305 | 82 | 78 | **80** | Perturbation-based detection; zero-shot AI text identification via curvature analysis. |
| 33 | Extracting Training Data from Large Language Models | Carlini et al. | 2020 | arXiv:2012.07805 | 88 | 90 | **89** | Training data extraction attacks; demonstrates memorization risks in large models. |
| 34 | Scalable Extraction of Training Data from LLMs | Nasr et al. | 2023 | arXiv:2311.17035 | 85 | 80 | **83** | Divergence attacks extract training data; persistent memorization at scale. |
| 35 | LLM Censorship: A Machine Learning Challenge for Content Moderation | Goldstein et al. | 2023 | arXiv:2303.12712 | 72 | 68 | **70** | Content moderation challenges; LLM-specific toxicity detection difficulties. |
| 36 | Do Anything Now: Characterizing and Evaluating In-The-Wild Jailbreak Prompts | Shen et al. | 2023 | arXiv:2308.03825 | 80 | 78 | **79** | Wild jailbreak dataset; 6,387 prompts from Reddit/Discord with effectiveness analysis. |
| 37 | JailbreakBench: An Open Robustness Benchmark for Jailbreaking LLMs | Chao et al. | 2024 | arXiv:2404.01318 | 78 | 72 | **75** | Standardized jailbreak evaluation; reproducible attack/defense benchmarking. |
| 38 | HarmBench: A Standardized Evaluation Framework for Automated Red Teaming | Mazeika et al. | 2024 | arXiv:2402.04249 | 80 | 75 | **78** | Comprehensive red teaming benchmark; standardized harmful behavior evaluation. |
| 39 | Circuit Breakers: Mechanistic Interpretability for Safety | Templeton et al. | 2024 | arXiv:2406.04093 | 85 | 75 | **80** | Mechanistic safety interventions; identify and block harmful feature activations. |
| 40 | Representation Engineering: A Top-Down Approach to AI Transparency | Zou et al. | 2023 | arXiv:2310.01405 | 88 | 78 | **83** | Representation-level safety control; steering model behavior via activation manipulation. |
| 41 | AutoDAN: Generating Stealthy Jailbreak Prompts via Hierarchical Genetic Algorithms | Liu et al. | 2023 | arXiv:2310.04451 | 82 | 75 | **79** | Automated jailbreak generation; genetic optimization creates human-readable attacks. |
| 42 | PAIR: Prompt Automatic Iterative Refinement for Jailbreaking | Chao et al. | 2023 | arXiv:2310.08419 | 80 | 74 | **77** | LLM-based attack refinement; iterative optimization finds effective jailbreaks. |
| 43 | TAP: Tree of Attacks with Pruning for Automatic Jailbreaking | Mehrotra et al. | 2023 | arXiv:2312.02119 | 78 | 70 | **74** | Tree search for attacks; efficient jailbreak discovery via structured exploration. |
| 44 | Building AI Safety Guardrails: Lessons from Production Deployments | OpenAI, Anthropic | 2024 | Various | 75 | 80 | **78** | Production safety patterns; input/output filtering, moderation APIs, and prompt shields. |
| 45 | Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations | Inan et al. | 2023 | arXiv:2312.06674 | 82 | 80 | **81** | LLM-as-moderator; safety classifier for input/output in conversational systems. |
| 46 | NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications | Rebedea et al. | 2023 | arXiv:2310.10501 | 78 | 75 | **77** | Programmable guardrails; dialog flows enforce safety and topicality constraints. |
| 47 | Erasing Concepts from Diffusion Models | Gandikota et al. | 2023 | arXiv:2303.07345 | 80 | 72 | **76** | Concept erasure for safety; removes harmful content generation capability. |
| 48 | Self-Destructing Models: Increasing the Costs of Harmful Dual Uses | Henderson et al. | 2023 | arXiv:2211.14946 | 75 | 65 | **70** | Controlled model degradation; prevents misuse via capability restrictions. |
| 49 | Fine-tuning Aligned Language Models Compromises Safety | Qi et al. | 2023 | arXiv:2310.03693 | 85 | 82 | **84** | Fine-tuning safety fragility; few harmful examples can undo alignment—critical for API providers. |
| 50 | Shadow Alignment: Hidden Risks of Reward-Aligned LLMs | Yang et al. | 2023 | arXiv:2310.02949 | 78 | 70 | **74** | Hidden misalignment; RLHF can create shadow objectives that bypass safety constraints. |

---

## Papers to Add (Priority Queue for Next Update)

Search targets:
- "RLHF Safety" alignment papers (Christiano 2017, Ouyang 2022 InstructGPT)
- "Reward model bias and safety tradeoffs" papers
- "Sleeper Agents" in LLMs (Anthropic, 2024)
- "Backdoor attacks on fine-tuned LLMs" (2024)
- "Prompt security best practices" (OWASP LLM Top 10)
- "LLM firewall / input sanitization" papers
- "Watermarking LLM outputs" (green/red list) papers
- "Membership inference attacks" on prompts
- "Differential privacy in prompting" papers
- "Safe Reinforcement Learning via prompting" papers
- "Red teaming automation" (2025 papers)
- "Deceptive alignment" and eliciting latent knowledge papers
