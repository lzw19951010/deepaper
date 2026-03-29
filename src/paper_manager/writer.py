"""Markdown note writer with Obsidian-compatible YAML frontmatter."""
from __future__ import annotations

import re
from pathlib import Path

import yaml


def sanitize_filename(title: str, arxiv_id: str = "") -> str:
    """Convert a paper title into a safe, readable filename stem.

    Args:
        title: Paper title to sanitize.
        arxiv_id: Fallback ID if sanitization yields an empty string.

    Returns:
        A lowercase, hyphen-separated filename stem (no extension).
    """
    result = title.lower()

    # Replace spaces with hyphens
    result = result.replace(" ", "-")

    # Remove only filesystem-unsafe chars: / \ : * ? " < > |
    result = re.sub(r'[/\\:*?"<>|]', "", result)

    # Remove leading/trailing hyphens and whitespace
    result = result.strip("-").strip()

    # Truncate to 80 characters at a word boundary
    if len(result) > 80:
        truncated = result[:80]
        # Find last hyphen to avoid cutting mid-word
        last_hyphen = truncated.rfind("-")
        if last_hyphen > 0:
            truncated = truncated[:last_hyphen]
        result = truncated.strip("-")

    if not result:
        return arxiv_id

    return result


def find_existing(arxiv_id: str, papers_dir: Path) -> Path | None:
    """Find an existing note file with a matching arxiv_id in its frontmatter.

    Args:
        arxiv_id: The arxiv ID to search for.
        papers_dir: Root directory to search recursively.

    Returns:
        Path to the matching file, or None if not found.
    """
    for md_file in papers_dir.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
        except OSError:
            continue

        # Extract YAML frontmatter between first --- and second ---
        if not content.startswith("---"):
            continue

        end_idx = content.find("---", 3)
        if end_idx == -1:
            continue

        frontmatter_text = content[3:end_idx]
        try:
            fm = yaml.safe_load(frontmatter_text)
        except yaml.YAMLError:
            continue

        if isinstance(fm, dict) and str(fm.get("arxiv_id", "")) == arxiv_id:
            return md_file

    return None


def update_frontmatter(md_path: Path, new_frontmatter: dict) -> None:
    """Replace the YAML frontmatter of a markdown file, preserving the body.

    Args:
        md_path: Path to the markdown file to update.
        new_frontmatter: New frontmatter dict to serialize and write.
    """
    content = md_path.read_text(encoding="utf-8")

    new_yaml = yaml.dump(
        new_frontmatter, default_flow_style=False, allow_unicode=True
    )
    new_block = f"---\n{new_yaml}---"

    if content.startswith("---"):
        end_idx = content.find("---", 3)
        if end_idx != -1:
            # Preserve everything after the closing ---
            body = content[end_idx + 3:]
            result = new_block + body
        else:
            # Malformed: no closing ---, prepend new block
            result = new_block + "\n\n" + content
    else:
        # No frontmatter: prepend
        result = new_block + "\n\n" + content

    md_path.write_text(result, encoding="utf-8")


def write_paper_note(
    analysis: dict,
    metadata: dict,
    tags: list[str],
    output_dir: Path,
    force: bool = False,
) -> Path:
    """Write a paper analysis as an Obsidian-compatible markdown note.

    Args:
        analysis: Analysis result dict (research_question, background, etc.).
        metadata: Paper metadata dict (title, authors, date, arxiv_id, url).
        tags: List of tag strings for the frontmatter.
        output_dir: Root directory for paper notes (year subdirs are created here).
        force: If True, overwrite an existing note for the same arxiv_id.

    Returns:
        Path to the written markdown file.

    Raises:
        FileExistsError: If a note for this arxiv_id already exists and force=False.
    """
    year = metadata["date"][:4]
    sanitized = sanitize_filename(metadata["title"], metadata["arxiv_id"])
    dest = output_dir / year / f"{sanitized}.md"

    existing = find_existing(metadata["arxiv_id"], output_dir)

    if existing is not None:
        if not force:
            raise FileExistsError(
                f"A note for arxiv_id {metadata['arxiv_id']!r} already exists: {existing}"
            )

    frontmatter: dict = {
        "title": metadata["title"],
        "authors": metadata["authors"],
        "date": metadata["date"],
        "arxiv_id": metadata["arxiv_id"],
        "url": metadata["url"],
        "venue": analysis.get("venue"),
        "keywords": analysis.get("keywords", []),
        "tags": tags,
        "status": analysis.get("status", "complete"),
    }

    limitations = analysis.get("limitations") or "_Not discussed_"
    future_work = analysis.get("future_work") or "_Not discussed_"

    body = (
        f"## Research Question\n{analysis['research_question']}\n\n"
        f"## Background\n{analysis['background']}\n\n"
        f"## Method\n{analysis['method']}\n\n"
        f"## Results\n{analysis['results']}\n\n"
        f"## Conclusions\n{analysis['conclusions']}\n\n"
        f"## Limitations\n{limitations}\n\n"
        f"## Future Work\n{future_work}\n"
    )

    yaml_content = yaml.dump(
        frontmatter, default_flow_style=False, allow_unicode=True
    )
    full_content = f"---\n{yaml_content}---\n\n{body}"

    if existing is not None and force:
        update_frontmatter(existing, frontmatter)
        # Rewrite the body section too
        existing_content = existing.read_text(encoding="utf-8")
        # Find end of frontmatter block
        fm_end = existing_content.find("---", 3)
        if fm_end != -1:
            new_content = existing_content[: fm_end + 3] + "\n\n" + body
        else:
            new_content = full_content
        existing.write_text(new_content, encoding="utf-8")
        return existing

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(full_content, encoding="utf-8")
    return dest
