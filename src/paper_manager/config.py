"""Configuration loading for paper-manager.

Priority order: environment variables > config.yaml > defaults.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class Config:
    api_key: str
    model: str = "claude-opus-4-6"
    tag_model: str = "claude-opus-4-6"
    git_remote: str = ""
    papers_dir: str = "papers"
    template: str = "default"
    chromadb_dir: str = ".chromadb"

    # Derived paths (set after init)
    root_dir: Path = field(default_factory=Path.cwd)

    @property
    def papers_path(self) -> Path:
        return self.root_dir / self.papers_dir

    @property
    def chromadb_path(self) -> Path:
        return self.root_dir / self.chromadb_dir

    @property
    def templates_path(self) -> Path:
        return self.root_dir / "templates"

    @property
    def tmp_path(self) -> Path:
        return self.root_dir / "tmp"


def load_config(root_dir: Path | None = None) -> Config:
    """Load configuration from environment variables and config.yaml.

    Args:
        root_dir: Project root directory. Defaults to current working directory.

    Returns:
        Config instance with all settings resolved.

    Raises:
        SystemExit: If required config (API key) is missing.
    """
    if root_dir is None:
        root_dir = Path.cwd()

    config_path = root_dir / "config.yaml"
    file_config: dict = {}

    if config_path.exists():
        with open(config_path, encoding="utf-8") as f:
            file_config = yaml.safe_load(f) or {}
    elif (root_dir / "config.yaml.example").exists():
        # config.yaml doesn't exist yet — user needs to run init
        pass

    # API key is optional — analysis now uses Claude Code CLI (Max subscription)
    api_key = (
        os.environ.get("ANTHROPIC_API_KEY")
        or file_config.get("anthropic_api_key", "")
    )

    # Warn if config.yaml is missing entirely
    if not config_path.exists():
        import typer
        typer.echo(
            "No config.yaml found. Run: paper-manager init",
            err=True,
        )
        raise typer.Exit(1)

    return Config(
        api_key=api_key,
        model=os.environ.get("PAPER_MANAGER_MODEL") or file_config.get("model", "claude-opus-4-6"),
        tag_model=file_config.get("tag_model", "claude-opus-4-6"),
        git_remote=file_config.get("git_remote", ""),
        papers_dir=file_config.get("papers_dir", "papers"),
        template=file_config.get("template", "default"),
        chromadb_dir=file_config.get("chromadb_dir", ".chromadb"),
        root_dir=root_dir,
    )
