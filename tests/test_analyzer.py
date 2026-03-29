"""Tests for paper_manager.analyzer module."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_config(api_key="test-key", model="claude-opus-4-6", tag_model="claude-opus-4-6"):
    cfg = MagicMock()
    cfg.api_key = api_key
    cfg.model = model
    cfg.tag_model = tag_model
    return cfg


def _make_tool_use_response(tool_name: str, input_data: dict):
    """Build a mock anthropic messages response with a single tool_use block."""
    block = MagicMock()
    block.type = "tool_use"
    block.name = tool_name
    block.input = input_data

    response = MagicMock()
    response.content = [block]
    return response


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestGetPageCount:
    def test_get_page_count(self, tmp_path: Path):
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_bytes(b"%PDF-1.4 placeholder")  # content doesn't matter; pdfplumber is mocked

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
    def test_analyze_paper_uses_pdf_mode_for_small_paper(self, tmp_path: Path):
        """When pages <= 100 and size <= 30 MB, content must include a base64 document block."""
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

        mock_response = _make_tool_use_response("extract_paper_analysis", expected_analysis)
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response

        with (
            patch("paper_manager.analyzer.get_page_count", return_value=10),
            patch("paper_manager.analyzer.get_file_size_mb", return_value=1.0),
            patch("paper_manager.analyzer.anthropic.Anthropic", return_value=mock_client),
        ):
            from paper_manager.analyzer import analyze_paper
            result = analyze_paper(pdf_path, "Analyze this paper.", _make_config())

        call_kwargs = mock_client.messages.create.call_args
        messages = call_kwargs.kwargs["messages"]
        user_content = messages[0]["content"]

        # Verify a document block with base64 source is present
        doc_blocks = [b for b in user_content if isinstance(b, dict) and b.get("type") == "document"]
        assert len(doc_blocks) == 1
        assert doc_blocks[0]["source"]["type"] == "base64"
        assert doc_blocks[0]["source"]["media_type"] == "application/pdf"

        assert result == expected_analysis

    def test_analyze_paper_uses_text_mode_for_large_paper(self, tmp_path: Path):
        """When page count > 100, content must be plain text (no document block)."""
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

        mock_response = _make_tool_use_response("extract_paper_analysis", expected_analysis)
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response

        with (
            patch("paper_manager.analyzer.get_page_count", return_value=150),
            patch("paper_manager.analyzer.get_file_size_mb", return_value=5.0),
            patch("paper_manager.analyzer.extract_text", return_value="paper text here"),
            patch("paper_manager.analyzer.anthropic.Anthropic", return_value=mock_client),
        ):
            from paper_manager.analyzer import analyze_paper
            result = analyze_paper(pdf_path, "Analyze this paper.", _make_config())

        call_kwargs = mock_client.messages.create.call_args
        messages = call_kwargs.kwargs["messages"]
        user_content = messages[0]["content"]

        # Verify content is a single text block (no document block)
        assert len(user_content) == 1
        assert user_content[0]["type"] == "text"
        assert "paper text here" in user_content[0]["text"]

        assert result == expected_analysis

    def test_analyze_paper_returns_dict(self, tmp_path: Path):
        """analyze_paper returns the tool input dict with expected keys."""
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

        mock_response = _make_tool_use_response("extract_paper_analysis", expected)
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response

        with (
            patch("paper_manager.analyzer.get_page_count", return_value=10),
            patch("paper_manager.analyzer.get_file_size_mb", return_value=1.0),
            patch("paper_manager.analyzer.anthropic.Anthropic", return_value=mock_client),
        ):
            from paper_manager.analyzer import analyze_paper
            result = analyze_paper(pdf_path, "prompt", _make_config())

        assert isinstance(result, dict)
        for key in ("research_question", "background", "method", "results", "conclusions", "keywords"):
            assert key in result


class TestGenerateTags:
    def test_generate_tags_returns_list(self):
        """generate_tags returns a list of tag strings from the tool response."""
        analysis = {
            "research_question": "How does attention work?",
            "method": "We apply self-attention.",
            "keywords": ["transformer", "attention", "nlp"],
        }
        expected_tags = ["NLP", "transformer", "deep-learning"]

        mock_response = _make_tool_use_response("generate_paper_tags", {"tags": expected_tags})
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response

        with patch("paper_manager.analyzer.anthropic.Anthropic", return_value=mock_client):
            from paper_manager.analyzer import generate_tags
            tags = generate_tags(analysis, _make_config())

        assert isinstance(tags, list)
        assert tags == expected_tags

        # Verify the summary was passed in the user message
        call_kwargs = mock_client.messages.create.call_args
        messages = call_kwargs.kwargs["messages"]
        assert "transformer" in messages[0]["content"]
        assert "attention" in messages[0]["content"]
