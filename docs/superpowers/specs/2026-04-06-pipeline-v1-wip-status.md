# Pipeline Perf Optimization v1 — WIP Status

> Snapshot of uncommitted work on `feat/pipeline-perf-optimization` branch before v2 refactor begins.

## Summary

This WIP implements the pipeline-perf-optimization spec from 2026-04-06. It refactors deepaper's internals to use a centralized `output_schema.py` as single source of truth, and fixes several pipeline issues discovered during OLMo 3 profiling.

## What Was Done

### New files created

| File | Status | Purpose |
|------|--------|---------|
| `src/deepaper/output_schema.py` | New, complete | Single source of truth for section specs, char floors, frontmatter fields, heading levels, H2/H8 gate parameters |
| `tests/test_gates_integration.py` | New, complete | Integration tests for full gate pipeline |
| `tests/fixtures/olmo3_v1_output.md` | New, complete | Fixture of OLMo 3 v1 pipeline output for regression testing |
| `docs/superpowers/specs/2026-04-06-output-schema-design.md` | New, complete | Design spec for output_schema centralization |
| `docs/superpowers/specs/2026-04-06-pipeline-issues-log.md` | New, complete | 7 pipeline issues with priority and optimization roadmap |
| `docs/superpowers/specs/2026-04-06-pipeline-perf-optimization-design.md` | New, complete | Design spec for pipeline perf optimization |
| `docs/superpowers/plans/2026-04-06-pipeline-perf-optimization.md` | New, complete | Implementation plan (partially executed) |

### Files modified (key changes)

| File | Changes |
|------|---------|
| `src/deepaper/gates.py` | Imports from `output_schema.py` instead of hardcoding CHAR_FLOORS; H5 TL;DR check now tries frontmatter first then body fallback; H2 uses `H2_MIN_COVERAGE` constant; H6 heading check uses `HEADING_FORBIDDEN` from schema |
| `src/deepaper/prompt_builder.py` | Imports `SECTION_ORDER`, `CHAR_FLOORS`, `HEADING_SECTION_LEVEL` from `output_schema`; each visual section gets own writer (`writer-method`, `writer-experiment` instead of single `writer-visual`); `_VISUAL_SLUGS` mapping added |
| `src/deepaper/cli.py` | `gates` command writes `gates.json` to disk; `merge` command reorders sections by `SECTION_ORDER` with proper frontmatter extraction; `prompt` command simplified merge_order logic |
| `src/deepaper/defaults.py` | Section order changed: 动机与第一性原理 moved before 核心速览 (template section reorder) |
| `src/deepaper/registry.py` | `_SUBSECTION_RE` now uses `H2_SUBSECTION_REGEX` from `output_schema.py` instead of inline regex |
| `src/deepaper/prompt_templates/extractor.md` | Core figures instruction clarified (mark positions only, don't describe) |
| `tests/test_prompt_builder.py` | Tests updated for writer-method/writer-experiment split; tests for new section order |

### Papers regenerated

| File | Change |
|------|--------|
| `papers/llm/pretraining/olmo-3.md` | Regenerated with v1 pipeline improvements |

### Papers deleted (cleanup, can be regenerated)

- `papers/llm/pretraining/deepseek-v3-technical-report.md`
- `papers/llm/pretraining/minicpm-*.md`
- `papers/llm/pretraining/scaling-laws-*.md`
- `papers/llm/reasoning/deepseek-r1-*.md`
- `papers/recsys/generative-rec/*.md` (4 files)
- `papers/recsys/llm-as-rec/*.md` (1 file)

## What Was NOT Done (v1 plan incomplete items)

- H2 subsection regex still noisy (matches table row labels)
- Merge frontmatter hoisting not implemented (frontmatter can end up mid-file)
- Double `#### ####` heading bug not fixed
- `compute_scaling_factor` still produces inflated char targets for long papers
- No form-based output constraints (v2 will address this)

## Relationship to v2

The v2 refactor (`docs/superpowers/specs/2026-04-07-per-paper-analysis-v2-design.md`) supersedes this work but builds on top of it:

| v1 Foundation | v2 Uses It |
|--------------|-----------|
| `output_schema.py` as single source of truth | v2 rewrites the SECTIONS and FRONTMATTER_FIELDS but keeps the architecture |
| Gates importing from schema | v2 updates gates logic but reuses the import pattern |
| Per-section visual writers | v2 replaces with 3 fixed writers but reuses WriterTask structure |
| Merge section reordering | v2 adds frontmatter hoisting on top of this |
| H5 frontmatter-first TL;DR check | v2 keeps this logic |

## Test Status at Time of Snapshot

Not all tests were passing at this snapshot — the v1 changes were in-progress.
Run `pytest tests/ -v` after checkout to see current state.
