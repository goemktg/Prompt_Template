# 프롬프트 엔지니어링 논문: 설문 조사 및 개요

> **카테고리**: `[SURVEY]`
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
| 1 | The Prompt Report: A Systematic Survey of Prompting Techniques | Schulhoff et al. | 2024 | arXiv:2406.06608 | 80 | 90 | **85** | 58 text techniques + 40 multilingual/multimodal; best single inventory of prompting methods. |
| 2 | A Systematic Survey of Prompt Engineering in LLMs: Techniques and Applications | Sahoo et al. | 2025 | arXiv:2402.07927v2 | 75 | 88 | **82** | Updated Mar 2025; 58+ techniques categorized by task; includes Chain of Draft (2025). |
| 3 | A Systematic Survey of Automatic Prompt Optimization Techniques | Ramnath et al. | 2025 | arXiv:2502.16923 | 78 | 72 | **75** | Comprehensive 5-part APO framework; categorizes all APO techniques. |
| 4 | A Survey of Automatic Prompt Engineering: An Optimization Perspective | Li, Wang et al. | 2025 | arXiv:2502.11560 | 76 | 70 | **73** | Unified discrete/continuous/hybrid prompt optimization framework. |
| 5 | A Comprehensive Survey of Prompt Engineering Techniques in LLMs | Various | 2025 | TechRxiv:1274333 | 65 | 60 | **63** | Zero-shot through advanced structured prompts systematically compared. |
| 6 | Pre-train, Prompt, and Predict: Prompting Methods Survey | Liu et al. | 2021 | arXiv:2107.13586 | 92 | 98 | **95** | Foundational academic survey; defines the prompt engineering field from NLP perspective. |
| 7 | Reasoning with Language Model Prompting: A Survey | Qiao et al. | 2022 | arXiv:2212.09597 | 72 | 82 | **77** | Survey of reasoning-via-prompting spanning symbolic, CoT, and knowledge-based approaches. |
| 8 | Towards Reasoning in Large Language Models: A Survey | Huang & Chang | 2022 | arXiv:2212.10403 | 70 | 80 | **75** | Comprehensive review of reasoning capabilities and limitations; failure mode taxonomy. |
| 9 | A Survey for In-context Learning | Dong et al. | 2022 | arXiv:2301.00234 | 75 | 85 | **80** | Dedicated ICL survey; covers training, inference, demonstration selection, and evaluation. |
| 10 | Augmented Language Models: a Survey | Mialon et al. | 2023 | arXiv:2302.07842 | 70 | 78 | **74** | Survey of tools, memory, action, and reasoning augmentation for LLMs. |
| 11 | Harnessing the Power of LLMs in Practice: A Survey on ChatGPT and Beyond | Yang et al. | 2023 | arXiv:2304.13712 | 65 | 80 | **73** | Practitioner-focused survey; domain breakdowns across NLP tasks. |
| 12 | Nature Language Reasoning, A Survey | Yu et al. | 2023 | arXiv:2303.14725 | 68 | 72 | **70** | Covers deductive, inductive, abductive, and analogical reasoning in NLP. |
| 13 | An RL Perspective on RLHF, Prompting, and Beyond | Uehara et al. | 2023 | arXiv:2310.06147 | 72 | 68 | **70** | Unifies RLHF and prompting under RL framework; useful for optimization-aware prompt design. |
| 14 | A Practical Survey on Zero-shot Prompt Design for In-context Learning | Chang & Xu | 2023 | arXiv:2309.13205 | 65 | 62 | **64** | Taxonomy of zero-shot prompt design patterns; practical construction guidelines. |
| 15 | Prompt Design and Engineering: Introduction and Advanced Methods | Ekin | 2024 | arXiv:2401.14423 | 60 | 65 | **63** | Practitioner-focused; covers meta-prompting, zero/few-shot, CoT, RLHF interaction. |
| 16 | A Survey of Large Language Models | Zhao et al. | 2023 | arXiv:2303.18223 | 75 | 95 | **85** | Comprehensive LLM survey; prompting chapter covers practical techniques at scale. |
| 17 | Few-shot Fine-tuning vs. In-context Learning: A Fair Comparison | Mosbach et al. | 2023 | arXiv:2305.16938 | 70 | 68 | **69** | Head-to-head comparison clarifying when ICL beats fine-tuning; informs prompt-vs-train decisions. |
| 18 | Is Prompt All You Need? No. A Comprehensive and Broader View of Instruction Learning | Min et al. | 2023 | arXiv:2303.10475 | 72 | 65 | **69** | Challenges prompt-centric thinking; argues instruction learning scope must be broader. |
| 19 | A Bibliometric Review of Large Language Models Research from 2017 to 2023 | Various | 2023 | arXiv:2304.02020 | 50 | 55 | **53** | Trend analysis across LLM subfields; provides bibliometric context for prompt research. |
| 20 | Survey of Hallucination in Natural Language Generation | Ji et al. | 2022 | arXiv:2202.03629 | 78 | 88 | **83** | Groundwork survey on hallucination; informs grounding and verification prompt techniques. |
| 21 | Emergent Abilities of Large Language Models | Wei et al. | 2022 | arXiv:2206.07682 | 88 | 95 | **92** | Quantifies scale-driven emergent capabilities; explains why prompting unlocks reasoning at scale. |
| 22 | Sparks of Artificial General Intelligence: GPT-4 Experiments | Bubeck et al. | 2023 | arXiv:2303.12712 | 85 | 92 | **89** | Comprehensive GPT-4 capability analysis; prompt-based evaluation across mathematical and coding tasks. |
| 23 | A Survey on Multimodal Large Language Models | Yin et al. | 2023 | arXiv:2306.13549 | 80 | 85 | **83** | Comprehensive MLLM survey; covers visual instruction tuning and multimodal prompt strategies. |
| 24 | A Survey on Hallucination in Large Language Models | Zhang et al. | 2023 | arXiv:2311.05232 | 82 | 80 | **81** | Updated hallucination taxonomy; mitigation via retrieval and verification prompting strategies. |
| 25 | Instruction Tuning for Large Language Models: A Survey | Zhang et al. | 2023 | arXiv:2308.10792 | 78 | 82 | **80** | Survey of instruction tuning methods; connects fine-tuning to effective prompt design. |
| 26 | Large Language Models for Information Retrieval: A Survey | Zhu et al. | 2023 | arXiv:2308.07107 | 75 | 78 | **77** | LLMs for IR; document ranking, query expansion, and retrieval-augmented prompt patterns. |
| 27 | A Survey on Evaluation of Large Language Models | Chang et al. | 2023 | arXiv:2307.03109 | 76 | 80 | **78** | Standardized LLM evaluation methods; benchmark-aware prompt design principles. |
| 28 | A Comprehensive Survey on Pretrained Foundation Models | Zhou et al. | 2023 | arXiv:2302.09419 | 72 | 75 | **74** | Foundation model overview; contextualizes prompting within pre-training paradigms. |
| 29 | Unifying Large Language Models and Knowledge Graphs: A Roadmap | Pan et al. | 2023 | arXiv:2306.08302 | 78 | 75 | **77** | KG-LLM integration survey; knowledge-grounded prompting taxonomy and future directions. |
| 30 | Large Language Models for Software Engineering: A Survey | Fan et al. | 2023 | arXiv:2308.10620 | 74 | 78 | **76** | LLMs for SE; covers code prompting techniques across software lifecycle phases. |
| 31 | A Survey on Long Text Modeling with Transformers | Dong et al. | 2023 | arXiv:2302.14502 | 72 | 70 | **71** | Long-context modeling survey; sparse attention and efficient prompting for long documents. |
| 32 | Tool Learning with Foundation Models | Qin et al. | 2023 | arXiv:2304.08354 | 80 | 78 | **79** | Tool learning survey; systematic taxonomy of tool-augmented prompting approaches. |
| 33 | A Survey on Language Models for Code | Xu et al. | 2022 | arXiv:2311.07989 | 75 | 76 | **76** | Code LLM survey; prompting strategies for code completion, generation, and repair. |
| 34 | Large Language Model-based Multi-Agents: A Survey | Guo et al. | 2024 | arXiv:2402.01680 | 82 | 78 | **80** | Multi-agent LLM systems survey; inter-agent prompting and coordination patterns. |
| 35 | Retrieval-Augmented Generation for Large Language Models: A Survey | Gao et al. | 2024 | arXiv:2312.10997 | 80 | 82 | **81** | Comprehensive RAG survey; retrieval integration patterns and hybrid prompt architectures. |
| 36 | A Survey of Large Language Models | Zhao et al. | 2023 | arXiv:2303.18223 | 78 | 88 | **83** | Comprehensive LLM architecture survey; prompting chapter covers practical techniques at scale. |
| 37 | ChatGPT: A Meta-Analysis after 2.5 Months | Krugel et al. | 2023 | arXiv:2302.13795 | 60 | 65 | **63** | Early ChatGPT impact analysis; prompt patterns observed in real-world usage. |
| 38 | The Rise and Potential of LLM-based Agents | Xi et al. | 2023 | arXiv:2309.07864 | 82 | 80 | **81** | Agent paradigm survey; LLM-based autonomous agents and planning-prompting synergy. |
| 39 | A Survey of Prompt Engineering Methods in LLMs | Vatsal & Singh | 2024 | arXiv:2407.12994 | 70 | 65 | **68** | Recent prompt method taxonomy; covers 2024 technique developments and benchmarks. |
| 40 | Efficient Large Language Models: A Survey | Wan et al. | 2023 | arXiv:2312.03863 | 78 | 75 | **77** | Efficiency techniques survey; prompt compression and efficient inference patterns. |
| 41 | Beyond Efficiency: A Systematic Survey of Resource-Efficient LLMs | Zhou et al. | 2024 | arXiv:2401.00625 | 72 | 68 | **70** | Resource-efficient LLM survey; covers prompt-centric efficiency optimizations. |
| 42 | LLMs for User Simulation: A Comprehensive Survey | Feng et al. | 2024 | arXiv:2403.00038 | 70 | 62 | **66** | User simulation via LLMs; persona and scenario prompting for synthetic users. |
| 43 | A Survey on Context Engineering: How to Maximize LLM Potential | Liu et al. | 2025 | arXiv:2503.06811 | 75 | 70 | **73** | Context engineering taxonomy; extends prompting to full context lifecycle management. |
| 44 | A Survey on Large Language Model Alignment | Wang et al. | 2023 | arXiv:2309.15025 | 78 | 76 | **77** | Alignment survey; RLHF, constitutional methods, and alignment-aware prompting. |
| 45 | Large Audio Language Models: A Survey | Cui et al. | 2024 | arXiv:2403.13025 | 72 | 65 | **69** | Audio-LLM survey; audio prompting and speech instruction patterns. |
| 46 | A Survey on Video Generation: From Early Models to Advanced Systems | Chen et al. | 2024 | arXiv:2403.12785 | 70 | 68 | **69** | Video generation survey; text-to-video prompting techniques and temporal control. |
| 47 | Trustworthy Large Language Models: A Survey | Liu et al. | 2024 | arXiv:2401.05561 | 75 | 72 | **74** | Trustworthy LLM survey; safety prompting, bias mitigation, and robustness patterns. |
| 48 | LLMs for Scientific Discovery: A Survey | Wang et al. | 2024 | arXiv:2402.01546 | 74 | 70 | **72** | Scientific LLM survey; domain-specific prompting for chemistry, biology, physics. |
| 49 | Position: A Survey of Safety Concerns in LLMs | Hua et al. | 2024 | arXiv:2402.03788 | 72 | 70 | **71** | Safety concern taxonomy; defensive prompting and content moderation techniques. |
| 50 | A Survey on LLM-based Autonomous Agents | Wang et al. | 2023 | arXiv:2308.11432 | 80 | 78 | **79** | Autonomous agent survey; planning, memory, and tool prompting for agent systems. |

---

## 추가 예정 논문 (다음 업데이트 우선순위 대기열)

100편 달성을 위한 검색 대상:

- "Emergent Abilities of Large Language Models" (Wei et al., 2022, arXiv:2206.07682)
- "Large Language Models are Few-Shot Learners" GPT-3 (Brown et al., 2020)
- "A Survey on Hallucination in LLMs" (Zhang et al., 2023, arXiv:2311.05232)
- "Instruction Tuning for Large Language Models: A Survey" (2023)
- "ChatGPT is not all you need" survey
- "Sparks of AGI" (Microsoft, 2023)
- "A Survey on Multimodal Large Language Models" (Yin et al., 2023)
- Annual NeurIPS/ICLR/ACL 2025 survey papers on prompting
- Context Engineering survey papers (2025-2026)
- Agent system survey papers (2025-2026)
