# 프롬프트 엔지니어링 논문: 멀티모달 프롬프팅

> **카테고리**: `[MULTIMODAL]`
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
| 1 | GPT-4V(ision): Technical Report | OpenAI | 2023 | arXiv:2303.08774 | 92 | 96 | **94** | GPT-4 with vision; sets standard for multimodal few-shot prompting with images. |
| 2 | LLaVA: Visual Instruction Tuning | Liu et al. | 2023 | arXiv:2304.08485 | 90 | 88 | **89** | Visual instruction tuning via GPT-4-generated data; end-to-end multimodal prompting pipeline. |
| 3 | MiniGPT-4: Enhancing Vision-Language Understanding | Zhu et al. | 2023 | arXiv:2304.10592 | 82 | 80 | **81** | Aligned visual instruction via two-stage training; efficient visual-language prompt alignment. |
| 4 | InstructBLIP: Towards General Visual Instruction Following | Dai et al. | 2023 | arXiv:2305.06500 | 85 | 82 | **84** | Instruction-tuned BLIP; visual instruction prompting across 26 zero-shot datasets. |
| 5 | Multimodal Chain-of-Thought Reasoning in Language Models | Zhang et al. | 2023 | arXiv:2302.00923 | 85 | 80 | **83** | Vision + language CoT; two-stage: rationale generation then answer; multimodal reasoning. |
| 6 | Flamingo: a Visual Language Model for Few-Shot Learning | Alayrac et al. | 2022 | arXiv:2204.14198 | 92 | 90 | **91** | Interleaves image/text few-shot; Flamingo's perceiver resampler enables flexible multimodal ICL. |
| 7 | CLIP: Learning Transferable Visual Models from Natural Language | Radford et al. | 2021 | arXiv:2103.00020 | 95 | 98 | **97** | Contrastive image-text training; zero-shot vision via natural language prompt classification. |
| 8 | Visual Prompt Tuning (VPT) | Jia et al. | 2022 | arXiv:2203.12119 | 88 | 84 | **86** | Learnable visual tokens prepended to vision transformer; PEFT for visual tasks without full fine-tuning. |
| 9 | CoCoOp: Conditional Context Optimization for Vision-Language Models | Zhou et al. | 2022 | arXiv:2203.05557 | 82 | 78 | **80** | Conditionally generate text prompts from visual input; generalizes across unseen class prompts. |
| 10 | CoOp: Learning to Prompt for Vision-Language Models | Zhou et al. | 2022 | arXiv:2109.01134 | 85 | 84 | **85** | Learnable continuous context for CLIP; soft text prompt tuning for image classification. |
| 11 | DALL-E 2: Hierarchical Text-Conditional Image Generation | Ramesh et al. | 2022 | arXiv:2204.06125 | 90 | 90 | **90** | CLIP embeddings for text-image synthesis; prompt engineering for image generation pioneered here. |
| 12 | Stable Diffusion: High-Resolution Image Synthesis with Latent Diffusion | Rombach et al. | 2022 | arXiv:2112.10752 | 92 | 95 | **94** | Latent diffusion + text conditioning; foundation of all modern text-to-image prompt engineering. |
| 13 | Prompt-to-Prompt: Image Editing with Cross Attention Control | Hertz et al. | 2022 | arXiv:2208.01626 | 88 | 82 | **85** | Attention maps for prompt-based image editing; swap/refine tokens for targeted image modification. |
| 14 | DreamBooth: Fine-Tuning Text-to-Image Diffusion Models | Ruiz et al. | 2022 | arXiv:2208.12242 | 88 | 88 | **88** | Subject-specific fine-tuning with unique identifier token; personalized image generation via prompts. |
| 15 | Textual Inversion: An Image is Worth One Word | Gal et al. | 2022 | arXiv:2208.01618 | 85 | 82 | **84** | Learns pseudo-words for visual concepts; new visual prompt tokens without architecture changes. |
| 16 | BLIP-2: Bootstrapping Language-Image Pre-training | Li et al. | 2023 | arXiv:2301.12597 | 88 | 86 | **87** | Q-Former bridges frozen vision encoder and LLM; efficient visual instruction prompting. |
| 17 | CogVLM: Visual Expert for Pretrained Language Models | Wang et al. | 2023 | arXiv:2311.03079 | 82 | 76 | **79** | Deep fusion via visual expert modules in each LLM layer; stronger than adapter approaches. |
| 18 | Gemini: A Family of Highly Capable Multimodal Models | Gemini Team | 2023 | arXiv:2312.11805 | 90 | 90 | **90** | Natively multimodal from pretraining; sets new bar for interleaved image-text prompting. |
| 19 | GPT-4o Technical Report | OpenAI | 2024 | Blog | 88 | 90 | **89** | Any-to-any modality model; simultaneous audio/image/text prompting in real-time. |
| 20 | ScienceQA with Multimodal CoT Prompting | Lu et al. | 2022 | arXiv:2209.09513 | 80 | 74 | **77** | Science QA with image context; introduces multimodal CoT annotation benchmark. |
| 21 | Video-LLaVA: Learning United Visual Representation by Alignment | Lin et al. | 2023 | arXiv:2311.10122 | 78 | 70 | **74** | Unified visual tokenization for image + video; single prompt template for both modalities. |
| 22 | Audio-Visual LLM Prompting for Scene Understanding | Various | 2024 | arXiv:2402.10436 | 75 | 62 | **69** | Combined audio-visual prompt strategies for scene understanding; multi-sensory grounding. |
| 23 | Claude 3 Vision Prompting Best Practices | Anthropic | 2024 | Documentation | 70 | 78 | **74** | Official guide for vision prompting; image detail, ordering, and task-specific patterns for Claude. |
| 24 | Emu2: Generative Multimodal Models are In-Context Learners | Sun et al. | 2024 | arXiv:2312.13286 | 82 | 70 | **76** | 37B generative model with strong multimodal ICL; arbitrary interleaved image-text sequences. |
| 25 | IDEFICS2: An 8B Vision-Language Model Efficient for Multimodal Tasks | Laurencon et al. | 2024 | arXiv:2405.02246 | 78 | 72 | **75** | Efficient multimodal ICL at scale; 8B model with strong interleaved understanding. |
| 26 | InternVL: Scaling Vision Foundation Models and Aligning for Multimodal Tasks | Chen et al. | 2024 | arXiv:2312.14238 | 82 | 78 | **80** | Large-scale vision-language alignment; progressive alignment strategy for multimodal prompting. |
| 27 | Phi-3-Vision: A Small Yet Capable Multimodal Model | Abdin et al. | 2024 | arXiv:2404.14219 | 76 | 74 | **75** | Efficient small multimodal model; strong vision prompt performance at 4B parameters. |
| 28 | VideoChat: Chat-Centric Video Understanding | Li et al. | 2023 | arXiv:2305.06355 | 78 | 70 | **74** | Video understanding via chat; temporal reasoning from video prompts. |
| 29 | Video-ChatGPT: Towards Detailed Video Understanding | Maaz et al. | 2023 | arXiv:2306.05424 | 76 | 72 | **74** | Video instruction tuning; spatiotemporal prompting for video QA tasks. |
| 30 | MovieChat: From Dense Token to Sparse Memory for Long Video Understanding | Song et al. | 2023 | arXiv:2307.16449 | 74 | 65 | **70** | Long video understanding via memory; sparse token prompts for hour-long videos. |
| 31 | Whisper: Robust Speech Recognition via Large-Scale Weak Supervision | Radford et al. | 2022 | arXiv:2212.04356 | 90 | 95 | **93** | Foundation speech model; text prompts control language, task, and output format. |
| 32 | AudioGPT: Understanding and Generating Speech, Music, Sound, and Talking Head | Huang et al. | 2023 | arXiv:2304.12995 | 78 | 70 | **74** | Multi-modal audio generation; text prompts for speech, music, and sound synthesis. |
| 33 | Qwen-Audio: Advancing Universal Audio Understanding | Chu et al. | 2023 | arXiv:2311.07919 | 80 | 72 | **76** | Unified audio-language model; handles diverse audio types with consistent prompting. |
| 34 | SALMONN: Speech Audio Large Language Model | Tang et al. | 2023 | arXiv:2310.13289 | 76 | 68 | **72** | Speech-text LLM; audio events and speech in unified prompt framework. |
| 35 | DocPedia: Unleashing the Power of LLMs in Document Understanding | Feng et al. | 2024 | arXiv:2312.03195 | 74 | 68 | **71** | Document understanding via prompting; handles diverse document formats and layouts. |
| 36 | TextMonkey: An OCR-Free Large Multimodal Model for Understanding Document | Liu et al. | 2024 | arXiv:2403.04473 | 72 | 65 | **69** | OCR-free document understanding; direct image-to-answer prompting for documents. |
| 37 | ChartLlama: A Multimodal LLM for Chart Understanding and Generation | Han et al. | 2023 | arXiv:2311.16483 | 74 | 66 | **70** | Chart-specific multimodal LLM; structured extraction from visual data representations. |
| 38 | MatPlotAgent: Method and Evaluation for LLM-Based Agentic Scientific Data Visualization | Yang et al. | 2024 | arXiv:2402.11453 | 70 | 62 | **66** | Scientific visualization agent; matplotlib code generation from data prompts. |
| 39 | DocOwl 1.5: Unified Structure Learning for OCR-free Document Understanding | Hu et al. | 2024 | arXiv:2403.12895 | 74 | 68 | **71** | Structure-aware document model; handles tables, charts, and text in unified framework. |
| 40 | Vary: Scaling up the Vision Vocabulary for LVLMs | Wei et al. | 2024 | arXiv:2312.06109 | 76 | 68 | **72** | Extended visual vocabulary; fine-grained document and chart understanding. |
| 41 | ControlNet: Adding Conditional Control to Text-to-Image Diffusion Models | Zhang et al. | 2023 | arXiv:2302.05543 | 90 | 92 | **91** | Spatial conditioning for image generation; edge/depth/pose prompts for precise control. |
| 42 | IP-Adapter: Text Compatible Image Prompt Adapter | Ye et al. | 2023 | arXiv:2308.06721 | 82 | 78 | **80** | Image prompts for diffusion models; image-based conditioning alongside text. |
| 43 | PhotoMaker: Customizing Realistic Human Photos via Stacked ID Embedding | Li et al. | 2023 | arXiv:2312.04461 | 76 | 72 | **74** | Identity-preserving generation; photo prompts for consistent character generation. |
| 44 | InstantID: Zero-shot Identity-Preserving Generation | Wang et al. | 2024 | arXiv:2401.07519 | 80 | 78 | **79** | Zero-shot face preservation; single image prompt for identity transfer. |
| 45 | SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis | Podell et al. | 2023 | arXiv:2307.01952 | 85 | 88 | **87** | Improved stable diffusion; enhanced prompt following and image quality at high resolution. |
| 46 | Playground v2.5: Three Insights towards Enhancing Aesthetic Quality | Li et al. | 2024 | arXiv:2402.17245 | 74 | 70 | **72** | Aesthetic-focused diffusion; improved prompt-to-aesthetic mapping. |
| 47 | DALL-E 3 Improving Image Generation with Better Captions | Betker et al. | 2023 | OpenAI Tech Report | 85 | 88 | **87** | Caption-improved generation; demonstrates prompt understanding advances via better training data. |
| 48 | Sora: Creating Video from Text | Brooks et al. | 2024 | OpenAI Tech Report | 92 | 90 | **91** | Text-to-video at unprecedented quality; minute-long coherent video from text prompts. |
| 49 | Imagen Video: High Definition Video Generation with Diffusion Models | Ho et al. | 2022 | arXiv:2210.02303 | 85 | 82 | **84** | High-def video diffusion; cascade diffusion with text prompts for video synthesis. |
| 50 | Make-A-Video: Text-to-Video Generation without Text-Video Data | Singer et al. | 2022 | arXiv:2209.14792 | 82 | 80 | **81** | Zero-shot video generation; leverages text-image knowledge for video prompting. |

---

## 추가 예정 논문 (다음 업데이트 우선순위 대기열)

검색 대상:
- "GPT-4V prompt engineering" systematic studies (2024)
- "Gemini Ultra multimodal" benchmarks vs prompting strategies
- "Claude Sonnet vision" evaluation papers
- "Video prompting" strategies for long video understanding
- "Audio prompting" (Whisper, speech LLMs)
- "Document understanding" prompting (PDFs, charts, tables)
- "OCR + LLM" prompting for document QA
- "Chart/graph understanding" prompting studies
- "3D scene understanding" multimodal prompts
- "Multi-image reasoning" prompting (2024-2025)
- "Interleaved generation" papers (text + image generation)
- "IDEFICS2" (multimodal ICL at scale)
- "InternVL" series (2024) prompting strategies
- "Phi-3-Vision" prompting efficiency papers
