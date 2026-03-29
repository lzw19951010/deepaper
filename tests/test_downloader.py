"""Tests for paper_manager.downloader."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from paper_manager.downloader import download_pdf, fetch_metadata, parse_arxiv_id

# ---------------------------------------------------------------------------
# Sample Atom XML returned by the arxiv API
# ---------------------------------------------------------------------------
SAMPLE_ATOM_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2301.00001v1</id>
    <title>Test Paper: A Survey of Testing</title>
    <author><name>Alice Smith</name></author>
    <author><name>Bob Jones</name></author>
    <published>2023-01-01T00:00:00Z</published>
    <summary>This paper surveys testing methodologies in depth.</summary>
    <category term="cs.SE" scheme="http://arxiv.org/schemas/atom"/>
    <category term="cs.LG" scheme="http://arxiv.org/schemas/atom"/>
  </entry>
</feed>
"""

EMPTY_ATOM_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
</feed>
"""


# ---------------------------------------------------------------------------
# parse_arxiv_id
# ---------------------------------------------------------------------------

def test_parse_arxiv_id_abs_url():
    assert parse_arxiv_id("https://arxiv.org/abs/2301.00001") == "2301.00001"


def test_parse_arxiv_id_pdf_url():
    assert parse_arxiv_id("https://arxiv.org/pdf/2301.00001v2") == "2301.00001"


def test_parse_arxiv_id_hf_url():
    assert parse_arxiv_id("https://huggingface.co/papers/2301.00001") == "2301.00001"


def test_parse_arxiv_id_bare():
    assert parse_arxiv_id("2301.00001") == "2301.00001"


def test_parse_arxiv_id_invalid():
    with pytest.raises(ValueError, match="Unrecognised arxiv URL"):
        parse_arxiv_id("https://google.com")


# ---------------------------------------------------------------------------
# fetch_metadata
# ---------------------------------------------------------------------------

def _make_httpx_response(text: str, status_code: int = 200) -> MagicMock:
    resp = MagicMock()
    resp.status_code = status_code
    resp.text = text
    resp.raise_for_status = MagicMock()
    return resp


def test_fetch_metadata_parses_xml():
    resp = _make_httpx_response(SAMPLE_ATOM_XML)

    with patch("paper_manager.downloader._rate_limit"), \
         patch("httpx.get", return_value=resp):
        meta = fetch_metadata("2301.00001")

    assert meta["arxiv_id"] == "2301.00001"
    assert meta["title"] == "Test Paper: A Survey of Testing"
    assert meta["authors"] == ["Alice Smith", "Bob Jones"]
    assert meta["date"] == "2023-01-01"
    assert "surveys testing" in meta["abstract"]
    assert "cs.SE" in meta["categories"]
    assert "cs.LG" in meta["categories"]
    assert meta["url"] == "https://arxiv.org/abs/2301.00001"


def test_fetch_metadata_raises_on_empty_response():
    resp = _make_httpx_response(EMPTY_ATOM_XML)

    with patch("paper_manager.downloader._rate_limit"), \
         patch("httpx.get", return_value=resp):
        with pytest.raises(ValueError, match="arxiv ID not found"):
            fetch_metadata("9999.99999")


# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------

def test_rate_limiter_enforces_delay():
    """When less than 3 seconds have elapsed, sleep should be called."""
    import paper_manager.downloader as dl

    # Simulate last request happening 1 second ago (monotonic time)
    fake_now = 1000.0
    fake_last = fake_now - 1.0  # only 1 second elapsed → need ~2 more seconds

    with patch("paper_manager.downloader._last_request_time", fake_last), \
         patch("time.monotonic", side_effect=[fake_now, fake_now + 2.0]), \
         patch("time.sleep") as mock_sleep:
        dl._rate_limit()

    mock_sleep.assert_called_once()
    sleep_arg = mock_sleep.call_args[0][0]
    assert 1.9 <= sleep_arg <= 2.1, f"Expected ~2.0s sleep, got {sleep_arg}"


# ---------------------------------------------------------------------------
# download_pdf
# ---------------------------------------------------------------------------

def test_download_pdf_saves_file(tmp_path: Path):
    fake_pdf_bytes = b"%PDF-1.4 fake content"
    resp = MagicMock()
    resp.status_code = 200
    resp.content = fake_pdf_bytes
    resp.raise_for_status = MagicMock()

    with patch("paper_manager.downloader._rate_limit"), \
         patch("httpx.get", return_value=resp):
        result = download_pdf("2301.00001", tmp_path / "pdfs")

    assert result == tmp_path / "pdfs" / "2301.00001.pdf"
    assert result.exists()
    assert result.read_bytes() == fake_pdf_bytes


def test_download_pdf_raises_on_404(tmp_path: Path):
    resp = MagicMock()
    resp.status_code = 404
    resp.raise_for_status = MagicMock()

    with patch("paper_manager.downloader._rate_limit"), \
         patch("httpx.get", return_value=resp):
        with pytest.raises(ValueError, match="not found \\(404\\)"):
            download_pdf("2301.00001", tmp_path)


def test_download_pdf_raises_on_410(tmp_path: Path):
    resp = MagicMock()
    resp.status_code = 410
    resp.raise_for_status = MagicMock()

    with patch("paper_manager.downloader._rate_limit"), \
         patch("httpx.get", return_value=resp):
        with pytest.raises(ValueError, match="withdrawn \\(410\\)"):
            download_pdf("2301.00001", tmp_path)
