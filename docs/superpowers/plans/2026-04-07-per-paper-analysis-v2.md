# Per-Paper Analysis v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor deepaper's per-paper analysis format from 7 verbose sections (~34K chars) to 4 structured-form sections (~10K chars, ~10 min reading), with frontmatter designed for future cross-paper wiki operations.

**Architecture:** Single atomic refactor of the schema + template + pipeline + gates. The foundation change is `output_schema.SECTIONS` (4 sections) and `DEFAULT_TEMPLATE` (new template text). Pipeline (prompt_builder, gates, cli.merge) adapts to the new schema. Tests updated in lockstep with each change.

**Tech Stack:** Python 3.11+, pytest, typer, pyyaml, ruff

**Spec:** `docs/superpowers/specs/2026-04-07-per-paper-analysis-v2-design.md`

---

## File Structure

### Files to modify

| File | Responsibility | Changes |
|------|---------------|---------|
| `src/deepaper/defaults.py` | Source of truth for `DEFAULT_TEMPLATE` (inline Python string) | Rewrite template to 4-section format with new frontmatter schema |
| `src/deepaper/output_schema.py` | Section specs, char floors, frontmatter fields | Update `SECTIONS` (4 entries), update `FRONTMATTER_FIELDS`, remove `CHAR_FLOORS` concept |
| `src/deepaper/content_checklist.py` | H9 content markers per section | Rewrite `CONTENT_MARKERS` for 4 new sections with structural markers (tables, flowchart, causal chain with `[C1]` prefix) |
| `src/deepaper/prompt_builder.py` | Writer task split, prompt assembly, constraints injection | Update `auto_split` (3 writers), delete `compute_scaling_factor`, rewrite `gates_to_constraints` (form preferences instead of char targets) |
| `src/deepaper/gates.py` | Quality gate checks H1-H10 | Change `check_char_floors` → `check_sections_exist`, update `check_baselines_format` to use new frontmatter fields |
| `src/deepaper/cli.py` | CLI commands (merge/gates/save) | Fix merge to hoist YAML frontmatter from anywhere in concatenated parts; fix double `####` bug |
| `src/deepaper/registry.py` | `build_coverage_checklist` builder | Filter noisy subsection headings (exclude table row labels matched by current regex) |
| `templates/default.md` | Dev-convenience mirror of `DEFAULT_TEMPLATE` | Sync with defaults.py after changes |

### Tests to modify

| File | Changes |
|------|---------|
| `tests/test_prompt_builder.py` | Update `TestParseTemplateSections`, `TestAutoSplit`, `TestGatesToConstraints` for 4 sections / 3 writers / form preferences |
| `tests/test_content_checklist.py` | Update marker assertions for 4 new sections |
| `tests/test_gates.py` | Update H3 tests (section existence), H1 frontmatter fields, remove CHAR_FLOORS references |
| `tests/test_cli.py` | Add test for frontmatter hoisting in merge; add test for double `####` collapse |
| `tests/test_registry.py` | Add test for subsection heading noise filter |

---

## Phase 1: Schema & Template Foundation

### Task 1: Rewrite DEFAULT_TEMPLATE in defaults.py to 4-section format

**Files:**
- Modify: `src/deepaper/defaults.py:27-200` (the `DEFAULT_TEMPLATE` string constant)
- Modify: `tests/test_prompt_builder.py:4-37` (`TestParseTemplateSections`, `TestExtractSystemRole`)

- [ ] **Step 1: Update the failing test for new 4-section structure**

Replace `TestParseTemplateSections` class in `tests/test_prompt_builder.py`:

```python
class TestParseTemplateSections:
    def test_extracts_all_four_sections(self):
        from deepaper.prompt_builder import parse_template_sections
        from deepaper.defaults import DEFAULT_TEMPLATE

        sections = parse_template_sections(DEFAULT_TEMPLATE)
        expected_keys = [
            "核心速览",
            "第一性原理分析",
            "技术精要",
            "机制迁移",
        ]
        assert set(sections.keys()) == set(expected_keys)
        for key in expected_keys:
            assert len(sections[key]) > 100, f"Section {key} too short: {len(sections[key])}"

    def test_sections_contain_key_markers(self):
        from deepaper.prompt_builder import parse_template_sections
        from deepaper.defaults import DEFAULT_TEMPLATE

        sections = parse_template_sections(DEFAULT_TEMPLATE)
        # 核心速览: TL;DR + 核心机制一句话 + 关键数字表
        assert "TL;DR" in sections["核心速览"]
        assert "核心机制" in sections["核心速览"]
        assert "关键数字" in sections["核心速览"]
        # 第一性原理分析: 痛点 + 因果链 with [C1] prefix
        assert "痛点" in sections["第一性原理分析"]
        assert "[C1]" in sections["第一性原理分析"]
        assert "Because" in sections["第一性原理分析"]
        # 技术精要: method flow + formula table + design decisions + ablation + confusions + hidden costs
        assert "方法流程" in sections["技术精要"]
        assert "设计决策" in sections["技术精要"]
        assert "消融排序" in sections["技术精要"]
        assert "易混淆点" in sections["技术精要"]
        assert "隐性成本" in sections["技术精要"]
        # 机制迁移: decomposition table + lineage (Ancestors)
        assert "机制解耦" in sections["机制迁移"]
        assert "前身" in sections["机制迁移"] or "Ancestors" in sections["机制迁移"]
```

Also update `TestExtractFrontmatterSpec`:

```python
class TestExtractFrontmatterSpec:
    def test_extracts_frontmatter_section(self):
        from deepaper.prompt_builder import extract_frontmatter_spec
        from deepaper.defaults import DEFAULT_TEMPLATE

        spec = extract_frontmatter_spec(DEFAULT_TEMPLATE)
        # Required new fields
        assert "tldr" in spec
        assert "baselines" in spec
        assert "tags" in spec
        assert "mechanisms" in spec
        assert "key_tradeoffs" in spec
        assert "key_numbers" in spec
        # Removed fields should NOT be present
        assert "datasets" not in spec
        assert "metrics" not in spec
        assert "keywords" not in spec
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_prompt_builder.py::TestParseTemplateSections tests/test_prompt_builder.py::TestExtractFrontmatterSpec -v`

Expected: FAIL (the template still uses 7 sections and old frontmatter fields)

- [ ] **Step 3: Rewrite DEFAULT_TEMPLATE in src/deepaper/defaults.py**

Replace the `DEFAULT_TEMPLATE = """\` block (lines 27 through the end-of-template marker) with this new content:

```python
DEFAULT_TEMPLATE = """\
# 论文深度剖析 (v2)

Role: 你是一位拥有深厚数学功底的LLM/推荐系统领域资深算法专家，同时也是一位擅长用费曼技巧（Feynman Technique）进行教学的导师。请对提供的论文进行深度剖析，目标是让读者在 ~10 分钟内获取最高密度的判断力增益。

---

## 输出格式

请直接输出一个完整的 Markdown 文档，包含 **YAML frontmatter** 和 **正文** 两部分。不要输出 JSON，不要用代码块包裹整个输出。

### YAML Frontmatter

在文档开头用 `---` 包裹的 YAML 块，承担「索引层」角色（支持跨论文程序化检索）：

```
---
title: "论文标题"
arxiv_id: "2512.13961"
date: "2025-12-15"
url: "https://arxiv.org/abs/..."
category: "llm/pretraining"
tldr: "一句话总结（≤100字，必须含 ≥2 个量化数字）"
baselines:
  - "主要对比的 baseline 模型名"
tags:
  - pretraining
  - data-engineering
mechanisms:
  - name: 机制名称
    scope: 使用范围（如 pretraining → midtraining）
    ancestor: 前身方法名
key_tradeoffs:
  - decision: 非 trivial 的设计决策
    chosen_over: 备选方案
    reason: 选择理由
key_numbers:
  - metric: 指标名
    value: 数值
    unit: 单位（可选）
    baseline: 对比基线
    baseline_value: 基线值
---
```

**字段规则：**
- `baselines` 至少 2 个，从论文实验部分提取
- `tldr` 必须含 ≥2 个具体量化数字（如 "MATH 96.2%"）
- `tags` 多标签支持多维度检索
- `mechanisms`、`key_tradeoffs`、`key_numbers` 是机器可读的结构化结论，每项尽量一行

### 正文（Markdown）

正文由以下 4 个章节组成，每个章节用 `#### 标题` 开头（h4）。**核心原则：默认使用结构化形式（表格/流程图/列表），散文仅用于补充推理语境。禁止生成伪代码。禁止用散文做表格能做的事。**

---

**#### 核心速览**

职责：30 秒内判断论文值不值得深入读。

- **TL;DR (≤100字):** 一句话讲清：它用什么新方法、解决什么旧问题、达到什么效果（含 ≥2 个量化数字）
- **核心机制一句话:** `[动作] + [对象] + [方式] + [效果]` 格式，剥离领域上下文
- **关键数字表** (≤7 行，标准化列名)：

  | 指标 | 数值 | 基线 | 基线值 | 增益 |
  |------|------|------|--------|------|

---

**#### 第一性原理分析**

职责：理解作者为什么做这个选择，建立因果直觉。

- **痛点 (The Gap):** 之前 SOTA 方法（提及具体相关 baseline）死在哪里？短散文 ≤5 句
- **因果链 (≤3 条):** 使用固定编号格式 `[C1]`, `[C2]`, `[C3]`，每条格式：

  ```
  [C1] Because {前提} → Therefore {结论}
       — {可选：≤1 句比喻或语境补充}
  ```

  编号 `[C1]` 等支持未来跨论文引用。不要把比喻展开成独立段落。

---

**#### 技术精要**

职责：掌握核心方法、关键结论、工程陷阱。**用结构化形式表达，禁止生成伪代码，禁止用散文复述数字对比。**

##### 方法流程

单个流程图（≤10 步），格式 `Input → Step A → Step B → ... → Output`。仅列主干，不展开 tensor shape 推导。

##### 核心公式与符号

- 列出 1-2 个核心公式（LaTeX）
- 符号表（标准化列名）：

  | 符号 | 含义 | 关键值 |
  |------|------|--------|

##### 设计决策

每条一行的表格（≤ 5 条）：

| 决策 | 备选方案 | 选择理由 | 证据来源 |
|------|---------|---------|---------|

不要展开散文描述每个决策。

##### 消融排序

按贡献降序的表格（≤ 6 行）：

| 排名 | 组件 | 增益 | 数据来源 |
|------|------|------|---------|

表格末尾可附 1-2 句可信度判断（如 "单次运行、无多种子方差；结论方向可信度中等"），不单独成段。

##### 易混淆点

≤ 3 对，每对 2 行：

- ❌ 错误理解：...
- ✅ 正确理解：...

##### 隐性成本

论文没明说的代价表格（≤ 5 行）：

| 成本项 | 量化数据 | 对决策的影响 |
|-------|---------|-------------|

---

**#### 机制迁移**

职责：提取可跨论文/跨领域复用的抽象模式。

##### 机制解耦

将方法拆解为 2-4 个独立的计算原语（标准化列名）：

| 原语名称 | 本文用途 | 抽象描述 | 信息论/几何直觉 |
|---------|---------|---------|----------------|

##### 机制谱系

- **前身 (Ancestors, ≥3):** 方法名 + 一句差异
- **兄弟 (Siblings, 可选):** 同期独立工作 + 一句差异
- **创新增量:** 本文相对前身谱系的核心增量是什么（1-2 句）

不要包含「迁移处方」或「后代」（推测性内容）。

---

## 格式规则（硬约束）

- 主标题 `####` (h4)，子标题 `#####` (h5)，禁止 h1/h2/h3
- **禁止生成伪代码块**（代码块 ```python``` 等不允许）
- **数字对比必须用表格**，禁止散文内嵌 "A 的 X 是 5.2，B 的 X 是 4.8" 这种对比
- **比喻 ≤ 1 句**，嵌入因果链内，不独立成段
- 对比/排序/成本/符号 必须用表格
- 设计决策的理由可用短散文补充（1-3 句），但不鼓励展开为段落

## 注意事项

- 忠实地从论文中提取信息，不要推测或编造
- YAML frontmatter 中的字符串值如包含冒号或特殊字符，请用引号包裹
- 直接输出最终 Markdown，不要用代码块包裹
"""
```

Note: The above template contains triple-backtick blocks inside a Python triple-double-quoted string, which is valid Python. Save as-is.

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_prompt_builder.py::TestParseTemplateSections tests/test_prompt_builder.py::TestExtractFrontmatterSpec -v`

Expected: PASS (all assertions match new 4-section structure)

- [ ] **Step 5: Commit**

```bash
git add src/deepaper/defaults.py tests/test_prompt_builder.py
git commit -m "refactor(template): rewrite DEFAULT_TEMPLATE to 4-section structured format

- Core sections reduced from 7 to 4: 核心速览 / 第一性原理分析 / 技术精要 / 机制迁移
- Frontmatter gains structured fields: tags, mechanisms, key_tradeoffs, key_numbers
- Frontmatter drops low-value fields: datasets, metrics, keywords, core_contribution
- Emphasize table/flowchart over prose; forbid pseudocode
- Causal chains use fixed [C1][C2] format for future cross-paper referencing"
```

---

### Task 2: Update output_schema.SECTIONS and FRONTMATTER_FIELDS

**Files:**
- Modify: `src/deepaper/output_schema.py:32-95` (FRONTMATTER_FIELDS, SECTIONS)

- [ ] **Step 1: Update FRONTMATTER_FIELDS in output_schema.py**

Replace the `FRONTMATTER_FIELDS` dict (around line 32-42) with:

```python
FRONTMATTER_FIELDS: dict[str, FieldSpec] = {
    "title": FieldSpec(type="str"),
    "arxiv_id": FieldSpec(type="str"),
    "date": FieldSpec(type="str_or_null"),
    "url": FieldSpec(type="str_or_null"),
    "category": FieldSpec(type="str"),
    "tldr": FieldSpec(type="str", min_numbers=2),
    "baselines": FieldSpec(type="list", min_items=2),
    "tags": FieldSpec(type="list", min_items=1),
    "mechanisms": FieldSpec(type="list", min_items=1),
    "key_tradeoffs": FieldSpec(type="list", min_items=1),
    "key_numbers": FieldSpec(type="list", min_items=1),
}
```

- [ ] **Step 2: Update SECTIONS in output_schema.py**

Replace the `SECTIONS` list (around line 59-95) with:

```python
SECTIONS: list[SectionSpec] = [
    SectionSpec(
        name="核心速览",
        min_chars=0,  # char floor no longer enforced; H3 now checks existence only
        content_markers=["tldr_with_numbers", "mechanism_one_line", "key_numbers_table"],
    ),
    SectionSpec(
        name="第一性原理分析",
        min_chars=0,
        content_markers=["numbered_causal_chain"],
    ),
    SectionSpec(
        name="技术精要",
        min_chars=0,
        content_markers=[
            "method_flowchart",
            "design_decisions_table",
            "ablation_ranking_table",
            "confusion_pairs",
            "hidden_costs_table",
        ],
    ),
    SectionSpec(
        name="机制迁移",
        min_chars=0,
        content_markers=["mechanism_table", "ancestors"],
    ),
]
```

- [ ] **Step 3: Run output_schema import smoke test**

Run: `python -c "from deepaper.output_schema import SECTIONS, FRONTMATTER_FIELDS, SECTION_ORDER, CHAR_FLOORS; print(SECTION_ORDER); print(list(FRONTMATTER_FIELDS.keys()))"`

Expected output:
```
['核心速览', '第一性原理分析', '技术精要', '机制迁移']
['title', 'arxiv_id', 'date', 'url', 'category', 'tldr', 'baselines', 'tags', 'mechanisms', 'key_tradeoffs', 'key_numbers']
```

- [ ] **Step 4: Commit**

```bash
git add src/deepaper/output_schema.py
git commit -m "refactor(schema): update SECTIONS and FRONTMATTER_FIELDS for v2 format

- SECTIONS reduced to 4: 核心速览 / 第一性原理分析 / 技术精要 / 机制迁移
- min_chars=0 for all (char floor enforcement moved to form-based gates)
- FRONTMATTER_FIELDS adds: tags, mechanisms, key_tradeoffs, key_numbers
- FRONTMATTER_FIELDS removes: datasets, metrics, keywords, core_contribution, venue, publication_type, doi, code_url"
```

---

### Task 3: Update content_checklist.CONTENT_MARKERS for 4 sections

**Files:**
- Modify: `src/deepaper/content_checklist.py:6-32` (CONTENT_MARKERS dict)
- Modify: `tests/test_content_checklist.py` (update section name assertions)

- [ ] **Step 1: Update the failing test**

Read the existing `tests/test_content_checklist.py` and replace its section references. Add this test class at the end:

```python
class TestV2ContentMarkers:
    """Test that CONTENT_MARKERS covers the new 4-section structure."""

    def test_markers_exist_for_all_four_sections(self):
        from deepaper.content_checklist import CONTENT_MARKERS
        expected_sections = ["核心速览", "第一性原理分析", "技术精要", "机制迁移"]
        for sec in expected_sections:
            assert sec in CONTENT_MARKERS, f"Missing section: {sec}"
            assert len(CONTENT_MARKERS[sec]) >= 1

    def test_v2_markers_catch_table_requirements(self):
        from deepaper.content_checklist import check_content_markers
        # Good md: has all required structural markers
        md = (
            "#### 核心速览\n"
            "TL;DR: MATH 96.2%, AIME 80.6%.\n"
            "[动作] + [对象] + [方式] + [效果]\n"
            "| 指标 | 数值 | 基线 | 基线值 | 增益 |\n"
            "|------|------|------|--------|------|\n"
            "| MATH | 96.2 | Qwen | 95.4 | +0.8 |\n"
            "\n"
            "#### 第一性原理分析\n"
            "痛点：基线死在数据质量。\n"
            "[C1] Because A → Therefore B — 比喻：像厨房备料\n"
            "\n"
            "#### 技术精要\n"
            "##### 方法流程\n"
            "Input → Step A → Step B → Step C → Output\n"
            "##### 设计决策\n"
            "| 决策 | 备选方案 | 选择理由 | 证据来源 |\n"
            "|------|---------|---------|---------|\n"
            "| X | Y | Z | W |\n"
            "##### 消融排序\n"
            "| 排名 | 组件 | 增益 | 数据来源 |\n"
            "|------|------|------|---------|\n"
            "| 1 | A | +3.0 | Table 1 |\n"
            "##### 易混淆点\n"
            "❌ 错误 ✅ 正确\n"
            "##### 隐性成本\n"
            "| 成本项 | 量化数据 | 对决策的影响 |\n"
            "|-------|---------|-------------|\n"
            "| X | 5 days | delayed |\n"
            "\n"
            "#### 机制迁移\n"
            "| 原语名称 | 本文用途 | 抽象描述 | 信息论/几何直觉 |\n"
            "|---------|---------|---------|----------------|\n"
            "| A | X | Y | Z |\n"
            "前身 (Ancestors): A, B, C\n"
        )
        result = check_content_markers(md)
        assert result["passed"] is True, f"Failed: missing={result['missing']}"

    def test_v2_markers_reject_prose_only(self):
        from deepaper.content_checklist import check_content_markers
        # Bad md: prose only, no tables, no causal chain, no flowchart
        md = (
            "#### 核心速览\nJust some prose without structure.\n"
            "#### 第一性原理分析\nPain points described in sentences.\n"
            "#### 技术精要\nMethodology explained in paragraphs.\n"
            "#### 机制迁移\nRelated work listed as text.\n"
        )
        result = check_content_markers(md)
        assert result["passed"] is False
```

- [ ] **Step 2: Run failing tests**

Run: `pytest tests/test_content_checklist.py::TestV2ContentMarkers -v`

Expected: FAIL (CONTENT_MARKERS still references old 7 sections)

- [ ] **Step 3: Rewrite CONTENT_MARKERS in src/deepaper/content_checklist.py**

Replace the `CONTENT_MARKERS` dict (lines 6-32) with:

```python
CONTENT_MARKERS: dict[str, list[dict]] = {
    "核心速览": [
        # TL;DR must contain at least one number
        {"marker": "tldr_with_numbers", "check": "contains_pattern",
         "pattern": r"TL;DR.*?\d+(?:\.\d+)?"},
        # Mechanism one-liner with [动作] + [对象] format
        {"marker": "mechanism_one_line", "check": "contains_pattern",
         "pattern": r"\[.+?\].*?\+.*?\[.+?\]"},
        # Key numbers table header (standardized columns)
        {"marker": "key_numbers_table", "check": "contains_pattern",
         "pattern": r"\|\s*指标\s*\|\s*数值\s*\|\s*基线\s*\|\s*基线值\s*\|\s*增益\s*\|"},
    ],
    "第一性原理分析": [
        # Numbered causal chain with [C1] prefix + Because/Therefore
        {"marker": "numbered_causal_chain", "check": "contains_pattern",
         "pattern": r"\[C\d+\].*?(?:Because|因为).*?(?:→|Therefore|所以|因此)"},
    ],
    "技术精要": [
        # Flowchart: at least 3 arrow steps
        {"marker": "method_flowchart", "check": "contains_pattern",
         "pattern": r"(?:→.*?){3,}"},
        # Design decisions table header
        {"marker": "design_decisions_table", "check": "contains_pattern",
         "pattern": r"\|\s*决策\s*\|\s*备选方案\s*\|\s*选择理由\s*\|\s*证据来源\s*\|"},
        # Ablation ranking table header
        {"marker": "ablation_ranking_table", "check": "contains_pattern",
         "pattern": r"\|\s*排名\s*\|\s*组件\s*\|\s*增益\s*\|\s*数据来源\s*\|"},
        # Confusion pairs: ❌ and ✅
        {"marker": "confusion_pairs", "check": "contains_pattern",
         "pattern": r"❌.*?✅|✅.*?❌"},
        # Hidden costs table header
        {"marker": "hidden_costs_table", "check": "contains_pattern",
         "pattern": r"\|\s*成本项\s*\|\s*量化数据\s*\|\s*对决策的影响\s*\|"},
    ],
    "机制迁移": [
        # Mechanism decomposition table header
        {"marker": "mechanism_table", "check": "contains_pattern",
         "pattern": r"\|\s*原语名称\s*\|\s*本文用途\s*\|\s*抽象描述\s*\|"},
        # Ancestors list
        {"marker": "ancestors", "check": "contains_pattern",
         "pattern": r"(?:前身|Ancestors)"},
    ],
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_content_checklist.py -v`

Expected: PASS (both positive and negative cases work)

- [ ] **Step 5: Commit**

```bash
git add src/deepaper/content_checklist.py tests/test_content_checklist.py
git commit -m "refactor(content_checklist): update CONTENT_MARKERS for v2 4-section format

- New markers detect standardized table headers (key_numbers, design_decisions, ablation, hidden_costs, mechanism)
- Causal chain marker now requires [C1] prefix for future cross-paper referencing
- Flowchart marker requires ≥3 arrow steps (Input → A → B → C → Output)
- Pseudocode marker removed (pseudocode is forbidden in v2)"
```

---

## Phase 2: Pipeline Logic Updates

### Task 4: Update prompt_builder.auto_split for 3 writers

**Files:**
- Modify: `src/deepaper/prompt_builder.py:312-364` (auto_split function, VISUAL_SECTIONS, _VISUAL_SLUGS)
- Modify: `tests/test_prompt_builder.py:63-130` (TestAutoSplit)

- [ ] **Step 1: Update failing tests**

Replace `TestAutoSplit` in `tests/test_prompt_builder.py` with:

```python
class TestAutoSplit:
    def _profile(self, pages=10, tables=3, figures=4, equations=2):
        return {
            "total_pages": pages,
            "num_tables": tables,
            "num_figures": figures,
            "num_equations": equations,
        }

    def test_produces_exactly_three_writers(self):
        from deepaper.prompt_builder import auto_split
        tasks = auto_split(self._profile())
        assert len(tasks) == 3
        names = [t.name for t in tasks]
        assert names == ["writer-overview", "writer-principle", "writer-technical"]

    def test_overview_writer_owns_speed_and_transfer(self):
        from deepaper.prompt_builder import auto_split
        tasks = auto_split(self._profile())
        overview = next(t for t in tasks if t.name == "writer-overview")
        assert overview.sections == ["核心速览", "机制迁移"]

    def test_principle_writer_owns_first_principles(self):
        from deepaper.prompt_builder import auto_split
        tasks = auto_split(self._profile())
        principle = next(t for t in tasks if t.name == "writer-principle")
        assert principle.sections == ["第一性原理分析"]

    def test_technical_writer_owns_consolidated_technical(self):
        from deepaper.prompt_builder import auto_split
        tasks = auto_split(self._profile())
        technical = next(t for t in tasks if t.name == "writer-technical")
        assert technical.sections == ["技术精要"]
        assert technical.needs_pdf_pages is True  # tables may need verification

    def test_long_paper_same_three_writers(self):
        """Long papers do not add more writers (content grows via tables, not prose)."""
        from deepaper.prompt_builder import auto_split
        tasks = auto_split(self._profile(pages=120, tables=50, figures=30))
        assert len(tasks) == 3
```

- [ ] **Step 2: Run failing tests**

Run: `pytest tests/test_prompt_builder.py::TestAutoSplit -v`

Expected: FAIL (auto_split still produces 4 tasks with old writer names)

- [ ] **Step 3: Rewrite auto_split and related constants in prompt_builder.py**

Replace lines 19-27 of `src/deepaper/prompt_builder.py`:

```python
# Sections that may benefit from PDF table pages for verification
VISUAL_SECTIONS = ["技术精要"]

# Writer task definitions for the v2 4-section layout
WRITER_ASSIGNMENTS: list[tuple[str, list[str], bool]] = [
    # (writer_name, sections, needs_pdf_pages)
    ("writer-overview", ["核心速览", "机制迁移"], False),
    ("writer-principle", ["第一性原理分析"], False),
    ("writer-technical", ["技术精要"], True),
]
```

Then replace the entire `auto_split` function (lines ~312-364) with:

```python
def auto_split(profile: dict) -> list[WriterTask]:
    """Split sections across 3 Writers with a fixed assignment.

    In v2 we use a fixed 3-writer layout regardless of paper length:
    - writer-overview: 核心速览 + 机制迁移 (both need global view)
    - writer-principle: 第一性原理分析 (independent causal reasoning)
    - writer-technical: 技术精要 (method + experiment + critique merged)

    Long papers grow tables (not prose), so 3 writers is enough for any
    paper length. The ``profile`` arg is retained for interface stability.
    """
    _ = profile  # interface compatibility; length no longer affects split
    tasks: list[WriterTask] = []
    for name, sections, needs_pdf in WRITER_ASSIGNMENTS:
        tasks.append(WriterTask(
            name=name,
            sections=sections,
            needs_pdf_pages=needs_pdf,
        ))
    return tasks
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_prompt_builder.py::TestAutoSplit -v`

Expected: PASS (all 5 tests pass with 3-writer fixed layout)

- [ ] **Step 5: Commit**

```bash
git add src/deepaper/prompt_builder.py tests/test_prompt_builder.py
git commit -m "refactor(prompt_builder): fixed 3-writer layout (overview/principle/technical)

Paper length no longer affects writer split — long papers grow tables not
prose, so 3 writers handles any length. Simplifies parallel dispatch and
eliminates the text-writer load balancing logic."
```

---

### Task 5: Delete compute_scaling_factor and rewrite gates_to_constraints for form preferences

**Files:**
- Modify: `src/deepaper/prompt_builder.py:96-216` (compute_scaling_factor, gates_to_constraints, _section_content_markers)

- [ ] **Step 1: Add failing test for form preference injection**

Add to `tests/test_prompt_builder.py` (at the bottom):

```python
class TestGatesToConstraintsV2:
    def _profile(self):
        return {"total_pages": 30, "num_tables": 10, "num_figures": 5, "num_equations": 3}

    def test_no_char_target_section(self):
        from deepaper.prompt_builder import gates_to_constraints
        text = gates_to_constraints(
            sections=["技术精要"],
            profile=self._profile(),
            registry={},
            core_figures=[],
        )
        # No "建议目标" section (removed in v2)
        assert "建议目标" not in text
        # No "~X,XXX 字符" suggestions
        assert "字符" not in text or "字符（H3）" in text  # only floor-based lines, no targets

    def test_form_preferences_present(self):
        from deepaper.prompt_builder import gates_to_constraints
        text = gates_to_constraints(
            sections=["技术精要"],
            profile=self._profile(),
            registry={},
            core_figures=[],
        )
        # Form-based preferences replace char targets
        assert "表格" in text
        assert "禁止" in text and "伪代码" in text
        assert "散文" in text  # discusses when prose is allowed

    def test_principle_section_constraints(self):
        from deepaper.prompt_builder import gates_to_constraints
        text = gates_to_constraints(
            sections=["第一性原理分析"],
            profile=self._profile(),
            registry={},
            core_figures=[],
        )
        # Must instruct use of [C1] numbered causal chain
        assert "[C1]" in text
        assert "Because" in text and "Therefore" in text

    def test_overview_section_constraints(self):
        from deepaper.prompt_builder import gates_to_constraints
        text = gates_to_constraints(
            sections=["核心速览", "机制迁移"],
            profile=self._profile(),
            registry={},
            core_figures=[],
        )
        # Requires standardized tables
        assert "关键数字表" in text or "指标 | 数值" in text
        assert "原语名称" in text  # mechanism decomposition table
```

- [ ] **Step 2: Run failing tests**

Run: `pytest tests/test_prompt_builder.py::TestGatesToConstraintsV2 -v`

Expected: FAIL (gates_to_constraints still outputs char targets and lacks form preferences)

- [ ] **Step 3: Delete compute_scaling_factor**

In `src/deepaper/prompt_builder.py`, delete the entire `compute_scaling_factor` function (lines ~96-109).

- [ ] **Step 4: Rewrite gates_to_constraints**

Replace the `gates_to_constraints` function body (lines ~112-198) with:

```python
def gates_to_constraints(
    sections: list[str],
    profile: dict,
    registry: dict,
    core_figures: list[dict],
) -> str:
    """Translate gate requirements into Writer prompt constraints.

    v2: replaces char-count targets with form-based preferences. We tell the
    writer WHAT STRUCTURE to use (tables, flowcharts, numbered causal chains),
    not HOW MANY CHARS to produce. Paper length grows the tables, not the
    prose.
    """
    _ = profile  # unused in v2
    _ = registry  # unused in v2
    lines = ["## ⚠️ 质量合同（写完后会被 programmatic 验证，不达标需返工）\n"]

    lines.append("**硬约束（gate 验证）：**")
    lines.append(f"- 主标题 {'#' * HEADING_SECTION_LEVEL}（h{HEADING_SECTION_LEVEL}），"
                 f"子标题 {'#' * HEADING_SUBSECTION_LEVEL}（h{HEADING_SUBSECTION_LEVEL}），"
                 f"禁止 h1/h2/h3（H6）。代码块内 # 注释不受限制")

    # Figure references (H7)
    if core_figures:
        fig_ids = [f"Figure {cf['id']}" for cf in core_figures]
        lines.append(f"- 必须引用灵魂图: {', '.join(fig_ids)}（H7）")

    # Frontmatter requirements (only for overview writer owning 核心速览)
    if "核心速览" in sections:
        lines.append("- YAML frontmatter baselines ≥ 2 个模型（H1）")
        lines.append("- frontmatter.tldr 字段必须包含 ≥2 个具体量化数字（H5）")
        lines.append("- frontmatter 必须包含 tags / mechanisms / key_tradeoffs / key_numbers 四个结构化字段")

    # Per-section structural content markers (H9)
    content_rules = _section_content_markers(sections)
    for rule in content_rules:
        lines.append(f"- {rule}")

    # --- Form preferences (the core v2 change) ---
    lines.append("\n**表达形式偏好（核心原则）：**")
    lines.append("- 默认使用结构化形式（表格/流程图/列表），散文仅用于补充推理语境")
    lines.append("- **禁止生成伪代码**（任何 ```python``` / ```pseudo``` 代码块都不允许）")
    lines.append("- **数字对比必须用表格**，禁止散文内嵌 \"A 的 X 是 5.2，B 是 4.8\" 这种对比")
    lines.append("- 对比 / 排序 / 成本 / 符号 必须用表格（硬性要求）")
    lines.append("- 因果链 / 设计决策的理由 可用 1-3 句短散文补充，不鼓励展开为段落")
    lines.append("- 比喻 ≤ 1 句，嵌入因果链内，不独立成段")

    # Standardized table column names (so outputs can be stitched across papers)
    if any(s in sections for s in ["核心速览", "技术精要", "机制迁移"]):
        lines.append("\n**标准化表格列名（跨论文可拼接，禁止改动）：**")
    if "核心速览" in sections:
        lines.append("- 关键数字表: `指标 | 数值 | 基线 | 基线值 | 增益`")
    if "技术精要" in sections:
        lines.append("- 符号表: `符号 | 含义 | 关键值`")
        lines.append("- 设计决策表: `决策 | 备选方案 | 选择理由 | 证据来源`")
        lines.append("- 消融排序表: `排名 | 组件 | 增益 | 数据来源`")
        lines.append("- 隐性成本表: `成本项 | 量化数据 | 对决策的影响`")
    if "机制迁移" in sections:
        lines.append("- 机制解耦表: `原语名称 | 本文用途 | 抽象描述 | 信息论/几何直觉`")

    # Causal chain format
    if "第一性原理分析" in sections:
        lines.append("\n**因果链格式（硬性要求）：**")
        lines.append("- 使用编号 `[C1]`, `[C2]`, `[C3]` 前缀（≤3 条）")
        lines.append("- 每条格式：`[C1] Because {前提} → Therefore {结论}`")
        lines.append("- 可附 ≤1 句比喻或语境补充，写在 `— ` 后")
        lines.append("- 编号支持未来跨论文引用，不要省略 `[Cx]` 前缀")

    return "\n".join(lines)
```

- [ ] **Step 5: Update _section_content_markers**

Replace the `_section_content_markers` function (around line 201-215) with:

```python
def _section_content_markers(sections: list[str]) -> list[str]:
    """Return H9 content marker constraints relevant to given sections."""
    markers = []
    if "核心速览" in sections:
        markers.append("TL;DR 含 ≥2 个量化数字（H9）")
        markers.append("核心机制一句话 `[动作]+[对象]+[方式]+[效果]` 格式（H9）")
        markers.append("关键数字表（标准化列名）必须存在（H9）")
    if "第一性原理分析" in sections:
        markers.append("因果链 `[C1]` 编号 + Because→Therefore 格式必须存在（H9）")
    if "技术精要" in sections:
        markers.append("方法流程图（≥3 个 → 箭头）必须存在（H9）")
        markers.append("设计决策表（决策|备选方案|选择理由|证据来源）必须存在（H9）")
        markers.append("消融排序表（排名|组件|增益|数据来源）必须存在（H9）")
        markers.append("易混淆点 ≥2 个 ❌/✅ 对（H9）")
        markers.append("隐性成本表（成本项|量化数据|对决策的影响）必须存在（H9）")
    if "机制迁移" in sections:
        markers.append("机制解耦表（4列: 原语名称|本文用途|抽象描述|信息论直觉）必须存在（H9）")
        markers.append("前身 (Ancestors) ≥ 3 个（H9）")
    return markers
```

- [ ] **Step 6: Run tests**

Run: `pytest tests/test_prompt_builder.py -v`

Expected: PASS (all tests including new TestGatesToConstraintsV2 pass)

- [ ] **Step 7: Commit**

```bash
git add src/deepaper/prompt_builder.py tests/test_prompt_builder.py
git commit -m "refactor(prompt_builder): form preferences replace char targets

- Delete compute_scaling_factor (char scaling no longer used)
- gates_to_constraints injects form preferences: tables over prose, no
  pseudocode, standardized column names, numbered causal chains
- Per-section H9 markers reflect v2 structural requirements
- Writer prompts now guide by STRUCTURE not LENGTH — long papers grow
  tables rather than prose"
```

---

## Phase 3: Gates Update

### Task 6: Change H3 from char-floor check to section-existence check

**Files:**
- Modify: `src/deepaper/gates.py` (H3 check function and run_hard_gates wiring)
- Modify: `tests/test_gates.py` (H3 test class)

- [ ] **Step 1: Add failing test**

Add to `tests/test_gates.py`:

```python
class TestH3SectionExistence:
    """H3 v2: checks that all 4 required sections exist (by heading), not char floor."""

    def test_all_four_sections_present(self):
        from deepaper.gates import check_sections_exist
        md = (
            "---\ntitle: X\n---\n"
            "#### 核心速览\ncontent\n"
            "#### 第一性原理分析\ncontent\n"
            "#### 技术精要\ncontent\n"
            "#### 机制迁移\ncontent\n"
        )
        result = check_sections_exist(md)
        assert result["passed"] is True
        assert result["missing"] == []

    def test_missing_one_section_fails(self):
        from deepaper.gates import check_sections_exist
        md = (
            "#### 核心速览\ncontent\n"
            "#### 第一性原理分析\ncontent\n"
            "#### 技术精要\ncontent\n"
            # 机制迁移 missing
        )
        result = check_sections_exist(md)
        assert result["passed"] is False
        assert "机制迁移" in result["missing"]

    def test_empty_section_still_counts_as_present(self):
        """v2 does not enforce char floors, only heading existence."""
        from deepaper.gates import check_sections_exist
        md = (
            "#### 核心速览\n"
            "#### 第一性原理分析\n"
            "#### 技术精要\n"
            "#### 机制迁移\n"
        )
        result = check_sections_exist(md)
        assert result["passed"] is True
```

- [ ] **Step 2: Run failing test**

Run: `pytest tests/test_gates.py::TestH3SectionExistence -v`

Expected: FAIL (ImportError — `check_sections_exist` does not exist yet)

- [ ] **Step 3: Add check_sections_exist in gates.py**

In `src/deepaper/gates.py`, locate the existing `check_char_floors` function (use Grep to find it). Add a new function right after it:

```python
def check_sections_exist(md: str) -> dict:
    """H3 v2: verify all 4 required section headings exist.

    Replaces char-floor based H3 from v1. In v2 we enforce structural
    presence, not character count. Paper length grows via tables, so a
    section can legitimately be short.
    """
    from deepaper.output_schema import SECTION_ORDER
    body = _extract_body(md)
    missing: list[str] = []
    for sec_name in SECTION_ORDER:
        # Match #### <name> at heading level 4 (or higher)
        pattern = re.compile(rf"^#{{4,6}}\s*{re.escape(sec_name)}\s*$", re.MULTILINE)
        if not pattern.search(body):
            missing.append(sec_name)
    return {
        "passed": len(missing) == 0,
        "missing": missing,
    }
```

- [ ] **Step 4: Wire check_sections_exist into run_hard_gates**

In `src/deepaper/gates.py`, locate `run_hard_gates` and find the H3 call (search for `results["H3"]`). Replace the old H3 line with:

```python
    # H3: Section existence (v2 — replaces char-floor check)
    results["H3"] = check_sections_exist(merged_md)
```

Delete the `check_char_floors` function entirely (it's replaced by `check_sections_exist`).

- [ ] **Step 5: Update old H3 tests in tests/test_gates.py**

Find the existing `TestH3CharFloors` class (or similar) in `tests/test_gates.py` and delete it — it tests the removed `check_char_floors` function.

- [ ] **Step 6: Run all gate tests**

Run: `pytest tests/test_gates.py -v`

Expected: PASS (new H3 tests pass, old H3 char-floor tests removed, other gates unaffected)

- [ ] **Step 7: Commit**

```bash
git add src/deepaper/gates.py tests/test_gates.py
git commit -m "refactor(gates): H3 now checks section existence, not char floors

- Delete check_char_floors (replaced by check_sections_exist)
- H3 passes when all 4 v2 sections have heading markers (#### name)
- Char floors deprecated: v2 uses structured forms, where section length
  is driven by table rows, not prose word count. A 'short' section can
  still convey the same info density."
```

---

### Task 7: Update H1 frontmatter check to use v2 fields

**Files:**
- Modify: `src/deepaper/gates.py` (check_baselines_format, any other frontmatter checks)
- Modify: `tests/test_gates.py` (TestH1 tests)

- [ ] **Step 1: Inspect current check_baselines_format and update test**

Run: `grep -n "check_baselines_format\|check_frontmatter" /Users/bytedance/github/deepaper/src/deepaper/gates.py`

Read the existing function to understand its interface.

Add this test to `tests/test_gates.py`:

```python
class TestH1V2FrontmatterFields:
    """H1 v2: frontmatter gains new structured fields."""

    def test_v2_fields_accepted(self):
        from deepaper.gates import check_baselines_format
        md = (
            "---\n"
            "title: Test\n"
            "baselines:\n"
            "  - ModelA\n"
            "  - ModelB\n"
            "tags:\n"
            "  - pretraining\n"
            "mechanisms:\n"
            "  - name: M1\n"
            "    scope: pretrain\n"
            "key_tradeoffs:\n"
            "  - decision: D1\n"
            "    reason: R1\n"
            "key_numbers:\n"
            "  - metric: MATH\n"
            "    value: 96.2\n"
            "tldr: \"Paper with MATH 96.2% and AIME 80.6%\"\n"
            "---\n"
            "#### 核心速览\ncontent\n"
        )
        result = check_baselines_format(md)
        assert result["passed"] is True
```

- [ ] **Step 2: Run test**

Run: `pytest tests/test_gates.py::TestH1V2FrontmatterFields -v`

Expected: Likely PASS if `check_baselines_format` only checks `baselines` field. If it also validates `datasets`/`metrics`/`keywords` (old required fields), it will FAIL.

- [ ] **Step 3: Fix check_baselines_format if needed**

If Step 2 fails, update `check_baselines_format` (and any related `check_frontmatter_fields` function) in `src/deepaper/gates.py` to:
- Only require `baselines` (≥2), `tldr` (≥2 numbers)
- Not require `datasets`, `metrics`, `keywords`
- Accept new fields `tags`, `mechanisms`, `key_tradeoffs`, `key_numbers` (don't reject if present)

If Step 2 passes without changes, skip this step.

- [ ] **Step 4: Run full gates test suite**

Run: `pytest tests/test_gates.py -v`

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/deepaper/gates.py tests/test_gates.py
git commit -m "refactor(gates): H1 accepts v2 frontmatter fields

New required fields: title, baselines (≥2), tldr (≥2 nums), tags, mechanisms,
key_tradeoffs, key_numbers. Removed requirements: datasets, metrics, keywords."
```

---

## Phase 4: Merge Command Bug Fixes

### Task 8: Fix merge frontmatter hoisting

**Files:**
- Modify: `src/deepaper/cli.py:649-706` (the merge function)
- Modify: `tests/test_cli.py` (add merge hoisting test)

**Context:** Currently `cli.py merge` concatenates writer parts in `SECTION_ORDER`. If the part containing YAML frontmatter (owned by `writer-overview` which writes 核心速览) is not first in the order, the frontmatter ends up mid-file and H1/H5 gates fail because `_extract_frontmatter` requires `---` at file start.

- [ ] **Step 1: Add failing test**

Add to `tests/test_cli.py`:

```python
class TestMergeFrontmatterHoisting:
    """Merge must hoist YAML frontmatter to file top regardless of part order."""

    def test_hoists_frontmatter_from_middle(self, tmp_path):
        from deepaper.cli import _hoist_frontmatter

        # Simulated merged output where frontmatter landed mid-file
        content = (
            "#### 第一性原理分析\n"
            "痛点: something\n"
            "\n"
            "---\n"
            "title: Test\n"
            "baselines:\n"
            "  - A\n"
            "  - B\n"
            "---\n"
            "\n"
            "#### 核心速览\n"
            "TL;DR: 96.2% MATH\n"
        )
        result = _hoist_frontmatter(content)
        assert result.startswith("---\n")
        # Frontmatter should be at top
        lines = result.split("\n")
        assert lines[0] == "---"
        # Second --- should close frontmatter
        second_dash = next(i for i, l in enumerate(lines[1:], start=1) if l == "---")
        assert "title: Test" in "\n".join(lines[1:second_dash])
        # Body sections should follow
        remainder = "\n".join(lines[second_dash + 1:])
        assert "#### 核心速览" in remainder
        assert "#### 第一性原理分析" in remainder

    def test_leaves_content_alone_when_frontmatter_already_at_top(self):
        from deepaper.cli import _hoist_frontmatter
        content = (
            "---\n"
            "title: Already at top\n"
            "---\n"
            "\n"
            "#### 核心速览\nbody\n"
        )
        result = _hoist_frontmatter(content)
        assert result.startswith("---\ntitle: Already at top")

    def test_collapses_double_heading_markers(self):
        from deepaper.cli import _hoist_frontmatter
        content = "#### #### 核心速览\nbody\n"
        result = _hoist_frontmatter(content)
        assert "#### ####" not in result
        assert "#### 核心速览" in result
```

- [ ] **Step 2: Run failing test**

Run: `pytest tests/test_cli.py::TestMergeFrontmatterHoisting -v`

Expected: FAIL (ImportError — `_hoist_frontmatter` does not exist)

- [ ] **Step 3: Add _hoist_frontmatter helper in cli.py**

In `src/deepaper/cli.py`, add this helper function above the `merge` command (around line 648, just before the `@app.command()` decorator for merge):

```python
def _hoist_frontmatter(content: str) -> str:
    """Move YAML frontmatter to the top and collapse double #### markers.

    When writers write parts independently, the part containing frontmatter
    may not be first in merge order, so frontmatter ends up mid-file. This
    helper detects the `---\\n...---\\n` block anywhere in the content and
    moves it to the start. Also collapses accidental `#### #### ` duplicates.
    """
    import re as _re

    content = content.strip()

    # Collapse double heading markers: "#### #### X" -> "#### X"
    content = _re.sub(r"#### #### ", "#### ", content)

    if content.startswith("---\n"):
        return content  # Already at top

    # Find the first standalone "---\n...\n---\n" YAML block
    match = _re.search(r"(^|\n)---\n(.*?)\n---\n", content, _re.DOTALL)
    if not match:
        return content  # No frontmatter to hoist

    fm_block = "---\n" + match.group(2).strip() + "\n---\n\n"
    body = content[:match.start()] + content[match.end():]
    body = body.lstrip("\n")
    return fm_block + body
```

- [ ] **Step 4: Wire _hoist_frontmatter into the merge command**

In `src/deepaper/cli.py`, locate the end of the merge function body (around line 702, just before `merged_path = run_dir / "merged.md"`). Add the hoist call after all concatenation is done but before writing:

Find this existing block:
```python
    # Remove stray title lines
    merged = re.sub(r"^#{1,3}\s+.*(?:Part [ABC]|深度分析|部分).*\n+", "", merged, flags=re.MULTILINE)

    merged_path = run_dir / "merged.md"
```

Insert `merged = _hoist_frontmatter(merged)` between them:

```python
    # Remove stray title lines
    merged = re.sub(r"^#{1,3}\s+.*(?:Part [ABC]|深度分析|部分).*\n+", "", merged, flags=re.MULTILINE)

    # Hoist YAML frontmatter to top and collapse double #### markers
    merged = _hoist_frontmatter(merged)

    merged_path = run_dir / "merged.md"
```

- [ ] **Step 5: Run tests**

Run: `pytest tests/test_cli.py::TestMergeFrontmatterHoisting -v`

Expected: PASS (all three tests)

- [ ] **Step 6: Run full cli test suite to catch regressions**

Run: `pytest tests/test_cli.py -v`

Expected: PASS (no regressions in existing merge tests)

- [ ] **Step 7: Commit**

```bash
git add src/deepaper/cli.py tests/test_cli.py
git commit -m "fix(cli): hoist YAML frontmatter to top and collapse double ####

Writers write parts independently, so the frontmatter-owning part may not
be first in merge order, leaving frontmatter mid-file and breaking H1/H5
gates. Also fix '#### #### X' duplicate heading bug from over-aggressive
section headers in writer output."
```

---

## Phase 5: H2 Coverage Noise Filter

### Task 9: Filter noisy table-row labels from subsection_headings

**Files:**
- Modify: `src/deepaper/output_schema.py` (H2_SUBSECTION_REGEX)
- Modify: `tests/test_registry.py` (add filter test)

**Context:** The current regex `r"^((?:[1-9]|1\d|20)\.\d{1,2}\.?\s+[A-Za-z].*)$"` matches lines like `3.1 Our Approach` (good) but also `1.0 Bits-per-byte` and `2.3 HarmBench` (table row labels, bad). We tighten the regex to require at least 2 words with letters.

- [ ] **Step 1: Add failing test**

Add to `tests/test_registry.py`:

```python
class TestSubsectionHeadingFilter:
    """Subsection detection must not match table row labels."""

    def test_legitimate_subsection_detected(self):
        from deepaper.registry import compute_paper_profile
        text_by_page = {
            1: "intro",
            2: "3.1 Main Results for Olmo 3 Base\nSome body text here.\n"
               "3.2 Modeling and Architecture\nMore body text.\n",
        }
        registry = {}
        profile = compute_paper_profile(text_by_page, registry)
        headings = profile["subsection_headings"]
        assert any("Main Results for Olmo 3 Base" in h for h in headings)
        assert any("Modeling and Architecture" in h for h in headings)

    def test_table_row_labels_filtered(self):
        from deepaper.registry import compute_paper_profile
        text_by_page = {
            1: "2.3 HarmBench\n"
               "1.0 Bits-per-byte\n"
               "14.5 GPQA\n"
               "3.1 Our Real Section Name Here\n",
        }
        registry = {}
        profile = compute_paper_profile(text_by_page, registry)
        headings = profile["subsection_headings"]
        # Only the multi-word section name should be detected
        assert any("Our Real Section Name Here" in h for h in headings)
        # Single-word table labels should be filtered
        assert not any("HarmBench" in h and len(h.split()) <= 2 for h in headings)
        assert not any("Bits-per-byte" in h and len(h.split()) <= 2 for h in headings)
        assert not any("GPQA" in h and len(h.split()) <= 2 for h in headings)
```

- [ ] **Step 2: Run failing test**

Run: `pytest tests/test_registry.py::TestSubsectionHeadingFilter -v`

Expected: FAIL (table row labels currently match)

- [ ] **Step 3: Tighten the regex in output_schema.py**

In `src/deepaper/output_schema.py`, replace line ~110:

```python
# H2: Structural coverage
# Subsection regex must require at least one letter after the number,
# to avoid matching table cell values like "96.2 49.2".
H2_SUBSECTION_REGEX = r"^((?:[1-9]|1\d|20)\.\d{1,2}\.?\s+[A-Za-z].*)$"
```

With this tighter version (requires at least 2 whitespace-separated word tokens with letters after the number):

```python
# H2: Structural coverage
# Subsection regex requires:
#   - numeric prefix like "3.1" or "10.2" (not "1.0" style that could be a
#     table cell because single-digit.single-digit is rare for subsections)
#   - at least THREE whitespace-separated tokens after the number (real
#     section titles are multi-word like "Main Results for Olmo 3 Base";
#     table row labels are typically 1-2 words like "BBH" or "MATH 500")
H2_SUBSECTION_REGEX = (
    r"^((?:[1-9]|1\d|20)\.\d{1,2}\.?\s+[A-Z][A-Za-z]+"
    r"(?:\s+[A-Za-z0-9][\w-]*){2,}.*)$"
)
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_registry.py::TestSubsectionHeadingFilter -v`

Expected: PASS

- [ ] **Step 5: Run full registry tests to catch regressions**

Run: `pytest tests/test_registry.py -v`

Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/deepaper/output_schema.py tests/test_registry.py
git commit -m "fix(registry): tighten H2 subsection regex to filter table row labels

The old regex matched any 'N.M + alpha' line, catching table cell labels
like '1.0 Bits-per-byte' as subsections. The new regex requires ≥3 word
tokens after the number, filtering short labels while keeping real
section titles like '3.1 Main Results for Olmo 3 Base'."
```

---

## Phase 6: Sync Dev Mirror and Full Pipeline Validation

### Task 10: Sync templates/default.md with DEFAULT_TEMPLATE

**Files:**
- Overwrite: `templates/default.md`

**Context:** `templates/default.md` at the repo root is a dev-convenience copy (not read at runtime — the source of truth is `src/deepaper/defaults.py:DEFAULT_TEMPLATE`). We keep it in sync so developers reading the repo see the current template.

- [ ] **Step 1: Generate the file from DEFAULT_TEMPLATE**

Run:
```bash
python -c "from deepaper.defaults import DEFAULT_TEMPLATE; open('/Users/bytedance/github/deepaper/templates/default.md', 'w').write(DEFAULT_TEMPLATE)"
```

- [ ] **Step 2: Verify content matches**

Run:
```bash
python -c "from deepaper.defaults import DEFAULT_TEMPLATE; import pathlib; assert pathlib.Path('/Users/bytedance/github/deepaper/templates/default.md').read_text() == DEFAULT_TEMPLATE; print('OK')"
```

Expected output: `OK`

- [ ] **Step 3: Commit**

```bash
git add templates/default.md
git commit -m "chore(templates): sync templates/default.md with defaults.py

Keeps the dev-mirror file in sync with the runtime source of truth
(src/deepaper/defaults.py:DEFAULT_TEMPLATE)."
```

---

### Task 11: Full test suite + lint

**Files:** (read-only checks)

- [ ] **Step 1: Run all tests**

Run: `pytest tests/ -v 2>&1 | tail -40`

Expected: All tests pass. If any fail, fix them before proceeding — note the failures by test name and add a fix-up commit.

- [ ] **Step 2: Run ruff lint**

Run: `ruff check src/deepaper/`

Expected: No errors. Fix any issues in a fix-up commit.

- [ ] **Step 3: Commit any fix-ups (if needed)**

If Steps 1 or 2 revealed issues, commit the fixes:

```bash
git add <fixed files>
git commit -m "fix: address lint/test issues from v2 refactor"
```

---

### Task 12: End-to-end pipeline validation on a real paper

**Files:** (runtime validation, no code changes expected)

- [ ] **Step 1: Pick a short paper for validation**

Use a ~20-page paper to keep the validation fast. Example: run against `2312.11805` (or any arxiv ID already downloaded).

If `.deepaper/runs/<id>/` doesn't exist, run:
```bash
deepaper download https://arxiv.org/abs/2312.11805
deepaper extract 2312.11805
```

(You can swap the ID for any short paper of your choice.)

- [ ] **Step 2: Run the extractor stage**

```bash
deepaper prompt 2312.11805 --role extractor
```

Manually dispatch the extractor agent (or use the `/deepaper` slash command). Verify `notes.md` is written.

- [ ] **Step 3: Run the writers stage (3 writers)**

```bash
deepaper prompt 2312.11805 --split
```

Expected JSON output should show exactly 3 writers: `writer-overview`, `writer-principle`, `writer-technical`.

Dispatch all 3 writers in parallel.

- [ ] **Step 4: Merge and gate**

```bash
deepaper merge 2312.11805
deepaper gates 2312.11805
```

Verify:
- `merged.md` starts with `---\n` (frontmatter at top)
- No `#### ####` duplicate headings (grep: `grep -c "#### ####" .deepaper/runs/2312.11805/merged.md` should return 0)
- Gates output shows H1 / H3 / H5 / H6 / H9 passing
- H2 may pass or skip (noise filter is in place)

- [ ] **Step 5: Verify output character count**

```bash
wc -c .deepaper/runs/2312.11805/merged.md
```

Expected: ~8,000 to ~15,000 characters (the ~10K target range). Document the actual number.

- [ ] **Step 6: Spot-check output readability**

Open `merged.md` and verify:
- 4 sections present with correct order
- Each section uses tables/flowcharts as primary form
- No pseudocode blocks
- Causal chains use `[C1]`, `[C2]` numbering
- Frontmatter includes `tags`, `mechanisms`, `key_tradeoffs`, `key_numbers`

- [ ] **Step 7: Document findings in commit message**

```bash
git commit --allow-empty -m "test: e2e pipeline validation for v2 format on arxiv 2312.11805

Output: <N> chars (target ~10K ± 50%)
Gates: H1=PASS H3=PASS H5=PASS H6=PASS H9=PASS H2=<status>
Sections: 4 present, correct order, frontmatter at top
Form: tables dominant, no pseudocode, [C1][C2] causal chains used
Frontmatter: tags/mechanisms/key_tradeoffs/key_numbers all populated"
```

---

## Self-Review Checklist

After implementing all tasks, verify:

**1. Spec coverage:**

| Spec Requirement | Task |
|------------------|------|
| 4 章节结构 (核心速览/第一性原理分析/技术精要/机制迁移) | Task 1, 2 |
| 表达形式约束（表格/流程图为主，禁止伪代码） | Task 1, 5 |
| 标准化表格列名 | Task 1, 5 |
| 因果链 `[C1][C2]` 编号 | Task 1, 3, 5 |
| YAML frontmatter 新增 tags/mechanisms/key_tradeoffs/key_numbers | Task 1, 2, 7 |
| YAML frontmatter 删除 datasets/metrics/keywords | Task 2, 7 |
| 3 writer 分配 (overview/principle/technical) | Task 4 |
| 删除 compute_scaling_factor | Task 5 |
| H3 改为章节存在性检查 | Task 6 |
| H5/H1 从 frontmatter 检查（兼容新字段） | Task 7 |
| merge frontmatter 置顶修复 | Task 8 |
| merge `#### ####` 双重标记修复 | Task 8 |
| H2 subsection 噪声过滤 | Task 9 |
| templates/default.md 同步 | Task 10 |
| reindex / log.md (deferred) | N/A — out of scope |
| 概念页 / 合成页 (deferred) | N/A — out of scope |

All in-scope spec requirements have corresponding tasks.

**2. No placeholders:** All tasks contain full code, not "implement similar to..." or "TBD".

**3. Type consistency:** Function names and section names are consistent across tasks:
- `check_sections_exist` (Task 6) — used consistently
- `_hoist_frontmatter` (Task 8) — used consistently
- Section names `核心速览 / 第一性原理分析 / 技术精要 / 机制迁移` — consistent across Task 1, 2, 3, 4, 5, 6

---

## Execution Notes

- **Order matters:** Tasks 1-5 form the foundational refactor. Do them in order. Tasks 6-9 are independent and can be done in any order after Task 5. Tasks 10-12 are final steps.
- **Breakage window:** Tests may be in a broken state between Task 1 (template changes) and Task 5 (prompt_builder updates). This is expected. Task 5 should leave the full test suite green again.
- **Rollback point:** Each task commits independently. If a task fails, `git reset --hard HEAD~1` reverts just that task.
- **Skipped tasks:** Task 12 (e2e validation) requires dispatching writer agents interactively. If running in an automated context without agent access, mark Task 12 as skipped and run it manually after merge.
