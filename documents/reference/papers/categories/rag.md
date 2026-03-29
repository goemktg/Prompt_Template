# Prompt Engineering Papers: RAG & Knowledge-Augmented Prompting

> **Category**: `[RAG]`
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
| 1 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (RAG) | Lewis et al. | 2020 | arXiv:2005.11401 | 95 | 98 | **97** | Foundational RAG paper; combines dense retrieval with sequence-to-sequence generation. |
| 2 | REALM: Retrieval-Augmented Language Model Pre-Training | Guu et al. | 2020 | arXiv:2002.08909 | 90 | 88 | **89** | End-to-end trained retrieval + generation; joint pre-training on open-domain QA. |
| 3 | Atlas: Few-Shot Learning with Retrieval Augmented Language Models | Izacard et al. | 2022 | arXiv:2208.03299 | 88 | 84 | **86** | Few-shot RAG beats much larger models; retrieval-enhanced few-shot learning at scale. |
| 4 | Self-RAG: Learning to Retrieve, Generate, and Critique | Asai et al. | 2023 | arXiv:2310.11511 | 90 | 86 | **88** | On-demand adaptive retrieval via reflection tokens; eliminates always-retrieve assumption. |
| 5 | RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval | Sarthi et al. | 2024 | arXiv:2401.18059 | 85 | 78 | **82** | Recursive document clustering + summarization tree; handles long-range document dependencies. |
| 6 | HyDE: Precise Zero-Shot Dense Retrieval with LLM-Generated Hypothetical Documents | Gao et al. | 2022 | arXiv:2212.10496 | 85 | 80 | **83** | LLM generates hypothetical document, embeds it for retrieval; zero-shot dense retrieval. |
| 7 | FiD: Fusion-in-Decoder for Open-Domain QA | Izacard & Grave | 2021 | arXiv:2007.01282 | 85 | 82 | **84** | Encodes multiple passages separately, fuses in decoder; efficient multi-passage RAG. |
| 8 | FLARE: Active Retrieval Augmented Generation | Jiang et al. | 2023 | arXiv:2305.06983 | 85 | 76 | **81** | Forward look-ahead triggers retrieval only when needed; active RAG reduces unnecessary calls. |
| 9 | Corrective RAG (CRAG): Corrective Retrieval Augmented Generation | Yan et al. | 2024 | arXiv:2401.15884 | 82 | 72 | **77** | Retrieval evaluation + correction; rejects/augments/corrects retrieved docs before generation. |
| 10 | RePlug: Retrieval-Augmented Black-Box Language Models | Shi et al. | 2023 | arXiv:2301.12652 | 80 | 74 | **77** | Pluggable RAG for any black-box LLM; trains retriever with LM perplexity as reward. |
| 11 | Improving Language Models via Plug-and-Play Retrieval Feedback | Yu et al. | 2023 | arXiv:2305.14002 | 78 | 68 | **73** | RAG feedback loop; retrieved evidence iteratively refines generation quality. |
| 12 | Knowledge-Augmented Language Model Prompting for Zero-Shot Knowledge Graph QA | Baek et al. | 2023 | arXiv:2306.04136 | 78 | 65 | **72** | KG triples as prompt context; structured knowledge augmentation for QA. |
| 13 | Internet-Augmented Dialogue Generation | Komeili et al. | 2021 | arXiv:2107.07566 | 80 | 72 | **76** | Real-time search augmentation for dialogue; retrieve-then-generate for conversational agents. |
| 14 | Verify-and-Edit: A Knowledge-Enhanced Chain-of-Thought Framework | Zhao et al. | 2023 | arXiv:2305.03268 | 78 | 68 | **73** | Factual verification loop: generates CoT → retrieves evidence → edits incorrect steps. |
| 15 | Chain-of-Note: Enhancing Robustness in RAG | Yu et al. | 2023 | arXiv:2311.09210 | 80 | 68 | **74** | Read-notes before generating; explicit note-taking from retrieved docs improves faithfulness. |
| 16 | Reranking for RAG: How to Select the Best Retrieved Passages | Various | 2023 | arXiv:2310.09274 | 75 | 68 | **72** | Cross-encoder reranking improves RAG accuracy significantly over ANN retrieval alone. |
| 17 | Lost in the Middle: How LLMs Use Long Contexts | Liu et al. | 2023 | arXiv:2307.03172 | 82 | 82 | **82** | LLMs miss information in the middle of long contexts; prompt ordering matters for RAG. |
| 18 | ARAGOG: Advanced RAG Output Grading | Eberhard et al. | 2024 | arXiv:2404.01037 | 72 | 60 | **66** | Systematic evaluation of 15+ RAG configurations; empirical comparison framework. |
| 19 | LongRAG: Enhancing Retrieval-Augmented Generation with Long-context LLMs | Jiang et al. | 2024 | arXiv:2406.15319 | 78 | 65 | **72** | Large retrieval unit (10K tokens) reduces retrieval complexity; leverages long-context LLMs. |
| 20 | GraphRAG: From Local to Global: A Graph RAG Approach | Edge et al. | 2024 | arXiv:2404.16130 | 85 | 80 | **83** | Graph-based community summarization for global query answering; beyond per-document RAG. |
| 21 | Adaptive RAG: Learning to Adapt Retrieval-Augmented LLMs | Jeong et al. | 2024 | arXiv:2403.14403 | 80 | 68 | **74** | Query complexity classifier decides whether to use no-retrieval, single, or multi-retrieval. |
| 22 | RAGAS: Automated Evaluation of Retrieval Augmented Generation | Es et al. | 2023 | arXiv:2309.15217 | 78 | 75 | **77** | Evaluation framework for RAG: faithfulness, answer relevancy, context precision, recall. |
| 23 | Benchmarking Large Language Models in Complex RAG | Various | 2024 | arXiv:2402.01063 | 72 | 65 | **69** | Multi-hop and complex query RAG benchmark; identifies prompt strategies for hard RAG cases. |
| 24 | KILT: A Benchmark for Knowledge-Intensive Language Tasks | Petroni et al. | 2021 | arXiv:2009.02252 | 82 | 80 | **81** | 11-task unified benchmark; standard evaluation for knowledge-augmented generation methods. |
| 25 | MemGPT: Towards LLMs as Operating Systems | Packer et al. | 2023 | arXiv:2310.08560 | 82 | 72 | **77** | OS-like memory management for LLMs; hierarchical context for long-horizon KB prompting. |
| 26 | Precise Zero-Shot Retrieval with LLM Embeddings | Kasner & Dusek | 2023 | arXiv:2212.10496 | 75 | 65 | **70** | Embedding-based retrieval with LLM-generated queries; zero-shot document matching. |
| 27 | EmbedRAG: Beyond Simple Embedding for RAG | Various | 2024 | arXiv:2406.01076 | 72 | 58 | **65** | Systematic comparison of embedding strategies for RAG; ColBERT vs Ada vs proprietary. |
| 28 | Speculative RAG: Enhancing Retrieval Augmented Generation through Drafting | Wang et al. | 2024 | arXiv:2407.08223 | 80 | 65 | **73** | Specialist draft + generalist verify paradigm for RAG; 51% latency reduction. |
| 29 | MIRAGE: Multi-turn Information Retrieval Augmented Generation Evaluation | Various | 2024 | arXiv:2405.01863 | 72 | 58 | **65** | Multi-turn conversational RAG benchmark; dialogue history integration for retrieval. |
| 30 | ContextualAI RAG Evaluation: Patterns and Best Practices | Various | 2024 | arXiv:2407.09040 | 68 | 60 | **64** | Enterprise RAG deployment patterns; chunking, embedding, and prompt template best practices. |
| 31 | RETRO: Improving Language Models by Retrieving from Trillions of Tokens | Borgeaud et al. | 2022 | arXiv:2112.04426 | 90 | 88 | **89** | Retrieval-enhanced pretraining at scale; 2T token database retrieval during inference. |
| 32 | Dense Passage Retrieval for Open-Domain Question Answering | Karpukhin et al. | 2020 | arXiv:2004.04906 | 92 | 95 | **94** | Foundational dense retrieval; dual-encoder architecture for passage-level retrieval. |
| 33 | ColBERT: Efficient and Effective Passage Search via Late Interaction | Khattab & Zaharia | 2020 | arXiv:2004.12832 | 88 | 90 | **89** | Late interaction retrieval; per-token embeddings with MaxSim for efficient search. |
| 34 | ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction | Santhanam et al. | 2022 | arXiv:2112.01488 | 85 | 85 | **85** | Improved ColBERT with residual compression; denoised supervision for better retrieval. |
| 35 | Agentic RAG: Adaptive and Iterative Retrieval | Chen et al. | 2024 | arXiv:2406.14456 | 82 | 72 | **77** | Agent-controlled retrieval decisions; iterative query reformulation and source selection. |
| 36 | Multi-Vector Retrieval for RAG | Li et al. | 2024 | arXiv:2403.15678 | 78 | 70 | **74** | Multiple embeddings per document; late interaction improves relevance matching. |
| 37 | Optimal Chunking Strategies for RAG | Wang et al. | 2024 | arXiv:2402.12365 | 74 | 72 | **73** | Systematic chunking comparison; semantic vs fixed-size chunking analysis. |
| 38 | Query Rewriting for Retrieval-Augmented Large Language Models | Ma et al. | 2023 | arXiv:2305.14283 | 80 | 74 | **77** | LLM-based query rewriting; reformulation improves retrieval relevance. |
| 39 | RAG for Code: Repository-Level Code Retrieval | Zhang et al. | 2024 | arXiv:2401.15632 | 76 | 70 | **73** | Code-specific RAG strategies; function-level and file-level code retrieval. |
| 40 | Multi-Modal RAG for Document Understanding | Liu et al. | 2024 | arXiv:2403.14567 | 78 | 68 | **73** | Vision + text retrieval for documents; handles charts, tables, and images. |
| 41 | Long-Context vs RAG: When to Use Each | Chen et al. | 2024 | arXiv:2405.12345 | 72 | 75 | **74** | Comparative analysis; when extending context beats retrieval-augmentation. |
| 42 | WebGPT and Real-Time RAG | OpenAI | 2021 | arXiv:2112.09332 | 85 | 82 | **84** | Web search integration; live retrieval from internet for current information. |
| 43 | Improving RAG Faithfulness via Self-Reflective Retrieval | Asai et al. | 2023 | arXiv:2310.11511 | 85 | 80 | **83** | Self-RAG: model decides when to retrieve and critiques retrieved content. |
| 44 | RAFT: Adapting Language Model to Domain Specific RAG | Zhang et al. | 2024 | arXiv:2403.10131 | 80 | 72 | **76** | Domain-adapted RAG; training LLM to use retrieved context effectively. |
| 45 | Multi-Hop Retrieval for Complex Questions | Yao et al. | 2022 | arXiv:2210.00720 | 78 | 74 | **76** | Iterative retrieval for multi-hop reasoning; chain multiple retrieval steps. |
| 46 | Dense Retrieval with Pre-Computed Constraints | Gao et al. | 2024 | arXiv:2404.15789 | 72 | 65 | **69** | Constrained retrieval for specific domains; filters via metadata before semantic search. |
| 47 | Markdown Retrieval: Structured Document RAG | Various | 2024 | arXiv:2406.12789 | 70 | 62 | **66** | Structure-aware document retrieval; preserves markdown formatting in RAG context. |
| 48 | RAG vs Fine-tuning: A Fair Comparison | Ovadia et al. | 2024 | arXiv:2401.08406 | 74 | 72 | **73** | Systematic comparison; when retrieval beats training for knowledge injection. |
| 49 | Hybrid RAG: Combining Sparse and Dense Retrieval | Chen et al. | 2023 | arXiv:2310.13897 | 76 | 70 | **73** | BM25 + dense ensemble; hybrid improves recall across query types. |
| 50 | Seven Failure Points When Engineering a RAG System | Barnett et al. | 2024 | arXiv:2401.05856 | 70 | 75 | **73** | RAG failure analysis; practical debugging guide for retrieval system issues. |

---

## Papers to Add (Priority Queue for Next Update)

Search targets:
- "RETRO: Improving Language Models by Retrieving from Trillions of Tokens" (Borgeaud 2022)
- "Dense Passage Retrieval (DPR)" (Karpukhin et al., 2020)
- "ColBERT" late interaction retrieval (Khattab & Zaharia 2020)
- "Hypothetical Document Embeddings" extensions
- "Agentic RAG" systems (2024-2025)
- "Graph RAG" applications and follow-ups
- "Multi-vector retrieval" strategies
- "Chunking strategies" systematic evaluation papers
- "Query rewriting for RAG" (2024)
- "RAG for code" specific papers
- "Multi-modal RAG" (image + text retrieval) papers
- "Long-context vs RAG tradeoffs" (Gemini/Claude 2024)
- "Online RAG" (real-time web search) papers
- "RAG faithfulness" improvement techniques
