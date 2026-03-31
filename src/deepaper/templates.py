"""Prompt template loading and rendering."""
from __future__ import annotations

from pathlib import Path


def load_template(name: str, templates_dir: Path) -> str:
    """Load a prompt template by name from the templates directory.

    Args:
        name: Template name (without .md extension).
        templates_dir: Directory containing template files.

    Returns:
        Template content as a string.

    Raises:
        FileNotFoundError: If the template file does not exist.
    """
    template_path = templates_dir / f"{name}.md"
    if not template_path.exists():
        raise FileNotFoundError(
            f"Template '{name}' not found. Expected file: {template_path}\n"
            f"Available templates: {[p.stem for p in templates_dir.glob('*.md')]}"
        )
    return template_path.read_text(encoding="utf-8")


def render_prompt(template: str, metadata: dict) -> str:
    """Prepend paper metadata as a context header to the template.

    Args:
        template: Raw template text.
        metadata: Paper metadata dict with keys: title, authors, date,
                  arxiv_id, categories.

    Returns:
        Combined string with metadata header followed by the template.
    """
    authors_str = ", ".join(metadata.get("authors", []))
    categories_str = ", ".join(metadata.get("categories", []))

    header = (
        "Paper Metadata:\n"
        f"- Title: {metadata.get('title', '')}\n"
        f"- Authors: {authors_str}\n"
        f"- Date: {metadata.get('date', '')}\n"
        f"- arXiv ID: {metadata.get('arxiv_id', '')}\n"
        f"- Categories: {categories_str}\n"
    )

    return f"{header}\n{template}"
