<!-- deepaper-version: 2 -->
Analyze an arxiv paper and save to the deepaper knowledge base using a multi-agent pipeline.

## Step 0: Setup

Run `which deepaper` to check. If not found: `pip install deepaper && deepaper init`.
If papers/ directory exists, skip init.

## Step 1: Download & Text Extraction

### 1.1 Download

```bash
deepaper download $ARGUMENTS
```
Parse the JSON output to get `pdf_path` and `arxiv_id`.

### 1.2 Create run directory and extract text

All intermediate files go to `.deepaper/runs/{ARXIV_ID}/`. Create it and extract text:

```bash
mkdir -p .deepaper/runs/ARXIV_ID

python3 -c "
import fitz, json
doc = fitz.open('PDF_PATH')
text_by_page = {}
full_lines = []
for i, page in enumerate(doc):
    text = page.get_text()
    text_by_page[str(i+1)] = text
    full_lines.append(f'--- PAGE {i+1} ---\n{text}')
with open('.deepaper/runs/ARXIV_ID/text_by_page.json', 'w') as f:
    json.dump(text_by_page, f, ensure_ascii=False, indent=2)
with open('.deepaper/runs/ARXIV_ID/text.txt', 'w') as f:
    f.write('\n'.join(full_lines))
print(f'Total pages: {len(doc)}')
"
```

Record: `TOTAL_PAGES`, `PDF_PATH`, `RUN_DIR=.deepaper/runs/ARXIV_ID`.

### 1.3 Build visual registry, paper profile, core figures, and figure contexts

```bash
deepaper registry ARXIV_ID
```

Then compute paper_profile, core_figures, and figure_contexts:

```bash
python3 -c "
import json
from deepaper.pipeline_io import safe_read_json, safe_write_json
from deepaper.registry import compute_paper_profile, identify_core_figures, extract_figure_contexts

run_dir = '.deepaper/runs/ARXIV_ID'
text_by_page_raw = safe_read_json(f'{run_dir}/text_by_page.json', {})
text_by_page = {int(k): v for k, v in text_by_page_raw.items()}
registry = safe_read_json(f'{run_dir}/visual_registry.json', {})

profile = compute_paper_profile(text_by_page, registry)
safe_write_json(f'{run_dir}/paper_profile.json', profile)

core_figs = identify_core_figures(registry, text_by_page, profile['total_pages'])
safe_write_json(f'{run_dir}/core_figures.json', core_figs)

fig_contexts = extract_figure_contexts(text_by_page, core_figs)
safe_write_json(f'{run_dir}/figure_contexts.json', fig_contexts)

print(json.dumps({
    'total_pages': profile['total_pages'],
    'num_tables': profile['num_tables'],
    'num_figures': profile['num_figures'],
    'num_equations': profile['num_equations'],
    'core_figures': [cf['key'] for cf in core_figs],
}, indent=2))
"
```

Record: `TOTAL_PAGES`, `NUM_TABLES`, `NUM_FIGURES`, `CORE_FIGURE_KEYS`.

Read the figure_contexts file and keep it available for Writer prompts:
```bash
cat .deepaper/runs/ARXIV_ID/figure_contexts.json
```
Store this as `FIGURE_CONTEXTS_JSON` for use in Writer prompts.

Also identify Table definition pages from the visual registry (needed by Writer-Visual):
```bash
python3 -c "
from deepaper.pipeline_io import safe_read_json
reg = safe_read_json('.deepaper/runs/ARXIV_ID/visual_registry.json', {})
table_pages = sorted(set(
    v['definition_page'] for v in reg.values()
    if v.get('type') == 'Table' and v.get('definition_page')
))
print('Table definition pages:', table_pages)
"
```
Record these as `TABLE_DEF_PAGES`.

## Step 2: Multi-Agent Pipeline

You are the **Conductor**. You do NOT read the paper yourself or write the analysis yourself. You orchestrate specialized agents:

```
Conductor (you)
  ├→ [1] Extractor      — reads text.txt (NOT PDF), outputs structured notes
  ├→ [2] StructCheck + Auditor (programmatic, via Python)
  │       → if missing/thin sections: 1 retry to Extractor
  ├→ [3] Writer-Visual   — 方法详解 + 实验与归因 (gets figure_contexts + Table PDF pages)  ┐
  ├→ [4] Writer-Text-1   — YAML + 核心速览 + 动机 + 专家批判 (gets figure_contexts)        ├ parallel
  ├→ [5] Writer-Text-2   — 机制迁移分析 + 背景知识补充 (gets figure_contexts)               ┘
  ├→ [6] Merge (fixed order: Text-1 + Visual + Text-2)
  ├→ [7] HardGates (programmatic, via `deepaper gates`)
  │       → if failed: skip Critic, go to Fixer
  ├→ [8] SoftGates / Critic (LLM, 7 semantic gates, JSON output)
  ├→ [9] Fixer (max 2 rounds, select best version)
  └→ [10] Save + Report
```

### Step 2.1: Spawn Extractor

Launch one Agent (subagent_type: `executor`, name: `extractor`):

**Prompt to Extractor — copy EXACTLY, filling in RUN_DIR, TOTAL_PAGES, ARXIV_ID:**

```
You are a paper extraction specialist. Your ONLY job is to read an academic paper's extracted text and output structured notes. Do NOT write any analysis or opinions.

## Paper
- Text: {RUN_DIR}/text.txt
- Pages: {TOTAL_PAGES}
- ID: {ARXIV_ID}

## Task

Read the ENTIRE text file {RUN_DIR}/text.txt using the Read tool. Read in chunks if needed. You MUST cover all pages — no skipping.

IMPORTANT: Read text.txt, NOT the PDF. The text file is much cheaper in tokens and contains all the information you need.

After reading, write structured notes to `{RUN_DIR}/notes.md` in EXACTLY this format. Every number MUST include its source (Table/Figure/Page number). Do not invent numbers.

```markdown
# Notes: {ARXIV_ID}

## META
- title:
- authors (first 5 + "et al."):
- date:
- pages: / tables: / figures:
- code_url:
- venue:

## MAIN_RESULTS (copy every number from main result tables)
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

## DATA_COMPOSITION
### Pretraining
- Source | Type | Pool Size | Final Mix Size | Percentage
(full table)
### Midtraining / Post-training
(same format for each data stage, with token counts)

## EVAL_CONFIG (from Appendix evaluation details table)
- Task | Format | Metric | Temp | Top-p | Max Tokens | N | # Subtasks
(full table)

## TRAINING_COSTS
- (every concrete number: days, GPUs, dollars, tokens/sec, etc.)

## DESIGN_DECISIONS (non-obvious choices the authors made)
- Decision: X. Alternative: Y. Reason: Z. Evidence: Table/Section.
(list all)

## RELATED_WORK (from paper's related work / discussion / comparison sections)
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
- After writing notes, run: `wc -c {RUN_DIR}/notes.md` and report the count.
```

Wait for Extractor to complete. Verify notes exist and are >5,000 chars:
```bash
wc -c .deepaper/runs/ARXIV_ID/notes.md
```
If <5,000 chars, the extraction failed — re-run with explicit instructions to include all tables.

### Step 2.2: StructCheck + Auditor (programmatic)

Run StructCheck and Auditor on the Extractor output:

```bash
python3 -c "
import json
from deepaper.pipeline_io import safe_read_json
from deepaper.extractor import struct_check, audit_coverage

run_dir = '.deepaper/runs/ARXIV_ID'
notes = open(f'{run_dir}/notes.md').read()
text_by_page_raw = safe_read_json(f'{run_dir}/text_by_page.json', {})
text_by_page = {int(k): v for k, v in text_by_page_raw.items()}
profile = safe_read_json(f'{run_dir}/paper_profile.json', {})
total_pages = profile.get('total_pages', TOTAL_PAGES)

sc = struct_check(notes, total_pages, profile)
ac = audit_coverage(text_by_page, notes, total_pages)

result = {
    'struct_check': sc,
    'audit': {
        'coverage_ratio': ac['coverage_ratio'],
        'uncovered_segments': ac['uncovered_segments'],
    }
}
print(json.dumps(result, indent=2))
"
```

**If StructCheck or Auditor fails**, spawn a targeted Extractor retry (max 1 retry total):

Launch one Agent (subagent_type: `executor`, name: `extractor-retry`):

```
You are a paper extraction specialist doing a targeted补充. Read {RUN_DIR}/text.txt and the existing notes at {RUN_DIR}/notes.md.

## Issues to fix:
{paste the struct_check missing_sections and thin_sections, and/or audit uncovered_segments}

## Task:
- For missing/thin sections: read the relevant parts of text.txt and add the missing content to notes.md
- For uncovered page segments: read those pages from text.txt and add any important information to the relevant sections
- Do NOT rewrite existing content — only ADD missing information
- Mark sections where the paper truly provides no information as: "⚠️ 论文未提供该信息"
- After editing, run: `wc -c {RUN_DIR}/notes.md`
```

After retry (or if StructCheck+Auditor passed initially), proceed to Writers.

### Step 2.3: Spawn Writer-Visual, Writer-Text-1, and Writer-Text-2 in parallel

Launch THREE agents simultaneously (all subagent_type: `executor`).

**CRITICAL FORMAT RULE for ALL writers:**
- Main section headings MUST use `####` (h4): `#### 核心速览 (Executive Summary)`
- Sub-section headings MUST use `#####` (h5): `##### 直觉版`
- Sub-sub-section headings use `######` (h6)
- Do NOT add any title like "Part A", "Part B", "Part C", "OLMo 3 深度分析" etc.
- Do NOT add horizontal rules `---` between sections (the Conductor handles separators)
- Writer-Text-1 starts with `---\n` for YAML; Writer-Visual and Writer-Text-2 start with `####`

**Prompt to Writer-Visual — copy EXACTLY, filling in variables:**

```
You are a technical paper analyst writing the visual-heavy sections of a structured analysis. Write in Chinese (中文).

## CRITICAL FORMAT RULES (violating these is a failure)
- Main sections: #### (h4) — e.g. `#### 方法详解 (Methodology)`
- Sub-sections: ##### (h5) — e.g. `##### 直觉版`
- Sub-sub-sections: ###### (h6)
- Do NOT add any title/header like "Part" or "深度分析"
- Do NOT add horizontal rules (---) at the start or between sections
- Start your file directly with `#### 方法详解`

## Inputs
- Structured notes: {RUN_DIR}/notes.md (READ THIS FIRST)
- Full text for grep: {RUN_DIR}/text.txt
- PDF for Table verification: {PDF_PATH} (ONLY read Table definition pages: {TABLE_DEF_PAGES})

## Core Figure Contexts (灵魂图文本描述)
{FIGURE_CONTEXTS_JSON}

Use these figure contexts to enrich your descriptions. Reference core figures by their Figure number.

## Your job
Write ONLY these sections to `{RUN_DIR}/part_visual.md`. Follow the format exactly.

### Section: 方法详解 (Methodology)

**字符数 GATE: ≥12,000 字符。写完后立即 `wc -c` 检查。不足则从 notes 的 HYPERPARAMETERS 和 FORMULAS 段补充。**

包含：
- **直觉版:** 引用 Figure (方法概览图)，旧→新对比。Use the figure contexts above to describe the core figures.
- **精确版:**
  - 完整数据流图 (Input→...→Output)，从 notes DATA_COMPOSITION 段取数字
  - 关键公式：从 notes FORMULAS 段复制，补充物理含义
  - 数值推演：用具体数字走一遍核心算法
  - 伪代码：Python/PyTorch 风格
  - **超参数表：** 从 notes HYPERPARAMETERS 段复制为 markdown 表格（必须包含 Appendix 的完整表）
- **设计决策 (≥3,000 字符 GATE):** 从 notes DESIGN_DECISIONS 段展开。每个决策必须包含：
  - 替代方案是什么
  - 论文是否做了对比？结果如何？（引用具体 Table/Figure 编号和数字）
  - 选择背后的核心 trade-off 是什么
  - 一句话解释 WHY 本文选择优于替代方案
  写完后 wc -c 检查设计决策段是否 ≥3,000 字符，不足则从 notes 补充更多决策。
- **易混淆点:** ≥3个 "❌错误理解 / ✅正确理解" 对

### Section: 实验与归因 (Experiments & Attribution)

- **对比表格:** ≥2张完整 markdown 表格。从 notes MAIN_RESULTS 段的完整表格转录。**包含 ALL baselines，不能只挑 top-3。** 如果 notes 有4张主表，输出4张。每张表后附 1-2 句关键发现。
  - **For tables with complex formatting:** Read the Table definition pages ({TABLE_DEF_PAGES}) from the PDF to verify table structure. Only read those specific pages, not the whole PDF.
- **归因排序:** 从 notes ABLATIONS 段按 delta 大小排序，每个组件标注具体数字。格式：
  - 组件名 (+X.X on Metric, Table N): 一句话解释为什么贡献大
- **可信度检查:** ≥3个维度（去污染、baseline公平性、未报告负面结果——从 notes 的内容找线索）

**写完后执行：**
```bash
python3 -c "
text = open('{RUN_DIR}/part_visual.md').read()
method_start = text.find('#### 方法详解')
method_end = text.find('#### 实验') if '#### 实验' in text else len(text)
method_chars = len(text[method_start:method_end]) if method_start >= 0 else 0
print(f'Methodology chars: {method_chars}')
if method_chars < 12000: print('WARNING: BELOW 12K GATE — add more hyperparameter tables and formulas')
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

**Prompt to Writer-Text-1 — copy EXACTLY, filling in variables:**

```
You are a technical paper analyst writing Part 1 (text-heavy sections) of a structured analysis. Write in Chinese (中文).

## CRITICAL FORMAT RULES (violating these is a failure)
- Main sections: #### (h4) — e.g. `#### 核心速览 (Executive Summary)`
- Sub-sections: ##### (h5) — e.g. `##### 直觉版`
- Sub-sub-sections: ###### (h6)
- Do NOT add any title/header like "Part" or "深度分析"
- Do NOT add horizontal rules (---) except inside YAML frontmatter
- Start your file with `---` (the YAML opening fence)

## Inputs
- Structured notes: {RUN_DIR}/notes.md (READ THIS FIRST)
- Full text for grep: {RUN_DIR}/text.txt

## Core Figure Contexts (灵魂图文本描述)
{FIGURE_CONTEXTS_JSON}

Use these figure contexts when referencing core figures.

## Your job
Write ONLY these sections to `{RUN_DIR}/part_text1.md`. Follow the format exactly.

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
  - "从 notes 的 DATA_COMPOSITION 段逐项转换"
  - "评测数据集也列出，标注 (eval, N subtasks)"
metrics:
  - "每个指标必须标注评测配置"
  - "格式: MetricName (format, temp=X, top-p=Y, max_tokens=Z, N=K)"
  - "从 notes 的 EVAL_CONFIG 表逐项转换"
code_url: "(从 notes META 段)"
---
```

**Frontmatter GATE — 写完后立即检查：**
1. baselines: 是否每个模型单独一行？如有分组（如 "Qwen 2.5 (7B/32B)"），必须拆开
2. datasets: 每项是否有 token 数/样本数？如缺，grep text.txt 找到并补充。评测数据集如无 token 数，标注 (eval) 即可
3. metrics: 每项是否有 eval config (temp, N, max_tokens)？如缺，grep "Table" text.txt 找到 Appendix eval table 的页码补充

### Section 2: 核心速览 (Executive Summary)

- **TL;DR:** 必须含具体量化数字（如"MATH 96.2%"），不接受"显著提升"
- **一图流:** "旧方法是X → 新方法是Y"的对比结构
- **核心机制一句话:** `[动作] + [对象] + [方式] + [效果]`

### Section 3: 动机与第一性原理 (Motivation & First Principles)

- **痛点:** 引用≥2个baseline的具体数字（从notes MAIN_RESULTS段取）
- **核心洞察:** Because→Therefore因果链≥3步，每步有论据
- **物理/直觉解释:** 一个完整类比

### Section 4: 专家批判 (Critical Review)

- **隐性成本:** ≥4个论文未明说的代价，每个必须含具体数字。从 notes TRAINING_COSTS 段 + 论文 footnotes 提取。如不足4个，grep text.txt 搜索 "day" "hour" "cost" "GPU" "node" "Lambda" "budget" "compute" "wall" "infra" 等关键词定位隐藏成本。
- **最值得复用的技术:** 1-2个可直接复用的方法，标注实现成本（改几行代码/需要集群/etc.）和预期收益
- **最大的坑:** 1-2个复现/落地的坑，标注具体数字和规避方法
- **关联技术:** ≥3个同期/经典方法对比。从 notes RELATED_WORK 段取素材。每个对比必须包含：
  - 与本文的共同点和差异
  - 具体 benchmark 数字对比（从 notes MAIN_RESULTS 段取）
  - 什么场景下该选哪个

**写完后执行隐性成本计数：**
```bash
python3 -c "
import re
text = open('{RUN_DIR}/part_text1.md').read()
cost_section = text[text.find('隐性成本'):text.find('最值得复用')] if '隐性成本' in text else ''
numbers = re.findall(r'\d+[\d,.]*\s*(?:天|day|hour|小时|GPU|node|节点|美元|\$|%|倍|x|Mtok|万|M|B|K|T)', cost_section)
print(f'Hidden costs with numbers: {len(numbers)} occurrences found')
if len(numbers) < 3: print('WARNING: BELOW 3 HIDDEN COSTS GATE')
"
```
```

**Prompt to Writer-Text-2 — copy EXACTLY, filling in variables:**

```
You are a technical paper analyst writing the transfer analysis and background sections. Write in Chinese (中文).

## CRITICAL FORMAT RULES (violating these is a failure)
- Main sections: #### (h4) — e.g. `#### 机制迁移分析 (Mechanism Transfer Analysis)`
- Sub-sections: ##### (h5) — e.g. `##### 机制解耦表格`
- Sub-sub-sections: ###### (h6)
- Do NOT add any title/header like "Part" or "深度分析"
- Do NOT add horizontal rules (---) at the start or between sections
- Start your file directly with `#### 机制迁移分析`

## Inputs
- Structured notes: {RUN_DIR}/notes.md (READ THIS FIRST — especially RELATED_WORK and DESIGN_DECISIONS sections)
- Full text for grep: {RUN_DIR}/text.txt

## Core Figure Contexts (灵魂图文本描述)
{FIGURE_CONTEXTS_JSON}

Use these figure contexts when referencing core figures.

## Your job
Write ONLY these 2 sections to `{RUN_DIR}/part_text2.md`. Follow the format exactly.

**字符数 GATE: 机制迁移分析 ≥5,000 字符。写完后立即 `wc -c` 检查。**

### Section: 机制迁移分析 (Mechanism Transfer Analysis)

##### 机制解耦表格
3-5个计算原语（不是2-4个！），四列全填（名称/本文用途/抽象描述/信息论直觉）。从 notes 的 DESIGN_DECISIONS 段提取候选原语。每个原语的"抽象描述"列必须剥离本文领域术语，用通用的计算/信息论语言重述。

##### 迁移处方
每个原语≥1个跨领域场景，四要素缺一不可：
- **目标领域+具体问题：** 不是泛泛说"NLP"，要具体到任务（如"推荐系统的多源特征配比优化"）
- **怎么接：** 具体到替换现有 pipeline 的哪个组件，输入输出是什么
- **预期收益：** 引用本文的具体提升数字作为类比依据（如"参考 OLMo 3 的 4x 吞吐提升"）
- **风险/不适用条件：** 具体说明什么情况下迁移会失败

##### 机制家族图谱
从 notes 的 RELATED_WORK 段取素材：
- **前身(Ancestors)：** ≥4个，每个标注：方法名(引用) + 与本文的继承关系 + 本文做了什么改进。优先从 notes RELATED_WORK 中的 ancestor 条目提取。
- **兄弟(Siblings)：** ≥3个同期工作，每个标注：在具体 benchmark 上的数字对比 + 核心差异。从 notes MAIN_RESULTS 和 RELATED_WORK 段交叉提取。
- **后代(Descendants)：** 从引用提取或标注"暂无"
- **创新增量：** 2-3句话，比单纯"系统集成"更具体——本文组合的独特之处是什么

### Section: 背景知识补充 (Background Context)

论文中每个被依赖的外部技术用表格输出（≥8项）：

| 外部技术 | 一句话定义 | 在本文中的角色 | 核心引用 |
|---|---|---|---|

从 notes 的 RELATED_WORK、FORMULAS、HYPERPARAMETERS 段识别所有外部依赖。如果 notes 列出的外部技术不足8个，grep text.txt 搜索常见技术名（如 "RoPE" "SwiGLU" "Flash" "vLLM" "DPO" "GRPO"）补充。

**写完后执行：**
```bash
python3 -c "
text = open('{RUN_DIR}/part_text2.md').read()
transfer_start = text.find('#### 机制迁移分析')
transfer_end = text.find('#### 背景知识') if '#### 背景知识' in text else len(text)
chars = len(text[transfer_start:transfer_end]) if transfer_start >= 0 else 0
print(f'Mechanism transfer chars: {chars}')
if chars < 5000: print('WARNING: BELOW 5K GATE — add more primitives, longer prescriptions, more ancestors/siblings')
"
```
如果 <5,000，补充更多原语或更详细的迁移处方。
```

### Step 2.4: Merge (fixed order: Text-1 + Visual + Text-2)

After all three writers complete, concatenate in the canonical order and normalize:

```bash
cat .deepaper/runs/ARXIV_ID/part_text1.md .deepaper/runs/ARXIV_ID/part_visual.md .deepaper/runs/ARXIV_ID/part_text2.md > .deepaper/runs/ARXIV_ID/merged_raw.md

python3 -c "
import re
text = open('.deepaper/runs/ARXIV_ID/merged_raw.md').read()

# Remove any 'Part A/B/C' or '深度分析' title lines
text = re.sub(r'^#+ .*(?:Part [ABC]|深度分析|部分).*\n+', '', text, flags=re.MULTILINE)

# Remove stray horizontal rules between sections (keep only inside frontmatter)
parts = text.split('---', 2)  # split at YAML fences
if len(parts) >= 3:
    yaml_block = parts[0] + '---' + parts[1] + '---'
    body = parts[2]
    body = re.sub(r'\n---\s*\n', '\n\n', body)
    text = yaml_block + body

# Normalize main section headings to #### (h4)
def normalize_heading(m):
    hashes = m.group(1)
    num_prefix = m.group(2) or ''
    title = m.group(3)
    main_keywords = ['核心速览', '动机', '方法详解', '实验与归因', '专家批判', '机制迁移', '背景知识']
    for kw in main_keywords:
        if kw in title:
            return f'#### {num_prefix}{title}'
    return m.group(0)

text = re.sub(r'^(#{1,6})\s+(\d+\.\s+)?(.*(?:核心速览|动机|方法详解|实验与归因|专家批判|机制迁移|背景知识).*)', normalize_heading, text, flags=re.MULTILINE)

# Ensure no double blank lines
text = re.sub(r'\n{3,}', '\n\n', text)

open('.deepaper/runs/ARXIV_ID/merged.md', 'w').write(text)
print(f'Merged: {len(text)} chars')
"
```

### Step 2.5: HardGates (programmatic)

Run HardGates BEFORE the Critic to catch quantitative failures cheaply:

```bash
deepaper gates ARXIV_ID
```

This outputs JSON with structure:
```json
{
  "passed": false,
  "results": {
    "H1": {"passed": true},
    "H2": {"passed": false, "coverage": 0.52, "missing": [...]},
    ...
  },
  "failed": ["H2", "H8"]
}
```

**If HardGates passed**: proceed to Critic (Step 2.6).

**If HardGates failed**: skip Critic entirely, go directly to Fixer (Step 2.7) with the failed gates.

Record `HARD_GATES_RESULT` (the full JSON) and `HARD_GATES_FAILED` (list of failed gate IDs).

### Step 2.6: SoftGates / Critic (LLM semantic check)

Only run if HardGates passed. Launch one Agent (name: `critic`):

**Prompt to Critic — copy EXACTLY:**

```
You are a quality auditor for academic paper analyses. Check a draft against 7 semantic quality gates and output a JSON verdict. You do NOT rewrite — you only diagnose.

## Input
- Draft analysis: {RUN_DIR}/merged.md
- Paper notes (ground truth for fact-checking): {RUN_DIR}/notes.md
- Core figure contexts: {RUN_DIR}/figure_contexts.json

Read all files completely.

## 7 SoftGates — check each one

### S1: Pain point baselines
In "动机与第一性原理", are there ≥2 specific baseline names with numbers (e.g., "OLMo 2 MATH 49.2%")?

### S2: Causal chain depth
In "动机与第一性原理", is there a Because→Therefore chain with ≥3 logical steps?

### S3: Ablation ordering
In "实验与归因", are ablation components ordered by contribution magnitude (largest delta first)?

### S4: Credibility
No signs of overfitting claims, cherry-picked results, or fabricated numbers. Sample 5 numbers from the draft and verify against notes.

### S5: Hidden costs ≥3 with quantification
In "专家批判 / 隐性成本", are there ≥3 distinct cost items, each with a specific number?

### S6: Cross-domain transfer analysis
In "机制迁移分析", do the transfer prescriptions cover a non-trivial cross-domain scenario (not just rephrasing the original domain)?

### S7: Family tree completeness
In "机制迁移分析 / 机制家族图谱", are there ≥4 ancestors and ≥3 siblings, each with specific details?

## Output — MANDATORY JSON format

Write your verdict to `{RUN_DIR}/critic_verdict.json` as valid JSON:

```json
{
  "verdict": "pass" or "fail",
  "passed": ["S1", "S3", ...],
  "failed": [
    {"id": "S2", "reason": "因果链只有2步，缺少从XX到YY的推导"},
    {"id": "S5", "reason": "隐藏成本只列了2个，且第2个未量化"}
  ]
}
```

CRITICAL: Output ONLY valid JSON to the file. No markdown, no extra text. The Conductor must be able to parse this.
```

**If the Critic agent fails (API error, timeout, etc.), use the inline fallback — run this script yourself as Conductor:**

```bash
python3 << 'PYEOF'
import re, json, yaml

draft = open('.deepaper/runs/ARXIV_ID/merged.md').read()
notes = open('.deepaper/runs/ARXIV_ID/notes.md').read()

passed_gates = []
failed_gates = []

# S1: Pain point baselines
motiv = draft[draft.find('动机'):draft.find('方法详解')] if '动机' in draft and '方法详解' in draft else ''
g1_nums = re.findall(r'(?:OLMo|Qwen|Llama|Gemma|DeepSeek|GPT|Marin|Apertus)[^\n]{0,40}\d+\.?\d*%', motiv)
if len(g1_nums) >= 2:
    passed_gates.append("S1")
else:
    failed_gates.append({"id": "S1", "reason": f"Only {len(g1_nums)} baseline numbers found in motivation"})

# S2: Causal chain
g2 = len(re.findall(r'Because|Therefore|因此|所以|→|导致|从而', motiv)) >= 3
if g2:
    passed_gates.append("S2")
else:
    failed_gates.append({"id": "S2", "reason": "Causal chain has fewer than 3 steps"})

# S3: Ablation ordering (simplified: check ablation section exists with numbers)
exp = draft[draft.find('实验与归因'):draft.find('专家批判')] if '实验与归因' in draft and '专家批判' in draft else ''
g3 = '归因' in exp and len(re.findall(r'[+\-]\d+\.?\d*', exp)) >= 2
if g3:
    passed_gates.append("S3")
else:
    failed_gates.append({"id": "S3", "reason": "Ablation section missing or lacks delta numbers"})

# S4: Credibility (simplified: sample check)
passed_gates.append("S4")  # Simplified inline check passes by default

# S5: Hidden costs
cost_sec = draft[draft.find('隐性成本'):draft.find('最值得复用')] if '隐性成本' in draft and '最值得复用' in draft else ''
cost_nums = re.findall(r'\d+[\d,.]*\s*(?:天|day|hour|小时|GPU|node|美元|\$|%|倍|x|M|B|K|T)', cost_sec)
if len(cost_nums) >= 3:
    passed_gates.append("S5")
else:
    failed_gates.append({"id": "S5", "reason": f"Only {len(cost_nums)} quantified costs found"})

# S6: Cross-domain transfer
transfer = draft[draft.find('迁移处方'):draft.find('机制家族')] if '迁移处方' in draft and '机制家族' in draft else ''
g6 = len(transfer) > 500
if g6:
    passed_gates.append("S6")
else:
    failed_gates.append({"id": "S6", "reason": "Transfer prescriptions too short or missing"})

# S7: Family tree
fam = draft[draft.find('前身'):draft.find('背景知识')] if '前身' in draft else ''
anc = len(re.findall(r'^\s*\d+\.?\s+\*\*', fam, re.MULTILINE))
sib_sec = fam[fam.find('兄弟'):] if '兄弟' in fam else ''
sibs = len(re.findall(r'^\s*\d+\.?\s+\*\*', sib_sec, re.MULTILINE))
if anc >= 4 and sibs >= 3:
    passed_gates.append("S7")
else:
    failed_gates.append({"id": "S7", "reason": f"Ancestors={anc} (need 4), Siblings={sibs} (need 3)"})

verdict = "pass" if not failed_gates else "fail"
result = {"verdict": verdict, "passed": passed_gates, "failed": failed_gates}
with open('.deepaper/runs/ARXIV_ID/critic_verdict.json', 'w') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(json.dumps(result, ensure_ascii=False, indent=2))
PYEOF
```

Read the verdict. Record `SOFT_GATES_RESULT` and `SOFT_GATES_FAILED`.

**If verdict is "pass"**: go to Step 3 (Save).

**If verdict is "fail"**: go to Step 2.7 (Fixer).

### Step 2.7: Fixer (max 2 rounds, select best version)

Combine all failed gates (HardGates + SoftGates) into a single failure list.

**Before each Fixer round**, save a copy of the current version:
```bash
cp .deepaper/runs/ARXIV_ID/merged.md .deepaper/runs/ARXIV_ID/merged_v{N}.md
```

**Special handling for H8 failures (number fingerprint):** If H8 failed, identify the suspect Table definition pages from the gates output and read those specific PDF pages to give to the Fixer:
```bash
# Only if H8 failed — read suspect Table pages from PDF
# The gates output includes suspect_tables. Find their definition pages from the registry.
python3 -c "
from deepaper.pipeline_io import safe_read_json
reg = safe_read_json('.deepaper/runs/ARXIV_ID/visual_registry.json', {})
# Replace SUSPECT_TABLE_KEYS with the actual keys from gates output
suspect_keys = {SUSPECT_TABLE_KEYS}
for key in suspect_keys:
    if key in reg and reg[key].get('definition_page'):
        print(f'{key}: definition page {reg[key][\"definition_page\"]}')
"
```
Then read those specific PDF pages and include the content in the Fixer prompt.

Launch one Agent (subagent_type: `executor`, name: `fixer`):

```
## 修复任务
以下质量门控未通过，请仅修复这些问题，不要改动已通过的部分。

### 失败清单
{ALL_FAILED_GATES_JSON — include both HardGates and SoftGates failures with their details}

### 当前全文
Read: {RUN_DIR}/merged.md

### 参考数据
- Extractor notes: {RUN_DIR}/notes.md
- Full text: {RUN_DIR}/text.txt
{IF H8 FAILED: - Suspect Table PDF pages: [include the PDF page content you read above]}

### 规则
- 只修改与失败门控相关的 section
- 不要删除或缩减已有内容
- 所有新增数字必须来自 Extractor 笔记或论文原文
- 输出完整的修改后全文到 {RUN_DIR}/merged.md

### FORMAT RULES
- Main sections: #### (h4)
- Sub-sections: ##### (h5)
- Do NOT add "Part" titles or --- horizontal rules in body
```

After Fixer completes, **re-run all gates** (both HardGates and SoftGates):
```bash
deepaper gates ARXIV_ID
```
Then re-run Critic if HardGates pass (same prompt as Step 2.6).

**If all gates pass**: go to Step 3.

**If still failing and round < 2**: run another Fixer round.

**If still failing after 2 rounds**: select the best version (the one that passed the most gates total):

```bash
python3 -c "
# Compare gate results across versions and pick the best
# The best version is the one with the fewest total failures (H+S combined)
best_version = 'merged.md'  # default to latest
# If version 1 had fewer failures, use it instead
# Copy best version to merged.md
print(f'Selected best version: {best_version}')
"
```

Then proceed to Step 3 with **degraded quality**.

## Step 3: Save

Determine quality status and prepare the save:

```bash
# Inject quality metadata into the YAML frontmatter before saving
python3 -c "
import re

merged = open('.deepaper/runs/ARXIV_ID/merged.md').read()

# Determine quality and failed gates
quality = 'QUALITY'  # 'full' or 'partial'
failed_gates = FAILED_GATES_LIST  # [] or ['H2', 'S5', ...]

# Inject into YAML frontmatter
if merged.startswith('---'):
    end = merged.find('---', 3)
    if end > 0:
        yaml_block = merged[3:end]
        body = merged[end+3:]
        yaml_block = yaml_block.rstrip() + f'''
quality: {quality}
failed_gates: {failed_gates}
pipeline_version: 2
'''
        merged = '---' + yaml_block + '---' + body
        open('.deepaper/runs/ARXIV_ID/merged.md', 'w').write(merged)
        print(f'Injected quality={quality}, failed_gates={failed_gates}, pipeline_version=2')
"
```

Then save:
```bash
deepaper save ARXIV_ID --category CATEGORY --input .deepaper/runs/ARXIV_ID/merged.md
```

Category choices:
- `llm/pretraining` `llm/alignment` `llm/reasoning` `llm/efficiency` `llm/agent`
- `recsys/matching` `recsys/ranking` `recsys/llm-as-rec` `recsys/generative-rec` `recsys/system`
- `multimodal/vlm` `multimodal/generation` `multimodal/understanding`
- `misc`

### Step 3.1: Pipeline Report

Write a pipeline report summarizing the run:

```bash
python3 -c "
import json
from deepaper.pipeline_io import safe_write_json, safe_read_json

run_dir = '.deepaper/runs/ARXIV_ID'
report = {
    'arxiv_id': 'ARXIV_ID',
    'paper_profile': safe_read_json(f'{run_dir}/paper_profile.json', {}),
    'core_figures': safe_read_json(f'{run_dir}/core_figures.json', []),
    'extractor': {
        'notes_chars': len(open(f'{run_dir}/notes.md').read()) if __import__('os').path.exists(f'{run_dir}/notes.md') else 0,
        'struct_check_passed': STRUCT_CHECK_PASSED,  # True/False
        'audit_passed': AUDIT_PASSED,  # True/False
        'retry_count': RETRY_COUNT,  # 0 or 1
    },
    'writers': {
        'visual': {'sections': ['方法详解', '实验与归因']},
        'text_1': {'sections': ['YAML', '核心速览', '动机与第一性原理', '专家批判']},
        'text_2': {'sections': ['机制迁移分析', '背景知识补充']},
    },
    'hard_gates': HARD_GATES_RESULT,
    'soft_gates': SOFT_GATES_RESULT,
    'fixer': {
        'rounds': FIXER_ROUNDS,  # 0, 1, or 2
        'best_version': BEST_VERSION,  # 'merged.md', 'merged_v1.md', etc.
    },
    'quality': 'QUALITY',  # 'full' or 'partial'
    'failed_gates': FINAL_FAILED_GATES,  # []
}
safe_write_json(f'{run_dir}/report.json', report)
print(json.dumps({'report_saved': f'{run_dir}/report.json', 'quality': report['quality']}, indent=2))
"
```

## Step 4: Citations (optional)

```bash
deepaper cite ARXIV_ID --update
```

## Reference: Section Template (for Writer agents)

Each section heading uses `####` (h4). The full analysis structure in merge order is:

```
---
(YAML frontmatter — Writer-Text-1)
---
#### 核心速览 (Executive Summary)          — Writer-Text-1
#### 动机与第一性原理 (Motivation)           — Writer-Text-1
#### 方法详解 (Methodology)                 — Writer-Visual
#### 实验与归因 (Experiments & Attribution)  — Writer-Visual
#### 专家批判 (Critical Review)              — Writer-Text-1
#### 机制迁移分析 (Mechanism Transfer)       — Writer-Text-2
#### 背景知识补充 (Background Context)       — Writer-Text-2
```

## Reference: Pipeline File Layout

```
.deepaper/runs/{ARXIV_ID}/
  ├── text.txt                 # Full text (page-delimited)
  ├── text_by_page.json        # Per-page text for programmatic analysis
  ├── visual_registry.json     # Table/Figure registry
  ├── paper_profile.json       # Structural profile (pages, sections, counts)
  ├── core_figures.json        # Identified core figures
  ├── figure_contexts.json     # Core figure captions + reference paragraphs
  ├── notes.md                 # Extractor output
  ├── part_visual.md           # Writer-Visual output
  ├── part_text1.md            # Writer-Text-1 output
  ├── part_text2.md            # Writer-Text-2 output
  ├── merged.md                # Final merged analysis
  ├── critic_verdict.json      # Critic output (SoftGates)
  └── report.json              # Pipeline execution report
```
