"""Tests for paper_manager.writer module."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from paper_manager.writer import (
    find_existing,
    sanitize_filename,
    update_frontmatter,
    write_paper_note,
)


# ---------------------------------------------------------------------------
# Inline fixtures (mirrors conftest.py fixtures as plain dicts for use below)
# ---------------------------------------------------------------------------

def _sample_metadata() -> dict:
    return {
        "arxiv_id": "2301.00001",
        "title": "Test Paper: A Survey of Testing",
        "authors": ["Alice Smith", "Bob Jones"],
        "date": "2023-01-01",
        "abstract": "This paper surveys testing methodologies.",
        "categories": ["cs.SE"],
        "url": "https://arxiv.org/abs/2301.00001",
    }


def _sample_analysis() -> dict:
    return {
        "research_question": "How can we improve software testing?",
        "background": "Testing is critical for software quality.",
        "method": "We propose a new testing framework.",
        "results": "Our approach improves test coverage by 30%.",
        "conclusions": "The framework is effective and efficient.",
        "limitations": "Only evaluated on Python projects.",
        "future_work": "Extend to other languages.",
        "venue": "ICSE 2023",
        "keywords": ["testing", "software quality", "automation"],
    }


# ---------------------------------------------------------------------------
# sanitize_filename
# ---------------------------------------------------------------------------

def test_sanitize_filename_basic() -> None:
    assert sanitize_filename("Attention Is All You Need") == "attention-is-all-you-need"


def test_sanitize_filename_special_chars() -> None:
    result = sanitize_filename('No/Bad\\Chars:Here*Or?Here"And<These>Too|Done')
    # None of the unsafe chars should survive
    for ch in r'/\:*?"<>|':
        assert ch not in result
    # Content words should still be present
    assert "no" in result
    assert "bad" in result


def test_sanitize_filename_unicode_preserved() -> None:
    # Chinese characters
    result = sanitize_filename("深度学习 Deep Learning")
    assert "深度学习" in result
    # Accented characters
    result2 = sanitize_filename("Réseau de Neurones")
    assert "é" in result2


def test_sanitize_filename_empty_fallback() -> None:
    # A title consisting entirely of unsafe chars should fall back to arxiv_id
    result = sanitize_filename('/:*?"<>|\\', arxiv_id="2301.99999")
    assert result == "2301.99999"


def test_sanitize_filename_truncation() -> None:
    long_title = "word " * 40  # 200 characters
    result = sanitize_filename(long_title)
    assert len(result) <= 80
    # Should not end with a hyphen (truncated at word boundary)
    assert not result.endswith("-")


# ---------------------------------------------------------------------------
# find_existing
# ---------------------------------------------------------------------------

def test_find_existing_finds_match(tmp_path: Path) -> None:
    papers_dir = tmp_path / "papers"
    papers_dir.mkdir()
    note = papers_dir / "some-paper.md"
    note.write_text(
        "---\narxiv_id: 2301.00001\ntitle: Some Paper\n---\n\n## Body\nContent here.\n",
        encoding="utf-8",
    )

    found = find_existing("2301.00001", papers_dir)
    assert found == note


def test_find_existing_returns_none(tmp_path: Path) -> None:
    papers_dir = tmp_path / "papers"
    papers_dir.mkdir()
    note = papers_dir / "other-paper.md"
    note.write_text(
        "---\narxiv_id: 9999.99999\ntitle: Other Paper\n---\n\n## Body\n",
        encoding="utf-8",
    )

    found = find_existing("2301.00001", papers_dir)
    assert found is None


# ---------------------------------------------------------------------------
# update_frontmatter
# ---------------------------------------------------------------------------

def test_update_frontmatter_preserves_body(tmp_path: Path) -> None:
    md = tmp_path / "paper.md"
    original_body = "\n## Notes\nMy hand-written notes go here.\n\nImportant insight!\n"
    md.write_text(
        f"---\narxiv_id: 2301.00001\ntitle: Old Title\n---{original_body}",
        encoding="utf-8",
    )

    new_fm = {"arxiv_id": "2301.00001", "title": "New Title", "status": "complete"}
    update_frontmatter(md, new_fm)

    updated = md.read_text(encoding="utf-8")

    # Body must be unchanged
    assert original_body in updated

    # New frontmatter must be present
    fm_end = updated.find("---", 3)
    fm_text = updated[3:fm_end]
    parsed = yaml.safe_load(fm_text)
    assert parsed["title"] == "New Title"
    assert parsed["arxiv_id"] == "2301.00001"


# ---------------------------------------------------------------------------
# write_paper_note
# ---------------------------------------------------------------------------

def test_write_paper_note_creates_file(tmp_path: Path) -> None:
    metadata = _sample_metadata()
    analysis = _sample_analysis()
    tags = ["machine-learning", "testing"]

    path = write_paper_note(analysis, metadata, tags, tmp_path)

    assert path.exists()
    content = path.read_text(encoding="utf-8")

    # Check frontmatter is valid YAML
    assert content.startswith("---")
    fm_end = content.find("---", 3)
    assert fm_end != -1
    fm = yaml.safe_load(content[3:fm_end])
    assert fm["arxiv_id"] == "2301.00001"
    assert fm["title"] == metadata["title"]
    assert fm["tags"] == tags
    assert fm["venue"] == "ICSE 2023"

    # Check year-based subdirectory
    assert path.parent.name == "2023"

    # Check body sections are present
    assert "## Research Question" in content
    assert "## Background" in content
    assert "## Method" in content
    assert "## Results" in content
    assert "## Conclusions" in content
    assert "## Limitations" in content
    assert "## Future Work" in content


def test_write_paper_note_skip_duplicate(tmp_path: Path) -> None:
    metadata = _sample_metadata()
    analysis = _sample_analysis()
    tags = ["ml"]

    write_paper_note(analysis, metadata, tags, tmp_path)

    with pytest.raises(FileExistsError) as exc_info:
        write_paper_note(analysis, metadata, tags, tmp_path)

    assert "2301.00001" in str(exc_info.value)


def test_write_paper_note_force_overwrites(tmp_path: Path) -> None:
    metadata = _sample_metadata()
    analysis = _sample_analysis()
    tags = ["ml"]

    first_path = write_paper_note(analysis, metadata, tags, tmp_path)
    assert first_path.exists()

    # Should not raise
    second_path = write_paper_note(analysis, metadata, tags, tmp_path, force=True)

    # File should still exist and contain valid frontmatter
    content = second_path.read_text(encoding="utf-8")
    fm_end = content.find("---", 3)
    fm = yaml.safe_load(content[3:fm_end])
    assert fm["arxiv_id"] == "2301.00001"
