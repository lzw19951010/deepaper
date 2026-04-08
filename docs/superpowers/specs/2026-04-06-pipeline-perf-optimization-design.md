# Pipeline 性能优化设计

**Date:** 2026-04-06
**Status:** Draft
**Baseline:** OLMo-3 profiling (2512.13961) — 117 pages, 55 tables, 43 min, 521K tokens

---

## 核心原则

论文阅读的目标是**提取核心信息、提炼核心观点**，不是翻译。当前管道把所有表格无差别搬运，既浪费 token 又稀释信息密度。优化围绕这一原则展开。

---

## 变更清单

### 1. 统一读取策略：30K tokens 分片

**适用范围：** 所有 agent（extractor、writer、fixer）

**规则：**
- 单次读取文件上限 **30K tokens**，按 1 token ≈ 2 中英混合字符估算（即 ~60K 字符 / ~2000 行）
- 程序在生成 prompt 前计算文件行数，注入 `total_lines` 和 `recommended_reads`（= ceil(total_lines / 2000)），agent 按此执行
- **< 30K tokens 的文件必须一次读完**，禁止无意义分块
- **> 30K tokens 的文件**按顺序分片，每片 ≤ 30K tokens，按页边界对齐（`--- PAGE N ---` 标记）

**改动点：**
- `prompt_templates/extractor.md`：删除"分块读取"指令，替换为分片策略说明
- `prompt_builder.py` 的 `generate_writer_prompt()`：注入文件大小信息和分片指引
- `.claude/commands/deepaper.md`：fixer agent prompt 同步更新

**预期效果：** Extractor 从 43 次 tool call 降到 1-2 次，单轮时间从 857s 降到 ~200s。

### 2. Extractor 精简：从全量搬运到核心提炼

**问题：** 当前 extractor 要求"表格必须完整复制——每行每列，超过 15 行也不能省略"。OLMo-3（55 张表）的 notes 仅覆盖 25% 页面就膨胀到 43K bytes，触发 retry（+695s, +155K tokens）。

**改动：**

#### 2a. 删除全量抄表段

删除 extractor prompt 中的以下三个独立 section：
- `MAIN_RESULTS`（"复制每张主结果表的完整数据"）
- `ABLATIONS`（"每张消融表 + delta"）
- `HYPERPARAMETERS`（"Appendix 的超参数表"）

删除指令："表格必须完整复制 — 每行每列，超过 15 行也不能省略"

#### 2b. 新增 KEY_FINDINGS 段

合并为一个 `KEY_FINDINGS` section，指令：

```
## KEY_FINDINGS (核心发现，不抄表格)
针对每个核心实验结论，写一行摘要：
- 结论（量化数据 + 对比基线 + 来源表号）
- 格式示例："MATH 96.2%, 比 Qwen 3 32B 高 0.8pp (Table 5)"
- 仅记录支撑核心论点的数据，不复制完整表格
- 消融实验只记录贡献最大的 top-3 因素及其 delta
```

#### 2c. Notes 目标调整

- 目标字符数从 10,000-20,000 降到 **6,000-12,000**
- 保留其余 section 不变：META、FORMULAS、DATA_COMPOSITION、EVAL_CONFIG、TRAINING_COSTS、DESIGN_DECISIONS、RELATED_WORK、BASELINES

**改动文件：** `src/deepaper/prompt_templates/extractor.md`

**预期效果：** Notes 从 ~43K 压到 ~10K，一轮覆盖全文，retry 消失（省 ~695s + 155K tokens）。

### 3. 灵魂表检测（core_tables）

**问题：** 灵魂图有程序化打分检测（`identify_core_figures`），但表格没有。Writer 无法区分核心表和普通表。

**方案：混合策略** — 程序打分缩小候选范围，extractor 最终选择。

#### 3a. 程序化打分：`identify_core_tables()`

在 `registry.py` 中新增，复用灵魂图的打分维度：

```python
def identify_core_tables(registry: dict, text_by_page: dict, max_core: int = 5) -> list[dict]:
    """从 visual_registry 中筛选核心表格候选。

    打分维度（与 identify_core_figures 一致）：
    - ref_count: 正文中被引用次数（权重 3）
    - position: 越靠前越重要（权重 2）
    - caption_length: caption 越长通常越重要（权重 1）

    Returns: [{key, id, page, score, ref_count}]，按 score 降序，取 top max_core。
    """
```

- `max_core = max(3, min(8, paper_tables * 0.2))`：3-8 张候选
- 输出 `core_tables.json`，与 `core_figures.json` 同级

#### 3b. Extractor 从候选中选择

Extractor prompt 注入 core_tables 候选列表：

```
## 核心表格候选（程序预筛选，按重要性排序）
{core_tables_json}

在 KEY_FINDINGS 中优先引用这些表格的数据。如果你认为有遗漏的关键表，也可以补充，但总数不超过候选数量。
```

#### 3c. Writer 围绕核心表分析

Writer prompt 的质量合同中，将 "≥ N 张完整 markdown 对比表格（H4）" 替换为：

```
- 围绕核心表格展开归因分析，引用数据必须来自 notes KEY_FINDINGS 段或原文
- 实验表格只保留核心行（支撑主要结论的对比行），不要求完整复制
- 数值后标注增量变化，格式：`95.9(+0.3)`
```

**改动文件：**
- `src/deepaper/registry.py`：新增 `identify_core_tables()`
- `src/deepaper/cli.py`：extract 命令输出 `core_tables.json`
- `src/deepaper/prompt_templates/extractor.md`：注入候选列表
- `src/deepaper/prompt_builder.py`：修改 `gates_to_constraints()` 中 H4 相关约束

### 4. Gate 调整

#### 4a. 删除 H4（Table Count gate）

**理由：** 不再要求 writer 输出 ≥ registry 全量表格数。表格数量不是质量指标。

**改动：**
- `gates.py`：`run_hard_gates()` 中移除 H4 调用，或将 H4 永久标记为 skipped
- `prompt_builder.py`：`gates_to_constraints()` 中删除 H4 相关约束生成

#### 4b. H8（Number Fingerprint）保持不动

Writer 引用的数字仍需追溯到原文 PDF。source 范围保持"所有 Table definition pages"不变。

#### 4c. Fixer no-op 检测

**问题：** OLMo-3 profiling 中 fixer 花了 352s + 98K tokens 但输出与输入完全一致。

**方案：** Fixer 输出后，程序化 diff 检查：

```
if merged_fixed.md == merged.md:
    skip Gates R2
    cp merged.md → final.md
else:
    run Gates R2 on merged_fixed.md
```

**改动文件：** `.claude/commands/deepaper.md`（fixer 阶段后加 diff 检查逻辑）

**预期效果：** no-op 时省 352s + 98K tokens + Gates R2 的 3s。

---

## 不改的部分

- Writer auto-split 逻辑不变（仍然 writer-visual + writer-text-0/1）
- Writer-visual 不拆分（表格减负后观察实际耗时再定）
- H8 source 范围不变
- H1/H2/H3/H5/H6/H7/H9/H10 不变
- 模板 7 个章节结构不变
- 分类和保存流程不变

---

## 预期效果（以 OLMo-3 为基准）

| 阶段 | 现在 | 优化后 | 节省 |
|------|------|--------|------|
| Extractor | 857s (43 tool calls) | ~200s (1-2 reads) | ~657s |
| Extractor retry | 695s | 0s (不再触发) | 695s |
| Writer-visual | 642s | ~400s (表格减负) | ~242s |
| Fixer | 352s (no-op) | 0s (diff 跳过) | 352s |
| **总计** | **2,563s (43 min)** | **~620s (~10 min)** | **~1,943s (75%)** |

注：10 min 为乐观估计，保守预期 12-15 min。短论文（< 30 页）预期 5-8 min。

---

## 改动文件汇总

| 文件 | 改动类型 |
|------|---------|
| `src/deepaper/prompt_templates/extractor.md` | 重写：删全量抄表，加 KEY_FINDINGS，加分片策略，注入 core_tables |
| `src/deepaper/registry.py` | 新增：`identify_core_tables()` |
| `src/deepaper/cli.py` | 修改：extract 命令输出 core_tables.json |
| `src/deepaper/gates.py` | 修改：删除/跳过 H4 |
| `src/deepaper/prompt_builder.py` | 修改：删 H4 约束，改 writer 表格指引，注入文件大小和分片策略 |
| `.claude/commands/deepaper.md` | 修改：fixer no-op 检测，所有 agent 分片策略 |
