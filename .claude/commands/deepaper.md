Analyze an arxiv paper and save to the deepaper knowledge base using a multi-agent pipeline.

## Step 0: Setup

Run `which deepaper` to check. If not found: `pip install deepaper && deepaper init`.
If papers/ directory exists, skip init.

## Step 1: Download & Prepare

```bash
deepaper download $ARGUMENTS
```
Parse the JSON output to get `pdf_path` and `arxiv_id`.

Then **always** extract full text (mandatory, not optional):
```bash
python3 -c "
import fitz
doc = fitz.open('PDF_PATH')
with open('/tmp/ARXIV_ID.txt', 'w') as f:
    for i, page in enumerate(doc):
        f.write(f'--- PAGE {i+1} ---\n{page.get_text()}\n')
print(f'Total pages: {len(doc)}')
"
```

Also count tables and figures:
```bash
grep -o "Table [0-9]*" /tmp/ARXIV_ID.txt | sort -t' ' -k2 -n -u | tail -1
grep -o "Figure [0-9]*" /tmp/ARXIV_ID.txt | sort -t' ' -k2 -n -u | tail -1
```

Record: `TOTAL_PAGES`, `MAX_TABLE`, `MAX_FIGURE`, `PDF_PATH`, `TEXT_PATH=/tmp/ARXIV_ID.txt`.

## Step 2: Multi-Agent Pipeline

You are the **Conductor**. You do NOT read the paper yourself or write the analysis yourself. You orchestrate 5 agents:

```
Conductor (you)
  ├→ [1] Extractor    — reads paper, outputs structured notes
  ├→ [2] Writer-A     — writes frontmatter + 核心速览 + 动机 + 方法详解   ┐
  ├→ [3] Writer-B     — writes 实验与归因 + 专家批判                      ├ parallel
  ├→ [4] Writer-C     — writes 机制迁移分析 + 背景知识补充                 ┘
  ├→ [5] Critic       — quality gate audit, outputs verdict
  └→ [6] (if needed)  — fix specific sections per Critic's verdict
```

### Step 2.1: Spawn Extractor

Launch one Agent (subagent_type: `executor`, name: `extractor`):

**Prompt to Extractor — copy EXACTLY, filling in PDF_PATH, TEXT_PATH, TOTAL_PAGES, ARXIV_ID:**

```
You are a paper extraction specialist. Your ONLY job is to read an academic paper and output structured notes. Do NOT write any analysis or opinions.

## Paper
- PDF: {PDF_PATH}
- Text: {TEXT_PATH}
- Pages: {TOTAL_PAGES}
- ID: {ARXIV_ID}

## Task

Read the ENTIRE paper (every page including Appendix) using the PDF Read tool. Read in chunks of 20 pages, issue 2-3 parallel Read calls per round. You MUST cover pages 1 through {TOTAL_PAGES} — no skipping.

After reading, write structured notes to `/tmp/{ARXIV_ID}_notes.md` in EXACTLY this format. Every number MUST include its source (Table/Figure/Page number). Do not invent numbers.

```markdown
# Notes: {ARXIV_ID}

## META
- title:
- authors (first 5 + "et al."):
- date:
- pages: / tables: / figures:
- code_url:
- venue:

## MAIN RESULTS (copy every number from main result tables)
### Table X: [title]
[reproduce the full table in markdown — ALL rows, ALL columns, no omissions]
### Table Y: ...
(repeat for every main result table: base model tables, post-training tables, instruct tables)

## ABLATIONS (every ablation table with deltas)
### Table X: [title]
[full table + compute delta for key comparisons]
(repeat for all ablation tables)

## HYPERPARAMETERS (from Appendix)
### Table X: [title] (e.g. architecture, training config, SFT/DPO/RL params)
[full table in markdown]
(repeat for every hyperparameter table in the Appendix)

## FORMULAS
### Eq.N: [name]
- formula: (LaTeX)
- each symbol: name = definition (physical meaning)
- key parameter values from paper: ε=..., β=..., etc.
(repeat for every important equation)

## DATA COMPOSITION
### Pretraining
- Source | Type | Pool Size | Final Mix Size | Percentage
(full table)
### Midtraining / Post-training
(same format for each data stage, with token counts)

## EVAL CONFIG (from Appendix evaluation details table)
- Task | Format | Metric | Temp | Top-p | Max Tokens | N | # Subtasks
(full table)

## TRAINING COSTS & TIMELINE
- (every concrete number: days, GPUs, dollars, tokens/sec, etc.)

## DESIGN DECISIONS (non-obvious choices the authors made)
- Decision: X. Alternative: Y. Reason: Z. Evidence: Table/Section.
(list all)

## KEY FINDINGS (verbatim from paper's "Key Findings" sections)
- finding: "..." (section X.Y)
(list all)

## RELATED WORK (from paper's related work / discussion / comparison sections)
- Method | Paper/Citation | Relation to this work | Key difference | Shared mechanism
(list every method discussed in related work, discussion, or comparison sections)
(include at minimum: 3 ancestor methods, 2 sibling/concurrent methods)

## BASELINES (every model compared against, across ALL tables)
- model name (parameter count, type: fully-open/open-weight/closed)
(deduplicated list, ONE model per line — do NOT group multiple models on one line)
```

IMPORTANT:
- Reproduce tables COMPLETELY — every row, every column. Partial tables are a failure.
- If a table has >15 rows, still include ALL rows.
- Include numbers from the Appendix — hyperparameter tables, eval config tables, data composition tables.
- BASELINES: list each model on its own line. "Qwen 2.5 7B" and "Qwen 2.5 32B" are separate entries.
- RELATED WORK: this section is critical. Read the paper's related work / discussion sections carefully and extract every method comparison. If the paper lacks a formal related work section, extract from inline comparisons throughout the paper.
- The notes should be 10,000-20,000 characters. If shorter, you missed tables or related work.
- After writing notes, run: `wc -c /tmp/{ARXIV_ID}_notes.md` and report the count.
```

Wait for Extractor to complete. Verify notes exist and are >5,000 chars:
```bash
wc -c /tmp/ARXIV_ID_notes.md
```
If <5,000 chars, the extraction failed — re-run with explicit instructions to include all tables.

### Step 2.2: Spawn Writer-A, Writer-B, and Writer-C in parallel

Launch THREE agents simultaneously (all subagent_type: `executor`), named `writer-a`, `writer-b`, `writer-c`.

**CRITICAL FORMAT RULE for ALL writers:**
- Main section headings MUST use `####` (h4): `#### 核心速览 (Executive Summary)`
- Sub-section headings MUST use `#####` (h5): `##### 直觉版`
- Sub-sub-section headings use `######` (h6)
- Do NOT add any title like "Part A", "Part B", "Part C", "OLMo 3 深度分析" etc.
- Do NOT add horizontal rules `---` between sections (the Conductor handles separators)
- Start the file directly with content (Writer-A starts with `---\n` for YAML; Writer-B/C start with `####`)

**Prompt to Writer-A — copy EXACTLY, filling in variables:**

```
You are a technical paper analyst writing Part A of a structured analysis. Write in Chinese (中文).

## CRITICAL FORMAT RULES (violating these is a failure)
- Main sections: #### (h4) — e.g. `#### 核心速览 (Executive Summary)`
- Sub-sections: ##### (h5) — e.g. `##### 直觉版`
- Sub-sub-sections: ###### (h6)
- Do NOT add any title/header like "Part A" or "深度分析"
- Do NOT add horizontal rules (---) except inside YAML frontmatter
- Start your file with `---` (the YAML opening fence)

## Inputs
- Structured notes: /tmp/{ARXIV_ID}_notes.md (READ THIS FIRST)
- Full text for grep: {TEXT_PATH}
- PDF for visual verification: {PDF_PATH}

## Your job
Write ONLY these sections to `/tmp/{ARXIV_ID}_part_a.md`. Follow the format exactly.

### Section 1: YAML Frontmatter

```yaml
---
venue: "发表场所，未找到则 null"
publication_type: "conference/journal/preprint/workshop/thesis"
doi: null
keywords:
  - 5-10个技术关键词
tldr: "一句话核心贡献（≤100字，必须含具体数字如 MATH 96.2%）"
core_contribution: "new-method/new-dataset/new-benchmark/new-framework/survey/empirical-study/theoretical"
baselines:
  - "每个模型单独一行，不允许分组合并"
  - "格式: ModelName (参数量, type: fully-open/open-weight/closed)"
  - "如 'Qwen 2.5 7B' 和 'Qwen 2.5 32B' 必须拆为两行"
  - "从 notes 的 BASELINES 段逐行复制"
datasets:
  - "每个数据集必须标注 token 数/样本数和组成比例"
  - "格式: DatasetName (X tokens/samples: A% Source1 + B% Source2)"
  - "从 notes 的 DATA COMPOSITION 段逐项转换"
  - "评测数据集也列出，标注 (eval, N subtasks)"
metrics:
  - "每个指标必须标注评测配置"
  - "格式: MetricName (format, temp=X, top-p=Y, max_tokens=Z, N=K)"
  - "从 notes 的 EVAL CONFIG 表逐项转换"
code_url: "(从 notes META 段)"
---
```

**Frontmatter GATE — 写完后立即检查：**
1. baselines: 是否每个模型单独一行？如有分组（如 "Qwen 2.5 (7B/32B)"），必须拆开
2. datasets: 每项是否有 token 数/样本数？如缺，grep TEXT_PATH 找到并补充。评测数据集如无 token 数，标注 (eval) 即可
3. metrics: 每项是否有 eval config (temp, N, max_tokens)？如缺，grep "Table" TEXT_PATH 找到 Appendix eval table 的页码，Read PDF 那几页补充

### Section 2: 核心速览 (Executive Summary)

- **TL;DR:** 必须含具体量化数字（如"MATH 96.2%"），不接受"显著提升"
- **一图流:** "旧方法是X → 新方法是Y"的对比结构
- **核心机制一句话:** `[动作] + [对象] + [方式] + [效果]`

### Section 3: 动机与第一性原理 (Motivation & First Principles)

- **痛点:** 引用≥2个baseline的具体数字（从notes MAIN RESULTS段取）
- **核心洞察:** Because→Therefore因果链≥3步，每步有论据
- **物理/直觉解释:** 一个完整类比

### Section 4: 方法详解 (Methodology)

**字符数 GATE: ≥12,000 字符。写完后立即 `wc -c` 检查。不足则从 notes 的 HYPERPARAMETERS 和 FORMULAS 段补充。**

包含：
- **直觉版:** 引用 Figure (方法概览图)，旧→新对比
- **精确版:**
  - 完整数据流图 (Input→...→Output)，从 notes DATA COMPOSITION 段取数字
  - 关键公式：从 notes FORMULAS 段复制，补充物理含义
  - 数值推演：用具体数字走一遍核心算法
  - 伪代码：Python/PyTorch 风格
  - **超参数表：** 从 notes HYPERPARAMETERS 段复制为 markdown 表格（必须包含 Appendix 的完整表）
- **设计决策 (≥3,000 字符 GATE):** 从 notes DESIGN DECISIONS 段展开。每个决策必须包含：
  - 替代方案是什么
  - 论文是否做了对比？结果如何？（引用具体 Table/Figure 编号和数字）
  - 选择背后的核心 trade-off 是什么
  - 一句话解释 WHY 本文选择优于替代方案
  写完后 wc -c 检查设计决策段是否 ≥3,000 字符，不足则从 notes 补充更多决策。
- **易混淆点:** ≥3个 "❌错误理解 / ✅正确理解" 对

**写完后执行：**
```bash
python3 -c "
text = open('/tmp/{ARXIV_ID}_part_a.md').read()
method_start = text.find('#### 方法详解')
method_end = text.find('#### 实验') if '#### 实验' in text else len(text)
method_chars = len(text[method_start:method_end]) if method_start >= 0 else 0
print(f'Methodology chars: {method_chars}')
if method_chars < 12000: print('WARNING: BELOW 12K GATE — add more hyperparameter tables and formulas')
# Check design decisions sub-gate
dd_start = text.find('##### 设计决策') if '##### 设计决策' in text else text.find('设计决策')
dd_end = text.find('##### 易混淆') if '##### 易混淆' in text else text.find('易混淆')
if dd_start >= 0 and dd_end > dd_start:
    dd_chars = len(text[dd_start:dd_end])
    print(f'Design decisions chars: {dd_chars}')
    if dd_chars < 3000: print('WARNING: BELOW 3K DESIGN DECISIONS GATE')
"
```
如果任一 gate 不达标，从 notes 补充直到达标。
```

**Prompt to Writer-B — copy EXACTLY:**

```
You are a technical paper analyst writing Part B of a structured analysis. Write in Chinese (中文).

## CRITICAL FORMAT RULES (violating these is a failure)
- Main sections: #### (h4) — e.g. `#### 实验与归因 (Experiments & Attribution)`
- Sub-sections: ##### (h5) — e.g. `##### 对比表格`
- Do NOT add any title/header like "Part B" or "深度分析"
- Do NOT add horizontal rules (---) at the start or between sections
- Start your file directly with `#### 实验与归因`

## Inputs
- Structured notes: /tmp/{ARXIV_ID}_notes.md (READ THIS FIRST)
- Full text for grep: {TEXT_PATH}
- PDF for visual verification: {PDF_PATH}

## Your job
Write ONLY these 2 sections to `/tmp/{ARXIV_ID}_part_b.md`. Follow the format exactly.

### Section 5: 实验与归因 (Experiments & Attribution)

- **对比表格:** ≥2张完整 markdown 表格。从 notes MAIN RESULTS 段的完整表格转录。**包含 ALL baselines，不能只挑 top-3。** 如果 notes 有4张主表，输出4张。每张表后附 1-2 句关键发现。
- **归因排序:** 从 notes ABLATIONS 段按 delta 大小排序，每个组件标注具体数字。格式：
  - 组件名 (+X.X on Metric, Table N): 一句话解释为什么贡献大
- **可信度检查:** ≥3个维度（去污染、baseline公平性、未报告负面结果——从 notes KEY FINDINGS 段找线索）

### Section 6: 专家批判 (Critical Review)

- **隐性成本:** ≥4个论文未明说的代价，每个必须含具体数字。从 notes TRAINING COSTS 段 + 论文 footnotes 提取。如不足4个，grep TEXT_PATH 搜索 "day" "hour" "cost" "GPU" "node" "Lambda" "budget" "compute" "wall" "infra" 等关键词定位隐藏成本。
- **最值得复用的技术:** 1-2个可直接复用的方法，标注实现成本（改几行代码/需要集群/etc.）和预期收益
- **最大的坑:** 1-2个复现/落地的坑，标注具体数字和规避方法
- **关联技术:** ≥3个同期/经典方法对比。从 notes RELATED WORK 段取素材。每个对比必须包含：
  - 与本文的共同点和差异
  - 具体 benchmark 数字对比（从 notes MAIN RESULTS 段取）
  - 什么场景下该选哪个

**写完后执行隐性成本计数：**
```bash
python3 -c "
text = open('/tmp/{ARXIV_ID}_part_b.md').read()
import re
cost_section = text[text.find('隐性成本'):text.find('最值得复用')] if '隐性成本' in text else ''
numbers = re.findall(r'\d+[\d,.]*\s*(?:天|day|hour|小时|GPU|node|节点|美元|\$|%|倍|x|Mtok|万|M|B|K|T)', cost_section)
print(f'Hidden costs with numbers: {len(numbers)} occurrences found')
if len(numbers) < 3: print('WARNING: BELOW 3 HIDDEN COSTS GATE')
"
```
```

**Prompt to Writer-C — copy EXACTLY:**

```
You are a technical paper analyst writing Part C of a structured analysis. Write in Chinese (中文).

## CRITICAL FORMAT RULES (violating these is a failure)
- Main sections: #### (h4) — e.g. `#### 机制迁移分析 (Mechanism Transfer Analysis)`
- Sub-sections: ##### (h5) — e.g. `##### 机制解耦表格`
- Do NOT add any title/header like "Part C" or "深度分析"
- Do NOT add horizontal rules (---) at the start or between sections
- Start your file directly with `#### 机制迁移分析`

## Inputs
- Structured notes: /tmp/{ARXIV_ID}_notes.md (READ THIS FIRST — especially RELATED WORK and DESIGN DECISIONS sections)
- Full text for grep: {TEXT_PATH}
- PDF for visual verification: {PDF_PATH}

## Your job
Write ONLY these 2 sections to `/tmp/{ARXIV_ID}_part_c.md`. Follow the format exactly.

**字符数 GATE: 机制迁移分析 ≥5,000 字符。写完后立即 `wc -c` 检查。**

### Section 7: 机制迁移分析 (Mechanism Transfer Analysis)

##### 机制解耦表格
3-5个计算原语（不是2-4个！），四列全填（名称/本文用途/抽象描述/信息论直觉）。从 notes 的 DESIGN DECISIONS 段提取候选原语。每个原语的"抽象描述"列必须剥离本文领域术语，用通用的计算/信息论语言重述。

##### 迁移处方
每个原语≥1个跨领域场景，四要素缺一不可：
- **目标领域+具体问题：** 不是泛泛说"NLP"，要具体到任务（如"推荐系统的多源特征配比优化"）
- **怎么接：** 具体到替换现有 pipeline 的哪个组件，输入输出是什么
- **预期收益：** 引用本文的具体提升数字作为类比依据（如"参考 OLMo 3 的 4x 吞吐提升"）
- **风险/不适用条件：** 具体说明什么情况下迁移会失败

##### 机制家族图谱
从 notes 的 RELATED WORK 段取素材：
- **前身(Ancestors)：** ≥4个，每个标注：方法名(引用) + 与本文的继承关系 + 本文做了什么改进。优先从 notes RELATED WORK 中的 ancestor 条目提取。
- **兄弟(Siblings)：** ≥3个同期工作，每个标注：在具体 benchmark 上的数字对比 + 核心差异。从 notes MAIN RESULTS 和 RELATED WORK 段交叉提取。
- **后代(Descendants)：** 从引用提取或标注"暂无"
- **创新增量：** 2-3句话，比单纯"系统集成"更具体——本文组合的独特之处是什么

### Section 8: 背景知识补充 (Background Context)

论文中每个被依赖的外部技术用表格输出（≥8项）：

| 外部技术 | 一句话定义 | 在本文中的角色 | 核心引用 |
|---|---|---|---|

从 notes 的 RELATED WORK、FORMULAS、HYPERPARAMETERS 段识别所有外部依赖。如果 notes 列出的外部技术不足8个，grep TEXT_PATH 搜索常见技术名（如 "RoPE" "SwiGLU" "Flash" "vLLM" "DPO" "GRPO"）补充。

**写完后执行：**
```bash
python3 -c "
text = open('/tmp/{ARXIV_ID}_part_c.md').read()
transfer_start = text.find('#### 机制迁移分析')
transfer_end = text.find('#### 背景知识') if '#### 背景知识' in text else len(text)
chars = len(text[transfer_start:transfer_end]) if transfer_start >= 0 else 0
print(f'Mechanism transfer chars: {chars}')
if chars < 5000: print('WARNING: BELOW 5K GATE — add more primitives, longer prescriptions, more ancestors/siblings')
"
```
如果 <5,000，补充更多原语或更详细的迁移处方。
```

### Step 2.3: Concatenate & Post-process

After all three writers complete, concatenate and normalize:

```bash
cat /tmp/ARXIV_ID_part_a.md /tmp/ARXIV_ID_part_b.md /tmp/ARXIV_ID_part_c.md > /tmp/deepaper_raw.md

# Post-process: fix heading levels, remove stray dividers and part titles
python3 -c "
import re
text = open('/tmp/deepaper_raw.md').read()

# Remove any 'Part A/B/C' or '深度分析' title lines
text = re.sub(r'^#+ .*(?:Part [ABC]|深度分析|部分).*\n+', '', text, flags=re.MULTILINE)

# Remove stray horizontal rules between sections (keep only inside frontmatter)
parts = text.split('---', 2)  # split at YAML fences
if len(parts) >= 3:
    yaml_block = parts[0] + '---' + parts[1] + '---'
    body = parts[2]
    # Remove standalone --- lines in body
    body = re.sub(r'\n---\s*\n', '\n\n', body)
    text = yaml_block + body

# Normalize main section headings to #### (h4)
# Match lines like ## N. 实验 or ## 实验 or ### 实验 and convert to ####
def normalize_heading(m):
    hashes = m.group(1)
    num_prefix = m.group(2) or ''
    title = m.group(3)
    # If it's a main section (核心速览/动机/方法详解/实验/专家批判/机制迁移/背景知识), force ####
    main_keywords = ['核心速览', '动机', '方法详解', '实验与归因', '专家批判', '机制迁移', '背景知识']
    for kw in main_keywords:
        if kw in title:
            return f'#### {num_prefix}{title}'
    return m.group(0)  # leave non-main headings unchanged

text = re.sub(r'^(#{1,6})\s+(\d+\.\s+)?(.*(?:核心速览|动机|方法详解|实验与归因|专家批判|机制迁移|背景知识).*)', normalize_heading, text, flags=re.MULTILINE)

# Ensure no double blank lines
text = re.sub(r'\n{3,}', '\n\n', text)

open('/tmp/deepaper_analysis.md', 'w').write(text)
print(f'Post-processed: {len(text)} chars')
"

wc -c /tmp/deepaper_analysis.md
```

### Step 2.4: Spawn Critic (with retry and fallback)

**Attempt to launch Critic agent (up to 2 retries with 30s wait between attempts).**

Launch one Agent (name: `critic`):

**Prompt to Critic — copy EXACTLY:**

```
You are a quality auditor for academic paper analyses. Your job is to check a draft analysis against mandatory quality gates and output a structured verdict. You do NOT rewrite — you only diagnose.

## Input
- Draft analysis: /tmp/deepaper_analysis.md
- Paper notes (ground truth for fact-checking): /tmp/{ARXIV_ID}_notes.md

Read both files completely.

## Quality Gates — check each one

Run the following checks and report results:

### Gate 1: TL;DR contains specific numbers
- Look for the TL;DR line. Does it contain at least 2 specific benchmark numbers (e.g., "MATH 96.2%")?
- PASS/FAIL

### Gate 2: Pain points cite baseline numbers
- In "动机与第一性原理", are there ≥2 specific baseline numbers (e.g., "OLMo 2 MATH 49.2%")?
- PASS/FAIL

### Gate 3: Causal chain ≥3 steps
- Count Because→Therefore or numbered causal steps
- PASS(N steps)/FAIL

### Gate 4: Methodology ≥12,000 characters
```bash
python3 -c "
text = open('/tmp/deepaper_analysis.md').read()
starts = ['#### 方法详解', '## 方法详解', '### 方法详解']
end_markers = ['#### 实验', '## 实验', '### 实验']
start = -1
for s in starts:
    if s in text: start = text.find(s); break
end = len(text)
for e in end_markers:
    if e in text and text.find(e) > start: end = text.find(e); break
if start >= 0:
    chars = len(text[start:end])
    print(f'Methodology: {chars} chars')
    print('PASS' if chars >= 12000 else 'FAIL')
else:
    print('FAIL: methodology section not found')
"
```
- PASS(N chars)/FAIL(N chars, need +M more)

### Gate 5: ≥2 complete comparison tables
- Count markdown tables in 实验 section that have ≥5 rows and ≥4 columns
- PASS(N tables)/FAIL

### Gate 6: Attribution has specific numbers
- In 归因排序, does each component cite a specific delta number?
- PASS/FAIL + list components missing numbers

### Gate 7: ≥3 hidden costs with numbers
- In 隐性成本, count distinct cost items that include a number
- PASS(N costs)/FAIL

### Gate 8: Transfer prescriptions complete
- For each 迁移处方, check all 4 elements: 目标领域, 怎么接, 预期收益, 风险
- PASS/FAIL + which prescriptions are incomplete

### Gate 9: Mechanism family counts
- Ancestors ≥4, Siblings ≥3
- PASS(A ancestors, S siblings)/FAIL

### Gate 10: Frontmatter completeness
- baselines: each model on its own line (no grouped entries like "Qwen 2.5 (7B/32B)")?
- datasets: each entry has token count or sample count?
- metrics: each entry has eval config (temp, N, max_tokens)?
- PASS/FAIL + list incomplete entries

### Gate 11: Factual consistency with notes
- Sample 5 numbers from the draft analysis. Look up each in the notes. Do they match?
- PASS/FAIL + list mismatches

### Gate 12: Heading format consistency
- All main sections use #### (h4)?
- No stray "Part A/B/C" titles?
- No stray --- horizontal rules in body?
- PASS/FAIL

## Output format

Write your verdict to `/tmp/{ARXIV_ID}_verdict.md`:

```markdown
# Quality Verdict: {ARXIV_ID}

## Gate Results
| # | Gate | Result | Details |
|---|------|--------|---------|
| 1 | TL;DR numbers | PASS/FAIL | ... |
| 2 | Pain point baselines | PASS/FAIL | ... |
...

## Failed Gates — Required Actions
(only if any gate failed)

### Gate N: [name] — FAIL
**Problem:** ...
**Action:** [specific instruction for what to add/fix, referencing notes sections]
**Location:** [which section of the draft to modify]

## Factual Issues
(if any numbers don't match notes)

## Overall: PASS / NEEDS REVISION (N gates failed)
```
```

**If the Critic agent fails (API error, timeout, etc.), use the inline fallback — run this script yourself as Conductor:**

```bash
python3 << 'PYEOF'
import re, yaml

draft = open('/tmp/deepaper_analysis.md').read()
notes = open('/tmp/ARXIV_ID_notes.md').read()

results = []

# Gate 1: TL;DR numbers
fm_match = re.match(r'^---\s*\n(.*?)\n---', draft, re.DOTALL)
fm = yaml.safe_load(fm_match.group(1)) if fm_match else {}
tldr = str(fm.get('tldr', ''))
g1 = len(re.findall(r'\d+\.?\d*%', tldr)) >= 2
results.append(('TL;DR numbers', g1, f'{len(re.findall(r"%", tldr))} percentages'))

# Gate 2: Pain point baselines
motiv = draft[draft.find('动机'):draft.find('方法详解')] if '动机' in draft and '方法详解' in draft else ''
g2_nums = re.findall(r'(?:OLMo|Qwen|Llama|Gemma|DeepSeek|GPT|Marin|Apertus)[^\n]{0,40}\d+\.?\d*%', motiv)
results.append(('Pain point baselines', len(g2_nums) >= 2, f'{len(g2_nums)} found'))

# Gate 3: Causal chain
g3 = len(re.findall(r'Because|Therefore|因此|所以|→|导致|从而', motiv)) >= 3
results.append(('Causal chain', g3, ''))

# Gate 4: Methodology ≥12K
for s in ['#### 方法详解', '### 方法详解', '## 方法详解']:
    if s in draft:
        mstart = draft.find(s); break
else:
    mstart = -1
for e in ['#### 实验', '### 实验', '## 实验']:
    idx = draft.find(e)
    if idx > mstart > -1:
        mend = idx; break
else:
    mend = len(draft)
mchars = mend - mstart if mstart >= 0 else 0
results.append(('Methodology ≥12K', mchars >= 12000, f'{mchars} chars'))

# Gate 5: ≥2 tables in experiments
exp_start = draft.find('实验与归因')
exp_end = draft.find('专家批判') if '专家批判' in draft else len(draft)
exp = draft[exp_start:exp_end] if exp_start >= 0 else ''
in_t = False; rows = 0; big = 0
for line in exp.split('\n'):
    s = line.strip()
    if s.startswith('|') and s.endswith('|'):
        if not in_t: in_t = True; rows = 1
        else: rows += 1
    else:
        if in_t and rows >= 5: big += 1
        in_t = False; rows = 0
if in_t and rows >= 5: big += 1
results.append(('≥2 comparison tables', big >= 2, f'{big} tables'))

# Gate 7: ≥3 hidden costs
cost_sec = draft[draft.find('隐性成本'):draft.find('最值得复用')] if '隐性成本' in draft and '最值得复用' in draft else ''
cost_nums = re.findall(r'\d+[\d,.]*\s*(?:天|day|hour|小时|GPU|node|美元|\$|%|倍|x|M|B|K|T)', cost_sec)
results.append(('≥3 hidden costs', len(cost_nums) >= 3, f'{len(cost_nums)} number refs'))

# Gate 9: Family counts
fam = draft[draft.find('前身'):draft.find('背景知识')] if '前身' in draft else ''
anc = len(re.findall(r'^\s*\d+\.?\s+\*\*', fam, re.MULTILINE))
sib_sec = fam[fam.find('兄弟'):] if '兄弟' in fam else ''
sibs = len(re.findall(r'^\s*\d+\.?\s+\*\*', sib_sec, re.MULTILINE))
results.append(('Ancestors≥4/Siblings≥3', anc >= 4 and sibs >= 3, f'A={anc} S={sibs}'))

# Gate 10: Baselines format
baselines = fm.get('baselines', [])
grouped = sum(1 for b in baselines if re.search(r'\d+B/\d+B|\(\d+B,\s*\d+B\)', str(b)))
results.append(('Baselines one-per-line', grouped == 0 and len(baselines) >= 5, f'{len(baselines)} entries, {grouped} grouped'))

# Gate 12: Heading format
g12a = '#### 核心速览' in draft and '#### 方法详解' in draft and '#### 实验与归因' in draft
g12b = 'Part A' not in draft and 'Part B' not in draft and 'Part C' not in draft
results.append(('Heading format', g12a and g12b, ''))

print('# Inline Critic Results')
failed = []
for name, passed, detail in results:
    status = 'PASS' if passed else 'FAIL'
    print(f'| {name:<25} | {status} | {detail}')
    if not passed: failed.append(name)
print(f'\nOverall: {"PASS" if not failed else "NEEDS REVISION"} ({len(failed)} failed)')
if failed: print(f'Failed: {", ".join(failed)}')
PYEOF
```

Review the output. If any gates failed, fix them directly using the Edit tool on `/tmp/deepaper_analysis.md`, referencing `/tmp/ARXIV_ID_notes.md` for correct data.

### Step 2.5: Handle Critic Verdict

Read `/tmp/ARXIV_ID_verdict.md` (if Critic agent succeeded) or use inline results.

**If PASS:** Go to Step 3.

**If NEEDS REVISION:** For each failed gate, either:
- (a) Fix it yourself with Edit tool (for simple additions like adding a missing number), OR
- (b) Spawn a targeted `executor` agent with a specific fix prompt:

```
Fix the following issues in /tmp/deepaper_analysis.md:

1. [paste failed gate action from verdict]
2. [paste failed gate action from verdict]

CRITICAL FORMAT RULES:
- Main sections: #### (h4)
- Sub-sections: ##### (h5)
- Do NOT add "Part" titles or --- horizontal rules

Reference data is in /tmp/{ARXIV_ID}_notes.md.
Paper text for grep is at {TEXT_PATH}.

Edit the file directly using the Edit tool. Do NOT rewrite the entire file — only patch the specific sections mentioned above.
```

After fixes, optionally re-run Critic (max 2 total rounds). If still failing after 2 rounds, save anyway with a note.

## Step 3: Save

```bash
deepaper save ARXIV_ID --category CATEGORY --input /tmp/deepaper_analysis.md
```

Category choices:
- `llm/pretraining` `llm/alignment` `llm/reasoning` `llm/efficiency` `llm/agent`
- `recsys/matching` `recsys/ranking` `recsys/llm-as-rec` `recsys/generative-rec` `recsys/system`
- `multimodal/vlm` `multimodal/generation` `multimodal/understanding`
- `misc`

## Step 4: Citations (optional)

```bash
deepaper cite ARXIV_ID --update
```

## Reference: Section Template (for Writer agents)

Each section heading uses `####` (h4). The full analysis structure is:

```
---
(YAML frontmatter)
---
#### 核心速览 (Executive Summary)
#### 动机与第一性原理 (Motivation & First Principles)
#### 方法详解 (Methodology)
#### 实验与归因 (Experiments & Attribution)
#### 专家批判 (Critical Review)
#### 机制迁移分析 (Mechanism Transfer Analysis)
#### 背景知识补充 (Background Context)
```
