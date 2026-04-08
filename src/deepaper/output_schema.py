"""Output Schema — single source of truth for merged.md format.

Both gates.py and prompt_builder.py derive their checks/constraints from this
schema. When the format changes, update HERE — both sides auto-adapt.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class FieldSpec:
    """Specification for a YAML frontmatter field."""
    type: str  # "str", "str_or_null", "list"
    required: bool = True
    min_items: int = 0  # for list type
    min_numbers: int = 0  # for str type: minimum numeric values required


@dataclass
class SectionSpec:
    """Specification for a body section."""
    name: str
    min_chars: int = 300
    content_markers: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Frontmatter fields
# ---------------------------------------------------------------------------

FRONTMATTER_FIELDS: dict[str, FieldSpec] = {
    "venue": FieldSpec(type="str_or_null"),
    "publication_type": FieldSpec(type="str"),
    "tldr": FieldSpec(type="str", min_numbers=2),
    "core_contribution": FieldSpec(type="str"),
    "baselines": FieldSpec(type="list", min_items=2),
    "datasets": FieldSpec(type="list", min_items=1),
    "metrics": FieldSpec(type="list", min_items=1),
    "keywords": FieldSpec(type="list", min_items=5),
    "code_url": FieldSpec(type="str_or_null"),
}

# ---------------------------------------------------------------------------
# Body structure
# ---------------------------------------------------------------------------

# Allowed heading levels in the body (after frontmatter)
HEADING_SECTION_LEVEL = 4       # ####
HEADING_SUBSECTION_LEVEL = 5    # #####
HEADING_DETAIL_LEVEL = 6        # ######
HEADING_FORBIDDEN = [1, 2, 3, 7]

# Code blocks (```...```) are exempt from heading-level checks.
# Python comments like `# comment` inside code blocks are NOT headings.
CODE_BLOCKS_EXEMPT_FROM_HEADING_CHECK = True

# Section definitions with char floors and H9 content markers
SECTIONS: list[SectionSpec] = [
    SectionSpec(
        name="动机与第一性原理",
        min_chars=400,
        content_markers=["causal_chain"],
    ),
    SectionSpec(
        name="核心速览",
        min_chars=300,
        content_markers=["tldr_with_numbers", "mental_model", "mechanism_one_line"],
    ),
    SectionSpec(
        name="方法详解",
        min_chars=1500,
        content_markers=["numerical_example", "pseudocode", "confusion_pairs", "flowchart"],
    ),
    SectionSpec(
        name="实验与归因",
        min_chars=800,
        content_markers=["attribution_analysis"],
    ),
    SectionSpec(
        name="专家批判",
        min_chars=500,
        content_markers=["hidden_costs_with_numbers"],
    ),
    SectionSpec(
        name="机制迁移分析",
        min_chars=600,
        content_markers=["mechanism_table", "ancestors"],
    ),
    SectionSpec(
        name="背景知识补充",
        min_chars=200,
        content_markers=[],
    ),
]

# Canonical section order
SECTION_ORDER = [s.name for s in SECTIONS]

# Char floors dict (for backward compat with gates.py)
CHAR_FLOORS: dict[str, int] = {s.name: s.min_chars for s in SECTIONS}

# ---------------------------------------------------------------------------
# Gate-specific parameters
# ---------------------------------------------------------------------------

# H2: Structural coverage
# Subsection regex must require at least one letter after the number,
# to avoid matching table cell values like "96.2 49.2".
H2_SUBSECTION_REGEX = r"^((?:[1-9]|1\d|20)\.\d{1,2}\.?\s+[A-Za-z].*)$"
H2_MIN_COVERAGE = 0.6

# H8: Number fingerprint
# When no table definition pages are found, H8 cannot perform cross-validation.
# Rather than producing a false-negative (100% untraced), skip gracefully.
H8_SKIP_WHEN_NO_DEFINITION_PAGES = True
H8_UNTRACED_THRESHOLD = 0.3
H8_TOLERANCE = 0.15
