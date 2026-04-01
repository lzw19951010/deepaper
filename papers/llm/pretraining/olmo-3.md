---
abstract: We introduce Olmo 3, a family of state-of-the-art, fully-open language models
  at the 7B and 32B parameter scales. Olmo 3 model construction targets long-context
  reasoning, function calling, coding, instruction following, general chat, and knowledge
  recall. This release includes the entire model flow, i.e., the full lifecycle of
  the family of models, including every stage, checkpoint, data point, and dependency
  used to build it. Our flagship model, Olmo 3 Think 32B, is the strongest fully-open
  thinking model released to-date.
arxiv_categories:
- cs.CL
arxiv_id: '2512.13961'
authors:
- Team Olmo
- ':'
- Allyson Ettinger
- Amanda Bertsch
- Bailey Kuehl
- David Graham
- David Heineman
- Dirk Groeneveld
- Faeze Brahman
- Finbarr Timbers
- Hamish Ivison
- Jacob Morrison
- Jake Poznanski
- Kyle Lo
- Luca Soldaini
- Matt Jordan
- Mayee Chen
- Michael Noukhovitch
- Nathan Lambert
- Pete Walsh
- Pradeep Dasigi
- Robert Berry
- Saumya Malik
- Saurabh Shah
- Scott Geng
- Shane Arora
- Shashank Gupta
- Taira Anderson
- Teng Xiao
- Tyler Murray
- Tyler Romero
- Victoria Graf
- Akari Asai
- Akshita Bhagia
- Alexander Wettig
- Alisa Liu
- Aman Rangapur
- Chloe Anastasiades
- Costa Huang
- Dustin Schwenk
- Harsh Trivedi
- Ian Magnusson
- Jaron Lochner
- Jiacheng Liu
- Lester James V. Miranda
- Maarten Sap
- Malia Morgan
- Michael Schmitz
- Michal Guerquin
- Michael Wilson
- Regan Huff
- Ronan Le Bras
- Rui Xin
- Rulin Shao
- Sam Skjonsberg
- Shannon Zejiang Shen
- Shuyue Stella Li
- Tucker Wilde
- Valentina Pyatkin
- Will Merrill
- Yapei Chang
- Yuling Gu
- Zhiyuan Zeng
- Ashish Sabharwal
- Luke Zettlemoyer
- Pang Wei Koh
- Ali Farhadi
- Noah A. Smith
- Hannaneh Hajishirzi
baselines:
- 'Qwen 3 32B (32B, type: open-weight)'
- 'Qwen 3 VL 32B Think (32B, type: open-weight)'
- 'Qwen 3 8B (8B, type: open-weight)'
- 'Qwen 3 VL 8B Think (8B, type: open-weight)'
- 'Qwen 2.5 32B (32B, type: open-weight)'
- 'Qwen 2.5 7B (7B, type: open-weight)'
- 'DeepSeek-R1-Distill-Qwen-32B (32B, type: open-weight)'
- 'DeepSeek-R1-Distill-Qwen-7B (7B, type: open-weight)'
- 'Gemma 3 27B (27B, type: open-weight)'
- 'Gemma 2 27B (27B, type: open-weight)'
- 'Gemma 2 9B (9B, type: open-weight)'
- 'Llama 3.1 70B (70B, type: open-weight)'
- 'Llama 3.1 8B (8B, type: open-weight)'
- 'Mistral Small 3.1 24B (24B, type: open-weight)'
- 'IBM Granite 3.3 8B (8B, type: open-weight)'
- 'Nemotron Nano 9B v2 (9B, type: open-weight)'
- 'Xiaomi MiMo 7B (7B, type: open-weight)'
- 'Seed 36B (36B, type: open-weight)'
- 'OpenThinker3 7B (7B, type: open-weight)'
- 'OpenReasoning Nemotron 7B (7B, type: open-weight)'
- 'OLMo 2 32B (32B, type: fully-open)'
- 'OLMo 2 7B (7B, type: fully-open)'
- 'Stanford Marin 32B (32B, type: fully-open)'
- 'Stanford Marin 8B (8B, type: fully-open)'
- 'Apertus 70B (70B, type: fully-open)'
- 'Apertus 8B (8B, type: fully-open)'
- 'Gaperon 24B (24B, type: fully-open)'
- 'Gaperon 8B (8B, type: fully-open)'
- 'LLM360 K2-V2 70B (70B, type: fully-open)'
category: llm/pretraining
code_url: github.com/allenai/OLMo-core (pretrain), github.com/allenai/open-instruct
  (posttrain), github.com/allenai/dolma3 (data), github.com/allenai/olmes (eval),
  github.com/allenai/decon (decontamination), github.com/allenai/duplodocus (dedup)
core_contribution: new-framework
datasets:
- 'Dolma 3 Mix (5.93T tokens: 76.1% Common Crawl + 13.6% olmOCR science PDFs + 6.89%
  Stack-Edu code + 2.56% FineMath + 0.86% arXiv + 0.04% Wikipedia)'
- 'Dolma 3 Dolmino Mix (100B tokens: 22.5% Common Crawl HQ + 18.5% Math synth + 20.0%
  Code + 8.9% QA synth + 6.1% Thinking traces synth + 6.1% Instruction + 5.0% olmOCR
  PDFs HQ + 5.0% STEM-Heavy Crawl + 7.9% other)'
- 'Dolma 3 Longmino Mix (50B tokens: 66.1% Midtraining mix + 17.8% olmOCR PDFs 8K-64K
  + 12.2% olmOCR+synth REX + 3.88% olmOCR+synth CWE)'
- Dolci Think SFT (45.2-45.4B tokens for 7B/32B)
- Dolci Think DPO (150K-200K preference pairs)
- 'Dolci Think RL (104,869 prompts: math + code + IF + general chat)'
- Dolci Instruct SFT (3.4M tokens)
- Dolci Instruct DPO (260K preference pairs)
- Dolci Instruct RL (171,950 prompts)
- Dolci RL-Zero (13,314 prompts)
- MATH 500 (eval)
- AIME 2024 (eval)
- AIME 2025 (eval)
- OMEGA Math (eval, 55 subtasks)
- BigBench-Hard (eval, 23 subtasks)
- ZebraLogic (eval)
- AGI Eval English (eval, 9 subtasks)
- HumanEvalPlus (eval)
- MBPP+ (eval)
- LiveCodeBench v3 (eval)
- IFEval (eval)
- IFBench (eval)
- MMLU (eval, 57 subtasks)
- PopQA (eval)
- GPQA (eval)
- AlpacaEval 2 (eval)
date: '2025-12-15'
doi: null
keywords: &id001
- fully-open language model
- thinking model
- reinforcement learning with verifiable rewards (RLVR)
- GRPO
- delta learning
- midtraining data curriculum
- long-context extension
- model flow
- olmOCR science PDFs
- post-training pipeline (SFT+DPO+RL)
metrics:
- EM Flex (CoT, temp=0.6, top-p=0.95, max_tokens=32768, N=1) — MATH, BigBench-Hard
- EM Flex (CoT, temp=0.6, top-p=0.95, max_tokens=32768, N=32) — AIME 2024, AIME 2025
- EM Flex (CoT, temp=0.6, top-p=0.95, max_tokens=32768, N=1, 55 subtasks) — OMEGA
  Math
- pass@1 (CoT Code, temp=0.6, top-p=0.95, max_tokens=32768, N=10) — HumanEvalPlus,
  MBPP+, LiveCodeBench v3
- Custom (CoT JSON, temp=0.6, top-p=0.95, max_tokens=32768, N=1) — ZebraLogic
- Accuracy (CoT MC, temp=0.6, top-p=0.95, max_tokens=32768, N=1) — GPQA, AGI Eval,
  MMLU, PopQA
- Custom (CoT, temp=0.6, top-p=0.95, max_tokens=32768, N=1) — IFEval
- Winrate (CoT, temp=0.6, top-p=0.95, max_tokens=32768, N=1) — AlpacaEval 2
publication_type: preprint
tags: *id001
title: Olmo 3
tldr: OLMo 3 是首个在 7B/32B 规模达到 SOTA 的完全开放语言模型家族，旗舰 OLMo 3.1 Think 32B 在 MATH 达 96.2%、AIME
  2025 达 78.1%，逼近 Qwen 3 32B 且仅用其 1/6 训练 token
url: https://arxiv.org/abs/2512.13961
venue: arXiv preprint
---

#### 核心速览 (Executive Summary)

##### TL;DR

OLMo 3 是 AI2 发布的完全开放（fully-open）语言模型家族，覆盖 7B 和 32B 两个参数规模，公开了从预训练数据、中间检查点到后训练代码的全部流程（model flow）。旗舰模型 OLMo 3.1 Think 32B 在 MATH 达到 96.2%、AIME 2024 达 80.6%、AIME 2025 达 78.1%、HumanEvalPlus 达 91.5%、IFEval 达 93.8%，是目前最强的完全开放思维模型，接近 Qwen 3 32B（MATH 95.4%、AIME 2025 70.9%）且仅使用约 1/6 的训练 token。整个 32B Think 模型训练在 1024 张 H100 上耗时约 56 天，估计成本约 275 万美元。

##### 一图流

**旧方法：** 以往完全开放模型（如 OLMo 2 32B：MATH 49.2%、AIME 2025 0.9%）在推理能力上远落后于开源权重模型（如 Qwen 3 32B：MATH 95.4%），核心差距在于缺乏思维链训练和有效的 RL 框架。

**新方法：** OLMo 3 构建了完整的 model flow 流水线——5.93T token 预训练 + 100B 高质量 midtraining + 50-100B 长上下文扩展 + SFT/DPO/RL 三阶段后训练——配合新提出的 OlmoRL 框架（4x 训练加速）和 Delta Learning 偏好调优，使完全开放模型首次逼近 SOTA 开源权重模型水平（MATH 96.2% vs 95.4%）。

##### 核心机制一句话

**通过三阶段后训练流水线（SFT → Delta Learning DPO → OlmoRL RLVR）对精心构建的多阶段基座模型进行推理能力渐进增强，使完全开放模型在数学/代码/指令遵循等任务上达到与闭源权重模型可比的性能。**

#### 动机与第一性原理 (Motivation & First Principles)

##### 痛点

1. **完全开放模型与开源权重模型的巨大性能鸿沟。** 在 OLMo 3 之前，完全开放模型（公开所有数据和代码）在推理任务上远落后于仅公开权重的模型。OLMo 2 Instruct 32B 在 MATH 仅 49.2%、AIME 2025 仅 0.9%，而同期 Qwen 3 32B 达到 MATH 95.4%、AIME 2025 70.9%——差距高达 46 和 70 个百分点。Apertus 70B 尽管参数量翻倍也仅 MATH 36.2%。这说明仅靠预训练数据公开还远不够，后训练阶段的数据和方法同样至关重要。

2. **思维模型的 RL 训练面临严重的效率瓶颈。** 思维模型生成的推理链极长（32K token 级别），导致 RL 训练中 75% 的时间用于等待推理引擎生成 rollout，推理与训练的计算比高达 5:1（32B 模型）。OLMo 2 的 RL 基础设施仅 881 tokens/sec，在如此长序列下完全不可行。

3. **高质量偏好数据的构造困境。** 传统 DPO 依赖 LLM-as-judge 评价，但在思维模型领域，几乎没有开放思维模型可用于生成对比数据。直接在 Qwen3 32B 的 chosen 数据上做 continued SFT 反而损害性能（对比 Table 21：Cont. SFT avg 64.5 vs DPO delta learning avg 72.9）。

##### 核心洞察（Because → Therefore 因果链）

1. **Because** 完全开放模型在预训练数据质量和规模上已接近开源权重模型（OLMo 3 Base 32B 在 base eval 上超越所有其他 fully-open 基座模型），**but** 差距主要在后训练阶段（SFT→DPO→RL 的累积效果）。**Therefore** 论文将核心精力放在构建完整的后训练流水线（Dolci 数据 + OlmoRL 框架），而非单纯扩大预训练规模。

2. **Because** 当 SFT 模型在某些推理能力维度上已接近饱和（对 Qwen3 32B 数据做 continued SFT 反而下降 5.8 个点，Table 21），而 DPO 的 delta learning 方式（强模型 chosen + 弱模型 rejected 配对）却能从相同数据中提取额外的对比信号（avg +8.4 对比 continued SFT，Table 21）。**Therefore** 论文选择 Delta Learning 作为核心偏好调优策略——利用模型能力差异（capability gap）构造对比对。

3. **Because** DPO 不仅直接提升推理能力（SFT→DPO: AIME 2025 从 66.2% 到 70.7%），更重要的是它为 RL 提供了更好的初始点（SFT+DPO+RLVR avg 74.1 vs SFT+RLVR avg 71.9，Table 22），且 DPO 后更短的响应让模型在固定 8K RL 窗口内能"更聪明地使用每个 token"。**Therefore** 三阶段流水线（SFT→DPO→RL）是系统最优，而非仅做 SFT+RL。

##### 物理/直觉解释

可以把 OLMo 3 的训练流程比作培养一个全能运动员。**预训练**相当于打基础体能——大量的跑步、游泳、力量训练（5.93T token 的通用文本）。**Midtraining** 相当于专项训练——开始重点练习数学推理、编程等特定技能（100B 高质量合成数据），同时加入"思维链示范"让运动员学会"边做边想"。**长上下文扩展**类似拉伸训练——增加运动员能处理的"动作幅度"（从 8K 扩展到 65K context）。然后是后训练三阶段：**SFT** 是教练示范标准动作（学习 45B token 的思维链示例）；**Delta Learning DPO** 是放两段比赛录像——一段是冠军的表现、一段是新手的表现——让运动员学会分辨"好在哪里"（对比式学习）；**RLVR** 是实战训练——每次比赛后自动判定对错，强化正确策略（10 万+ 次"模拟赛"）。OlmoRL 的 inflight updates 就像教练不等所有运动员都跑完比赛就开始点评先完成的运动员，把等待时间利用起来——最终获得 4 倍训练效率提升。

#### 方法详解 (Methodology)

##### 直觉版

参考 Figure 2（model flow 概览图），OLMo 3 的整体流程分为两大阶段：

**旧方法（OLMo 2）：** 预训练 → midtraining → SFT → DPO，无长上下文支持，无思维链训练，RL 仅限数学领域，基础设施慢（881 tokens/sec）。结果：MATH 49.2%。

**新方法（OLMo 3）：** 预训练（5.93T）→ Midtraining（100B，含思维链和指令数据）→ 长上下文扩展（50-100B）→ Think SFT（45B token 思维链数据）→ Delta Learning DPO（150-200K 对）→ OlmoRL RLVR（10 万+ 多领域 prompt）。同时构建了 Instruct 和 RL-Zero 两个分支。结果：MATH 96.2%，提升 47 个百分点。

核心创新在三处：(1) Delta Learning 让 DPO 在模仿学习饱和后仍能提取对比信号；(2) OlmoRL 通过 7 项算法改进和 inflight updates 实现 4x 训练加速；(3) 精心设计的数据课程让中间阶段逐步为后训练铺路。

##### 精确版

###### 完整数据流图

```
Input: Raw web text (9.31T pool)
  │
  ├─ Resiliparse 提取 → 语言过滤(fastText) → 去重(duplodocus: exact + MinHash)
  │   → WebOrganizer 24-topic 分类 → fastText 质量评分
  │   → quality-aware upsampling → Dolma 3 Mix (5.93T tokens)
  │
  ▼
[Stage 1: Pretraining] 5.93T tokens (7B) / 5.5T tokens (32B)
  │  76.1% Common Crawl + 13.6% olmOCR PDFs + 6.89% Code + 2.56% FineMath + 0.86% arXiv
  │  Architecture: 32/64 layers, SwiGLU, QK-Norm, RMSNorm, sliding window attention (3/4 layers, 4096 window)
  │  8192 seq len, batch 512/1024, peak LR 3e-4 / 6e-4
  │
  ▼
[Stage 2: Midtraining] 100B tokens (Dolma 3 Dolmino Mix)
  │  22.5% HQ web + 18.5% math synth + 20% code + 8.9% QA + 6.1% thinking traces + 6.1% instruction
  │  关键：加入思维链/指令数据 → base eval avg +1.9, Math +5.6 (Table 10)
  │  迭代 5 轮混合 → Round5 vs Round1: avg +3.4, Math +9.7 (Table 6)
  │  32B: model souping (合并两次独立 midtraining run)
  │
  ▼
[Stage 3: Long-context Extension] 50B (7B) / 100B (32B) tokens
  │  66.1% midtraining data + 17.8% olmOCR PDFs(8K-64K) + 12.2% synth REX + 3.88% synth CWE
  │  seq len: 65536, YaRN on full attention layers only
  │  → OLMo 3 Base (支持 65K context)
  │
  ▼
[Post-training Branch 1: Think]
  │
  ├─ Think SFT: 45.2-45.4B tokens, LR 5e-5 / 1e-4, max_seq 32K
  │   数据: 多源合成思维链 (Qwen3 32B / DeepSeek R1 生成)
  │   模型 souping: 合并不同 LR 检查点
  │
  ├─ Think DPO (Delta Learning): 150-200K pairs, beta=5
  │   Chosen: Qwen 3 32B 生成 (强模型)
  │   Rejected: Qwen 3 0.6B 生成 (弱模型)
  │   → 长度归一化 DPO loss
  │   → avg +2.6 (SFT→DPO, Table 22), AIME25 +4.5
  │
  ├─ Think RL (OlmoRL): 104,869 prompts, 750-1,400 steps
  │   4 domain: Math(30K) + Code(23K) + IF(30K) + Chat(21K)
  │   → GRPO + 7 algorithmic improvements
  │   → 4x infra speedup via inflight updates
  │
  ▼
Output: OLMo 3.1 Think 32B (MATH 96.2%, AIME25 78.1%, IFEval 93.8%)

[Post-training Branch 2: Instruct] — 从 Think SFT 检查点出发 warm-start
[Post-training Branch 3: RL-Zero] — 直接从 Base 出发做 RLVR
```

###### 关键公式

**公式 1: OlmoRL 目标函数（Eq. 1）**

$$J(\theta) = \frac{1}{\sum_{i=1}^{G}|y_i|}\sum_{i=1}^{G}\sum_{t=1}^{|y_i|}\min\left(\frac{\pi(y_{i,t}|x,y_{i,<t};\theta_{old})}{\pi_{vllm}(y_{i,t}|x,y_{i,<t};\theta_{old})}, \rho\right)\min\left(r_{i,t}A_{i,t}, \text{clip}(r_{i,t}, 1-\varepsilon_{low}, 1+\varepsilon_{high})A_{i,t}\right)$$

物理含义：
- 外层 $\frac{1}{\sum|y_i|}$ 是 **token-level 归一化**——按总 token 数而非样本数归一化损失，消除长序列偏差（长回答不会因为 token 多而获得更大梯度权重）
- $\min(\cdot, \rho)$ 是 **截断重要性采样（TIS）**——因为推理引擎（vLLM）和训练引擎的 log prob 可能因精度/实现不同而有差异，$\rho = 2.0$（32B）截断极端比率，稳定训练
- $r_{i,t} = \frac{\pi(y_{i,t}|\cdot;\theta)}{\pi(y_{i,t}|\cdot;\theta_{old})}$ 是标准的策略比率
- $\text{clip}(r_{i,t}, 1-\varepsilon_{low}, 1+\varepsilon_{high})$ 使用非对称裁剪：$\varepsilon_{low} = 0.2$, $\varepsilon_{high} = 0.272$。上界更宽松是为了允许策略向好的方向做更大更新（来自 DAPO）
- 与 vanilla GRPO 的区别：去除了 KL 惩罚项（允许更自由的策略更新且未导致过优化）

**公式 2: 优势函数（Eq. 2）**

$$A_{i,t} = r(x, y_i) - \text{mean}(\{r(x, y_i)\}_{i=1}^{G})$$

物理含义：
- 组内相对优势，$G = 8$（group size）
- **不做标准差归一化**（来自 Dr GRPO）——传统 GRPO 除以 std 会导致"太简单"（全对）和"太难"（全错）的题 std 很小，归一化后 advantage 被放大，形成 difficulty bias
- $r(x, y_i)$ 由对应领域的 verifier 返回（数学: SymPy 判定 0/1; 代码: 测试用例通过率; IF: 约束满足率; Chat: LLM-judge 0-1 连续分数）

**公式 3: 长度归一化 DPO Loss（Appendix A.6.2）**

$$\max_{\pi_\theta} \mathbb{E}_{(x,y_c,y_r)\sim D}\left[\log\sigma\left(\frac{\beta}{|y_c|}\log\frac{\pi_\theta(y_c|x)}{\pi_{ref}(y_c|x)} - \frac{\beta}{|y_r|}\log\frac{\pi_\theta(y_r|x)}{\pi_{ref}(y_r|x)}\right)\right]$$

物理含义：
- $\beta = 5$（KL 正则化系数，较高值约束策略不要偏离参考模型太远）
- 对 chosen 和 rejected 的 log likelihood 分别除以其长度 $|y_c|$ 和 $|y_r|$——消除长度偏差，避免模型仅因为短回答的 per-token log prob 更高而偏好短回答

###### 数值推演：OlmoRL 单步更新

假设一个数学题 $x$，group size $G = 8$，生成 8 个回答 $y_1, \ldots, y_8$：
- 5 个回答正确 ($r = 1$)，3 个错误 ($r = 0$)
- $\text{mean}(r) = 5/8 = 0.625$
- 正确回答的 advantage: $A = 1 - 0.625 = +0.375$（鼓励）
- 错误回答的 advantage: $A = 0 - 0.625 = -0.625$（抑制）

对于正确回答中的某个 token $t$，假设策略比率 $r_{i,t} = 1.1$：
- 无裁剪项: $r_{i,t} \times A = 1.1 \times 0.375 = 0.4125$
- 裁剪项: $\text{clip}(1.1, 0.8, 1.272) \times 0.375 = 1.1 \times 0.375 = 0.4125$（未触发裁剪）
- 取 min = 0.4125

如果策略比率增大到 $r_{i,t} = 1.5$（策略变化较大）：
- 无裁剪项: $1.5 \times 0.375 = 0.5625$
- 裁剪项: $\text{clip}(1.5, 0.8, 1.272) \times 0.375 = 1.272 \times 0.375 = 0.477$
- 取 min = 0.477（触发上界裁剪，限制过大更新）

同时 TIS cap 生效：如果 vLLM 与训练引擎的比率超过 $\rho = 2.0$，则被截断为 2.0。

注意：如果 8 个回答全部正确（$\text{std} = 0$），则 zero gradient filtering 会丢弃这个组——因为所有 advantage 为 0，不提供梯度信号。Active sampling 会自动补充新样本填满 batch。

###### 伪代码

```python
# OlmoRL Training Loop (simplified)
def olmo_rl_step(policy, vllm_engine, prompts, verifiers, config):
    """One step of OlmoRL training with inflight updates."""
    # config: G=8, eps_low=0.2, eps_high=0.272, rho=2.0, lr=2e-6
    
    # Step 1: Generate rollouts (75% of wall-clock time for 32B)
    all_responses = []
    for prompt in prompts:  # 128 unique prompts per batch (32B)
        responses = vllm_engine.generate(
            prompt, n=config.G,  # G=8 responses per prompt
            max_tokens=32768, temperature=1.0, top_p=1.0
        )
        all_responses.append(responses)
    
    # Step 2: Compute rewards via domain-specific verifiers
    rewards = []
    for prompt, responses in zip(prompts, all_responses):
        domain = get_domain(prompt)  # math/code/IF/chat
        r = verifiers[domain].score(prompt, responses)  # returns list of G scores
        rewards.append(r)
    
    # Step 3: Zero gradient filtering + active sampling
    filtered = []
    for prompt, responses, r in zip(prompts, all_responses, rewards):
        if torch.std(torch.tensor(r)) > 0:  # skip all-same-reward groups
            filtered.append((prompt, responses, r))
    # Active sampling: refill batch to maintain consistent size
    while len(filtered) < config.batch_size:
        new_prompt = sample_new_prompt()
        new_responses = vllm_engine.generate(new_prompt, n=config.G, ...)
        new_r = verifiers[get_domain(new_prompt)].score(new_prompt, new_responses)
        if torch.std(torch.tensor(new_r)) > 0:
            filtered.append((new_prompt, new_responses, new_r))
    
    # Step 4: Compute advantages (no std normalization, per Dr GRPO)
    for prompt, responses, r in filtered:
        mean_r = sum(r) / len(r)
        advantages = [ri - mean_r for ri in r]  # NOT divided by std
    
    # Step 5: Policy gradient with token-level loss
    total_tokens = sum(len(y) for _, responses, _ in filtered for y in responses)
    loss = 0.0
    for prompt, responses, advantages_group in filtered:
        for y, A in zip(responses, advantages_group):
            for t in range(len(y)):
                # Importance ratio
                r_t = policy.log_prob(y[t] | prompt, y[:t]) - old_policy.log_prob(y[t] | ...)
                r_t = torch.exp(r_t)
                # Truncated importance sampling
                tis = min(policy.log_prob(y[t]) / vllm_log_prob(y[t]), config.rho)
                # Clipped surrogate objective (asymmetric)
                unclipped = r_t * A
                clipped = torch.clamp(r_t, 1-config.eps_low, 1+config.eps_high) * A
                loss += tis * torch.min(unclipped, clipped)
    
    loss = loss / total_tokens  # token-level normalization
    loss.backward()
    optimizer.step()  # No KL penalty term
    
    # Step 6: Inflight update — update vllm weights without waiting for full epoch
    vllm_engine.update_weights(policy)  # Key: 4x speedup
```

###### 超参数表

**Table 33: 模型架构**

| 参数 | 7B | 32B |
|---|---|---|
| 层数 | 32 | 64 |
| 隐藏维度 (d_model) | 4096 | 5120 |
| Q 头数 | 32 | 40 |
| KV 头数 | 32 | 8 |
| 激活函数 | SwiGLU | SwiGLU |
| QKV 归一化 | QK-Norm | QK-Norm |
| 层归一化 | RMSNorm (on outputs) | RMSNorm (on outputs) |
| 梯度裁剪 | 1.0 | 1.0 |
| Z-loss 权重 | 10^-5 | 10^-5 |
| 滑动窗口注意力 | 3/4 层; 4096 tokens | 3/4 层; 4096 tokens |
| RoPE theta | 500,000 | 500,000 |
| RoPE 扩展 | YaRN (仅 full attention 层) | YaRN (仅 full attention 层) |

**Table 35: 基座模型训练超参数**

| 参数 | 7B 预训练 | 7B Midtrain | 7B LC | 32B 预训练 | 32B Midtrain | 32B LC |
|---|---|---|---|---|---|---|
| LR 调度 | Modified cosine | Linear decay | Linear decay | Cosine trunc@5.5T | Linear decay | Linear decay |
| LR warmup | 2000 steps | 0 steps | 200 steps | 2000 steps | 0 steps | 200 steps |
| Peak LR | 3.0e-4 | 2.074e-4 | 2.074e-4 | 6.0e-4 | 2.071e-4 | 2.071e-4 |
| Final LR | 3.0e-5 | 0 | 0 | 6.0e-5 | 0 | 0 |
| Batch size (instances) | 512 | 256 | 64 | 1024 | 512 | 128 |
| Sequence length | 8192 | 8192 | 65536 | 8192 | 8192 | 65536 |
| Total tokens | 5.93T | 100B | 50B | 5.5T | 100B (x2) | 100B |

**Table 47: SFT 超参数**

| 参数 | 7B Think SFT | 32B Think SFT | 7B Instruct SFT |
|---|---|---|---|
| Total Tokens | 45.4B | 45.2B | 3.4M |
| Learning Rate | 5.0e-5 | 1.0e-4 souped with 5.0e-5 | 8.0e-5 |
| Num. GPUs | 64 | 256 | 8-64 |
| Max Sequence Length | 32K | 32K | 32K |

**Table 48: DPO 超参数**

| 参数 | 7B Think DPO | 32B Think DPO | 7B Instruct DPO |
|---|---|---|---|
| Num. Preference Pairs | 150K | 200K | 260K |
| Epochs | 1 | 1 | 1 |
| DPO beta | 5 | 5 | 5 |
| Learning Rate | 8.0e-8 | 7.0e-8 | 1.0e-6 |
| LR Schedule | Linear decay | Linear decay | Linear decay |
| Warmup Ratio | 0.1 | 0.1 | 0.1 |
| Batch Size | 128 | 128 | 128 |
| Max Seq Length | 16K | 8K | 16K |

**Table 49: RL 超参数**

| 参数 | 7B Think RL | 32B Think RL | 7B Instruct RL | 7B RL-Zero |
|---|---|---|---|---|
| Dataset size | 104,869 | 104,869 | 171,950 | 13,314 |
| Learning rate | 1.0e-6 | 2.0e-6 | 1.0e-6 | 1.0e-6 |
| LR schedule | constant | constant | constant | constant |
| Training steps | 1,400 | 750 | 450 | 2,000 |
| Max prompt length | 2,048 | 2,048 | 2,048 | 2,048 |
| Response length | 32,768 | 32,768 | 8,192 | 16,384 |
| Unique prompts/batch | 64 | 128 | 64 | 32 |
| Group size | 8 | 8 | 8 | 8 |
| Clip-lower (ε_low) | 0.2 | 0.2 | 0.2 | 0.2 |
| Clip-higher (ε_high) | 0.272 | 0.272 | 0.272 | 0.272 |
| Num learner GPUs | 16 | 64 | 8 | 8 |
| Num actor GPUs | 56 | 160 | 56 | 64 |

**Table 23: OlmoRL 基础设施改进**

| 配置 | Total tokens (Mtok) | Tokens/sec | MFU (%) | MBU (%) |
|---|---|---|---|---|
| OLMo 2 (baseline) | 6.34 | 881 | 0.30 | 12.90 |
| + continuous batching | 7.02 | 975 | 0.33 | 14.29 |
| + better threading | 9.77 | 1358 | 0.46 | 19.89 |
| + inflight updates (OLMo 3) | 21.23 | 2949 | 1.01 | 43.21 |

**训练成本与时间线**

| 项目 | 耗时 | 硬件 |
|---|---|---|
| 总计 (OLMo 3 Think 32B) | ~56 天 | 1024x H100 |
| 预训练 | ~47 天 | 512→1024 GPUs |
| Midtraining | ~1.5 天 | 2x512 GPUs |
| LC extension | ~1 天 | 1024 GPUs |
| 后训练 (SFT+DPO+RL) | ~9 天 | 64-256 GPUs |
| OLMo 3.1 延长 RL | +21 天 | 224 GPUs |
| 估计成本 ($2/H100-hr) | ~$2.75M | — |

##### 设计决策

###### 决策 1: 滑动窗口注意力 on 3/4 层 + 最后层全注意力

**替代方案：** 所有层都用全注意力（full attention everywhere），如 Llama 3、Qwen 2.5 等多数模型采用的方式。

**论文是否做了对比？** Section 3.2 引用了 Bertsch et al. (2026) 的相关工作。虽然未直接在论文中给出消融实验对比表，但从架构设计角度来看，这是一个从 OLMo 2 延续并改进的设计。OLMo 3 在长上下文扩展阶段的 RULER 性能达到与 Qwen 2.5 32B、Mistral Small 3.1 24B 和 Gemma 3 27B 可比的水平（Table 12），证明了此设计在长上下文场景中的有效性。

**核心 trade-off：** 计算效率 vs 全局信息交互。滑动窗口注意力将大部分层的复杂度从 $O(n^2)$ 降低到 $O(n \times w)$（$w = 4096$），大幅降低了长序列的推理和训练成本。保留最后层（1/4）的全注意力确保模型在输出层仍能看到完整上下文。

**为什么本文选择优于替代方案：** 在 65K 序列长度下，全注意力的计算量是滑动窗口的约 16 倍（65536/4096），3/4 层用滑动窗口意味着约 75% 的注意力计算被压缩，使得在合理的 GPU 预算内完成 5.93T token 的预训练变得可行。

###### 决策 2: Delta Learning 取代传统 LLM-judge DPO 管线

**替代方案：** UltraFeedback 风格的 LLM-as-judge 管线——对同一模型的多个回答用强 LLM 打分，取最高分和最低分配对。

**论文是否做了对比？** 是。Table 21 直接对比了三种方式在 7B dev 模型上的效果：
- Dev 7B SFT checkpoint baseline: avg 70.3
- Continued SFT on Qwen3 32B chosen: avg 64.5（反而下降 5.8）
- Delta learning (Qwen3 32B chosen + Qwen3 0.6B rejected): avg 72.9（提升 2.6）

Delta learning vs Continued SFT: avg +8.4, AIME 2025 +13.5, LiveCodeBench +17.5。这些数字清楚表明：当 SFT 已饱和时，相同数据在 DPO 框架下仍能提取有效信号。

此外，Section 5.5 的 Instruct DPO 消融实验（Table 32）还发现：结合 delta-learning pairs 和 GPT-judge pairs 效果互补，不同偏好信号的组合优于单一来源。

**核心 trade-off：** Delta learning 不需要对同一模型做多次采样后让 judge 打分（省去 judge 模型推理成本），但依赖于能找到能力差距明确的模型对（Qwen 3 32B vs Qwen 3 0.6B）。如果没有合适的弱模型，该方法无法直接应用。

**为什么本文选择优于替代方案：** 在思维模型领域，可用的开放思维模型非常少，LLM-judge 管线的多样性受限。而 delta learning 利用 Qwen 3 32B（强）和 Qwen 3 0.6B（弱）这一自然存在的能力差距，无需额外的 judge 模型即可生成高质量对比对。更关键的是，Continued SFT 在 chosen 数据上反而下降，说明模型在 SFT 维度上已接近能力边界，DPO 的对比学习机制能利用相同数据中 SFT 无法利用的信息。

###### 决策 3: 去除 GRPO 的 KL 损失和标准差归一化

**替代方案：** 保留 KL 散度惩罚项（限制策略偏离参考模型），保留 advantage 的标准差归一化（如原始 GRPO）。

**论文是否做了对比？** Section 4.4.1 引用了 GLM-4.5 Team et al. (2025)、DAPO (Yu et al., 2025) 和 Dr GRPO (Liu et al., 2025b) 的结论，表明去除 KL 不会导致过优化或训练不稳定。关于标准差归一化，论文引用 Dr GRPO 解释了 difficulty bias 的具体机制。虽然未在本论文中给出专门的消融表，但 Table 22 显示 SFT+DPO+RLVR 组合在所有指标上均优于 SFT+RLVR（avg 74.1 vs 71.9），间接验证了 OlmoRL 配方的有效性。Table 24 显示 RL 阶段的 IFEval 从 80.6 提升到 93.8（+13.2），AIME 2025 从 70.7 到 78.1（+7.4），证实了长时间稳定 RL 训练的可行性。

**核心 trade-off：** 去除 KL 允许策略做更大幅度的更新，理论上可能导致 reward hacking。但论文发现多领域混合训练本身就是一种正则化——mixing data yields lower train reward but not lower downstream performance（Section 4.5），混合训练降低了单领域 reward hacking 的风险。不做 std 归一化的代价是对不同难度的题不再"一视同仁"（简单题的正确回答获得与难题正确回答相同大小的 advantage），但好处是消除了 difficulty bias 导致的极端 advantage 放大。

**为什么本文选择优于替代方案：** 思维模型的 RL 训练需要非常长的 run（750-1400 步，生成长度达 32K token），任何限制策略更新幅度的机制（KL 惩罚）都会减慢学习速度。同时 difficulty bias 在数学推理领域尤其严重（竞赛题和基础题的难度差距极大），std 归一化会让几乎全对或全错的题目获得异常高的 advantage。OLMo 3 的选择让训练更快更稳，配合 zero gradient filtering 和 active sampling 消除了无梯度信号的浪费。

###### 决策 4: 从 Think SFT 检查点 warm-start Instruct 训练

**替代方案：** 直接从 base 模型训练 Instruct（跳过 Think SFT 阶段），或完全独立训练 Instruct 和 Think 两条线。

**论文是否做了对比？** 是。Table 29 直接对比了 7B Instruct 模型：
- 无 Think SFT warm-start: avg 44.5
- 有 Think SFT warm-start: avg 47.8（+3.3）

具体指标：MATH 60.3→65.9（+5.6），GSM8K 87.6→91.1（+3.5），GPQA 29.7→34.4（+4.7），IFEval 81.0→84.7（+3.7）。所有指标一致提升，且最终 Instruct 模型不会在响应中生成思维链标记。

**核心 trade-off：** 使用 Think SFT 作为起点意味着 Instruct 和 Think 共享初期训练投入（节省计算），但风险是 Think 的思维链模式可能残留在 Instruct 模型中导致不必要的冗长输出。

**为什么本文选择优于替代方案：** Think SFT 阶段学到的推理能力"内化"在模型权重中，即使后续 Instruct SFT 训练移除了显式思维链格式，内部推理能力仍然保留。+3.3 avg 的提升是"免费"的——因为 Think SFT 检查点本身就是 Think pipeline 的中间产物。

###### 决策 5: Midtraining 数据去污染覆盖所有 benchmark splits（含 train split）

**替代方案：** 仅对 test split 去污染（常规做法）。

**论文是否做了对比？** Section 3.5.3 和 Figure 12 展示了去污染对性能的影响。关键发现是部分常用 benchmark 使用 train split 进行评估（为了降低噪声），如果 midtraining 数据包含 train split 的内容，即使 test split "干净"也会导致评估结果虚高。

**核心 trade-off：** 更激进的去污染会丢弃更多训练数据，但确保了评估结果的可信度。

**为什么本文选择优于替代方案：** 作为完全开放模型，OLMo 3 的核心价值在于可复现性和评估公正性。如果评估结果因数据泄露而不可信，整个 fully-open 的意义就大打折扣。

###### 决策 6: 在 midtraining 数据中排除 special tokens（chat template 标记）

**替代方案：** 在 midtraining 数据中包含 chat template 的 special tokens，让模型提前学会对话格式。

**论文是否做了对比？** Section 3.5.4 明确报告：在 midtraining 中加入 special tokens 会导致 base 模型在推理时自发输出这些标记，破坏评估流程。具体影响：GSM8K 分数直接降到 0——因为模型的回答中混入了 `<|assistant|>` 等标记，导致 exact match 失败。

**核心 trade-off：** 不含 special tokens 意味着 midtraining 阶段无法让模型学习对话格式，但 SFT 阶段会完成这一学习。

**为什么本文选择优于替代方案：** 把格式学习推迟到 SFT 阶段是更安全的选择——midtraining 阶段的核心目标是提升数学/代码/推理能力，而非学习对话格式。混入 special tokens 不仅破坏 base model 评估，还可能在 SFT 时造成冲突（base 模型已经学了一种格式，SFT 又要教另一种）。

##### 易混淆点

**1. Delta Learning vs 普通 DPO 数据构造**

- ❌ 错误理解：Delta Learning 就是用同一个模型生成多个回答，然后选最好和最差的配对（即 on-policy rejection sampling）
- ✅ 正确理解：Delta Learning 是用两个 **不同能力级别的模型** 生成回答——Qwen 3 32B（强模型）作为 chosen，Qwen 3 0.6B（弱模型）作为 rejected。关键不是"同一模型的好坏回答"，而是"强弱模型之间的能力差距（capability gap）"。Table 21 证明直接在强模型数据上做 SFT 反而掉点（avg 64.5 vs baseline 70.3），但 DPO 框架能利用同样的 chosen 数据获得提升（avg 72.9）。

**2. OlmoRL 中的 inflight updates vs 传统 batch 更新**

- ❌ 错误理解：Inflight updates 是一种新的梯度计算方法或优化算法
- ✅ 正确理解：Inflight updates 是一个 **工程优化**——在 RL 训练中，不等所有 group 的 rollout 都生成完毕再更新权重，而是当部分 rollout 完成后就立即用它们更新 policy 网络，然后将新权重同步到推理引擎继续生成。这解决了长序列（32K token）生成时严重的 GPU idle 问题——生成长度方差很大（有的 2K 就结束，有的要 32K），传统方式需要等最慢的那个完成。Table 23 显示此优化将吞吐从 1358 tokens/sec 提升到 2949 tokens/sec（+2.17x），加上 continuous batching 总计 4x 加速。

**3. Midtraining 中的思维链数据 vs Think SFT 数据**

- ❌ 错误理解：Midtraining 阶段的思维链数据和 Think SFT 阶段的思维链数据是同一套数据，只是阶段不同
- ✅ 正确理解：两者在数据来源、格式和目的上都不同。Midtraining 的思维链数据（如 QWQ Reasoning Traces 1.87B, Math/Code Meta-Reasoning, General Reasoning Mix 等）**不含** chat template special tokens，目的是让 base 模型内化推理模式（Table 10 显示 Math +5.6 提升）。Think SFT 数据（Dolci Think SFT, 45.2B tokens）包含完整的 `<think>...</think>` 格式化思维链，目的是教模型显式地生成结构化推理输出。前者是"打地基"，后者是"建框架"。

**4. 完全开放 (fully-open) vs 开源权重 (open-weight)**

- ❌ 错误理解：Fully-open 和 open-weight 的区别只是许可证不同，模型本身性能差异是因为模型能力不同
- ✅ 正确理解：Fully-open 要求公开**全部** model flow——包括预训练数据、midtraining 数据、后训练数据、所有中间检查点和训练代码。这不仅是开放程度的差异，更直接限制了可用的训练数据：OLMo 3 必须确保所有数据来源的许可证允许公开发布，且必须对所有 benchmark splits 做去污染。而 open-weight 模型（如 Qwen 3）可以使用任意数据（包括可能包含 benchmark 数据的来源）且不必披露。OLMo 3 在这些约束下仍逼近 Qwen 3 的性能（MATH 96.2 vs 95.4），且使用了 6x 更少的 token，说明其方法论的高效性。
#### 实验与归因 (Experiments & Attribution)

##### 对比表格

**表1: OLMo 3.1 Think 32B vs 开放权重与全开放模型（后训练评估）**

| Benchmark | OLMo 3.1 32B Think | OLMo 2 Instruct 32B | Apertus Instruct 70B | LLM360 K2-V2 Instruct 70B | Qwen 3 32B | Qwen 3 VL 32B Think | Qwen 2.5 32B | Gemma 3 27B | Gemma 2 27B | DS-R1 32B |
|---|---|---|---|---|---|---|---|---|---|---|
| MATH | 96.2 | 49.2 | 36.2 | 94.5 | 95.4 | 96.7 | 80.2 | 87.4 | 51.5 | 92.6 |
| AIME 2024 | 80.6 | 4.6 | 0.3 | 78.4 | 80.8 | 86.3 | 15.7 | 28.9 | 4.7 | 70.3 |
| AIME 2025 | 78.1 | 0.9 | 0.1 | 70.3 | 70.9 | 78.8 | 13.4 | 22.9 | 0.9 | 56.3 |
| OMEGA | 53.4 | 9.8 | 5.6 | 46.1 | 47.7 | 50.8 | 19.2 | 24.0 | 9.1 | 38.9 |
| BigBenchHard | 88.6 | 65.6 | 57.0 | 87.6 | 90.6 | 91.1 | 80.9 | 82.4 | 66.0 | 89.7 |
| ZebraLogic | 80.1 | 13.3 | 9.0 | 79.2 | 88.3 | 96.1 | 24.1 | 24.8 | 17.2 | 69.4 |
| AGI Eval English | 89.2 | 68.4 | 61.7 | 89.6 | 90.0 | 92.2 | 78.9 | 76.9 | 70.9 | 88.1 |
| HumanEvalPlus | 91.5 | 44.4 | 42.9 | 88.0 | 91.2 | 90.6 | 82.6 | 79.2 | 67.5 | 92.3 |
| MBPP+ | 68.3 | 49.0 | 45.8 | 66.0 | 70.6 | 66.2 | 66.6 | 65.7 | 61.2 | 70.1 |
| LiveCodeBench v3 | 83.3 | 10.6 | 9.7 | 78.4 | 90.2 | 84.8 | 49.9 | 39.0 | 28.7 | 79.5 |
| IFEval | 93.8 | 85.8 | 70.4 | 68.7 | 86.5 | 85.5 | 81.9 | 85.4 | 62.1 | 78.7 |
| IFBench | 68.1 | 36.4 | 26.0 | 46.3 | 37.3 | 55.1 | 36.7 | 31.3 | 27.8 | 23.8 |
| MMLU | 86.4 | 77.1 | 70.2 | 88.4 | 88.8 | 90.1 | 84.6 | 74.6 | 76.1 | 88.0 |
| PopQA | 30.9 | 37.2 | 33.6 | 32.2 | 30.7 | 32.2 | 28.0 | 30.2 | 30.4 | 26.7 |
| GPQA | 57.5 | 36.4 | 27.9 | 64.0 | 67.3 | 67.4 | 44.6 | 45.0 | 39.9 | 61.8 |
| AlpacaEval 2 LC | 69.1 | 38.0 | 19.9 | - | 75.6 | 80.9 | 81.9 | 65.5 | 39.8 | 26.2 |

OLMo 3.1 Think 32B 在全开放模型中全面领先，尤其在 AIME 2025（78.1）和 IFBench（68.1）上大幅超越所有全开放竞品。与最强开放权重模型 Qwen 3 VL 32B Think 相比，仅在 ZebraLogic（80.1 vs 96.1）和 GPQA（57.5 vs 67.4）上有明显差距，且训练 token 量仅为 Qwen 3 的约 1/6。

**表14: OLMo 3 Think 32B 各训练阶段与基线对比**

| Benchmark | SFT | DPO | Final Think 3.0 | Final Think 3.1 | Qwen 3 32B | Qwen 3 VL 32B Think | DS-R1 32B | K2-V2 70B Instruct |
|---|---|---|---|---|---|---|---|---|
| MATH | 95.6 | 95.9 | 96.1 | 96.2 | 95.4 | 96.7 | 92.6 | 94.5 |
| AIME 2024 | 73.5 | 76.0 | 76.8 | 80.6 | 80.8 | 86.3 | 70.3 | 78.4 |
| AIME 2025 | 66.2 | 70.7 | 72.5 | 78.1 | 70.9 | 78.8 | 56.3 | 70.3 |
| OMEGA | 43.1 | 45.2 | 50.6 | 53.4 | 47.7 | 50.8 | 38.9 | 46.1 |
| BigBenchHard | 88.8 | 89.1 | 89.8 | 88.6 | 90.6 | 91.1 | 89.7 | 87.6 |
| ZebraLogic | 70.5 | 74.5 | 76.0 | 80.1 | 88.3 | 96.1 | 69.4 | 79.2 |
| AGI Eval English | 85.9 | 87.8 | 88.2 | 88.8 | 90.0 | 92.2 | 88.1 | 89.6 |
| HumanEvalPlus | 90.0 | 91.6 | 91.4 | 91.5 | 91.2 | 90.6 | 92.3 | 88.0 |
| MBPP+ | 66.7 | 67.2 | 68.0 | 68.3 | 70.6 | 66.2 | 70.1 | 66.0 |
| LiveCodeBench v3 | 75.8 | 81.9 | 83.5 | 83.3 | 90.2 | 84.8 | 79.5 | 78.4 |
| IFEval | 83.9 | 80.6 | 89.0 | 93.8 | 86.5 | 85.5 | 78.7 | 68.7 |
| IFBench | 37.0 | 34.4 | 47.6 | 68.1 | 37.3 | 55.1 | 23.8 | 46.3 |
| MMLU | 85.3 | 85.2 | 85.4 | 86.4 | 88.8 | 90.1 | 88.0 | 88.4 |
| PopQA | 33.1 | 37.0 | 31.9 | 30.9 | 30.7 | 32.2 | 26.7 | 32.2 |
| GPQA | 55.7 | 57.6 | 58.1 | 56.7 | 67.3 | 67.4 | 61.8 | 64.0 |
| AlpacaEval 2 LC | 69.1 | 78.6 | 74.2 | 69.1 | 75.6 | 80.9 | 26.2 | - |
| Safety | 64.8 | 65.3 | 68.8 | 83.6 | 69.0 | 82.7 | 63.6 | 88.5 |

从 SFT 到 Final Think 3.1 的渐进式提升清晰可见：AIME 2025 从 66.2 到 78.1（+11.9），IFEval 从 83.9 到 93.8（+9.9），IFBench 从 37.0 到 68.1（+31.1）。RL 阶段的延长训练（3.0 到 3.1）主要提升了 IF 能力和 Safety。

**表25: OLMo 3.1 32B Instruct 各阶段与基线对比**

| Benchmark | SFT | DPO | Final Instruct 3.1 | Apertus 70B | Qwen 3 32B NoThink | Qwen 3 VL 32B Inst | Qwen 2.5 32B | Gemma 3 27B | Gemma 2 27B | OLMo 2 32B |
|---|---|---|---|---|---|---|---|---|---|---|
| MATH | 74.4 | 86.6 | 93.4 | 36.2 | 84.3 | 95.1 | 80.2 | 87.4 | 51.5 | 49.2 |
| AIME 2025 | 8.2 | 23.3 | 57.9 | 0.1 | 21.3 | 64.2 | 13.4 | 22.9 | 0.9 | 0.9 |
| HumanEvalPlus | 80.8 | 85.7 | 86.7 | 42.9 | 83.9 | 89.3 | 82.6 | 79.2 | 67.5 | 44.4 |
| IFEval | 87.7 | 87.3 | 88.8 | 70.4 | 87.5 | 88.1 | 81.9 | 85.4 | 62.1 | 85.8 |
| IFBench | 29.7 | 36.3 | 39.7 | 26.0 | 31.3 | 37.2 | 36.7 | 31.3 | 27.8 | 36.4 |
| MMLU | 79.0 | 81.9 | 80.9 | 70.2 | 85.8 | 88.7 | 84.6 | 74.6 | 76.1 | 77.1 |
| AlpacaEval 2 LC | 42.2 | 69.7 | 59.8 | 19.9 | 67.9 | 84.3 | 81.9 | 65.5 | 39.8 | 38.0 |

Instruct 模型最大亮点在于 AIME 2025 从 SFT 的 8.2 飙升至最终的 57.9（+49.7），表明 DPO+RL 流水线对非 thinking 模型的推理能力也有极大提升。但在 MMLU 上 Instruct（80.9）仍然落后于 Qwen 3 NoThink（85.8），且 AlpacaEval 2 LC 从 DPO 的 69.7 回落至最终的 59.8，暗示 RL 阶段可能对聊天风格有负面影响。

**表15: OLMo 3 Think 7B 与基线对比**

| Benchmark | SFT | DPO | Final Think | OpenThinker3 7B | Nemotron Nano 9B v2 | DS-R1 Qwen 7B | Qwen 3 8B | Qwen 3 VL 8B Think | OR Nemotron 7B |
|---|---|---|---|---|---|---|---|---|---|
| MATH | 94.4 | 92.4 | 95.1 | 94.5 | 94.4 | 87.9 | 95.1 | 95.2 | 94.6 |
| AIME 2024 | 69.6 | 74.6 | 71.6 | 67.7 | 72.1 | 54.9 | 74.0 | 70.9 | 77.0 |
| AIME 2025 | 57.6 | 62.7 | 64.6 | 57.2 | 58.9 | 40.2 | 67.8 | 61.5 | 73.1 |
| OMEGA | 37.8 | 40.5 | 45.0 | 38.4 | 42.4 | 28.5 | 43.4 | 38.1 | 43.2 |
| BigBenchHard | 84.1 | 83.7 | 86.6 | 77.1 | 86.2 | 73.5 | 84.4 | 86.8 | 81.3 |
| ZebraLogic | 57.9 | 60.6 | 66.5 | 34.9 | 60.8 | 26.1 | 85.2 | 91.2 | 22.4 |
| AGI Eval English | 77.2 | 79.1 | 81.5 | 78.6 | 83.1 | 69.5 | 87.0 | 90.1 | 81.4 |
| HumanEvalPlus | 88.2 | 91.4 | 89.9 | 87.4 | 89.7 | 83.0 | 80.2 | 83.7 | 89.7 |
| MBPP+ | 63.2 | 63.0 | 64.7 | 61.4 | 66.1 | 63.5 | 69.1 | 63.0 | 61.2 |
| LiveCodeBench v3 | 67.8 | 75.1 | 75.2 | 68.0 | 83.4 | 58.8 | 86.2 | 85.5 | 82.3 |
| IFEval | 77.9 | 75.9 | 88.2 | 51.7 | 86.0 | 59.6 | 87.4 | 85.5 | 42.5 |
| IFBench | 30.0 | 28.3 | 41.6 | 23.0 | 34.6 | 16.7 | 37.1 | 40.4 | 23.4 |
| MMLU | 74.9 | 74.8 | 77.8 | 77.4 | 84.3 | 67.9 | 85.4 | 86.5 | 80.7 |
| PopQA | 20.8 | 24.7 | 23.7 | 18.0 | 17.9 | 12.8 | 24.3 | 29.3 | 14.5 |
| GPQA | 45.8 | 48.6 | 46.2 | 47.6 | 56.2 | 54.4 | 57.7 | 61.5 | 56.6 |
| AlpacaEval 2 LC | 43.9 | 50.6 | 52.1 | 24.0 | 58.0 | 7.7 | 60.5 | 73.5 | 8.6 |

7B 规模下 OLMo 3 Think 在 IFEval（88.2）和 IFBench（41.6）上领先同量级全部 baseline，但在 LiveCodeBench（75.2 vs Qwen 3 8B 的 86.2）、ZebraLogic（66.5 vs Qwen 3 VL 8B 的 91.2）和 GPQA（46.2 vs Qwen 3 VL 8B 的 61.5）上差距显著，说明 7B 规模的推理天花板仍受知识容量限制。

##### 归因排序

按消融实验中的 delta 大小排序，从高到低列出各组件的贡献：

1. **Delta Learning DPO vs 继续 SFT** (+8.4 Avg, +17.5 LiveCodeBench, +13.5 AIME 2025, Table 21): 使用强模型（Qwen3 32B）vs 弱模型（Qwen3 0.6B）的能力差对构造偏好对，比直接在同样的 chosen 数据上继续 SFT 效果好得多。原因是 SFT 的 chosen 数据已弱于模型已见过的训练数据，无法提供有效的模仿目标，但偏好对比信号仍然有效。

2. **DPO 作为 RL 起点 vs 纯 SFT 起点** (+2.2 Avg overall, SFT+DPO+RLVR 74.1 vs SFT+RLVR 71.9, Table 22): DPO 阶段为 RL 提供了更好的初始化——GPQA 从 42.7 提升至 50.2（+7.5），AIME 2025 从 62.4 提升至 64.2。DPO 在 RL 之前先建立偏好结构，使后续策略优化更高效。

3. **Midtraining 迭代优化**（+3.4 Avg, +9.7 Math, +4.3 Code, Round 5 vs Round 1, Table 6）: 五轮迭代的混合配方逐步加入去污染、新数据源和更好的质量过滤，数学从 47.4 提升至 57.1。候选数据质量随迭代改善，且第5轮加入了去污染流程，意味着实际增益可能被低估。

4. **从 Think SFT 热启动 Instruct 模型**（+3.3 Avg, Table 29）: 在 Instruct 训练前先经过 Think SFT 阶段，MATH 从 60.3 提升至 65.9（+5.6），GPQA 从 29.7 提升至 34.4（+4.7），IFEval 从 81.0 提升至 84.7。Think SFT 建立的推理结构对后续非 thinking 模型同样有益，且不会显著增加响应长度。

5. **OlmoRL 基础设施优化**（3.3x 吞吐量提升, 881 -> 2949 tokens/sec, Table 23）: Continuous batching + inflight updates 将 RL 训练从 15 天缩短至 6 天（7B Think），节省了 54% 的潜在计算浪费。这不是模型精度提升，但使更长的 RL 运行在有限集群资源下成为可能。

6. **Thinking traces 和指令数据加入 midtraining**（+1.9 Avg, +5.6 Math, +1.1 Code, Table 10）: 在预训练阶段就加入推理链和指令数据，即使模型尚未经过后训练也能提升各项基础能力。数学提升最显著，表明推理链为基础模型提供了有效的结构化推理示范。

##### 可信度检查

**1. 去污染 (Decontamination)**

论文投入了大量精力进行去污染，使用专门开发的 `decon` 工具对 midtraining 数据的所有 benchmark splits（包括 train split）进行去污染。实验表明（Figure 12），部分 benchmark（如 DROP、Minerva、SQuAD）在去污染后确实出现性能下降，证明去污染有效。但值得注意的是：(1) 预训练的 5.93T 数据并未进行系统去污染，仅 midtraining 的 100B 数据做了去污染；(2) 来自 Flan、Nemotron 等已有数据集中的模板化污染非常普遍，说明开源生态整体的去污染水平存疑；(3) 部分 benchmark 即使存在污染也没有表现出性能膨胀（如 DeepSeek LeetCode 接近 0），而 GSM8K 甚至在去污染后性能更好——作者对此现象也无法完全解释。

**2. Baseline 公平性**

论文在所有模型上使用统一的评估框架（OLMES），参数一致（temp=0.6, top-p=0.95, max_tokens=32768），这增加了可比性。但存在几个隐忧：(1) K2-V2-Instruct 在 AlpacaEval 上因输出格式导致 LLM judge 解析失败而缺失数据，说明统一评估框架对不同模型的兼容性有限；(2) Qwen 3 的 "NoThink" 模式并非为纯 Instruct 设计，在 Instruct 对比中可能不是最佳配置；(3) 论文对比的全开放模型（Apertus 70B、K2-V2 70B）参数量是 OLMo 3 的 2 倍以上，OLMo 3 仍能胜出令人印象深刻，但与同等规模全开放模型的直接对比不足（只有 OLMo 2 32B 和 Stanford Marin 32B）。

**3. 未报告的负面结果与局限**

论文罕见地披露了多项负面发现，但仍有值得关注的盲区：(1) GPQA 上 OLMo 3.1 Think 32B（57.5）大幅落后 Qwen 3（67.3），且 GPQA 被标记为"高方差"评估（std=1.4798），单次运行的可靠性存疑；(2) AlpacaEval 2 LC 在 DPO 阶段达到 78.6 后在 RL 阶段回落至 69.1（Final Think 3.1），暗示 RL 优化推理能力的同时可能损害聊天质量；(3) PopQA 上 OLMo 3.1 Think（30.9）低于 OLMo 2 Instruct（37.2），说明 thinking 训练可能以知识召回能力为代价；(4) 论文坦承"因计算资源限制在 2300 步停止"RL 训练，且"性能尚未完全饱和"，意味着报告的结果可能不是该方法的上限；(5) 32B Instruct 的 MMLU（80.9）低于 SFT 阶段的 DPO 后的 81.9，表明 RL 阶段在知识类任务上可能有轻微退化。

#### 专家批判 (Critical Review)

##### 隐性成本

1. **集群独占成本**：训练全程独占 1024 块 H100 GPU 长达 56 天，按 $2/H100-hour 计算总成本约 275 万美元。但这仅是 OLMo 3 Think 32B 一个模型的成本——OLMo 3.1 Think 32B 额外在 224 块 GPU 上继续 RL 训练 21 天，按同一费率至少再增加约 22.5 万美元，使旗舰模型总成本接近 300 万美元。

2. **RL 推理计算开销**：RL 阶段 75% 以上的时间用于等待 rollout 生成，32B 模型推理使用的计算资源是训练的 5 倍（8 个 H100 节点训练 vs 20 个节点推理）。即使经过 OlmoRL 4 倍加速优化，7B Think RL 仍需 6 天，32B Think RL 需约 5 天（且至少 1 天因稳定性问题损失）。若使用静态 batching 而非 continuous batching，在平均生成长度 14628 token、最大 32K token 的情况下，高达 54% 的计算将被浪费。

3. **超参搜索与评估的隐藏开支**：SFT 阶段同时在 4 组 256 GPU 上并行扫描学习率，持续 36 小时（合计约 36864 GPU-hours）；DPO 阶段每次全扫描需 64 GPU 运行 18 小时，实际因集群不稳定延续数天。论文明确指出评估消耗了 10-20% 的总计算预算，对于 $275 万的基准来说意味着额外 27.5-55 万美元仅用于评估。

4. **数据工程前置投入**：处理 2.38 亿份 PDF 经过 olmOCR 提取、质量过滤后保留 1.08 亿份文档（淘汰率 55%）；pretraining 数据从 9.31T 的候选池筛选至 5.93T 的最终 mix；midtraining 数据从 2.19T 池子筛至 100B。此外，去污染流程需对 midtraining 数据中所有 benchmark 的所有 splits 进行匹配检测。Swarm-based 数据配比搜索需训练 5 倍于域数量的代理模型（约 100+ 个 1B 模型 x 100B tokens），这些前置实验的 GPU 开销在报告的 $275 万中并未体现。

5. **合成数据生成成本**：midtraining 使用大量合成数据（CraneMath 5.62B tokens 由 Qwen3 生成、CraneCode 由 Qwen3 两阶段改写、QWQ 推理链 4.77B tokens 等），Think SFT 数据使用 QwQ-32B 和 GPT-4.1/o4-mini 生成推理链，DPO 的 GPT-judged 偏好对也需要调用闭源 API。这些合成数据的 API 调用成本和本地推理 GPU 成本均未被计入总开销。

##### 最值得复用的技术

1. **Delta Learning for DPO**：用强模型生成 chosen、弱模型生成 rejected 构建偏好对，替代传统 LLM-judge 流水线。实现成本极低——仅需修改偏好对构造逻辑（约 20-50 行代码），无需额外集群。核心思路是拿一个大模型和一个小模型分别对同一 prompt 生成回复，然后做 DPO。在 OLMo 3 实验中 delta learning 相比继续 SFT 带来 +8.4 平均分提升，且比 LLM-judge 流水线更稳定（Table 21）。适用于任何有现成强弱模型对的团队。

2. **OlmoRL 的 Continuous Batching + Inflight Updates**：将 RL 训练吞吐量从 881 tokens/sec 提升至 2949 tokens/sec（3.3 倍），节省 54% 的潜在计算浪费。实现成本中等——需要修改 RL 训练框架的推理调度逻辑，使 actor 异步工作并在训练步之间不暂停地更新权重。代码已开源（Open Instruct），可直接集成到基于 vLLM 的 RL 流水线中。对于任何做长序列 RLVR 的团队，预期可节省 2-3 倍训练时间。

##### 最大的坑

1. **特殊 token 泄露导致灾难性 eval 崩溃**：论文发现在 midtraining 数据中包含 chat template 的特殊 token 会导致基础模型在推理时自动输出这些 token，直接导致 GSM8K 等评估分数降至 0。这是一个极其隐蔽的陷阱——错误发生在 midtraining 数据准备阶段，但症状要到后训练评估时才暴露。规避方法：在所有 midtraining/pretraining 数据中严格过滤 `<|start|>`、`<|end|>` 等特殊 token，将其留给 SFT 阶段引入。

2. **单领域 RL 导致跨领域退化**：论文发现仅在数学领域做 RL 训练会伤害代码等其他领域的表现，反之亦然。表面看用混合领域数据做 RL 的 train reward 更低，但下游性能并不差——说明单领域 RL 的高 reward 可能是 reward hacking。规避方法：始终使用混合领域的 RL 训练集，并监控跨领域 benchmark 防止过拟合。OLMo 3 使用了约 10.5 万条混合 prompt，涵盖数学、代码、IF 和通用推理四个领域。

##### 关联技术

**1. Qwen 3 32B (Yang et al., 2025a)**

- **共同点**：同为 32B 规模的 thinking 模型，均使用 GRPO 变体做 RL 训练，均支持长上下文推理
- **差异**：Qwen 3 使用从最大模型的蒸馏策略，训练 token 量约为 OLMo 3 的 6 倍；OLMo 3 完全开放模型流（数据、代码、中间 checkpoint 全公开），Qwen 3 仅开放最终权重
- **Benchmark 对比**：在 AIME 2025 上 OLMo 3.1 Think 32B（78.1）vs Qwen 3 32B（70.9），OLMo 3 领先 +7.2；但在 LiveCodeBench v3 上 Qwen 3（90.2）大幅领先 OLMo 3（83.3）+6.9；ZebraLogic 上 Qwen 3（88.3）领先 OLMo 3（80.1）+8.2；GPQA 上 Qwen 3（67.3）领先 OLMo 3（57.5）+9.8
- **选择建议**：需要可审计训练数据和可干预模型流的研究场景选 OLMo 3；追求代码和逻辑推理极致性能的生产场景选 Qwen 3；有蒸馏/定制需求且需回溯数据来源时选 OLMo 3

**2. DeepSeek-R1-Distill-Qwen-32B (Guo et al., 2025)**

- **共同点**：均为开放权重的 32B 推理模型，均使用 RLVR 驱动推理能力
- **差异**：DS-R1 是从 DeepSeek-R1 671B 蒸馏至 Qwen-32B 底座，核心推理能力来自大模型蒸馏；OLMo 3 从自有 base model 出发，经 SFT+DPO+RL 完整流水线训练。DS-R1 未公开训练数据和流程
- **Benchmark 对比**：OLMo 3.1 Think 32B 在 AIME 2025（78.1 vs 56.3）、IFEval（93.8 vs 78.7）、IFBench（68.1 vs 23.8）上全面大幅领先 DS-R1。DS-R1 仅在 MBPP+（70.1 vs 68.3）和 HumanEvalPlus（92.3 vs 91.5）上小幅领先
- **选择建议**：DS-R1 的时代优势已被后来者抹平；在几乎所有任务上 OLMo 3 均优于 DS-R1，且 OLMo 3 提供完整开放性。仅在极端低延迟需求下 DS-R1 可能因更短思考链有优势

**3. Stanford Marin 32B (Hall et al., 2025) / Apertus 70B (Apertus Team, 2025)**

- **共同点**：均为全开放模型（公开数据、代码、中间 checkpoint），与 OLMo 3 处于同一"全开放"赛道
- **差异**：Marin 和 Apertus 的后训练流程不如 OLMo 3 成熟——OLMo 3 采用 SFT+DPO+RL 三阶段完整流水线，而 Marin/Apertus 主要依赖 SFT（+部分 DPO）。Apertus 虽有 70B 参数量（2 倍于 OLMo 3），仍全面落后
- **Benchmark 对比**：OLMo 3.1 Think 32B vs Apertus 70B：MATH 96.2 vs 36.2，AIME 2025 78.1 vs 0.1，HumanEvalPlus 91.5 vs 42.9——量级差异。OLMo 3 base 32B 在 base eval 上也超越 Marin 32B（Figure 1）
- **选择建议**：在全开放赛道中 OLMo 3 目前无可争议是最强选择。Marin/Apertus 的价值更多在于提供独立的训练配方和数据视角作为对照实验；如果研究者需要对比不同训练范式（如不同数据策略），可结合使用

**4. DAPO (Yu et al., 2025) / Dr GRPO (Liu et al., 2025b)**

- **共同点**：均为 GRPO 的改进变体，OLMo 3 的 OlmoRL 直接集成了两者的核心改进——DAPO 的 clip-higher（epsilon_high=0.272）和 zero-gradient filtering，Dr GRPO 的无标准差归一化 advantage
- **差异**：DAPO 和 Dr GRPO 是独立提出的算法改进，OlmoRL 将其统一整合并添加了 token-level loss、truncated importance sampling（TIS cap=2.0）和 active sampling 等工程优化
- **Benchmark 对比**：OlmoRL 的基础设施优化带来 3.3 倍吞吐量提升（Table 23），使 RL 运行稳定持续 750-2300 步成为可能。DS-R1 使用原版 GRPO 训练的 32B 蒸馏模型在 AIME 2025 上仅 56.3，而 OlmoRL 训练的 OLMo 3 达到 78.1
- **选择建议**：对于新的 RLVR 项目，建议直接采用 OlmoRL 框架（已开源），它整合了 DAPO/Dr GRPO 的理论改进和大量工程优化；单独使用 DAPO 或 Dr GRPO 的算法改进而不配套基础设施优化，效果会大打折扣
#### 机制迁移分析 (Mechanism Transfer Analysis)

##### 机制解耦表格

| 计算原语 | 本文用途 | 抽象描述 | 信息论直觉 |
|---|---|---|---|
| **群体代理搜索定向优化（Swarm-based Proxy Search）** | 在9T token池中，通过训练大量小型代理模型（proxy models）对24个WebOrganizer主题的混合比例进行联合优化（RegMix风格），生成最优的预训练数据配比Dolma 3 Mix | 在高维离散资源空间中，通过低成本代理评估器的群体采样来逼近全局最优配置。每个代理模型是一个从"配置→性能"映射的采样点，群体覆盖使得无需梯度即可在组合爆炸的配置空间中导航 | 用少量比特的代理信号（小模型评估结果）来压缩指数级配置空间的不确定性。核心trade-off是代理信号与真实目标之间的互信息：代理模型越能预测大模型行为，搜索效率越高。条件混合（conditional mixing）进一步利用已知配置的信息来约束后续搜索空间，实现信息的递增复用 |
| **分层课程注入（Staged Curriculum Injection）** | 预训练(5.9T)→中训练(100B)→长上下文扩展(50-100B)的三阶段数据课程。中训练阶段注入数学/代码/推理trace等高质量数据，使Math指标提升+9.7点（Table 6）。长上下文阶段用olmOCR学术PDF将上下文窗口从8K扩展至65K | 在序列式学习过程中，按照信息复杂度递增的顺序安排训练样本，后一阶段的数据分布是前一阶段的条件细化（conditional refinement）。每个阶段的数据量级递减（T→100B→50B），但信息密度递增 | 从信息瓶颈（Information Bottleneck）视角：早期阶段建立广泛的表征压缩，后期阶段用高信息密度样本定向扩展特定子空间的表征容量。数据量递减但互信息密度递增，确保梯度信号不被噪声淹没。这等价于对模型参数空间施加由粗到细的约束序列 |
| **能力差对比学习（Capability-Gap Contrastive Learning / Delta Learning）** | Think模型的DPO阶段使用Qwen3 32B生成chosen、Qwen3 0.6B生成rejected来构造偏好对，利用能力差距产生对比信号。相比在同样chosen数据上做continued SFT，Delta Learning在Avg上提升+8.4，AIME 2025上提升+13.5（Table 21） | 通过人为构造信号强度可控的正负样本对来驱动判别式学习。关键创新在于"对比信号"不依赖于同一模型的不同样本，而是来自能力水平已知且差距可量化的两个外部系统，使得对比梯度的方向和幅度均可预测 | 在信息几何视角下，DPO的梯度方向取决于chosen与rejected的对数概率差。当能力差距过小时，差值信号淹没在估计噪声中（低信噪比）；差距过大则梯度指向已饱和区域（信息冗余）。Delta Learning通过选择最优能力差（如32B vs 0.6B）来最大化DPO梯度的有效信息量，等价于选择最大化Fisher信息的对比分布 |
| **异步推理-训练流水线（Inflight Asynchronous RL Pipeline）** | OlmoRL通过continuous batching + inflight updates实现RL训练3.3x加速（881→2949 tokens/sec，Table 23）。核心是在vLLM actor生成rollout的同时，learner已在处理之前完成的rollout，两者异步并行 | 将"样本生成"和"参数更新"两个本质串行的阶段解耦为可重叠的流水线。通过容忍生成时使用略旧的策略参数（staleness），换取计算资源利用率的大幅提升。关键约束是staleness不能超过策略变化速率的阈值 | 经典的延迟-吞吐量trade-off：staleness引入的策略偏差（旧参数生成的样本对新策略的重要性权重偏离1）通过truncated importance sampling来控制上界（ρ=2.0）。这等价于在信息新鲜度（freshness）和处理吞吐量之间寻找Pareto最优。当策略更新步幅较小（clip ε ≈ 0.2-0.27）时，staleness的信息损失可忽略，流水线并行的吞吐增益则是数倍级 |
| **质量感知上采样（Quality-Aware Upsampling）** | 在预训练数据混合中，对每个WebOrganizer主题内的文档按质量分数进行非均匀上采样，替代DCLM的平坦质量过滤。在数据受限场景（如从1T池构建250B mix）下，相比flat filtering能保留更多样化的高质量数据 | 在有限资源预算下，用连续的质量权重函数（而非二值过滤阈值）来调控样本的重复概率。高质量样本被多次呈现，低质量样本以低概率出现但不被完全丢弃，从而在质量和多样性之间取得平衡 | 从KL散度最小化角度：目标是找到一个采样分布q(x)，使得在固定token预算T下，q与理想质量分布p*之间的KL散度最小，同时保持对原始分布p_0的支撑覆盖。平坦过滤等价于截断分布（将阈值以下概率置零），会丢失长尾信息；质量感知上采样则通过平滑的重加权保留了分布的完整支撑，以较小的信息损失换取显著的质量提升 |

##### 迁移处方

**原语1：群体代理搜索定向优化 → 推荐系统的多源特征配比优化**

- **目标领域+具体问题：** 大规模推荐系统（如电商、短视频）通常融合用户行为序列、物品属性、上下文特征、社交图谱等多种特征源。每种特征源对不同用户群体和场景的贡献率不同，当前主流做法是凭经验固定特征权重或用简单网格搜索，无法高效探索高维特征组合空间。
- **怎么接：** 替换现有推荐pipeline中的特征融合层（如DeepFM的feature interaction层或DCN的cross network权重）的超参搜索模块。将每种特征源类比为OLMo 3中的WebOrganizer主题类别，训练一批小规模代理推荐模型（如在1%用户采样上训练的轻量MLP），通过swarm搜索得到各特征源的最优混合权重，然后将该权重配置应用于全量模型训练。输入是多组特征源配比方案，输出是各方案在代理模型上的离线评估指标（AUC/NDCG）。
- **预期收益：** 参考OLMo 3通过swarm-based mixing在midtraining中实现Math +9.7、Code +4.3的提升（Table 6 Round5 vs Round1），推荐场景中多特征源的精细配比有望在核心指标上获得3-10%的相对提升。此外，条件混合策略可直接迁移到推荐系统频繁更新的场景——当新特征源上线时，无需从头搜索，只需在已有最优配置上做条件扩展。
- **风险/不适用条件：** 当特征源之间存在强非线性交互（如用户行为与实时上下文的交叉效应占主导）时，小规模代理模型可能无法捕捉这些交互，导致代理信号与全量模型的相关性下降。此外，推荐系统的数据分布快速漂移（如节假日效应）可能使搜索到的最优配比快速失效，需要引入时间衰减机制。

**原语2：分层课程注入 → 医疗AI的多阶段知识蒸馏**

- **目标领域+具体问题：** 医疗影像诊断模型（如胸部X光异常检测）需要同时掌握通用视觉特征、解剖结构知识和病变特异性模式。当前做法是ImageNet预训练→医疗域微调的两阶段训练，但中间缺少从"通用视觉"到"解剖结构"的过渡阶段，导致微调时需要大量标注数据才能弥补领域鸿沟。
- **怎么接：** 在现有两阶段pipeline中插入类似OLMo 3 midtraining的中间课程阶段。具体：(1) 预训练阶段在ImageNet等通用数据上训练（对应OLMo 3的5.9T预训练）；(2) 中间课程阶段在大规模无标注医疗影像+少量合成标注上训练，注入解剖结构先验（对应100B midtraining中注入推理trace）；(3) 微调阶段在目标任务标注数据上训练（对应长上下文扩展的定向能力注入）。每阶段数据量级递减但领域专业度递增。
- **预期收益：** 参考OLMo 3中训练阶段的thinking/instruction数据注入使基础模型全指标平均提升+1.9（Table 10），且中训练5轮迭代后SFT Avg从35.2提升至37.3（Table 6），医疗领域的中间课程有望在标注数据仅为当前1/3的情况下达到相当的微调性能。
- **风险/不适用条件：** 医疗影像的分布差异远大于NLP中的文本域差异——通用视觉特征到医疗解剖结构的迁移距离可能过远，导致中间课程需要远超100B等比例的数据量。此外，如果中间课程数据质量控制不当（如合成标注含有解剖错误），错误知识会被后续阶段放大。

**原语3：能力差对比学习 → 代码审查系统的质量判别训练**

- **目标领域+具体问题：** 自动代码审查工具需要区分高质量代码与有缺陷的代码，但获取人工标注的正负代码对成本极高。当前做法依赖规则引擎（如linter）或在有限人工标注上训练分类器，覆盖面不足。
- **怎么接：** 替换现有代码审查pipeline中的训练数据构造模块。借鉴Delta Learning的能力差配对思路：用强代码生成模型（如GPT-4级别）生成chosen代码，用弱模型（如CodeGen 350M）生成rejected代码，对同一编程任务构造能力差明确的正负对。然后用DPO训练代码审查模型，使其学会区分代码质量的细粒度差异。输入是(任务描述, chosen代码, rejected代码)三元组，输出是训练好的代码质量判别器。
- **预期收益：** 参考Delta Learning相比continued SFT在Avg上+8.4、LiveCodeBench上+17.5的提升（Table 21），能力差配对策略有望显著提升代码审查模型对subtle bugs的检出率。关键优势是完全消除了人工标注需求——质量信号来自模型能力差距本身。
- **风险/不适用条件：** 当代码缺陷不是"能力不足"型（如逻辑错误、性能问题）而是"风格/规范"型（如命名不当、注释缺失）时，强弱模型的输出差异可能不在目标维度上，对比信号无效。此外，如果弱模型的错误模式与真实开发者的错误模式差异过大，学到的判别边界可能无法泛化到真实场景。

**原语4：异步推理-训练流水线 → 机器人仿真中的策略优化加速**

- **目标领域+具体问题：** 机器人强化学习中，物理仿真环境（如MuJoCo/Isaac Gym）生成rollout的速度通常是训练瓶颈——仿真器占用75%以上的训练时间（与OLMo 3 RL中推理占75%时间高度类似，Section 4.4.3），导致GPU训练资源大量空闲。
- **怎么接：** 替换现有机器人RL pipeline中的同步采集-训练循环。将OlmoRL的inflight updates架构迁移：多个仿真器实例（对应vLLM actor节点）持续生成轨迹数据并推入共享buffer，策略网络（对应learner GPU）从buffer中取出已完成的轨迹立即开始训练，无需等待所有仿真器完成当前batch。通过truncated importance sampling修正策略参数滞后（staleness）导致的分布偏差。
- **预期收益：** 参考OlmoRL通过inflight updates实现3.3x总吞吐提升（Table 23: 881→2949 tokens/sec），机器人RL场景中仿真与训练的解耦有望实现2-4x的训练加速。这对于需要数十亿步仿真的灵巧操作任务尤其关键。
- **风险/不适用条件：** 当策略更新步幅较大（如使用大学习率或无clip约束）时，staleness导致的重要性权重偏差可能超出truncated IS的修正能力，引发训练不稳定。此外，物理仿真中的state-dependent action（动作依赖于精确状态）比LLM的token生成对策略滞后更敏感，需要更保守的staleness上界。

**原语5：质量感知上采样 → 自动驾驶感知模型的场景配比优化**

- **目标领域+具体问题：** 自动驾驶感知训练数据中，大部分场景是常规直线行驶，而关键的corner cases（如行人突然横穿、恶劣天气、施工区域）极为稀少。简单过采样corner cases会降低数据多样性，简单过滤低价值场景会丢失分布信息。
- **怎么接：** 替换现有数据管线中的固定采样策略。为每个驾驶场景片段计算质量/难度分数（如基于检测难度、场景稀有度、标注质量），然后应用类似OLMo 3的质量感知上采样曲线：高价值场景获得更高的重复概率，低价值场景以低但非零的概率出现。输入是场景质量分数分布和目标训练数据预算，输出是每个场景的采样权重。
- **预期收益：** 参考OLMo 3中quality-aware upsampling相比DCLM的flat filtering在数据受限场景下的一致性改进（Appendix Table 40），自动驾驶场景中，在同等训练预算下，有望将corner case召回率提升15-25%，同时维持常规场景的检测精度不降。
- **风险/不适用条件：** 当质量评估模型本身存在偏差（如将某些rare-but-normal场景误判为低质量）时，上采样策略会系统性地压制这些场景，导致模型在特定区域的性能退化。此外，自动驾驶数据的质量维度远比文本复杂（空间分辨率、时间连续性、标注精度等多维质量），需要设计多维质量评分函数。

##### 机制家族图谱

**前身 (Ancestors)**

1. **OLMo 2 (OLMo et al., 2024)：** 直接前身，提供了基础架构（同一tokenizer、类似transformer结构）、Dolma数据管线和微退火（microanneal）方法论。OLMo 3的改进包括：(a) 新增长上下文扩展阶段（OLMo 2仅支持4096 context）；(b) 将RL从纯数学域扩展至代码、指令遵循、通用对话四个域；(c) 引入OlmoRL异步流水线实现4x加速；(d) 中训练阶段从单一配方升级为5轮迭代的integration test框架。

2. **GRPO (Shao et al., 2024)：** OlmoRL的算法基础。GRPO引入了group-based相对优势估计替代传统PPO的value function，大幅降低了RL训练的内存需求。OLMo 3在GRPO基础上集成了7项改进：zero gradient filtering、active sampling、token-level loss、no KL loss、clip-higher、truncated importance sampling、no std normalization。这些改进来自DAPO和Dr GRPO等后续工作，但OLMo 3是第一个将它们全部整合并在大规模thinking model上验证的系统。

3. **DCLM (Li et al., 2024a)：** 网页数据处理管线的基础。提供了Resiliparse文本提取、启发式过滤和质量分类器的标准流程。OLMo 3的改进包括：(a) 将flat quality filtering替换为quality-aware upsampling，在数据受限场景下保留更多样性；(b) 引入WebOrganizer进行24主题分区，使优化在主题粒度而非文档粒度上进行；(c) 条件混合（conditional mixing）允许在新数据源到达时增量更新配比而非重新搜索。

4. **RegMix (Liu et al., 2024a) / Data Mixing Laws (Ye et al., 2025)：** swarm-based数据混合搜索的方法论来源。RegMix提出通过训练多个小规模代理模型来预测最优数据配比。OLMo 3的改进包括：(a) 引入条件混合（conditional mixing）处理数据源不断演化的现实场景；(b) 将单次swarm搜索改为多轮迭代（5轮integration tests），每轮利用前轮结果缩小搜索空间；(c) 将搜索范围从源级别扩展到WebOrganizer主题级别+源级别的层次化搜索。

5. **Delta Learning (Geng et al., 2025)：** DPO偏好数据构造方法的来源。原始Delta Learning提出利用模型能力差距构造对比对。OLMo 3的改进包括：(a) 将其从instruct模型推广到thinking模型场景，解决了开源thinking模型稀缺导致无法用传统LLM-judge方法构造偏好对的问题；(b) 实证发现在chosen数据上做continued SFT反而性能下降，但同样的数据通过Delta Learning DPO能获得+8.4的提升（Table 21），为对比学习的必要性提供了强证据。

**兄弟 (Siblings)**

1. **Qwen 3 32B (Yang et al., 2025a)：** 最接近的open-weight竞争者。在AIME 2024上Qwen 3 (80.8) vs OLMo 3.1 Think (80.6)几乎持平；在LiveCodeBench v3上Qwen 3 (90.2) 大幅领先 OLMo 3.1 (83.3)；在IFEval上OLMo 3.1 (93.8) 显著领先Qwen 3 (86.5)；在IFBench上OLMo 3.1 (68.1) 远超 Qwen 3 (37.3)。核心差异：Qwen 3未公开训练数据、代码和中间检查点，使用了从更大模型蒸馏的策略，且训练token量约为OLMo 3的6倍。OLMo 3在token效率上更优但在代码推理上仍有差距。

2. **DeepSeek-R1-Distill-Qwen-32B (Guo et al., 2025)：** 开源推理模型的代表。OLMo 3.1 Think在MATH (96.2 vs 92.6)、AIME 2025 (78.1 vs 56.3)、IFEval (93.8 vs 78.7)上全面领先。核心差异：DS-R1采用蒸馏路线（从671B模型蒸馏到32B），OLMo 3采用从头训练+三阶段post-training路线。DS-R1在AlpacaEval 2 LC上仅26.2（可能是未针对chat优化），而OLMo 3达69.1。

3. **Stanford Marin 32B (Hall et al., 2025)：** 同期fully-open模型。在base model评估中（Figure 1），OLMo 3 Base 32B在预训练和中训练后均显著领先Marin 32B。核心差异：Marin使用相对标准的数据管线，而OLMo 3引入了swarm-based mixing + quality-aware upsampling + olmOCR PDF数据源的组合创新。Marin的decontamination分析揭示了GSM8K泄露不提升性能的现象，OLMo 3独立验证了这一发现。

4. **Apertus 70B (Apertus Team, 2025)：** 70B规模的fully-open模型，但在几乎所有指标上被32B的OLMo 3超越（如MATH: OLMo 3 96.2 vs Apertus 36.2；AIME 2025: 78.1 vs 0.1；HumanEvalPlus: 91.5 vs 42.9）。这表明OLMo 3的post-training pipeline（SFT+DPO+RLVR三阶段）相比仅依赖SFT的方案具有压倒性优势，同时也说明模型规模不是post-training后性能的决定因素。

**后代 (Descendants)**

截至目前暂无直接后代工作发表。但OLMo 3作为fully-open release，其完整的model flow（包括所有中间检查点、数据配方和训练代码）为以下后续研究方向提供了基础设施：(a) 基于Dolci RL-Zero的预训练数据对RL影响的因果分析；(b) 基于OlmoRL代码库的新型RL算法研究；(c) 基于Dolma 3数据管线的数据工程研究。

**创新增量**

OLMo 3的核心创新不是任何单一技术，而是**在fully-open约束下实现了与closed-source方案（如Qwen 3的大模型蒸馏）可比的推理性能**。这一看似"系统集成"的成果背后有三个非平凡的技术贡献：(1) Delta Learning在thinking model场景的成功应用——当开源thinking模型稀缺、传统LLM-judge管线失效时，能力差配对提供了唯一可行的高质量DPO数据构造路径，且实证表明DPO在SFT无法学习的区域仍能提取信号（Table 21的continued SFT反降现象）；(2) OlmoRL的工程-算法协同设计——7项算法改进与inflight updates等基础设施优化互相依赖（如truncated IS是inflight updates的算法保障，active sampling是zero gradient filtering的效率补偿），拆开任何一项都无法独立工作；(3) 条件混合框架将数据优化从"一次性搜索"转变为"持续迭代"——这一思想转变使得OLMo 3能在数据源不断演化的现实研发周期中保持最优配比，是传统RegMix方法无法处理的场景。

#### 背景知识补充 (Background Context)

| 外部技术 | 一句话定义 | 在本文中的角色 | 核心引用 |
|---|---|---|---|
| **RoPE (Rotary Position Embedding)** | 通过旋转矩阵编码token的绝对和相对位置信息的位置嵌入方法 | OLMo 3的基础位置编码方案，θ=500,000；长上下文扩展时通过YaRN对其进行外推 | Su et al., 2024 |
| **YaRN (Yet another RoPE extensioN)** | 通过插值和外推混合策略扩展RoPE支持更长上下文的方法 | 仅应用于全注意力层（非滑动窗口层），将OLMo 3的有效上下文从8K扩展至65K | Peng et al., 2023 |
| **SwiGLU** | 结合Swish激活函数和门控线性单元（GLU）的前馈层激活机制 | OLMo 3 7B和32B模型的标准激活函数 | Shazeer, 2020（隐含引用，架构表Table 33） |
| **RMSNorm** | 仅使用均方根进行归一化（省略均值中心化）的轻量级Layer Normalization变体 | 应用于OLMo 3所有层的输出归一化 | Zhang & Sennrich, 2019（隐含引用） |
| **QK-Norm** | 对注意力机制中Query和Key向量在点积之前进行归一化以稳定训练 | OLMo 3全部模型的标准组件，防止注意力logit爆炸 | Dehghani et al., 2023（隐含引用） |
| **GRPO (Group Relative Policy Optimization)** | 通过同一prompt生成一组回复并用组内相对奖励替代value function来计算优势的RL算法 | OlmoRL的算法基础，OLMo 3在此之上集成了7项改进形成最终训练目标 | Shao et al., 2024 |
| **DPO (Direct Preference Optimization)** | 将RLHF的reward model训练和策略优化统一为直接在偏好对上优化策略的方法 | OLMo 3 Think和Instruct的第二阶段post-training，使用length-normalized变体(β=5) | Rafailov et al., 2024 |
| **DAPO (Decoupled Clip and Dynamic Sampling Policy Optimization)** | 对GRPO的改进，引入zero gradient filtering、clip-higher、token-level loss等技术 | OlmoRL从DAPO采纳了zero gradient filtering、clip-higher和token-level loss三项技术 | Yu et al., 2025 |
| **Dr GRPO** | GRPO的变体，移除优势计算中的标准差归一化以消除难度偏差 | OlmoRL采纳其no-std-normalization策略，公式中A_{i,t}仅减去均值不除以标准差 | Liu et al., 2025b |
| **vLLM** | 基于PagedAttention的高效LLM推理引擎，支持continuous batching | OlmoRL中所有actor节点的推理后端，负责生成RL训练的rollout | Kwon et al., 2023 |
| **Truncated Importance Sampling (TIS)** | 对重要性采样比率设置上界截断以降低方差的方法 | OlmoRL中用于修正vLLM推理引擎与训练引擎之间的对数概率差异(ρ=2.0) | Yao et al., 2025 |
| **DCLM (DataComp for Language Models)** | 大规模网页文本数据集及其标准化处理管线（包括Resiliparse提取、启发式过滤、质量分类） | OLMo 3预训练数据管线的基础，Dolma 3 Mix的Common Crawl处理直接复用DCLM流程 | Li et al., 2024a |
| **WebOrganizer** | 基于LLM标注训练的文档主题分类器，将网页文本划分为24个主题类别 | OLMo 3用其（蒸馏为fastText版本）对预训练数据进行主题分区，作为swarm mixing的优化粒度 | Wettig et al., 2025 |
| **olmOCR** | 将学术PDF文档转换为线性化纯文本的OCR工具 | OLMo 3最重要的新数据源之一：预训练中贡献13.6%数据(805B tokens)，长上下文扩展的核心素材 | Poznanski et al., 2025a,b |
| **CLIPPER** | 通过合成任务（如跨文档摘要、信息检索）增强长上下文训练数据的方法 | OLMo 3的CWE（跨文档写作练习）和REX（检索式练习）合成任务直接受CLIPPER启发 | Pham et al., 2025 |
| **Fill-in-the-Middle (FIM)** | 将代码文档重排为前缀-后缀-中间的格式以训练代码补全能力的数据变换方法 | 中训练阶段Stack-Edu的50%文档经FIM变换（参照StarCoder2的infilling procedure）以注入代码补全能力 | Lozhkov et al., 2024 (StarCoder2) |
| **RULER** | 评估LLM长上下文能力的综合基准，覆盖检索、追踪、聚合等多种长程依赖任务 | OLMo 3长上下文开发的主要评估指标，用于指导YaRN配置和长上下文数据配比决策 | Hsieh et al., 2024（隐含引用） |
| **RegMix** | 通过训练大量小规模代理模型搜索最优数据混合比例的swarm-based方法 | OLMo 3预训练数据配比优化的方法论基础，OLMo 3在此基础上扩展了条件混合和迭代搜索 | Liu et al., 2024a |
