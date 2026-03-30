---
abstract: General reasoning represents a long-standing and formidable challenge in
  artificial intelligence. Recent breakthroughs, exemplified by large language models
  (LLMs) and chain-of-thought prompting, have achieved considerable success on foundational
  reasoning tasks. However, this success is heavily contingent upon extensive human-annotated
  demonstrations, and models&#39; capabilities are still insufficient for more complex
  problems. Here we show that the reasoning abilities of LLMs can be incentivized
  through pure reinforcement learning (RL), obviating the need for human-labeled reasoning
  trajectories. The proposed RL framework facilitates the emergent development of
  advanced reasoning patterns, such as self-reflection, verification, and dynamic
  strategy adaptation. Consequently, the trained model achieves superior performance
  on verifiable tasks such as mathematics, coding competitions, and STEM fields, surpassing
  its counterparts trained via conventional supervised learning on human demonstrations.
  Moreover, the emergent reasoning patterns exhibited by these large-scale models
  can be systematically harnessed to guide and enhance the reasoning capabilities
  of smaller models.
arxiv_categories:
- cs.CL
arxiv_id: '2501.12948'
authors:
- DeepSeek-AI
- Daya Guo
- Dejian Yang
- Haowei Zhang
- Junxiao Song
- Peiyi Wang
- Qihao Zhu
- Runxin Xu
- Ruoyu Zhang
- Shirong Ma
- Xiao Bi
- Xiaokang Zhang
- Xingkai Yu
- Yu Wu
- Z. F. Wu
- Zhibin Gou
- Zhihong Shao
- Zhuoshu Li
- Ziyi Gao
- Aixin Liu
- Bing Xue
- Bingxuan Wang
- Bochao Wu
- Bei Feng
- Chengda Lu
- Chenggang Zhao
- Chengqi Deng
- Chenyu Zhang
- Chong Ruan
- Damai Dai
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
- Honghui Ding
- Huajian Xin
- Huazuo Gao
- Hui Qu
- Hui Li
- Jianzhong Guo
- Jiashi Li
- Jiawei Wang
- Jingchang Chen
- Jingyang Yuan
- Junjie Qiu
- Junlong Li
- J. L. Cai
- Jiaqi Ni
- Jian Liang
- Jin Chen
- Kai Dong
- Kai Hu
- Kaige Gao
- Kang Guan
- Kexin Huang
- Kuai Yu
- Lean Wang
- Lecong Zhang
- Liang Zhao
- Litong Wang
- Liyue Zhang
- Lei Xu
- Leyi Xia
- Mingchuan Zhang
- Minghua Zhang
- Minghui Tang
- Meng Li
- Miaojun Wang
- Mingming Li
- Ning Tian
- Panpan Huang
- Peng Zhang
- Qiancheng Wang
- Qinyu Chen
- Qiushi Du
- Ruiqi Ge
- Ruisong Zhang
- Ruizhe Pan
- Runji Wang
- R. J. Chen
- R. L. Jin
- Ruyi Chen
- Shanghao Lu
- Shangyan Zhou
- Shanhuang Chen
- Shengfeng Ye
- Shiyu Wang
- Shuiping Yu
- Shunfeng Zhou
- Shuting Pan
- S. S. Li
- Shuang Zhou
- Shaoqing Wu
- Shengfeng Ye
- Tao Yun
- Tian Pei
- Tianyu Sun
- T. Wang
- Wangding Zeng
- Wanjia Zhao
- Wen Liu
- Wenfeng Liang
- Wenjun Gao
- Wenqin Yu
- Wentao Zhang
- W. L. Xiao
- Wei An
- Xiaodong Liu
- Xiaohan Wang
- Xiaokang Chen
- Xiaotao Nie
- Xin Cheng
- Xin Liu
- Xin Xie
- Xingchao Liu
- Xinyu Yang
- Xinyuan Li
- Xuecheng Su
- Xuheng Lin
- X. Q. Li
- Xiangyue Jin
- Xiaojin Shen
- Xiaosha Chen
- Xiaowen Sun
- Xiaoxiang Wang
- Xinnan Song
- Xinyi Zhou
- Xianzu Wang
- Xinxia Shan
- Y. K. Li
- Y. Q. Wang
- Y. X. Wei
- Yang Zhang
- Yanhong Xu
- Yao Li
- Yao Zhao
- Yaofeng Sun
- Yaohui Wang
- Yi Yu
- Yichao Zhang
- Yifan Shi
- Yiliang Xiong
- Ying He
- Yishi Piao
- Yisong Wang
- Yixuan Tan
- Yiyang Ma
- Yiyuan Liu
- Yongqiang Guo
- Yuan Ou
- Yuduan Wang
- Yue Gong
- Yuheng Zou
- Yujia He
- Yunfan Xiong
- Yuxiang Luo
- Yuxiang You
- Yuxuan Liu
- Yuyang Zhou
- Y. X. Zhu
- Yanhong Xu
- Yanping Huang
- Yaohui Li
- Yi Zheng
- Yuchen Zhu
- Yunxian Ma
- Ying Tang
- Yukun Zha
- Yuting Yan
- Z. Z. Ren
- Zehui Ren
- Zhangli Sha
- Zhe Fu
- Zhean Xu
- Zhenda Xie
- Zhengyan Zhang
- Zhewen Hao
- Zhicheng Ma
- Zhigang Yan
- Zhiyu Wu
- Zihui Gu
- Zijia Zhu
- Zijun Liu
- Zilin Li
- Ziwei Xie
- Ziyang Song
- Zizheng Pan
- Zhen Huang
- Zhipeng Xu
- Zhongyu Zhang
- Zhen Zhang
baselines:
- OpenAI o1-1217
- OpenAI o1-mini
- GPT-4o-0513
- Claude-3.5-Sonnet-1022
- DeepSeek-V3
category: llm/reasoning
code_url: https://huggingface.co/deepseek-ai
core_contribution: new-method/new-framework
datasets:
- MMLU
- MMLU-Redux
- MMLU-Pro
- C-Eval
- CMMLU
- IFEval
- FRAMES
- GPQA Diamond
- SimpleQA
- C-SimpleQA
- SWE-Bench Verified
- Aider-Polyglot
- LiveCodeBench
- Codeforces
- CNMO 2024
- AIME 2024
- MATH-500
- DROP
- AlpacaEval 2.0
- ArenaHard
- CLUEWSC
date: '2025-01-22'
doi: null
keywords:
- reinforcement learning
- chain-of-thought reasoning
- GRPO
- LLM post-training
- rule-based reward
- knowledge distillation
- emergent reasoning
- self-evolution
- Mixture-of-Experts
- test-time scaling
metrics:
- Pass@1
- Cons@16
- EM
- F1
- Prompt Strict
- LC-winrate
- Percentile
- Rating
- Resolved
- Accuracy
- Correct
publication_type: preprint
status: complete
tags:
- reinforcement learning
- chain-of-thought reasoning
- GRPO
- LLM post-training
- knowledge distillation
- emergent reasoning
- test-time scaling
- Mixture-of-Experts
title: 'DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement
  Learning'
tldr: 通过纯强化学习（GRPO算法+规则奖励）直接在预训练基座上训练，无需人工标注推理轨迹，LLM自主涌现自我反思与验证等高级推理行为，在数学竞赛和编程任务上达到与OpenAI
  o1匹敌的SOTA水平。
url: https://arxiv.org/abs/2501.12948
venue: null
---

## 核心速览 (Executive Summary)

### TL;DR (≤100字)

DeepSeek-R1证明**纯强化学习**（GRPO+规则奖励）可在预训练LLM上直接激发高级推理能力，无需人工标注推理轨迹。模型自主涌现自我反思、验证与策略切换等行为，在AIME数学竞赛（79.8%）和Codeforces编程（96.3%百分位）上达到与OpenAI o1匹敌的水平。

### 一图流 (Mental Model)

如果传统SFT是**手把手教学生解题步骤**（学生只能复制老师的方法），那么DeepSeek-R1的纯RL方法就是**只告诉学生答案对不对，让他自己摸索出解题策略**——结果学生不仅学会了，还自发发明了老师没教过的技巧（回溯检验、换方法重试）。更进一步，R1的完整pipeline则是先让学生自由探索（RL），再用他发现的好方法编成教材教给其他学生（蒸馏）。

### 核心机制一句话 (Mechanism in One Line)

**[采样]** 对每个推理问题的多个候选回答 **[评估]** 仅以最终答案正确性给予二值奖励 **[优化]** 通过组内相对优势排序的策略梯度更新 **[涌现]** 模型自主发展出长链推理、自我反思和动态策略适应行为。

---

## 动机与第一性原理 (Motivation & First Principles)

### 痛点 (The Gap)

此前的SOTA推理方法存在三个核心瓶颈：

1. **人工标注瓶颈**：传统SFT+CoT（如InstructGPT、GPT-4的post-training）严重依赖人工标注的推理轨迹。标注高质量数学证明和代码推理的成本极高，且难以规模化。
2. **认知偏见天花板**：人类标注者提供的推理路径受自身认知模式限制——例如人类习惯线性思维，但最优推理路径可能需要回溯、并行探索等非人类直觉的策略。SFT将模型锁定在人类思维模式中，阻止了更优推理路径的发现。
3. **过程奖励模型的脆弱性**：Process-based Reward Model（PRM）虽然提供更细粒度的反馈，但在大规模RL训练中极易被reward hacking利用（如Figure 6所示，奖励持续上升但Codeforces实际性能下降）。且重新训练PRM需要巨大算力，增加了pipeline的复杂度。

### 核心洞察 (Key Insight)

作者发现了一条被忽视的因果链：

**Because** 预训练base model在海量数学/代码网页数据上已经隐式习得了推理能力的"种子"（DeepSeek-V3-Base的预训练数据包含大量数学和代码内容）
→ **Therefore** 只要给予足够简单但可靠的结果反馈信号（答案对/错的二值奖励），而不需要教模型"如何"推理
→ **Then** 模型会在RL探索的压力下自主发展出验证（verification）、反思（reflection）、策略切换（dynamic strategy adaptation）等高级推理行为
→ **Result** 这些自发涌现的推理模式甚至**优于**人工设计的推理模板，因为它们是模型在特定计算架构约束下的最优适应

关键证据：DeepSeek-R1-Zero在训练过程中自然出现了"aha moment"（Table 2），模型学会了使用"Wait"来触发重新思考，这一行为完全未被人为设计。

### 物理/直觉解释

用大白话说：预训练就像一个人读了几百万本数学书和代码——他"懂"很多东西，但没有系统地"练"过解题。传统SFT是请名师写出标准解法让他背诵——他能解常规题，但遇到超纲题就傻了，因为他只会背过的套路。

纯RL则是直接把他扔进考场，只告诉他每道题答对没有。开始他乱猜，但因为他脑子里有那些书的底子，慢慢就摸索出了自己的方法——先试一种方法，不确定就换一种，算完了回头检查一遍。这些策略不是谁教他的，是他为了"考高分"自己琢磨出来的。而且因为没有被"标准答案的推理过程"限制，他可能发现比老师更聪明的解法。

---

## 方法详解 (Methodology)

## 直觉版 (Intuitive Walk-through)

### 论文方法概览（参考Figure 2）

Figure 2展示了DeepSeek-R1的完整多阶段pipeline，从左到右分为5个关键阶段：

**旧方法（标准Post-Training Pipeline）的数据流：**
```
Base Model → SFT（人工标注的输入-输出对）→ RLHF（PPO + 价值模型 + 神经网络奖励模型）→ Final Model
```

**新方法（DeepSeek-R1 Pipeline）的数据流：**
```
DeepSeek-V3-Base → Cold Start SFT（千级CoT数据）→ 第一阶段RL（GRPO + 规则奖励）
                 → Rejection Sampling + SFT（80万样本）→ 第二阶段RL（规则 + 偏好奖励）→ DeepSeek-R1
```

**关键差异详解：**

| 维度 | 旧方法 | DeepSeek-R1 | 改进原因 |
|------|--------|-------------|----------|
| RL算法 | PPO（需要价值模型） | GRPO（组内相对优势） | 去掉价值模型，减50%内存，避免长CoT下价值估计困难 |
| 奖励信号 | 神经网络奖励模型 | 规则奖励（答案正确性） | 避免reward hacking，更可靠 |
| 训练顺序 | SFT → RL | RL → SFT → RL | 先让模型自由探索推理模式，再整理格式 |
| 推理过程约束 | 人工标注的推理轨迹 | 仅约束输出格式（<think>标签） | 不限制推理内容，允许模型发现非人类策略 |

**用最简单的例子走一遍差异：**

假设有一道数学题 "求 √(a - √(a+x)) = x 的解之和"：

- **旧方法做一步**：用人工标注的标准解法（先平方，再整理，求解四次方程）作为SFT目标，模型学会复制这个固定流程。
- **新方法做一步**：模型生成16个不同的尝试。有的直接求解成功（奖励=1），有的走到死胡同后说"Wait, let me reevaluate"然后换方法成功（奖励=1），有的算错了（奖励=0）。GRPO计算这16个回答的相对优势，提升成功策略的概率，降低失败策略的概率。
- **差异所在**：旧方法的模型只会"一种标准解法"；新方法的模型学会了"尝试 → 验证 → 回溯 → 换方法"的元策略，这正是Table 2中"aha moment"展示的行为。

### R1-Zero vs R1的关系

R1-Zero是纯RL验证实验（概念验证），证明纯RL即可涌现推理能力，但存在可读性差、语言混合等问题。R1是工程优化版本，通过多阶段pipeline解决这些问题，同时保持推理能力。

---

## 精确版 (Formal Specification)

### 流程图 (Text-based Flow)

```
Input: 问题 q (string)
  ↓
[Rollout] 从当前策略 π_θ_old 采样 G=16 个回答 {o_1, ..., o_16}
  每个 o_i: 最长 32768/65536 tokens
  ↓
[Rule-based Reward] 对每个 o_i 计算奖励 r_i
  r_i = r_accuracy + r_format
  r_accuracy ∈ {0, 1}（数学：答案匹配；代码：通过测试用例）
  r_format ∈ {0, 1}（是否包含 <think>...</think> 标签）
  ↓
[Advantage Computation] 组内标准化
  A_i = (r_i - mean(r_1,...,r_G)) / std(r_1,...,r_G)
  ↓
[Policy Update] GRPO目标函数优化 π_θ
  clip ratio ε=10, KL系数 β=0.001
  ↓
Output: 更新后的策略 π_θ
```

### 关键公式与变量

**公式1：GRPO目标函数**

$$J_{GRPO}(\theta) = \mathbb{E} \left[ \frac{1}{G} \sum_{i=1}^{G} \left( \min\left( \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{old}}(o_i|q)} A_i, \text{clip}\left(\frac{\pi_\theta(o_i|q)}{\pi_{\theta_{old}}(o_i|q)}, 1-\varepsilon, 1+\varepsilon\right) A_i \right) - \beta D_{KL}(\pi_\theta || \pi_{ref}) \right) \right]$$

| 符号 | 数学定义 | 物理含义 |
|------|---------|----------|
| $\pi_\theta$ | 当前策略（LLM参数θ下的条件概率） | 模型"现在"生成回答的方式 |
| $\pi_{\theta_{old}}$ | 采样时的策略快照 | 模型"之前"生成回答的方式（用于importance sampling） |
| $\pi_{ref}$ | 参考策略（每400步更新为最新策略） | 防止策略偏离太远的"锚点" |
| $G=16$ | 每个问题的采样数 | 组大小，用于估计相对优势 |
| $\varepsilon=10$ | clip范围 | 限制单步策略更新幅度（注意：比标准PPO的0.2大50倍） |
| $\beta=0.001$ | KL惩罚系数 | 控制策略与参考策略的偏离程度 |
| $A_i$ | 第i个回答的优势值 | 该回答相对于组内平均水平的好坏程度 |

**公式2：组内优势计算**

$$A_i = \frac{r_i - \text{mean}(\{r_1, r_2, \cdots, r_G\})}{\text{std}(\{r_1, r_2, \cdots, r_G\})}$$

物理含义：不需要额外的价值网络，直接用同一问题的G个回答互相比较。正确回答获得正优势，错误回答获得负优势，优势的绝对值取决于正确率的"稀缺程度"。

**公式3：KL散度（无偏估计）**

$$D_{KL}(\pi_\theta || \pi_{ref}) = \frac{\pi_{ref}(o_i|q)}{\pi_\theta(o_i|q)} - \log\frac{\pi_{ref}(o_i|q)}{\pi_\theta(o_i|q)} - 1$$

关键细节：GRPO将KL散度**直接加入loss**（Eq.11），而PPO将per-token KL作为**密集奖励**。后者会隐式惩罚长回答（累积KL更大），阻碍模型发展长CoT。

**公式4：第二阶段综合奖励**

$$Reward = Reward_{reasoning} + Reward_{general} + Reward_{language}$$

其中：
- $Reward_{reasoning} = Reward_{rule}$（规则奖励，同R1-Zero）
- $Reward_{general} = Reward_{reward\_model} + Reward_{format}$（神经网络偏好奖励 + 格式奖励）
- $Reward_{language} = \frac{Num(Words_{target})}{Num(Words)}$（目标语言词汇占比，缓解语言混合）

### 数值推演 (Numerical Example)

**场景**：一道AIME数学题，G=16个采样中有4个正确、12个错误。

**Step 1：计算奖励**
- 正确回答：$r_i = 1$（4个）
- 错误回答：$r_i = 0$（12个）

**Step 2：计算优势**
- $\text{mean} = (4 \times 1 + 12 \times 0) / 16 = 0.25$
- $\text{std} = \sqrt{\frac{4 \times (1-0.25)^2 + 12 \times (0-0.25)^2}{16}} = \sqrt{\frac{4 \times 0.5625 + 12 \times 0.0625}{16}} = \sqrt{\frac{3.0}{16}} \approx 0.433$
- 正确回答优势：$A = (1 - 0.25) / 0.433 \approx +1.73$
- 错误回答优势：$A = (0 - 0.25) / 0.433 \approx -0.577$

**Step 3：策略更新方向**
- 正确回答（A=+1.73）：策略梯度**提升**这些回答中每个token的生成概率
- 错误回答（A=-0.577）：策略梯度**降低**这些回答中每个token的生成概率
- 注意：正确但稀缺的回答获得更高的正优势，推动策略更强烈地学习这些"难能可贵"的正确策略

**直觉**：如果16个回答全对（std=0），优势无法计算（除以0），此题不产生训练信号——这符合直觉，"太简单的题"不提供学习信息。反之，如果只有1个正确（更稀缺），其优势更高（约+3.87），学习信号更强。

### 伪代码 (Pseudocode)

```python
# DeepSeek-R1-Zero GRPO Training Loop
# Model: DeepSeek-V3-Base (671B MoE, 37B activated)

for step in range(10400):  # 1.6 epochs total
    # === Rollout Phase ===
    questions = sample_batch(training_set, batch_size=32)  # 32 unique questions
    
    for q in questions:
        max_len = 32768 if step < 8200 else 65536  # length increase at step 8.2k
        outputs = []  # G=16 samples per question
        for _ in range(16):
            o = policy_old.generate(q, temperature=1.0, max_tokens=max_len)
            # o shape: (seq_len,) where seq_len varies per sample
            outputs.append(o)
    
    # === Reward Computation ===
    rewards = []
    for q, o in zip(questions_expanded, all_outputs):
        r_acc = 1.0 if check_answer(o, ground_truth[q]) else 0.0  # rule-based
        r_fmt = 1.0 if has_think_tags(o) else 0.0
        rewards.append(r_acc + r_fmt)
    
    # === Advantage Computation (per group of G=16) ===
    advantages = []
    for group in chunk(rewards, G=16):  # 每个问题的16个奖励
        mean_r = mean(group)
        std_r = std(group)
        group_advantages = [(r - mean_r) / (std_r + 1e-8) for r in group]
        advantages.extend(group_advantages)
    
    # === Policy Update (GRPO) ===
    # Split 8192 outputs into 16 mini-batches, 1 inner epoch
    mini_batches = random_split(all_data, num_splits=16)
    for mb in mini_batches:
        ratio = policy.log_prob(mb.outputs) - policy_old.log_prob(mb.outputs)
        ratio = exp(ratio)  # π_θ(o|q) / π_θ_old(o|q)
        
        # Clipped surrogate objective
        surr1 = ratio * mb.advantages
        surr2 = clip(ratio, 1 - 10, 1 + 10) * mb.advantages  # ε=10!
        policy_loss = -mean(min(surr1, surr2))
        
        # KL penalty (unbiased estimator)
        kl = ref_policy.log_prob(mb.outputs) / policy.log_prob(mb.outputs) \
             - log(ref_policy.log_prob(mb.outputs) / policy.log_prob(mb.outputs)) - 1
        kl_loss = 0.001 * mean(kl)  # β=0.001
        
        loss = policy_loss + kl_loss
        loss.backward()
        optimizer.step(lr=3e-6)
    
    # Update reference model every 400 steps
    if step % 400 == 0:
        ref_policy = copy(policy)
```

---

## 设计决策 (Design Decisions)

### 决策1：GRPO vs PPO

| 方面 | PPO | GRPO | 论文选择 |
|------|-----|------|----------|
| 价值模型 | 需要（与策略模型同等规模） | **不需要** | GRPO ✓ |
| 内存开销 | 2× 模型内存 | 1× 模型内存 | GRPO ✓ |
| 长CoT适配 | 价值模型难以预测长序列最终奖励 | 直接用结果比较，无此问题 | GRPO ✓ |
| 性能 | λ=1.0时接近GRPO（Figure 4） | 基准线 | 相当 |
| 超参敏感度 | 对GAE的λ非常敏感 | 相对稳定 | GRPO ✓ |

论文在Figure 4中用DeepSeek-Coder-V2-Lite (16B MoE)做了直接对比。PPO在默认λ=0.95时**显著落后**GRPO；调到λ=1.0后性能接近但仍需额外调参成本。结论：GRPO在大规模场景下更实用。

### 决策2：规则奖励 vs 神经网络奖励模型

- **替代方案**：Outcome-based RM、Process-based RM
- **论文选择**：规则奖励（答案匹配 + 编译器验证）
- **核心trade-off**：可靠性 vs 覆盖范围
  - 规则奖励极其可靠但只能覆盖有确定答案的任务（数学、代码）
  - 神经网络RM覆盖范围广但在大规模RL中易被hack（Figure 6展示了奖励上升但Codeforces性能下降的reward hacking现象）
- **论文做法**：推理任务用规则奖励，通用任务才用神经网络RM，且限制RM训练步数（仅最后400步）

### 决策3：RL-first vs SFT-first（训练顺序）

- **传统方案**：先SFT学习基本格式和推理，再RL优化
- **论文假设**：SFT会"限制模型探索"——人工标注的推理过程并非最优，会将模型锁定在次优路径上
- **验证**：R1-Zero（纯RL，无SFT）在AIME上达77.9%，证明假设成立
- **实际工程妥协**：R1仍然使用了cold-start SFT（千级数据），但目的是改善可读性和用户体验，非教授推理能力

### 决策4：极大的clip ratio ε=10

- **标准PPO**：ε = 0.1~0.2
- **论文选择**：ε = 10（大50-100倍）
- **原因**：长CoT推理中，某些关键token的策略概率可能极低。标准clip ratio会截断大量token的梯度，导致训练信号过弱。大clip ratio允许更大的策略更新幅度。
- **论文指出**："A lower value can lead to the truncation of gradients for a significant number of tokens, thereby degrading the model's performance, while a higher value may cause instability during training." 这是一个重要的工程发现。

### 决策5：语言一致性奖励

- **问题**：R1-Zero在推理过程中经常混合中英文
- **方案**：添加语言一致性奖励 $R_{lang} = Num(Words_{target}) / Num(Words)$
- **trade-off**：Supplementary B.6的消融实验表明，语言一致性奖励会导致**推理性能轻微下降**，但显著改善了可读性和用户体验
- 论文未讨论的替代方案：使用语言检测模型作为更精细的奖励、在SFT阶段强制语言一致性 — **论文未讨论**

---

## 易混淆点 (Potential Confusions)

### 混淆1："纯RL"的含义

- ❌ **错误理解**：R1-Zero完全没有任何监督信号，是无监督学习
- ✅ **正确理解**：R1-Zero有明确的监督信号——答案正确性奖励（0/1）和格式奖励。"纯RL"是指没有**人工标注的推理过程**作为SFT目标，而非没有任何反馈。模型收到的是outcome-level supervision，而非process-level supervision。

### 混淆2："涌现推理"的来源

- ❌ **错误理解**：推理能力完全由RL从零创造，与预训练无关
- ✅ **正确理解**：预训练阶段的海量数学/代码数据是推理能力的**种子**。论文明确指出："DeepSeek-V3-Base has been exposed to a significant volume of reasoning trace data. This extensive exposure equips the model with the capability to generate plausible solution candidates, from which reinforcement learning can effectively identify and optimize high-quality outputs." RL的角色是**激活和优化**预训练中已经存在的潜在能力，而非从零创建。

### 混淆3：GRPO与PPO的本质区别

- ❌ **错误理解**：GRPO只是PPO去掉了value model的简化版，两者效果差距很大
- ✅ **正确理解**：除了去掉value model外，GRPO还有一个关键区别——**KL散度的处理方式**。PPO将per-token KL作为密集奖励添加到每个token，这会**隐式惩罚长回答**（token越多累积KL越大），从而阻碍模型发展长CoT。GRPO将KL直接加入loss函数，不对长度产生偏见。这个区别对长链推理模型至关重要。在Figure 4中，PPO调到λ=1.0后性能可接近GRPO，说明核心差异可能更多在KL处理上。

---

## 实验与归因 (Experiments & Attribution)

### 核心收益 (Key Gains)

#### DeepSeek-R1-Zero的训练动态（Figure 1）

| 阶段 | AIME Pass@1 | 响应长度 |
|------|------------|----------|
| 训练初期（step 0） | 15.6% | ~3000 tokens |
| 训练中期（step 5000） | ~55% | ~8000 tokens |
| 长度扩展后（step 8200+） | ~72% | ~12000 tokens |
| 训练结束（step 10400） | 77.9% | ~15000 tokens |
| + Cons@16 | 86.7% | - |

关键观察：性能与思考长度**同步增长**，模型自发学会"用更多时间思考"来解决更难的问题。在step 8200处，最大长度从32768扩展到65536时，出现了性能和长度的**同步跃升**。

#### DeepSeek-R1 vs 竞品（Table 8）

| 基准 | DeepSeek-R1 | OpenAI o1-1217 | GPT-4o | Claude-3.5 | DeepSeek-V3 |
|------|------------|----------------|--------|------------|-------------|
| AIME 2024 (Pass@1) | **79.8** | 79.2 | 9.3 | 16.0 | 39.2 |
| MATH-500 (Pass@1) | **97.3** | 96.4 | 74.6 | 78.3 | 90.2 |
| Codeforces (Percentile) | 96.3 | **96.6** | 23.6 | 20.3 | 58.7 |
| MMLU (EM) | 90.8 | **91.8** | 87.2 | 88.3 | 88.5 |
| GPQA Diamond (Pass@1) | 71.5 | **75.7** | 49.9 | 65.0 | 59.1 |
| LiveCodeBench (Pass@1) | **65.9** | 63.4 | 32.8 | 38.9 | 36.2 |
| AlpacaEval 2.0 (LC) | **87.6** | - | 51.1 | 52.0 | 70.0 |
| ArenaHard | **92.3** | - | 80.4 | 85.2 | 85.5 |

**核心结论**：
- 数学/编程推理任务上，DeepSeek-R1与OpenAI o1-1217**基本持平**（AIME R1略优，Codeforces o1略优）
- 通用任务（AlpacaEval、ArenaHard）上，R1**大幅领先**所有竞品
- 对比DeepSeek-V3（同架构无RL推理），AIME提升+40.6pp，证明RL推理训练的巨大价值
- 在GPQA Diamond上R1(71.5)不及o1(75.7)，Figure 10指出人类专家（Ph.D.级别+网络资源）仍达81.2%，说明R1在开放域科学问题上仍有差距

#### 人类对比（Figure 10）

- AIME 2024：R1（79.8%）和R1-Zero（37.8%均超过人类平均（~50%）
- Codeforces：R1达到96.3百分位，超越96.3%的人类参赛者
- GPQA Diamond：人类专家（81.2%）仍优于R1（71.5%），这是R1需要工具增强（如搜索引擎）才能弥合的差距

---

### 归因分析 (Ablation Study)

**按贡献大小排序的阶段归因（Table 3）：**

| 排名 | 阶段 | 最大受益基准 | 提升幅度 | 核心贡献 |
|------|------|------------|---------|----------|
| 1 | 第一阶段RL (Dev1→Dev2) | AIME | +15.0pp | **推理能力的核心提升**，数学/代码/STEM全面增强 |
| 2 | 第二阶段RL (Dev3→R1) | AlpacaEval 2.0 | +25.5pp | **用户偏好对齐**，通用任务大幅改善 |
| 3 | SFT (Dev2→Dev3) | Aider-Polyglot | +19.2pp | **工程代码和非推理能力**，通过大规模数据混合 |
| 4 | Cold Start (Base→Dev1) | IF-Eval | +25.1pp | **指令遵循**，但推理能力暂时下降（AIME -18.9pp） |

**关键发现**：
- Cold Start SFT的"推理代价"：Dev1在AIME上从77.9%降至59.0%（-18.9pp），证实了作者的假设——SFT数据可能限制了模型的推理探索空间。但IF-Eval从46.6%升至71.7%，说明格式/可读性显著改善。
- 推理RL的恢复能力：Dev2不仅恢复了推理性能（AIME 74.0%），还在代码（LiveCodeBench +6.0pp）和学术任务（MMLU-Pro +9.7pp）上大幅超越R1-Zero。
- 最终RL的主要价值在偏好对齐而非推理：R1 vs Dev3在AIME仅+1.7pp，但AlpacaEval +25.5pp。

**语言一致性奖励的消融（Supplementary B.6）：**
- 添加语言一致性奖励导致数学基准**轻微下降**
- 但语言一致性显著改善，使输出更可读
- 这是一个明确的**性能-可读性trade-off**

---

### 可信度检查 (Credibility Check)

**优点：**
- ✅ 在20+个基准上进行了全面评估，覆盖数学、代码、STEM、通用、中英文
- ✅ 使用t-test (p<0.01)进行统计显著性检验（Table 3）
- ✅ 与OpenAI o1直接对比，而非只对比弱baseline
- ✅ 报告了中间checkpoint（Dev1-3）的完整演进，展示了每个阶段的真实贡献
- ✅ Figure 6诚实展示了reward hacking问题
- ✅ 公开了模型权重和蒸馏模型

**疑点：**
- ⚠️ OpenAI o1的架构和参数量未公开，与671B MoE直接对比的公平性存疑
- ⚠️ SimpleQA上R1(30.1)不如DeepSeek-V3(24.9?)和Claude-3.5(28.4)，但论文未深入分析此退化
- ⚠️ SWE-Bench Verified上R1(49.2)显著落后于Claude-3.5(80.8)，论文承认"large-scale RL has not been applied extensively in software engineering tasks"但仅简单归因于评估效率
- ⚠️ 蒸馏实验的对比中，被蒸馏模型（如Qwen-32B）的原始性能baseline未完全展示
- ⚠️ 训练数据的AIME/Codeforces题目与评估集的重叠程度虽提及了污染检测，但细节在附录中

**总体评估**：实验设计总体公平且全面，主要结论可信。少数基准上的性能退化被作者在Limitation部分诚实承认。

---

## 专家批判 (Critical Review)

### 隐性成本 (Hidden Costs)

1. **计算成本巨大**：在671B MoE模型上进行RL训练，每个问题采样16个回答（每个最长65536 tokens），10400个训练步。虽然论文未公开具体GPU小时数（Table 7提及但在主文中未详述），但从架构规模推算，这需要**数千张高端GPU训练数周**。GRPO虽然比PPO省了一半内存（去掉value model），但rollout的16倍采样仍是巨大开销。

2. **推理成本高**：R1的回答通常包含数千到上万tokens的"思考过程"。Figure 1(b)显示平均响应长度从~3000增长到~15000 tokens。对比传统模型的几百tokens回答，推理成本增加了10-50倍。论文承认存在"overthinking"问题——简单问题也生成过长推理。

3. **对超参极度敏感**：
   - clip ratio ε=10是非标准值（标准PPO用0.1-0.2），论文明确指出太小会截断梯度、太大会不稳定
   - 第二阶段RL的温度必须从1.0降到0.7，否则生成"incoherent"
   - 基于模型的偏好奖励只能训练最后400步，更多步会导致reward hacking（Figure 6）
   - 这些敏感点意味着复现需要大量调参实验

4. **Prompt敏感性**：论文明确指出"Few-shot prompting consistently degrades its performance"，推荐zero-shot。这与传统LLM的使用习惯相反，可能给用户造成困惑。

5. **语言混合问题未完全解决**：虽然引入了语言一致性奖励，但论文承认对非中英文语言仍存在问题——模型可能对其他语言的查询使用英文推理和回答。

### 工程落地建议

1. **最大的"坑"——reward hacking**：Figure 6清楚展示了使用神经网络奖励模型时的reward hacking：奖励信号持续上升，但Codeforces实际性能在约400步后开始下降。工程落地时，**必须设计早停策略**，使用独立的验证集监控实际性能，而非依赖奖励信号。

2. **规则奖励的覆盖范围有限**：规则奖励只适用于有确定答案的任务。对于开放域问答、写作、摘要等任务，必须使用神经网络RM，但又面临reward hacking风险。论文的解决方案是限制RM训练步数（400步），但这本质上是回避而非解决问题。

3. **冷启动数据的质量至关重要**：虽然冷启动只需"thousands of"数据（相对较少），但这些数据需要精心设计——第一人称视角、语言一致、包含反思和验证步骤。论文用R1-Zero的输出经人工筛选和DeepSeek-V3改写来构造，这个pipeline本身不简单。

4. **长序列训练的基础设施挑战**：65536 tokens的最大长度对训练系统提出极高要求。论文开发了专门的RL框架（Figure 5），包含rollout/inference/reward/training四个解耦模块、VRAM动态管理（模块完成后卸载到CPU/磁盘）、数据packing策略、DualPipe流水线并行等。复现这套系统的工程量不亚于算法本身。

5. **蒸馏是更实用的路径**：论文表明，将R1的推理能力蒸馏到较小模型（如Qwen-32B、LLaMA-70B）可以获得显著的推理提升，且成本远低于在小模型上直接做RL。对于资源有限的团队，**蒸馏是最佳性价比方案**。

### 关联思考

1. **与MoE架构的协同**：DeepSeek-R1基于DeepSeek-V3的MoE架构（671B总参数，37B激活），MoE的稀疏激活在长CoT推理中尤为重要——每个token只激活37B参数，使得生成10000+ tokens的推理链在计算上可行。如果使用同等规模的dense model，推理成本将高出约18倍。

2. **与FlashAttention/长上下文技术的关系**：65536 tokens的最大推理长度对attention计算提出挑战。论文使用MLA（Multi-head Latent Attention）压缩KV cache，这与FlashAttention在不同层面解决长序列问题——MLA减少内存，FlashAttention减少计算。两者可叠加使用。

3. **与LoRA/PEFT的潜在冲突**：GRPO需要对完整模型参数进行策略梯度更新。LoRA的低秩约束可能限制策略探索空间，尤其是在需要大幅策略更新的早期训练阶段（ε=10暗示需要较大的参数更新幅度）。将GRPO与LoRA结合的可行性是开放问题。

4. **与Process Reward Model (PRM)的关系**：论文明确选择不使用PRM（如Lightman et al., 2023的方法），理由是大规模RL中PRM易被hack。但PRM在小规模/短CoT场景下仍可能有效。两种方法可能在不同规模/任务复杂度下各有优势。

5. **与Test-Time Compute Scaling的关系**：R1的长CoT本质上是一种test-time compute scaling——用更多推理时间换取更好的答案。但与MCTS或majority voting等外部搜索方法不同，R1的计算分配是**内化在模型中的**——模型自己决定在哪里多想、在哪里少想。这是一种更优雅但更不可控的test-time scaling方式。

---

## 机制迁移分析 (Mechanism Transfer Analysis)

## 机制解耦 (Mechanism Decomposition)

| 原语名称 | 本文用途 | 抽象描述 | 信息论/几何直觉 |
|---------|---------|---------|---------------|
| **组内相对优势估计 (Group-Relative Advantage)** | 用同一问题的G个采样互相比较，替代价值模型 | 在无法获得绝对价值估计时，通过同组内的相对排名来计算梯度信号 | 将绝对评估问题转化为相对排序问题——当评判标准难以量化时，"A比B好"的判断通常比"A值8.5分"更可靠（类似信息论中序数比基数更鲁棒） |
| **纯结果奖励 (Outcome-Only Reward)** | 仅以最终答案正确性为奖励，不干预中间推理过程 | 只在序列末端给予稀疏反馈，让生成过程自由探索中间状态空间 | 减少了奖励信号中的人为先验偏见（信息瓶颈原理：过程奖励注入了过多约束，限制了解空间的探索维度） |
| **非约束涌现 (Emergent Behavior via Unconstrained RL)** | 不预设推理模式，让模型自发发展出反思、验证、策略切换等行为 | 在大参数空间+简单目标函数的条件下，复杂行为作为优化的副产品自然涌现 | 类似物理学中的自组织现象——简单的能量最小化规则可以产生复杂的晶体结构；同理，简单的"答案对不对"奖励可以催生复杂的推理策略 |
| **多阶段课程式训练 (Multi-Stage Curriculum)** | 从纯推理RL → 混合SFT → 通用RL，逐步扩展能力范围 | 先在约束环境中建立核心能力，再在更广阔的环境中泛化 | 类似课程学习（curriculum learning）的几何直觉：先在低维子空间找到好的解，再投影到高维空间进行微调，比直接在高维空间搜索更高效 |

---

## 迁移处方 (Transfer Prescription)

### 原语1：组内相对优势估计

**迁移场景A：推荐系统中的排序学习**
- **目标领域 + 具体问题**：电商推荐中，对同一用户query生成多个推荐列表，优化列表排序质量
- **怎么接**：输入 = 用户query + 候选item集合；生成 = G个不同的排序策略（通过采样不同temperature）；奖励 = 用户点击/购买的NDCG；优势 = 组内NDCG的标准化差异。替换现有的pointwise/pairwise排序loss
- **预期收益**：避免了训练单独的"排序质量评估模型"，直接用结果反馈优化。适合奖励函数已知但最优策略难以标注的场景
- **风险**：G个采样的计算成本在实时推荐中可能过高；低采样数下优势估计方差大

**迁移场景B：药物分子生成**
- **目标领域 + 具体问题**：蛋白质/小分子设计中，评估生成分子的活性需要昂贵的实验或模拟
- **怎么接**：输入 = 目标蛋白口袋；生成 = G个候选分子（通过SMILES生成模型）；奖励 = 对接分数（docking score）；优势 = 组内对接分数标准化
- **预期收益**：无需训练分子"价值函数"，直接用对接分数的相对排序优化生成策略
- **风险**：对接分数本身可能不够准确，导致reward hacking；G需要足够大以覆盖化学空间

### 原语2：纯结果奖励 + 非约束涌现

**迁移场景A：机器人操控**
- **目标领域 + 具体问题**：机械臂抓取任务——只有"抓到/没抓到"的二值反馈，中间动作序列无法标注
- **怎么接**：输入 = 视觉观察；生成 = 动作序列（通过扩散策略或autoregressive策略）；奖励 = 是否成功抓取（0/1）；不对中间动作施加过程奖励
- **预期收益**：机器人可能涌现出人类未设计的抓取策略（如利用桌面摩擦力辅助抓取），类似R1涌现出"Wait"反思行为
- **风险**：物理世界的采样成本极高（每次试验需要真实时间），G=16可能不够；sim-to-real gap可能导致涌现行为不可迁移

**迁移场景B：定理证明 / 形式化验证**
- **目标领域 + 具体问题**：自动定理证明中，证明步骤的"正确性"可由证明检查器（如Lean4）自动验证
- **怎么接**：输入 = 定理陈述；生成 = 多个证明尝试（tactic sequences）；奖励 = 证明检查器通过(1)/失败(0)；让模型自由探索证明策略
- **预期收益**：这是本文方法最天然的迁移目标——形式化验证提供了与数学/代码同样可靠的规则奖励
- **风险**：定理证明的搜索空间比数学竞赛更大，可能需要更大的G或更多的训练步数

### 原语3：多阶段课程式训练

**迁移场景：多模态模型的渐进式能力构建**
- **目标领域**：视觉-语言模型的post-training
- **怎么接**：Stage 1: 纯视觉推理RL（图表理解、空间关系推理，规则奖励）→ Stage 2: 混合SFT（视觉+文本数据）→ Stage 3: 通用RL（视觉QA + 文本QA + 偏好对齐）
- **预期收益**：避免视觉推理和文本能力的相互干扰，先在视觉推理上建立强项，再泛化
- **风险**：视觉推理的规则奖励设计比数学/代码更困难（图像理解的"正确性"更模糊）

---

## 机制家族图谱 (Mechanism Family Tree)

### 前身 (Ancestors)

| 工作 | 年份 | 类似机制 | 本文的创新增量 |
|------|------|---------|-------------|
| **REINFORCE** (Williams, 1992) | 1992 | 策略梯度方法 | GRPO加入了组内相对优势和clipped objective |
| **PPO** (Schulman et al., 2017) | 2017 | Clipped surrogate objective | GRPO去掉了value model，用group relative advantage替代GAE |
| **RLHF/InstructGPT** (Ouyang et al., 2022) | 2022 | RL用于LLM对齐 | R1将RL目标从"对齐人类偏好"扩展到"激发推理能力" |
| **Chain-of-Thought** (Wei et al., 2022) | 2022 | 中间推理步骤提升性能 | R1的CoT是RL自发涌现的，而非人工设计或prompt引导的 |
| **STaR** (Zelikman et al., 2022) | 2022 | 用正确推理轨迹自我训练 | R1不需要种子推理轨迹，直接从base model开始RL |
| **GRPO原始论文** (Shao et al., 2024) | 2024 | Group Relative Policy Optimization | R1将GRPO从数学推理扩展到完整的LLM post-training pipeline |

### 兄弟 (Siblings)

| 工作 | 关系 | 关键差异 |
|------|------|----------|
| **OpenAI o1** (2024) | 最直接的竞争者，同期独立开发 | o1的训练方法未公开；R1是开源的；从结果看两者性能接近 |
| **Process Reward Models** (Lightman et al., 2023) | 另一种提升数学推理的RL方法 | PRM提供步骤级奖励（更细粒度但更易被hack）；R1只用结果奖励（更粗粒度但更可靠） |
| **Quiet-STaR** (Zelikman et al., 2024) | 让模型在每个token前"思考" | 思考机制是嵌入在前向传播中的；R1的思考是显式的CoT生成 |

### 后代 (Descendants)

| 方向 | 描述 |
|------|------|
| **R1-Distill系列** | 本文自带的蒸馏模型（Qwen-1.5B/7B/14B/32B, LLaMA-8B/70B），证明推理能力可跨模型迁移 |
| **开源社区复现** | R1的开源推动了大量基于GRPO的推理RL实验（如open-r1等项目） |
| **多模态推理RL** | 将R1的方法扩展到视觉推理、多模态理解等领域（潜在方向） |
| **工具增强推理RL** | R1论文明确提出的未来方向：在RL过程中集成搜索引擎、编译器等工具 |

### 创新增量总结

本文在族谱中的核心创新增量是：**首次在工业级规模（671B参数）上验证了"纯结果RL可以激发复杂推理行为"这一假说**。具体地：
1. 从PPO到GRPO的简化使大规模RL可行
2. 从过程奖励到纯结果奖励的简化消除了reward hacking风险
3. 从SFT-first到RL-first的范式转换释放了模型的自主探索能力
4. 完整的multi-stage pipeline展示了如何将纯RL的推理能力工程化为可用产品

---

## 背景知识补充 (Background Context)

### 核心依赖技术

#### 1. Proximal Policy Optimization (PPO)
- **地位**：LLM RL阶段的事实标准算法（Schulman et al., 2017）
- **核心思想**：通过clipped surrogate objective限制策略更新幅度，平衡探索与稳定性
- **本文关系**：GRPO是PPO的简化版，去掉了value model和GAE，用组内相对奖励替代
- **关键引用**：Schulman et al., 2017; Ouyang et al., 2022

#### 2. Reinforcement Learning from Human Feedback (RLHF)
- **地位**：现代LLM对齐的标准范式（InstructGPT, ChatGPT）
- **核心流程**：收集人类偏好 → 训练奖励模型 → PPO优化策略
- **本文关系**：R1用规则奖励替代了人类偏好奖励模型（在推理任务上），但在通用任务的第二阶段RL中仍使用了传统的偏好奖励模型
- **关键引用**：Christiano et al., 2017; Ouyang et al., 2022

#### 3. Chain-of-Thought (CoT) Prompting
- **地位**：提升LLM推理能力的里程碑技术
- **核心思想**：通过few-shot示例或"Let's think step by step"引导模型生成中间推理步骤
- **本文关系**：R1的CoT是RL自发涌现的长链推理，而非人工设计的prompt引导；且R1的CoT远长于传统CoT（数千vs数百tokens）
- **关键引用**：Wei et al., 2022b; Kojima et al., 2022

#### 4. Mixture-of-Experts (MoE) 架构
- **地位**：大规模高效LLM的主流架构选择
- **核心思想**：每个token只激活部分专家网络（37B/671B），实现参数量与计算量的解耦
- **本文关系**：MoE是R1能在合理成本下生成超长推理链的关键——671B的知识容量 + 37B的推理计算成本
- **关键引用**：DeepSeek-AI, 2024b

#### 5. Multi-head Latent Attention (MLA)
- **地位**：DeepSeek系列的核心推理效率技术
- **核心思想**：将KV cache压缩到低维潜空间，大幅减少长序列推理的内存占用
- **本文关系**：支撑R1在65536 tokens长度下的高效推理
- **关键引用**：DeepSeek-AI, 2024a

#### 6. Self-Consistency Decoding
- **地位**：Test-time compute scaling的基线方法
- **核心思想**：采样多个回答，取多数一致的答案
- **本文关系**：R1-Zero使用Cons@16（16个采样的多数投票）将AIME从77.9%提升到86.7%
- **关键引用**：Wang et al., 2023c
