# Output Schema: Gate/Writer 统一契约

**Date:** 2026-04-06
**Status:** Approved
**Baseline:** OLMo-3 profiling Run 2 — 27 min, 671K tokens, H2/H5/H6/H8 全部失败

---

## 问题

Gate 和 Writer prompt 各自独立定义 merged.md 的格式期望，没有共享的数据契约。导致：

1. **H5:** Gate 检查 YAML `fm.get("tldr")`，Writer 写在 body `##### TL;DR` — 字段位置不一致
2. **H6:** Gate 全文扫描 `^#{1,7}\s+`，不排除代码块 — 与 H9 要求伪代码冲突
3. **H2:** `_SUBSECTION_RE` 误匹配表格数值行 — 正则未约束必须含字母
4. **H8:** `definition_page=None` 时 source_numbers 为空，100% untraced — 缺少退化输入处理

Fixer 被触发后为绕过 gate 做了两个破坏性 hack：塞 PDF 原文附录（hack H2）、把 markdown 表格改成纯文本（hack H8）。

## 方案

新增 `output_schema.py` 作为 merged.md 格式的唯一真相源。Gate 和 Writer prompt 都从它派生。

### output_schema.py 结构

```python
OUTPUT_SCHEMA = {
    "frontmatter": {
        "required_fields": {
            "venue": {"type": "str_or_null"},
            "tldr": {"type": "str", "min_numbers": 2},
            "baselines": {"type": "list", "min_items": 2},
            "datasets": {"type": "list", "min_items": 1},
            "metrics": {"type": "list", "min_items": 1},
            "keywords": {"type": "list", "min_items": 5},
        },
    },
    "body": {
        "heading_levels": {
            "section": 4,
            "subsection": 5,
            "forbidden": [1, 2, 3, 7],
        },
        "code_blocks_exempt_from_heading_check": True,
        "sections": SECTIONS,  # list of SectionSpec
    },
    "gates": {
        "H2": {
            "subsection_regex": r"^(\d+\.\d+\.?\s+[A-Za-z].*)$",
            "min_coverage": 0.6,
        },
        "H8": {
            "skip_when_no_definition_pages": True,
            "untraced_threshold": 0.3,
        },
    },
}
```

`SECTIONS` 是一个列表，每个元素定义一个 section 的名称、char floor、content markers：

```python
SECTIONS = [
    SectionSpec(
        name="核心速览",
        min_chars=300,
        content_markers=["tldr_with_numbers", "mental_model", "mechanism_one_line"],
    ),
    SectionSpec(
        name="方法详解",
        min_chars=1500,
        content_markers=["numerical_example", "pseudocode", "confusion_pairs"],
    ),
    # ...
]
```

### 派生关系

```
output_schema.py
    │
    ├─→ gates.py
    │     H1: schema.frontmatter.required_fields["baselines"].min_items
    │     H2: schema.gates["H2"].subsection_regex (含字母约束)
    │     H3: schema.body.sections[i].min_chars
    │     H5: schema.frontmatter.required_fields["tldr"].min_numbers
    │         + fallback: 查 body ##### TL;DR section
    │     H6: schema.body.heading_levels + code_blocks_exempt
    │     H8: schema.gates["H8"].skip_when_no_definition_pages
    │     H9: schema.body.sections[i].content_markers
    │
    ├─→ prompt_builder.py
    │     gates_to_constraints() 从 schema 生成:
    │       "YAML frontmatter 的 tldr 字段必须包含 ≥2 个量化数字"
    │       "主标题 h4，子标题 h5，代码块内 # 注释不受限"
    │
    └─→ registry.py
          _SUBSECTION_RE 从 schema.gates["H2"].subsection_regex 读取
```

### 具体修复

| Bug | 改什么 | 怎么改 |
|-----|--------|--------|
| H2 假小节 | `registry.py` `_SUBSECTION_RE` | 正则加 `[A-Za-z]` 约束，值从 schema 读 |
| H5 字段错位 | `gates.py` `check_tldr_numbers` | 先查 FM `tldr`，没有则 fallback 到 body `##### TL;DR` section 文本 |
| H5 writer 侧 | `prompt_builder.py` | 约束文本明确说"写进 YAML frontmatter 的 tldr 字段" |
| H6 代码块 | `gates.py` `check_heading_levels` | 扫描前剥离 fenced code blocks |
| H8 退化 | `gates.py` `check_number_fingerprint` | `source_numbers` 为空时返回 `{passed: True, skipped: True}` |

### 集成测试

新增 `tests/test_gates_integration.py`，包含一份满足 schema 的完整 merged.md fixture（含 YAML frontmatter with tldr、h4/h5 headings、代码块、markdown 表格），跑全部 H1-H10 gate 验证通过。

### 不改的部分

- `DEFAULT_TEMPLATE` 不变（写作指导，非格式规范）
- Writer auto-split 逻辑不变
- Merge/classify/save 流程不变
- 7 个章节结构不变
- Fixer 流程不变（但修完 gate 后大部分情况不会触发）

### 改动文件

| 文件 | 改动类型 |
|------|---------|
| **新增** `src/deepaper/output_schema.py` | Schema 定义 |
| `src/deepaper/gates.py` | 从 schema 读参数，修 H2/H5/H6/H8 |
| `src/deepaper/registry.py` | `_SUBSECTION_RE` 从 schema 读 |
| `src/deepaper/prompt_builder.py` | `gates_to_constraints()` 从 schema 生成约束 |
| `tests/test_gates.py` | 更新现有 gate 单测 |
| **新增** `tests/test_gates_integration.py` | 集成测试 fixture |

### 预期效果

Gate bug 修复后：
- H2/H5/H6/H8 在正常 writer 输出上通过 → fixer 不触发 → 省 ~500s + 111K tokens
- 不再产生附录 slop 和表格格式破坏
- 总耗时从 ~27 min 降到 ~19 min（去掉 fixer 阶段）
