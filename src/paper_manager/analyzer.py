"""Paper analysis using Claude Code CLI (uses Max subscription, not API billing)."""
from __future__ import annotations

import json
import logging
import re
import subprocess
from pathlib import Path

import pdfplumber

logger = logging.getLogger(__name__)


def get_page_count(pdf_path: Path) -> int:
    """Return the number of pages in a PDF file."""
    with pdfplumber.open(pdf_path) as pdf:
        return len(pdf.pages)


def get_file_size_mb(pdf_path: Path) -> float:
    """Return file size in megabytes."""
    return pdf_path.stat().st_size / (1024 * 1024)


def extract_text(pdf_path: Path) -> str:
    """Extract all text from a PDF using pdfplumber."""
    with pdfplumber.open(pdf_path) as pdf:
        pages_text = [page.extract_text() or "" for page in pdf.pages]
    return "\n\n".join(pages_text)


def _call_claude(prompt: str) -> str:
    """Call Claude Code CLI in print mode and return the response text."""
    result = subprocess.run(
        ["claude", "-p", prompt, "--output-format", "text"],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Claude CLI error: {result.stderr.strip()}")
    return result.stdout.strip()


def _extract_json(text: str) -> dict:
    """Extract a JSON object from Claude's response text."""
    # Try to find JSON in a code block first
    match = re.search(r"```(?:json)?\s*\n(\{.*?\})\s*\n```", text, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    # Try to find a raw JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    raise ValueError("No JSON object found in response")


ANALYSIS_JSON_SCHEMA = """\
Respond with ONLY a JSON object (no markdown, no explanation) with these fields:
{
  "research_question": "Core research question (1-3 sentences)",
  "background": "Background context and motivation (2-4 sentences)",
  "method": "Proposed approach/methodology (3-6 sentences)",
  "results": "Key quantitative and qualitative results (3-5 sentences)",
  "conclusions": "Main conclusions and contributions (2-4 sentences)",
  "limitations": "Acknowledged limitations, or null",
  "future_work": "Future research directions, or null",
  "venue": "Publication venue (e.g. NeurIPS 2023), or null",
  "keywords": ["keyword1", "keyword2", "...5-10 technical keywords"]
}"""


def analyze_paper(pdf_path: Path, prompt: str, config) -> dict:
    """Analyze a paper using Claude Code CLI.

    Extracts text from the PDF, sends it to Claude Code for analysis.

    Args:
        pdf_path: Path to the PDF file.
        prompt: Rendered prompt string (template + metadata header).
        config: Config object (kept for interface compatibility).

    Returns:
        Dict with extracted paper analysis fields.
    """
    text = extract_text(pdf_path)
    if not text.strip():
        raise RuntimeError(f"Could not extract text from {pdf_path.name}")

    # Truncate very long papers to avoid CLI limits
    max_chars = 80000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[...truncated...]"

    full_prompt = f"{prompt}\n\n{ANALYSIS_JSON_SCHEMA}\n\n---\nPaper text:\n{text}"
    response = _call_claude(full_prompt)
    return _extract_json(response)


def generate_tags(analysis: dict, config) -> list[str]:
    """Generate classification tags for a paper using Claude Code CLI."""
    keywords = analysis.get("keywords", [])
    keywords_str = ", ".join(keywords) if isinstance(keywords, list) else str(keywords)
    summary = (
        f"{analysis.get('research_question', '')} "
        f"{analysis.get('method', '')} "
        f"{keywords_str}"
    ).strip()

    prompt = (
        f"Generate 3-8 classification tags for this academic paper.\n\n"
        f"Paper summary: {summary}\n\n"
        f"Respond with ONLY a JSON object: {{\"tags\": [\"tag1\", \"tag2\", ...]}}"
    )

    response = _call_claude(prompt)
    result = _extract_json(response)
    return result.get("tags", [])
