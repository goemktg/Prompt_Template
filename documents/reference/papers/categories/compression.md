# Prompt Engineering Papers: Prompt Compression & Efficiency

> **Category**: `[COMPRESSION]`
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
| 1 | LLMLingua: Compressing Prompts for Accelerated Inference | Jiang et al. | 2023 | arXiv:2310.05736 | 88 | 82 | **85** | Small LM compresses prompts by dropping low-perplexity tokens; 3-20× compression ratio. |
| 2 | LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression | Wu et al. | 2024 | arXiv:2403.12968 | 85 | 78 | **82** | Bidirectional training for compression; task-agnostic + 3-6× faster than LLMLingua v1. |
| 3 | Selective Context: Efficient Long-Context LLM Utilization | Li et al. | 2023 | arXiv:2304.01597 | 82 | 72 | **77** | Selects informative sentences from context via self-information; reduces tokens without perplexity hit. |
| 4 | SnapKV: LLM Knows What You are Looking for Before Generation | Li et al. | 2024 | arXiv:2404.14469 | 85 | 76 | **81** | Key-value cache compression by clustering attending positions; 3.6× memory reduction, no quality loss. |
| 5 | StreamingLLM: Efficient Streaming Language Models with Attention Sinks | Xiao et al. | 2023 | arXiv:2309.17453 | 85 | 80 | **83** | Attention sinks enable infinite-length generation via KV eviction; streaming without re-computation. |
| 6 | Efficient Prompting via Dynamic In-Context Learning | Li et al. | 2023 | arXiv:2305.11170 | 78 | 68 | **73** | Dynamically selects minimum examples for ICL; achieves target accuracy with fewer tokens. |
| 7 | Compressing Context to Enhance Inference Efficiency of LLMs | Mu et al. | 2023 | arXiv:2307.01061 | 80 | 68 | **74** | "Gisting": trains model to compress prompts into virtual tokens; 26× compression possible. |
| 8 | Token Elimination for Efficient LLM Inference | Kim et al. | 2024 | arXiv:2402.01035 | 78 | 65 | **72** | Importance-based token elimination during generation; 30% FLOPs reduction at minimal quality cost. |
| 9 | Prompt Compression and Contrastive Conditioning (PC2) | Wingate et al. | 2022 | arXiv:2211.01562 | 75 | 65 | **70** | Soft prompt encoding of few-shot examples; fixed-length prefix replaces lengthy demonstrations. |
| 10 | FaithComp: Faithful Compression of Long Documents for QA | Zhang et al. | 2023 | arXiv:2311.01375 | 72 | 60 | **66** | Extractive document compression for QA prompts; faithfulness-preserving sentence selection. |
| 11 | ICAE: In-Context Autoencoder for Context Compression | Ge et al. | 2023 | arXiv:2307.06945 | 82 | 68 | **75** | Autoencoder compresses arbitrary contexts into fixed-length memory slots; retrieval-free long context. |
| 12 | AutoCompressors: Compressing Long Contexts via Soft Tokens | Chevalier et al. | 2023 | arXiv:2305.14788 | 80 | 70 | **75** | Recursive compression via trainable soft token summarization; enables very long contexts. |
| 13 | Long Context Prompting with Segment-Based Compression | Various | 2023 | arXiv:2309.10923 | 72 | 60 | **66** | Segments long documents + compresses each independently; modular context management approach. |
| 14 | FlexGen: High-Throughput Generative Inference of LLMs via Offloading | Sheng et al. | 2023 | arXiv:2303.06865 | 80 | 74 | **77** | Memory offloading + computation scheduling; enables large batch inference on limited hardware. |
| 15 | PowerInfer: Fast Large Language Model Serving with a Consumer GPU | Song et al. | 2023 | arXiv:2312.12456 | 78 | 70 | **74** | Hot neuron caching for consumer GPU; activates frequently-used neurons locally = faster inference. |
| 16 | Efficient Attention: Attention with Linear Complexities | Shen et al. | 2021 | arXiv:1812.01243 | 82 | 75 | **79** | Linear attention mechanisms for long-context efficiency; useful for understanding KV compression. |
| 17 | Chain-of-Draft for Efficient Reasoning | Xu et al. | 2025 | arXiv:2502.18600 | 82 | 70 | **76** | Minimal draft reasoning achieves CoT quality at 7.6× token savings. |
| 18 | LLMLingua-Long: Effective Prompt Optimization for Long Contexts | Jiang et al. | 2024 | arXiv:2407.03253 | 78 | 65 | **72** | Extends LLMLingua for 100K+ contexts; handles book-length inputs efficiently. |
| 19 | RECOMP: Improving Retrieval-Augmented LMs with Compression | Xu et al. | 2023 | arXiv:2310.04408 | 80 | 68 | **74** | Extractive + abstractive compressors for RAG context; trained compressor outperforms uncondensed. |
| 20 | Prompt Cache: Modular Attention Reuse for Low-Latency Inference | Gim et al. | 2024 | arXiv:2311.04934 | 80 | 70 | **75** | Prompt schema caching in KV-cache; modular reuse of shared system prompt computations. |
| 21 | PCW: Parallel Context Windows for Large Language Models | Ratner et al. | 2023 | arXiv:2212.10947 | 82 | 75 | **79** | Parallel encoding of context segments; extends effective context via windowed attention. |
| 22 | MInference: Million-Token Long-Context Inference via Dynamic Sparse Attention | Liu et al. | 2024 | arXiv:2407.02490 | 85 | 78 | **82** | Dynamic sparse attention for 1M+ tokens; 10x speedup on long-context prompts. |
| 23 | H2O: Heavy-Hitter Oracle for Efficient Generative Inference | Zhang et al. | 2023 | arXiv:2306.14048 | 82 | 76 | **79** | KV cache eviction based on attention scores; keeps heavy-hitter tokens for efficiency. |
| 24 | InfLLM: Training-Free Long-Context Extrapolation for LLMs | Xiao et al. | 2024 | arXiv:2402.04617 | 80 | 72 | **76** | Block-level memory management; context-memory units enable infinite context without training. |
| 25 | Quest: Query-Aware Sparsity for Efficient Long-Context LLM Inference | Tang et al. | 2024 | arXiv:2406.10774 | 78 | 68 | **73** | Query-specific KV cache selection; 7x speedup with minimal quality loss. |
| 26 | Scissorhands: Exploiting the Persistence of Importance Hypothesis | Liu et al. | 2023 | arXiv:2305.17118 | 78 | 70 | **74** | Attention pattern persistence for KV pruning; one-time importance scoring. |
| 27 | LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding | Bai et al. | 2023 | arXiv:2308.14508 | 75 | 78 | **77** | Standardized long-context benchmark; evaluates compression impact on diverse tasks. |
| 28 | Unlimiformer: Long-Range Transformers with Unlimited Length | Bertsch et al. | 2023 | arXiv:2305.01625 | 82 | 74 | **78** | kNN retrieval over encoded inputs; unlimited context via retrieval-based compression. |
| 29 | CoLT5: Faster Long-Range Transformers with Conditional Computation | Ainslie et al. | 2023 | arXiv:2303.09752 | 80 | 72 | **76** | Conditional computation for long context; light vs heavy branches based on token importance. |
| 30 | Token Merging: Your ViT but Faster | Bolya et al. | 2023 | arXiv:2210.09461 | 78 | 75 | **77** | Token merging via bipartite matching; applicable to prompt compression in vision-language models. |
| 31 | Dynamic Context Pruning for Efficient and Interpretable Autoregressive Transformers | Anagnostidis et al. | 2023 | arXiv:2305.15805 | 76 | 68 | **72** | Learn-to-prune context tokens dynamically; interpretable attention-based compression. |
| 32 | Landmark Attention: Random-Access Infinite Context Length for Transformers | Mohtashami & Jaggi | 2023 | arXiv:2305.16300 | 80 | 70 | **75** | Landmark tokens enable random access to long contexts; memory blocks with retrieval. |
| 33 | Efficient Memory Management for Large Language Model Serving | Kwon et al. | 2023 | arXiv:2309.06180 | 82 | 80 | **81** | PagedAttention for vLLM; memory-efficient KV cache management via paging. |
| 34 | LoRAShear: Efficient Large Language Model Structured Pruning and Knowledge Recovery | Chen et al. | 2024 | arXiv:2310.18356 | 75 | 65 | **70** | Structured pruning with LoRA recovery; reduces model size while preserving prompt performance. |
| 35 | SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot | Frantar & Alistarh | 2023 | arXiv:2301.00774 | 82 | 78 | **80** | One-shot unstructured pruning to 50-60%; preserves prompt-following capability efficiently. |
| 36 | AWQ: Activation-aware Weight Quantization for LLM Compression | Lin et al. | 2023 | arXiv:2306.00978 | 80 | 78 | **79** | Activation-aware quantization; minimal prompt accuracy degradation at 4-bit precision. |
| 37 | GPTQ: Accurate Post-Training Quantization for GPT Models | Frantar et al. | 2022 | arXiv:2210.17323 | 82 | 85 | **84** | Layer-wise quantization for GPT models; enables efficient inference with preserved prompt quality. |
| 38 | LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale | Dettmers et al. | 2022 | arXiv:2208.07339 | 85 | 88 | **87** | Mixed-precision int8 inference; enables large model prompting on consumer hardware. |
| 39 | QLoRA: Efficient Finetuning of Quantized LLMs | Dettmers et al. | 2023 | arXiv:2305.14314 | 88 | 90 | **89** | 4-bit quantized fine-tuning; enables instruction tuning on constrained hardware. |
| 40 | Speculative Decoding with Big Little Decoder | Kim et al. | 2023 | arXiv:2302.07863 | 78 | 72 | **75** | Small model drafts, large model verifies; 2x speedup without quality loss. |
| 41 | Medusa: Simple LLM Inference Acceleration Framework | Cai et al. | 2024 | arXiv:2401.10774 | 80 | 74 | **77** | Multiple decoding heads for parallel token prediction; 2-3x throughput improvement. |
| 42 | Draft & Verify: Lossless Large Language Model Acceleration | Leviathan et al. | 2022 | arXiv:2211.17192 | 80 | 75 | **78** | Speculative execution with verification; guarantees identical output with faster inference. |
| 43 | Distilling Step-by-Step: Outperforming Larger LMs with Less Training | Hsieh et al. | 2023 | arXiv:2305.02301 | 82 | 78 | **80** | CoT distillation from large to small models; efficient reasoning via knowledge transfer. |
| 44 | LaMini-LM: A Diverse Herd of Distilled Models from Large-Scale Instructions | Wu et al. | 2023 | arXiv:2304.14402 | 74 | 70 | **72** | Instruction-tuned small models from GPT-4 distillation; efficient prompt-following at small scale. |
| 45 | Orca: Progressive Learning from Complex Explanation Traces | Mukherjee et al. | 2023 | arXiv:2306.02707 | 80 | 82 | **81** | Chain-of-thought distillation at scale; 13B model approaches GPT-4 on reasoning prompts. |
| 46 | Phi-2: Small Language Models with Reasoning Capability | Li et al. | 2023 | Microsoft Blog | 78 | 80 | **79** | High-quality data for small model training; 2.7B model with strong prompt reasoning. |
| 47 | Mixtral of Experts: Sparse Mixture of Experts | Jiang et al. | 2024 | arXiv:2401.04088 | 85 | 88 | **87** | Sparse MoE for efficient scaling; 8x7B active params matches 70B dense model on prompts. |
| 48 | Efficient Streaming Language Models with Attention Sinks | Xiao et al. | 2023 | arXiv:2309.17453 | 84 | 80 | **82** | Attention sink discovery enables infinite streaming; keeps first tokens for stable generation. |
| 49 | GQA: Training Generalized Multi-Query Attention | Ainslie et al. | 2023 | arXiv:2305.13245 | 78 | 76 | **77** | Grouped-query attention for KV efficiency; reduces memory with minimal quality impact. |
| 50 | Ring Attention with Blockwise Transformers for Near-Infinite Context | Liu et al. | 2024 | arXiv:2310.01889 | 82 | 75 | **79** | Distributed attention across devices; enables context length scaling beyond single-GPU memory. |

---

## Papers to Add (Priority Queue for Next Update)

Search targets:
- "PCW: Parallel Context Windows" (Ratner et al., 2022) — extended context via parallel encoding
- "MInference: Speeding Up Long-Context LLM" (2024)
- "H2O: Heavy-Hitter Oracle for KV Cache" (Zhang et al., 2023)
- "Dynamic NTK RoPE scaling" for longer context prompts
- "InfLLM: Infinite Context LLMs" (Xiao et al., 2024)
- "Quest: Query-Aware Sparse KV Cache" (2024)
- "Scissorhands: KV cache compression with attention patterns" (2023)
- "LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding" (2023)
- "Needle-in-a-Haystack" evaluation papers and compression impacts
- Quantization methods impact on prompting quality
- "CoLT5: Faster Long-Range Transformers" (2023)
- Token merging papers (ToMe, DiffRate)
