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
- Stanford Marin 32B
- Qwen 3 32B
- Apertus 70B
- DeepSeek R1 32B
- OLMo 2 32B
- Gemma 3 27B
- Llama 3.1 70B
category: llm/pretraining
code_url: null
core_contribution: ''
datasets: []
date: '2025-12-15'
doi: null
failed_gates: []
keywords: []
metrics: []
pipeline_version: 1
publication_type: preprint
quality: full
tags: []
title: Olmo 3
tldr: 全流程开放的推理模型，旗舰 Olmo 3.1 Think 32B 仅用 Qwen 3 约 1/6 的 token 量达到 MATH 96.2%、AIME
  2024 80.6%；OlmoRL 通过 inflight 权重更新将 RL 吞吐从 881 提升至 2949 tok/s（3.35×），Delta Learning
  DPO 在 SFT 饱和后平均再提升 +2.6pp。
url: https://arxiv.org/abs/2512.13961
venue: null
---

#### 动机与第一性原理

##### 痛点 (The Gap)

在 OLMo 3 发布之前，开源语言模型生态存在一个根本性分裂：要么是"完全开放"（fully-open）但能力平庸，要么是能力顶尖但数据与训练过程封闭。Stanford Marin 32B（基于约 6.5T tokens 训练）在完全开放阵营中代表当时最高水平，但其 OlmoBaseEval Math 综合分仅 49.3，落后封闭权重模型 Qwen 2.5 32B（64.7）整整 15 个百分点（Table 2）。更严峻的是，推理模型方向已被 DeepSeek R1 和 Qwen 3 系列主导，而这两者的预训练数据与中间检查点均不对外公开——研究社区无法复现、无法溯源、无法干预，也无法排除"中训数据已包含评测题目"这一混淆变量。Shao et al. (2025b) 和 Wu et al. (2025c) 均指出，benchmark 污染可使虚假奖励与真实奖励一样有效，令整个 RLVR 改进声明失去可信度。

这一困境的深层原因不是简单的"数据少"。OLMo 2 32B 已用约 6.5T tokens 但 Math 仅 53.9、Code 仅 20.5，说明问题不在数据量，而在于**数据组成的结构性缺陷**：缺乏针对性的中训数据注入，没有系统性的长上下文扩展，也没有从预训练就开始埋入推理 trace 的前置投资。Apertus 70B 虽用了 15T tokens，Math 也仅 39.7——说明堆 token 数量在一定程度上已是边际递减的策略。

##### 核心洞察 (Key Insight)

作者发现的第一性原理可以用一条因果链表达：

**Because** 模型能力的天花板在预训练和中训阶段已经隐性确定——数据分布决定了 post-training 各阶段能被"解锁"的上限 → **Therefore** 如果在中训阶段（100B tokens）就系统注入高质量合成推理数据（CraneMath +18.5pp MATH、TinyMATH +13.2pp MATH、Meta-Reasoning +14pp Minerva）并混入 thinking traces，让 base 模型在"体格定型"之前就具备元推理能力的热启动 → **Therefore** post-training 的 SFT 只需"激活"而非"新建"能力，DPO 可以用对比信号突破模仿饱和，RL 则在更高的能力平台上收益显著放大，最终以约 Qwen 3 32B 六分之一的训练 token 数达到相近的推理性能（Table 14）。

第二条核心因果链专门针对 DPO 阶段：**Because** 经过充分 SFT 的模型已经对同质高质量输出形成分布饱和——直接在 Qwen3-32B thinking traces 上继续 SFT 反而平均下降 5.8pp（Table 21）→ **Therefore** 不应追求更好的"正例绝对质量"，而应最大化"正例与负例之间的质量差（delta）"——以 Qwen3-32B thinking 为 chosen、Qwen3-0.6B thinking 为 rejected，对比信号精准 → **Therefore** DPO 平均提升 +2.6pp 且为后续 RLVR 提供更高的 pass@K 起始点，SFT+DPO+RL 比 SFT+RL 平均高出 2.2pp（Table 22）。

第三条因果链是 RL 基础设施的瓶颈与突破：**Because** 推理模型生成长度极不均匀（均值 14,628 tokens，最大 32K），静态批处理会浪费最多 54% 算力在空闲等待上 → **Therefore** 引入连续批处理（continuous batching）消除尾部等待；**Because** 权重同步需 actor 暂停 KV cache 导致 GPU idle → **Therefore** inflight 权重更新（不停推理引擎直接推送新权重）在同等硬件上实现 4× 吞吐提升（881 → 2949 tok/s，Table 23）。

##### 物理/直觉解释

把整个训练流程想象成**培养一个顶级厨师**。大多数竞争者的做法是：先用大量普通食材（预训练）把厨师养大，然后在最后的精英培训（SFT+RL）阶段拼命灌输米其林级别菜谱。问题在于，一个从未接触过精细食材的厨师，就算给再好的菜谱，手感也不对——这正是 OLMo 2 和 Marin 32B 的处境。

OLMo 3 的做法是：**从食材预处理环节（中训阶段）就开始有意识地引入高质量原料**——把数学解题过程（CraneMath 5.62B tokens）、Python 代码重写范式（CraneCode 10B tokens）、推理 trace（QWQ Reasoning Traces 1.87B tokens）提前埋入中训 mix，让模型在"体格定型"之前就熟悉这些高密度结构。到了精英培训阶段，SFT 只需强化已有技能，DPO 用"强弱对比"打磨判断力（就像让厨师对比顶厨与学徒做的同一道菜），RL 则在真实竞赛中反复修正——每一阶段都在前一阶段的高平台上增量叠加，而非从零开始。

Figure 2 直观呈现了这一"分层激活"的全流程：左侧预训练→中训→长上下文扩展构成能力地基，右侧 SFT→DPO→RLVR 则逐步精雕细琢，Think、Instruct、RL-Zero 三条分支共享同一个高质量 Base，而非各自从弱基础出发。Figure 1 则从宏观视角展示了完全开放路线的竞争力：开放中间检查点（beige 节点）才能真正研究各阶段对能力的贡献，这是封闭权重模型天然缺失的维度。正是这条"把宝压在数据工程而非扩大 token 数量"的路径，让 Olmo 3 以更少的总计算量接近了 Qwen 3 的推理天花板。



#### 核心速览

**TL;DR (≤100字):** OLMo 3 用三阶段基础训练（预训 5.93T→中训 100B→长上下文扩展 100B）配合 SFT→Delta DPO→OlmoRL 流水线，构建完全开放的思维模型；旗舰 OLMo 3.1 Think 32B 仅用 Qwen 3 约 1/6 token 量，达到 MATH 96.2%、AIME 2024 80.6%，成为当前最强全开放思维模型。

##### 一图流 (Mental Model)

如果 OLMo 2 是"一次性炼丹"——把所有数据混在一起烧一遍——那么 OLMo 3 更像**分段精炼的高炉**：先用 5.93T 通用矿石打底（预训），再用 100B 精矿强化数学/代码/推理结晶（中训），然后用 50–100B 科学长文献拉伸炉膛口径（长上下文扩展），最后进入后处理车间做三次淬火——SFT 定型、Delta DPO 提纯、OlmoRL 压光。每一道工序都留下完整的中间检查点和配方，任何人都可以从任意节点分叉。

Figure 1 直观呈现这条流水线：左侧基础模型各阶段检查点（浅褐色）与右侧后训练各阶段检查点（深青色）一字排开，形成可追溯的完整模型流。只有全开放模型（Marin、Apertus、OLMo）在流水线上提供中间检查点，而仅开放权重的模型只有终点节点。Figure 2 把每个阶段的数据来源和方法细分为子流程，展示了 Think、Instruct、RL-Zero 三条产品线如何从同一个 Base 分叉——这种"可插拔流水线"使研究者可在 Think SFT、Instruct SFT、RL-Zero 任意节点切入，验证各自假设。

##### 核心机制一句话 (Mechanism in One Line)

**[渐进式分布迁移]** + **[每阶段独立数据课程]** + **[Delta Learning 将对比学习推至 SFT 边界之外]** + **[异步 inflight 权重更新解耦生成与训练]** → **[在约 1/6 token 预算下将全开放模型推理能力逼近 closed-weight 同量级水平]**。

**关键量化结果：**
- Olmo 3 Base 32B Math：61.9（vs 全开放第二名 Marin 32B 49.3，**+12.6pp**）
- 中训对 7B Math：23.5 → 59.8（**+36.3pp**，仅 100B tokens）
- Model Souping 合并两个中训 seed（32B）：Math **+2.9pp**，MCSTEM +1pp
- OlmoRL inflight updates：881 → 2949 tok/s（**3.35×**），inflight 单项贡献 **+117%**
- Delta Learning DPO vs 直接 SFT on chosen：**+5.8pp** avg（SFT chosen 反而下降）
- SFT+DPO+RL vs SFT+RL（7B）：平均 **+2.2pp**
- 长上下文：Olmo 3 32B RULER@65K=79.70，仅用 100B LC tokens 对标 Qwen 2.5 32B（80.73）



#### 方法详解

##### 直觉版 (Intuitive Walk-through)

如 Figure 1 所示，Olmo 3 的整体模型流（Model Flow）覆盖了从数据到最终检查点的全生命周期——这正是它与大多数"仅释放权重"的开放模型的根本区别。Figure 1 的纵轴是基础/后训练平均分，横轴是模型规模；其中浅米色节点代表中间检查点（每个训练阶段均公开），深青色节点代表最终权重。读者可以从 Figure 1 清楚地看到 OLMo 2 → Olmo 3 的性能跃迁，以及 Olmo 3 Base 32B 在全开放模型中独占鳌头的位置。

**旧方法（OLMo 2 基线）的数据流**

OLMo 2 的训练管线较为扁平：预训练阶段用约 4T Web 文本 + 代码 + 数学；随后接一段 Dolmino 中训（以数学为主的 100B token）；后训练仅有 SFT + DPO + 少量数学 RLVR，且不支持长上下文。整体可用以下数字感知：假设拿出 1,000 份文档放进预训练池，OLMo 2 会对其做简单质量过滤（顶部 25% 保留），最终约 250 份文档被使用，且每份文档只出现一次。

**新方法（Olmo 3）改了哪里**

Olmo 3 在同样 1,000 份文档的基础上，先按话题和质量做二维分桶（24 话题 × 20 质量档位 = 480 个子集），然后对顶部 5% 的文档重采样 7 次，底部 40% 直接丢弃，最终可以从 1,000 份文档中"榨出"约 350~400 份有效训练份额——且高质量内容出现频率是低质量内容的 7 倍。这就是 **quality-aware upsampling** 的核心直觉：不是简单过滤，而是"好文章多读几遍"。

除此之外，Olmo 3 新增了三个关键阶段：

1. **Base Model Training — Stage 1: Pretraining（5.93T tokens）**：主体仍是 CommonCrawl，但加入了 olmOCR 科学 PDF（805B token，占 13.6%）——这是第一次将大规模科学文献纳入预训练。Figure 2 左侧展示了这一阶段的数据来源：web text、science PDFs、code 三路并行汇入。

2. **Stage 2: Midtraining（100B tokens）**：从纯数据转向"能力定向"——数学合成数据（CraneMath、MegaMath、TinyMATH 等）占约 20%，代码（Stack-Edu FIM + CraneCode）占 20%，QA 合成占 14%，思维链数据占约 9%。如 Figure 2 所示，中训阶段专门引入 math、reasoning、Q&A、synthetic 等新数据流，为后训练埋好"种子"。

3. **Stage 3: Long-context Extension（50B/100B tokens）**：借助 olmOCR PDFs（主力数据，600B pool）+ CWE/REX 合成任务，将上下文从 8K 扩展到 65K。

Post-training（Figure 2 右侧）分成 Think / Instruct / RL-Zero 三条分支，每条分支都经历 Supervised Finetuning (SFT) → Preference Tuning with Delta Learning (DPO) → Reinforcement Learning with OlmoRL (RLVR) 三级，且各阶段数据（Dolci 系列）完全公开。

**一个具体数字示例**：假设有 100 个数学问题送进中训。旧方法（OLMo 2）会直接把这 100 题作为 SFT 数据。Olmo 3 的做法是：先对这 100 题生成 100 × 100 = 10,000 个同类新题（TinyMATH），再生成 Python 代码解答（TinyMATH-PoT），再生成英文对话讨论（TinyMATH-MIND），最终得到约 1.14B token 的合成数据，在微调后 MATH 基准提升 13.2 分。

Figure 2 还展示了后训练阶段数据流的分叉：Think SFT 从 Base 开始；Instruct SFT 从 **Think SFT checkpoint** 出发（"warm-start"），这一设计让 Instruct 模型在不增加冗长输出的前提下平均提升 3.3pp（Table 29）。

##### 精确版 (Formal Specification)

**流程图 (Text-based Flow)**

```
[9T 原始数据池]
    → HTML/PDF 文本抽取 (Resiliparse / olmOCR)
    → 启发式过滤 (URL过滤、长度、符号比例、语言检测)
    → 三级去重 (精确哈希 → MinHash模糊去重 → 后缀数组子串去重)
    → 话题分类 (WebOrganizer fastText, 24类) × 质量分类 (fastText, 20档位)
    → 480个(话题, 质量)子集 [Shape: N_topic × N_quality_bucket]
    → 约束混合 (Constrained Mixing): 30M代理模型 swarm → 回归 → 优化
    → 质量感知上采样 (Quality-Aware Upsampling, 最高7×, 底部40%丢弃)
    → Dolma 3 Mix (5.93T tokens)
    → 预训练 Olmo 3 Base Stage 1
    → 中训 Stage 2 (Dolma 3 Dolmino Mix, 100B tokens)
       ├─ microanneal反馈 (5B快速测试)
       └─ 集成测试 (100B候选混合)
    → 长上下文扩展 Stage 3 (Dolma 3 Longmino Mix, 50B/100B tokens)
       ├─ olmOCR PDFs (8K~32K自然长文档)
       └─ 合成CWE/REX任务注入
    → Olmo 3 Base (8K→65K 上下文)
    → 后训练分支
       ├─ Think: SFT(~2.27M样本) → DPO(200K, Delta Learning) → RLVR(~105K)
       ├─ Instruct: Think SFT热启 → Instruct SFT → DPO → RLVR
       └─ RL-Zero: Base直接RLVR(13.3K数学题, 无SFT热启)
    → Olmo 3 Think / Instruct / RL-Zero
```

**关键公式与变量**

**Eq.1：OlmoRL 目标函数**

$$J(\theta) = \frac{1}{\sum_{i=1}^{G}|y_i|} \sum_{i=1}^{G}\sum_{t=1}^{|y_i|} \min\!\left(\frac{\pi_{\text{old}}}{\pi_{\text{vllm}}}, \rho\right) \cdot \min\!\left(r_{i,t} A_{i,t},\ \text{clip}(r_{i,t}, 1{-}\varepsilon_{\text{low}}, 1{+}\varepsilon_{\text{high}}) A_{i,t}\right)$$

- $r_{i,t} = \pi(y_{i,t}|x,y_{i,<t};\theta) / \pi(y_{i,t}|x,y_{i,<t};\theta_{\text{old}})$：每个 token 的 importance sampling 比率，衡量新旧策略在该 token 上的概率差距
- $\rho$：截断 IS 上限（truncated importance sampling cap），控制极端离策率以降低方差
- $\varepsilon_{\text{low}}, \varepsilon_{\text{high}}$：不对称裁剪界限，$\varepsilon_{\text{high}} > \varepsilon_{\text{low}}$，允许策略在正向更新时迈更大步
- $A_{i,t}$：第 $i$ 条回复第 $t$ 个 token 的优势值（advantage），对同一 prompt 的 $G$ 条回复计算相对奖励
- 分母 $\sum|y_i|$：token 级归一化（而非样本级），消除长回复对损失的偏倚

**Eq.2：优势函数（无标准差归一化）**

$$A_{i,t} = r(x, y_i) - \text{mean}\!\left(\{r(x, y_i)\}_{i=1}^{G}\right)$$

- $r(x, y_i)$：验证器对回复 $y_i$ 给出的奖励（0/1 或连续值）
- $G$：同一 prompt 采样的回复数（group size）
- **关键设计**：去掉 GRPO 中的标准差除法项。原因：如果一道题所有 G 条回复奖励相同（方差=0），标准差归一化会将优势放大至无穷大，引入难度偏置；去掉后对难题/简单题一视同仁

**数值推演 (Numerical Example)**

以 OlmoRL 的一个 mini-batch（G=4 条回复，一道数学题）为例：

设 prompt $x$ = "Steve 猜一道二选一题的概率是多少至少猜对一半"，4 条回复奖励为：
$$r_1=1, \quad r_2=1, \quad r_3=0, \quad r_4=0$$

**Step 1**：计算 group mean：
$$\bar{r} = (1+1+0+0)/4 = 0.5$$

**Step 2**：计算各回复优势（去掉std归一化）：
$$A_1 = 1 - 0.5 = +0.5, \quad A_2 = +0.5, \quad A_3 = -0.5, \quad A_4 = -0.5$$

**Step 3**：若使用 GRPO 标准差归一化，$\sigma = 0.5$，则优势变为 $\pm 1.0$，放大了梯度。对于全对（G条全1）或全错的 batch，$\sigma=0$，归一化后 $A \to \infty$，造成训练不稳定。OlmoRL 直接跳过此步。

**Step 4**：计算 clip-higher 项，$\varepsilon_{\text{low}}=0.2, \varepsilon_{\text{high}}=0.28$（论文设定）：
- 对于 $r_{i,t}=1.1$（略偏离 old policy），clip 范围 = $[0.8, 1.28]$，$r_{i,t}=1.1$ 在范围内，不截断
- 对于 $r_{i,t}=1.5$，超过 1.28，截断为 1.28；但若 $r_{i,t}=0.6$，低于 0.8，截断为 0.8

**Step 5**：token 级损失归一化：设 4 条回复分别有 300, 250, 200, 150 个 token，分母 = 900（不是 4），每条回复贡献损失与其长度成正比，防止短回复因样本数归一化而被过度代表。

**伪代码 (Pseudocode)**

```python
import torch
import torch.nn.functional as F

def olmo_rl_loss(
    logprobs_new: torch.Tensor,    # [B, T] - 当前策略的 log prob
    logprobs_old: torch.Tensor,    # [B, T] - 旧策略的 log prob (θ_old)
    logprobs_vllm: torch.Tensor,   # [B, T] - vLLM 推理时的 log prob
    rewards: torch.Tensor,         # [B]    - 每条回复的 verifier 奖励
    attention_mask: torch.Tensor,  # [B, T] - padding 掩码
    group_size: int = 8,
    eps_low: float = 0.2,
    eps_high: float = 0.28,
    rho: float = 3.0,              # 截断 IS 上限
):
    B, T = logprobs_new.shape
    assert B % group_size == 0
    G = group_size

    # Step 1: 计算优势（无 std 归一化）
    rewards = rewards.view(-1, G)                      # [B/G, G]
    advantages = rewards - rewards.mean(dim=-1, keepdim=True)  # [B/G, G]
    advantages = advantages.view(B)                    # [B]
    # 扩展到 token 维度
    advantages = advantages.unsqueeze(1).expand(B, T)  # [B, T]

    # Step 2: 计算 per-token importance sampling ratio
    ratio = torch.exp(logprobs_new - logprobs_old)     # [B, T]

    # Step 3: 截断 IS（调整 vLLM 与 trainer 策略的差距）
    is_correction = torch.exp(logprobs_old - logprobs_vllm)  # [B, T]
    is_correction = torch.clamp(is_correction, max=rho)

    # Step 4: clip-higher PPO 目标
    surr1 = ratio * advantages                         # [B, T]
    ratio_clipped = torch.where(
        advantages > 0,
        torch.clamp(ratio, max=1 + eps_high),          # 正优势: 允许更大上界
        torch.clamp(ratio, min=1 - eps_low),            # 负优势: 截断下界
    )
    surr2 = ratio_clipped * advantages                 # [B, T]
    per_token_loss = -is_correction * torch.min(surr1, surr2)  # [B, T]

    # Step 5: token 级归一化（非样本级）
    token_counts = attention_mask.sum()                # scalar
    loss = (per_token_loss * attention_mask).sum() / token_counts

    return loss


def zero_gradient_filtering(batch_rewards, group_size):
    """过滤全相同奖励的 group（零梯度样本）"""
    rewards = batch_rewards.view(-1, group_size)       # [N_groups, G]
    # 如果 group 内所有奖励相同（std=0），则过滤掉
    valid_mask = rewards.std(dim=-1) > 0               # [N_groups]
    return valid_mask


def active_sampling(prompt_queue, desired_batch_size, model, verifier, group_size):
    """持续从队列中采样，直到凑够 desired_batch_size 个非零梯度样本"""
    valid_completions = []
    while len(valid_completions) < desired_batch_size:
        prompts = prompt_queue.get(group_size)
        completions = model.generate(prompts)          # vLLM 连续批处理
        rewards = verifier.score(prompts, completions)
        mask = zero_gradient_filtering(rewards, group_size)
        for i, valid in enumerate(mask):
            if valid:
                valid_completions.append((prompts[i], completions[i*group_size:(i+1)*group_size], rewards[i]))
    return valid_completions[:desired_batch_size]
```

##### 设计决策 (Design Decisions)

**决策 1：Modeling and Architecture — SWA（滑动窗口注意力）仅在 3/4 层使用，最后一层保留全注意力**

- **备选方案 A**：全部 SWA（全滑动窗口）→ 显存最省，但长距离依赖丢失
- **备选方案 B**：全部全注意力 → 长上下文性能最强，但显存二次方增长
- **Olmo 3 选择**：3/4 层 SWA (window=4096) + 1/4 层全注意力（含最后一层）
- **核心 trade-off**：以轻微质量损失换取推理和训练中显著的显存节省；最后一层全注意力保留了全局上下文汇聚能力，对分类和生成至关重要
- YaRN 位置编码仅应用于全注意力层，RULER@65K=79.70，与 Qwen 2.5 32B（80.73）相近（Figure 13a，论文做了对比实验）

**决策 2：质量感知上采样曲线（非平坦过滤）**

- **备选方案**：DCLM 式平坦过滤（顶部 25% 直接保留，剩余全丢）
- **Olmo 3 选择**：单调递增上采样曲线，顶部 5% 重复 7 次，底部 40% 丢弃，中间部分线性插值
- **证据**：Table 39（附录）显示，在所有重复因子下，质量感知上采样均优于平坦过滤
- **trade-off**：曲线需要为每个 24 个话题桶分别拟合（积分=目标 token 量），增加实现复杂度，但带来更细粒度的质量控制

**决策 3：条件混合（Conditional Mixing）**

- **问题背景**：PDF 数据比 Web 数据晚好几个月才处理完毕；重新做一遍完整的 swarm（训练 30M 代理模型 × 120 次）代价极高
- **解决方案**：将已优化的 Web+Code 混合比例"冻结"视为一个虚拟域，只在此基础上再做 PDF 的增量 swarm
- **对比**：论文未与从头重做完整 swarm 做直接对比，但工程合理性充分；Chen et al. (2026) 给出了理论依据
- **trade-off**：子空间限制可能错过全局最优，但大幅降低了计算成本并缩短了开发周期

**决策 4：Delta Learning DPO（chosen=大模型，rejected=小模型）**

- **旧做法**：UltraFeedback 式 GPT-judge 打分，从多个模型池中选最好最坏的一对
- **新发现**：直接在 Qwen3-32B 的输出上做 SFT 会损害 Olmo 3 Think SFT 性能 −5.8pp（Table 21），因为 32B 输出质量已不如 Olmo 3 自己的 SFT 数据
- **Delta Learning 解法**：paired (Qwen3-32B thinking 作为 chosen, Qwen3-0.6B thinking 作为 rejected)，DPO 后平均增益 +2.6pp（Table 21）
- **核心原理**：preference 数据的关键是 chosen 与 rejected 之间的质量 **差值（delta）**，而非 chosen 的绝对质量
- **trade-off**：小模型 rejected 的多样性有限，但在 thinking 模型可用选择极少的现实条件下（几乎无多个开放 thinking 模型），这是最优解

**决策 5：Instruct SFT 从 Think SFT 检查点热启**

- **备选方案**：从 Base 直接训 Instruct SFT
- **实验结果**：热启平均提升 3.3pp（Table 29），且 Instruct 回复长度不增加（无思维链泄漏）
- **机制推断**：Think SFT 强化了模型的内部推理结构；即使后续 Instruct SFT 去除 `<think>` 标记，推理能力的"遗产"仍保留在权重中
- **trade-off**：需要先完成 Think SFT 才能开始 Instruct SFT，增加了流水线串行依赖；但性能收益显著（如 Figure 2 所示的 warm-start 路径）

**决策 6：去除 KL 项 + 去除标准差归一化**

- **KL 项**：标准 GRPO 有 KL 正则防止策略偏离参考；OlmoRL 去掉后发现"不会导致过度优化或训练不稳定"（Section 4.4.1）
- **std 归一化**：GRPO 计算优势时除以组内奖励标准差。对于全对/全错的 group（std=0），此操作引发数值爆炸，且对简单题的梯度放大倍数高于难题，形成难度偏置（Dr.GRPO，Liu et al. 2025b 最先发现）
- **论文对比**：Table 23 展示 inflight updates（+117% 吞吐），是最大的单项基础设施收益；算法改动（去KL、去std）的单独消融未在主文给出，但整体 OlmoRL 相比 OLMo 2 baseline 从 881 tok/s 提升到 2949 tok/s

##### 易混淆点 (Potential Confusions)

**混淆点 1：质量感知上采样 vs. 去重策略，两者关系**

❌ 错误理解：去重之后就不需要质量感知上采样了，因为去重已经"净化"了数据，剩下的都是好数据。

✅ 正确理解：去重和质量上采样是**相辅相成但目标不同**的两个步骤。去重（三级：精确哈希 → MinHash → 后缀数组）的目标是消除内容重复——它会有意**丢弃**重复文档的质量信号（因为高重复文档计数本可作为质量信号）。质量上采样则是在去重之后的洁净数据集上，通过**重新引入受控重复**来补偿：把顶部 5% 的文档重复 7 次，实现数据利用率最大化。两者缺一不可：如果只去重不上采样，高质量文档出现频率与低质量相同；如果只上采样不去重，大量噪声文档也会被放大。

**混淆点 2：OlmoRL 的 off-policy 是问题还是特性？**

❌ 错误理解：OlmoRL 使用全异步框架，actor 和 learner 之间存在权重不同步（off-policy），这会导致训练不稳定，需要用 KL 项来纠正。

✅ 正确理解：OlmoRL **故意** 选择 off-policy 异步框架（Noukhovitch et al. 2024），并用**截断 IS（truncated importance sampling）**而非 KL 项来处理策略差异。具体地，公式（1）中 $\min(\pi_{\text{old}}/\pi_{\text{vllm}}, \rho)$ 这一因子对比推理引擎（vLLM）和训练引擎（PyTorch）之间的 log prob 差距并加以截断，防止极端离策样本主导梯度。KL 项被去除的原因是它会**限制**策略更新幅度，反而不利于长 RL 运行中的持续改进——实验显示去掉 KL 后训练不会过度优化（Section 4.4.1）。Inflight weight updates（无需暂停生成引擎即可更新权重）进一步缩小了 off-policy 程度，带来 4× 吞吐提升（Table 23）。

**混淆点 3：中训中加入思维链和指令数据，会不会让 Base 模型"污染"成 Instruct 模型？**

❌ 错误理解：在中训中混入 QWQ 思维链（1.87%）和 Tulu3 指令数据（1.1%）会使 Base 模型学到 chat template 特殊 token，导致 Base 推理时异常输出，破坏其作为"纯净"基础模型的性质。

✅ 正确理解：论文专门做了消融实验发现这个问题，并找到了解法：**去掉指令数据中的特殊 token（`<|im_start|>`、`<|im_end|>` 等）和 chat template，改用普通换行符格式**。实验显示，保留 chat template + 特殊 token 的版本会导致 Base 模型推理时不断输出这些 token，GSM8K 从 49.43 骤降至 0（Section 3.5.4）。正确去掉后，含指令和思维链数据的中训混合比不含的版本在所有基础评估指标上均更好（Table 10，平均 +1.9pp），包括数学、代码和 QA，而不是拉低 Base 性能。这一发现说明：格式是关键，内容本身有利于 Base 能力，只要去掉"后训练专属语法"即可。




#### 实验与归因

##### 核心收益：从基座到旗舰的量化跨越

Olmo 3 的实验体系横跨三个独立维度：基座模型的分阶段训练、思考模型（Think）的三段式后训练、以及强化学习基础设施的效率革命。理解这三条线上的数字，才能把握整个项目的技术密度。整个体系最聪明的地方在于，它不是「调好一个超参数再调下一个」的线性优化，而是在数据、算法、工程三个维度上同时打出协同组合拳——每一层的提升都为下一层创造了更好的起点，而 Figure 2 的模型流图正是这套逻辑最直观的可视化。

**基座模型的绝对领先优势。** Table 2 给出了最直接的答案：Olmo 3 Base 32B 在 OlmoBaseEval Math 上达到 61.9，比同为完全开放的 Stanford Marin 32B 高出 12.6 个百分点（49.3），比 Apertus 70B 高出 22.2 个百分点（39.7）；代码评测（OlmoBaseEval Code）则以 39.7 对 Marin 32B 的 30.8 领先 8.9 个百分点。这是在参数规模相近的完全开放模型中取得的双位数差距，并非边际优化的产物。值得注意的是，Marin 32B 使用了约 6.5T tokens，而 Olmo 3 Base 32B 的预训练仅 5.9T tokens——更少的数据取得更高的分数，说明数据质量和混合策略（尤其是 olmOCR 科学 PDF 和质量感知上采样）带来了实质性的效率提升。论文的 Main Results for Olmo 3 Think 章节中，旗舰推理模型 Olmo 3.1 Think 32B 展示了完整的竞技实力：MATH 500 96.2、AIME 2024 80.6、AIME 2025 78.1、LiveCodeBench v3 83.3，是迄今最强的完全开放思考模型，且仅使用了 Qwen 3 32B 约六分之一的训练量（p.5, Table 1）。与 Qwen 3 32B 的对比尤为说明问题：AIME 2024 80.6 vs 86.3（差距 5.7pp），AIME 2025 78.1 vs 78.8（差距仅 0.7pp），IFBench 68.1 vs 37.3（Olmo 3.1 领先 +30.8pp）——在 token 效率相差 6 倍的前提下，两者在多数高难度推理基准上的差距已进入个位数，而 Olmo 3.1 在指令遵循维度上反超。

如图 Figure 1 所示，这一成绩并非一步到位：图中沿着 Pretrain → Midtrain → Long Context 的横轴，Olmo 3 32B 的基础评测均值呈阶梯式跃升——中训练阶段贡献了 Math 和 Code 的最大单步涨幅，而长上下文扩展则在不损失短文本性能的前提下解锁了 65K 上下文能力。在右侧的后训练轴（SFT → DPO → RL）上，Olmo 3.1 32B 的后训练平均分同样逐级攀升，最终在完全开放模型中独占鳌头。这两条曲线共同支撑了 Figure 2 所描绘的整体模型流图：左侧三阶段基座训练为右侧三段式后训练提供了质量基础，两者缺一不可。Figure 1 还揭示了一个微妙的竞争格局：Marin 32B 和 Apertus 70B 作为同为完全开放的对手，其基础评测均值均低于 Olmo 3 32B；而 Qwen 2.5 32B 和 Gemma 3 27B 虽然是开放权重模型（非完全开放），其后训练结果也被 Olmo 3.1 32B 追平或超过。

---

##### 归因分析：消融实验按贡献大小排序

###### 第一梯队：工程基础设施——OlmoRL 吞吐量的 4× 跃升

消融实验中贡献最大、也最容易被忽视的是强化学习基础设施。Table 23 呈现了从 OLMo 2 基线到 Olmo 3 完整堆栈的逐步拆解：

| 配置 | 总 token (M) | token/s | MFU (%) | MBU (%) |
|---|---|---|---|---|
| OLMo 2 基线 | 6.34 | 881 | 0.30 | 12.90 |
| + 连续批处理 | 7.02 | 975(+10.7%) | 0.33 | 14.29 |
| + 更优线程 | 9.77 | 1358(+39.3%) | 0.46 | 19.89 |
| + 飞行中权重更新（Olmo 3） | 21.23 | **2949(+117%)** | 1.01 | 43.21 |

三项改进中，「飞行中权重更新（inflight updates）」贡献最大，单独带来超过 117% 的吞吐量提升，将全栈吞吐从 881 tok/s 拉升至 2949 tok/s（p.47, Table 23）。这项改进的原理是：传统方案每次训练步结束后要暂停所有 actor、清空 KV 缓存再同步权重，导致 GPU 空转；Olmo 3 改为在不中断生成的情况下立即更新权重，依赖生成框架的线程安全性实现零停顿同步。结合连续批处理对长序列（均值 14,628 token，最长 32K）动态 padding 浪费（最高 54%）的消除，最终实现用更少节点（5 节点对比 9 节点）在更短时间（7 天对比 14 天）完成一个 epoch 的训练（p.51）。这是整个消融体系中绝对值提升最显著的单点改进。

如 Figure 2 所示，OlmoRL 基础设施的突破直接使延长 RL 训练成为现实——Olmo 3.1 Think 32B 正是在此基础上将 RL 步数从 750 步（Olmo 3 Think 32B）延长至 2300 步，方才取得 AIME 2024 +3.8pp、AIME 2025 +5.6pp、IFBench +20.5pp 的额外增益（p.50, Table 14）。换言之，没有 inflight updates 带来的 4× 吞吐提升，Olmo 3.1 就不可能在相同时间预算内完成 2300 步的延长训练——基础设施改进和模型性能提升之间存在直接因果链条，而非并行的独立贡献。

此外，OlmoRL 还引入了**主动采样（active sampling）**机制来解决零梯度批次退化问题：当某个批次中所有样本的奖励标准差为零（全对或全错）时，传统 GRPO 会将该批次纳入训练但梯度为零，导致有效批次比例随训练进行而不断下降；OlmoRL 的主动采样框架则持续从 actor 队列中拉取样本并重新采样，直到积累足够的非零梯度样本为止。论文在 Section 6（RL-Zero）中验证：主动采样能在整个训练过程中维持超过 90% 的非零优势批次比例，而标准 GRPO 配置随训练步数增加这一比例持续下滑（Figure 26, p.67）。这对数学单域 RL 训练尤其关键——模型越来越强，越来越多的题目被完全解决，零梯度批次问题愈发严重。

###### 第二梯队：Delta Learning DPO——SFT 饱和后的突围

第二大贡献来自于 Delta Learning 驱动的偏好优化（DPO）。论文通过 Table 21 和 Table 22 的两层实验将其锁定：

**Table 21 的核心发现：直接 SFT 的失败。** 对 Qwen 3 32B Think 生成的 chosen response 继续做监督微调，结果是所有评测指标全面下滑——chosen response 质量已弱于模型在 Dolci Think SFT 阶段见过的数据，继续模仿只会退步。Delta Learning 的解法是将这些「不够好」的 chosen response 与 Qwen 3 0.6B Think 生成的 rejected response 配对，用「大模型选择 vs 小模型拒绝」的强对比度（质量差值最大化）驱动 DPO 信号，将失效的 SFT 数据变为有效的对比训练信号（p.43）。定量效果：chosen 方采用 Qwen 3 32B、rejected 方采用 Qwen 3 0.6B 的 DPO 配置相较于直接 SFT 平均提升 +2.6pp（notes KEY_FINDINGS, p.48）。

**Table 22 的核心发现：DPO 是更好的 RL 起点。** 在 7B 模型上对比四条路径（1000 步 RL 后）：

| 训练路径 | Avg. | AIME25 | AIME24 | IFEval | LCB |
|---|---|---|---|---|---|
| SFT | 70.1 | 57.6 | 69.6 | 77.9 | 67.8 |
| SFT + DPO | 72.7(+2.6) | 62.7(+5.1) | 74.6(+5.0) | 75.9(-2.0) | 75.1(+7.3) |
| SFT + RLVR | 71.9(+1.8) | 62.4(+4.8) | 70.0(+0.4) | 82.8(+4.9) | 70.7(+2.9) |
| SFT + DPO + RLVR | **74.1(+4.0)** | **64.2(+6.6)** | **73.2(+3.6)** | 82.3(+4.4) | **73.4(+5.6)** |

SFT+DPO+RLVR 以平均 74.1 分全面优于 SFT+RLVR（71.9），差距 2.2pp（p.53, Table 22）。更关键的结论：SFT → DPO 的增益和 DPO → RL 的增益不是相互抵消的，而是叠加的。DPO 为 RL 提供了更高的 pass@K 起点（AIME 评测上 DPO 模型 pass@K 高于 SFT 模型），而 RLVR 的作用之一正是将 pass@K 的潜力转化为 pass@1 的实际分数（p.50）。

###### 第三梯队：中训练中注入指令与思维链数据

基座训练阶段的关键消融来自 Table 10。在一个 100B token 中训练集成测试中，对比「含指令+思维链数据的完整混合」与「无此类数据的混合」（保持总 token 数不变）：

| 配置 | Avg | MC STEM | MC Non-STEM | GenQA | Math | Code |
|---|---|---|---|---|---|---|
| 无指令/思维链数据 | 48.8 | 63.6 | 74.0 | 66.7 | 43.1 | 23.3 |
| 完整混合（含指令+思维链） | **50.7(+1.9)** | **64.9(+1.3)** | **75.7(+1.7)** | **68.1(+1.4)** | **48.7(+5.6)** | **24.4(+1.1)** |

平均提升 1.9pp，且每个子维度均正向（p.29, Table 10）。这一发现颠覆了传统认知——通常认为指令数据只对后训练有效，但 Olmo 3 证明将其纳入中训练混合，在后训练之前就能带来显著的基础能力增益（math 子项提升高达 5.6pp）。其背后的机理是：中训练阶段接触过格式化推理示例的模型，在面对后训练的对齐学习时具备更好的「热身」状态，如 Figure 2 中展示的模型流程所示，中训练与后训练并非截然分开的独立阶段，而是存在数据层面的深度耦合。

Table 13 进一步验证了三阶段基座训练对绝对分数的贡献：Olmo 3 7B 从 Stage 1（预训练完成）的 Math 23.5、Code 19.8，经 Stage 2（中训练）跃升至 Math 59.8(+36.3)、Code 31.9(+12.1)，再经 Stage 3（长上下文扩展）保持水平，100B token 的中训练贡献了绝大部分数学与代码能力的增益（p.29）。这组数字有一个重要的比较视角：OLMo 2 7B 在相同预训练规模（约 4T tokens）下，Stage 2 中训练后的 Math 仅 41.7、Code 仅 10.4，而 Olmo 3 7B Stage 2 分别达到 59.8 和 31.9。同等中训练预算（100B tokens）下，Olmo 3 的 Dolmino Mix 比 OLMo 2 的中训练数据在 Math 上多出 18.1pp、Code 上多出 21.5pp，这正是数据配方迭代（五轮候选混合 + 微退火验证 + 去污染）的量化收益。

域权衡实验（Table 7）为这个配方的合理性提供了反证：当研究团队故意将混合向 GenQA 方向倾斜时，Math Code 从 Round 5 的 57.3/31.2 暴跌至 27.5/11.9；当向 Math-Code-Thinking 方向倾斜时，MCSTEM 和 GenQA 则从 66.4/73.1 分别跌至 62.5/65.9。最终 Round 5 混合在所有子域保持均衡，代价是 Math 略低于极限（57.3 vs 60.8），但换来了 MCSTEM（66.4 vs 62.5）和 GenQA（73.1 vs 65.9）的全面保全——这是有意为之的帕累托权衡，而非优化失败。

###### 第四梯队：模型汤融合（仅 32B）

Olmo 3 Base 32B 的中训练采用双种子独立训练后做模型汤融合。相比两次独立运行中的最佳单次结果，融合后的模型在 MCSTEM 上提升近 1pp，GenQA 提升 0.4pp，Math 相对两次运行分别提升 2.9pp 和 1.6pp，MMLU 提升约 1pp，GSM Symbolic 提升 5pp 和 2pp（p.30, Section 3.5.4）。这一方法的额外成本是多一次独立运行，收益则是完全不引入新数据就获得的稳健提升，属于「无附加风险」的工程优化。注意此方法对 7B 模型初步实验未见类似收益，因此仅 32B 采用。

###### 第五梯队：Instruct 模型从 Think SFT 热启动

Table 29 展示了 Instruct 模型的一个关键设计选择——从 Think SFT checkpoint 而非基座模型开始 Instruct SFT：

| 配置 | Avg | GPQA | MATH | GSM8K | OMEGA | MBPP | LCB |
|---|---|---|---|---|---|---|---|
| 无 Think SFT（从基座启动） | 44.5 | 29.7 | 60.3 | 87.6 | 8.6 | 54.1 | 13.0 |
| 有 Think SFT（热启动） | **47.8(+3.3)** | **34.4(+4.7)** | **65.9(+5.6)** | **91.1(+3.5)** | **12.2(+3.6)** | **57.1(+3.0)** | **17.1(+4.1)** |

平均增益 3.3pp，且平均回复长度几乎不受影响（无明显冗长化），说明 Think SFT 的收益主要体现在内化推理结构上，而非输出格式上（p.59, Table 29）。如 Figure 2 的模型流所示，Think SFT → Instruct SFT 的传导路径是一条有效的能力复用通道。

###### 第六梯队：Instruct DPO 偏好信号的互补效应

Table 32 将 Instruct DPO 的偏好信号来源拆解为五个递进实验：

| 配置 | Avg | BBH | GPQA | MATH | CHE | LCB | IFEval | AE2 |
|---|---|---|---|---|---|---|---|---|
| Dev 7B SFT ckpt（基线） | 51.9 | 47.7 | 30.2 | 65.5 | 69.3 | 17.9 | 83.2 | 23.8 |
| OLMo 2 preference data | 55.5(+3.6) | 55.6 | 33.7 | 63.6 | 73.7 | 12.7 | 84.5 | 35.2 |
| Updated GPT UltraF pipeline | 55.4(-0.1) | 51.2 | 31.5 | 61.8 | 71.5 | 14.7 | 80.8 | 47.5 |
| + 引入弱模型 | 56.3(+0.9) | 50.4 | 33.9 | 63.8 | 74.3 | 18.2 | 81.9 | 44.4 |
| + 最低分 rejected | 57.4(+1.1) | 53.6 | 34.4 | 64.2 | 75.2 | 19.1 | 82.3 | 47.0 |
| Delta learning only | 57.6(+0.2) | 49.5 | 35.5 | 64.6 | 73.9 | 22.0 | 79.1 | 46.1 |
| **Delta learning + GPT** | **60.4(+2.8)** | **66.9** | **34.6** | **64.3** | **74.1** | **21.1** | **83.0** | **49.8** |

两个关键结论：1）直接用更好的 GPT judge（GPT-4o → GPT-4.1）不但没有提升，反而微降（55.4 vs 55.5），根源在于新生成的 chosen/rejected 对之间质量差异太小；2）Delta learning + GPT 的组合（60.4）显著超过任何单独来源（delta-only 57.6，GPT-only 约 57.4），说明两者的偏好信号在维度上互补，组合收益 +8.5pp（相比 SFT 基线 51.9）大于两者单独收益之和（p.61, Table 32）。

###### 补充：RL-Zero——基座直接 RL 的极限探测

作为独立实验线，Olmo 3 RL-Zero 系列从纯基座（Olmo 3 Base 7B）出发，不经任何 SFT 或 DPO，直接施加 RLVR，用于研究预训练数据对 RL 效果的影响。核心发现来自 Figure 24：在数学域 RL 训练中，Olmo 3 Base 7B 的 AIME 2024 pass@1 从约 20% 在 2500 步内稳步提升至约 50%——这与 DAPO（Yu et al., 2025）在 Qwen 2.5 32B（参数规模大 4 倍以上）上用 10 倍步数取得的结果相当（p.65, KEY_FINDINGS）。此结果有两层意义：第一，验证了 Olmo 3 的预训练数据质量足够支撑 RL 从零冷启动，消除了「模型只是在中训练时见过评测数据」的混淆变量（因为 RL-Zero 数据集已对预训练和评测数据均做了去污染）；第二，为 RL 算法研究社区提供了一个真正干净的 fully-open 基准——此前主流 RL 开放基准（DAPO、GRPO 变体等）均基于 Qwen 2.5 系列，而 Qwen 2.5 的中训练数据不公开，无法排除其对特定基准的隐性适配。

RL-Zero 实验还验证了 active sampling 在极端难度梯度下的必要性：数学 RL 训练初期，Olmo 3 Base 7B 在许多题目上 pass@8 接近 0%，大量批次为全零梯度；而主动采样通过持续重采样保持了有效训练信号的密度，Figure 26 显示非零优势批次比例全程高于 90%，对比标准 GRPO 在 1000 步后比例降至 50% 以下（p.67）。

---

##### 可信度检查：公平性与刷榜嫌疑分析

**实验设置是否公平？** 整体而言，Olmo 3 的实验设置是开放生态中难得的高透明度案例，但仍有若干值得审视的细节：

**正面证据——去污染的严格执行。** Olmo 3 针对中训练数据专门开发了 `decon` 工具包，采用 n-gram 抽样检测 + 聚类扩展双阶段流程，对 OLMES 评测套件中的所有 benchmark 进行比对和移除（p.28, Section 3.5.3）。更重要的是，论文通过「虚假奖励验证实验」（spurious-reward RL training，Figure 27）直接证明：在本数据上做 RL 且没有真实学习信号时，benchmark 分数不会提升，排除了中训练数据泄露导致的虚假收益（p.30, KEY_FINDINGS）。这是同类论文中少见的主动去伪证明。

**正面证据——多种子方差报告。** 评测采用 3 次运行取均值，并报告了所有 14 个模型（基线+自研模型）每个评测的标准差：高方差组（GPQA σ=1.48，AlpacaEval σ=1.24，IFEval σ=0.88）被明确标注，数据使用者可以据此判断结论的统计可靠性（p.41）。

**潜在问题 1——Table 22 的单次运行局限。** Table 22 本身附注了「evaluations are from one run only」，即 SFT/DPO/RL 四条路径的比较仅基于单次实验，缺乏跨种子置信区间。考虑到 AIME 2024 的评测方差为 0.54，而表中 SFT+DPO 与 SFT+RLVR 的 Avg 差距仅 0.8pp（72.7 vs 71.9），此处结论的统计显著性存疑。论文作者承认这一局限，但未提供解决方案。

**潜在问题 2——中训练混合 ablation 使用了中间 checkpoint。** Table 6（候选混合对比）和 Table 10（指令/思维链数据效果）均在「中间预训练 checkpoint」而非最终 32B 基座上进行，且 Round 1/3 未做去污染、只有 Round 5 做了去污染（p.29）。这意味着 Round 5 相对早期版本的增益被系统性低估——真实收益可能更大，但具体大多少无法精确量化。

**潜在问题 3——Instruct 与 Think 对比中的基线选择。** 在论文 Main Results for Olmo 3 Instruct 章节的 Table 25 中，Olmo 3.1 Instruct 32B 与 Qwen 3 32B No-Thinking 的 AIME 2025 对比（57.9 vs 21.3，差距 +36.6pp），需注意 Qwen 3 No-Thinking 本身并非面向复杂推理优化的配置；而 IFBench 对比（39.7 vs 31.3）的差距则更能反映 Instruct 模型在指令遵循上的真实优势（Key Findings，p.57）。不同 benchmark 上选择不同对比对象的习惯在整篇论文中均有出现，读者应结合具体任务设置加以审视。

**潜在问题 4——评测套件选择的自我有利偏差。** OlmoBaseEval 是团队自行构建的基础评测套件，用于指导开发决策；论文同时保留了 BBH、MMLU Pro 等作为「held-out」评测集（在发布前未用于决策）。然而，held-out 评测集与开发套件之间并非完全无重叠（p.41 脚注 24 也承认 RULER 和 HELMET 存在部分重叠），这意味着「held-out」的隔离程度有限。另一个值得注意的点是：post-training 评测套件（Table 14 所用）与 base model 评测套件（Table 2 所用）是两套不同的指标体系，且 post-training 套件中包含多个通过 32 次采样取均值的高难度基准（AIME 2024/2025 各 32 次采样），这显著降低了高方差评测的随机噪声，但也意味着评测成本极高，不利于与资源有限的外部研究者进行公平复现。

**潜在问题 5——长上下文基准的测试集污染风险。** 论文使用 RULER 作为长上下文配方开发的主指标，HELMET 作为保留评测。RULER 是合成基准（Needle-in-a-Haystack 变体），其数据内容与预训练数据无重叠，污染风险极低。但 HELMET 包含真实文档摘要和 in-context learning 任务，其文档来源（如 arXiv 论文、Wikipedia）与 olmOCR 科学 PDF 数据池存在一定语义重叠——这并不意味着答案被记忆，但可能影响 in-context 任务中的先验分布，使 HELMET 分数部分反映预训练分布匹配而非纯粹的长程理解能力。Olmo 3 32B 在 RULER@65K 上达到 79.70，接近 Qwen 2.5 32B 的 80.73（用了约 8 倍更多的长上下文训练 token），但 HELMET 分数的绝对对比需要以上述视角加以保留（p.33, Table 12）。

**综合判断。** 在完全开放（fully-open）这一约束条件下，Olmo 3 展示的结果具备较高可信度。量化评估的可信度基础有三：第一，去污染流程透明可复现（decon 工具包开源）；第二，spurious-reward 验证实验直接排除了数据泄露带来的虚假 RL 收益；第三，评测配置（温度、采样次数、最大 token 数）完整公开（Table 16，p.40-41）。主要的可信度风险集中在两处：小规模消融的单次运行（Table 22）使统计显著性无法完全确认；不同阶段使用不同中间 checkpoint 进行消融（Table 6、Table 10）导致各轮增益的量级不直接可比。这两点在资源受限的开放研究中较为普遍，并非刻意规避，且论文本身均有注释说明，透明度相对较高。

Figure 2 所展示的完整模型流图（从预训练 → 中训练 → 长上下文扩展 → SFT → DPO → RL）和 Figure 1 所呈现的纵向进展曲线（基础评测与后训练评测双维度对比），共同构成了贯穿整个实验体系的一致性视觉证据：每一条折线的斜率、每一个阶段的相对位置，都与文中各消融实验的结论方向相互印证，使得各模块的贡献归因具有相对可靠的内部逻辑链条。相较于同期仅发布权重和结果表格的工作，Olmo 3 的实验透明度在完全开放模型中处于最高水平。




#### 专家批判

##### 隐性成本 (Hidden Costs)

论文在 Costs（Section 2.4）给出了成本数字，但若仔细拆解，隐性代价远超表面：

1. **总计约 56 天、1024 块 H100 GPU、折合约 $2.75M**——这是"最优 recipe"的执行成本，不含研发探索阶段的消耗：5 轮 integration test（每轮需训练 100B 中训 + SFT 评估）、80+ 次数学 microanneal、4 个 SFT 学习率 sweep（256 GPU × 36 小时）、以及多轮 DPO 超参扫描（64 GPU × 18 小时/次）。真实 R&D 成本估计是公开数字的 3–5 倍。Olmo 3.1 Think 的扩展 RL 又追加了 **21 天 × 224 GPU**，使这条线上的边际成本继续攀升。

2. **RL 阶段推理/训练节点比高达 5:1（32B）乃至 14:1（7B）**：8 个训练节点 vs. 20 个推理节点（32B），每步训练平均 **1000 秒中只有 125 秒**在真正计算梯度，其余时间在等待 rollout。有效 GPU 利用率不足 15%，大量算力被消耗在自回归推理的漫长等待中。这意味着若要将 OlmoRL 扩展到 70B+ 规模，推理节点数将成为第一约束，而非训练显存。

3. **数据工程的隐性复杂度**：3 轮 conditional mixing 需要训练数十个 30M-parameter proxy model（每个 3B tokens 5×Chinchilla 规模），共 480 个 topic-quality 子集；PII 过滤流水线用 Gemma 3 12B 对 **1.48 亿 PDF 文档**逐一进行类型分类；decon 去污染工具在首版中对 SQuAD v2（短问格式）和 DROP（问答分离格式）均失效，需要多轮人工审查修复。这些隐性人力投入无法被 $2.75M 数字捕捉。

##### 工程落地建议

**最大的坑在于中训数据的领域权衡是不可逃避的帕累托约束。** Table 7 明确展示：将 math/code/thinking 比例大幅提升的 mix 使 MCQA 和 GenQA 各下降 5–10pp；反之 Gen-QA skewed mix 使 Math 跌幅超过 20pp。在业务场景中，如果只关心代码能力而激进地往 code 方向倾斜，通用能力的损失会在 RLVR 阶段被放大——因为 RL 数据中混有通用 chat，而 base 的 GenQA 能力不足会直接损害 LM judge 奖励信号的质量，形成隐性的反馈回路。

**特殊 token 的时序问题是复现中最容易踩的坑**：若在中训数据中保留 `<|im_start|>` 等 chat template token，base 模型会在推理时自发输出这些 token，导致 GSM8K 从 49.4 骤降至 0（Section 3.5.4）。必须在中训阶段用双换行替代特殊 token，等到 SFT 阶段才引入 chat template。这个陷阱几乎不会出现在任何论文的 abstract 或 method 章节，但实际工程中极易遇到。

**Delta Learning 的有效性高度依赖 chosen/rejected 模型的能力差幅度。** 论文选用 Qwen3-32B（顶级推理模型）vs. Qwen3-0.6B（入门模型），能力差约 48pp（Table 21）。若两个对比模型能力相近，delta 过小，DPO 梯度将退化为噪声，效果反而不如直接 SFT。随着自研模型能力迭代提升，如何持续维持足够大的 chosen-rejected 差是一个开放工程问题。

##### 关联思考

**与 LoRA 的结构性冲突**：OlmoRL 的 inflight 权重更新依赖将完整的 bf16 权重矩阵直接推送到 actor vLLM 实例，这与 LoRA 的低秩增量结构不兼容——无法在不重建完整权重的情况下做 inflight 同步。因此，在显存受限场景中尝试用 LoRA+OlmoRL，将丧失最核心的 4× 吞吐收益，使长 RL 训练重新变得不可行。

**与 FlashAttention/SWA 的协同与约束**：OLMo 3 采用 3/4 层 SWA（window=4096）+ 最后一层 full attention 的非对称架构，YaRN 仅应用于 full attention 层（Figure 13a 验证这是最优选择）。这一设计使长上下文训练显存占用显著降低，但要求 context parallelism 的 all-gather 策略必须区分两类 attention 层的掩码，实现复杂度高于标准 full-attention 长上下文方案。直接套用开源 YaRN patch（通常对所有层一视同仁）会导致性能下降。

**与 MoE 架构的定位差异**：Olmo 3 坚持 dense 架构（7B/32B），这在推理效率上处于劣势（active params/总 params = 100% vs. MoE 典型的 15–25%），但在 RL-Zero 研究范式中有不可替代的价值——在 dense 且数据完全透明的前提下，研究者可以精确追踪"预训练数据分布如何影响 RLVR 效果"（Olmo 3 RL-Zero 从 Base 直接做 RL，AIME 2024 pass@1 从约 20% 升至约 50%）。MoE 封闭模型因路由专家分配的不透明性，无法提供同等质量的实验控制。

**Reward hacking 的潜在风险**：Figure 21 显示，在混合数据上训练时各域的 train reward 均低于单域专项训练，论文将此解读为"混合数据抑制了过拟合"。但这也可能意味着：混合 reward 信号相互干扰，模型未能充分利用每个域的奖励结构，而非真正的泛化改善。Olmo 3.1 Think 的扩展 RL（750→2300 steps）仍有提升且未饱和，但论文缺乏超过 2300 steps 后 reward hacking 行为的分析——这是部署长周期 RL 训练时最需要警惕的未知风险。


#### 机制迁移分析

##### 机制解耦 (Mechanism Decomposition)

| 原语名称 | 本文用途 | 抽象描述 | 信息论/几何直觉 |
|---------|---------|---------|---------------|
| **渐进式课程数据调度** | 预训→中训→长上下文三阶段，各阶段独立混合比例；中训 100B tokens 将 Math 从 23.5→59.8，Code 从 19.8→31.9 | 将目标分布分解为多个从易到难的子分布序列，每阶段用精选子集引导参数向目标流形逐步靠近 | KL 散度视角：每阶段数据分布与当前模型分布的 KL 散度受控缩小；避免一次性大 KL 跳跃导致的灾难遗忘 |
| **Delta Learning DPO（质量差最大化对比）** | Think DPO 阶段：chosen=Qwen3-32B thinking traces，rejected=Qwen3-0.6B thinking traces；直接 SFT chosen 反而 −5.8pp，DPO 获 +2.6pp | 选取质量极差最大的正负对做偏好学习：chosen 来自能力强模型，rejected 来自同提示下能力弱模型的回答 | 互信息视角：quality gap 越大，偏好梯度信号越显著，噪声信噪比越高；SFT 饱和后仍能从对比分布中提取有效信息 |
| **OlmoRL 异步 Inflight 权重更新** | RL 训练时生成节点持续异步接收最新 policy 权重，无需等待完整同步；relative to continuous batching alone +117% 吞吐，整体达 2949 tok/s | 将策略网络权重更新与样本生成解耦为异步流水线；生成节点使用稍旧权重采样，训练节点同步梯度更新 | 重要性采样视角：引入截断 IS ratio ρ 补偿权重滞后引起的分布偏移；以轻微方差换取大幅吞吐提升 |
| **质量感知上采样（Quality-Aware Upsampling）** | 预训练时对 web 文本按质量分位数设置单调递增的重复因子（最高 7×），而非阶跃式截断过滤；底部 40% 剔除，顶部 5% 重复 7× | 在固定 token 预算下，将数据集的"有效质量密度"从均匀分布调整为按质量排列的凸曲线分布 | 最大化训练分布与高质量子集分布之间的 KL 散度减少；等价于对 token 赋予与质量分位数单调相关的重要性权重 |

##### 迁移处方 (Transfer Prescription)

**原语 1：渐进式课程数据调度**

- **目标领域 + 具体问题：** 推荐系统中的多兴趣序列建模——从通用点击行为预训练到垂类精排微调，直接在小样本精排数据冷启动导致欠拟合。
- **怎么接：** 第一阶段用全域行为日志（通用）预训 Embedding 层；第二阶段用高质量精排场景数据（类比中训）做 100B 步课程微调；第三阶段用长会话序列（类比长上下文扩展）扩展序列编码器的位置感知范围。替换现有"单阶段端到端"训练方案。
- **预期收益：** 逐步收窄训练分布与目标场景分布的 KL 散度；每阶段可独立评估，避免单阶段欠拟合或过拟合。
- **风险：** 若各阶段数据边界不清晰，中间阶段可能引入负迁移；阶段间超参（LR、batch size）需单独调优，工程复杂度上升。

**原语 2：Delta Learning DPO**

- **目标领域 + 具体问题：** 代码生成模型 SFT 后能力瓶颈——用同级别模型输出继续 SFT 无法提升 pass@1，需要在不增加 SFT 数据质量上限的前提下突破边界。
- **怎么接：** 输入为编程题 prompt 池；chosen = 大模型（如 GPT-4.1）生成的正确代码，rejected = 同 prompt 下小模型（如 Qwen-0.5B）生成的错误/低效代码。替换现有 DPO pipeline 中人工标注或 UltraFeedback 式均质对生成步骤。
- **预期收益：** 自动获取质量差最大的对比对，信噪比高；在 SFT 饱和后仍可拓展能力边界（本文实测 DPO 阶段 pass@K on AIME 显著优于 SFT）。
- **风险：** rejected 质量过低可能导致 DPO 退化为"学会避免明显错误"而非"学会正确推理"；需控制 chosen-rejected gap 在合理范围内（过大则 OOD，过小则梯度饱和）。

**原语 3：OlmoRL 异步 Inflight 权重更新**

- **目标领域 + 具体问题：** 任何需要大规模在线 RL 的生成模型（对话 RLHF、图像生成 RLHF），现有同步 PPO/GRPO 的"生成→等待→更新"串行导致 GPU 严重空闲。
- **怎么接：** 将生成池与训练节点完全解耦：生成池持续采样，训练节点持续更新并将权重差值推送给 actor；actor 接收新权重后立即继续生成，无需清空 KV cache。引入截断 IS ratio（ρ 截断）作为理论收敛保证。替换现有 vLLM + 同步训练的调度层。
- **预期收益：** GPU 利用率大幅提升（本文实测 +117% 吞吐）；训练墙钟时间显著缩短，长 RL 实验可行性提高。
- **风险：** IS ratio 截断引入额外超参 ρ；权重滞后程度需与截断强度匹配，过大滞后可能导致策略偏移过快，需监控 behavior policy 与 target policy 的 KL 散度。

##### 机制家族图谱 (Mechanism Family Tree)

**前身 (Ancestors):**
- **GRPO (Shao et al., 2024)：** OlmoRL 的直接算法基础；group relative policy optimization 去掉了 value network 需求，OLMo 3 在此基础上去掉 KL 正则项和标准差归一化，修正了对简单/困难问题的难度偏差。
- **DAPO (Yu et al., 2025)：** 贡献了零梯度过滤和 token 级 loss 归一化；OLMo 3 在此基础上叠加 inflight 权重更新和主动采样，进一步提升工程效率。
- **Dr.GRPO (Liu et al., 2025b)：** 同期独立提出去掉标准差归一化以消除难度偏差；OLMo 3 的 advantage 公式 Aᵢ,ₜ = r(x,yᵢ) − mean({r}) 与之几乎同构。
- **Delta Learning (Geng et al., 2025)：** 核心 DPO 数据构造原则——"chosen-rejected 质量差决定学习效率"；OLMo 3 将其系统化为 Dolci Think/Instruct DPO 流水线。
- **Model Souping (Wortsman et al., 2022)：** 权重空间线性平均的理论基础；OLMo 3 将其应用到中训多 seed 合并（32B Math +2.9pp）和长上下文扩展末尾三个 checkpoint 平均。
- **Tülu 3 (Lambert et al., 2024)：** SFT+DPO+RL 三段式后训练流水线的先行实践；OLMo 3 在此基础上增加 Delta Learning DPO 并将 RL 扩展至多领域（IF、chat、code）。

**兄弟 (Siblings):**
- **DeepSeek R1 (Guo et al., 2025)：** 同期大规模 RLVR 思维模型，能力对标；区别在于 OLMo 3 完全开放数据、中间 checkpoint 和训练代码。
- **Qwen 3 (Yang et al., 2025)：** 同期 SFT+DPO+RL 三阶段 thinking 模型，无 base model 公开发布，训练数据不公开；OLMo 3 用约 1/6 训练量追平其 32B 推理性能。
- **Stanford Marin 32B (Hall et al., 2025)：** 同期全开放 base 模型，使用 model souping，但无长上下文扩展阶段；OLMo 3 Base 32B Math 超出 Marin 32B +12.6pp。

**后代 (Descendants):**
- **OLMo 3.1（本文 Extended RL 阶段）：** 将 RL 步数从 750 扩展到 2300，AIME 2024 +3.8pp，AIME 2025 +5.6pp，IFBench +20.5pp；是 OLMo 3 的直接演进，证明 RL 训练远未饱和。
- **Dolci RL-Zero：** OLMo 3 释放的完全开放 RL-Zero 数据集和基准，为"预训练数据影响 RLVR 效果"这一研究方向提供受控实验平台，预计成为后续 RL 算法比较的标准基准。

**创新增量定位：** OLMo 3 在机制族谱中的核心增量不在单一算法突破，而在于**将渐进式课程调度、异步 RL 基础设施、Delta DPO 三个原语整合成可完全复现的端到端流水线**，并以全开放方式释放每阶段中间检查点——这是同期所有竞争模型（DeepSeek R1、Qwen 3）均未提供的。Figure 2 中多产品线分叉结构正是这种"可插拔流水线"的体现：Think、Instruct、RL-Zero 三条线共享同一 Base，分叉点完全透明。



#### 背景知识补充

**SWA（Sliding Window Attention，Beltagy et al., 2020）：** OLMo 3 在前 3/4 层使用 window=4096 的滑动窗口注意力，仅最后一层保留全注意力（full attention）。这是对 Mistral/Gemma 系列 SWA 设计的沿用，目的是在保持长程依赖感知能力的同时大幅降低 KV cache 显存占用。YaRN 在长上下文扩展时仅应用于全注意力层而非 SWA 层，是 OLMo 3 通过 Figure 13a 消融实验确定的最优策略。

**olmOCR（Poznanski et al., 2025）：** Allen AI 开发的科学 PDF 线性化工具，将扫描或排版复杂的学术 PDF 转为高质量纯文本。Dolma 3 中 13.6%（805B tokens）学术 PDF 数据均来源于此，其中超过 22.3M 篇文档长度超过 8K tokens，是 OLMo 3 长上下文数据池的主干，也是 OLMo 3 Base 在科学知识类 benchmark 上超越同量级竞争者的关键数据基础设施。

**Active Sampling（主动采样）：** OlmoRL 对标准 GRPO 的重要工程改进——在 RL 训练中动态过滤"全组样本优势为零"的 batch（即所有 response reward 相同，GRPO 梯度为零的情况），并持续补充新样本维持 batch 大小。实验表明（Figure 26）主动采样维持了 >90% 非零优势 batch 比例，而标准 GRPO 随训练进行 batch 质量持续退化，有效梯度信号逐渐消失。
