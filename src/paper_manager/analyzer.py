"""Claude API paper analysis using tool_use for structured output."""
from __future__ import annotations

import base64
import logging
import time
from pathlib import Path

import anthropic
import pdfplumber

logger = logging.getLogger(__name__)

ANALYSIS_TOOL = {
    "name": "extract_paper_analysis",
    "description": "Extract structured information from an academic paper",
    "input_schema": {
        "type": "object",
        "properties": {
            "research_question": {"type": "string", "description": "Core research question (1-3 sentences)"},
            "background": {"type": "string", "description": "Background context and motivation (2-4 sentences)"},
            "method": {"type": "string", "description": "Proposed approach/methodology (3-6 sentences)"},
            "results": {"type": "string", "description": "Key quantitative and qualitative results (3-5 sentences)"},
            "conclusions": {"type": "string", "description": "Main conclusions and contributions (2-4 sentences)"},
            "limitations": {"type": ["string", "null"], "description": "Acknowledged limitations, or null"},
            "future_work": {"type": ["string", "null"], "description": "Future research directions, or null"},
            "venue": {"type": ["string", "null"], "description": "Publication venue (e.g. NeurIPS 2023), or null"},
            "keywords": {"type": "array", "items": {"type": "string"}, "description": "5-10 technical keywords"},
        },
        "required": ["research_question", "background", "method", "results", "conclusions", "keywords"],
    },
}

TAG_TOOL = {
    "name": "generate_paper_tags",
    "description": "Generate classification tags for a paper",
    "input_schema": {
        "type": "object",
        "properties": {
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "3-8 tags for categorizing the paper (e.g. 'NLP', 'transformer', 'image-generation')",
            }
        },
        "required": ["tags"],
    },
}


def get_page_count(pdf_path: Path) -> int:
    """Return the number of pages in a PDF file."""
    with pdfplumber.open(pdf_path) as pdf:
        return len(pdf.pages)


def get_file_size_mb(pdf_path: Path) -> float:
    """Return file size in megabytes."""
    return pdf_path.stat().st_size / (1024 * 1024)


def extract_text(pdf_path: Path) -> str:
    """Extract all text from a PDF using pdfplumber.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Extracted text joined with double newlines between pages.
        May be empty for scanned PDFs.
    """
    with pdfplumber.open(pdf_path) as pdf:
        pages_text = [page.extract_text() or "" for page in pdf.pages]
    return "\n\n".join(pages_text)


def _find_tool_use_block(response) -> dict | None:
    """Find and return the input dict from the first tool_use block in response.content."""
    for block in response.content:
        if block.type == "tool_use":
            return block.input
    return None


def analyze_paper(pdf_path: Path, prompt: str, config) -> dict:
    """Analyze a paper with Claude using tool_use for structured output.

    Uses PDF mode (base64 document) for small papers (<=100 pages, <=30 MB),
    falling back to text extraction mode for larger papers.

    Args:
        pdf_path: Path to the PDF file.
        prompt: Rendered prompt string (template + metadata header).
        config: Config object with api_key, model attributes.

    Returns:
        Dict with extracted paper analysis fields.

    Raises:
        anthropic.APIError: After 3 failed attempts with no partial result.
    """
    pages = get_page_count(pdf_path)
    size_mb = get_file_size_mb(pdf_path)

    use_pdf_mode = pages <= 100 and size_mb <= 30

    if not use_pdf_mode:
        logger.warning(
            "Paper %s is large (%d pages, %.1f MB); falling back to text extraction mode.",
            pdf_path.name,
            pages,
            size_mb,
        )

    if use_pdf_mode:
        pdf_data = base64.standard_b64encode(pdf_path.read_bytes()).decode("utf-8")
        content = [
            {
                "type": "document",
                "source": {"type": "base64", "media_type": "application/pdf", "data": pdf_data},
            },
            {"type": "text", "text": prompt},
        ]
    else:
        text = extract_text(pdf_path)
        content = [{"type": "text", "text": f"{prompt}\n\n---\nPaper text:\n{text}"}]

    client = anthropic.Anthropic(api_key=config.api_key)
    last_error: anthropic.APIError | None = None

    for attempt in range(3):
        try:
            response = client.messages.create(
                model=config.model,
                max_tokens=4096,
                tools=[ANALYSIS_TOOL],
                tool_choice={"type": "tool", "name": "extract_paper_analysis"},
                messages=[{"role": "user", "content": content}],
            )
            result = _find_tool_use_block(response)
            if result is not None:
                return result
        except anthropic.APIError as exc:
            last_error = exc
            delay = 2 ** attempt  # 1s, 2s, 4s
            logger.warning("API error on attempt %d/%d: %s. Retrying in %ds.", attempt + 1, 3, exc, delay)
            time.sleep(delay)

    if last_error is not None:
        raise last_error
    # Should not be reached, but satisfy type checker
    return {}


def generate_tags(analysis: dict, config) -> list[str]:
    """Generate classification tags for a paper based on its analysis.

    Args:
        analysis: Analysis dict containing research_question, method, keywords.
        config: Config object with api_key, tag_model attributes.

    Returns:
        List of classification tag strings.
    """
    keywords = analysis.get("keywords", [])
    keywords_str = ", ".join(keywords) if isinstance(keywords, list) else str(keywords)
    summary = (
        f"{analysis.get('research_question', '')} "
        f"{analysis.get('method', '')} "
        f"{keywords_str}"
    ).strip()

    client = anthropic.Anthropic(api_key=config.api_key)
    response = client.messages.create(
        model=config.tag_model,
        max_tokens=256,
        tools=[TAG_TOOL],
        tool_choice={"type": "tool", "name": "generate_paper_tags"},
        messages=[{"role": "user", "content": f"Generate 3-8 classification tags for this paper: {summary}"}],
    )

    result = _find_tool_use_block(response)
    if result is not None:
        return result.get("tags", [])
    return []
