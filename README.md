# paper-manager

Personal arxiv paper manager. Paste an arxiv link, get a structured Markdown note with AI analysis, stored in an Obsidian-compatible vault synced via Git.

## Features

- **One command to add a paper**: `paper-manager add https://arxiv.org/abs/2301.00001`
- **Claude Opus analysis**: structured extraction of research question, method, results, limitations, and more
- **Obsidian vault**: notes live in `papers/YYYY/` with YAML frontmatter compatible with Dataview
- **Semantic search**: "forgot the paper name but remember the idea" — RAG via ChromaDB + sentence-transformers
- **Auto-tagging**: Claude generates classification tags for every paper
- **Git sync**: push your notes to a private GitHub/GitLab repo, pull on any machine

## Requirements

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)
- Git (optional, for sync)
- Obsidian (optional, for vault browsing)

## Installation

```bash
pip install -e .
```

## Setup

1. Copy `config.yaml.example` to `config.yaml` and add your API key, **or** run:

```bash
paper-manager init --git-remote https://github.com/you/my-papers.git
```

`init` creates `config.yaml`, `papers/`, and `.obsidian/app.json` (excludes `src/` and `tests/` from Obsidian indexing).

2. Edit `config.yaml`:

```yaml
anthropic_api_key: "sk-ant-..."
git_remote: "https://github.com/you/my-papers.git"
model: "claude-opus-4-6"
tag_model: "claude-opus-4-6"
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

Each paper goes through: metadata fetch → PDF download → Claude analysis → tag generation → Markdown note → ChromaDB index → PDF cleanup.

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

Useful after pulling notes from another machine (sync handles this automatically, but run reindex if the index gets out of sync).

### Show configuration

```bash
paper-manager config
```

Displays all settings and validates your API key.

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

## Research Question
...

## Background
...

## Method
...

## Results
...

## Conclusions
...

## Limitations
...

## Future Work
...
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
# Machine A — add papers and push
paper-manager add 2301.00001
paper-manager sync

# Machine B — pull and auto-reindex
paper-manager sync
```

## Configuration reference

| Key | Default | Description |
|-----|---------|-------------|
| `anthropic_api_key` | — | Required. Set via env var `ANTHROPIC_API_KEY` or in `config.yaml` |
| `model` | `claude-opus-4-6` | Model for full paper analysis |
| `tag_model` | `claude-opus-4-6` | Model for auto-tagging |
| `papers_dir` | `papers` | Directory for paper notes |
| `template` | `default` | Prompt template (filename without `.md` in `templates/`) |
| `chromadb_dir` | `.chromadb` | Local vector database directory |
| `git_remote` | — | Remote URL for `paper-manager sync` |

`config.yaml` is gitignored — your API key is never committed.
