"""Tests for frontmatter field preservation."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

PAPERS_DIR = Path("papers")


def _find_paper_mds():
    """Find all paper .md files with YAML frontmatter."""
    if not PAPERS_DIR.exists():
        return []
    results = []
    for md in PAPERS_DIR.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        if text.startswith("---"):
            results.append(md)
    return results


@pytest.mark.skipif(not PAPERS_DIR.exists(), reason="no papers dir")
def test_all_papers_have_arxiv_id():
    """Every paper markdown must have arxiv_id in frontmatter."""
    papers = _find_paper_mds()
    if not papers:
        pytest.skip("no papers found")
    missing = []
    for p in papers:
        text = p.read_text(encoding="utf-8")
        end = text.find("---", 3)
        if end < 0:
            continue
        fm = yaml.safe_load(text[3:end]) or {}
        if not fm.get("arxiv_id"):
            missing.append(str(p))
    assert not missing, f"Papers missing arxiv_id: {missing}"
