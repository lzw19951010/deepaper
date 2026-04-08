# Pipeline Issues Log — 2026-04-06

基于 3 次完整 pipeline 运行（同一篇论文 2512.13961 OLMo 3, 117 页）暴露的问题，按优先级排序。

---

## P0: 必须修复

### 1. `deepaper gates` 不自动保存 gates.json
- **现象**: `deepaper fix` 依赖 `gates.json` 文件，但 `deepaper gates` 只输出到 stdout，不写文件
- **影响**: 每次都需要手动 `deepaper gates ARXID > gates.json`，否则 fix 报错
- **建议**: `deepaper gates` 自动写入 `{run_dir}/gates.json`

### 2. H2 Gate (subsection coverage) 结构性误判
- **现象**: TOC parser 将表格内的数值行误识别为 subsection（如 `subsection:92.6\nAIME 2024`、`subsection:0.751\nTravel and Tourism`）
- **数据**: 3 次运行 H2 均 fail，即使人工添加了完整的 §X.Y 引用，coverage 仍为 0.0077
- **根因**: `extract` 阶段的 TOC 解析逻辑不区分真实章节标题和表格 cell，对于多表格论文会产生数百个虚假 subsection
- **影响**: 每次都触发无效的 fixer 流程（浪费 ~2-8 min + ~50-111K tokens）
- **建议**:
  - 修复 TOC parser，过滤掉以数字开头的行（大概率是表格数据）
  - 或者在 H2 中只匹配 `X.Y` 格式的章节编号（如 `2.1`, `3.4`），忽略其他
  - 验证: 117 页论文实际只有 ~23 个真实 subsection（§2.1-§6.2）

---

## P1: 显著优化

### 3. writer-visual 是瓶颈（5-7x 慢于其他 writer）
- **数据**: 3 次运行 writer-visual 耗时 465s/642s/1099s，而 text-0 和 text-1 稳定在 163-210s
- **根因**: writer-visual 负责「方法详解」(建议~16,650字符) + 「实验与归因」(建议~12,960字符)，产出量是其他 writer 的 3-5 倍，且包含表格、伪代码、数值推演等重格式内容
- **建议**: 将 writer-visual 拆分为 2 个 writer:
  - writer-method: 方法详解（直觉版 + 精确版 + 设计决策 + 易混淆点）
  - writer-experiment: 实验与归因（核心收益 + 归因分析 + 可信度检查）
- **预期收益**: 并行后 writer 阶段从 ~1099s 降至 ~500s（约 2x 加速）

### 4. Extractor 首轮总是缺少页码引用 → 总是需要 retry
- **数据**: 3 次运行 extractor 首轮 coverage_ratio 均为 0.0，retry 才补上
- **耗时**: retry 额外消耗 239-695s
- **根因**: extractor prompt 中虽有 `(p.X)` 格式说明，但没有足够强的约束
- **建议**:
  - 在 extractor prompt 中加入硬约束: "每个 KEY_FINDINGS 条目必须以 `(p.XX)` 或 `(pp.XX-YY)` 结尾"
  - 在 prompt 末尾加入格式示例
  - 或在 `deepaper check` 中将 coverage 检查提前到 struct_check 同级，让 extractor 一次性通过

---

## P2: 改善体验

### 5. writer-visual 耗时波动大（465s-1099s，2.4x 方差）
- **现象**: 同一论文同一 prompt，writer-visual 耗时在 Run 2 和 Run 3 之间差 2.4 倍
- **可能原因**: LLM 推理路径差异、输出长度不确定、网络波动
- **建议**: 监控各 writer 的输出 char 数与耗时的比率（chars/s），建立基准线

### 6. Fixer 对 H2 无效但仍被触发
- **现象**: fixer 花费 129-495s 尝试修复 H2，但因 H2 是 parser bug 导致永远无法通过
- **建议**: 在 gates 输出中区分 "content issue" vs "parser/tool issue"，对后者跳过 fixer

### 7. 非 H2 的 gate 质量在 Run 3 显著提升
- **数据**: Run 1/2 有多个 gate 失败 (H2/H4/H5/H6/H8)，Run 3 仅 H2 失败
- **可能原因**: 前几次迭代中对 writer prompt 的优化（hardcoded Read commands, 质量合同）生效
- **结论**: prompt 工程的优化方向是正确的，继续保持

---

## 优化优先级路线图

```
短期 (P0):
  gates.json 自动保存 → 1 行代码改动
  H2 TOC parser 修复 → 可消除 fixer 阶段 (~2-8 min)

中期 (P1):
  writer-visual 拆分 → writer 阶段 2x 加速
  extractor 页码硬约束 → 消除 retry (~4-10 min)

合计预期: pipeline 从 ~31 min 降至 ~15 min (2x 加速)
```
