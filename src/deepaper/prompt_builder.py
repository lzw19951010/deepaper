"""Prompt generation: template parsing, auto-split, gate contract injection."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from deepaper.output_schema import (
    FRONTMATTER_FIELDS,
    HEADING_SECTION_LEVEL,
    HEADING_SUBSECTION_LEVEL,
    SECTION_ORDER as _SCHEMA_SECTION_ORDER,
)

# Canonical section names and their order (matches DEFAULT_TEMPLATE)
SECTION_ORDER = _SCHEMA_SECTION_ORDER

# Sections that may benefit from PDF table pages for verification
VISUAL_SECTIONS = ["技术精要"]

# Writer task definitions for the v2 4-section layout.
# Fixed assignment: paper length does not affect split.
WRITER_ASSIGNMENTS: list[tuple[str, list[str], bool]] = [
    # (writer_name, sections, needs_pdf_pages)
    ("writer-overview", ["核心速览", "机制迁移"], False),
    ("writer-principle", ["第一性原理分析"], False),
    ("writer-technical", ["技术精要"], True),
]

# Section heading pattern in DEFAULT_TEMPLATE: **## 中文名 (English Name)**
_TEMPLATE_SECTION_RE = re.compile(
    r"^\*\*##\s+(.+?)\s*\((.+?)\)\*\*\s*$", re.MULTILINE
)


@dataclass
class WriterTask:
    name: str
    sections: list
    needs_pdf_pages: bool = False


def extract_system_role(template: str) -> str:
    """Extract the Role: line from the template header."""
    for line in template.split("\n"):
        if line.startswith("Role:"):
            return line
    return ""


def extract_frontmatter_spec(template: str) -> str:
    """Extract the YAML frontmatter specification block from the template."""
    # Look for the ``` block that contains venue:/baselines:/datasets:
    blocks = re.findall(r"```\s*\n(.*?)\n```", template, re.DOTALL)
    for block in blocks:
        if "baselines:" in block and ("venue:" in block or "tldr:" in block):
            return block
    return ""


def parse_template_sections(template: str) -> dict[str, str]:
    """Split DEFAULT_TEMPLATE into {short_chinese_name: section_text}.

    Parses the **## 中文名 (English)** headings and extracts content
    between consecutive headings.
    """
    sections: dict[str, str] = {}

    matches = list(_TEMPLATE_SECTION_RE.finditer(template))
    if not matches:
        return sections

    for i, m in enumerate(matches):
        chinese_name = m.group(1).strip()
        # Map to canonical name
        short_name = chinese_name
        for canonical in SECTION_ORDER:
            if canonical in chinese_name:
                short_name = canonical
                break

        start = m.end()
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end_marker = template.find("## 注意事项", start)
            end = end_marker if end_marker > 0 else len(template)

        content = template[start:end].strip()
        content = re.sub(r"^---\s*", "", content)
        content = re.sub(r"\s*---\s*$", "", content)
        sections[short_name] = content

    return sections


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
    """Generate a complete prompt for one Writer agent."""
    parts = []

    # 1. System role (every writer gets this)
    parts.append(system_role)
    parts.append("")

    # 2. Gate contract (before section instructions)
    if constraints:
        parts.append(constraints)
        parts.append("")

    # 3. Figure contexts (broadcast to all writers)
    parts.append("## 灵魂图上下文（所有 Writer 共享）\n")
    if figure_contexts:
        parts.append(f"```json\n{json.dumps(figure_contexts, ensure_ascii=False, indent=2)}\n```\n")
        parts.append("在描述方法和实验时引用这些核心图，用 Figure N 格式。\n")
    else:
        parts.append("（本论文未检测到核心图）\n")

    # 4. Section instructions (verbatim from DEFAULT_TEMPLATE)
    parts.append("## 你的章节\n")
    parts.append("以下指令直接来自分析模板，请严格遵循。\n")
    for sec_name in task.sections:
        sec_text = template_sections.get(sec_name, "")
        parts.append(f"**#### {sec_name}**\n")
        parts.append(sec_text)
        parts.append("")

    # 5. Format rules
    parts.append("## 格式规则")
    parts.append("- 主标题: #### (h4)")
    parts.append("- 子标题: ##### (h5)")
    parts.append("- 禁止添加 '深度分析'、'Part' 等总标题")
    parts.append("- 禁止在章节间添加 `---` 分隔线")
    first_section = task.sections[0]
    if first_section == "核心速览":
        parts.append("- 文件开头必须是 `---`（YAML frontmatter 开始）")
    else:
        parts.append(f"- 文件开头直接是 `#### {first_section}`")
    parts.append("")

    # 6. Inputs
    parts.append("## 输入")
    parts.append(f"- 结构化笔记: {run_dir}/notes.md（先读这个）")
    parts.append(f"- 全文检索: {run_dir}/text.txt")
    if task.needs_pdf_pages and table_def_pages:
        parts.append(f"- PDF 表格验证页: {pdf_path}（仅读这些页: {table_def_pages}）")
    parts.append("")

    # 6b. Read strategy — generate exact Read commands
    if file_info:
        parts.append("## 读取策略（严格执行，禁止修改）")
        parts.append("")
        chunk = 2000
        for label, fpath_suffix, total in [
            ("notes.md", "notes.md", file_info.get("notes_lines", 0)),
            ("text.txt", "text.txt", file_info.get("text_lines", 0)),
        ]:
            if total <= 0:
                continue
            fpath = f"{run_dir}/{fpath_suffix}"
            if total <= chunk:
                parts.append(f'- `Read(file_path="{fpath}")`')
            else:
                n = max(1, -(-total // chunk))
                for i in range(n):
                    offset = i * chunk
                    limit = min(chunk, total - offset)
                    parts.append(f'- `Read(file_path="{fpath}", offset={offset}, limit={limit})`')
        parts.append("")
        parts.append("按以上顺序逐条执行，禁止拆分、合并或跳过。读完所有内容后再开始写作。")
        parts.append("")

    # 7. Output
    output_file = f"{run_dir}/part_{task.name.replace('writer-', '')}.md"
    parts.append("## 输出")
    parts.append(f"写入文件: `{output_file}`")
    parts.append("写完后对照上方「质量合同」逐项自检，不达标立即补充。")

    return "\n".join(parts)


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
