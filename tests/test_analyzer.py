"""Tests for paper_manager.analyzer module."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_config():
    cfg = MagicMock()
    return cfg


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestGetPageCount:
    def test_get_page_count(self, tmp_path: Path):
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_bytes(b"%PDF-1.4 placeholder")

        mock_page = MagicMock()
        mock_pdf = MagicMock()
        mock_pdf.pages = [mock_page, mock_page, mock_page]
        mock_pdf.__enter__ = lambda s: mock_pdf
        mock_pdf.__exit__ = MagicMock(return_value=False)

        with patch("paper_manager.analyzer.pdfplumber.open", return_value=mock_pdf):
            from paper_manager.analyzer import get_page_count
            count = get_page_count(pdf_path)

        assert count == 3


class TestAnalyzePaper:
    def test_analyze_paper_uses_text_mode_for_small_paper(self, tmp_path: Path):
        """analyze_paper extracts text and sends to Claude CLI."""
        pdf_path = tmp_path / "small.pdf"
        pdf_path.write_bytes(b"%PDF-1.4 placeholder")

        expected_analysis = {
            "research_question": "How does X work?",
            "background": "Context here.",
            "method": "We do Y.",
            "results": "Z% improvement.",
            "conclusions": "X works well.",
            "keywords": ["ml", "nlp"],
        }

        with (
            patch("paper_manager.analyzer.extract_text", return_value="paper text here"),
            patch("paper_manager.analyzer._call_claude", return_value=json.dumps(expected_analysis)) as mock_call,
        ):
            from paper_manager.analyzer import analyze_paper
            result = analyze_paper(pdf_path, "Analyze this paper.", _make_config())

        # Verify prompt included paper text
        prompt_sent = mock_call.call_args[0][0]
        assert "paper text here" in prompt_sent

        assert result == expected_analysis

    def test_analyze_paper_uses_text_mode_for_large_paper(self, tmp_path: Path):
        """Large paper text is truncated."""
        pdf_path = tmp_path / "large.pdf"
        pdf_path.write_bytes(b"%PDF-1.4 placeholder")

        expected_analysis = {
            "research_question": "How does X work?",
            "background": "Context here.",
            "method": "We do Y.",
            "results": "Z% improvement.",
            "conclusions": "X works well.",
            "keywords": ["ml", "nlp"],
        }

        long_text = "x" * 100000  # exceeds 80000 char limit

        with (
            patch("paper_manager.analyzer.extract_text", return_value=long_text),
            patch("paper_manager.analyzer._call_claude", return_value=json.dumps(expected_analysis)) as mock_call,
        ):
            from paper_manager.analyzer import analyze_paper
            result = analyze_paper(pdf_path, "Analyze this paper.", _make_config())

        # Verify text was truncated in the prompt
        prompt_sent = mock_call.call_args[0][0]
        assert "[...truncated...]" in prompt_sent

        assert result == expected_analysis

    def test_analyze_paper_returns_dict(self, tmp_path: Path):
        """analyze_paper returns the parsed dict with expected keys."""
        pdf_path = tmp_path / "paper.pdf"
        pdf_path.write_bytes(b"%PDF-1.4 placeholder")

        expected = {
            "research_question": "RQ",
            "background": "BG",
            "method": "M",
            "results": "R",
            "conclusions": "C",
            "keywords": ["a", "b"],
            "limitations": None,
            "future_work": "More work",
            "venue": "NeurIPS 2023",
        }

        with (
            patch("paper_manager.analyzer.extract_text", return_value="some text"),
            patch("paper_manager.analyzer._call_claude", return_value=json.dumps(expected)),
        ):
            from paper_manager.analyzer import analyze_paper
            result = analyze_paper(pdf_path, "prompt", _make_config())

        assert isinstance(result, dict)
        for key in ("research_question", "background", "method", "results", "conclusions", "keywords"):
            assert key in result


class TestClassifyPaper:
    def test_classify_paper_returns_category(self, tmp_path: Path):
        """classify_paper returns a category string from Claude CLI response."""
        analysis = {
            "executive_summary": "This paper presents a new pretraining method for LLMs.",
            "keywords": ["pretraining", "scaling law", "LLM"],
        }
        categories_path = tmp_path / "categories.md"
        categories_path.write_text("# Categories\nllm/pretraining — pretraining methods", encoding="utf-8")

        cfg = _make_config()
        cfg.templates_path = tmp_path

        with patch("paper_manager.analyzer._call_claude", return_value='{"category": "llm/pretraining"}') as mock_call:
            from paper_manager.analyzer import classify_paper
            result = classify_paper(analysis, cfg)

        assert result == "llm/pretraining"
        assert "pretraining" in mock_call.call_args[0][0]

    def test_classify_paper_falls_back_to_misc_on_failure(self, tmp_path: Path):
        """classify_paper returns 'misc' when Claude CLI fails."""
        analysis = {
            "executive_summary": "Some paper.",
            "keywords": ["foo"],
        }
        categories_path = tmp_path / "categories.md"
        categories_path.write_text("# Categories", encoding="utf-8")

        cfg = _make_config()
        cfg.templates_path = tmp_path

        with patch("paper_manager.analyzer._call_claude", side_effect=RuntimeError("error")):
            from paper_manager.analyzer import classify_paper
            result = classify_paper(analysis, cfg)

        assert result == "misc"

    def test_classify_paper_falls_back_to_misc_when_no_categories_file(self, tmp_path: Path):
        """classify_paper returns 'misc' when categories.md does not exist."""
        analysis = {
            "executive_summary": "Some paper.",
            "keywords": ["foo"],
        }

        cfg = _make_config()
        cfg.templates_path = tmp_path  # no categories.md here

        from paper_manager.analyzer import classify_paper
        result = classify_paper(analysis, cfg)

        assert result == "misc"


class TestGenerateTags:
    def test_generate_tags_returns_list(self):
        """generate_tags returns a list of tag strings from Claude CLI response."""
        analysis = {
            "research_question": "How does attention work?",
            "method": "We apply self-attention.",
            "keywords": ["transformer", "attention", "nlp"],
        }
        expected_tags = ["NLP", "transformer", "deep-learning"]

        with patch("paper_manager.analyzer._call_claude", return_value=json.dumps({"tags": expected_tags})) as mock_call:
            from paper_manager.analyzer import generate_tags
            tags = generate_tags(analysis, _make_config())

        assert isinstance(tags, list)
        assert tags == expected_tags

        # Verify keywords were included in the prompt
        prompt_sent = mock_call.call_args[0][0]
        assert "transformer" in prompt_sent
        assert "attention" in prompt_sent
