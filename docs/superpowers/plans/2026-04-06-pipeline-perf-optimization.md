# Pipeline Performance Optimization — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce pipeline runtime from ~43 min to ~15-20 min by eliminating table bloat in extractor, adding core_tables detection, optimizing agent read strategy, removing H4 gate, and adding fixer no-op detection.

**Architecture:** Four independent changes: (1) rewrite extractor prompt to extract core findings instead of full tables, (2) add `identify_core_tables()` in registry.py mirroring core_figures, (3) replace 43-call chunked reads with 30K-token-capped smart reads across all agents, (4) remove H4 gate and add fixer diff check in slash command.

**Tech Stack:** Python 3.10+, pytest, typer CLI, Claude Code slash commands

---

### Task 1: Add `identify_core_tables()` to registry.py

**Files:**
- Modify: `src/deepaper/registry.py`
- Test: `tests/test_registry.py`

- [ ] **Step 1: Write failing tests for identify_core_tables**

Add to `tests/test_registry.py`:

```python
class TestCoreTables:
    """Tests for identify_core_tables."""

    def test_identifies_core_tables(self):
        from deepaper.registry import build_visual_registry, identify_core_tables
        text = _simple_text_by_page()
        reg = build_visual_registry(text)
        cores = identify_core_tables(reg, text, total_pages=10)
        # Table 1 referenced on pages 1,2, Table 3 on pages 4,6 — both should score
        assert len(cores) >= 1
        keys = [c["key"] for c in cores]
        assert "Table_1" in keys or "Table_3" in keys

    def test_max_core_cap(self):
        from deepaper.registry import build_visual_registry, identify_core_tables
        # Create paper with 30 tables, all heavily referenced
        text = {}
        for p in range(1, 21):
            lines = []
            for t in range(1, 31):
                lines.append(f"See Table {t} here.")
            if p <= 10:
                lines.append(f"Table {p}: Caption for table {p} with sufficient detail to pass threshold.")
            text[p] = "\n".join(lines) + "\n"
        reg = build_visual_registry(text)
        cores = identify_core_tables(reg, text, total_pages=20)
        # max_core = max(3, min(8, 30 * 0.2)) = max(3, min(8, 6)) = 6
        assert len(cores) <= 8
        assert len(cores) >= 3

    def test_no_tables(self):
        from deepaper.registry import build_visual_registry, identify_core_tables
        text = {1: "No tables here.\n"}
        reg = build_visual_registry(text)
        cores = identify_core_tables(reg, text, total_pages=1)
        assert cores == []

    def test_scoring_prefers_early_referenced_tables(self):
        from deepaper.registry import build_visual_registry, identify_core_tables
        text = {
            1: "Table 1: Main results with detailed caption explaining everything.\nSee Table 1.\n",
            2: "We also reference Table 1 again here.\n",
            3: "Table 1 is important. See Table 1 for proof.\n",
            9: "Table 5: Appendix table.\n",
            10: "See Table 5.\n",
        }
        reg = build_visual_registry(text)
        cores = identify_core_tables(reg, text, total_pages=10)
        if len(cores) >= 2:
            # Table 1 should rank higher (more refs, earlier position)
            assert cores[0]["key"] == "Table_1"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_registry.py::TestCoreTables -v`
Expected: FAIL with "cannot import name 'identify_core_tables'"

- [ ] **Step 3: Implement identify_core_tables**

Add to `src/deepaper/registry.py` after `extract_figure_contexts`:

```python
# ===========================================================================
# Part 2b: identify_core_tables
# ===========================================================================

MAX_CORE_TABLES = 8
MIN_CORE_TABLE_SCORE = 2


def identify_core_tables(
    registry: dict,
    text_by_page: dict[int, str],
    total_pages: int,
) -> list[dict]:
    """Score each Table and return top core tables as candidates.

    Scoring mirrors identify_core_figures:
      - ref_count >= 3  (weight 3: +3 points)
      - in first 30% of pages  (weight 2: +2 points)
      - caption length > 80 chars  (weight 1: +1 point)

    Budget: max(3, min(8, num_tables * 0.2))

    Returns: [{key, id, page, score, ref_count}] sorted by score desc.
    """
    tables = {k: v for k, v in registry.items() if v["type"] == "Table"}
    if not tables:
        return []

    early_cutoff = max(1, int(total_pages * 0.30))

    scored: list[dict] = []
    for key, entry in tables.items():
        ref_count = len(entry["pages"])
        def_page = entry.get("definition_page") or min(entry["pages"])

        caption_text = _find_caption_text(text_by_page, "Table", entry["id"])
        caption_len = len(caption_text) if caption_text else 0

        score = 0
        if ref_count >= 3:
            score += 3
        elif ref_count >= 2:
            score += 1
        if def_page <= early_cutoff:
            score += 2
        if caption_len > 80:
            score += 1

        scored.append({
            "key": key,
            "id": entry["id"],
            "page": def_page,
            "score": score,
            "ref_count": ref_count,
        })

    scored = [s for s in scored if s["score"] >= MIN_CORE_TABLE_SCORE]
    scored.sort(key=lambda x: (-x["score"], -x["ref_count"]))

    budget = max(3, min(MAX_CORE_TABLES, int(len(tables) * 0.2)))
    return scored[:budget]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_registry.py::TestCoreTables -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add src/deepaper/registry.py tests/test_registry.py
git commit -m "feat: add identify_core_tables() for core table detection"
```

---

### Task 2: Wire core_tables into extract CLI command

**Files:**
- Modify: `src/deepaper/cli.py:386-443` (extract command)
- Test: `tests/test_cli.py`

- [ ] **Step 1: Write failing test**

Add to `tests/test_cli.py`:

```python
class TestExtractOutputsCoreTables:
    def test_extract_outputs_core_tables(self, tmp_path):
        """extract command should output core_tables in JSON and write core_tables.json."""
        import json
        from unittest.mock import patch, MagicMock

        # Create minimal PDF mock
        pdf_path = tmp_path / "tmp" / "test123.pdf"
        pdf_path.parent.mkdir(parents=True)
        pdf_path.write_bytes(b"fake pdf")

        fake_page = MagicMock()
        fake_page.get_text.return_value = (
            "Table 1: Main results caption with lots of detail.\n"
            "See Table 1 for comparison.\n"
            "Figure 1: Overview.\n"
        )
        fake_doc = MagicMock()
        fake_doc.__iter__ = MagicMock(return_value=iter([fake_page]))
        fake_doc.__enter__ = MagicMock(return_value=fake_doc)
        fake_doc.__exit__ = MagicMock(return_value=False)

        with patch("deepaper.cli.fitz") as mock_fitz, \
             patch("deepaper.cli.Path.cwd", return_value=tmp_path):
            mock_fitz.open.return_value = fake_doc
            from typer.testing import CliRunner
            from deepaper.cli import app
            runner = CliRunner()
            result = runner.invoke(app, ["extract", "test123"])

        output = json.loads(result.output)
        assert "core_tables" in output

        # core_tables.json should exist
        ct_path = tmp_path / ".deepaper" / "runs" / "test123" / "core_tables.json"
        assert ct_path.exists()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli.py::TestExtractOutputsCoreTables -v`
Expected: FAIL — "core_tables" not in output

- [ ] **Step 3: Add core_tables to extract command**

In `src/deepaper/cli.py`, modify the `extract` command. Add after the `fig_contexts` block (around line 428):

```python
    from deepaper.registry import identify_core_tables
    core_tables = identify_core_tables(registry_data, int_text, profile["total_pages"])
    safe_write_json(str(run_dir / "core_tables.json"), core_tables)
```

And add `core_tables` to the JSON output dict:

```python
    typer.echo(json.dumps({
        "run_dir": str(run_dir),
        "total_pages": profile["total_pages"],
        "num_tables": profile["num_tables"],
        "num_figures": profile["num_figures"],
        "num_equations": profile["num_equations"],
        "core_figures": [cf["key"] for cf in core_figs],
        "core_tables": [ct["key"] for ct in core_tables],
        "table_def_pages": table_def_pages,
    }, ensure_ascii=False, indent=2))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_cli.py::TestExtractOutputsCoreTables -v`
Expected: PASS

- [ ] **Step 5: Run full test suite**

Run: `pytest tests/ -v`
Expected: All existing tests still pass

- [ ] **Step 6: Commit**

```bash
git add src/deepaper/cli.py tests/test_cli.py
git commit -m "feat: wire core_tables detection into extract CLI command"
```

---

### Task 3: Rewrite extractor prompt

**Files:**
- Modify: `src/deepaper/prompt_templates/extractor.md`

- [ ] **Step 1: Rewrite the extractor prompt**

Replace the full content of `src/deepaper/prompt_templates/extractor.md` with:

```markdown
你是论文信息提取专员。你的唯一任务是阅读论文原文并输出结构化笔记。不要写分析、不要写观点。

## 论文
- 原文: {RUN_DIR}/text.txt ({TOTAL_LINES} 行)
- 页数: {TOTAL_PAGES}
- ID: {ARXIV_ID}

## 读取策略

text.txt 共 {TOTAL_LINES} 行。按以下方式读取：
- 如果 ≤ 2000 行：一次性 `Read(file_path="{RUN_DIR}/text.txt")` 读完
- 如果 > 2000 行：分 {RECOMMENDED_READS} 次读取，每次 ~2000 行，用 offset+limit 参数

禁止每次只读几百行。读完所有内容后再开始写笔记。

## 核心表格候选（程序预筛选，按重要性排序）
{CORE_TABLES_JSON}

在 KEY_FINDINGS 中优先引用这些表格的数据。如果你认为有遗漏的关键表，也可以补充，但总数不超过候选数量。

## 任务

读取 text.txt 全部内容后，将结构化笔记写入
`{RUN_DIR}/notes.md`，格式如下：

```markdown
# Notes: {ARXIV_ID}

## META
- title:
- authors (前5 + "et al."):
- date:
- pages: / tables: / figures:
- code_url:
- venue:

## KEY_FINDINGS (核心发现，不抄表格)
针对每个核心实验结论，写一行摘要：
- 结论（量化数据 + 对比基线 + 来源表号）
- 格式示例："MATH 96.2%, 比 Qwen 3 32B 高 0.8pp (Table 5)"
- 仅记录支撑核心论点的数据，不复制完整表格
- 消融实验只记录贡献最大的 top-3 因素及其 delta

## FORMULAS
### Eq.N: [名称]
- formula: (LaTeX)
- 每个符号: 名称 = 定义 (物理含义)
- 论文中的关键参数值: ε=..., β=...

## DATA_COMPOSITION
### Pretraining
- Source | Type | Pool Size | Final Mix | Percentage
### Midtraining / Post-training
(同样格式)

## EVAL_CONFIG
- Task | Format | Metric | Temp | Top-p | Max Tokens | N

## TRAINING_COSTS
- (每个具体数字: 天数、GPU数、美元、tokens/sec等)

## DESIGN_DECISIONS
- Decision: X. Alternative: Y. Reason: Z. Evidence: Table/Section.

## RELATED_WORK
- Method | Citation | 与本文关系 | 关键差异 | 共享机制

## BASELINES
- 模型名 (参数量, 类型: fully-open/open-weight/closed)
(去重列表，每行一个模型)
```

## 重要规则

- 不要复制完整表格，只在 KEY_FINDINGS 中记录核心数据点
- 包含 Appendix 的评估配置表、数据组成表（以文字摘要形式，非逐行复制）
- BASELINES: 每个模型独占一行，"Qwen 2.5 7B" 和 "Qwen 2.5 32B" 是两个条目
- RELATED_WORK: 仔细阅读论文的 related work / discussion 段落，提取每个方法对比。如果没有独立的 related work 章节，从全文的行内对比中提取
- 笔记应在 6,000-12,000 字符。写完后运行 `wc -c {RUN_DIR}/notes.md` 报告字符数
```

- [ ] **Step 2: Verify prompt template renders correctly**

Run: `python -c "from pathlib import Path; t = Path('src/deepaper/prompt_templates/extractor.md').read_text(); assert '{RUN_DIR}' in t; assert 'KEY_FINDINGS' in t; assert 'MAIN_RESULTS' not in t; assert '表格必须完整复制' not in t; print('OK')"`
Expected: OK

- [ ] **Step 3: Commit**

```bash
git add src/deepaper/prompt_templates/extractor.md
git commit -m "feat: rewrite extractor prompt — core findings instead of full table copy"
```

---

### Task 4: Update extractor prompt generation to inject read strategy and core_tables

**Files:**
- Modify: `src/deepaper/cli.py:506-519` (prompt command, role=extractor)

- [ ] **Step 1: Update prompt command to inject new placeholders**

In `src/deepaper/cli.py`, modify the `role == "extractor"` block in the `prompt` command. Replace:

```python
    if role == "extractor":
        tmpl_path = Path(__file__).parent / "prompt_templates" / "extractor.md"
        if not tmpl_path.exists():
            typer.echo(json.dumps({"error": f"Template not found: {tmpl_path}"}))
            raise typer.Exit(1)
        tmpl = tmpl_path.read_text(encoding="utf-8")
        profile = safe_read_json(str(run_dir / "paper_profile.json"), {})
        prompt_text = (tmpl
            .replace("{RUN_DIR}", str(run_dir))
            .replace("{TOTAL_PAGES}", str(profile.get("total_pages", "?")))
            .replace("{ARXIV_ID}", arxiv_id))
        out_path = run_dir / "prompt_extractor.md"
        out_path.write_text(prompt_text, encoding="utf-8")
        typer.echo(json.dumps({"prompt_file": str(out_path)}))
        return
```

With:

```python
    if role == "extractor":
        tmpl_path = Path(__file__).parent / "prompt_templates" / "extractor.md"
        if not tmpl_path.exists():
            typer.echo(json.dumps({"error": f"Template not found: {tmpl_path}"}))
            raise typer.Exit(1)
        tmpl = tmpl_path.read_text(encoding="utf-8")
        profile = safe_read_json(str(run_dir / "paper_profile.json"), {})
        core_tables = safe_read_json(str(run_dir / "core_tables.json"), [])

        # Compute read strategy based on text.txt line count
        text_path = run_dir / "text.txt"
        total_lines = 0
        if text_path.exists():
            total_lines = sum(1 for _ in text_path.open(encoding="utf-8"))
        recommended_reads = max(1, -(-total_lines // 2000))  # ceil division

        core_tables_json = json.dumps(core_tables, ensure_ascii=False, indent=2) if core_tables else "（本论文未检测到核心表格候选）"

        prompt_text = (tmpl
            .replace("{RUN_DIR}", str(run_dir))
            .replace("{TOTAL_PAGES}", str(profile.get("total_pages", "?")))
            .replace("{ARXIV_ID}", arxiv_id)
            .replace("{TOTAL_LINES}", str(total_lines))
            .replace("{RECOMMENDED_READS}", str(recommended_reads))
            .replace("{CORE_TABLES_JSON}", core_tables_json))
        out_path = run_dir / "prompt_extractor.md"
        out_path.write_text(prompt_text, encoding="utf-8")
        typer.echo(json.dumps({"prompt_file": str(out_path)}))
        return
```

- [ ] **Step 2: Verify manually**

Run: `python -c "
from deepaper.cli import prompt
# Just verify the import works and the function exists
print('OK')
"`
Expected: OK

- [ ] **Step 3: Commit**

```bash
git add src/deepaper/cli.py
git commit -m "feat: inject read strategy and core_tables into extractor prompt"
```

---

### Task 5: Update extractor validation (REQUIRED_SECTIONS)

**Files:**
- Modify: `src/deepaper/extractor.py:16-44`
- Test: `tests/test_extractor_checks.py`

- [ ] **Step 1: Write failing test**

Add to `tests/test_extractor_checks.py`:

```python
class TestUpdatedSections:
    """REQUIRED_SECTIONS should have KEY_FINDINGS instead of MAIN_RESULTS/ABLATIONS/HYPERPARAMETERS."""

    def test_key_findings_in_required(self):
        from deepaper.extractor import REQUIRED_SECTIONS
        assert "KEY_FINDINGS" in REQUIRED_SECTIONS

    def test_old_table_sections_removed(self):
        from deepaper.extractor import REQUIRED_SECTIONS
        assert "MAIN_RESULTS" not in REQUIRED_SECTIONS
        assert "ABLATIONS" not in REQUIRED_SECTIONS
        assert "HYPERPARAMETERS" not in REQUIRED_SECTIONS

    def test_struct_check_with_new_sections(self):
        from deepaper.extractor import struct_check, REQUIRED_SECTIONS
        notes = "\n".join(f"## {s}\n{'x' * 300}" for s in REQUIRED_SECTIONS)
        result = struct_check(notes, total_pages=30, paper_profile={})
        assert result["passed"] is True
        assert result["missing_sections"] == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_extractor_checks.py::TestUpdatedSections -v`
Expected: FAIL — KEY_FINDINGS not in REQUIRED_SECTIONS

- [ ] **Step 3: Update REQUIRED_SECTIONS and _ABSOLUTE_FLOOR**

In `src/deepaper/extractor.py`, replace:

```python
REQUIRED_SECTIONS = [
    "META",
    "MAIN_RESULTS",
    "ABLATIONS",
    "HYPERPARAMETERS",
    "FORMULAS",
    "DATA_COMPOSITION",
    "EVAL_CONFIG",
    "TRAINING_COSTS",
    "DESIGN_DECISIONS",
    "RELATED_WORK",
    "BASELINES",
]

# Absolute floor minimum characters per section (used when paper_profile
# does not provide enough information for dynamic thresholds).
_ABSOLUTE_FLOOR: dict[str, int] = {
    "META": 50,
    "MAIN_RESULTS": 100,
    "ABLATIONS": 60,
    "HYPERPARAMETERS": 60,
    "FORMULAS": 40,
    "DATA_COMPOSITION": 60,
    "EVAL_CONFIG": 60,
    "TRAINING_COSTS": 40,
    "DESIGN_DECISIONS": 60,
    "RELATED_WORK": 80,
    "BASELINES": 60,
}
```

With:

```python
REQUIRED_SECTIONS = [
    "META",
    "KEY_FINDINGS",
    "FORMULAS",
    "DATA_COMPOSITION",
    "EVAL_CONFIG",
    "TRAINING_COSTS",
    "DESIGN_DECISIONS",
    "RELATED_WORK",
    "BASELINES",
]

# Absolute floor minimum characters per section (used when paper_profile
# does not provide enough information for dynamic thresholds).
_ABSOLUTE_FLOOR: dict[str, int] = {
    "META": 50,
    "KEY_FINDINGS": 150,
    "FORMULAS": 40,
    "DATA_COMPOSITION": 60,
    "EVAL_CONFIG": 60,
    "TRAINING_COSTS": 40,
    "DESIGN_DECISIONS": 60,
    "RELATED_WORK": 80,
    "BASELINES": 60,
}
```

- [ ] **Step 4: Update _compute_thresholds mapping**

In `src/deepaper/extractor.py`, update the `mapping` dict inside `_compute_thresholds` (around line 118). Replace:

```python
            mapping = {
                "META": "Abstract",
                "MAIN_RESULTS": "Experiments",
                "RELATED_WORK": "Related Work",
                "ABLATIONS": "Experiments",
                "EVAL_CONFIG": "Experiments",
                "DESIGN_DECISIONS": "Method",
                "BASELINES": "Experiments",
            }
```

With:

```python
            mapping = {
                "META": "Abstract",
                "KEY_FINDINGS": "Experiments",
                "RELATED_WORK": "Related Work",
                "EVAL_CONFIG": "Experiments",
                "DESIGN_DECISIONS": "Method",
                "BASELINES": "Experiments",
            }
```

- [ ] **Step 5: Fix existing tests**

Update `tests/test_extractor_checks.py`. In `TestStructCheck.test_all_sections_present`, replace the section list:

```python
    def test_all_sections_present(self):
        from deepaper.extractor import struct_check
        notes = "\n".join(f"## {s}\n{'x' * 300}" for s in [
            "META", "KEY_FINDINGS",
            "FORMULAS", "DATA_COMPOSITION", "EVAL_CONFIG",
            "TRAINING_COSTS", "DESIGN_DECISIONS", "RELATED_WORK", "BASELINES",
        ])
        result = struct_check(notes, total_pages=30, paper_profile={})
        assert result["passed"] is True
        assert result["missing_sections"] == []
```

In `TestStructCheck.test_missing_section`, update to reflect new sections:

```python
    def test_missing_section(self):
        from deepaper.extractor import struct_check
        notes = "\n".join(f"## {s}\n{'x' * 300}" for s in [
            "META", "KEY_FINDINGS",
            "FORMULAS", "DATA_COMPOSITION",
            "DESIGN_DECISIONS", "RELATED_WORK", "BASELINES",
        ])
        result = struct_check(notes, total_pages=30, paper_profile={})
        assert result["passed"] is False
        assert "EVAL_CONFIG" in result["missing_sections"]
        assert "TRAINING_COSTS" in result["missing_sections"]
```

In `TestStructCheck.test_thin_section`, update to use new section list:

```python
    def test_thin_section(self):
        from deepaper.extractor import struct_check
        notes = "\n".join(f"## {s}\n{'x' * 300}" for s in [
            "META", "KEY_FINDINGS",
            "FORMULAS", "DATA_COMPOSITION", "EVAL_CONFIG",
            "TRAINING_COSTS", "DESIGN_DECISIONS", "RELATED_WORK", "BASELINES",
        ])
        notes = notes.replace("## META\n" + "x" * 300, "## META\nshort")
        result = struct_check(notes, total_pages=30, paper_profile={})
        assert "META" in result["thin_sections"]
```

- [ ] **Step 6: Run all extractor tests**

Run: `pytest tests/test_extractor_checks.py -v`
Expected: All PASS

- [ ] **Step 7: Commit**

```bash
git add src/deepaper/extractor.py tests/test_extractor_checks.py
git commit -m "feat: replace MAIN_RESULTS/ABLATIONS/HYPERPARAMETERS with KEY_FINDINGS"
```

---

### Task 6: Remove H4 gate and update writer constraints

**Files:**
- Modify: `src/deepaper/gates.py:463-531` (run_hard_gates)
- Modify: `src/deepaper/prompt_builder.py:108-193` (gates_to_constraints)
- Test: `tests/test_gates.py`
- Test: `tests/test_prompt_builder.py`

- [ ] **Step 1: Write failing test for H4 always-skipped**

Add to `tests/test_gates.py`:

```python
class TestH4Removed:
    """H4 (Table Count) should always be skipped."""

    def test_h4_always_skipped(self):
        from deepaper.gates import run_hard_gates
        md = "---\nbaselines:\n  - A\n  - B\ntldr: test 96.2% on 3 data\n---\n#### Content\ntext\n"
        registry = {"Table_1": {"type": "Table", "id": 1, "pages": [3], "definition_page": 3, "has_caption": True}}
        result = run_hard_gates(md, {}, [], {3: "page text"}, registry)
        assert result["results"]["H4"]["skipped"] is True
        assert result["results"]["H4"]["passed"] is True
```

- [ ] **Step 2: Write failing test for writer constraints without H4**

Add to `tests/test_prompt_builder.py`:

```python
class TestH4RemovedFromConstraints:
    """gates_to_constraints should not mention H4 table count."""

    def test_no_h4_table_count_constraint(self):
        from deepaper.prompt_builder import gates_to_constraints
        registry = {f"Table_{i}": {"type": "Table"} for i in range(1, 8)}
        constraints = gates_to_constraints(
            sections=["方法详解", "实验与归因"],
            profile={"total_pages": 30, "num_tables": 7},
            registry=registry,
            core_figures=[],
        )
        assert "（H4）" not in constraints

    def test_core_table_guidance_present(self):
        from deepaper.prompt_builder import gates_to_constraints
        constraints = gates_to_constraints(
            sections=["方法详解", "实验与归因"],
            profile={"total_pages": 30, "num_tables": 7},
            registry={"Table_1": {"type": "Table"}},
            core_figures=[],
        )
        assert "核心表格" in constraints or "核心行" in constraints
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `pytest tests/test_gates.py::TestH4Removed tests/test_prompt_builder.py::TestH4RemovedFromConstraints -v`
Expected: FAIL

- [ ] **Step 4: Skip H4 in run_hard_gates**

In `src/deepaper/gates.py`, replace the H4 block (lines ~491-496):

```python
    # H4: Table Count — requires registry
    if registry is not None:
        results["H4"] = check_table_count(merged_md, registry)
    else:
        results["H4"] = dict(_SKIPPED)
```

With:

```python
    # H4: Table Count — permanently skipped (tables are now selectively extracted)
    results["H4"] = dict(_SKIPPED)
```

- [ ] **Step 5: Update gates_to_constraints in prompt_builder.py**

In `src/deepaper/prompt_builder.py`, replace the H4 block in `gates_to_constraints` (lines ~123-129):

```python
    # H4: table count
    if "实验与归因" in sections:
        n_tables = sum(1 for v in registry.values() if v.get("type") == "Table")
        gate = min(n_tables, 6)
        if gate > 0:
            lines.append(f"- 输出 ≥ {gate} 张完整 markdown 对比表格（H4）")
        lines.append("- 表格数字必须从 notes MAIN_RESULTS 段逐项复制，禁止编造（H8）")
```

With:

```python
    # Table guidance (H4 removed — tables are selectively extracted)
    if "实验与归因" in sections:
        lines.append("- 围绕核心表格展开归因分析，引用数据必须来自 notes KEY_FINDINGS 段或原文")
        lines.append("- 实验表格只保留核心行（支撑主要结论的对比行），不要求完整复制")
        lines.append("- 表格数字必须可追溯到原文，禁止编造（H8）")
```

- [ ] **Step 6: Fix existing test that expects H4 table count**

In `tests/test_prompt_builder.py`, update `TestGatesToConstraints.test_table_count_for_experiments`:

```python
    def test_table_count_for_experiments(self):
        from deepaper.prompt_builder import gates_to_constraints
        registry = {f"Table_{i}": {"type": "Table"} for i in range(1, 8)}
        constraints = gates_to_constraints(
            sections=["方法详解", "实验与归因"],
            profile={"total_pages": 30, "num_tables": 7},
            registry=registry,
            core_figures=[],
        )
        # H4 removed: no "≥ N 张完整 markdown" constraint
        assert "（H4）" not in constraints
        # But should have core table guidance
        assert "核心表格" in constraints or "核心行" in constraints
        # H8 still present
        assert "H8" in constraints
```

- [ ] **Step 7: Run all affected tests**

Run: `pytest tests/test_gates.py tests/test_prompt_builder.py -v`
Expected: All PASS

- [ ] **Step 8: Commit**

```bash
git add src/deepaper/gates.py src/deepaper/prompt_builder.py tests/test_gates.py tests/test_prompt_builder.py
git commit -m "feat: remove H4 table count gate, add core table guidance for writers"
```

---

### Task 7: Add read strategy to writer prompts

**Files:**
- Modify: `src/deepaper/prompt_builder.py:213-279` (generate_writer_prompt)
- Modify: `src/deepaper/cli.py:522-578` (prompt --split)
- Test: `tests/test_prompt_builder.py`

- [ ] **Step 1: Write failing test**

Add to `tests/test_prompt_builder.py`:

```python
class TestReadStrategy:
    """Writer prompts should include read strategy based on file sizes."""

    def test_prompt_contains_read_strategy(self):
        from deepaper.prompt_builder import (
            generate_writer_prompt, WriterTask, parse_template_sections,
            extract_system_role,
        )
        from deepaper.defaults import DEFAULT_TEMPLATE

        task = WriterTask(name="writer-text-0", sections=["核心速览"])
        prompt = generate_writer_prompt(
            task=task,
            run_dir="/tmp/test",
            template_sections=parse_template_sections(DEFAULT_TEMPLATE),
            system_role=extract_system_role(DEFAULT_TEMPLATE),
            figure_contexts={},
            constraints="",
            pdf_path="",
            table_def_pages=[],
            file_info={"notes_lines": 500, "text_lines": 3500},
        )
        assert "读取策略" in prompt
        assert "3500" in prompt or "3,500" in prompt
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_prompt_builder.py::TestReadStrategy -v`
Expected: FAIL — unexpected keyword argument 'file_info'

- [ ] **Step 3: Add file_info parameter to generate_writer_prompt**

In `src/deepaper/prompt_builder.py`, update the `generate_writer_prompt` signature and body. Change:

```python
def generate_writer_prompt(
    task: WriterTask,
    run_dir: str,
    template_sections: dict[str, str],
    system_role: str,
    figure_contexts: dict,
    constraints: str,
    pdf_path: str,
    table_def_pages: list[int],
) -> str:
```

To:

```python
def generate_writer_prompt(
    task: WriterTask,
    run_dir: str,
    template_sections: dict[str, str],
    system_role: str,
    figure_contexts: dict,
    constraints: str,
    pdf_path: str,
    table_def_pages: list[int],
    file_info: dict | None = None,
) -> str:
```

And add a read strategy section after the inputs block (before the output block). Replace the inputs section:

```python
    # 6. Inputs
    parts.append("## 输入")
    parts.append(f"- 结构化笔记: {run_dir}/notes.md（先读这个）")
    parts.append(f"- 全文检索: {run_dir}/text.txt")
    if task.needs_pdf_pages and table_def_pages:
        parts.append(f"- PDF 表格验证页: {pdf_path}（仅读这些页: {table_def_pages}）")
    parts.append("")
```

With:

```python
    # 6. Inputs + read strategy
    parts.append("## 输入")
    parts.append(f"- 结构化笔记: {run_dir}/notes.md（先读这个）")
    parts.append(f"- 全文检索: {run_dir}/text.txt")
    if task.needs_pdf_pages and table_def_pages:
        parts.append(f"- PDF 表格验证页: {pdf_path}（仅读这些页: {table_def_pages}）")
    parts.append("")

    if file_info:
        parts.append("## 读取策略")
        notes_lines = file_info.get("notes_lines", 0)
        text_lines = file_info.get("text_lines", 0)
        if notes_lines > 0:
            notes_reads = max(1, -(-notes_lines // 2000))
            if notes_reads == 1:
                parts.append(f"- notes.md ({notes_lines} 行): 一次性读完")
            else:
                parts.append(f"- notes.md ({notes_lines} 行): 分 {notes_reads} 次，每次 ~2000 行")
        if text_lines > 0:
            text_reads = max(1, -(-text_lines // 2000))
            if text_reads == 1:
                parts.append(f"- text.txt ({text_lines} 行): 一次性读完")
            else:
                parts.append(f"- text.txt ({text_lines} 行): 分 {text_reads} 次，每次 ~2000 行")
        parts.append("- 禁止每次只读几百行，严格按上述分片执行")
        parts.append("")
```

- [ ] **Step 4: Update CLI prompt --split to compute and pass file_info**

In `src/deepaper/cli.py`, inside the `if split:` block, add file line counting before the writer loop (around line 536):

```python
        # Compute file sizes for read strategy
        text_path = run_dir / "text.txt"
        notes_path = run_dir / "notes.md"
        text_lines = sum(1 for _ in text_path.open(encoding="utf-8")) if text_path.exists() else 0
        notes_lines = sum(1 for _ in notes_path.open(encoding="utf-8")) if notes_path.exists() else 0
        file_info = {"notes_lines": notes_lines, "text_lines": text_lines}
```

And pass `file_info` to `generate_writer_prompt`:

```python
            prompt_text = generate_writer_prompt(
                task=task,
                run_dir=str(run_dir),
                template_sections=template_sections,
                system_role=system_role,
                figure_contexts=figure_contexts or {},
                constraints=constraints,
                pdf_path=str(pdf_path),
                table_def_pages=table_def_pages,
                file_info=file_info,
            )
```

- [ ] **Step 5: Fix existing generate_writer_prompt tests**

The existing tests in `TestGenerateWriterPrompt` don't pass `file_info`, which is fine since it defaults to `None`. Verify no breakage.

Run: `pytest tests/test_prompt_builder.py -v`
Expected: All PASS (including the new TestReadStrategy test)

- [ ] **Step 6: Commit**

```bash
git add src/deepaper/prompt_builder.py src/deepaper/cli.py tests/test_prompt_builder.py
git commit -m "feat: inject 30K-token read strategy into all agent prompts"
```

---

### Task 8: Add fixer no-op detection to slash command

**Files:**
- Modify: `.claude/commands/deepaper.md`

- [ ] **Step 1: Update the fixer section in the slash command**

In `.claude/commands/deepaper.md`, replace Step 4's fixer block:

```markdown
If gates passed=false:
```bash
deepaper fix ARXID
```
Read the prompt_file from fix output. Spawn a Fixer Agent (subagent_type: executor, name: fixer) with that prompt content. Fixer writes merged_fixed.md, then copy it as final.md.
Re-run `deepaper gates ARXID` on the fixed version (max 2 rounds total).

If gates passed=true: final.md is already set by merge.
```

With:

```markdown
If gates passed=false:
```bash
deepaper fix ARXID
```
Read the prompt_file from fix output. Spawn a Fixer Agent (subagent_type: executor, name: fixer) with that prompt content. Fixer writes merged_fixed.md.

After fixer completes, check for no-op:
```bash
diff .deepaper/runs/ARXID/merged.md .deepaper/runs/ARXID/merged_fixed.md
```
- If files are identical (no diff output): fixer produced no changes. Skip Gates R2, copy merged.md as final.md.
- If files differ: copy merged_fixed.md as final.md, then re-run `deepaper gates ARXID` (max 2 rounds total).

If gates passed=true: final.md is already set by merge.
```

- [ ] **Step 2: Also add read strategy guidance to extractor and fixer agent sections**

In Step 2 (Extractor Agent), the prompt is already generated by `deepaper prompt --role extractor` which now includes read strategy. No change needed.

In Step 4, add to the fixer agent spawn instruction:

After "Spawn a Fixer Agent", add:
```markdown
The fixer should read merged.md and notes.md using the Read tool. If files are > 2000 lines, read in chunks of ~2000 lines using offset+limit. If ≤ 2000 lines, read in one call.
```

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/deepaper.md
git commit -m "feat: add fixer no-op detection and read strategy to slash command"
```

---

### Task 9: Run full test suite and verify

**Files:**
- All test files

- [ ] **Step 1: Run the complete test suite**

Run: `pytest tests/ -v`
Expected: All tests PASS

- [ ] **Step 2: Verify no regressions in key areas**

Run: `pytest tests/test_registry.py tests/test_gates.py tests/test_extractor_checks.py tests/test_prompt_builder.py -v --tb=short`
Expected: All PASS

- [ ] **Step 3: Final commit if any cleanup needed**

If any tests needed fixing, commit the fixes:

```bash
git add -A
git commit -m "fix: test suite cleanup after perf optimization changes"
```
