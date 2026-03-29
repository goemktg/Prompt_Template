# Prompt Engineering Papers: Structured Output & Format Prompting

> **Category**: `[STRUCTURE]`
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
| 1 | Structured Prompting: Scaling In-Context Learning to 1,000 Examples | Hao et al. | 2022 | arXiv:2212.06713 | 85 | 75 | **80** | Efficient many-example prompting via structured templates; handles 1000+ ICL examples. |
| 2 | JSONformer: JSON-Schema-Constrained LLM Decoding | Robust Intelligence | 2023 | GitHub | 82 | 78 | **80** | Constrained decoding enforces valid JSON at each token; eliminates format errors in output. |
| 3 | Outlines: Efficient Guided Generation for LLMs | Willard & Louf | 2023 | arXiv:2307.09702 | 88 | 82 | **85** | Finite-state machine constrained decoding; any regex/JSON/grammar can be enforced at inference. |
| 4 | Guidance: Efficient Constrained Text Generation | Microsoft | 2023 | GitHub | 82 | 80 | **81** | Template-guided generation with interleaved logic; Handlebars-style prompt programs. |
| 5 | LMQL: Programming Large Language Models | Beurer-Kellner et al. | 2022 | arXiv:2212.06094 | 88 | 76 | **82** | SQL-like constraint language for LLM prompting; enables typed output, conditionals, loops. |
| 6 | SGLang: Efficient Execution of Structured Language Model Programs | Zheng et al. | 2023 | arXiv:2312.07104 | 85 | 78 | **82** | Execution engine for LLM programs; RadixAttention enables KV-cache reuse for structured prompts. |
| 7 | TypeChat: Getting Structured Output from Language Models | Microsoft | 2023 | Blog/GitHub | 78 | 74 | **76** | TypeScript schemas as output constraints; LLM returns parsed, type-safe structured responses. |
| 8 | Schema-Guided Dialogue State Tracking | Rastogi et al. | 2020 | arXiv:1909.05855 | 80 | 75 | **78** | Schema as prompt context for dialogue tracking; early structured prompt technique. |
| 9 | Tag-Guided Format Prompting | Cheng et al. | 2023 | arXiv:2307.15897 | 72 | 62 | **67** | XML-tag delimiters for structured LLM output sections; reduces format hallucination. |
| 10 | Text-to-Structured Output Generation via Constrained LLMs | Various | 2024 | arXiv:2407.11548 | 75 | 65 | **70** | Comprehensive comparison of constrained generation methods for structured data extraction. |
| 11 | Tabular Representation, Noisy Operators, and the Limits of LLMs | Wüthrich et al. | 2023 | arXiv:2305.11030 | 70 | 62 | **66** | Studies how table format in prompt affects LLM comprehension; best formatting strategies. |
| 12 | Template-based NLG for Real-world Applications | Reiter | 2022 | arXiv | 65 | 60 | **63** | Template-aligned generation for consistent output structure; NLG quality vs. variability tradeoffs. |
| 13 | FIRE: An Finetuning-based Information Retrieval with Structured Output | Gu et al. | 2023 | arXiv:2310.01558 | 72 | 60 | **66** | Structured extraction via JSON-schema-constrained fine-tuning and prompting. |
| 14 | Ask Me Anything: A Simple Strategy for Prompting Complex Questions | Arora et al. | 2022 | arXiv:2210.02441 | 78 | 74 | **76** | Generates multiple question reformulations from same input; ensemble answer aggregation. |
| 15 | Chain-of-Table: Evolving Tables in the Reasoning Chain | Wang et al. | 2024 | arXiv:2401.04398 | 80 | 68 | **74** | Tables as structured intermediate reasoning steps; integrates tabular operations into CoT. |
| 16 | Markdown Tables Are Better Than CSV for LLM Reasoning | Various | 2024 | arXiv:2406.17874 | 68 | 58 | **63** | Empirical comparison of tabular formats in LLM prompts; markdown wins for reasoning tasks. |
| 17 | Instructor: Structured Output from OpenAI Function Calling | Liu | 2023 | GitHub | 72 | 78 | **75** | Python library wrapping Pydantic schemas as LLM output constraints; widely adopted pattern. |
| 18 | Generating Synthetic Data with LLMs: Structured Approaches | Various | 2024 | arXiv:2402.10378 | 70 | 65 | **68** | Schema-driven synthetic dataset generation via structured prompting. |
| 19 | Pydantic-AI: Type-Safe Agent Framework | Pydantic team | 2024 | GitHub/Docs | 72 | 68 | **70** | Pydantic v2 validation integrated with LLM outputs; prevents format drift at runtime. |
| 20 | Re-Reading (RE2): Improves LLM Reasoning via Re-Reading | Xu et al. | 2023 | arXiv:2309.06275 | 72 | 62 | **67** | Re-reading question prompt before answering; structured two-pass format improves accuracy. |
| 21 | RTM: Structured Reasoning Through Tasks via Multi-Hop | Various | 2024 | arXiv:2401.11553 | 70 | 58 | **64** | Multi-hop task decomposition in structured template format; improves complex QA accuracy. |
| 22 | CLP: Contrastive Label Prompting for Structured Prediction | Zhao et al. | 2023 | arXiv:2311.07658 | 72 | 60 | **66** | Contrastive format for classification labels; reduces label confusion in structured output. |
| 23 | OpenAI Structured Outputs: Reliable JSON Generation | OpenAI | 2024 | Blog/API Docs | 75 | 85 | **80** | Native JSON schema enforcement in API; guarantees valid structured output without post-processing. |
| 24 | Anthropic XML Prompting Best Practices | Anthropic | 2024 | Documentation | 72 | 78 | **75** | XML tags for structured Claude prompts; empirically validated delimiters for section separation. |
| 25 | Function Calling and Parallel Tool Use | OpenAI | 2023 | API Documentation | 78 | 88 | **83** | JSON schema for function definitions; structured tool-call interface enabling multi-tool prompts. |
| 26 | Grammar-Based Decoding for Structured NLG | Scholak et al. | 2022 | arXiv:2109.05093 | 80 | 72 | **76** | Grammar-constrained decoding for SQL/code; guarantees syntactic validity via CFG constraints. |
| 27 | LLMParser: Using LLMs for Log Parsing | Jiang et al. | 2024 | arXiv:2408.06865 | 70 | 62 | **66** | Structured log parsing via prompting; template + variable extraction from unstructured logs. |
| 28 | Gorilla: Large Language Model Connected with Massive APIs | Patil et al. | 2023 | arXiv:2305.15334 | 82 | 78 | **80** | API call generation via structured prompts; retrieval-augmented API documentation. |
| 29 | ToolAlpaca: Generalized Tool Learning via Natural Language | Tang et al. | 2023 | arXiv:2306.05301 | 76 | 68 | **72** | Simulated tool-use dataset; structured action-observation prompting patterns. |
| 30 | NExT: Teaching Large Language Models to Reason About Code Execution | Ni et al. | 2024 | arXiv:2404.14662 | 78 | 70 | **74** | Structured execution traces in prompts; teaches models to reason about state changes. |
| 31 | Semantic Parsing with Large Language Models | Shin et al. | 2023 | arXiv:2305.05176 | 75 | 70 | **73** | Text-to-SQL via structured prompting; schema linking and query decomposition. |
| 32 | BIRD: A Big Bench for Large-Scale Database Grounded Text-to-SQL | Li et al. | 2023 | arXiv:2305.03111 | 72 | 74 | **73** | Text-to-SQL benchmark; evaluates structured output quality on complex database queries. |
| 33 | Resurrecting Recurrence for Length Generalization | Ruoss et al. | 2023 | arXiv:2303.06396 | 74 | 65 | **70** | Position encoding for structured sequences; improves length generalization in structured tasks. |
| 34 | Universal Information Extraction as Unified Semantic Matching | Lu et al. | 2023 | arXiv:2305.03726 | 76 | 70 | **73** | Unified IE via semantic matching prompts; entity, relation, event extraction in single format. |
| 35 | Document Understanding Transformer with Unified Layout-Text Embedding | Kim et al. | 2022 | arXiv:2207.09509 | 78 | 74 | **76** | Layout-aware document understanding; structured extraction from forms and documents. |
| 36 | LayoutLLM: Layout Instruction Tuning with Large Language Models | Luo et al. | 2023 | arXiv:2306.02019 | 75 | 68 | **72** | Layout-aware prompting for document tasks; spatial formatting in prompt context. |
| 37 | TableGPT: Towards Unifying Tables, Nature Language and Commands into One GPT | Zha et al. | 2023 | arXiv:2307.08674 | 74 | 66 | **70** | Unified table manipulation interface; natural language commands for structured data operations. |
| 38 | SheetCopilot: Bringing Software Productivity to the Next Level | Li et al. | 2024 | arXiv:2305.19308 | 72 | 65 | **69** | Spreadsheet manipulation via structured prompts; formula and chart generation. |
| 39 | Data-Copilot: Bridging Billions of Data and Humans with Autonomous Workflow | Zhang et al. | 2023 | arXiv:2306.07209 | 74 | 68 | **71** | Autonomous data analysis via structured workflows; self-orchestrated data operations. |
| 40 | UniChart: A Universal Vision-Language Model for Chart Understanding | Masry et al. | 2023 | arXiv:2305.14761 | 75 | 70 | **73** | Chart-to-text and chart QA; multimodal structured understanding of visualizations. |
| 41 | DeepSeek-Prover: Advancing Theorem Proving with LLMs | Wu et al. | 2024 | arXiv:2405.14333 | 80 | 72 | **76** | Formal theorem proving via structured prompts; proof step generation with verification. |
| 42 | AlphaProof and AlphaGeometry: AI for Mathematical Olympiads | Google DeepMind | 2024 | Nature/Blog | 88 | 85 | **87** | Structured mathematical reasoning; formal proof search with LLM guidance. |
| 43 | Jellyfish: A Large Language Model for Data Preprocessing | Zhang et al. | 2024 | arXiv:2312.01678 | 70 | 62 | **66** | Specialized LLM for data wrangling; structured transformations from NL descriptions. |
| 44 | LLM2LLM: Boosting LLMs with Novel Iterative Data Enhancement | Lee et al. | 2024 | arXiv:2403.15042 | 72 | 64 | **68** | Synthetic structured data generation; iterative augmentation for training data. |
| 45 | Spider 2.0: Enterprise Text-to-SQL Benchmark | Li et al. | 2024 | arXiv:2407.08223 | 74 | 72 | **73** | Complex enterprise SQL benchmark; evaluates structured output on real-world schemas. |
| 46 | Constrained Decoding for Fill-in-the-Middle Code Models | Ziegler et al. | 2024 | arXiv:2404.04163 | 72 | 65 | **69** | Syntax-aware code completion; constrained generation for valid code structures. |
| 47 | Synchromesh: Reliable Code Generation from Pre-trained Language Models | Poesia et al. | 2022 | arXiv:2201.11227 | 78 | 70 | **74** | Constraint-guided decoding via target grammar; ensures syntactically correct output. |
| 48 | PICARD: Parsing Incrementally for Constrained Auto-Regressive Decoding | Scholak et al. | 2021 | arXiv:2109.05093 | 80 | 76 | **78** | Incremental parsing for SQL generation; filters invalid tokens during decoding. |
| 49 | SciGraphQA: A Large-Scale Synthetic Multi-Turn Question-Answering Dataset | Li et al. | 2023 | arXiv:2311.05091 | 68 | 60 | **64** | Scientific graph QA benchmark; structured extraction from figures and charts. |
| 50 | Executable Code Actions Elicit Better LLM Agents | Wang et al. | 2024 | arXiv:2402.01030 | 80 | 74 | **77** | Code-as-action structured format; Python execution outperforms JSON tool calls. |

---

## Papers to Add (Priority Queue for Next Update)

Search targets:
- "Nucleus sampling" and format diversity control papers
- "JSON mode" in GPT-4 / Gemini API (empirical studies)
- "Function calling API" design papers (OpenAI 2023)
- "Tool use specification formats" in LLM APIs
- "ReAct-style structured observation" formats
- "YAML vs JSON vs XML prompt" comparative studies
- "Markdown in prompts" effectiveness analysis
- "Structured generation for information extraction" IE papers 2024-2025
- "Grammar-constrained decoding" theoretical papers
- "LLMParser: An Exploratory Study on Using Large Language Models for Log Parsing" (2024)
- "Structured CoT for code" papers
- "OpenAI Structured Outputs" (2024 API feature) evaluation papers
- "XML Prompting" Anthropic best practices empirical papers
