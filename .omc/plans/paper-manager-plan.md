# Implementation Plan: Personal Paper Manager

## Source Spec
`.omc/specs/deep-interview-paper-manager.md` (ambiguity: 15.2%, 14-round deep interview)

## RALPLAN-DR Summary

### Principles
1. **Local-first**: All data is local Markdown files; GitHub is sync/backup only
2. **Obsidian-native**: YAML frontmatter + standard Markdown; every output file works as an Obsidian note out of the box
3. **CLI-driven**: No server, no daemon; all operations are explicit CLI commands
4. **Template-extensible**: Prompt templates are user-editable Markdown files, not hardcoded
5. **Incremental & edit-safe**: Re-running commands is safe; `tag` only modifies YAML frontmatter, never touches user-edited Markdown body

### Decision Drivers
1. **Development speed**: User wants a working MVP fast; Python ecosystem has all needed libraries
2. **Obsidian compatibility**: YAML frontmatter must use Obsidian-recognized property types (text, list, date)
3. **Cross-platform**: Must work identically on Windows and Mac without OS-specific code

### Viable Options

#### Option A: Monolithic Script (Rejected)
Single `paper_manager.py` file with all logic.
- **Pros**: Fastest to write, zero package structure overhead
- **Cons**: Untestable, unmaintainable past ~500 lines, no reusable components
- **Invalidation**: With 7+ distinct responsibilities (download, parse, analyze, tag, write, sync, search), a single file becomes unmanageable quickly. The user wants this tool to grow (RAG, tagging, future Zotero integration). While each responsibility is invoked sequentially, the tool's future growth path (Zotero import, web dashboard, custom embeddings) makes modular boundaries worth the ~15 min setup cost.

#### Option B: Modular Python Package with Typer CLI (Selected)
Package under `src/paper_manager/` with one module per responsibility, Typer for CLI, pyproject.toml for packaging.
- **Pros**: Clean separation, testable, installable via `pip install -e .`, each module independently modifiable
- **Cons**: Slightly more initial setup (pyproject.toml, __init__.py)
- **Why selected**: Marginal setup cost pays for itself immediately in maintainability. Typer provides auto-generated help and shell completion for free.

---

## Spec Deviations

| Spec Requirement | Deviation | Rationale |
|-----------------|-----------|-----------|
| `HuggingFace Hub 下载 arxiv 论文 PDF` (referenced 6x in spec) | Replaced with direct `httpx` download from `export.arxiv.org` | HF Hub's `hf_hub_download()` is designed for HuggingFace repository files (models, datasets), not arbitrary arxiv PDFs. There is no HF Hub API endpoint that accepts an arxiv ID and returns a PDF. The HF Paper Pages feature (`hf.co/papers/xxxx`) is a web UI, not a download API. Direct download from `export.arxiv.org` is simpler, has zero unnecessary dependencies, and is how all major tools (Semantic Scholar, Zotero) actually fetch arxiv papers. **HF URL support is preserved**: `parse_arxiv_id()` accepts `huggingface.co/papers/{id}` URLs, extracts the arxiv ID, and downloads from arxiv. **Lost capability**: No HF Hub caching or auth. **Follow-up**: v2 may add `huggingface-hub` for paper discovery/trending features if user requests. |
| `Claude Opus` as LLM (referenced 5x in spec) | Default model is `claude-opus-4-0-20250514` per spec. `claude-opus-4-0-20250514` available as cost-saving option via `model` config field. | Spec explicitly mandates Opus. Config makes model switchable so user can downgrade for cost savings (~$0.01-0.03/paper for Sonnet vs ~$0.05-0.15/paper for Opus). README documents the tradeoff. |

---

## Requirements Summary

Build a Python CLI tool (`paper-manager`) that:
1. Accepts arxiv links (including `huggingface.co/papers/` URLs) and downloads papers via `httpx` from arxiv.org
2. Sends PDFs to Claude Opus for structured analysis using configurable prompt templates
3. Outputs Obsidian-compatible Markdown with YAML frontmatter (Dataview-compatible)
4. Auto-generates tags and categories via Claude
5. Manages git sync (pull + push) to GitHub for multi-device use
6. Provides RAG-based semantic search via ChromaDB

---

## Acceptance Criteria

- [ ] **AC1**: `paper-manager add https://arxiv.org/abs/2301.00001` downloads the paper, analyzes it, and writes a `.md` file to `papers/2023/` — verifiable by checking the file exists with correct YAML frontmatter fields
- [ ] **AC2**: YAML frontmatter contains: `title`, `authors` (list), `date`, `arxiv_id`, `url`, `keywords` (list), `tags` (list), `venue` (if available) — verifiable by parsing the YAML and checking all fields are present and correctly typed
- [ ] **AC3**: Markdown body contains structured sections from the prompt template (e.g., Research Question, Method, Results, Conclusions) — verifiable by checking section headers exist
- [ ] **AC4**: `paper-manager add <url1> <url2> <url3>` batch-processes multiple papers sequentially with 3s delay between downloads — verifiable by checking 3 output files created
- [ ] **AC5**: `paper-manager sync` runs `git pull` (with rebase) then `git add`, `git commit`, `git push` — verifiable by checking git log after sync; multi-device: changes from other devices are pulled before pushing
- [ ] **AC6**: `paper-manager search "diffusion model acceleration"` returns relevant paper titles from ChromaDB — verifiable by adding 3+ papers and searching for a known topic
- [ ] **AC7**: Running `paper-manager add` on an already-processed arxiv ID skips it with a message; `--force` flag overrides and re-analyzes — verifiable by running twice on same ID (skip), then with `--force` (re-process)
- [ ] **AC8**: `paper-manager tag` re-tags all papers by updating YAML frontmatter only (preserves user-edited Markdown body) — verifiable by checking YAML tags field is populated and body text unchanged
- [ ] **AC9**: Obsidian opens the `papers/` directory as a vault and displays all notes with working frontmatter properties — verifiable by opening in Obsidian
- [ ] **AC10**: Tool runs on both Windows and Mac with identical behavior — verifiable by running on both platforms
- [ ] **AC11**: Papers with >100 pages fall back to text extraction via pdfplumber instead of Claude PDF mode — verifiable by testing with a long paper
- [ ] **AC12** (Core Scenario): After indexing 5+ papers across different domains, searching with a vague concept description (not a paper title or exact keyword) returns the correct paper in the top 3 results — this is THE primary use case ("forgot paper name, search by idea")

---

## Architecture

### Project Structure
```
paper_project/                  # git repo root = Obsidian vault root
├── papers/                     # Parsed paper notes (Obsidian browsable)
│   ├── 2023/
│   │   └── attention-is-all-you-need.md
│   ├── 2024/
│   └── 2025/
├── templates/                  # Prompt templates (user-editable)
│   └── default.md              # Default analysis template
├── src/                        # Tool source code (Obsidian excluded via init)
│   └── paper_manager/
│       ├── __init__.py         # Version string
│       ├── cli.py              # Typer CLI entry point
│       ├── downloader.py       # arxiv PDF download via httpx + arxiv API
│       ├── analyzer.py         # Claude API — PDF analysis + tagging
│       ├── templates.py        # Load and render prompt templates
│       ├── writer.py           # Generate Markdown + YAML frontmatter
│       ├── sync.py             # git add/commit/push operations
│       ├── search.py           # ChromaDB indexing + RAG query
│       └── config.py           # Config loading (env vars + config.yaml)
├── tests/                      # Test suite
│   ├── test_downloader.py
│   ├── test_analyzer.py
│   ├── test_writer.py
│   ├── test_search.py
│   ├── test_cli.py             # Test init, config creation, CLI arg parsing
│   └── conftest.py
├── config.yaml.example         # Config template (tracked in git, safe)
├── config.yaml                 # Actual config (gitignored, user creates)
├── pyproject.toml              # Package definition + dependencies
├── .gitignore                  # Ignore: config.yaml, .chromadb/, .obsidian/, tmp/, *.pdf
└── README.md                   # Usage instructions
```

### Obsidian Compatibility
- `.obsidian/` is gitignored (per-machine config)
- `paper-manager init` creates `.obsidian/app.json` with exclusion patterns for `src/`, `tests/`, `node_modules/`, `__pycache__/`
- `papers/` directory is the main browsing area
- `templates/` are visible and editable in Obsidian
- `tag` command only modifies YAML frontmatter (between `---` delimiters), never the Markdown body below
- YAML frontmatter is fully compatible with **Obsidian Dataview** plugin for structured queries (e.g., `TABLE authors, date, tags FROM "papers" WHERE contains(tags, "NLP")`)
- README documents recommended Dataview installation for advanced querying

### Data Flow
```
User runs: paper-manager add https://arxiv.org/abs/2301.00001

1. cli.py         → parse arxiv URL, extract arxiv_id (supports arxiv.org/abs/, /pdf/, huggingface.co/papers/)
2. downloader.py  → download PDF via httpx from https://export.arxiv.org/pdf/{id}
                  → fetch metadata from arxiv API (http://export.arxiv.org/api/query?id_list={id})
                  → 3-second delay between requests (arxiv rate limit compliance)
3. templates.py   → load prompt template from templates/default.md
4. analyzer.py    → check PDF page count via pdfplumber
                  → if ≤100 pages: send PDF (base64) to Claude API
                  → if >100 pages: extract text via pdfplumber, send as text to Claude API
                  → receive structured analysis + auto-generated tags
5. writer.py      → create YAML frontmatter + Markdown body
                  → write to papers/{year}/{sanitized-title}.md
6. search.py      → index the new document in ChromaDB
7. cleanup        → delete temp PDF from tmp/
```

---

## Implementation Steps

### Phase 1: Project Scaffolding (Files: 5)
**Goal**: Runnable project skeleton with config

| Step | File | Action | Details |
|------|------|--------|---------|
| 1.1 | `pyproject.toml` | Create | Define package with `[project.scripts] paper-manager = "paper_manager.cli:app"`. Dependencies: `typer[all]>=0.9`, `anthropic>=0.40`, `chromadb>=0.4`, `gitpython>=3.1`, `pyyaml>=6.0`, `pdfplumber>=0.10`, `httpx>=0.25`, `sentence-transformers>=2.2` (ChromaDB's `all-MiniLM-L6-v2` embedding model dependency). No `huggingface-hub` (see Spec Deviations section). |
| 1.2 | `src/paper_manager/__init__.py` | Create | `__version__ = "0.1.0"` |
| 1.3 | `config.yaml.example` | Create | Template (tracked in git) with: `anthropic_api_key: ""`, `model: "claude-opus-4-0-20250514"` (default per spec; user can switch to `claude-sonnet-4-5-20250514` for cost savings), `tag_model: "claude-sonnet-4-5-20250514"` (secondary model for lightweight tag generation; overridable for restricted orgs), `git_remote: ""`, `papers_dir: "papers"`, `template: "default"`, `chromadb_dir: ".chromadb"`. Include comments explaining each field, model cost tradeoffs, and that batch `tag` operations use `tag_model` to manage costs. |
| 1.4 | `src/paper_manager/config.py` | Create | Load config with priority: env vars (`ANTHROPIC_API_KEY`, `PAPER_MANAGER_MODEL`) > `config.yaml` > defaults. If `config.yaml` missing **and** the `init` command is running, copy from `config.yaml.example`; otherwise print error with `paper-manager init` instructions. Validate required fields (api_key must be set). Config dataclass with typed fields. Use `pathlib.Path` for cross-platform paths. Model identifier configurable (default: `claude-opus-4-0-20250514` per spec). |
| 1.5 | `.gitignore` | Create | Ignore: `config.yaml`, `.chromadb/`, `__pycache__/`, `*.pyc`, `.obsidian/`, `tmp/`, `*.pdf`, `.env`, `dist/`, `*.egg-info/` |
| 1.6 | `templates/default.md` | Create | Placeholder default prompt template (finalized in Phase 8) |

**Verification**: `pip install -e .` succeeds, `paper-manager --help` shows version

### Phase 2: Download Pipeline (Files: 2)
**Goal**: Download arxiv papers given a URL with rate limiting

| Step | File | Action | Details |
|------|------|--------|---------|
| 2.1 | `src/paper_manager/downloader.py` | Create | `parse_arxiv_id(url: str) -> str`: extract arxiv ID from multiple URL formats (`arxiv.org/abs/`, `arxiv.org/pdf/`, `huggingface.co/papers/`). `fetch_metadata(arxiv_id: str) -> dict`: call arxiv API, parse XML response, return `{title, authors, date, abstract, categories}`. `download_pdf(arxiv_id: str, output_dir: Path) -> Path`: download PDF from `https://export.arxiv.org/pdf/{id}` via httpx with 60s timeout. Handle 404 (paper not found) and 410 (withdrawn) with clear error messages. **Rate limiting**: module-level `_last_request_time` tracker; each request sleeps until 3s have elapsed since the last one (arxiv ToS compliance). Retry: 3 attempts with exponential backoff on transient HTTP errors (5xx, timeouts). |
| 2.2 | `tests/test_downloader.py` | Create | Test URL parsing for all 3 formats, test rate limiter logic (mock time), test metadata XML parsing |

**Verification**: `paper-manager add https://arxiv.org/abs/2301.00001` downloads a PDF; batch of 3 papers takes ≥9 seconds due to rate limiting

### Phase 3: Analysis Pipeline (Files: 3)
**Goal**: Analyze a PDF using Claude API with page-count-aware routing

| Step | File | Action | Details |
|------|------|--------|---------|
| 3.1 | `src/paper_manager/templates.py` | Create | `load_template(name: str, templates_dir: Path) -> str`: read from `templates/{name}.md`. `render_prompt(template: str, metadata: dict) -> str`: inject metadata (title, authors, date) into prompt template as context preamble. |
| 3.2 | `src/paper_manager/analyzer.py` | Create | `get_page_count(pdf_path: Path) -> int`: use pdfplumber to count pages. `get_file_size(pdf_path: Path) -> int`: return file size in bytes. `extract_text(pdf_path: Path) -> str`: use pdfplumber to extract full text (fallback path). `analyze_paper(pdf_path: Path, prompt: str, config: Config) -> dict`: check page count AND file size; if pages ≤ 100 AND size ≤ 30MB, send PDF as base64 document to Claude Messages API; otherwise extract text via pdfplumber and send as text content. Use `config.model` for model selection (default: `claude-opus-4-0-20250514` per spec). **Response format — use Anthropic `tool_use` (structured output)**: define a tool schema with required fields (`research_question: str`, `method: str`, `results: str`, `conclusions: str`, `limitations: str`, `keywords: list[str]`, `venue: str | None`) and pass it as `tools=[analysis_tool]` in the API call. Claude returns structured JSON via tool invocation — no regex parsing of free-text. On validation failure (missing required field), retry once; on second failure, write partial results with `status: incomplete` in YAML frontmatter. Prompt instructs Claude to extract `venue` from the paper content if available. Retry: 3 attempts with exponential backoff on API errors. `generate_tags(analysis: dict, config: Config) -> list[str]`: call Claude with analysis summary using `config.tag_model` (defaults to Sonnet for cost efficiency) to auto-generate 3-8 tags. Also uses tool_use with a simple `{tags: list[str]}` schema. |
| 3.3 | `tests/test_analyzer.py` | Create | Test page count routing logic, test response parsing, test tag generation format, test retry behavior |

**Verification**: Given a downloaded PDF, Claude returns a structured analysis dict; papers with >100 pages use text extraction path

### Phase 4: Markdown Output (Files: 2)
**Goal**: Write Obsidian-compatible Markdown with YAML frontmatter; edit-safe updates

| Step | File | Action | Details |
|------|------|--------|---------|
| 4.1 | `src/paper_manager/writer.py` | Create | `write_paper_note(analysis: dict, metadata: dict, tags: list, output_dir: Path, force: bool = False) -> Path`: construct YAML frontmatter (`title`, `authors` list, `date`, `arxiv_id`, `url`, `keywords` list, `tags` list, `venue`), write Markdown body with sections from analysis dict, save to `{output_dir}/{year}/{sanitized_title}.md`. If `force=True` and file exists, re-generate entirely. `sanitize_filename(title: str) -> str`: lowercase, hyphens for spaces, keep Unicode letters (CJK, accented chars) but remove filesystem-unsafe chars (`/\:*?"<>|`), truncate to 80 chars, use arxiv_id as fallback if result is empty. `find_existing(arxiv_id: str, papers_dir: Path) -> Path or None`: scan YAML frontmatter for duplicate arxiv_id. `update_frontmatter(md_path: Path, new_frontmatter: dict) -> None`: parse existing file at first `---`...`---` boundary, replace YAML frontmatter only, preserve everything below (user-edited body content safe). |
| 4.2 | `tests/test_writer.py` | Create | Test YAML format, filename sanitization, duplicate detection, frontmatter-only update preserves body |

**Verification**: Output file opens in Obsidian with correct properties; `update_frontmatter` preserves user body edits

### Phase 5: Git Sync (Files: 1)
**Goal**: Commit and push changes to GitHub

| Step | File | Action | Details |
|------|------|--------|---------|
| 5.1 | `src/paper_manager/sync.py` | Create | `sync_to_git(repo_dir: Path, message: str = None) -> bool`: (1) `git pull --rebase` to fetch remote changes first (multi-device support), (2) stage changes in `papers/` and `templates/`, (3) auto-generate commit message (e.g., "Add: paper-title-1, paper-title-2"), (4) commit, (5) `git push` to configured remote. `init_repo(repo_dir: Path, remote_url: str) -> Repo`: initialize git repo if not exists, add remote. Handle: no changes (return False), pull conflicts (abort rebase, warn user to resolve manually), push failures (warn + retry once). After pull, run `reindex` if new `.md` files arrived from remote. |

**Verification**: After `paper-manager sync`, `git log` shows a new commit and `git status` is clean

### Phase 6: Search / RAG (Files: 2)
**Goal**: Semantic search across paper notes

| Step | File | Action | Details |
|------|------|--------|---------|
| 6.1 | `src/paper_manager/search.py` | Create | `get_collection(chromadb_dir: Path) -> Collection`: get or create ChromaDB collection with default embedding function (`all-MiniLM-L6-v2`). `index_paper(md_path: Path, collection: Collection)`: read Markdown, chunk by sections (split on `## ` headers), upsert into collection with metadata (arxiv_id, title, tags, section_name). `search_papers(query: str, collection: Collection, n_results: int = 5) -> list[dict]`: query ChromaDB, return ranked results with title, relevance score, matched section. `reindex_all(papers_dir: Path, collection: Collection)`: clear collection, reindex all `.md` files in papers/. |
| 6.2 | `tests/test_search.py` | Create | Test indexing, search retrieval, reindex idempotency |

**Verification**: After indexing 3+ papers, `paper-manager search "attention mechanism"` returns relevant results

### Phase 7: CLI Integration (Files: 1)
**Goal**: Wire everything together into the Typer CLI

| Step | File | Action | Details |
|------|------|--------|---------|
| 7.1 | `src/paper_manager/cli.py` | Create | Typer app with commands: **`init`** (create config.yaml from example, create .obsidian/app.json with exclusion patterns for src/tests/, init git repo; idempotent), **`add`** (accept 1+ arxiv URLs, `--force` flag to re-process existing; sequential download with 3s delay → analyze → write → index; skip existing arxiv_ids unless `--force`), **`sync`** (pull --rebase → commit → push; reindex if remote brought new files), **`search`** (query ChromaDB, display results as formatted table with title, score, matched section), **`tag`** (re-tag papers via Claude — frontmatter-only update; supports `--limit N` and `--since YYYY-MM-DD` to avoid re-tagging entire library; each paper is a lightweight tag-only Claude call), **`reindex`** (rebuild ChromaDB from all .md files), **`config`** (show current config and validate API key). Progress bars via `typer.progressbar` for batch. Error handling: missing API key → clear message with `paper-manager init` instructions; network error → retry + skip with warning; invalid URL → skip with message; 404/withdrawn paper → skip with clear message. |

**Verification**: All CLI commands work end-to-end

### Phase 8: Default Template & Polish (Files: 2)
**Goal**: Production-ready default template and README

| Step | File | Action | Details |
|------|------|--------|---------|
| 8.1 | `templates/default.md` | Update | Finalize default prompt template with Zotero-inspired fields: Title, Authors, Date, Venue, Research Question, Background/Motivation, Method, Key Results, Conclusions, Limitations, Future Work, Keywords, Related Work. Include instructions for Claude: "Output as Markdown with these exact section headers. Be concise but complete." |
| 8.2 | `README.md` | Create | Installation (`pip install -e .`), quick start (`paper-manager init` → edit config.yaml → `paper-manager add <url>`), configuration (API keys via env var or config.yaml, model selection), usage examples for all commands, Obsidian setup (just open the folder), template customization guide, cross-platform notes |

**Verification**: A new user can follow README from scratch to working setup

---

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Claude API rate limits on batch | Batch processing delayed | Medium | 1s delay between Claude calls, retry with exponential backoff (3 attempts) |
| arxiv rate limiting / IP block | Downloads blocked | High (if no delay) | **3-second delay between all arxiv requests** (mandatory, arxiv ToS). Sequential batch only. |
| PDF >100 pages exceeds Claude limit | Analysis fails | Medium | **Check page count via pdfplumber before sending**. >100 pages → extract text, send as text content instead of PDF. Log warning to user. |
| PDF >32MB exceeds Claude request limit | Analysis fails | Low | Check file size; if >32MB, always use text extraction path |
| ChromaDB version incompatibility | Search broken | Low | Pin chromadb version range in pyproject.toml |
| Git merge conflicts on multi-device | Sync fails | Medium | On conflict, abort push and warn user to resolve manually; never force-push |
| YAML frontmatter breaks Obsidian | Notes unreadable | Low | Validate YAML before writing; escape special chars in titles/authors |
| API key leaked to git | Security vulnerability | High | **config.yaml is gitignored**; config.yaml.example (no secrets) is tracked; primary config path is `ANTHROPIC_API_KEY` env var |
| User edits Markdown body, then tag overwrites it | Data loss | Medium | **`tag` and `update_frontmatter` only modify YAML between `---` delimiters**, never touch body content |

---

## Verification Steps

1. **Unit tests**: `pytest tests/` — all modules have isolated tests with mocks for external APIs (including test_cli.py for init command)
2. **Integration test**: `paper-manager add https://arxiv.org/abs/1706.03762` (Attention Is All You Need) — verify full pipeline produces a valid Markdown note with correct frontmatter
3. **Batch test**: `paper-manager add <url1> <url2> <url3>` — verify 3 files created, total time ≥9s (rate limiting), all searchable
4. **Duplicate test**: Add same paper twice → verify second run skips with message; then `paper-manager add --force <same_url>` → verify re-processed
5. **Large paper test**: Test with a paper >100 pages → verify text extraction fallback activates and produces valid output
6. **Search test**: After adding 3+ papers, `paper-manager search "transformer architecture"` returns relevant results ranked by relevance
7. **Core scenario test (AC12)**: Add 5+ papers across different domains (NLP, CV, RL, etc.). Search with a vague concept: "that paper about making language models faster without losing quality" (not a title or keyword). Verify the correct paper (e.g., a distillation or pruning paper) appears in top 3 results. This tests the primary use case: "forgot paper name, search by idea."
8. **Tag safety test**: Manually edit a paper's Markdown body in Obsidian (add personal notes) → run `paper-manager tag --limit 1` → verify body is unchanged, only frontmatter tags updated
9. **Sync test**: After adding papers, `paper-manager sync` creates a git commit with descriptive message; on a second machine, `paper-manager sync` pulls the new files
10. **Cross-platform**: Run `paper-manager init` and `paper-manager add` on Windows — verify `pathlib.Path` handles backslashes correctly, git works, filenames with Unicode are valid
11. **Obsidian test**: Open `paper_project/` in Obsidian → verify frontmatter appears as properties, `src/` and `tests/` excluded after `init`, Dataview query works on paper properties
12. **Config test**: Run with `ANTHROPIC_API_KEY` env var (no config.yaml) → verify tool works; run without any key → verify clear error message pointing to `paper-manager init`
13. **Error handling test**: `paper-manager add https://arxiv.org/abs/0000.00000` (nonexistent) → verify graceful error message, no crash; `paper-manager add https://arxiv.org/abs/1234.56789` (withdrawn) → verify clear "paper withdrawn" message

---

## ADR: Architecture Decision Record

### Decision
Build a modular Python CLI package using Typer, with local Markdown files synced via git, ChromaDB for RAG search, and Claude API for paper analysis. Download papers directly from arxiv.org via httpx.

### Drivers
1. User wants fast development → Python has all needed libraries
2. User wants Obsidian compatibility → Markdown + YAML frontmatter is native to Obsidian
3. User wants cross-platform → Python + git + Obsidian all work on Win/Mac
4. User wants RAG → ChromaDB is the simplest local vector DB (zero config)
5. User wants git sync → 10K papers = ~50MB Markdown, well within GitHub free limits

### Alternatives Considered
1. **Notion API for storage**: Rejected — Markdown fidelity is lossy through block model conversion, API rate limits (3 req/s), $10+/month, higher integration complexity
2. **Obsidian Sync for multi-device**: Not needed — git push/pull achieves the same; user can add Obsidian Sync later ($4-5/month) if desired
3. **Monolithic script**: Rejected — while faster for initial MVP, 7+ responsibilities with planned growth (Zotero, web dashboard) make modular boundaries worth the ~15 min setup overhead
4. **Web UI (Flask/FastAPI)**: Rejected — user chose CLI + Obsidian; web UI is a non-goal for v1
5. **SQLite for metadata**: Rejected — YAML frontmatter in Markdown files serves the same purpose and is directly readable by Obsidian Dataview plugin
6. **HuggingFace Hub for PDF download**: Rejected — HF Hub's `hf_hub_download` is for HF repository files, not arxiv PDFs. Direct download from `export.arxiv.org` via httpx is simpler and has no unnecessary dependencies

### Why Chosen
The selected architecture (Python CLI + Markdown + git + ChromaDB + Obsidian) minimizes moving parts while satisfying all acceptance criteria. Zero external services required beyond GitHub (free) and Anthropic API (usage-based). Every component is replaceable: swap ChromaDB for FAISS, swap git for Obsidian Sync, swap Claude for another LLM — the Markdown files remain the source of truth.

### Consequences
- User must install Python 3.10+ and configure API key
- PDF processing costs per paper: ~$0.05-0.15 (Opus default per spec); user can switch to Sonnet (~$0.01-0.03) in config.yaml for cost savings. Model is configurable.
- ChromaDB adds ~100MB to disk for 10K papers (gitignored, local only)
- `sentence-transformers` adds ~500MB to the Python environment (one-time install for embedding model)
- No real-time sync — user must run `paper-manager sync` manually (pull + push)
- Batch downloads are rate-limited to 1 paper per 3 seconds (arxiv ToS compliance)
- Papers >100 pages or >30MB use text extraction fallback (slightly lower analysis quality vs. native PDF mode)
- `tag --limit N` allows controlled re-tagging to manage API costs at scale

### Follow-ups
- v2: Zotero import (read Zotero SQLite DB or BetterBibTeX JSON export)
- v2: Scheduled auto-tagging (cron or system scheduler)
- v2: Web dashboard for browsing (optional, if CLI proves insufficient)
- v2: Custom embedding models for domain-specific search quality
- v2: HuggingFace Hub integration for paper discovery/trending papers

---

## Changelog

### Iteration 2 (Critic Review Revisions)
- **Added** formal Spec Deviations section documenting HF Hub replacement with full rationale
- **Changed** default model to `claude-opus-4-0-20250514` per spec (was Sonnet); Sonnet documented as cost-saving option
- **Added** AC12: core scenario test ("forgot paper name, search by idea") with concrete verification
- **Changed** `sync` to pull-then-push (was push-only) for multi-device support
- **Added** `--force` flag on `add` command for re-processing existing papers
- **Added** `--limit N` and `--since` flags on `tag` command to control API costs at scale
- **Added** `sentence-transformers` to dependencies (ChromaDB embedding requirement)
- **Added** httpx timeout (60s) and 404/withdrawn paper handling in downloader
- **Added** 32MB file size check alongside 100-page check in analyzer
- **Added** Unicode-safe filename sanitization (keeps CJK/accented chars, falls back to arxiv_id)
- **Added** `test_cli.py` to test suite for init command testing
- **Added** Dataview compatibility note and README documentation guidance
- **Fixed** config.yaml creation flow: only `init` command creates config (not auto-copy on any run)
- **Added** venue extraction note: Claude extracts from paper content since arxiv API doesn't provide it
- **Added** verification steps: core scenario test, error handling test, multi-device sync test
- **Added** tag cost management: `generate_tags()` uses lightweight Sonnet call regardless of main model

### Iteration 2c (Critic Final — Response Format Gap)
- **Added** Claude `tool_use` structured output specification to analyzer.py (Step 3.2) — defines JSON schema for analysis response, validation on receipt, partial-result fallback with `status: incomplete` frontmatter flag
- **Added** `tool_use` schema for `generate_tags()` as well (consistent pattern)

### Iteration 2b (Architect Re-review Improvements)
- **Added** `tag_model` config field to config.yaml.example — makes secondary Sonnet dependency explicit and overridable
- **Fixed** Changelog Iteration 1 model default text (see superseded note below)

### Iteration 1 (Architect Review Revisions) — *Note: model default was changed to Opus in Iteration 2*
- **Removed** `huggingface-hub` from dependencies — phantom dep, not used in actual data flow
- **Added** PDF page-count validation in analyzer.py — falls back to text extraction for >100 pages (Claude API limit)
- **Added** arxiv rate limiting in downloader.py — 3-second delay between requests (arxiv ToS)
- **Split** config.yaml into config.yaml.example (tracked) + config.yaml (gitignored) — prevents API key leakage
- **Added** configurable Claude model identifier *(superseded: Iteration 2 changed default to Opus per spec)*
- **Added** `paper-manager init` command — creates .obsidian/ with file exclusion patterns for src/, tests/
- **Added** frontmatter-only update mode for `tag` command — preserves user-edited Markdown body content
- **Added** AC11 for >100 page PDF fallback verification
- **Updated** cost estimates to reflect Sonnet (default) vs Opus (configurable) pricing
- **Updated** batch AC4 to specify sequential processing with 3s delay
