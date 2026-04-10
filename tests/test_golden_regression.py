"""Golden reference regression test.

Compares structural metrics between golden (frozen v2 output) and current
papers/ output. Does NOT check exact wording — only structural indicators.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

GOLDEN = Path("tests/golden/olmo-3.md")
CURRENT_P2 = Path("papers/llm/pretraining/olmo-3/olmo-3.md")
CURRENT_FLAT = Path("papers/llm/pretraining/olmo-3.md")


def _current_path() -> Path:
    if CURRENT_P2.exists():
        return CURRENT_P2
    return CURRENT_FLAT


def _parse(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    fm = yaml.safe_load(text[3:end]) or {}
    body = text[end + 3:]
    return fm, body


def _count_table_rows(body: str) -> int:
    return sum(1 for line in body.split("\n")
               if line.strip().startswith("|") and line.strip().endswith("|")
               and "---" not in line)


def _count_causal_chains(body: str) -> int:
    return len(re.findall(r"\[C\d+\]", body))


def _count_confusion_points(body: str) -> int:
    return len(re.findall(r"[❌]", body))


def _count_page_refs(body: str) -> int:
    return len(re.findall(r"(?:p\.|page\s+)\d+", body, re.IGNORECASE))


@pytest.mark.skipif(not GOLDEN.exists(), reason="golden not frozen yet")
class TestGoldenRegression:
    def setup_method(self):
        self.golden_fm, self.golden_body = _parse(GOLDEN)
        current = _current_path()
        if not current.exists():
            pytest.skip("current output not yet generated")
        self.current_fm, self.current_body = _parse(current)

    def test_causal_chains_not_fewer(self):
        golden_count = _count_causal_chains(self.golden_body)
        current_count = _count_causal_chains(self.current_body)
        assert current_count >= golden_count, \
            f"Causal chains regressed: {current_count} < {golden_count}"

    def test_confusion_points_not_fewer(self):
        golden_count = _count_confusion_points(self.golden_body)
        current_count = _count_confusion_points(self.current_body)
        assert current_count >= golden_count, \
            f"Confusion points regressed: {current_count} < {golden_count}"

    def test_table_rows_not_fewer(self):
        golden_count = _count_table_rows(self.golden_body)
        current_count = _count_table_rows(self.current_body)
        assert current_count >= golden_count, \
            f"Table rows regressed: {current_count} < {golden_count}"

    def test_page_refs_not_fewer(self):
        golden_count = _count_page_refs(self.golden_body)
        current_count = _count_page_refs(self.current_body)
        assert current_count >= golden_count, \
            f"Page refs regressed: {current_count} < {golden_count}"

    def test_arxiv_id_preserved(self):
        assert self.current_fm.get("arxiv_id"), "arxiv_id missing from current output"
