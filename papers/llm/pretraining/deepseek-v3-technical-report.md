---
abstract: We present DeepSeek-V3, a strong Mixture-of-Experts (MoE) language model
  with 671B total parameters with 37B activated for each token. To achieve efficient
  inference and cost-effective training, DeepSeek-V3 adopts Multi-head Latent Attention
  (MLA) and DeepSeekMoE architectures, which were thoroughly validated in DeepSeek-V2.
  Furthermore, DeepSeek-V3 pioneers an auxiliary-loss-free strategy for load balancing
  and sets a multi-token prediction training objective for stronger performance. We
  pre-train DeepSeek-V3 on 14.8 trillion diverse and high-quality tokens, followed
  by Supervised Fine-Tuning and Reinforcement Learning stages to fully harness its
  capabilities. Comprehensive evaluations reveal that DeepSeek-V3 outperforms other
  open-source models and achieves performance comparable to leading closed-source
  models. Despite its excellent performance, DeepSeek-V3 requires only 2.788M H800
  GPU hours for its full training. In addition, its training process is remarkably
  stable. Throughout the entire training process, we did not experience any irrecoverable
  loss spikes or perform any rollbacks. The model checkpoints are available at this
  https URL.
arxiv_categories:
- cs.CL
arxiv_id: '2412.19437'
authors:
- DeepSeek-AI
- Aixin Liu
- Bei Feng
- Bing Xue
- Bingxuan Wang
- Bochao Wu
- Chengda Lu
- Chenggang Zhao
- Chengqi Deng
- Chenyu Zhang
- Chong Ruan
- Damai Dai
- Daya Guo
- Dejian Yang
- Deli Chen
- Dongjie Ji
- Erhang Li
- Fangyun Lin
- Fucong Dai
- Fuli Luo
- Guangbo Hao
- Guanting Chen
- Guowei Li
- H. Zhang
- Han Bao
- Hanwei Xu
- Haocheng Wang
- Haowei Zhang
- Honghui Ding
- Huajian Xin
- Huazuo Gao
- Hui Li
- Hui Qu
- J. L. Cai
- Jian Liang
- Jianzhong Guo
- Jiaqi Ni
- Jiashi Li
- Jiawei Wang
- Jin Chen
- Jingchang Chen
- Jingyang Yuan
- Junjie Qiu
- Junlong Li
- Junxiao Song
- Kai Dong
- Kai Hu
- Kaige Gao
- Kang Guan
- Kexin Huang
- Kuai Yu
- Lean Wang
- Lecong Zhang
- Lei Xu
- Leyi Xia
- Liang Zhao
- Litong Wang
- Liyue Zhang
- Meng Li
- Miaojun Wang
- Mingchuan Zhang
- Minghua Zhang
- Minghui Tang
- Mingming Li
- Ning Tian
- Panpan Huang
- Peiyi Wang
- Peng Zhang
- Qiancheng Wang
- Qihao Zhu
- Qinyu Chen
- Qiushi Du
- R. J. Chen
- R. L. Jin
- Ruiqi Ge
- Ruisong Zhang
- Ruizhe Pan
- Runji Wang
- Runxin Xu
- Ruoyu Zhang
- Ruyi Chen
- S. S. Li
- Shanghao Lu
- Shangyan Zhou
- Shanhuang Chen
- Shaoqing Wu
- Shengfeng Ye
- Shengfeng Ye
- Shirong Ma
- Shiyu Wang
- Shuang Zhou
- Shuiping Yu
- Shunfeng Zhou
- Shuting Pan
- T. Wang
- Tao Yun
- Tian Pei
- Tianyu Sun
- W. L. Xiao
- Wangding Zeng
- Wanjia Zhao
- Wei An
- Wen Liu
- Wenfeng Liang
- Wenjun Gao
- Wenqin Yu
- Wentao Zhang
- X. Q. Li
- Xiangyue Jin
- Xianzu Wang
- Xiao Bi
- Xiaodong Liu
- Xiaohan Wang
- Xiaojin Shen
- Xiaokang Chen
- Xiaokang Zhang
- Xiaosha Chen
- Xiaotao Nie
- Xiaowen Sun
- Xiaoxiang Wang
- Xin Cheng
- Xin Liu
- Xin Xie
- Xingchao Liu
- Xingkai Yu
- Xinnan Song
- Xinxia Shan
- Xinyi Zhou
- Xinyu Yang
- Xinyuan Li
- Xuecheng Su
- Xuheng Lin
- Y. K. Li
- Y. Q. Wang
- Y. X. Wei
- Y. X. Zhu
- Yang Zhang
- Yanhong Xu
- Yanhong Xu
- Yanping Huang
- Yao Li
- Yao Zhao
- Yaofeng Sun
- Yaohui Li
- Yaohui Wang
- Yi Yu
- Yi Zheng
- Yichao Zhang
- Yifan Shi
- Yiliang Xiong
- Ying He
- Ying Tang
- Yishi Piao
- Yisong Wang
- Yixuan Tan
- Yiyang Ma
- Yiyuan Liu
- Yongqiang Guo
- Yu Wu
- Yuan Ou
- Yuchen Zhu
- Yuduan Wang
- Yue Gong
- Yuheng Zou
- Yujia He
- Yukun Zha
- Yunfan Xiong
- Yunxian Ma
- Yuting Yan
- Yuxiang Luo
- Yuxiang You
- Yuxuan Liu
- Yuyang Zhou
- Z. F. Wu
- Z. Z. Ren
- Zehui Ren
- Zhangli Sha
- Zhe Fu
- Zhean Xu
- Zhen Huang
- Zhen Zhang
- Zhenda Xie
- Zhengyan Zhang
- Zhewen Hao
- Zhibin Gou
- Zhicheng Ma
- Zhigang Yan
- Zhihong Shao
- Zhipeng Xu
- Zhiyu Wu
- Zhongyu Zhang
- Zhuoshu Li
- Zihui Gu
- Zijia Zhu
- Zijun Liu
- Zilin Li
- Ziwei Xie
- Ziyang Song
- Ziyi Gao
- Zizheng Pan
baselines:
- DeepSeek-V2
- Qwen2.5-72B
- LLaMA-3.1-405B
- GPT-4o-0513
- Claude-3.5-Sonnet-1022
category: llm/pretraining
code_url: https://github.com/deepseek-ai/DeepSeek-V3
core_contribution: new-method+new-framework
datasets:
- MMLU
- MMLU-Pro
- MMLU-Redux
- MMMLU
- GPQA-Diamond
- MATH-500
- AIME 2024
- Codeforces
- SWE-bench Verified
- HumanEval
- MBPP
- LiveCodeBench
- GSM8K
- MGSM
- BBH
- DROP
- TriviaQA
- NaturalQuestions
- ARC
- HellaSwag
- PIQA
- WinoGrande
- C-Eval
- CMMLU
- CMRC
- C3
- CCPM
- CMath
- AGIEval
- CRUXEval
- RACE
- CLUEWSC
- Pile-test
- SimpleQA
- Chinese SimpleQA
- AlpacaEval 2.0
- Arena-Hard
- RewardBench
date: '2024-12-27'
doi: null
keywords:
- Mixture-of-Experts
- Multi-head Latent Attention
- auxiliary-loss-free load balancing
- multi-token prediction
- FP8 mixed precision training
- pipeline parallelism
- knowledge distillation
- large language model
- DeepSeekMoE
- speculative decoding
metrics:
- EM (Exact Match)
- Pass@1
- F1
- BPB (Bits-Per-Byte)
- Percentile
- Resolved%
- LC-WinRate
- WinRate
publication_type: preprint
status: complete
tags:
- mixture-of-experts
- large-language-model
- efficient-training
- multi-token-prediction
- load-balancing
- FP8-mixed-precision
- knowledge-distillation
- speculative-decoding
title: DeepSeek-V3 Technical Report
tldr: DeepSeek-V3是一个671B参数（37B激活）的MoE大语言模型，通过无辅助损失负载均衡、多token预测目标和FP8混合精度训练，以仅$5.576M的成本在14.8T
  token上训练，达到与GPT-4o和Claude-3.5-Sonnet可比的性能。
url: https://arxiv.org/abs/2412.19437
venue: null
---

## 核心速览 (Executive Summary)

## TL;DR (≤100字)

DeepSeek-V3采用无辅助损失的MoE负载均衡策略和多token预测训练目标，结合MLA高效注意力和FP8混合精度训练，以$5.576M的极低成本训练671B参数模型，在代码和数学任务上达到开源SOTA，整体性能比肩GPT-4o和Claude-3.5-Sonnet。

## 一图流 (Mental Model)

如果传统Dense模型是一个"全员参会"的公司（每个决策都需要所有员工参与），那么DeepSeek-V3就是一个"精英委员会制"公司：
- **MLA** = 把冗长的会议记录压缩成精炼的摘要存档（KV cache压缩~57倍），需要时再展开——节省了大量存储空间
- **DeepSeekMoE** = 每个任务只召集8位最相关的专家（从256位中选），而非全员出动——节省计算量
- **无辅助损失均衡** = 不通过罚款（辅助损失）来分配工作，而是用一个动态调整的"优先级偏置"来自然引导工作流向空闲专家——更灵活，专家能更好地专精
- **多token预测** = 每位专家不仅要完成当前任务，还要提前预判下一步——让规划能力更强

## 核心机制一句话 (Mechanism in One Line)

`[动态偏置调节] + [专家路由决策] + [无梯度干扰方式] + [实现MoE负载均衡与模型性能的帕累托最优]`

---

## 动机与第一性原理 (Motivation & First Principles)

## 痛点 (The Gap)

### 1. MoE负载均衡与模型性能的根本冲突

传统MoE模型（如GShard、Switch Transformer）使用**辅助损失（auxiliary loss）**来强制实现专家间的负载均衡。这产生了一个根本性的trade-off：
- 辅助损失太小 → 负载不均衡，产生路由崩溃（routing collapse），部分专家被废弃
- 辅助损失太大 → 模型性能明显下降（Wang et al., 2024a已实证），因为辅助损失的梯度会干扰主任务的学习信号

DeepSeek-V2虽然已经采用了DeepSeekMoE和MLA，但仍然依赖辅助损失来维持负载均衡，限制了模型的极致性能。

### 2. 单token预测目标的信号稀疏性

标准的next-token prediction目标每个位置只提供一个监督信号，这在大规模预训练中可能导致数据效率不足。Gloeckle et al. (2024)虽然提出了并行多token预测，但缺乏完整的因果链。

### 3. 大规模MoE训练的通信瓶颈

跨节点专家并行引入了计算与通信比约1:1的低效比率，传统pipeline并行方法（如1F1B）的pipeline bubble也显著浪费算力。

### 4. 低精度训练在超大规模模型上的验证缺失

FP8训练虽然前景广阔，但在>600B参数的超大规模模型上缺乏成功的端到端验证。

## 核心洞察 (Key Insight)

**洞察一：负载均衡可以不通过损失函数来实现。**

Because 辅助损失本质上是在主损失函数中注入了一个与主任务无关的梯度方向 → 这个梯度方向会干扰模型对主任务的学习 → 负载越均衡，模型性能越差。**因此，如果能在不影响梯度的情况下引导路由决策，就能打破这个trade-off。**

具体做法：给每个专家引入一个不参与梯度计算的偏置项$b_i$，仅用于影响top-K选择，而实际的门控值（乘以FFN输出的权重）仍由原始的affinity score决定。偏置项通过简单的规则动态调整：过载专家减$\gamma$，欠载专家加$\gamma$。

**洞察二：多token预测应保持因果链完整性。**

Because 独立并行预测多个token会破坏token间的依赖关系 → 导致每个预测头学到的表征不一致 → 预测质量受限。**因此，应该用序列化的方式预测额外token，让第k个预测依赖于第k-1个预测的表征。**

**洞察三：计算与通信可以在pipeline级别完全重叠。**

Because 在一对前向/反向chunk中，attention和MLP的计算可以与all-to-all的dispatch和combine通信交错执行 → 配合双向pipeline调度 → 可以将通信overhead几乎完全隐藏。

## 物理/直觉解释

**无辅助损失均衡**就像自助餐厅的排队管理：传统方法是给所有人发罚单（辅助损失）让他们不要都排同一个窗口——但罚单会让人心烦、影响就餐体验。DeepSeek-V3的方法是在热门窗口前放一个"当前等待时间"的牌子（偏置项）——人们自然会看到等待时间长就去另一个窗口，不需要罚单。关键是：牌子只影响人们"选窗口"的决定，不影响他们"打多少饭"（门控值）。

**多token预测**就像下棋时不仅要想好下一步，还要预判后面几步。而且每一步的预判都要基于前一步的预判结果（保持因果链），而不是独立地预测后面每一步。

---

## 方法详解 (Methodology)

## 直觉版 (Intuitive Walk-through)

### 参考Figure 2（基础架构图）

DeepSeek-V3的每个Transformer Block包含两大组件：

**① Multi-Head Latent Attention (MLA)**
- **旧方法（标准MHA）**：每个token的K和V都是完整的$n_h \times d_h$维向量，推理时需要缓存所有历史token的完整KV，内存消耗巨大
- **MLA改了什么**：先把输入h_t通过一个down-projection压缩到低维latent向量$c_t^{KV}$（512维 vs 原始16384维），然后再up-project回去得到各头的K和V。推理时只需缓存这个低维latent向量，外加一个携带RoPE的解耦key
- **为什么有效**：因为注意力的K/V天然存在大量冗余（多头之间高度相关），低秩压缩可以保留绝大部分信息
- **图中关键元素**：黄色"Cached During Inference"框标注了只需缓存$c_t^{KV}$和$k_t^R$两个向量

**② DeepSeekMoE + 无辅助损失均衡**
- **旧方法（GShard等）**：所有experts粒度大（如8个大专家选2个），用辅助损失强制均衡
- **DeepSeekMoE改了什么**：用256个细粒度小专家（intermediate dim=2048）选8个，外加1个共享专家始终激活。路由函数用sigmoid+top-K归一化
- **无辅助损失均衡改了什么**：不在loss中加均衡项，而是给每个专家加一个偏置$b_i$仅用于影响top-K选择，按步动态调整

### 参考Figure 3（多token预测）

- **旧方法**：每个位置只预测下一个token
- **MTP改了什么**：在主模型之上串联D个MTP模块，第k个模块利用第k-1深度的表征和第i+k个token的embedding，通过一个Transformer block预测第i+k+1个token
- **关键区别**：与Gloeckle et al.不同，MTP保持了完整的因果链——第k个预测依赖于第k-1个预测的表征
- **图中关键元素**：注意embedding层和output head是共享的（标注"Shared"）；每个MTP模块之间通过concatenation连接前一深度的表征和当前深度的token embedding

### 简单例子：3个token的处理流程

假设输入序列 [A, B, C]：

**旧方法（标准Transformer）**：
- 位置1：用A的表征预测B ✓
- 位置2：用A,B的表征预测C ✓
- 位置3：用A,B,C的表征预测D ✓
- 每个位置只有1个监督信号

**DeepSeek-V3（D=1的MTP）**：
- 主模型：和旧方法一样预测下一个token
- MTP模块1：取主模型在位置1的输出表征 + B的embedding → 预测C；取位置2的输出 + C的embedding → 预测D
- 每个位置有2个监督信号，训练信号密度翻倍

---

## 精确版 (Formal Specification)

### 流程图 (Text-based Flow)

```
Input tokens t_1...t_T
    ↓ [Embedding Layer] → h_t ∈ R^7168
    ↓
┌── Transformer Block × 61 ──┐
│                             │
│  h_t → [RMSNorm] → [MLA]   │
│  ┌─ MLA 详细流程 ─┐          │
│  │ h_t → W^DKV → c_t^KV ∈ R^512 (down-project)  │
│  │ c_t^KV → W^UK → k_t^C ∈ R^(128×128) (up-project K)│
│  │ c_t^KV → W^UV → v_t^C ∈ R^(128×128) (up-project V)│
│  │ h_t → W^KR → k_t^R ∈ R^64 (decoupled RoPE key)    │
│  │ h_t → W^DQ → c_t^Q ∈ R^1536 (down-project Q)      │
│  │ c_t^Q → W^UQ → q_t^C ∈ R^(128×128) (up-project Q) │
│  │ c_t^Q → W^QR → q_t^R ∈ R^(128×64) (decoupled Q)   │
│  │ q_i = [q_i^C; q_i^R], k_j = [k_j^C; k_j^R]        │
│  │ Attention → o_t → W^O → u_t ∈ R^7168              │
│  └────────────────┘          │
│  u_t → [RMSNorm] → [MoE FFN]│
│  ┌─ MoE 详细流程 ─┐          │
│  │ Shared Expert(s): FFN_i^(s)(u_t), i=1..1      │
│  │ Router: s_i,t = sigmoid(u_t^T e_i), i=1..256  │
│  │ Top-K select (K=8): 用 s_i,t + b_i 选择       │
│  │ Gate: g_i,t = s_i,t / Σ_selected s_j,t        │
│  │ Output: h'_t = u_t + Σ FFN^(s) + Σ g_i,t·FFN^(r)(u_t)│
│  └────────────────┘          │
└─────────────────────────────┘
    ↓ h_t^0 (main model output representation)
    ↓ [Output Head] → P_next_token (主模型next-token预测)
    ↓
┌── MTP Module k (k=1..D=1) ──┐
│ h'_i^k = M_k · [RMSNorm(h_i^{k-1}); RMSNorm(Emb(t_{i+k}))] │
│ h_i^k = TRM_k(h'_i^k)  ∈ R^7168                              │
│ P_{i+k+1}^k = OutHead(h_i^k) ∈ R^V                           │
└──────────────────────────────┘
```

### 关键公式与变量

#### MLA核心公式

| 公式 | 数学定义 | 物理含义 |
|------|---------|--------|
| $c_t^{KV} = W^{DKV} h_t$ | $R^{512} = R^{512×7168} \cdot R^{7168}$ | 将token表征压缩到低维KV latent空间 |
| $k_t^C = W^{UK} c_t^{KV}$ | $R^{16384} = R^{16384×512} \cdot R^{512}$ | 从latent空间恢复各头的content key |
| $k_t^R = \text{RoPE}(W^{KR} h_t)$ | $R^{64}$ | 携带位置信息的解耦key（所有头共享） |
| $v_t^C = W^{UV} c_t^{KV}$ | $R^{16384} = R^{16384×512} \cdot R^{512}$ | 从latent空间恢复各头的value |

#### 无辅助损失均衡核心公式

| 公式 | 数学定义 | 物理含义 |
|------|---------|--------|
| $s_{i,t} = \sigma(u_t^T e_i)$ | sigmoid affinity | token与专家的亲和度，值域[0,1] |
| $g'_{i,t} = s_{i,t}$ if $s_{i,t}+b_i \in \text{Topk}$ | 条件门控 | 用偏置后的分数选择，但门控值用原始分数 |
| $g_{i,t} = g'_{i,t} / \sum g'_{j,t}$ | 归一化门控 | 保证选中专家的权重和为1 |
| $b_i \leftarrow b_i \pm \gamma$ | 步末更新 | 过载减、欠载加，动态平衡 |

#### MTP核心公式

| 公式 | 数学定义 | 物理含义 |
|------|---------|--------|
| $h'^k_i = M_k[\text{RMSNorm}(h^{k-1}_i); \text{RMSNorm}(\text{Emb}(t_{i+k}))]$ | $R^{7168} = R^{7168×14336} \cdot R^{14336}$ | 融合上一深度的表征和当前深度的token embedding |
| $L_{MTP} = \frac{\lambda}{D} \sum_{k=1}^{D} L^k_{MTP}$ | 加权平均 | D个深度的MTP损失取平均，乘以权重λ |

### 数值推演 (Numerical Example)

#### MLA的KV Cache压缩比计算

```
标准MHA每token每层的KV cache:
  K: n_h × d_h = 128 × 128 = 16,384 个float16元素
  V: n_h × d_h = 128 × 128 = 16,384 个float16元素
  总计: 32,768 个元素 = 64 KB (FP16)

MLA每token每层的KV cache:
  c_t^KV: d_c = 512 个元素
  k_t^R: d_h^R = 64 个元素
  总计: 576 个元素 = 1.125 KB (FP16)

压缩比: 576 / 32,768 ≈ 1.76%，约57倍压缩
```

#### 无辅助损失均衡的数值例子

```
假设3个专家 e1, e2, e3，K=1（选1个），初始 b1=b2=b3=0, γ=0.001

Token A的affinity: s1=0.8, s2=0.75, s3=0.6
  加偏置后: s1+b1=0.8, s2+b2=0.75, s3+b3=0.6
  选择 e1（最高），门控值 g1=0.8/0.8=1.0

Token B的affinity: s1=0.7, s2=0.85, s3=0.65
  加偏置后: s1+b1=0.7, s2+b2=0.85, s3+b3=0.65
  选择 e2，门控值 g2=0.85/0.85=1.0

... 假设batch结束后 e1被选了5次, e2被选3次, e3被选2次
  理论均衡: 每个被选 10/3 ≈ 3.33次
  e1过载 → b1 -= 0.001 → b1 = -0.001
  e2接近均衡 → 不变
  e3欠载 → b3 += 0.001 → b3 = 0.001

下一步Token C的affinity: s1=0.79, s2=0.78, s3=0.77
  加偏置后: s1-0.001=0.789, s2=0.78, s3+0.001=0.771
  仍选 e1（但差距缩小了）
  随着训练推进，偏置会持续调节直到负载趋于均衡
```

### 伪代码 (Pseudocode)

```python
# === MLA Forward (per layer) ===
def mla_forward(h_t, W_DKV, W_UK, W_UV, W_KR, W_DQ, W_UQ, W_QR, W_O):
    # h_t: [batch, seq_len, 7168]
    
    # KV compression
    c_kv = h_t @ W_DKV.T          # [B, T, 7168] -> [B, T, 512]
    k_C = c_kv @ W_UK.T           # [B, T, 512] -> [B, T, 128*128] -> reshape [B, T, 128, 128]
    v_C = c_kv @ W_UV.T           # [B, T, 512] -> [B, T, 128*128] -> reshape [B, T, 128, 128]
    k_R = RoPE(h_t @ W_KR.T)      # [B, T, 7168] -> [B, T, 64]
    
    # Query compression
    c_q = h_t @ W_DQ.T            # [B, T, 7168] -> [B, T, 1536]
    q_C = c_q @ W_UQ.T            # [B, T, 1536] -> [B, T, 128*128] -> reshape [B, T, 128, 128]
    q_R = RoPE(c_q @ W_QR.T)      # [B, T, 1536] -> [B, T, 128*64] -> reshape [B, T, 128, 64]
    
    # Concat content + RoPE parts
    q = concat(q_C, q_R, dim=-1)  # [B, T, 128, 192]
    k = concat(k_C, k_R_broadcast, dim=-1)  # [B, T, 128, 192]
    
    # Standard attention
    attn = softmax(q @ k.T / sqrt(192)) @ v_C  # [B, T, 128, 128]
    output = attn.reshape(B, T, 128*128) @ W_O.T  # [B, T, 7168]
    
    # Cache: only c_kv (512) and k_R (64) — NOT full K,V
    return output, c_kv, k_R


# === DeepSeekMoE with Aux-Loss-Free Balancing ===
def moe_forward(u_t, shared_experts, routed_experts, expert_centroids, bias, K_r=8):
    # u_t: [B, T, 7168]
    
    # Shared expert output (always computed)
    shared_out = sum(expert(u_t) for expert in shared_experts)  # 1 shared expert
    
    # Router scores
    scores = sigmoid(u_t @ expert_centroids.T)  # [B, T, 256]
    
    # Top-K selection WITH bias (bias不参与梯度)
    biased_scores = scores + bias.detach()       # [B, T, 256]
    _, top_k_indices = topk(biased_scores, K_r)  # [B, T, 8]
    
    # Gate values from ORIGINAL scores (no bias)
    selected_scores = gather(scores, top_k_indices)  # [B, T, 8]
    gates = selected_scores / selected_scores.sum(dim=-1, keepdim=True)  # normalize
    
    # Compute weighted expert outputs
    routed_out = sum(gates[:,:,i] * routed_experts[idx](u_t) 
                     for i, idx in enumerate(top_k_indices))
    
    return u_t + shared_out + routed_out  # residual connection


# === Bias update (after each training step, no gradient) ===
def update_bias(bias, expert_load_counts, gamma=0.001):
    target_load = expert_load_counts.sum() / len(bias)
    for i in range(len(bias)):
        if expert_load_counts[i] > target_load:
            bias[i] -= gamma  # overloaded → decrease bias
        else:
            bias[i] += gamma  # underloaded → increase bias


# === MTP Module ===
def mtp_forward(h_prev, tokens_shifted, M_k, trm_k, embed, out_head):
    # h_prev: [B, T-k, 7168] — representation from depth k-1
    # tokens_shifted: token IDs shifted by k positions
    
    tok_emb = embed(tokens_shifted)               # [B, T-k, 7168]
    combined = M_k @ concat(RMSNorm(h_prev), RMSNorm(tok_emb), dim=-1)
    # concat: [B, T-k, 14336] → M_k projects to [B, T-k, 7168]
    
    h_k = trm_k(combined)                         # [B, T-k, 7168]
    logits = out_head(h_k)                         # [B, T-k, vocab_size]
    return h_k, logits
```

---

## 设计决策 (Design Decisions)

### 1. Sigmoid + Top-K归一化 vs Softmax门控

| 方面 | DeepSeek-V3 (Sigmoid+Norm) | 替代方案 (Softmax) |
|------|---------------------------|-------------------|
| 门控计算 | $\sigma(u^T e_i)$后top-K归一化 | $\text{softmax}(u^T e_i)$后top-K |
| 分数耦合 | 各专家分数独立 | 所有专家分数互相竞争 |
| 偏置兼容性 | 偏置加在sigmoid后，不影响其他专家的原始分数 | 偏置加在softmax前会改变所有专家的概率分布 |

论文选择sigmoid是因为它更好地配合了辅助损失-free策略：偏置项只影响"谁被选中"，不影响"选中后的权重"。**论文未做sigmoid vs softmax的消融实验。**

### 2. MTP深度D=1 vs 更深的D

论文设D=1（只预测1个额外token），但Gloeckle et al.使用了更大的D。论文未详细讨论D>1的消融结果，但提到λ从0.3降到0.1（后4.8T tokens），说明MTP是一个辅助目标，权重不宜过大。**论文未讨论D=2或D=3的对比。**

### 3. 序列化MTP vs 并行MTP (Gloeckle et al.)

| 方面 | DeepSeek-V3 (序列化) | Gloeckle et al. (并行) |
|------|---------------------|----------------------|
| 因果链 | 完整——第k个预测依赖第k-1个 | 断裂——各预测头独立 |
| 计算开销 | 更大（串行计算） | 更小（可并行） |
| 推理复用 | 可直接用于speculative decoding（类似EAGLE） | 需要额外适配 |

论文选择序列化方案是为了保持因果链完整性，且MTP模块可在推理时复用于speculative decoding。

### 4. 辅助损失free vs 纯辅助损失 vs batch-wise辅助损失

论文在Section 4.5.3中做了三种方法的对比：
- 序列-wise辅助损失：validation loss = 2.258 (1B) / 2.085 (3B)
- 辅助损失-free：validation loss = 2.253 (1B) / 2.080 (3B)
- Batch-wise辅助损失：validation loss = 2.253 (1B) / 2.080 (3B)

**核心trade-off**：batch-wise方法允许更灵活的域内专家特化（Figure 9验证了aux-loss-free模型的专家特化模式更明显），但面临序列内/小batch内负载不均和推理时domain-shift导致负载不均的挑战。

### 5. FP8格式选择：全E4M3 vs 混合E4M3/E5M2

| 方面 | DeepSeek-V3 (全E4M3) | 常规方案 (E4M3 Fprop + E5M2 Dgrad/Wgrad) |
|------|---------------------|---------------------------------------|
| 精度 | 3-bit mantissa全程 | Dgrad/Wgrad用2-bit mantissa |
| 动态范围 | 较小 | Dgrad/Wgrad有更大动态范围 |

论文归因于fine-grained quantization（tile/block-wise scaling）有效共享了组内元素的指数位，弥补了E4M3较小的动态范围。

---

## 易混淆点 (Potential Confusions)

### ❌ 错误理解1：无辅助损失意味着完全没有任何均衡loss
✅ 正确理解：DeepSeek-V3仍然保留了一个极小权重（α=0.0001）的**序列级**辅助损失（Eq.17），目的是防止单个序列内的极端不均衡。"无辅助损失"指的是不再依赖辅助损失作为主要均衡手段。

### ❌ 错误理解2：偏置项$b_i$参与了梯度反传
✅ 正确理解：$b_i$仅用于确定top-K选择（Eq.16），不参与门控值计算（门控值仍用原始$s_{i,t}$）。$b_i$的更新是基于统计规则（过载减、欠载加），不通过反向传播。因此，它不会产生任何影响主任务学习的梯度。

### ❌ 错误理解3：MTP在推理时也需要额外计算
✅ 正确理解：MTP模块在推理时可以完全丢弃，主模型可以独立正常运行。MTP只是训练时的辅助目标。当然，也可以选择保留MTP模块用于speculative decoding来加速生成。

---

## 实验与归因 (Experiments & Attribution)

## 核心收益

### 预训练基座模型 (Table 3)

DeepSeek-V3-Base（37B激活 / 671B总参数）vs 主要对手：

| 维度 | DeepSeek-V3-Base | Qwen2.5-72B-Base | LLaMA-3.1-405B-Base | 优势 |
|------|-----------------|------------------|---------------------|------|
| BBH | **87.5** | 79.8 | 82.9 | +4.6 vs 次优 |
| MMLU | **87.1** | 85.0 | 84.4 | +2.1 |
| MMLU-Pro | **64.4** | 58.3 | 52.8 | +6.1 |
| DROP (F1) | **89.0** | 80.6 | 86.0 | +3.0 |
| HumanEval | **65.2** | 53.0 | 54.9 | +10.3 |
| MATH | **61.6** | 54.4 | 49.0 | +7.2 |
| GSM8K | **89.3** | 88.3 | 83.5 | +1.0 |
| LiveCodeBench | **19.4** | 12.9 | 15.5 | +3.9 |

关键发现：DeepSeek-V3-Base在代码（HumanEval +10.3 vs LLaMA）和数学（MATH +7.2 vs Qwen）上优势尤为显著。

### Chat模型 (Figure 1 + Table 6)

| 基准 | DeepSeek-V3 | GPT-4o | Claude-3.5-Sonnet |
|------|------------|--------|------------------|
| MMLU-Pro | 75.9 | 73.3 | 78.0 |
| GPQA-Diamond | 59.1 | 49.9 | 65.0 |
| MATH-500 | **90.2** | 74.7 | 78.3 |
| AIME 2024 | **39.2** | 9.3 | 16.0 |
| Codeforces | **51.6** | 23.6 | 20.3 |
| SWE-bench Verified | 42.0 | 38.8 | **50.8** |

在数学和代码竞赛上，DeepSeek-V3显著超越GPT-4o和Claude-3.5-Sonnet。在工程任务（SWE-bench）上略逊于Claude-3.5-Sonnet。

### 训练效率 (Table 1)

| 阶段 | GPU小时 (H800) | 成本 (USD) |
|------|---------------|----------|
| 预训练 | 2,664K | $5.328M |
| 上下文扩展 | 119K | $0.238M |
| 后训练 | 5K | $0.01M |
| **总计** | **2,788K** | **$5.576M** |

每万亿token仅需180K H800 GPU小时，即2048卡集群上3.7天。全部训练不到两个月。

---

## 归因分析 (Ablation Study)

### 1. MTP策略消融 (Table 4) — 贡献排序

在Large MoE模型（228.7B参数，540B tokens）上：

| 基准 | Baseline | w/ MTP | 绝对提升 | 相对提升 |
|------|---------|--------|---------|--------|
| HumanEval | 44.5 | **53.7** | +9.2 | +20.7% |
| MATH | 38.6 | **39.8** | +1.2 | +3.1% |
| GSM8K | 72.3 | **74.0** | +1.7 | +2.4% |
| DROP | 68.5 | **70.6** | +2.1 | +3.1% |
| NaturalQuestions | 27.2 | **28.5** | +1.3 | +4.8% |

MTP在代码任务上提升最大（HumanEval +9.2），其次是推理和数学任务。值得注意的是，MTP不增加推理成本（推理时丢弃MTP模块）。

### 2. 无辅助损失均衡消融 (Table 5) — 贡献排序

在Large MoE模型（228.7B参数，578B tokens）上：

| 基准 | Aux-Loss-Based | Aux-Loss-Free | 绝对提升 |
|------|---------------|---------------|--------|
| HumanEval | 40.2 | **46.3** | +6.1 |
| GSM8K | 70.7 | **74.5** | +3.8 |
| MATH | 37.2 | **39.6** | +2.4 |
| MBPP | 59.2 | **61.2** | +2.0 |
| BBH | 66.7 | **67.9** | +1.2 |
| Pile BPB | 0.656 | **0.652** | -0.004 |

无辅助损失策略在代码（+6.1 HumanEval）和数学（+3.8 GSM8K）上的收益最显著，同时语言建模质量（BPB）也有微小改善。

### 3. Batch-wise vs Sequence-wise均衡 (Section 4.5.3)

1B MoE模型验证损失：sequence-wise aux loss = 2.258, aux-loss-free = 2.253, batch-wise aux loss = 2.253。batch-wise方法与aux-loss-free效果相当，均优于sequence-wise。

### 贡献大小排序

1. **MTP** — 对代码任务贡献最大（HumanEval +9.2 / +20.7%）
2. **无辅助损失均衡** — 对代码和数学均有显著贡献（HumanEval +6.1, GSM8K +3.8）
3. **FP8训练** — 相对BF16基线的loss误差<0.25%，无性能损失的情况下训练速度接近翻倍
4. **R1知识蒸馏** — 在数学推理任务上有显著提升（论文未给出精确消融数字，但定性描述为"notably improves reasoning performance"）

---

## 可信度检查

### 优点
- 所有基线模型使用同一评估框架和设置（"We evaluate all these models with our internal evaluation framework, and ensure that they share the same evaluation setting"），评估公平性较高
- 提供了两个不同规模的消融实验（Small MoE 15.7B 和 Large MoE 228.7B），结论一致性强
- 训练过程"no irrecoverable loss spikes or rollbacks"，说明训练极为稳定
- FP8与BF16的对比在两个模型规模上验证，loss误差<0.25%

### 需要注意的点
- ⚠️ 后训练阶段使用了DeepSeek-R1的蒸馏数据，这使得DeepSeek-V3的推理能力可能部分来源于R1而非架构本身的贡献
- ⚠️ 训练成本$5.576M仅计算了"官方训练"，不包括前期架构搜索、数据处理、消融实验的成本（"excluding the costs associated with prior research and ablation experiments"）
- ⚠️ 评估使用内部框架，虽然声明了公平设置，但第三方独立验证困难
- ⚠️ MTP消融在Large MoE上只训练了540B tokens（vs 正式的14.8T），可能不完全代表最终效果
- ⚠️ 部分基准（如Codeforces percentile、AIME 2024）的样本量较小，可能存在方差

---

## 专家批判 (Critical Review)

## 隐性成本 (Hidden Costs)

### 1. 推理部署的复杂性

论文描述的推理部署方案极其复杂：
- Prefilling需要4节点32 GPU作为最小单元，TP4+EP32+DP8
- Decoding需要40节点320 GPU作为最小单元，TP4+EP320+DP80
- 需要冗余专家部署（32个冗余专家用于prefilling），并定期（~10分钟）根据在线统计重新调整
- 正在探索的"动态冗余"策略需要每层实时计算全局最优路由方案

这意味着：(a) 中小型团队几乎不可能自行部署；(b) 推理成本虽然单次便宜（37B激活参数），但基础设施门槛极高。

### 2. 训练框架的不可复现性

- DualPipe的实现依赖于对H800 GPU的深度优化（SM分配、warp specialization、PTX指令定制）
- FP8训练框架大量依赖NVIDIA Hopper架构的特定硬件行为（如Tensor Core的14-bit累加精度限制）
- 跨节点all-to-all通信内核针对IB/NVLink的具体拓扑定制

换言之，这些工程优化与特定硬件深度绑定，难以在不同硬件平台上复现。

### 3. 数据质量的不可见成本

论文提到"14.8T high-quality and diverse tokens"和"optimized data processing pipeline"，但数据构建的细节（来源、清洗方法、质量过滤标准）几乎未公开。数据工程可能是DeepSeek-V3成功的最大隐性因素之一。

### 4. R1蒸馏的依赖

后训练阶段的推理能力提升很大程度上依赖DeepSeek-R1的蒸馏。R1本身是一个long-CoT模型，其训练成本未计入DeepSeek-V3的$5.576M预算。这意味着实际的"全栈"研发成本远高于报告数字。

---

## 工程落地建议

### 最大的"坑"

1. **专家负载不均衡在推理时更难处理**：训练时batch-wise均衡在大规模EP+DP下自然实现，但推理时（尤其是在线服务场景，请求domain分布变化大）可能出现严重的domain-shift导致负载不均。论文的冗余专家部署方案是一个权宜之计，增加了1/9的推理GPU开销。

2. **MLA的KV cache虽然小，但up-projection在推理时仍然需要计算**：每次attention计算时需要将$c_t^{KV}$（512维）up-project回$k_t^C$和$v_t^C$（各16384维），这增加了推理计算量。论文通过吸收$W^{UK}$和$W^{UV}$到attention计算中来避免显式up-projection，但这需要特殊的kernel实现。

3. **FP8训练的tile/block-wise quantization在非NVIDIA硬件上可能不可用**：论文自己指出Hopper架构不原生支持fine-grained quantization，需要在CUDA Core上做dequantization。Blackwell（下一代）才会原生支持microscaling formats。

4. **MTP模块的训练开销**：虽然推理时可丢弃，但训练时每个MTP模块包含一个完整的Transformer block + 线性投影，增加了训练的计算和内存开销（论文未量化此开销）。

---

## 关联思考

### 与MoE领域
- **vs Switch Transformer / GShard**：DeepSeek-V3的核心创新在于证明了辅助损失是不必要的——简单的偏置调节就能实现更好的均衡，同时让专家获得更好的域内特化。这可能改变MoE社区对负载均衡的共识。
- **vs Mixtral**：Mixtral使用8个大专家选2个，而DeepSeek-V3使用256个小专家选8个+1共享。更细粒度的专家划分允许更精细的路由，但也增加了通信复杂度（部分由node-limited routing缓解）。

### 与FlashAttention
- MLA的低秩压缩与FlashAttention是互补的：FlashAttention优化attention计算的内存访问模式，MLA则从根本上减少了需要存储和计算的KV数量。两者可以同时使用。
- 但MLA的up-projection步骤可能需要定制的FlashAttention kernel来融合，标准FlashAttention实现可能不直接适用。

### 与LoRA / PEFT
- MLA的down-projection/up-projection结构与LoRA的理念惊人相似——都利用低秩假设来压缩信息。不同之处在于MLA在推理时压缩KV cache，LoRA在微调时压缩参数更新。
- 对DeepSeek-V3做LoRA微调时，需要注意MLA的特殊结构：微调目标应该是down-projection矩阵还是up-projection矩阵，值得研究。

### 与知识蒸馏
- R1到V3的蒸馏策略（将长CoT模型的推理能力蒸馏到标准模型中，同时控制输出长度和格式）是一个有实际价值的范式。这意味着可以先训练一个"不计成本"的推理模型，再将其能力迁移到高效的部署模型中。
- 这与OpenAI从o1到GPT-4o的能力迁移路线异曲同工。

---

## 机制迁移分析 (Mechanism Transfer Analysis)

## 机制解耦 (Mechanism Decomposition)

| 原语名称 | 本文用途 | 抽象描述 | 信息论/几何直觉 |
|---------|---------|---------|---------------|
| **低秩联合压缩** (Low-Rank Joint Compression) | MLA中将多头KV联合压缩到低维latent空间 | 对一组高维关联信号，找到其低维公共子空间进行压缩存储，使用时再恢复 | 信息论：多头KV的互信息很高，联合编码的rate远低于独立编码；几何：多头KV分布在一个低维流形上，down-projection是找到该流形的线性近似 |
| **无梯度偏置调节** (Gradient-Free Bias Steering) | 无辅助损失的MoE负载均衡 | 在离散选择（routing）过程中，引入不参与梯度的偏置项来调节选择倾向，同时保持选择后的权重（gate）不受影响 | 控制论：类似PID控制器的积分项，根据误差（负载偏差）持续调节；信息论：将"选谁"的决策与"选了之后给多大权重"解耦，避免辅助目标污染主信号 |
| **因果链式辅助预测** (Causal Chain Auxiliary Prediction) | MTP通过串联模块预测多个未来token | 在主预测目标之外，构建一条保持因果依赖的辅助预测链，每步预测都依赖前一步的表征+新输入 | 信息论：增加了训练信号的互信息密度（每个位置从1个标签变为D+1个标签）；几何：强迫模型的中间表征包含对更远未来有预测力的特征，扩大了表征的"时间感受野" |
| **细粒度混合精度量化** (Fine-Grained Mixed Precision Quantization) | FP8训练中按tile(1×128)/block(128×128)分组量化 | 对张量按局部区域分组，每组独立计算scaling factor，在精度损失和存储/计算效率间取得更好的trade-off | 信息论：局部量化相当于分段自适应编码，比全局统一编码更接近信源的率失真下界；几何：outlier只影响局部组的scale，不会"拖累"全局其他元素的精度 |

---

## 迁移处方 (Transfer Prescription)

### 原语1：低秩联合压缩

**场景A：推荐系统中的用户行为序列建模**
- **目标领域**：长序列用户行为建模（如Transformer4Rec中的用户点击序列）
- **怎么接**：在多头self-attention中，将用户行为token的KV表征通过down-projection压缩后存储，只缓存低维latent。对于千级别的行为序列，KV cache的内存从O(T·n_h·d_h)降至O(T·d_c)
- **预期收益**：支持更长的用户行为序列（如从256扩展到4096+），在embedding-based的推荐模型中尤为关键
- **风险**：如果不同用户行为token的KV分布差异很大（如异构行为类型混合），低秩假设可能不成立，需要验证压缩后的注意力质量

**场景B：多模态模型的视觉token压缩**
- **目标领域**：视觉-语言模型（VLM）中的视觉token过多导致推理慢
- **怎么接**：对视觉encoder输出的多头KV进行联合低秩压缩，减少视觉token在cross-attention中的缓存需求
- **预期收益**：在保持视觉理解能力的同时，将视觉token的KV cache压缩10-50倍
- **风险**：视觉信息的冗余程度可能低于语言（局部细节信息多），需要较高的压缩维度

### 原语2：无梯度偏置调节

**场景A：多任务学习中的任务路由**
- **目标领域**：多任务学习（MTL）中的动态任务权重调节
- **怎么接**：在hard parameter sharing + task-specific head的MTL架构中，用偏置项引导样本路由到不同的专家子网络，偏置根据各任务的loss均衡程度动态调整
- **预期收益**：避免任务权重（辅助损失）的超参敏感性问题，让各任务自然均衡
- **风险**：如果任务间存在根本性冲突（negative transfer），偏置调节可能无法解决，需要架构层面的隔离

**场景B：联邦学习中的client selection**
- **目标领域**：异构联邦学习中选择参与训练的client
- **怎么接**：为每个client维护一个参与偏置，根据历史参与频率动态调整，过多参与的client降低偏置、参与不足的增加偏置
- **预期收益**：无需设计复杂的client selection策略即可实现参与均衡
- **风险**：client的数据质量差异可能需要被保留（让高质量client参与更多），而非被均衡掉

### 原语3：因果链式辅助预测

**场景A：时间序列预测中的多步预测**
- **目标领域**：长期时间序列预测（如PatchTST、iTransformer）
- **怎么接**：在单步预测基础上，串联D个轻量级预测模块，第k个模块利用第k-1步的表征+第k个真实值embedding来预测第k+1步。训练时提供D+1步监督信号
- **预期收益**：训练信号密度提高D+1倍，模型被迫在中间表征中编码长期趋势信息
- **风险**：时间序列的非平稳性可能使得"预判未来"的能力在distribution shift下失效

**场景B：蛋白质序列建模中的motif预测**
- **目标领域**：蛋白质语言模型（如ESM）
- **怎么接**：在masked language modeling基础上，增加一个辅助目标：预测当前位置后续k个氨基酸的类型
- **预期收益**：强迫模型学习长程结构依赖（如alpha-helix、beta-sheet的序列模式）
- **风险**：蛋白质序列的局部依赖可能不如自然语言强，需要调整预测深度D

---

## 机制家族图谱 (Mechanism Family Tree)

### 1. 低秩联合KV压缩 (MLA)

**前身 (Ancestors):**
- **Multi-Query Attention (MQA)** (Shazeer, 2019)：所有头共享一组KV → 极致压缩但性能损失大。MLA可视为MQA的"软"版本——不是共享KV，而是共享KV的低秩表示
- **Grouped-Query Attention (GQA)** (Ainslie et al., 2023)：将头分组共享KV → 折中方案。MLA进一步：不分组，而是所有头从一个shared latent恢复各自的KV
- **Linear Attention** (Katharopoulos et al., 2020)：用低秩核近似attention → MLA的低秩思想类似，但作用在KV cache层面而非attention kernel

**兄弟 (Siblings):**
- **Cross-Layer Attention** (不同layer共享KV cache)：与MLA正交的压缩维度
- **Paged Attention** (vLLM)：优化KV cache的内存管理，而非压缩KV本身

**后代 (Descendants):**
- DeepSeek后续模型可能进一步探索非线性latent空间（如VAE-style KV compression）
- MiniMax-01等模型已开始采用类似的latent attention设计

**创新增量**：MLA的核心创新在于"联合压缩K和V到同一个latent空间"（而非独立压缩），并用解耦的RoPE key解决了位置编码与压缩的冲突。

### 2. 无辅助损失负载均衡

**前身 (Ancestors):**
- **Auxiliary Load Balancing Loss** (Shazeer et al., 2017; Fedus et al., 2021)：标准方案，DeepSeek-V3要替代的对象
- **Expert Choice Routing** (Zhou et al., 2022)：让专家选token而非token选专家 → 自然均衡但破坏因果性

**兄弟 (Siblings):**
- **Router z-loss** (Zoph et al., 2022)：正则化router logits的大小 → 间接促进均衡
- **Hash routing** (Roller et al., 2021)：确定性均衡但牺牲了自适应性

**后代 (Descendants):**
- Wang et al. (2024a) 是本策略的原始论文，DeepSeek-V3是其首次大规模验证
- 该策略可能启发MoE社区重新审视辅助损失的必要性

**创新增量**：将"选择"与"加权"解耦——偏置影响选择，但不影响选中后的权重——这是一个简单但被忽略的设计，避免了辅助损失对主梯度的污染。

### 3. 多Token预测 (MTP)

**前身 (Ancestors):**
- **Multi-Token Prediction** (Gloeckle et al., 2024, Meta)：并行独立预测多个未来token → 缺乏因果链
- **EAGLE** (Li et al., 2024b)：在speculative decoding中维护因果链预测 → 目标是加速推理，不是增强训练

**兄弟 (Siblings):**
- **Medusa** (Cai et al., 2024)：为speculative decoding训练多个独立头 → 类似Gloeckle的并行方案
- **Lookahead Decoding**：利用Jacobi迭代并行生成 → 不同的加速思路

**后代 (Descendants):**
- DeepSeek-V3的MTP模块可直接复用于speculative decoding（Table 7显示acceptance rate为85-91%）
- 未来可能探索D>1的更深MTP或非线性组合方案

**创新增量**：将Gloeckle的"并行"改为"串行+因果链"，同时共享embedding和output head以减少参数开销。目标从"纯训练增强"扩展到"训练增强+推理加速"双重用途。

---

## 背景知识补充 (Background Context)

## 背景知识补充

### 1. Mixture-of-Experts (MoE)

MoE是一种稀疏激活架构，每个token只激活部分参数（专家），从而在保持模型容量的同时降低推理计算量。关键组件包括：
- **Router/Gating Network**：决定每个token被发送到哪些专家。常见方案有top-K routing (Shazeer et al., 2017)、expert choice routing (Zhou et al., 2022)
- **负载均衡**：确保各专家被均匀使用，避免routing collapse。标准方法是辅助损失 (Fedus et al., 2021)
- **GShard** (Lepikhin et al., 2021) 和 **Switch Transformer** (Fedus et al., 2021) 是代表性工作

### 2. Rotary Position Embedding (RoPE)

Su et al. (2024)提出的位置编码方案，通过旋转矩阵将位置信息编码到Q和K中。在MLA中的挑战是：如果对压缩后的KV施加RoPE，位置编码会与低秩压缩纠缠，导致无法复用缓存的latent向量。DeepSeek-V2的解决方案是"解耦RoPE"：单独计算一个携带RoPE的key（$k_t^R$），与content key拼接。

### 3. YaRN (Yet another RoPE extensioN)

Peng et al. (2023a)提出的RoPE外推方法，通过调整RoPE的基频来扩展上下文长度。DeepSeek-V3使用YaRN将预训练的4K上下文扩展到32K再到128K。

### 4. GRPO (Group Relative Policy Optimization)

DeepSeek自研的RL算法，替代PPO。核心思想是在一组采样输出中进行相对排序来计算优势函数，而不需要单独的critic模型。在DeepSeek-V3的后训练阶段使用。

### 5. Fill-in-Middle (FIM)

一种预训练数据增强策略，将文档随机分为prefix/suffix/middle三部分，训练模型根据prefix和suffix预测middle。使用PSM (Prefix-Suffix-Middle)格式。DeepSeek-V3以0.1的比率应用FIM。

### 6. Pipeline Parallelism (PP)

将模型的不同层分配到不同GPU上，数据以micro-batch的形式流水线式通过各层。关键挑战是pipeline bubble（GPU空闲时间）。常见方案：
- **1F1B** (Harlap et al., 2018)：交替执行前向和反向
- **ZeroBubble** (Qi et al., 2023b)：将反向拆分为input-grad和weight-grad以减少bubble
- **DualPipe** (本文)：双向流水线+计算/通信重叠

### 7. Speculative Decoding

Leviathan et al. (2023)和Xia et al. (2023)提出的推理加速方法：用小模型（draft model）快速生成多个候选token，再用大模型并行验证。DeepSeek-V3的MTP模块可直接作为draft model使用，Table 7显示acceptance rate达85-91%。
