# paper-manager

Personal arxiv paper manager. Paste an arxiv link, get a structured Markdown note with AI deep analysis, stored in an Obsidian-compatible vault synced via Git.

## Features

- **One command to add a paper**: `paper-manager add https://arxiv.org/abs/2301.00001`
- **Claude Code deep analysis**: structured 7-section deep dive (executive summary, motivation, methodology with pseudocode, experiments, critical review, mechanism transfer analysis, background context)
- **PDF figure extraction**: automatically detects and renders key figure/table pages as images for visual analysis
- **Obsidian vault**: notes live in `papers/YYYY/` with YAML frontmatter compatible with Dataview
- **Semantic search**: "forgot the paper name but remember the idea" -- RAG via ChromaDB + sentence-transformers
- **Auto-tagging**: Claude generates classification tags for every paper
- **Git sync**: push your notes to a private GitHub/GitLab repo, pull on any machine
- **No API billing**: uses Claude Code CLI (Max subscription), not per-token API calls

## Requirements

- Python 3.10+
- [Claude Code](https://claude.ai/code) CLI installed and authenticated (Max subscription)
- Git (optional, for sync)
- Obsidian (optional, for vault browsing)

## Installation

```bash
pip install -e .
```

## Setup

1. Run init to create config and directories:

```bash
paper-manager init --git-remote https://github.com/you/my-papers.git
```

`init` creates `config.yaml`, `papers/`, and `.obsidian/app.json`.

2. Edit `config.yaml` (optional -- most defaults work out of the box):

```yaml
git_remote: "https://github.com/you/my-papers.git"
```

## Usage

### Add papers

```bash
# Single paper
paper-manager add https://arxiv.org/abs/2301.00001

# Multiple papers
paper-manager add 2301.00001 2301.00002 2301.00003

# HuggingFace papers page also works
paper-manager add https://huggingface.co/papers/2301.00001

# Re-analyze an existing paper
paper-manager add --force https://arxiv.org/abs/2301.00001
```

Each paper goes through: metadata fetch -> PDF download -> figure page extraction -> Claude Code deep analysis -> tag generation -> Markdown note -> ChromaDB index -> cleanup.

### Search

```bash
paper-manager search "attention mechanism for long sequences"
paper-manager search "contrastive learning vision" --n 10
```

Results show title, similarity score, matched section snippet, and arxiv ID.

### Sync to Git

```bash
paper-manager sync
paper-manager sync --message "Add three NLP papers"
```

Runs `git pull --rebase` first, then commits and pushes. New files pulled from remote are automatically indexed.

### Re-tag papers

```bash
# Re-tag all papers
paper-manager tag

# Re-tag only recent papers
paper-manager tag --since 2024-01-01

# Re-tag at most 10 papers
paper-manager tag --limit 10
```

### Rebuild search index

```bash
paper-manager reindex
```

### Show configuration

```bash
paper-manager config
```

Displays all settings and validates Claude Code CLI availability.

## Analysis output

Each note contains a Zotero-compatible YAML frontmatter plus a 7-section deep analysis:

| Section | Content |
|---------|---------|
| Executive Summary | TL;DR, mental model analogy, core mechanism in one line |
| Motivation & First Principles | Pain points, key insight with causal chain, intuitive explanation |
| Methodology | Intuitive walk-through with figures, formal spec with pseudocode, design decisions, potential confusions |
| Experiments & Attribution | Quantitative gains, ablation ranking, credibility check |
| Critical Review | Hidden costs, engineering pitfalls, connections to existing techniques |
| Mechanism Transfer Analysis | Mechanism decomposition, cross-domain transfer prescriptions, mechanism family tree |
| Background Context | (optional) Referenced techniques and common practices |

## Figure extraction

The analyzer automatically:
1. Scans the PDF for pages containing figures/tables (bitmap images, vector graphics, captions)
2. Prioritizes main body pages over appendix
3. Renders up to 20 key pages as JPEG images
4. Passes them to Claude Code for visual analysis
5. Cleans up temporary images after analysis

## Note format

Notes are stored as `papers/YYYY/paper-title.md` with YAML frontmatter:

```yaml
---
title: "Attention Is All You Need"
authors: [Ashish Vaswani, ...]
date: "2017-06-12"
arxiv_id: "1706.03762"
url: "https://arxiv.org/abs/1706.03762"
venue: "NeurIPS 2017"
keywords: [transformer, attention, NLP, sequence-to-sequence]
tags: [NLP, deep-learning, transformer]
status: complete
---
```

## Obsidian

Open the project root as an Obsidian vault. Use [Dataview](https://github.com/blacksmithgu/obsidian-dataview) to query notes:

```dataview
TABLE date, venue, tags
FROM "papers"
WHERE contains(tags, "NLP")
SORT date DESC
```

## Multi-device sync

```bash
# Machine A -- add papers and push
paper-manager add 2301.00001
paper-manager sync

# Machine B -- pull and auto-reindex
paper-manager sync
```

## Configuration reference

| Key | Default | Description |
|-----|---------|-------------|
| `anthropic_api_key` | — | Optional. Only needed if using API directly |
| `model` | `claude-opus-4-6` | Model name (for display/logging) |
| `tag_model` | `claude-opus-4-6` | Model name for auto-tagging (display only) |
| `papers_dir` | `papers` | Directory for paper notes |
| `template` | `default` | Prompt template (filename without `.md` in `templates/`) |
| `chromadb_dir` | `.chromadb` | Local vector database directory |
| `git_remote` | — | Remote URL for `paper-manager sync` |

`config.yaml` is gitignored -- your settings are never committed.

## Customizing the analysis prompt

Edit `templates/default.md` to customize the analysis structure. You can also create new templates (e.g. `templates/my-style.md`) and set `template: "my-style"` in `config.yaml`.
