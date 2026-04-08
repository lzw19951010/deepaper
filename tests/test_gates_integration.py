"""Integration tests: a complete merged.md fixture passes all gates together.

This ensures gates don't conflict with each other (e.g., H9 requiring code
blocks while H6 scans for headings inside code blocks).
"""
import pytest

from deepaper.gates import run_hard_gates


# A complete merged.md that satisfies all gates simultaneously.
# This is the "golden" fixture — if a gate change breaks it, the change
# must update both the gate AND this fixture.
COMPLETE_MERGED_MD = """\
---
venue: "arXiv preprint"
publication_type: preprint
tldr: "OLMo 3 achieves MATH 96.2% and AIME 2024 80.6% via three-stage training with Delta Learning DPO."
core_contribution: new-method
baselines:
  - "Qwen 2.5 32B"
  - "Llama 3.1 70B"
  - "DeepSeek-R1 32B"
datasets:
  - "MATH"
  - "AIME 2024"
  - "LiveCodeBench"
metrics:
  - "accuracy"
  - "pass@1"
keywords:
  - language model
  - pretraining
  - reinforcement learning
  - DPO
  - open source
code_url: "https://github.com/allenai/OLMo-core"
---

#### 核心速览

##### TL;DR
OLMo 3 通过三阶段训练（预训练 5.9T tokens + 中训练 + 长上下文扩展）与 Delta Learning DPO，在 32B 参数规模达到 MATH 96.2%、AIME 2024 80.6%，以 Qwen 3 32B 六分之一的训练量逼近其性能。

##### 一图流 (Mental Model)
如果旧方法是拿着固定食谱做菜（数据配比写死），新方法就是根据每道食材的品质实时调整用量——品质高的食材多放，品质低的直接丢弃。如 Figure 1 所示，整条流水线从原料加工到精装上桌全程透明开放。

##### 核心机制一句话
[分阶段蒸馏对比] + [偏好对] + [大小模型能力落差作为信号] + [突破 SFT 饱和上限]

##### 关键数字速查

| 指标 | 数值 | 基线 | 基线值 | 增益 |
|------|------|------|--------|------|
| MATH | 96.2% | Qwen 2.5 32B | 94.1% | +2.1pp |
| AIME 2024 | 80.6% | DeepSeek-R1 32B | 72.6% | +8.0pp |

#### 第一性原理分析

##### 痛点 (The Gap)
[C1] Because 现有开源模型（如 Llama 3.1、OLMo 2）只公开最终权重而隐藏训练数据和中间检查点 → Therefore 社区无法复现训练过程、无法进行可控消融实验 → Therefore 开源 LLM 的科学可重复性严重受损。如 Figure 2 所示，OLMo 3 的模型流程涵盖从预训练到后训练的完整生命周期。

##### 核心洞察 (Key Insight)
作者发现 SFT 存在饱和效应：当 SFT 数据已被充分学习后，继续增加 SFT 数据的边际收益为零。Because SFT 本质是最大似然模仿 → 模型能力上限被教师数据锁死 → Therefore 需要跳出模仿范式。Delta Learning DPO 利用大模型与小模型之间的能力落差构建偏好信号（如 Figure 1 中后训练阶段所示），绕过了这一瓶颈。

##### 物理/直觉解释
这就像学徒从两位师傅那里学手艺：一位是顶级大师（Qwen 3 32B），一位是刚入门的新手（Qwen 3 0.6B）。学徒不是简单模仿大师（那是 SFT），而是观察"大师做对了什么、新手做错了什么"——这个差异信号才是真正的学习材料。

#### 技术精要

##### 直觉版 (Intuitive Walk-through)
如 Figure 1 所示，OLMo 3 的模型流程是一条三段式流水线。假设我们有 9T tokens 的原始数据池。旧方法（如 Llama 2）直接随机抽样 2T tokens 训练，好坏数据一视同仁。新方法先按质量分 4 档：顶部 10% 以 7x 倍率重采样，次优 20% 以 3.5x，中等 30% 以 1.2x，底部 40% 直接丢弃。最终从 9T 中生成约 5.9T 有效 tokens，高质量数据密度提升了 3 倍。读者可以验算：0.1×7 + 0.2×3.5 + 0.3×1.2 = 0.7+0.7+0.36 = 1.76，对应约 9T×1.76/3 ≈ 5.3T（实际略有调整）。

##### 精确版 (Formal Specification)

数据流图：Raw Web Crawl (9T tokens) → Quality Classifier → Bucketed Upsampling → Filtered Corpus (5.9T) → Stage 1 Pretraining → Stage 2 Midtraining (100B) → Stage 3 Long-Context Extension → Base Model → SFT → DPO → RL → Final Model

关键公式：DPO 损失函数

$$L_{DPO} = -\log\sigma(\beta \cdot (\log\frac{\pi_\theta(y_c|x)}{\pi_{ref}(y_c|x)} - \log\frac{\pi_\theta(y_r|x)}{\pi_{ref}(y_r|x)}))$$

其中：
- $\pi_\theta$: 当前策略模型
- $\pi_{ref}$: 参考模型（SFT checkpoint）
- $y_c$: chosen response（来自 Qwen 3 32B thinking）
- $y_r$: rejected response（来自 Qwen 3 0.6B thinking）
- $\beta$: 温度参数，控制偏好锐度

##### 数值推演 (Numerical Example)

假设对一个数学问题，大模型给出正确推理链的 log prob = -2.0，小模型给出错误推理链的 log prob = -8.0。参考模型对两者的 log prob 分别为 -3.0 和 -7.5。

则 DPO 损失中的关键项 = β × [(-2.0 - (-3.0)) - (-8.0 - (-7.5))] = β × [1.0 - (-0.5)] = β × 1.5

当 β=0.1 时，sigmoid(0.15) ≈ 0.537，损失 = -log(0.537) ≈ 0.62。梯度方向正确地推动模型偏好 chosen。

```python
# OLMo RL training loop (simplified)
def olmo_rl_step(policy, prompts, reward_fn):
    # Generate rollouts with continuous batching
    responses = policy.generate(prompts, max_tokens=32768)  # (B, T)

    # Compute rewards (multi-domain verifiable)
    rewards = reward_fn(prompts, responses)  # (B,)

    # GRPO-style update: no KL penalty, no std normalization
    advantages = rewards - rewards.mean()  # (B,)

    # Asymmetric clipping: clip_high=0.28, clip_low=0.20
    ratio = (policy.log_prob(responses) - old_log_prob).exp()  # (B, T)
    clipped = torch.where(
        advantages > 0,
        torch.clamp(ratio, max=1.28),
        torch.clamp(ratio, min=0.80),
    )
    loss = -(clipped * advantages.unsqueeze(-1)).mean()
    return loss
```

##### 设计决策 (Design Decisions)

| 决策 | 备选方案 | 选择理由 | 证据来源 |
|------|----------|----------|----------|
| 无 KL 惩罚 | 标准 PPO KL 散度约束 | 更充分利用 RL 信号，MATH 提升 2.1pp | 消融实验 Table 3 |
| 非对称裁剪 | 对称裁剪 clip=0.2 | 正奖励步幅更大，加速正确行为学习 | Figure 4 |

##### 消融排名 (Ablation Ranking)

| 排名 | 组件 | 增益 | 数据来源 |
|------|------|------|----------|
| 1 | Delta Learning DPO | +8.6pp MATH | Table 2 |
| 2 | OlmoRL | +3.4pp MATH | Table 2 |
| 3 | 模型融合 (souping) | +2.9pp MMLU | Table 4 |

##### 隐性成本 (Hidden Costs)

| 成本项 | 量化数据 | 对决策的影响 |
|--------|----------|--------------|
| 训练时长 | 约 47 天 | 需要长期 GPU 预留 |
| 外部模型依赖 | Qwen 3 32B + 0.6B | 数据质量高度敏感 |
| 工程复杂度 | 5x 标准推理 | inflight updates 调参成本高 |

##### 易混淆点 (Potential Confusions)

- ❌ 错误理解: Delta Learning DPO 是一种新的损失函数
- ✅ 正确理解: 损失函数不变（标准 DPO），创新在于 **偏好对的构造方式**——用大小模型能力差而非人工标注

- ❌ 错误理解: OlmoRL 不使用 KL 约束意味着没有任何正则化
- ✅ 正确理解: 截断重要性采样比（IS ratio clipping）替代了 KL 约束的角色，控制策略更新步长

- ❌ 错误理解: "完全开源"只是指模型权重开源
- ✅ 正确理解: 完全开源包括训练数据、每个阶段的检查点、数据处理代码、训练脚本——全生命周期透明

#### 实验与归因

##### 核心收益
OLMo 3.1 Think 32B 在 MATH 达 96.2%，AIME 2024 达 80.6%，LiveCodeBench 达 83.3%，是截至发布时最强的完全开源思考模型。

##### 归因分析 (Ablation Study)

OLMo 3 Think 32B 后训练各阶段贡献（按 MATH 得分）：

- SFT 阶段：84.2%（基线）
- +DPO (Delta Learning)：92.8%(+8.6)，贡献最大
- +RL (OlmoRL)：96.2%(+3.4)

中训练阶段消融（按 MMLU 得分）：
- 模型融合 (model souping)：+2.9pp（最大贡献因素）
- 数据质量过滤：+1.7pp
- 长上下文扩展：+0.8pp

OlmoRL 基础设施优化效果：
- 连续批处理 + inflight updates：从 881 tok/s 提升到 2949 tok/s（3.3x 加速）
- 静态批处理在 32K 生成长度下浪费高达 54% 算力

##### 可信度检查
实验设置基本公平。所有 baseline 均使用官方公开数据，评测框架 open-instruct 完全开源可复现。RL-Zero 的 spurious reward 实验（随机奖励仍获提升则说明泄露）证实了训练过程的可信度。一个潜在偏差：Think 模型使用 Qwen 3 32B 生成的数据训练，而 Qwen 本身也是 baseline 之一。值得注意的是，OLMo 3 7B 在同参数级别也表现出色，MATH 达到 78.1%，IFEval 达到 70.9%，验证了方法在不同规模上的通用性。Instruct 路线的 32B 模型在 BBH 上达到 88.3%，在 GPQA 上达到 24.1%，与 Think 路线形成互补。RL-Zero 路线则证明了从 base 模型直接做 RL 的可行性。

#### 专家批判

##### 隐性成本 (Hidden Costs)
论文未充分讨论的代价包括：完整训练流程需要约 47 天、数千 GPU（基础设施规模约为 Qwen 3 的 14 分之一但仍然巨大）。Delta Learning DPO 依赖 Qwen 3 32B 和 0.6B 两个外部模型生成偏好对——对这些模型的质量高度敏感。OlmoRL 的连续批处理需要约 5 倍于标准推理的工程复杂度，且 inflight updates 引入的 off-policy 误差需要仔细调参。RL 阶段在 2,300 步内完成（约 2.75M tokens），但 rollout 的 GPU 占用峰值远高于 SFT。

##### 工程落地建议
最大的坑在于 Delta Learning 的数据质量：如果 chosen 模型不够强或 rejected 模型太强，能力差太小，DPO 梯度信号退化。建议先在小规模（7B）上验证 delta 幅度是否足够。

##### 关联思考
OlmoRL 的非对称裁剪与 DAPO 的思路一致（同期独立提出）。连续批处理可与 vLLM 的 PagedAttention 结合进一步优化内存。模型融合（souping）与 LoRA merge 在概念上类似，但操作在全参数空间。

#### 机制迁移

##### 机制解耦 (Mechanism Decomposition)

| 原语名称 | 本文用途 | 抽象描述 | 信息论/几何直觉 |
|---------|---------|---------|---------------|
| 质量感知上采样 | 预训练数据按质量分档重采样 | 离散质量分位映射到连续重采样权重 | 等效于温度 <1 的 softmax 重权重 |
| Delta Learning DPO | 大小模型能力差作为偏好信号 | 偏好对有用性取决于 chosen/rejected 能力落差 | log ratio 梯度正比于概率差 |
| 连续批处理 | 消除 RL rollout 中的气泡浪费 | 同步点从全批完成移至逐序列完成 | TV 距离球内约束策略更新步长 |

##### 迁移处方 (Transfer Prescription)

**质量感知上采样**可迁移至推荐系统的行为日志清洗：对高质量交互重采样，低质量截断。

**Delta Learning DPO**可迁移至代码 LLM 对齐：大参数代码模型为 chosen，小参数模型为 rejected。

##### 机制家族图谱 (Mechanism Family Tree)

**前身 (Ancestors):**
- GRPO (DeepSeek, 2024): group relative policy optimization，OlmoRL 的基础框架
- RegMix/CLIMB: 数据混合比例优化的早期工作
- DCLM: 数据质量分类器驱动的语料筛选
- Orca/WizardLM: 早期利用强模型生成训练数据的蒸馏范式

**兄弟 (Siblings):**
- DAPO (2025): 独立提出的非对称裁剪 RL 策略
- Qwen 3 (2025): 同期的大规模思考模型训练

**后代 (Descendants):**
- OLMo 3.1: 基于 OLMo 3 继续 RL 训练的增强版本

#### 背景知识补充

**DPO (Direct Preference Optimization):** Rafailov et al. 2023 提出的直接偏好优化方法，绕过显式奖励模型，直接在偏好对上优化策略。已成为 LLM 对齐的标准方法之一。

**GRPO (Group Relative Policy Optimization):** DeepSeek 提出的 RL 算法变体，以组内相对奖励替代绝对奖励估计，简化了 value function 的训练。OlmoRL 在此基础上进一步去掉了 KL 惩罚和标准差归一化。

**Model Souping:** 将多个独立训练的模型检查点进行权重平均（weight averaging），无需额外训练即可获得性能提升。OLMo 3 在中训练阶段使用此技术获得 +2.9pp MATH 提升。
"""

# Coverage checklist for H2 tests
_BASIC_CHECKLIST = {
    "subsection:3.1 Main Results": {
        "source": "subsection_heading",
        "match_text": "3.1 Main Results",
    },
}


class TestAllGatesPass:
    """A complete merged.md that passes ALL gates simultaneously."""

    def test_all_gates_pass_with_minimal_deps(self):
        """All gates pass when text_by_page/registry are None (skip H7/H8/H10)."""
        result = run_hard_gates(
            merged_md=COMPLETE_MERGED_MD,
            coverage_checklist={},
            core_figures=[],
            text_by_page=None,
            registry=None,
        )
        failed = result["failed"]
        assert failed == [], f"Gates failed: {failed}. Details: {result['results']}"
        assert result["passed"] is True

    def test_h5_finds_tldr_in_frontmatter(self):
        """H5 reads tldr from YAML frontmatter."""
        result = run_hard_gates(COMPLETE_MERGED_MD, {}, [], None, None)
        h5 = result["results"]["H5"]
        assert h5["passed"] is True
        assert h5["source"] == "frontmatter"
        assert h5["count"] >= 2

    def test_h6_ignores_code_block_comments(self):
        """H6 does not flag Python # comments inside code blocks."""
        result = run_hard_gates(COMPLETE_MERGED_MD, {}, [], None, None)
        h6 = result["results"]["H6"]
        assert h6["passed"] is True
        assert h6["violations"] == []

    def test_h8_skips_when_no_definition_pages(self):
        """H8 skips (passes) when all tables have definition_page=None."""
        registry = {
            "Table_1": {
                "type": "Table", "id": 1, "pages": [3],
                "definition_page": None, "has_caption": True,
            },
        }
        result = run_hard_gates(
            COMPLETE_MERGED_MD, {}, [],
            text_by_page={3: "Table 1: some numbers 95.2 87.3\n"},
            registry=registry,
        )
        h8 = result["results"]["H8"]
        assert h8["passed"] is True
        assert h8.get("skipped") is True

    def test_h9_content_markers_pass(self):
        """H9 content markers are satisfied by the complete fixture."""
        result = run_hard_gates(COMPLETE_MERGED_MD, {}, [], None, None)
        h9 = result["results"]["H9"]
        assert h9["passed"] is True, f"H9 failed. Missing: {h9.get('missing')}"


class TestH5FallbackToBody:
    """H5 falls back to body ##### TL;DR when frontmatter tldr is missing."""

    def test_body_fallback(self):
        from deepaper.gates import check_tldr_numbers

        md = (
            "---\n"
            "baselines:\n  - A\n  - B\n"
            "---\n"
            "#### 核心速览\n\n"
            "##### TL;DR\n"
            "达到 MATH 96.2% 和 AIME 80.6% 的成绩。\n"
        )
        result = check_tldr_numbers(md)
        assert result["passed"] is True
        assert result["source"] == "body"
        assert result["count"] >= 2

    def test_no_tldr_anywhere(self):
        from deepaper.gates import check_tldr_numbers

        md = (
            "---\nbaselines:\n  - A\n---\n"
            "#### 核心速览\nJust some text.\n"
        )
        result = check_tldr_numbers(md)
        assert result["passed"] is False
        assert result["source"] == "not_found"


class TestH6CodeBlockExemption:
    """H6 ignores # comments inside fenced code blocks."""

    def test_python_comment_in_code_block(self):
        from deepaper.gates import check_heading_levels

        md = (
            "---\ntitle: Test\n---\n"
            "#### Method\n"
            "Some text.\n"
            "```python\n"
            "# This is a Python comment, not a heading\n"
            "## Another comment\n"
            "def foo(): pass\n"
            "```\n"
            "##### Subsection\n"
            "More text.\n"
        )
        result = check_heading_levels(md)
        assert result["passed"] is True
        assert result["violations"] == []

    def test_real_h1_still_caught(self):
        from deepaper.gates import check_heading_levels

        md = (
            "---\ntitle: Test\n---\n"
            "# Real H1 heading\n"
            "#### Good section\n"
        )
        result = check_heading_levels(md)
        assert result["passed"] is False
        assert any("h1" in v for v in result["violations"])


class TestH8SkipNoDefinitionPages:
    """H8 skips when source_numbers is empty (no definition_page found)."""

    def test_all_definition_pages_none(self):
        from deepaper.gates import check_number_fingerprint

        text_by_page = {1: "Some text with numbers 42.0 and 99.9\n"}
        registry = {
            "Table_1": {
                "type": "Table", "id": 1, "pages": [1],
                "definition_page": None, "has_caption": True,
            },
            "Table_2": {
                "type": "Table", "id": 2, "pages": [1],
                "definition_page": None, "has_caption": True,
            },
        }
        md = (
            "---\ntitle: Test\n---\n"
            "#### Results\n"
            "| Model | Score |\n| --- | --- |\n| A | 95.2 |\n| B | 87.3 |\n"
        )
        result = check_number_fingerprint(md, text_by_page, registry)
        assert result["passed"] is True
        assert result.get("skipped") is True

    def test_with_valid_definition_pages_still_works(self):
        from deepaper.gates import check_number_fingerprint

        text_by_page = {3: "Table 1: Results\nModel A 95.2 accuracy Model B 87.3\n"}
        registry = {
            "Table_1": {
                "type": "Table", "id": 1, "pages": [3],
                "definition_page": 3, "has_caption": True,
            },
        }
        md = (
            "---\ntitle: Test\n---\n"
            "#### Results\n"
            "| Model | Accuracy |\n| --- | --- |\n| A | 95.2 |\n| B | 87.3 |\n"
        )
        result = check_number_fingerprint(md, text_by_page, registry)
        assert result["passed"] is True
        assert "skipped" not in result or result.get("skipped") is not True
