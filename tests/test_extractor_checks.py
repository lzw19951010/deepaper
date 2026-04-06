"""Tests for StructCheck and Auditor."""
import pytest


class TestStructCheck:
    def test_all_sections_present(self):
        from deepaper.extractor import struct_check
        notes = "\n".join(f"## {s}\n{'x' * 300}" for s in [
            "META", "KEY_FINDINGS",
            "FORMULAS", "DATA_COMPOSITION", "EVAL_CONFIG",
            "TRAINING_COSTS", "DESIGN_DECISIONS", "RELATED_WORK", "BASELINES",
        ])
        result = struct_check(notes, total_pages=30, paper_profile={})
        assert result["passed"] is True
        assert result["missing_sections"] == []

    def test_missing_section(self):
        from deepaper.extractor import struct_check
        notes = "\n".join(f"## {s}\n{'x' * 300}" for s in [
            "META", "KEY_FINDINGS",
            "FORMULAS", "DATA_COMPOSITION",
            "DESIGN_DECISIONS", "RELATED_WORK", "BASELINES",
        ])
        result = struct_check(notes, total_pages=30, paper_profile={})
        assert result["passed"] is False
        assert "EVAL_CONFIG" in result["missing_sections"]
        assert "TRAINING_COSTS" in result["missing_sections"]

    def test_thin_section(self):
        from deepaper.extractor import struct_check
        notes = "\n".join(f"## {s}\n{'x' * 300}" for s in [
            "META", "KEY_FINDINGS",
            "FORMULAS", "DATA_COMPOSITION", "EVAL_CONFIG",
            "TRAINING_COSTS", "DESIGN_DECISIONS", "RELATED_WORK", "BASELINES",
        ])
        notes = notes.replace("## META\n" + "x" * 300, "## META\nshort")
        result = struct_check(notes, total_pages=30, paper_profile={})
        assert "META" in result["thin_sections"]


class TestParseNotesSections:
    def test_parses_sections(self):
        from deepaper.extractor import parse_notes_sections
        notes = "## META\nSome meta\n## MAIN_RESULTS\nSome results\n## ABLATIONS\nSome ablations"
        sections = parse_notes_sections(notes)
        assert "META" in sections
        assert "MAIN_RESULTS" in sections
        assert "ABLATIONS" in sections
        assert "Some meta" in sections["META"]


class TestAuditCoverage:
    def test_full_coverage(self):
        from deepaper.extractor import audit_coverage
        text_by_page = {i: f"page {i} content alpha beta gamma delta {i * 100}" for i in range(1, 21)}
        notes = " ".join(f"alpha beta gamma delta {i * 100}" for i in range(1, 21))
        result = audit_coverage(text_by_page, notes, total_pages=20)
        assert result["coverage_ratio"] >= 0.7

    def test_partial_coverage(self):
        from deepaper.extractor import audit_coverage
        text_by_page = {i: f"unique_term_page{i} " * 20 for i in range(1, 21)}
        notes = " ".join(f"unique_term_page{i}" for i in range(1, 6))
        result = audit_coverage(text_by_page, notes, total_pages=20)
        assert len(result["uncovered_segments"]) > 0


class TestUpdatedSections:
    def test_key_findings_in_required(self):
        from deepaper.extractor import REQUIRED_SECTIONS
        assert "KEY_FINDINGS" in REQUIRED_SECTIONS

    def test_old_table_sections_removed(self):
        from deepaper.extractor import REQUIRED_SECTIONS
        assert "MAIN_RESULTS" not in REQUIRED_SECTIONS
        assert "ABLATIONS" not in REQUIRED_SECTIONS
        assert "HYPERPARAMETERS" not in REQUIRED_SECTIONS
