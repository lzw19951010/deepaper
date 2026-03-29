"""Shared test fixtures for paper-manager tests."""
from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import MagicMock

import chromadb
import pytest


@pytest.fixture(autouse=True)
def _reset_chromadb_ephemeral_state() -> None:
    """Clear the ChromaDB EphemeralClient shared in-process cache before each test.

    EphemeralClient instances share a module-level system singleton, so data
    added in one test leaks into the next.  clear_system_cache() resets that
    singleton, guaranteeing every test starts with a clean in-memory store.
    """
    chromadb.EphemeralClient().clear_system_cache()


@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    """Create a minimal project directory structure for testing."""
    (tmp_path / "papers").mkdir()
    (tmp_path / "templates").mkdir()
    (tmp_path / "tmp").mkdir()
    (tmp_path / "src" / "paper_manager").mkdir(parents=True)

    # Write a minimal config.yaml
    (tmp_path / "config.yaml").write_text(
        "anthropic_api_key: test-key\n"
        "model: claude-opus-4-6\n"
        "tag_model: claude-opus-4-6\n"
    )

    # Write a minimal template
    (tmp_path / "templates" / "default.md").write_text(
        "Analyze this paper and extract key information.\n"
    )

    return tmp_path


@pytest.fixture
def sample_metadata() -> dict:
    return {
        "arxiv_id": "2301.00001",
        "title": "Test Paper: A Survey of Testing",
        "authors": ["Alice Smith", "Bob Jones"],
        "date": "2023-01-01",
        "abstract": "This paper surveys testing methodologies.",
        "categories": ["cs.SE"],
        "url": "https://arxiv.org/abs/2301.00001",
    }


@pytest.fixture
def sample_analysis() -> dict:
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
