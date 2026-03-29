"""Tests for paper_manager.search."""
from __future__ import annotations

from pathlib import Path

import chromadb
import pytest

from paper_manager.search import (
    chunk_document,
    index_paper,
    parse_frontmatter,
    reindex_all,
    search_papers,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_collection() -> chromadb.Collection:
    """Return a fresh in-memory ChromaDB collection for each test."""
    client = chromadb.EphemeralClient()
    return client.get_or_create_collection("test_papers")


def _write_paper(tmp_path: Path, filename: str, content: str) -> Path:
    p = tmp_path / filename
    p.write_text(content, encoding="utf-8")
    return p


PAPER_1 = """\
---
arxiv_id: "2301.00001"
title: "Attention Is All You Need"
tags:
  - transformers
  - nlp
---

## Introduction

The transformer architecture revolutionised natural language processing.

## Method

We propose a novel self-attention mechanism that replaces recurrence entirely.
"""

PAPER_2 = """\
---
arxiv_id: "2301.00002"
title: "Deep Residual Learning"
tags:
  - deep-learning
  - vision
---

## Introduction

Residual connections allow training of very deep networks.

## Experiments

We evaluate on ImageNet and achieve state-of-the-art results.
"""


# ---------------------------------------------------------------------------
# parse_frontmatter
# ---------------------------------------------------------------------------

def test_parse_frontmatter_with_yaml():
    md = "---\narxiv_id: '2301.00001'\ntitle: 'My Paper'\n---\n\nBody text here."
    fm, body = parse_frontmatter(md)
    assert fm["arxiv_id"] == "2301.00001"
    assert fm["title"] == "My Paper"
    assert "Body text here." in body


def test_parse_frontmatter_without_yaml():
    md = "# Just a heading\n\nSome content without frontmatter."
    fm, body = parse_frontmatter(md)
    assert fm == {}
    assert body == md


# ---------------------------------------------------------------------------
# chunk_document
# ---------------------------------------------------------------------------

def test_chunk_document_by_headers():
    body = "## Section1\n\nContent of section one.\n\n## Section2\n\nContent of section two."
    chunks = chunk_document(body)
    assert len(chunks) == 2
    assert "Section1" in chunks[0]
    assert "Section2" in chunks[1]


def test_chunk_document_no_headers():
    body = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
    chunks = chunk_document(body)
    assert len(chunks) == 3
    assert chunks[0] == "First paragraph."
    assert chunks[1] == "Second paragraph."
    assert chunks[2] == "Third paragraph."


# ---------------------------------------------------------------------------
# index_paper
# ---------------------------------------------------------------------------

def test_index_paper_creates_entries(tmp_path: Path):
    md_path = _write_paper(tmp_path, "2301.00001.md", PAPER_1)
    collection = _make_collection()

    index_paper(md_path, collection)

    results = collection.get(where={"arxiv_id": {"$eq": "2301.00001"}})
    assert len(results["ids"]) >= 1
    # Verify metadata fields are stored
    meta = results["metadatas"][0]
    assert meta["arxiv_id"] == "2301.00001"
    assert meta["title"] == "Attention Is All You Need"


# ---------------------------------------------------------------------------
# search_papers
# ---------------------------------------------------------------------------

def test_search_papers_returns_results(tmp_path: Path):
    md1 = _write_paper(tmp_path, "2301.00001.md", PAPER_1)
    md2 = _write_paper(tmp_path, "2301.00002.md", PAPER_2)
    collection = _make_collection()

    index_paper(md1, collection)
    index_paper(md2, collection)

    results = search_papers("transformer self-attention nlp", collection, n_results=5)

    assert len(results) >= 1
    # Each result must have the required keys
    for r in results:
        assert "title" in r
        assert "arxiv_id" in r
        assert "score" in r
        assert "matched_section" in r
        assert "tags" in r


# ---------------------------------------------------------------------------
# reindex_all
# ---------------------------------------------------------------------------

def test_reindex_all_counts_papers(tmp_path: Path):
    papers_dir = tmp_path / "papers"
    papers_dir.mkdir()

    for i in range(3):
        content = (
            f"---\narxiv_id: '2301.0000{i}'\ntitle: 'Paper {i}'\n---\n\n"
            f"## Introduction\n\nContent for paper {i}.\n"
        )
        (papers_dir / f"paper{i}.md").write_text(content, encoding="utf-8")

    collection = _make_collection()
    count = reindex_all(papers_dir, collection)

    assert count == 3


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def test_search_deduplicates_by_arxiv_id(tmp_path: Path):
    # Paper with many sections → multiple chunks
    body_sections = "\n\n".join(
        f"## Section {i}\n\nContent about transformers and attention in section {i}."
        for i in range(6)
    )
    content = (
        "---\narxiv_id: '2301.00001'\ntitle: 'Multi-Chunk Paper'\ntags:\n  - transformers\n---\n\n"
        + body_sections
    )
    md_path = _write_paper(tmp_path, "2301.00001.md", content)
    collection = _make_collection()

    index_paper(md_path, collection)

    # Request more results than chunks to stress dedup
    results = search_papers("transformers attention", collection, n_results=10)

    arxiv_ids = [r["arxiv_id"] for r in results]
    # All results belong to the same paper — deduplicated to exactly 1
    assert len(results) == 1
    assert arxiv_ids[0] == "2301.00001"
