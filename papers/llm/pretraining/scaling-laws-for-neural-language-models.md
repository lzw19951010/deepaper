---
abstract: We study empirical scaling laws for language model performance on the cross-entropy
  loss. The loss scales as a power-law with model size, dataset size, and the amount
  of compute used for training, with some trends spanning more than seven orders of
  magnitude. Other architectural details such as network width or depth have minimal
  effects within a wide range. Simple equations govern the dependence of overfitting
  on model/dataset size and the dependence of training speed on model size. These
  relationships allow us to determine the optimal allocation of a fixed compute budget.
  Larger models are significantly more sample-efficient, such that optimally compute-efficient
  training involves training very large models on a relatively modest amount of data
  and stopping significantly before convergence.
arxiv_categories:
- cs.LG
arxiv_id: '2001.08361'
authors:
- Jared Kaplan
- Sam McCandlish
- Tom Henighan
- Tom B. Brown
- Benjamin Chess
- Rewon Child
- Scott Gray
- Alec Radford
- Jeffrey Wu
- Dario Amodei
baselines:
- LSTM
- Universal Transformer (Recurrent Transformer)
category: llm/pretraining
code_url: null
core_contribution: empirical-study
datasets:
- WebText2
- Books Corpus
- Common Crawl
- English Wikipedia
- Internet Books
date: '2020-01-23'
doi: null
keywords:
- scaling laws
- power laws
- language models
- Transformer
- compute efficiency
- sample efficiency
- overfitting
- critical batch size
- optimal compute allocation
- cross-entropy loss
metrics:
- Cross-entropy loss (nats)
publication_type: preprint
status: complete
tags:
- scaling-laws
- language-model
- power-law
- compute-efficiency
- transformer
- training-optimization
- neural-scaling
title: Scaling Laws for Neural Language Models
tldr: 通过大规模实验发现语言模型的交叉熵损失与模型参数量N、数据集大小D、计算量C之间存在精确的幂律关系，并据此推导出最优计算资源分配策略：应优先增大模型而非延长训练时间。
url: https://arxiv.org/abs/2001.08361
venue: null
---

## 核心速览 (Executive Summary)

### TL;DR

语言模型的测试损失与模型参数量、数据集大小、训练计算量分别呈精确的幂律(power-law)关系，跨越7个数量级保持一致；最优计算分配策略是训练非常大的模型但远未收敛就停止，而非训练小模型到收敛。

### 一图流 (Mental Model)

如果把训练语言模型比作烧水：旧的做法是用小锅（小模型）把水烧到100°C（完全收敛），新的发现告诉我们——用大锅（大模型）把水烧到60°C（远未收敛）反而更省燃气（计算资源），而且水温（性能）还更高。锅的形状（宽/窄/深/浅）几乎不影响结果，只有锅的总容量（参数量）才重要。

### 核心机制一句话

**拟合** 语言模型性能与规模因子（N, D, C）的关系，以 **幂律方程** 的形式，**揭示** 规模、数据和计算之间的普适性定量规律，从而 **实现** 对最优资源分配和模型性能的精确预测。

---

## 动机与第一性原理 (Motivation & First Principles)

### 痛点 (The Gap)

在2020年之前，研究者对语言模型的扩展行为缺乏系统性的定量理解。具体而言：

1. **资源分配无据可依**：给定固定的计算预算，应该训练多大的模型、用多少数据、训练多少步？此前完全依赖经验和直觉，没有定量指导。典型做法是训练较小的模型到收敛，这被证明是计算效率极低的。
2. **架构选择的迷信**：研究者花费大量精力调整模型的深度、宽度、注意力头数等超参数，但这些调整的实际收益未被系统量化。
3. **数据需求不明确**：随着模型增大，需要多少额外数据来避免过拟合？此前的工作（如[HNA+17]）甚至给出了相反的结论（超线性增长 vs 本文发现的亚线性增长）。
4. **性能预测困难**：无法根据小规模实验可靠地外推大规模模型的性能。

### 核心洞察 (Key Insight)

**Because** 语言模型的损失函数景观具有某种内在的规则性（可能与自然语言数据的统计结构有关），**→** 模型性能与N、D、C各自呈现精确的幂律关系（L ∝ X^{-α}），且这些幂律在各自不被其他因素瓶颈时跨越多个数量级保持稳定，**→** 因此可以推导出一套完整的最优资源分配方案：给定计算预算C，最优模型大小 N ∝ C^{0.73}，训练步数几乎不增长 S ∝ C^{0.03}，即绝大部分新增计算应用于放大模型。

关键的因果链是：
- 大模型的样本效率更高（达到相同损失需要更少的数据点）
- 因此最优策略不是"小模型训练到收敛"，而是"大模型训练到远未收敛"
- 过拟合程度仅取决于 N^{0.74}/D 这一比值，因此数据需求亚线性增长于模型大小

### 物理/直觉解释

想象你在学一门外语。一个"大模型"就像一个记忆力超强的学生——他只需要翻一遍课本（少量数据/训练步数），就能记住大部分内容。而一个"小模型"就像记忆力一般的学生——他需要反复读课本很多遍（大量训练步数到收敛）才能记住同样的内容。

如果你的目标是"一小时内学到尽可能多的内容"（固定计算预算），最优策略不是让记忆力一般的学生反复读——而是找一个记忆力更强的学生，让他快速浏览一遍。这就是为什么"大模型 + 早停"比"小模型 + 收敛"更有效率。

幂律之所以成立，直觉上是因为语言数据本身具有多层次的结构（从字符级别到语法到语义到世界知识），每增加一个数量级的参数/数据/计算，模型只能再"解锁"一小部分更精细的模式，收益递减但以一种非常有规律的方式递减。

---

## 方法详解 (Methodology)

## 直觉版 (Intuitive Walk-through)

### 论文的"方法"是什么？

本文不是提出新模型架构，而是进行大规模的系统性实验（empirical study）。核心方法是：

1. **训练大量不同配置的Transformer模型**：参数量从768到1.5B，数据集从22M到23B tokens，形状（深度/宽度/注意力头数/FFN维度）全面变化
2. **测量测试集交叉熵损失**：在WebText2测试集及多个其他数据分布上
3. **拟合幂律方程**：找到L与N、D、C之间的定量关系
4. **推导最优分配策略**：基于拟合的方程，数学推导出给定计算预算时的最优模型大小和训练策略

### 引用论文Figure 1（page 3）解读

Figure 1 展示了三张log-log图：
- **左图（Compute）**：横轴是训练计算量（PF-days），纵轴是测试损失。每条彩色曲线代表一个不同大小的模型的训练轨迹，黑色粗线是最优包络线（每个计算预算下选择最优模型）。在log-log坐标下，包络线几乎是完美的直线 → 幂律。
- **中图（Dataset Size）**：横轴是数据集大小（tokens），纵轴是测试损失。在足够大的模型下，损失与数据量呈幂律关系。
- **右图（Parameters）**：横轴是非嵌入参数量，纵轴是测试损失。在足够多数据和计算下，损失与参数量呈幂律关系。

### 旧方法 vs 新方法

这不是一个"旧方法 vs 新方法"的论文，而是一个发现规律的论文。但如果把"旧的训练实践"和"新的基于scaling law的训练实践"对比：

- **旧做法**：选择一个能放进GPU的模型大小 → 尽可能训练到收敛 → 调各种超参数（深度/宽度/LR等）
- **新做法**：根据计算预算C，直接计算最优模型大小 N ∝ C^{0.73} → 训练到约10%高于收敛损失就停止 → 几乎不需要关心模型形状细节

## 精确版 (Formal Specification)

### 流程图 (Text-based Flow)

```
实验设计流程:
Input: 计算预算 C (PF-days)
    ↓
Step 1: 确定最优模型大小
    N_opt = (1.3×10^9) × C_min^{0.73}
    ↓
Step 2: 确定批量大小
    B_crit(L) = B_* / L^{1/α_B} = 2×10^8 / L^{4.8}
    ↓
Step 3: 确定训练步数
    S = C_min / (6 × N × B_crit)
    ↓
Step 4: 训练到 L ≈ 1.1 × L(N, ∞)  [约10%高于收敛损失]
    ↓
Output: 测试损失 L(C_min) = (C_c^min / C_min)^{α_C^min}
```

### 关键公式与变量

#### 公式1：参数量scaling law
$$L(N) = (N_c / N)^{\alpha_N}$$

| 符号 | 数学定义 | 物理含义 | 拟合值 |
|------|---------|---------|-------|
| $L$ | 交叉熵损失 (nats) | 模型预测下一个token的不确定性 | — |
| $N$ | 非嵌入参数量 | 模型的"容量"，不含词表和位置嵌入 | 变量 |
| $N_c$ | 幂律尺度常数 | 假想的"完美"参数量（损失归零时的参数量） | 8.8×10^{13} |
| $\alpha_N$ | 幂律指数 | 每倍增参数的损失递减速率（越大越好） | 0.076 |

#### 公式2：数据量scaling law
$$L(D) = (D_c / D)^{\alpha_D}$$

| 符号 | 拟合值 | 物理含义 |
|------|-------|--------|
| $D_c$ | 5.4×10^{13} tokens | 数据尺度常数 |
| $\alpha_D$ | 0.095 | 每倍增数据的损失递减速率 |

#### 公式3：联合scaling law
$$L(N,D) = \left[\left(\frac{N_c}{N}\right)^{\alpha_N/\alpha_D} + \frac{D_c}{D}\right]^{\alpha_D}$$

物理含义：模型能力瓶颈 $(N_c/N)^{\alpha_N/\alpha_D}$ 和数据瓶颈 $D_c/D$ 以加法方式组合——两个瓶颈中更大的那个主导总损失。

#### 公式4：计算量scaling law
$$L(C_{min}) = (C_c^{min} / C_{min})^{\alpha_C^{min}}$$

| 符号 | 拟合值 | 物理含义 |
|------|-------|--------|
| $C_c^{min}$ | 3.1×10^8 PF-days | 计算尺度常数 |
| $\alpha_C^{min}$ | 0.050 | 每倍增计算的损失递减速率 |

#### 公式5：训练曲线 scaling law
$$L(N, S_{min}) = \left(\frac{N_c}{N}\right)^{\alpha_N} + \left(\frac{S_c}{S_{min}}\right)^{\alpha_S}$$

| 符号 | 拟合值 | 物理含义 |
|------|-------|--------|
| $S_c$ | 2.1×10^3 步 | 训练步数尺度常数 |
| $\alpha_S$ | 0.76 | 训练时间的幂律指数 |

关键关系：$\alpha_C^{min} = 1/(1/\alpha_S + 1/\alpha_B + 1/\alpha_N) \approx 0.054$

#### 公式6：临界批量大小
$$B_{crit}(L) = B_* / L^{1/\alpha_B}$$

| 符号 | 拟合值 | 物理含义 |
|------|-------|--------|
| $B_*$ | 2×10^8 tokens | 批量大小尺度常数 |
| $\alpha_B$ | 0.21 | 批量大小的幂律指数 |

#### 公式7：过拟合与数据需求
$$D \geq (5 \times 10^3) \cdot N^{0.74}$$

物理含义：为了避免显著过拟合，数据量需以模型参数量的0.74次方增长——即模型参数量增大8倍时，数据仅需增加约5倍。

### 数值推演 (Numerical Example)

**场景**：假设有 C_min = 10 PF-days 的计算预算，如何最优分配？

**Step 1: 最优模型大小**
$$N_{opt} = 1.3 \times 10^9 \times 10^{0.73} = 1.3 \times 10^9 \times 5.37 \approx 7.0 \times 10^9 \text{ (约70亿参数)}$$

**Step 2: 预测最优损失**
$$L(C_{min}) = (3.1 \times 10^8 / 10)^{0.050} = (3.1 \times 10^7)^{0.050}$$
$$\log_{10}(3.1 \times 10^7) = 7.49$$
$$L = 10^{0.050 \times 7.49} = 10^{0.375} \approx 2.37 \text{ nats}$$

**Step 3: 预测收敛损失**
根据 L(N) = (N_c/N)^{α_N}：
$$L(N, \infty) = (8.8 \times 10^{13} / 7.0 \times 10^9)^{0.076} = (1.26 \times 10^4)^{0.076}$$
$$= 10^{0.076 \times 4.1} = 10^{0.31} \approx 2.05 \text{ nats}$$

**Step 4: 确认"10%规则"**
$$L_{train}/L_{converge} = 2.37/2.05 \approx 1.16$$

大约比收敛损失高16%（理论预测约 α_N/α_S ≈ 10%，与拟合参数轻微差异属正常范围）。

**Step 5: 数据需求**
$$D \geq 5 \times 10^3 \times (7.0 \times 10^9)^{0.74}$$
$$= 5 \times 10^3 \times 10^{0.74 \times 9.85} = 5 \times 10^3 \times 10^{7.29} \approx 10^{11} \text{ tokens (约1000亿)}$$

### 伪代码 (Pseudocode)

```python
# 核心不是一个训练算法，而是一个资源分配决策框架
# 以下是根据scaling laws进行最优计算分配的伪代码

def optimal_allocation(C_min_pf_days: float) -> dict:
    """给定计算预算(PF-days), 返回最优训练配置"""
    
    # Scaling law 常数 (来自Table 5, 6)
    alpha_N = 0.076
    alpha_S = 0.76
    alpha_B = 0.21
    N_c = 8.8e13  # params
    S_c = 2.1e3   # steps
    B_star = 2e8   # tokens
    C_c_min = 3.1e8  # PF-days
    
    # Step 1: 最优模型大小  N ∝ C^{0.73}
    N_opt = 1.3e9 * C_min_pf_days ** 0.73  # [params]
    
    # Step 2: 预测目标损失
    alpha_C_min = 1.0 / (1/alpha_S + 1/alpha_B + 1/alpha_N)  # ≈ 0.054
    L_target = (C_c_min / C_min_pf_days) ** alpha_C_min  # [nats]
    
    # Step 3: 临界批量大小
    B_crit = B_star / L_target ** (1/alpha_B)  # [tokens]
    
    # Step 4: 最优训练步数
    C_flops = C_min_pf_days * 8.64e19  # 转换为 FLOPs
    S_min = C_flops / (6 * N_opt * B_crit)  # [steps]
    
    # Step 5: 数据需求
    D_opt = B_crit * S_min  # [tokens], 即1个epoch
    
    return {
        "model_params": N_opt,
        "batch_size_tokens": B_crit,
        "training_steps": S_min,
        "dataset_tokens": D_opt,
        "predicted_loss": L_target,
    }
```

## 设计决策 (Design Decisions)

### 决策1：排除嵌入参数
- **选择**：用非嵌入参数量 N（排除词表嵌入和位置嵌入）作为"模型大小"
- **替代方案**：用总参数量
- **论文对比**：Figure 6 明确对比了两种做法。包含嵌入参数时，不同深度的模型趋势线发散；排除后，所有模型（除极端情况外）收敛到单一趋势线
- **核心trade-off**：排除嵌入参数得到更干净的scaling law，但代价是模型大小的定义不直观

### 决策2：L(N,D) 的函数形式
- **选择**：$L(N,D) = [(N_c/N)^{\alpha_N/\alpha_D} + D_c/D]^{\alpha_D}$
- **替代方案**：$L(N,D) = [(N_c/N)^{\alpha_N} + (D_c/D)^{\alpha_D}]^\beta$（对称形式）
- **论文讨论**：作者基于三个原则排除了对称形式——对称形式没有1/D的整数幂展开，这违反了他们关于过拟合应以1/D为主导的理论预期
- **核心trade-off**：解析性（1/D展开）vs 对称美学。作者选择了解析性，并用实验验证了拟合质量

### 决策3：计算量估计 C ≈ 6NBS
- **选择**：忽略与上下文长度相关的计算（注意力掩码的 2n_layer × n_ctx × d_attn 项）
- **替代方案**：包含上下文相关计算
- **论文讨论**：Table 1 列出了完整的计算分解。作者指出，当 d_model >> n_ctx/12 时（本文大部分模型满足），上下文相关计算占比很小
- **核心trade-off**：简洁性 vs 精确性。在n_ctx很大的场景下（如n_ctx ≥ 12 × d_model），这个近似会失效

### 决策4：使用 C_min 而非原始 C
- **选择**：将所有实验的计算量调整为在临界批量大小 B_crit 下训练的等效计算量 C_min
- **替代方案**：直接使用实际计算量 C
- **论文对比**：Figure 13 对比了两种做法，C_min 得到了更干净的幂律趋势
- **核心trade-off**：需要额外估计 B_crit(L)，但得到了更准确的scaling law

## 易混淆点 (Potential Confusions)

### 混淆1："更大的模型需要更多数据"
- ❌ 错误理解：模型参数增大10倍，数据也必须增大10倍
- ✅ 正确理解：数据需求增长远低于线性——模型参数增大8倍，数据仅需增加约5倍（D ∝ N^{0.74}）。更重要的是，对于最优计算效率的训练，数据增长更慢（D ∝ C^{0.27}）

### 混淆2："应该训练到收敛"
- ❌ 错误理解：给定计算预算，应该选择能收敛的最大模型并训练到收敛
- ✅ 正确理解：最优策略是选择一个更大的模型（约2.7倍于"能收敛"的大小），训练到仅比收敛损失高约10%就停止。这比训练到收敛节省约65%的计算

### 混淆3："L(C) 和 L(C_min) 是同一个东西"
- ❌ 错误理解：Figure 1 中的计算趋势线就是最终的scaling law
- ✅ 正确理解：Figure 1 中的 L(C) 是在固定batch size下的经验结果（α_C ≈ 0.057），而真正应用于预测的是调整到最优batch size后的 L(C_min)（α_C^{min} ≈ 0.050）。两者通过 C_min = C/(1+B/B_crit) 关联

---

## 实验与归因 (Experiments & Attribution)

### 核心收益

本文是一篇实验驱动的论文，其"收益"不是在某个benchmark上的提升，而是发现了一组跨越多个数量级的定量规律：

| Scaling Law | 关系 | 跨越范围 | 拟合质量 |
|-------------|------|---------|--------|
| L(N) | L ∝ N^{-0.076} | 6个数量级 (10^3 ~ 10^9) | 极好 |
| L(D) | L ∝ D^{-0.095} | 2+个数量级 (10^7 ~ 10^{10}) | 好 |
| L(C_min) | L ∝ C^{-0.050} | 8个数量级 | 极好 |
| B_crit(L) | B ∝ L^{-4.8} | 2个数量级 | 好 |
| L(N,S) | 双项幂律 | 6个数量级(N) × 5个数量级(S) | 好 |

**关键量化发现**：

1. **计算效率提升**：相比训练小模型到收敛的传统做法，基于scaling law的最优分配节省约65%的计算
2. **样本效率**：最大模型（10^9参数）比最小模型（10^3参数）的样本效率高近100倍（Figure 19）
3. **架构不敏感**：在总参数量固定时，深度/宽度的比值（aspect ratio）变化40倍，损失仅变化约3%（Figure 5）
4. **跨分布泛化**：在WebText2、Books、Wikipedia、Common Crawl等不同分布上，scaling law的指数几乎相同，仅存在一个小的常数偏移（Figure 8）

### 归因分析 (Ablation Study)

本文不是传统的ablation study结构，但其系统性实验本身就是一种归因分析。按"发现的重要性"排序：

1. **模型大小 N 是最重要的因素**（贡献排名第1）：最优计算分配中，增加10倍计算 → 模型增大5倍，数据仅增大2倍。N ∝ C^{0.73} 的指数远大于其他分配
2. **数据量 D 的亚线性需求**（贡献排名第2）：D ∝ N^{0.74} 的发现表明数据增长需求远低于此前预期
3. **训练步数 S 几乎不变**（贡献排名第3）：S ∝ C^{0.03}，几乎为常数，说明应通过增大batch size而非增加步数来利用更多数据
4. **模型形状几乎不影响性能**（贡献排名第4）：Figure 5 的实验表明，在固定N的条件下，深度/宽度/注意力头数/FFN比例等架构超参数的影响极小

### 可信度检查

**优点**：
- 实验规模大、覆盖面广：模型大小跨6个数量级，计算量跨8个数量级
- 在多个数据分布上验证了泛化性
- 理论预测（Section 6.2）与经验观察独立吻合（如 α_C^{min} 理论值0.054 vs 经验值0.050）
- 与LSTM和Universal Transformer做了对比
- 考虑了batch size效应并进行了修正

**潜在问题**：
- 所有实验仅在WebText2一个训练集上进行，scaling law的常数项（N_c, D_c, C_c）依赖于该数据集和tokenization
- 最大模型仅1.5B参数，外推到更大规模（10^{12}参数）的可靠性存疑（作者在Section 6.3坦诚讨论了这一点）
- 未充分探索正则化的影响（仅使用固定10%的dropout）
- 学习率调度的影响虽然被研究了（Figure 22），但主要在小模型上
- 作者在Appendix C中坦诚列出了多项caveats，透明度较高

---

## 专家批判 (Critical Review)

### 隐性成本 (Hidden Costs)

1. **外推不确定性**：论文自己在Section 6.3揭示了一个根本性矛盾——L(C_min)和L(D)的外推在约C* ~ 10^4 PF-days处交叉，表明scaling laws必须在此之前失效。但该交叉点对幂律指数的精确值极其敏感，"在两个方向上各变化一个数量级"。这意味着这些scaling laws的预测范围实际上是有限的。

2. **硬件约束未纳入**：论文的最优分配建议（"主要增大模型"）假设可以训练任意大的模型，但实际中受限于GPU内存和模型并行效率。论文在Discussion中承认了这一点，但未量化这些约束的影响。

3. **Tokenization和数据依赖**：N_c、D_c、C_c等常数依赖于特定的BPE tokenization和WebText2数据集。换用不同的tokenizer或不同语言的数据，这些常数会变化，幂律指数本身是否变化也不确定。

4. **仅衡量交叉熵损失**：论文没有研究scaling laws如何映射到下游任务性能。损失的smooth improvement是否对应下游任务的smooth improvement？后来的工作（如GPT-3）表明，某些能力会出现"涌现"现象，这与smooth power law的预期存在张力。

5. **优化器限制**：大部分实验使用Adam，最大模型使用Adafactor（"due to memory constraints"）。不同优化器可能改变scaling law的指数。

### 工程落地建议

1. **最大的"坑"——幂律指数的测量精度**：整个框架的实用性取决于α_N、α_S、α_B的精确值。但这些值需要在你自己的数据和tokenization上重新测量。小的测量误差会在外推时被放大（因为最优分配 N ∝ C^{α_C/α_N}，指数之比对误差敏感）。

2. **先做pilot实验**：建议先训练5-10个不同大小的小模型到收敛，拟合你自己的L(N)，然后再做资源分配决策。

3. **batch size调度**：论文建议在B_crit处训练，但B_crit随损失变化。实际中可以先小batch训练，随着损失降低逐步增大batch size。

4. **与后续工作[Chinchilla]的矛盾**：Hoffmann et al. (2022) 的Chinchilla scaling laws发现N和D应等比增长（N ∝ C^{0.5}, D ∝ C^{0.5}），与本文的N ∝ C^{0.73}存在显著差异。Chinchilla的实验更大规模，通常被认为更可靠。落地时应参考Chinchilla的结论。

### 关联思考

1. **与Chinchilla Scaling Laws的关系**：Hoffmann et al. (2022) 的工作是本文的"精神续作"，使用更大规模实验得到了不同的最优分配比例。关键差异是Chinchilla认为应给数据更多分配（D ∝ C^{0.5} vs 本文的 D ∝ C^{0.27}），这导致了训练实践的重大转变。

2. **与MoE的关系**：Mixture of Experts通过稀疏激活增加N而不成比例增加C。如果scaling law主要依赖于N，MoE可能获得"免费"的性能提升。但如果关键的是"有效参数量"（每个token激活的参数），则需要重新测量scaling law。

3. **与FlashAttention的关系**：FlashAttention减少了注意力计算的实际wall-clock时间，但不改变FLOPs计数。因此它不直接影响scaling law本身，但使得在相同硬件约束下能训练更大的模型（更接近理论最优分配）。

4. **与LoRA/Parameter-Efficient Fine-tuning的关系**：本文的scaling law适用于从头训练。微调场景下是否存在类似的scaling law是一个开放问题。LoRA的低秩假设暗示微调时的"有效N"远小于总参数量。

5. **与数据质量/课程学习的关系**：本文假设数据是同质的，仅考虑数据量D。数据质量或数据排列顺序可能引入新的scaling维度，这在后续工作中被研究（如data pruning、data mixing laws）。

---

## 机制迁移分析 (Mechanism Transfer Analysis)

### 机制解耦 (Mechanism Decomposition)

| 原语名称 | 本文用途 | 抽象描述 | 信息论/几何直觉 |
|---------|---------|---------|---------------|
| **幂律资源-性能映射** | 描述语言模型损失与N/D/C的关系 | 给定资源量X，系统性能按 L ∝ X^{-α} 改善，其中α是领域/任务特定常数 | 信息论：每增加一个数量级的资源，只能"解锁"数据中固定比例的额外互信息。几何：损失景观是分形的，不同尺度的特征以幂律分布 |
| **多瓶颈加法分解** | L(N,D)中N瓶颈和D瓶颈的加法组合 | 当系统受多个独立资源约束时，总损失 ≈ f(瓶颈1 + 瓶颈2)，各瓶颈以幂律形式出现 | 信息论：总信息损失 = 模型容量不足造成的损失 + 数据不足造成的损失，两者近似独立 |
| **临界批量大小 / 噪声-效率平衡** | B_crit(L) 决定梯度并行的最优粒度 | 在优化过程中，存在一个与当前性能水平相关的临界并行度，低于此值可免费并行，高于此值则收益递减 | 信号处理：当梯度的信噪比 ≈ 1时，batch内样本开始提供冗余信息。B_crit标记了从"每个样本都有新信息"到"样本间开始重复"的转变点 |
| **早停最优性 / 收敛低效** | 最优训练应停在约10%高于收敛损失处 | 在迭代优化中，最后接近收敛的阶段消耗了大量计算但贡献极少的性能提升，存在一个最优的"粗糙度"水平 | 几何：损失景观在最小值附近近似二次函数，从二次区域的边缘到最小值的优化具有递减回报，而相同的计算用于增大模型可获得更多收益 |

### 迁移处方 (Transfer Prescription)

#### 原语1：幂律资源-性能映射

**应用场景A：推荐系统的Embedding维度scaling**
- 目标领域：推荐系统中的用户/物品embedding
- 怎么接：以embedding总参数量（num_items × embed_dim）为X轴，以CTR预估的logloss为Y轴，拟合幂律关系。找到你自己系统的α_N
- 输入：不同embedding维度配置下的logloss
- 输出：给定参数预算下的最优embedding维度分配
- 预期收益：避免"拍脑袋"选择embedding维度，可能发现当前配置离最优有显著距离
- 风险：推荐系统中特征工程和模型结构的交互可能破坏简单幂律的适用性

**应用场景B：图像生成模型（扩散模型）的资源分配**
- 目标领域：文生图/视频扩散模型训练
- 怎么接：用FID/CLIP score替代交叉熵损失，以U-Net/DiT参数量为N，拟合scaling law
- 预期收益：避免在固定架构上过度训练，转而训练更大的扩散模型
- 风险：FID等指标可能不如交叉熵那样呈现clean的幂律关系

#### 原语2：多瓶颈加法分解

**应用场景：多模态模型的模态分配**
- 目标领域：Vision-Language Models (如LLaVA, Flamingo)
- 具体问题：如何在视觉编码器和语言模型之间分配参数预算？
- 怎么接：将总损失建模为 L ≈ [视觉瓶颈 + 语言瓶颈 + 对齐瓶颈]^β，分别测量各瓶颈的scaling指数
- 预期收益：发现当前系统的主要瓶颈是哪个模态，定量指导参数分配
- 风险：模态间的交互可能使加法分解失效

#### 原语3：临界批量大小

**应用场景：分布式强化学习的经验回放并行度**
- 目标领域：大规模分布式RL（如AlphaGo/AlphaStar式训练）
- 具体问题：使用多少并行Actor收集经验？
- 怎么接：测量梯度噪声尺度随训练进展的变化，据此动态调整Actor数量
- 预期收益：避免过多Actor带来的冗余计算，也避免过少Actor导致的训练不稳定
- 风险：RL中策略变化导致数据分布非平稳，可能使得梯度噪声尺度的估计不稳定

#### 原语4：早停最优性

**应用场景：AutoML/NAS中的模型选择**
- 目标领域：神经架构搜索
- 具体问题：在固定搜索预算下，应该训练少量候选架构到收敛，还是训练更多候选架构但每个训练更少？
- 怎么接：基于scaling law预测，每个候选架构只需训练到约10%高于收敛损失即可可靠排序。将节省的计算用于评估更多候选
- 预期收益：可能将NAS效率提升2-3倍
- 风险：如果不同架构的scaling指数差异很大，早停可能导致排序不一致

### 机制家族图谱 (Mechanism Family Tree)

#### 前身 (Ancestors)
- **Hestness et al. (2017)** [HNA+17]：最早系统研究深度学习的scaling行为，但发现了与本文相反的结论（数据需求超线性于模型大小）。他们研究了多个领域（翻译、语音、图像），但每个领域的规模较小
- **Banko & Brill (2001)** [BB01]：在NLP任务中首次发现数据量与性能的幂律关系
- **McCandlish et al. (2018)** [MKAT18]：提出了临界批量大小的概念和梯度噪声尺度理论。本文的B_crit分析直接建立在此基础上
- **统计学习理论中的偏差-方差分解**：过拟合 ∝ 1/D 的假设来自经典统计理论

#### 兄弟 (Siblings)
- **Rosenfeld et al. (2019)** [RRBS19a,b]：独立且几乎同时地研究了模型大小和数据集大小的scaling，使用了类似的ansatz
- **EfficientNet (Tan & Le, 2019)** [TL19]：在图像领域发现了模型大小与性能的幂律关系，但关注的是深度/宽度/分辨率的联合缩放，而非本文的"形状不重要，总量才重要"

#### 后代 (Descendants)
- **GPT-3 (Brown et al., 2020)**：直接应用本文的scaling laws指导训练了175B参数模型
- **Chinchilla / Training Compute-Optimal LLMs (Hoffmann et al., 2022)**：用更大规模实验修正了本文的最优分配比例，发现N和D应等比增长。这是本文最重要的后代，也是最重要的修正
- **Scaling Laws for Autoregressive Generative Modeling (Henighan et al., 2020)**：将本文的方法论推广到图像、视频、数学、代码等领域
- **Scaling Data-Constrained Language Models (Muennighoff et al., 2023)**：研究数据重复（多epoch）场景下的scaling law
- **Scaling Laws for Neural Machine Translation (Ghorbani et al., 2021)**：将scaling law推广到机器翻译
- **Scaling Laws for Reward Model Overoptimization (Gao et al., 2022)**：将scaling law思想应用到RLHF中的奖励模型

**创新增量**：本文的核心创新不在于"发现幂律"（前人已有），而在于(1)系统性地覆盖了N/D/C三个维度并发现了统一框架，(2)推导了最优资源分配策略及其定量预测，(3)发现了模型形状的不重要性。这些发现共同构成了一个从描述性到预测性的跨越——从"观察到幂律"到"用幂律指导训练决策"。

---

## 背景知识补充 (Background Context)

### 前置知识补充

#### Transformer 架构
本文研究的是decoder-only Transformer [Vaswani et al., 2017; Liu et al., 2018]，即GPT系列使用的自回归架构。模型参数量的估算公式 N ≈ 12 × n_layer × d_model^2 是一个标准近似，其中因子12来自：每层包含自注意力的QKV投影(3d^2)、输出投影(d^2)、和FFN的两层(2 × 4d^2 = 8d^2)，共12d^2。

#### 临界批量大小 (Critical Batch Size)
来自McCandlish et al. (2018) [MKAT18]的概念。核心思想是：训练存在一个"信噪转折点"B_crit。当batch size B < B_crit时，每个样本的梯度都贡献有用信号，增大batch几乎不增加总计算量；当B > B_crit时，样本间梯度开始冗余，增大batch主要浪费计算。B_crit可以通过梯度噪声尺度(gradient noise scale)来估计。这是本文分析C_min和S_min的理论基础。

#### 交叉熵损失与perplexity的关系
本文使用nats（自然对数底的交叉熵）作为损失单位。与perplexity的关系为：perplexity = e^{L(nats)}。例如，L = 3.0 nats 对应 perplexity ≈ 20.1。

#### WebText2 数据集
是OpenAI的WebText数据集的扩展版，来自Reddit上获得至少3 karma的外链文本。总计约23B tokens（2.29×10^{10}），使用GPT-2的BPE tokenizer（词表大小50257）。该数据集未公开。
