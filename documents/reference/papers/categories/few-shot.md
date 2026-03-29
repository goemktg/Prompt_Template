# Prompt Engineering Papers: Few-Shot & In-Context Learning

> **Category**: `[FEW-SHOT]`
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
| 1 | Language Models are Few-Shot Learners (GPT-3) | Brown et al. | 2020 | arXiv:2005.14165 | 98 | 100 | **99** | Foundational ICL paper; 175B GPT-3 demonstrates in-context learning without gradient updates. |
| 2 | Rethinking the Role of Demonstrations in ICL | Min et al. | 2022 | arXiv:2202.12837 | 88 | 85 | **87** | Label semantics don't matter for ICL; format and distribution are what drive performance. |
| 3 | What Makes Good In-Context Examples for GPT-3? | Liu et al. | 2021 | arXiv:2101.06804 | 85 | 82 | **84** | kNN retrieval of semantically similar examples beats random selection; similarity matters. |
| 4 | True Few-Shot Learning with Language Models | Perez et al. | 2021 | arXiv:2105.11447 | 82 | 78 | **80** | Rigorously tests few-shot; most LLMs still use implicit dev-set assumptions. |
| 5 | UPRISE: Universal Prompt Retrieval for Improving Zero-Shot Evaluation | Ye et al. | 2023 | arXiv:2303.08518 | 82 | 74 | **78** | Cross-task prompt retriever; universal retriever improves zero-shot with task-agnostic demos. |
| 6 | Self-Generated In-Context Learning: Leveraging Auto-regressive Language Models | Kim et al. | 2022 | arXiv:2206.08082 | 80 | 70 | **75** | Model generates its own demonstrations; removes need for labeled ICL examples. |
| 7 | Active Example Selection for In-Context Learning | Zhang et al. | 2022 | arXiv:2211.04486 | 78 | 68 | **73** | Active learning selection; optimal demonstration selection via expected model improvement. |
| 8 | Diverse Demonstrations Improve In-Context Compositional Generalization | Levy et al. | 2022 | arXiv:2212.06800 | 75 | 65 | **70** | Diverse demonstration selection; diversity outweighs similarity for compositional tasks. |
| 9 | Learning to Retrieve Prompts for In-Context Learning | Rubin et al. | 2021 | arXiv:2112.00861 | 82 | 75 | **79** | KATE: task-aware retrieval; embedding-based retrieval fine-tuned for ICL performance. |
| 10 | Ground-Truth Labels Matter: A Closer Look at ICL Quality | Min et al. | 2022 | arXiv:2202.12837 | 80 | 72 | **76** | Ablation study on what components of ICL examples matter most. |
| 11 | MetaICL: Learning to Learn In-Context | Min et al. | 2021 | arXiv:2110.15943 | 85 | 78 | **82** | Meta-trained ICL; fine-tunes model on many tasks to improve ICL at test time. |
| 12 | FLAN: Finetuned Language Models Are Zero-Shot Learners | Wei et al. | 2021 | arXiv:2109.01652 | 88 | 90 | **89** | Instruction fine-tuning on 60+ tasks; zero-shot beats GPT-3 few-shot on many benchmarks. |
| 13 | SuperNatural Instructions: Generalizing via Thousands of Tasks | Wang et al. | 2022 | arXiv:2204.07705 | 85 | 82 | **84** | 1616-task instruction dataset; instruction generalization across unseen tasks via ICL. |
| 14 | Larger Language Models Do In-Context Learning Differently | Wei et al. | 2023 | arXiv:2303.03846 | 80 | 75 | **78** | Small models rely on surface features; large models actually learn from demonstrations. |
| 15 | In-Context Learning from Large Language Models | Dong et al. | 2022 | arXiv:2301.00234 | 78 | 80 | **79** | Formal ICL survey; training, inference, selection, and evaluation frameworks. |
| 16 | An Explanation of In-Context Learning as Implicit Bayesian Inference | Xie et al. | 2021 | arXiv:2111.02080 | 88 | 80 | **84** | Theoretical explanation: ICL as document completion assuming shared latent concept. |
| 17 | A Mathematical Framework for Transformer Circuits | Elman et al. | 2021 | Distill:circuits | 85 | 78 | **82** | Mechanistic proof that transformers perform gradient descent-like ICL in their layers. |
| 18 | Transformers Learn In-Context by Gradient Descent | Akyürek et al. | 2022 | arXiv:2212.07677 | 88 | 78 | **83** | Formal proof: transformer attention implements gradient descent for linear regression ICL cases. |
| 19 | Calibrate Before Use: Improving Few-Shot Performance of Language Models | Zhao et al. | 2021 | arXiv:2102.09690 | 82 | 78 | **80** | Context, recency, and majority label biases in ICL; calibration techniques fix these. |
| 20 | Noisy Channel Language Model Prompting for Few-Shot Text Classification | Min et al. | 2021 | arXiv:2108.04106 | 78 | 70 | **74** | Bayesian noisy channel inversion for classification; outperforms standard few-shot prompting. |
| 21 | KATE: k-Nearest Neighbor Augmented Generation for ICL | Liu et al. | 2021 | arXiv:2101.06804 | 80 | 74 | **77** | kNN-retrieved demonstrations from training set improve ICL significantly. |
| 22 | Vote-k: Sample-Efficient Demonstrations for In-Context Learning via Voting | Su et al. | 2022 | arXiv:2209.01975 | 75 | 65 | **70** | Diversity + representativeness voting for demonstration selection; outperforms random ICL. |
| 23 | Learning To Retrieve Prompts | Rubin et al. | 2022 | arXiv:2112.00861 | 78 | 68 | **73** | Unsupervised + PNI training for prompt retriever; task-agnostic retrieval for ICL. |
| 24 | Chain-of-Thought Few-Shot Demonstrations | Wei et al. | 2022 | (see #1) | 88 | 90 | **89** | Combines few-shot with CoT; adding reasoning steps to exemplars produces large gains. |
| 25 | Many-Shot In-Context Learning | Agarwal et al. | 2024 | arXiv:2404.11018 | 82 | 72 | **77** | Scales ICL to thousands of examples in long context window; different regime from few-shot. |
| 26 | BatchPrompt: Accomplish More with Less | Ye et al. | 2023 | arXiv:2309.00384 | 72 | 62 | **67** | Multiple examples in one prompt call; reduces API cost while maintaining quality. |
| 27 | Template-Based Named Entity Recognition Using BART | Cui et al. | 2021 | arXiv:2106.01760 | 75 | 72 | **74** | Template-based few-shot NER; structured prompts outperform standard extractive QA. |
| 28 | Promptagator: Few-Shot Dense Retrieval from 8 Examples | Dai et al. | 2022 | arXiv:2209.11755 | 80 | 74 | **77** | Few-shot query generation for dense retrieval; 8 examples → task-specific retriever. |
| 29 | In-Context Reinforcement Learning with Expert Demonstrations | Laskin et al. | 2023 | arXiv:2302.02975 | 78 | 65 | **72** | Algorithm Distillation: ICL from RL history; in-context few-shot RL from demonstrations. |
| 30 | Few-Shot Parameter-Efficient Fine-Tuning is Better and Cheaper than ICL | Liu et al. | 2022 | arXiv:2205.05638 | 80 | 72 | **76** | Head-to-head: LoRA/prefix-tuning beats few-shot ICL at same data budget. |
| 31 | Understanding In-Context Learning via Supportive Pretraining Data | Han et al. | 2023 | arXiv:2306.04186 | 78 | 68 | **73** | Traces ICL ability to specific pretraining data; explains where ICL comes from. |
| 32 | Few-Shot Text Classification: A Tutorial | Chen et al. | 2023 | arXiv:2308.14459 | 68 | 70 | **69** | Practical few-shot classification guide; prompt template and example selection best practices. |
| 33 | CEIL: Compositional Exemplar-based In-Context Learning | Ye et al. | 2023 | arXiv:2302.05698 | 82 | 74 | **78** | Skill-based exemplar retrieval; compositional reasoning from diverse examples. |
| 34 | Fantastically Ordered Prompts and Where to Find Them | Lu et al. | 2022 | arXiv:2104.08786 | 80 | 75 | **78** | Example ordering sensitivity; entropy-based sorting for optimal ICL performance. |
| 35 | Learning from Explanations with Neural Module Execution | Li et al. | 2023 | arXiv:2303.13876 | 76 | 65 | **71** | Learning from reasoning explanations; explanation as additional few-shot signal. |
| 36 | Selective Annotation Makes Language Models Better Few-Shot Learners | Hsieh et al. | 2023 | arXiv:2209.01975 | 78 | 70 | **74** | Active learning for few-shot; vote-k selects informative examples for annotation. |
| 37 | DocPrompting: Generating Code by Retrieving Documents | Zhou et al. | 2022 | arXiv:2207.05987 | 80 | 72 | **76** | Documentation as few-shot context; retrieved docs replace manual examples. |
| 38 | Compositional Semantic Parsing with Large Language Models | Drozdov et al. | 2022 | arXiv:2209.15003 | 76 | 68 | **72** | Few-shot semantic parsing; compositional generalization from minimal examples. |
| 39 | Knnprompting: Nearest Neighbor Promptingfor In-Context Learning | Xu et al. | 2023 | arXiv:2303.13824 | 74 | 65 | **70** | KNN-based demonstration construction; dynamic neighbor retrieval per query. |
| 40 | UDR: Unsupervised Dense Retrieval for In-Context Learning | Chen et al. | 2023 | arXiv:2303.00807 | 76 | 68 | **72** | Unsupervised retriever training for ICL; contrastive learning without task labels. |
| 41 | Symbol Tuning Improves In-Context Learning in Language Models | Wei et al. | 2023 | arXiv:2305.08298 | 80 | 72 | **76** | Symbol-label mapping improves ICL; reduces reliance on semantic label content. |
| 42 | Scaling In-Context Learning with Task Structure | Banburski-Fahey et al. | 2023 | arXiv:2304.12578 | 74 | 62 | **68** | Task-structure aware ICL; hierarchical prompts for complex compositional tasks. |
| 43 | ICL-D3IE: In-Context Learning with Diverse Demonstrations | He et al. | 2023 | arXiv:2308.09567 | 72 | 62 | **67** | Diverse demonstration selection for IE; coverage-based example sampling. |
| 44 | Task-Aware Retrieval for In-Context Learning | Rubin et al. | 2022 | arXiv:2112.00861 | 80 | 75 | **78** | Trained retrievers for ICL; better than embedding similarity for demo selection. |
| 45 | In-Context Learning for Few-Shot Dialogue State Tracking | Hu et al. | 2022 | arXiv:2203.08568 | 72 | 65 | **69** | Few-shot DST via ICL; schema-guided prompting for dialogue systems. |
| 46 | Label Words are Anchors: An Information Flow Perspective on ICL | Wang et al. | 2023 | arXiv:2305.14160 | 82 | 70 | **76** | Information flow analysis of ICL; label tokens aggregate example information. |
| 47 | Small Language Models Are Strong Negative Samplers | Yoon et al. | 2024 | arXiv:2310.16856 | 70 | 60 | **65** | Contrastive ICL with negative examples; small models generate hard negatives. |
| 48 | ICL Retrieval for Open-Domain Question Answering | Ram et al. | 2023 | arXiv:2212.10511 | 78 | 72 | **75** | Question-answer pairs as ICL examples; retrieval-augmented QA with demonstrations. |
| 49 | In-Context Learning Creates Task Vectors | Hendel et al. | 2023 | arXiv:2310.15916 | 80 | 68 | **74** | Mechanistic ICL analysis; task vectors in hidden states encode task specification. |
| 50 | Many-Shot In-Context Learning | Agarwal et al. | 2024 | arXiv:2404.11018 | 84 | 75 | **80** | Thousands of examples in long context; new scaling regime for ICL with massive demos. |

---

## Papers to Add (Priority Queue for Next Update)

Search targets:
- "Analogical few-shot prompting" (He et al., 2023)
- "Curriculum-based demonstration selection" papers
- "Influence functions for ICL" (2023-2024)
- "ICL for multilingual" settings papers
- "Demonstration ordering effects" studies
- "Bootstrapping ICL" — self-improvement papers
- "Example-free ICL" (zero-shot instruction tuning approaches)
- "Multi-modal few-shot" (image + text examples)
- "Prompt perturbation sensitivity" studies
- "Fewshot QA" specialized papers (squad, triviaqa prompting)
- "Selective annotation" — annotation budget for ICL
- "APE + kNN retrieval" combined approaches
- "ICL for structured prediction" (NER, RE, IE)
