"""Tests for H9 ContentMarkers gate."""
import pytest


class TestCheckContentMarkers:
    def test_pass_on_complete_output(self):
        from deepaper.content_checklist import check_content_markers

        md = (
            "---\ntldr: test\n---\n"
            "#### 核心速览\n"
            "- **TL;DR:** 在 MATH 达 96.2%\n"
            "- **一图流:** 如果旧方法是X\n"
            "- **核心机制一句话:** [压缩] + [表示] + [渐进式] + [提升效率]\n\n"
            "#### 动机与第一性原理\n"
            "Because A导致B → Therefore C解决了D → 最终E\n\n"
            "#### 方法详解\n"
            "##### 数值推演\n假设 x=3, 代入公式...\n"
            "```python\ndef train(): pass\n```\n"
            "##### 易混淆点\n"
            "- ❌ 错误: blah\n- ✅ 正确: blah\n"
            "- ❌ 错误: blah2\n- ✅ 正确: blah2\n\n"
            "#### 实验与归因\n归因分析排序\n\n"
            "#### 专家批判\n隐性成本: 训练花了47天, 1024个GPU, 2.75M美元\n\n"
            "#### 机制迁移分析\n"
            "| 原语名称 | 本文用途 | 抽象描述 | 信息论/几何直觉 |\n"
            "|---|---|---|---|\n"
            "| A | B | C | D |\n"
            "前身 (Ancestors):\n- Method1\n- Method2\n- Method3\n"
        )
        result = check_content_markers(md)
        assert result["passed"] is True
        assert result["score"] >= 0.7

    def test_fail_on_missing_pseudocode(self):
        from deepaper.content_checklist import check_content_markers

        md = (
            "---\ntldr: test\n---\n"
            "#### 方法详解\n"
            "##### 数值推演\n假设 x=3\n"
            "##### 易混淆点\n- ❌ A\n- ✅ B\n- ❌ C\n- ✅ D\n"
        )
        result = check_content_markers(md)
        assert "方法详解:伪代码" in result["missing"]

    def test_fail_on_missing_causal_chain(self):
        from deepaper.content_checklist import check_content_markers

        md = (
            "---\ntldr: test\n---\n"
            "#### 动机与第一性原理\n"
            "这个方法很好因为它解决了问题。\n"
        )
        result = check_content_markers(md)
        assert "动机与第一性原理:因果链" in result["missing"]

    def test_missing_section_marks_all_markers_failed(self):
        from deepaper.content_checklist import check_content_markers

        md = "---\ntldr: test\n---\n#### 核心速览\nSome content with 96.2% TL;DR\n"
        result = check_content_markers(md)
        # 方法详解 section missing entirely
        assert "方法详解:数值推演" in result["missing"]
        assert "方法详解:伪代码" in result["missing"]
