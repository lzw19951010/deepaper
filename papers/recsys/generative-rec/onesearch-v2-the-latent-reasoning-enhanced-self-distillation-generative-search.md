---
abstract: 'Generative Retrieval (GR) has emerged as a promising paradigm for modern
  search systems. Compared to multi-stage cascaded architecture, it offers advantages
  such as end-to-end joint optimization and high computational efficiency. OneSearch,
  as a representative industrial-scale deployed generative search framework, has brought
  significant commercial and operational benefits. However, its inadequate understanding
  of complex queries, inefficient exploitation of latent user intents, and overfitting
  to narrow historical preferences have limited its further performance improvement.
  To address these challenges, we propose \textbf{OneSearch-V2}, a latent reasoning
  enhanced self-distillation generative search framework. It contains three key innovations:
  (1) a thought-augmented complex query understanding module, which enables deep query
  understanding and overcomes the shallow semantic matching limitations of direct
  inference; (2) a reasoning-internalized self-distillation training pipeline, which
  uncovers users&#39; potential yet precise e-commerce intentions beyond log-fitting
  through implicit in-context learning; (3) a behavior preference alignment optimization
  system, which mitigates reward hacking arising from the single conversion metric,
  and addresses personal preference via direct user feedback. Extensive offline evaluations
  demonstrate OneSearch-V2&#39;s strong query recognition and user profiling capabilities.
  Online A/B tests further validate its business effectiveness, yielding +3.98\% item
  CTR, +3.05\% buyer conversion rate, and +2.11\% order volume. Manual evaluation
  further confirms gains in search experience quality, with +1.65\% in page good rate
  and +1.37\% in query-item relevance. More importantly, OneSearch-V2 effectively
  mitigates common search system issues such as information bubbles and long-tail
  sparsity, without incurring additional inference costs or serving latency.'
arxiv_categories:
- cs.IR
arxiv_id: '2603.24422'
authors:
- Ben Chen
- Siyuan Wang
- Yufei Ma
- Zihan Liang
- Xuxin Zhang
- Yue Lv
- Ying Yang
- Huangyu Dai
- Lingtao Mao
- Tong Zhao
- Zhipeng Qian
- Xinyu Sun
- Zhixin Zhai
- Yang Zhao
- Bochao Liu
- Jingshan Lv
- Xiao Liang
- Hui Kong
- Jing Chen
- Han Li
- Chenyi Lei
- Wenwu Ou
- Kun Gai
baselines:
- OneSearch-V1
- Standard GRPO
- PARS (reward model)
- Listwise DPO
- CODI (hidden-state L1 alignment)
- EMA-mode distillation
- Joint-mode distillation
- Special-token distillation
- Direct CoT injection (ablation)
category: recsys/generative-rec
code_url: https://github.com/benchen4395/onesearch-family
core_contribution: new-framework
datasets:
- Kuaishou Mall Search Platform (5M clicked query-item pairs for training; 30k PV
  test set with 30k clicks and 7229 orders)
date: '2026-03-25'
doi: null
keywords:
- generative search
- knowledge distillation
- self-distillation
- reinforcement learning from human feedback
- query understanding
- chain-of-thought
- e-commerce recommendation
- GRPO
- preference alignment
- cold-start items
metrics:
- HR@10 (Order)
- HR@10 (Click)
- MRR@10 (Order)
- MRR@10 (Click)
- ItemCTR
- PVCTR
- PVCVR
- BuyerConversionRate
- OrderVolume
- GMV
- SIDRate
- PageGoodRate
- QueryItemRelevance
publication_type: preprint
status: complete
tags:
- generative-search
- knowledge-distillation
- reinforcement-learning
- query-understanding
- chain-of-thought
- e-commerce
- preference-alignment
- GRPO
title: 'OneSearch-V2: The Latent Reasoning Enhanced Self-distillation Generative Search
  Framework'
tldr: OneSearch-V2通过思维增强查询理解、推理内化自蒸馏和行为反馈偏好对齐三项创新，在快手商城搜索中实现GMV+3.45%、订单量+2.11%的显著在线收益。
url: https://arxiv.org/abs/2603.24422
venue: null
---

## 核心速览 (Executive Summary)

## TL;DR

OneSearch-V2（快手技术，arXiv 2603.24422，2026年3月）在生成式电商搜索领域提出了一套**推理内化**框架：让LLM在训练时借助离线生成的关键词CoT作为「教师」，在推理时不依赖任何额外输入即可复现教师的推理质量，同时通过细粒度Token-Position奖励对齐用户真实行为反馈。在线A/B测试中，GMV提升3.45%，订单量提升2.11%。

## 一图流

```
离线阶段
  查询 q → LLM CoT → 关键词 kw（缓存，零推理延迟）
                           ↓
训练阶段（SDFT）
  教师路径: (uid, q, SID序列, kw) → LLM → logits^T
  学生路径: (uid, q, SID序列      ) → LLM → logits^S  ← 同一模型，权重共享
  损失: L_CE + α_KL·KL(T‖S) + α_R·R-Drop + L_adv(FGM) + FocalLoss
                           ↓
推理阶段
  仅用学生输入 → 已内化关键词推理的LLM → 生成SID序列
                           ↓
TPMA-GRPO阶段
  前缀门控奖励 R_{i,l} → 位置级优势 Â_{i,l} → 细粒度策略梯度
  复合奖励: R_Rel（相关性）+ R_CTR（点击）+ R_C&O（转化&订单）
```

## 核心机制一句话

用**同一模型扮演教师和学生**，通过KL散度让学生在缺少关键词输入时仍能匹配教师的输出分布，从而将离线关键词知识以「隐式推理」的形式永久固化在模型权重中，推理期零成本获得CoT增益。

---

## 动机与第一性原理 (Motivation & First Principles)

## 痛点（Pain Points）

**OneSearch-V1的三个核心缺陷**：

1. **查询理解浅层化**：V1直接将原始查询作为输入，缺乏对意图的深度语义分析，对长尾查询和冷启动商品的泛化能力弱。实验显示直接拼接CoT（+directCoT）会使Order HR@10从0.2046灾难性下降至0.0898，说明朴素CoT不能直接使用。

2. **知识利用效率低**：即便离线有丰富的关键词/意图信息，如何在不增加推理延迟的前提下让模型利用这些信息是工程难题。额外的在线关键词生成模块意味着额外的延迟和服务成本。

3. **奖励信号粗粒度**：标准GRPO对序列中每个位置施加相同的序列级优势估计，忽视了「商品ID前几位token更关键」的结构先验，导致奖励信号对早期生成位置的引导不足。

## 核心洞察（Key Insights）

**因果链推导**：

- A：SID序列生成具有严格的层次因果结构（前缀→细粒度属性）
- → B：前缀token的正确性对最终检索结果影响更大，应获得更强的优化信号
- → C：位置差异化的优势估计（TPMA）比均匀序列级优势（标准GRPO）更有效

- A：关键词CoT提供丰富的语义信号，但在线生成代价高昂
- → B：若将关键词蒸馏为模型内部参数，则推理时无需关键词
- → C：信息不对称自蒸馏（Self-mode，共享权重）可将「理解关键词的能力」内化为「无关键词推理能力」

## 直觉解释

想象一个学生备考：教师有「考试答案手册（关键词）」，学生没有。通过让学生的答题分布（logits分布）不断向教师靠拢（KL散度），学生被迫「悟出」答案手册背后的逻辑，而不只是死记硬背（交叉熵）。考试时（推理时），手册收走了，但学生已经内化了推理模式，仍能超越原始基线。

这也解释了为什么自蒸馏后学生甚至**超越了教师**（Self-Distill(S) > Base(T)）：蒸馏过程中，优化目标是「学生在信息缺失时仍能预测准确」，这比直接带关键词预测要求更高，强迫模型建立更鲁棒的内部表征。

---

## 方法详解 (Methodology)

## 直觉版（Intuitive Overview）

OneSearch-V2的核心思路是**「离线赚钱，在线花钱」**：
- 离线：用大模型（Qwen3-32B）生成查询的关键词CoT，缓存起来，零在线成本。
- 训练：同一个小模型同时扮演「看过关键词的教师」和「看不到关键词的学生」，通过KL蒸馏让学生内化教师的推理能力。
- 强化：用用户真实行为（点击、转化、订单）作为奖励，通过细粒度位置级优势引导模型更好地生成商品ID前缀。

旧方法（OneSearch-V1）数据流：`raw query → 直接生成SID → PARS奖励模型排序`

新方法（OneSearch-V2）数据流：`raw query → [训练时+关键词教师] → KL蒸馏 → [推理时无关键词] → TPMA-GRPO用行为反馈对齐`

---

## 精确版（Formal Specification）

### Innovation 1: Thought-Augmented Query Understanding

**三步CoT流程**（离线，结果缓存为 `kw`）：

```
Step 1: Query Analysis    → 意图理解、类目识别、属性抽取、话题推荐
Step 2: Keyword Extraction → 根据约束提取高精度搜索关键词列表（按商品流行度排序）
Step 3: Preference Calibration → 结合用户历史行为序列校准偏好，过滤或补充关键词
```

**关键设计**：意图类型分四种（商品搜索/功能需求/问答/否定偏好），非商品搜索意图提前终止，专用引擎处理。对否定型查询（如「缓解疲劳，不要补剂」）、疑问型查询（「游泳必备品？」）尤为有效。

---

### Innovation 2: Reasoning-Internalized Self-Distillation (SDFT)

输入特征定义：
- `uid`: 用户ID
- `q`: 查询文本
- `SID_q`, `Seq_q`, `Seq_short`, `Seq_emb`: 查询SID和用户行为序列（多粒度）
- `kw`: 离线生成的关键词CoT（仅训练时教师可见）

**教师输入**：`x^T = (uid, q, SID_q, Seq_q, Seq_short, Seq_emb, kw)`
**学生输入**：`x^S = (uid, q, SID_q, Seq_q, Seq_short, Seq_emb)` （无 kw）

**KL蒸馏损失**：
```
L_KL = (1/|V|) · Σ_{t∈V} KL(softmax(z^T_t/τ) ∥ softmax(z^S_t/τ)) · τ²
```
其中 τ=1.0（论文设置），|V| 为有效非padding token位置集合，τ² 为温度补偿项。

**R-Drop损失**（双向KL，增强预测稳定性）：
```
L_R-Drop = (1/2)[KL(P1 ∥ P2) + KL(P2 ∥ P1)]
```
其中 P1, P2 为同一学生输入的两次独立dropout前向传播结果。

**FGM对抗训练**（平滑embedding空间）：
```
δ = ε · ∇_e L_base / ‖∇_e L_base‖₂   （ε=0.6）
L_adv = CE(model(x^S + δ), y) + α_KL · KL_loss_on_perturbed_input
```

**总训练目标**：
```
L_SDFT = L_CE + α_KL · L_KL + α_R · L_R-Drop + L_adv
         （α_KL=0.1, α_R=0.5）
```
加上 **Focal Loss** 替换 CE 处理长尾类别不平衡（α=2, γ=3）。

**数值推演示例**（τ=1，简化为3个候选token）：
```
教师 logits^T = [3.0, 1.0, -1.0] → softmax → [0.844, 0.114, 0.042]
学生 logits^S = [2.0, 1.5, -0.5] → softmax → [0.587, 0.356, 0.057]

KL(teacher ∥ student) = 0.844·log(0.844/0.587) + 0.114·log(0.114/0.356) + ...
                      ≈ 0.844·0.362 + 0.114·(-1.138) + 0.042·(-0.303)
                      ≈ 0.305 - 0.130 - 0.013 ≈ 0.162

学生被迫增大第一个token的概率（向教师靠拢），
从0.587逐渐向0.844收敛，即使没有看到关键词。
```

**伪代码**（PyTorch风格，简化关键逻辑）：
```python
for batch in dataloader:
    x_T = (uid, q, sid_q, seq_q, seq_short, seq_emb, kw)  # [B, L_T]
    x_S = (uid, q, sid_q, seq_q, seq_short, seq_emb)       # [B, L_S]
    y   = target_sids                                        # [B, L_out]

    # 教师前向（无梯度）
    with torch.no_grad():
        z_T = model(x_T, labels=y)   # [B, L_out, V]

    # 学生前向 pass 1
    z_S1 = model(x_S, labels=y)     # [B, L_out, V]

    # 基础损失：CE + KL蒸馏
    L_CE  = focal_loss(z_S1, y)
    L_KL  = kl_divergence(z_T.detach(), z_S1, tau=1.0)
    L_base = L_CE + alpha_kl * L_KL

    # R-Drop：学生第二次前向（不同dropout mask）
    z_S2 = model(x_S, labels=y)     # [B, L_out, V]
    L_rdrop = 0.5 * (kl(z_S1, z_S2) + kl(z_S2, z_S1))  # 对称KL

    L_base_full = L_base + alpha_r * L_rdrop
    L_base_full.backward()           # 计算embedding梯度

    # FGM：扰动embedding空间
    delta = epsilon * emb.grad / (emb.grad.norm() + 1e-8)
    emb.data += delta
    z_adv = model(x_S, labels=y)    # [B, L_out, V]
    L_adv = focal_loss(z_adv, y) + alpha_kl * kl_divergence(z_T, z_adv, tau=1.0)
    L_adv.backward()
    emb.data -= delta               # 恢复embedding

    optimizer.step()
    optimizer.zero_grad()
```

---

### Innovation 3: TPMA-GRPO

**复合奖励**：`R_item = R_C&O + R_CTR + R_Rel`（加法组合，避免稀疏问题）
- `R_C&O`：若rollout SID对应已购商品得v_o=3，点击商品得v_c=4
- `R_CTR`：calibrated后验CTR，clip至(0,1)
- `R_Rel`：相关性分级奖励（0-3级）

**前缀奖励**（L=5 SID tokens，编码5层从粗到细）：
```
R_{i,l} = max_{t∈T} Σ_{k=1}^{l} [o_{i,k} = t_k] · ΔR_{i,l}

ΔR_{i,l} = 2  if l < 3   （前缀决定大类，权重更高）
ΔR_{i,l} = 1  if 3 ≤ l < L  （细粒度属性，权重较低）
```

**位置级优势估计**（独立归一化）：
```
Â_{i,l} = (ΔR_{i,l} - mean_j(ΔR_{j,l})) / (std_j(ΔR_{j,l}) + δ)
```

**前缀门控**（阻断错误前缀后的梯度）：
```
g_{i,l} = 1  if l=1 或 R_{i,l-1} > 0  （前缀正确则开门）
g_{i,l} = 0  if R_{i,l-1} = 0         （前缀错误则关门，阻断下游梯度）
```

**最终TPMA-GRPO损失**：
```
L_TPMA = -(1/G) Σ_i (1/L) Σ_l g_{i,l} · r_{i,l} · Â_{i,l}^final

Â_{i,l}^final = Â_{i,l} + w_item · Â_i^item
r_{i,l} = π_θ(o_{i,l}|x_u, o_{i,<l}) / π_θ_old(o_{i,l}|x_u, o_{i,<l})
```
注意：故意省略了标准GRPO的概率比裁剪，因为前缀门控已提供自然的梯度正则化。

---

## 设计决策（Design Decisions）

| 决策点 | 选择 | 被排除的方案 | 理由 |
|--------|------|-------------|------|
| 蒸馏架构 | Self-mode（权重共享） | EMA-mode / Joint-mode | 权重完全共享，梯度仅来自学生路径，使模型优化偏向信息缺失鲁棒性 |
| 知识对齐层 | KL散度（output logits层） | CODI L1（hidden state层） | KL捕获完整输出分布；L1只对齐中间激活，联合使用反而损害性能（Table 11：CODI+Proj+SD < Self-Distill alone） |
| CoT注入方式 | 离线缓存+蒸馏 | 直接拼接（+directCoT） | 直接拼接使Order HR@10从0.2046→0.0898（-56%），因为SID和文本CoT的表示空间异质性导致混乱 |
| SID编码 | Unimodal KHQE | Multimodal（图文联合） | Table 1：unimodal KHQE Recall@10=0.2542，远超最佳multimodal方案0.2389；多模态图文噪声压制核心属性 |
| 优势粒度 | 位置级TPMA | 序列级标准GRPO | SID前3位token决定大类归属，精确匹配信号不应等同于后续细粒度token |

## 易混淆点（Common Confusions）

1. **❌ Self-Distillation = 自监督学习**
   **✅** 这里「self」指教师和学生使用**同一套权重**（self-mode），而非「无标签」自监督。教师的监督信号来自关键词增强输入的前向传播，有明确的训练标签。

2. **❌ 学生超越教师是实现上的Bug**
   **✅** Self-Distill(S) > Base(T)是有理论依据的：蒸馏的KL损失强制学生在信息缺失时仍能预测正确，等价于训练了一个更鲁棒的底层表征，消除了对关键词的捷径依赖，反而泛化更好（Born-again Networks现象）。

3. **❌ TPMA中的「前缀门控」等同于标准PPO的裁剪机制**
   **✅** 前缀门控是基于**结构先验**（前缀正确性）的梯度屏蔽，而PPO裁剪是基于**概率比幅度**的梯度约束。前缀门控当前缀完全错误时将梯度直接归零，语义更明确，而非连续衰减。

---

## 实验与归因 (Experiments & Attribution)

## 核心收益（Key Results）

### 离线评估（Table 5，30k PV测试集）

| 指标 | OneSearch-V1基线 | OneSearch-V2 | 相对提升 |
|------|----------------|-------------|--------|
| Order HR@10 | 0.2046 | 0.2314 | **+13.1%** |
| Order MRR@10 | 0.0985 | 0.1151 | **+16.9%** |
| Click HR@10 | 0.2231 | 0.2568 | **+15.1%** |
| Click MRR@10 | 0.0728 | 0.0833 | **+14.4%** |

### 在线A/B测试（Table 9）

| 业务指标 | V2_RAG | V2_Reason | V2_Full |
|---------|--------|-----------|--------|
| ItemCTR | +0.52% | +2.59% | **+3.98%** |
| PVCVR | +0.63% | +2.21% | **+2.90%** |
| 订单量 | +1.07% | +1.57% | **+2.11%** |
| GMV | — | — | **+3.45%** |

所有在线结果均通过统计显著性检验（P<0.05）。

### 细分场景分析（Figure 6）
- 冷启动商品 ItemCTR: **+6.16%**（最大获益）
- 热门商品 ItemCTR: +4.81%
- 长尾查询 CTR: **+5.37%**
- 高频查询 CTR: +5.01%
- 低活跃用户：显著提升（具体数值未列，图中可见明显增益）

---

## 归因分析（Ablation Attribution）

**组件贡献排序**（按单独增量，基于Table 5、6）：

1. **Self-Distillation（SDFT）**：+1.17% Order HR@10，+1.67% Click HR@10 ← **最大单项贡献**
2. **TPMA-GRPO vs 标准GRPO**：MRR@10额外提升，精排质量改善明显
3. **FocalLoss**：Click HR@10 +0.73%，Long-tail类别显著改善（SIDRate从98.xx→99.00%+）
4. **R-Drop**：Order MRR@10 +0.28%，预测稳定性增强
5. **FGM**：Order HR@10 +0.12%（叠加自蒸馏后），输入鲁棒性改善
6. **R-Drop+FGM+FocalLoss 协同效应 > 各自之和**（重要发现）

**架构无关性**（Table 12-15）：BART-B / GPT-2 / Qwen3-0.6B三种骨干网络均呈相同改进模式，证明框架的通用性。

**自蒸馏内化验证**（Table 7）：
```
Base(S)无关键词:   Order HR@10 = 0.2094
Base(T)有关键词:   Order HR@10 = 0.2139  （优于无关键词，符合预期）
Self-Distill(S)无关键词: Order HR@10 = 0.2163  （超越有关键词的Base(T)！）
Self-Distill(T)有关键词: Order HR@10 = 0.2155  （反而略低于学生）
```

---

## 可信度检查（Credibility Assessment）

**支持可信度的因素**：
- 在线A/B是工业界最高标准验证，GMV+3.45%在电商场景具有直接商业意义。
- 冷启动+6.16%与FocalLoss机制高度一致，数据与方法解释相互印证。
- 多骨干网络验证排除模型特有的过拟合可能。
- 「学生超越教师」结论虽反直觉但在Self-Distillation文献中有理论支撑。

**潜在可疑点**：
- 所有数据均来自快手内部平台（无公开测试集），外部可重复性受限。
- directCoT的灾难性失败（-56%）异常严重，超参/数据处理细节未充分披露，可能影响结论的普适性。
- 复合奖励三个子信号的权重设置（v_o, v_c, R_CTR的缩放系数）未详细披露，对在线结果的可重复性有影响。

---

## 专家批判 (Critical Review)

## 隐性成本（Hidden Costs）

### 训练时成本
1. **约3×前向传播开销**：SDFT需要教师前向（no_grad，约0.5×）+ 学生前向1（1×）+ R-Drop学生前向2（1×）+ FGM扰动前向（1×）= 约3.5×标准微调的计算量。
2. **离线CoT生成基础设施**：需要Qwen3-32B规模的大模型推理服务，定期更新5M+查询的关键词缓存。热点事件/新品爆发时缓存时效性是隐患。
3. **TPMA-GRPO训练pipeline复杂度**：复合奖励依赖实时行为日志、相关性系统、CTR预估模型三路信号，对数据pipeline的工程要求极高，且各信号的数据延迟不同（行为日志有分钟级延迟）。

### 系统依赖风险
- 离线关键词缓存覆盖率决定SDFT训练质量上限，新查询（cold query）无缓存时退化为标准微调。
- R_CTR作为奖励信号容易被「标题党」商品（高点击低转化）利用，需要R_C&O的制衡，但二者权重的动态调整机制未披露。

---

## 工程落地建议（Engineering Deployment Guidelines）

### 三阶段渐进部署策略

```
Phase 1（低风险，建议先上）: SDFT + KL蒸馏
  依赖：离线CoT缓存 + 双路前向传播修改训练代码
  侵入性：最小（无需改变推理服务）
  预期：Order HR@10 +1%

Phase 2（中等复杂度）: 加入 R-Drop + FGM + FocalLoss
  依赖：调整训练超参（α_KL=0.1, α_R=0.5, γ_focal=3）
  建议：在验证集上做3-5轮超参搜索
  预期：额外 +0.5% HR@10，主要受益于长尾改善

Phase 3（高复杂度，需完整行为闭环）: TPMA-GRPO
  依赖：完整的在线行为反馈闭环 + 相关性系统集成
  前提：CTR模型AUC>0.75，行为日志延迟<5min
  风险：奖励设计不当会导致reward hacking（如高CTR低质量商品大量召回）
```

### 关键调优建议
- 前缀权重ΔR的阈值位置（l<3）应根据SID编码方案调整；若前2位已决定大类，则阈值改为l<2。
- 首先验证 Self-Distill(S) > Base(T) 的指标关系：若在你的场景中不成立，说明关键词覆盖率不足，需优先提升离线CoT生成质量。

---

## 关联思考（Related Insights）

1. **与RAG的本质差异**：RAG在推理时注入检索结果（在线成本高），V2在训练时注入关键词再「蒸馏遗忘」（零在线成本）。这是两种截然不同的「利用外部知识」哲学，V2更适合延迟敏感场景。

2. **与LoRA/PEFT的关系**：V2不修改模型架构，而是修改训练目标（多路损失）。两者正交，可以组合：用LoRA低成本适配，用SDFT提升推理能力。

3. **与DeepSeek-R1的对比**：R1用显式CoT（训练+推理均有思维链）提升推理，V2用隐式CoT（只训练有思维链，推理无）提升推理。R1适合高延迟容忍场景，V2适合在线推理延迟敏感场景，二者是同一个「推理增强」目标的不同工程权衡。

4. **前缀门控的MoE类比**：TPMA的前缀门控机制与MoE的专家门控有结构相似性：都是根据某种条件（前缀正确性 vs 路由概率）决定是否激活特定计算路径的梯度流。

---

## 机制迁移分析 (Mechanism Transfer Analysis)

## 机制解耦（Mechanism Decomposition）

| 原语名称 | 本文用途 | 抽象描述 | 信息论/几何直觉 |
|---------|---------|---------|---------------|
| **信息不对称自蒸馏** | 用关键词增强的教师输入指导无关键词的学生，共享权重 | 同一函数在不同信息状态下的输出对齐 | 将高维信息流形上的教师点映射到低维学生流形，约束学生靠近最近的教师点 |
| **离线特权信息缓存** | LLM离线生成CoT关键词，训练时注入，推理时不用 | 将昂贵的在线推理转为廉价的存储查询 | 以空间（缓存存储）换时间（推理延迟），适用于访问模式集中的分布 |
| **位置差异化优势估计** | SID前缀位置权重更高，后续细粒度位置权重更低 | 将结构先验编码进策略梯度的信用分配 | 在树状搜索空间中，根节点分支决策比叶节点更重要 |
| **前缀门控梯度屏蔽** | 前缀错误时阻断后续位置的梯度信号 | 条件依赖的梯度路由 | 因果链断裂后，下游信息失去因果解释性，不应作为训练信号 |

---

## 迁移处方（Transfer Prescription）

### 原语1：信息不对称自蒸馏

**迁移场景A：代码生成（GitHub Copilot类应用）**
- 目标：在推理时无注释的情况下生成高质量代码
- 特权信息：代码注释 + 函数签名（训练时可见，推理时不可用）
- 怎么接：教师输入 = (code_context, docstring, signature)，学生输入 = (code_context only)，KL对齐输出分布
- 预期收益：无文档注释的代码补全质量接近有注释的水平
- 风险：代码token空间比SID空间更大，KL损失的数值稳定性需要更细心的超参调整

**迁移场景B：对话系统（知识型QA）**
- 目标：推理时无需检索知识库，直接从参数中「回忆」相关知识
- 特权信息：检索到的相关文档段落（训练时注入，推理时移除）
- 怎么接：替换RAG的检索模块 → 蒸馏模块，将检索内容内化为参数知识
- 预期收益：降低在线延迟，消除检索模块的单点故障风险
- 风险：知识时效性问题（训练后的新知识无法更新），需要定期重新蒸馏

### 原语2：离线特权信息缓存

**迁移场景：实时视频推荐（抖音/TikTok类）**
- 目标：推荐时利用视频深度内容理解（OCR、ASR、场景分析），但这些分析耗时
- 怎么接：离线提前抽取视频关键帧OCR/ASR/标签，缓存为视频的「语义摘要」，训练时注入推荐模型，推理时只用商品ID查询缓存
- 预期收益：实时推荐延迟不变，但模型具有深度内容理解能力
- 风险：新发布视频缓存未建立时（冷启动），退化为无深度理解的基础模型

### 原语3：位置差异化优势估计

**迁移场景：分子生成（药物发现）**
- 目标：生成满足药理约束的分子SMILES字符串
- 结构先验：SMILES的前缀（环结构、官能团）比后缀（具体取代基位置）对药理活性影响更大
- 怎么接：按SMILES的语法结构定义前缀权重ΔR，前几个核心结构token权重=3，后续修饰token权重=1
- 预期收益：更快地学习生成符合药理约束的骨架结构，减少无效分子

---

## 机制家族图谱（Mechanism Family Tree）

```
知识蒸馏家族（Knowledge Distillation）
│
├── 经典KD（Hinton 2015）: 大教师→小学生，软标签对齐
│   ├── FitNets（2015）: 中间层特征对齐
│   ├── PKD（Patient KD）: 层间逐步对齐
│   └── Born-Again Networks（2018）: 同架构迭代自蒸馏 ← 启发了Self-mode概念
│
├── 特权信息蒸馏（LUPI范式）
│   ├── Vapnik's LUPI（2009）: SVM+框架的理论源头
│   ├── SDFT（2026，Li et al.）: 通过上下文差异实现LUPI，few-shot vs zero-shot
│   ├── OPSD（2026）: 数学推理中的参考解-增强教师蒸馏
│   └── OneSearch-V2 SDFT ★ 本文: 关键词CoT增强的生成式检索自蒸馏
│
└── 隐式推理内化
    ├── Coconut（2025）: 用连续思维向量替代文本推理步骤
    ├── CODI（2025）: 隐层L1对齐压缩CoT → 与V2比较的Baseline
    ├── Latent-R3（2026）: 连续隐空间的强化学习
    └── OneSearch-V2 ★: 无需额外参数/特殊token的输出分布对齐（最小侵入性）

强化学习对齐家族（RL Alignment）
│
├── PPO → GRPO（DeepSeek，2024）: 无Critic的组内相对优势
│   ├── ECPO（OneRec，2025）: 早停裁剪GRPO
│   ├── GBPO（OneRec-V2，2025）: 梯度有界策略优化
│   └── TPMA-GRPO ★ 本文: 位置级差异优势 + 前缀门控（创新增量：结构先验编码）
│
└── 行为偏好对齐
    ├── RLHF → DPO → Listwise DPO: 成对/列表式偏好学习
    ├── PARS（OneSearch-V1）: 奖励模型引导的自适应排序 ← V2取代的方案
    └── TPMA-GRPO ★: 直接用行为日志（点击/订单），无奖励模型依赖

**本文的核心创新增量**：
- 相比Coconut/CODI：无架构修改，无额外token，蒸馏发生在输出logit层而非隐层
- 相比标准GRPO：引入结构先验（前缀权重+门控），首次在生成式检索中实现细粒度信用分配
- 相比传统LUPI：将LUPI范式从分类器推广到自回归生成模型，并提供了稳定训练的正则化组合（R-Drop+FGM）
```

---

## 背景知识补充 (Background Context)

## 背景与先验知识

### 生成式搜索（Generative Search）范式
传统搜索系统采用「检索-排序」两阶段架构（retrieve-then-rank），依赖倒排索引或向量检索召回候选集，再由排序模型精排。生成式搜索（如TIGER, GENRE, OneSearch-V1）直接用自回归语言模型生成商品ID（SID），将检索问题转化为序列生成问题，端到端优化，且天然支持对用户历史行为序列的建模。

### 语义ID（SID, Semantic ID）
SID是将商品的语义信息（标题、图片、类目）压缩编码为一组离散token序列的表示方法，通常使用RQ-VAE（Residual Quantized Variational Autoencoder）或类似方法实现。模型自回归生成SID的每个token，等价于在语义空间中逐步缩小候选范围（类似前缀树检索）。V2中使用KHQE（关键词层次量化编码），实验证明优于多模态编码方案。

### GRPO（Group Relative Policy Optimization）
GRPO是DeepSeek在DeepSeekMath/R1中提出的无Critic强化学习算法，通过组内（一批rollout样本间）相对优势估计（而非绝对价值函数估计）来稳定策略梯度训练，避免了训练Critic网络的额外开销。已在数学推理、代码生成等任务上取得显著成功。V2的TPMA-GRPO是其在结构化ID生成场景的细粒度扩展。

### 特权信息学习（LUPI, Learning with Privileged Information）
Vapnik（2009）提出的框架：训练时允许使用「特权信息」（即测试时不可用的额外信息）。核心洞察是：教学过程中的额外提示（如老师的解题思路）虽然考试时不可用，但通过适当的知识传递机制（SVM+）可以显著提升模型的泛化性能。V2的自蒸馏本质上是LUPI在LLM场景的现代化实例，关键词CoT即为特权信息。

### R-Drop正则化
R-Drop（NeurIPS 2021，梁晓波等）通过对同一输入进行两次带独立dropout的前向传播，最小化两次输出分布的双向KL散度，作为额外正则化项。在多个NLP基准上超越传统dropout，在数据稀疏时尤为有效，已成为序列生成模型微调的标准trick之一。

### FGM（Fast Gradient Method）对抗训练
对抗训练的一种高效实现（Miyato 2017），在embedding层沿梯度方向添加小扰动，训练模型对输入噪声的鲁棒性。仅需在标准反向传播后额外做一次前向-反向传播，计算开销约为2×标准训练，是目前NLP文本对抗训练的主流方法之一（优于FGSM和PGD在文本场景的应用）。
