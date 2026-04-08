# Per-Paper Analysis v2 Design Spec

## 目标

重新设计 deepaper 的单篇论文分析输出格式，优化阅读效率（~10 分钟/篇），同时为未来 LLM Wiki 式的跨论文知识库留好接口。

## 设计原则

三个杠杆最大化信息效率：

| 杠杆 | 含义 | 实现方式 |
|------|------|---------|
| 信息质量 | 只保留提升判断力的信息 | 筛选规则：保留因果链/设计决策/消融排序/易混淆点/隐性成本/机制解耦，删除展开性散文/伪代码/背景常识 |
| 表达效率 | 用最高效的形式表达每种信息 | 表格/流程图/列表为主，散文仅用于补充推理语境 |
| 阅读时间 | 控制在 ~10 分钟 | 通过表达形式约束（非字符数约束）自然实现 |

## 章节结构

4 个章节，按阅读顺序排列：

```
1. 核心速览        — 30 秒定位论文价值
2. 第一性原理分析   — 3 分钟理解为什么
3. 技术精要        — 4 分钟掌握怎么做 + 做得怎么样
4. 机制迁移        — 2 分钟提取可复用模式
```

### 1. 核心速览

**职责**：30 秒内判断这篇论文值不值得深入读。

**包含**：
- TL;DR（≤100 字，含 ≥2 个量化数字）
- 核心机制一句话（`[动作] + [对象] + [方式] + [效果]`）
- 关键数字表（≤7 行）：指标 | 数值 | 基线 | 基线值 | 增益

**删除**：一图流（Mental Model）比喻段。

**表达形式**：TL;DR 一句话 + 核心机制一句话 + 关键数字表格。

### 2. 第一性原理分析

**职责**：理解作者为什么做这个选择，建立因果直觉。

**包含**：
- 痛点（The Gap）：之前 SOTA 死在哪？短散文（≤5 句）
- 因果链（≤3 条）：编号 `[C1]` `[C2]`，格式 `Because {前提} → Therefore {结论}`。每条可附 ≤1 句比喻或语境补充
- 因果链的散文补充：仅在结构化链式无法传达关键语境时使用

**删除**：独立的「物理/直觉解释」段落（比喻嵌入因果链内）。

**表达形式**：短散文（痛点）+ 编号因果链。

### 3. 技术精要

**职责**：掌握核心方法、关键结论、工程陷阱。合并当前「方法详解」「实验与归因」「专家批判」三个章节的精华。

**包含**：

| 子项 | 表达形式 | 说明 |
|------|---------|------|
| 方法流程 | 流程图（≤10 步） | 合并直觉版和精确版为一个精简版 |
| 公式与符号 | 公式 + 符号表（符号 \| 含义 \| 关键值） | 只列核心公式，不展开推导 |
| 设计决策 | 表格（决策 \| 备选方案 \| 选择理由 \| 证据来源） | 每条一行，不展开散文 |
| 消融排序 | 表格（排名 \| 组件 \| 增益 \| 数据来源） | 按贡献降序 |
| 易混淆点 | ❌ 一句 / ✅ 一句（≤3 对） | 保持精炼对仗 |
| 隐性成本 | 表格（成本项 \| 量化数据 \| 对决策的影响） | 论文没说的代价 |
| 可信度判断 | 1-2 句嵌入消融表末尾 | 不单独成段 |

**删除**：
- 伪代码（全部删除）
- 数值推演（删除，公式 + 符号表已够）
- 核心收益散文段（TL;DR 已覆盖）
- 可信度检查 5 段展开（压缩为 1-2 句）
- 工程落地建议散文（隐性成本表已覆盖）
- 关联思考散文（如有重要关联，以一行加入设计决策表）

**表达形式**：流程图 + 表格为主，散文仅用于补充推理语境。

### 4. 机制迁移

**职责**：提取可跨论文/跨领域复用的抽象模式。

**包含**：
- 机制解耦表（原语名称 | 本文用途 | 抽象描述 | 信息论直觉）
- 机制谱系：前身（Ancestors, ≥3）+ 兄弟（Siblings）+ 创新增量。每项一行：方法名 + 一句差异

**删除**：
- 迁移处方（推测性内容）
- 后代（预测性内容）
- 背景知识补充（整章删除）

**表达形式**：表格 + 精简列表。

## 表达形式约束

不用字符数限制，用形式偏好控制阅读效率：

**核心原则**：默认用结构化形式（表格/流程图/列表）；只在结构化形式会丢失关键推理语境时，才用散文补充。

**具体偏好**：
- 对比/排序/成本/符号 → 表格（严格更优，无例外）
- 因果链/设计决策的理由 → 允许短散文补充（1-3 句），但不鼓励展开为段落
- 比喻 → 嵌入因果链内 ≤1 句，不独立成段
- 伪代码 → 不生成（硬规则）
- 数字对比 → 表格（硬规则，禁止散文内嵌数字对比）

**Gate 验证改动**：
- **H3（字符下限）→ H3（章节存在性）**：不再检查字符数，改为检查 4 个章节标题是否存在
- **H9（内容标记）→ 检查结构化元素存在性**：关键数字表、设计决策表、消融排序表、隐性成本表、符号表、机制解耦表、因果链编号 `[C1]`
- **H7（figure 引用）**：保留
- **H1（baselines）**：保留，从 frontmatter 检查
- **H5（TL;DR 数字）**：保留，从 frontmatter 检查
- **H2（结构覆盖）**：简化 checklist 生成逻辑，过滤掉非章节标题的噪声条目
- **删除**：H3 的 `CHAR_FLOORS` 和 `compute_scaling_factor` 的字符建议目标

## YAML Frontmatter 设计

承担「索引层」角色，支持跨论文程序化检索。

### 保留字段

```yaml
title: "论文标题"
arxiv_id: "2512.13961"
date: "2025-12-15"
url: "https://arxiv.org/abs/2512.13961"
category: "llm/pretraining"
tldr: "一句话总结（≤100字，含 ≥2 个量化数字）"
baselines:
  - "Qwen 3 32B"
  - "DeepSeek R1 32B"
```

### 新增字段

```yaml
tags:
  - pretraining
  - data-engineering
  - rl-training
  - open-source

mechanisms:
  - name: 渐进式课程数据调度
    scope: pretraining → midtraining → long-context
    ancestor: curriculum learning
  - name: Delta Learning DPO
    scope: post-training DPO
    ancestor: DPO (Rafailov 2023)

key_tradeoffs:
  - decision: SWA 3/4 层 + 全注意力 1/4 层
    chosen_over: 全 SWA / 全注意力
    reason: 显存效率 vs 长程依赖

key_numbers:
  - metric: MATH 500
    value: 96.2
    baseline: Qwen 3 32B
    baseline_value: 95.4
  - metric: RL throughput
    value: 2949
    unit: tok/s
    baseline: OLMo 2
    baseline_value: 881
```

### 删除字段

- `keywords`（tags 替代）
- `datasets`（对分析无价值）
- `metrics`（对分析无价值）
- `core_contribution`（tldr 已覆盖）
- `publication_type`（低价值）
- `doi`（低价值）

## 表格列名标准化

所有论文使用统一列名，支持跨论文拼接：

```
关键数字表:   指标 | 数值 | 基线 | 基线值 | 增益
设计决策表:   决策 | 备选方案 | 选择理由 | 证据来源
消融排序表:   排名 | 组件 | 增益 | 数据来源
隐性成本表:   成本项 | 量化数据 | 对决策的影响
符号表:       符号 | 含义 | 关键值
机制解耦表:   原语名称 | 本文用途 | 抽象描述 | 信息论直觉
```

## 因果链格式

编号 + 固定格式，支持跨论文引用：

```
[C1] Because {前提} → Therefore {结论}
     — {可选：≤1 句比喻或语境补充}

[C2] Because {前提} → Therefore {结论}
```

## 分类与索引

- **文件路径保留目录结构**：`papers/llm/pretraining/olmo-3.md`
- **frontmatter 用 tags 支持多标签**：补充主分类无法覆盖的维度
- **分类变了就 move 文件**：简单直接，git 追踪历史
- **`deepaper reindex` 命令（deferred）**：从所有文件的 frontmatter 重建 `papers/INDEX.md`。本次不实现，但 frontmatter 结构已为其预留足够字段
- **每次 save 追加 `papers/log.md`（deferred）**：格式 `## [YYYY-MM-DD] ingest | 论文标题`。本次不实现，优先级低于核心分析格式改造

## Pipeline 改动

### 需要改的文件

| 文件 | 改什么 |
|------|--------|
| `templates/default.md` | 重写为 4 章节结构 + 表达形式偏好 + 标准化表格列名 |
| `output_schema.py` | 更新 SECTIONS（4 个）、删旧 content_markers、加新 markers、更新 frontmatter 字段 |
| `prompt_builder.py` | 更新 auto_split（3 writer）、删除 `compute_scaling_factor` 和字符建议目标、注入表达形式偏好（替代字符约束） |
| `gates.py` | H9 检查结构化元素存在性（不检查散文长度）、更新 H1/H2/H5 逻辑 |
| `cli.py` (merge) | 添加 frontmatter 置顶逻辑、修复 `####` 重复 bug |
| `cli.py` (save) | 追加 log.md 条目（deferred，本次不实现） |
| `cli.py` (reindex) | 新增命令：从 frontmatter 生成 INDEX.md（deferred，本次不实现） |

### Writer 分配

从 4 个 writer 降为 3 个：

```
writer-overview:   核心速览 + 机制迁移    （共享 frontmatter 和全局视角）
writer-principle:  第一性原理分析          （独立因果推理）
writer-technical:  技术精要               （方法 + 实验 + 批判合并）
```

### 不改的部分

- Extractor（notes.md 格式不变）
- Download / Extract pipeline
- PDF 处理逻辑

## 为 LLM Wiki 留的接口（本次不实现）

| 未来能力 | 当前预留的接口 |
|---------|--------------|
| 概念页（concepts/） | frontmatter.mechanisms 提供机器可读的机制列表 |
| 交叉引用 | frontmatter.baselines + mechanisms.ancestor 提供链接目标 |
| 跨论文合成 | 标准化表格列名 + key_numbers 支持拼接对比 |
| 矛盾检测 | 因果链编号 [C1] [C2] 支持精确引用和对比 |
| 全局搜索 | tags 多标签 + INDEX.md + log.md 提供多维索引 |
| Obsidian 集成 | frontmatter YAML 兼容 Dataview 插件查询 |

## 示例产出（OLMo 3 精炼版预览）

```yaml
---
title: "OLMo 3"
arxiv_id: "2512.13961"
date: "2025-12-15"
category: llm/pretraining
tags: [pretraining, data-engineering, rl-training, open-source, thinking-model]
tldr: "全流程开放推理模型，旗舰 OLMo 3.1 Think 32B 以 Qwen 3 约 1/6 token 量达到 MATH 96.2%、AIME 2024 80.6%"
baselines: ["Qwen 3 32B", "DeepSeek R1 32B", "Stanford Marin 32B", "Apertus 70B"]
mechanisms:
  - name: 渐进式课程数据调度
    scope: pretraining → midtraining → long-context
    ancestor: curriculum learning
  - name: Delta Learning DPO
    scope: post-training DPO
    ancestor: DPO
  - name: Inflight 权重更新
    scope: RL infrastructure
    ancestor: GRPO
key_tradeoffs:
  - decision: SWA 3/4 层 + 全注意力 1/4 层
    chosen_over: 全 SWA / 全注意力
    reason: 显存效率 vs 长程依赖
key_numbers:
  - {metric: MATH 500, value: 96.2, baseline: Qwen 3 32B, baseline_value: 95.4}
  - {metric: RL throughput, value: 2949, unit: tok/s, baseline: OLMo 2, baseline_value: 881}
  - {metric: Midtraining Math gain, value: 59.8, baseline: pre-midtrain, baseline_value: 23.5}
---

#### 核心速览

**TL;DR**: OLMo 3 用三阶段基础训练 + SFT→Delta DPO→OlmoRL 流水线构建完全开放思维模型；旗舰 OLMo 3.1 Think 32B 以 Qwen 3 约 1/6 token 量达到 MATH 96.2%、AIME 2024 80.6%。

**核心机制**: [渐进式分布迁移] 每阶段独立数据课程 + [Delta Learning] 质量差最大化对比突破 SFT 饱和 + [异步 inflight 更新] 解耦生成与训练 → 1/6 token 预算逼近 closed-weight 水平。

| 指标 | 数值 | 基线 | 基线值 | 增益 |
|------|------|------|--------|------|
| MATH 500 | 96.2 | Qwen 3 32B | 95.4 | +0.8 |
| AIME 2024 | 80.6 | Qwen 3 32B | 86.3 | -5.7 |
| Base Math (fully-open) | 61.9 | Marin 32B | 49.3 | +12.6 |
| Midtrain 7B Math | 59.8 | pre-midtrain | 23.5 | +36.3 |
| RL throughput | 2949 tok/s | OLMo 2 | 881 | +235% |
| IFBench (Instruct) | 39.7 | Qwen 3 No-Think | 31.3 | +8.4 |

#### 第一性原理分析

##### 痛点
全开放模型（Marin 32B Math 49.3, Apertus 70B Math 39.7）与封闭权重模型（Qwen 2.5 32B Math 64.7）存在 15+ pp 差距。问题不在数据量（OLMo 2 用 6.5T tokens，Math 仅 53.9），而在数据组成的结构性缺陷。

[C1] Because 模型能力天花板在预训练/中训阶段已隐性确定 → Therefore 在中训阶段系统注入合成推理数据（CraneMath +18.5pp, TinyMATH +13.2pp），让 base 模型在"体格定型"前就具备推理热启动，post-training 只需激活而非新建能力。

[C2] Because SFT 后模型对同质高质量输出分布饱和（直接 SFT Qwen3-32B traces 反而 -5.8pp）→ Therefore 最大化 chosen-rejected 质量差（Qwen3-32B vs Qwen3-0.6B），DPO 获 +2.6pp，为 RL 提供更高起点。

[C3] Because 推理模型生成长度极不均匀（均值 14,628 tokens），静态批处理浪费最多 54% 算力 → Therefore inflight 权重更新解耦生成与训练，4× 吞吐提升（881→2949 tok/s）。

（后续章节省略，完整示例在实现后生成）
```
