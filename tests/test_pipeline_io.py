"""Tests for pipeline I/O safety layer."""
import json


def test_safe_write_json_creates_file(tmp_path):
    from deepaper.pipeline_io import safe_write_json
    path = tmp_path / "test.json"
    result = safe_write_json(str(path), {"key": "value"})
    assert result is True
    assert path.exists()
    data = json.loads(path.read_text())
    assert data == {"key": "value"}


def test_safe_write_json_creates_parent_dirs(tmp_path):
    from deepaper.pipeline_io import safe_write_json
    path = tmp_path / "nested" / "dir" / "test.json"
    result = safe_write_json(str(path), {"nested": True})
    assert result is True
    assert path.exists()


def test_safe_write_json_returns_false_on_failure():
    from deepaper.pipeline_io import safe_write_json
    result = safe_write_json("/nonexistent/readonly/test.json", {"fail": True})
    assert result is False


def test_safe_write_json_atomic_no_partial(tmp_path):
    from deepaper.pipeline_io import safe_write_json
    path = tmp_path / "test.json"
    safe_write_json(str(path), {"first": True})
    tmp_file = path.with_suffix(".tmp")
    assert not tmp_file.exists()


def test_safe_read_json_reads_valid(tmp_path):
    from deepaper.pipeline_io import safe_read_json
    path = tmp_path / "test.json"
    path.write_text('{"key": "value"}')
    result = safe_read_json(str(path))
    assert result == {"key": "value"}


def test_safe_read_json_returns_default_on_missing():
    from deepaper.pipeline_io import safe_read_json
    result = safe_read_json("/nonexistent/file.json", default={"fallback": True})
    assert result == {"fallback": True}


def test_safe_read_json_returns_default_on_corrupt(tmp_path):
    from deepaper.pipeline_io import safe_read_json
    path = tmp_path / "bad.json"
    path.write_text("{broken json content")
    result = safe_read_json(str(path), default=None)
    assert result is None


def test_safe_read_json_returns_default_on_empty(tmp_path):
    from deepaper.pipeline_io import safe_read_json
    path = tmp_path / "empty.json"
    path.write_text("")
    result = safe_read_json(str(path), default={})
    assert result == {}


def test_ensure_run_dir_creates_structure(tmp_path):
    from deepaper.pipeline_io import ensure_run_dir
    run_dir = ensure_run_dir(tmp_path, "2401.12345")
    assert run_dir.exists()
    assert run_dir == tmp_path / ".deepaper" / "runs" / "2401.12345"
