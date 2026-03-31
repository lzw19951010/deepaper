# Plan: Paper-Manager Virality & Citation-Based Descendants

**Created:** 2026-03-30
**Status:** Draft - awaiting confirmation
**Complexity:** HIGH (multi-phase, spans distribution, API integration, UX, and marketing)

---

## Context

paper-manager is a Python CLI (v0.1.0) that analyzes arxiv papers via Claude Code CLI and generates structured 7-section Obsidian-compatible markdown notes. It has strong analytical depth but limited discoverability, polish, and one key analytical weakness: the "Descendants" section in the Mechanism Family Tree relies only on speculative future-works content from the paper itself rather than actual citation data.

**Current architecture:**
- CLI entry: `src/paper_manager/cli.py` (typer-based, commands: init/add/search/sync/tag/reindex/config)
- Analysis: `src/paper_manager/analyzer.py` (calls Claude Code CLI via subprocess, returns JSON)
- Output: `src/paper_manager/writer.py` (YAML frontmatter + 7 markdown sections)
- Search: `src/paper_manager/search.py` (ChromaDB + bge-small-zh-v1.5 embeddings)
- Download: `src/paper_manager/downloader.py` (arxiv HTML scraping + PDF streaming)
- Config: `src/paper_manager/config.py` (dataclass, yaml-based)
- Templates: `templates/default.md` (Chinese-language analysis prompt), `templates/categories.md`

**Target audience:** ML researchers, primarily Chinese-speaking, who read arxiv papers and use Obsidian.

---

## Work Objectives

### Part A: Virality & Usability (6 steps)
### Part B: Citation-Based Descendants (2 steps)

---

## Guardrails

### Must Have
- All changes backward-compatible with existing paper notes
- No new API billing (continue using Claude Code CLI Max subscription for analysis)
- pip-installable from PyPI
- Chinese-language output maintained as default

### Must NOT Have
- No breaking changes to existing `papers/` directory structure or frontmatter schema
- No mandatory external API keys for core functionality (citation lookup should degrade gracefully)
- No heavy dependencies that bloat install time (sentence-transformers is already heavy enough)

---

## Task Flow (Prioritized: High-Impact, Low-Effort First)

### Step 1: Distribution & First-Time Experience (HIGH impact, MEDIUM effort)

**Goal:** Someone who sees the project can go from zero to first analyzed paper in under 3 minutes.

**1a. PyPI Publishing**
- Add proper metadata to `pyproject.toml`: author, license (MIT), project-urls (homepage, repository), classifiers, long_description from README
- Add `pypdfium2` to dependencies (it's imported in analyzer.py but missing from pyproject.toml)
- Test `pip install paper-manager` flow end-to-end
- **Acceptance:** `pip install paper-manager && paper-manager --help` works from a clean venv

**1b. One-Command Quick Start**
- Modify `init` command to auto-create a minimal `config.yaml` without requiring `config.yaml.example` to exist (currently fails if run outside the repo root)
- Make `paper-manager init` work from any empty directory (not just the repo root)
- Auto-detect Claude Code CLI availability during init and give clear error if missing
- **Acceptance:** `mkdir test && cd test && paper-manager init && paper-manager add 2301.00001` works

**1c. Progress UX Polish**
- Add rich/colorful terminal output (use `rich` library) -- progress bars for PDF download, spinner for analysis, colored status messages
- Add estimated time remaining for analysis (based on token count)
- Add a final summary card after `add` completes showing: title, category, tags, file path, and time taken
- **Acceptance:** `paper-manager add <url>` shows visually polished output with progress indicators

---

### Step 2: README & Demo-ability (HIGH impact, LOW effort)

**Goal:** The GitHub README should make someone want to star and share the project within 10 seconds.

**2a. README Overhaul**
- Hero section: One-line pitch + animated GIF/asciicast showing `paper-manager add <url>` end-to-end
- "Why this tool?" section: 3-4 bullet comparisons vs alternatives (Zotero, Semantic Scholar, manual notes)
- Feature showcase: Screenshot of an actual generated note opened in Obsidian (use existing DeepSeek-V3 note)
- Clear badge row: PyPI version, Python version, License, Stars
- Quick start: exactly 3 commands (install, init, add)
- Chinese README section or separate README_CN.md

**2b. Demo Recording**
- Record terminal session with `asciinema` or `vhs` (charmbracelet/vhs) showing: install, init, add a paper, search, view in Obsidian
- Convert to GIF for README hero section
- **Acceptance:** README has a working demo GIF, install badges, and takes < 30 seconds to understand the value proposition

---

### Step 3: Citation-Based Descendants via Semantic Scholar API (HIGH impact, HIGH effort)

**Goal:** Replace the speculative "Descendants" section with real citing papers fetched from Semantic Scholar API.

**3a. New Module: `src/paper_manager/citations.py`**
- Use Semantic Scholar API (free, no API key required for basic access, 100 req/5min rate limit)
  - Endpoint: `GET https://api.semanticscholar.org/graph/v1/paper/ArXiv:{arxiv_id}/citations`
  - Fields: `title,authors,year,citationCount,externalIds,url,abstract,isInfluential`
  - Returns papers that CITE the given paper
- Implement `fetch_citing_papers(arxiv_id: str, limit: int = 50) -> list[dict]`
  - Rate limiting: respect 100 req/5min (reuse existing `_rate_limit` pattern from downloader.py)
  - Graceful degradation: if API fails, return empty list (don't break the pipeline)
  - Sort by `citationCount` descending to surface most impactful descendants
  - Filter for `isInfluential=True` to highlight significant citations
- Implement `format_descendants_section(citing_papers: list[dict]) -> str`
  - Group into: "High-Impact Descendants" (influential citations) and "Other Notable Citations"
  - For each: title, authors (first author + et al.), year, venue, citation count, one-line connection
  - Include total citation count as a metric

**3b. Integration into Analysis Pipeline**
- In `cli.py` `add` command: after `analyze_paper()`, call `fetch_citing_papers()`
- Pass citing papers to a new Claude prompt that asks: "Given these citing papers, rewrite the Descendants section of the Mechanism Family Tree to reflect actual follow-up work rather than speculation"
- Alternatively (cheaper, no extra Claude call): directly format the citation data into markdown and inject it into the `mechanism_transfer` section, replacing the speculative descendants subsection
- Store citation metadata in frontmatter: `citation_count`, `influential_citations` count, `citation_fetch_date`
- **Acceptance:** Running `paper-manager add <old-paper-url>` (e.g., the 2017 Attention Is All You Need paper) produces a Descendants section listing real citing papers with citation counts, not speculation

**3c. Standalone Citation Command**
- `paper-manager cite <arxiv-url-or-id>` -- fetch and display citing papers without re-analyzing
- `paper-manager cite --update` -- update the descendants section of an existing note in place
- **Acceptance:** `paper-manager cite 1706.03762` shows citing papers for the Transformer paper

---

### Step 4: Table-Stakes Paper Management Features (MEDIUM impact, MEDIUM effort)

**Goal:** Feature parity with what researchers expect from a paper management tool.

**4a. Paper List / Browse Command**
- `paper-manager list` -- show all papers in a formatted table (title, date, category, tags)
- `paper-manager list --category llm/pretraining` -- filter by category
- `paper-manager list --tag transformer` -- filter by tag
- `paper-manager list --sort date|title|category` -- sorting
- **Acceptance:** `paper-manager list` outputs a readable table of all indexed papers

**4b. Paper Open Command**
- `paper-manager open <query>` -- fuzzy-search and open a paper note in the default editor or Obsidian
- Use semantic search to resolve the query, then `open` the file
- **Acceptance:** `paper-manager open "deepseek v3"` opens the DeepSeek-V3 note

**4c. Batch Import from Reading List**
- `paper-manager import <file>` -- read a text file with one arxiv URL per line, process all
- Show progress: "Processing 3/10 papers..."
- Skip already-processed papers (existing behavior, just surface it clearly)
- **Acceptance:** Create a file with 5 arxiv URLs, run `paper-manager import list.txt`, all 5 get processed

**4d. Export / Stats**
- `paper-manager stats` -- show collection stats: total papers, papers by category, papers by month, top tags
- **Acceptance:** `paper-manager stats` outputs meaningful collection statistics

---

### Step 5: Sharing & Community Features (MEDIUM impact, LOW effort)

**Goal:** Make it easy for users to share their paper notes and discover others'.

**5a. Single-Paper Export**
- `paper-manager export <query> --format md|html` -- export a paper note as a standalone file or HTML page
- For HTML: use a simple template with good typography (similar to arxiv-sanity)
- **Acceptance:** `paper-manager export "deepseek" --format html` produces a readable HTML file

**5b. Collection README Generator**
- `paper-manager readme` -- auto-generate a `papers/README.md` index with links to all papers, grouped by category
- This makes the git repo itself browsable on GitHub
- **Acceptance:** `paper-manager readme` creates a browsable index at `papers/README.md`

---

### Step 6: Language & Internationalization (LOW impact on virality, but removes friction)

**Goal:** Make the tool accessible to English-speaking researchers too.

**6a. Language Config Option**
- Add `language: zh|en` to `config.yaml`
- Create `templates/default_en.md` -- English version of the analysis prompt
- Section headings in writer.py should switch based on language config
- **Acceptance:** Setting `language: en` produces English-language analysis notes

---

## Detailed Implementation Notes

### Semantic Scholar API Details (Step 3)

**Why Semantic Scholar over alternatives:**

| API | Free Tier | Rate Limit | Citation Data | Reliability |
|-----|-----------|------------|---------------|-------------|
| Semantic Scholar | Yes, no key needed | 100 req/5min | Excellent, includes `isInfluential` flag | High, academic-backed |
| OpenAlex | Yes, no key needed | 100k/day | Good, but no influence scoring | High |
| Google Scholar | No official API | N/A (scraping is TOS violation) | Best coverage | Fragile, gets blocked |
| CrossRef | Yes | 50 req/sec | References only (not citations) | High but wrong direction |

**Recommendation:** Use Semantic Scholar as primary. Consider OpenAlex as fallback. Do NOT scrape Google Scholar.

**API call example:**
```
GET https://api.semanticscholar.org/graph/v1/paper/ArXiv:1706.03762/citations
    ?fields=title,authors,year,citationCount,externalIds,url,isInfluential
    &limit=50
    &offset=0
```

**Expected output format in the note:**
```markdown
### 后代 (Descendants) — 基于引用分析

> 截至 2026-03-30，本文共被引用 **127,453** 次（数据来源：Semantic Scholar）

#### 高影响力后续工作
| 论文 | 年份 | 引用数 | 关键继承/改进 |
|------|------|--------|-------------|
| BERT: Pre-training of Deep Bidirectional... | 2019 | 89,234 | 将Transformer encoder用于预训练 |
| GPT-2: Language Models are Unsupervised... | 2019 | 12,456 | 将Transformer decoder扩展到大规模语言模型 |
| ...

#### 其他引用统计
- 被标记为"有重大影响"的引用：**X** 篇
- 引用趋势：[按年分布]
```

### Architecture Decision: Where Citation Fetch Happens

**Option A (Recommended):** Fetch citations as a separate step AFTER Claude analysis, then format directly into markdown without an additional Claude call. This is simpler, faster, and doesn't consume Claude Code bandwidth.

**Option B:** Pass citation data into the Claude prompt so Claude can synthesize a narrative. Richer output but uses more Claude tokens and makes the prompt longer.

**Decision:** Start with Option A. Add Option B as an optional `--deep-cite` flag later if users want narrative synthesis.

---

## Success Criteria

1. **Distribution:** `pip install paper-manager` works and the tool runs from any directory
2. **First impression:** README has demo GIF, clear value proposition, takes < 30s to understand
3. **Citation descendants:** `paper-manager add` for a well-cited paper shows real citing papers in the Descendants section
4. **Usability:** `paper-manager list`, `paper-manager stats`, and `paper-manager open` work
5. **Sharing:** `paper-manager readme` generates a browsable index for the GitHub repo

---

## Execution Order (Recommended)

| Phase | Steps | Rationale |
|-------|-------|-----------|
| Phase 1 (Week 1) | 1a, 1b, 2a | Distribution + README are pre-requisites for any virality |
| Phase 2 (Week 1-2) | 3a, 3b | Citation-based descendants is the differentiating feature |
| Phase 3 (Week 2) | 1c, 3c, 4a | Polish UX + standalone cite command + list command |
| Phase 4 (Week 3) | 4b, 4c, 4d, 5a, 5b | Table-stakes features that round out the tool |
| Phase 5 (Later) | 6a | English support expands audience but isn't needed for initial launch |

---

## Open Questions

See `.omc/plans/open-questions.md`
