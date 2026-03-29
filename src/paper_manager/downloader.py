"""arxiv paper downloader with rate limiting."""
from __future__ import annotations

import time
import xml.etree.ElementTree as ET
from pathlib import Path

import httpx

_last_request_time: float = 0.0
_RATE_LIMIT_SECONDS = 3.0
_ARXIV_NS = "http://www.w3.org/2005/Atom"
_ARXIV_NS2 = "http://arxiv.org/schemas/atom"


def _rate_limit() -> None:
    """Sleep until at least 3 seconds have elapsed since the last request."""
    global _last_request_time
    elapsed = time.monotonic() - _last_request_time
    if elapsed < _RATE_LIMIT_SECONDS:
        time.sleep(_RATE_LIMIT_SECONDS - elapsed)
    _last_request_time = time.monotonic()


def parse_arxiv_id(url: str) -> str:
    """Extract an arxiv ID from a URL or bare ID string.

    Supported formats:
        https://arxiv.org/abs/2301.00001
        https://arxiv.org/pdf/2301.00001
        https://arxiv.org/pdf/2301.00001v2
        https://huggingface.co/papers/2301.00001
        2301.00001  (bare ID)

    Version suffixes (e.g. v2) are stripped.

    Raises:
        ValueError: If the format is not recognised.
    """
    url = url.strip()

    # Bare ID: digits.digits with optional version suffix
    import re
    bare_pattern = re.compile(r"^(\d{4}\.\d{4,5})(v\d+)?$")
    m = bare_pattern.match(url)
    if m:
        return m.group(1)

    # arxiv.org abs or pdf URL
    arxiv_pattern = re.compile(
        r"https?://(?:export\.)?arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(v\d+)?(?:\.pdf)?$"
    )
    m = arxiv_pattern.match(url)
    if m:
        return m.group(1)

    # huggingface.co papers URL
    hf_pattern = re.compile(
        r"https?://huggingface\.co/papers/(\d{4}\.\d{4,5})(v\d+)?$"
    )
    m = hf_pattern.match(url)
    if m:
        return m.group(1)

    raise ValueError(
        f"Unrecognised arxiv URL or ID format: {url!r}. "
        "Expected formats: https://arxiv.org/abs/<id>, "
        "https://arxiv.org/pdf/<id>[v<n>], "
        "https://huggingface.co/papers/<id>, or bare ID like 2301.00001."
    )


def fetch_metadata(arxiv_id: str) -> dict:
    """Fetch paper metadata from the arxiv API.

    Args:
        arxiv_id: A bare arxiv ID such as "2301.00001".

    Returns:
        dict with keys: arxiv_id, title, authors, date, abstract,
        categories, url.

    Raises:
        ValueError: If the arxiv ID is not found.
        httpx.HTTPError: On unrecoverable HTTP errors.
    """
    api_url = f"https://export.arxiv.org/api/query?id_list={arxiv_id}"

    last_exc: Exception | None = None
    for attempt in range(3):
        if attempt > 0:
            time.sleep(2 ** attempt)
        _rate_limit()
        try:
            response = httpx.get(api_url, timeout=30.0)
            if response.status_code >= 500:
                last_exc = httpx.HTTPStatusError(
                    f"Server error {response.status_code}",
                    request=response.request,
                    response=response,
                )
                continue
            response.raise_for_status()
            break
        except httpx.TimeoutException as exc:
            last_exc = exc
            continue
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code >= 500:
                last_exc = exc
                continue
            raise
    else:
        raise last_exc  # type: ignore[misc]

    root = ET.fromstring(response.text)
    ns = {"atom": _ARXIV_NS, "arxiv": _ARXIV_NS2}

    entries = root.findall("atom:entry", ns)
    if not entries:
        raise ValueError(f"arxiv ID not found: {arxiv_id!r}")

    entry = entries[0]

    # Check for the "no results" entry arxiv returns for unknown IDs
    title_el = entry.find("atom:title", ns)
    title = (title_el.text or "").strip() if title_el is not None else ""
    if title.lower() == "error":
        raise ValueError(f"arxiv ID not found: {arxiv_id!r}")

    authors = [
        (name_el.text or "").strip()
        for author_el in entry.findall("atom:author", ns)
        for name_el in [author_el.find("atom:name", ns)]
        if name_el is not None
    ]

    published_el = entry.find("atom:published", ns)
    date_raw = (published_el.text or "").strip() if published_el is not None else ""
    date = date_raw[:10] if date_raw else ""

    abstract_el = entry.find("atom:summary", ns)
    abstract = " ".join((abstract_el.text or "").split()) if abstract_el is not None else ""

    categories = [
        el.get("term", "")
        for el in entry.findall("atom:category", ns)
        if el.get("term")
    ]

    return {
        "arxiv_id": arxiv_id,
        "title": title,
        "authors": authors,
        "date": date,
        "abstract": abstract,
        "categories": categories,
        "url": f"https://arxiv.org/abs/{arxiv_id}",
    }


def download_pdf(arxiv_id: str, output_dir: Path) -> Path:
    """Download a paper PDF from arxiv.

    Args:
        arxiv_id: A bare arxiv ID such as "2301.00001".
        output_dir: Directory in which to save the PDF.

    Returns:
        Path to the saved PDF file.

    Raises:
        ValueError: On 404 (not found) or 410 (withdrawn).
        httpx.HTTPError: On other unrecoverable HTTP errors.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_url = f"https://export.arxiv.org/pdf/{arxiv_id}"
    dest = output_dir / f"{arxiv_id}.pdf"

    last_exc: Exception | None = None
    for attempt in range(3):
        if attempt > 0:
            time.sleep(2 ** attempt)
        _rate_limit()
        try:
            response = httpx.get(pdf_url, timeout=60.0, follow_redirects=True)
            if response.status_code == 404:
                raise ValueError(f"Paper {arxiv_id} not found (404)")
            if response.status_code == 410:
                raise ValueError(f"Paper {arxiv_id} has been withdrawn (410)")
            if response.status_code >= 500:
                last_exc = httpx.HTTPStatusError(
                    f"Server error {response.status_code}",
                    request=response.request,
                    response=response,
                )
                continue
            response.raise_for_status()
            dest.write_bytes(response.content)
            return dest
        except ValueError:
            raise
        except httpx.TimeoutException as exc:
            last_exc = exc
            continue
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code >= 500:
                last_exc = exc
                continue
            raise
    else:
        raise last_exc  # type: ignore[misc]

    return dest  # unreachable, satisfies type checker
