"""Safe JSON I/O and run directory management for the pipeline."""
from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger("deepaper")


def safe_write_json(path: str, data: dict) -> bool:
    """Atomic JSON write. Returns True on success, False on failure."""
    try:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".tmp")
        tmp.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        tmp.rename(p)
        return True
    except Exception as e:
        logger.warning("JSON write failed: %s: %s", path, e)
        try:
            Path(path).with_suffix(".tmp").unlink(missing_ok=True)
        except Exception:
            pass
        return False


def safe_read_json(path: str, default=None):
    """Read JSON file. Returns default on any failure."""
    try:
        text = Path(path).read_text(encoding="utf-8")
        if not text.strip():
            return default
        return json.loads(text)
    except (FileNotFoundError, json.JSONDecodeError, OSError) as e:
        logger.warning("JSON read failed: %s: %s", path, e)
        return default


def ensure_run_dir(project_root: Path, arxiv_id: str) -> Path:
    """Create and return .deepaper/runs/{arxiv_id}/ directory."""
    run_dir = project_root / ".deepaper" / "runs" / arxiv_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir
