"""Git sync operations: pull + commit + push for multi-device paper sync."""
from __future__ import annotations

from pathlib import Path

import git


def init_repo(repo_dir: Path, remote_url: str) -> git.Repo:
    """Initialize or open a git repo at repo_dir, configuring the remote.

    Args:
        repo_dir: Directory in which to init or open the repo.
        remote_url: Remote URL to set as "origin". Ignored if empty string.

    Returns:
        The git.Repo object for repo_dir.
    """
    is_new = not (repo_dir / ".git").exists()

    if is_new:
        repo = git.Repo.init(repo_dir)
    else:
        repo = git.Repo(repo_dir)

    # Configure remote
    if remote_url:
        try:
            origin = repo.remote("origin")
            # Update URL if it differs
            if origin.url != remote_url:
                origin.set_url(remote_url)
        except ValueError:
            # No remote named "origin" exists
            repo.create_remote("origin", remote_url)

    # Create an initial commit for new repos
    if is_new:
        files_to_add: list[str] = []
        for candidate in (".gitignore", "config.yaml.example"):
            if (repo_dir / candidate).exists():
                files_to_add.append(candidate)
        if files_to_add:
            repo.index.add(files_to_add)
            try:
                repo.index.commit("Initial commit")
            except git.GitCommandError:
                pass

    return repo


def get_changed_papers(repo: git.Repo, papers_dir: str = "papers") -> list[str]:
    """Return file names (not paths) of new/modified .md files in papers_dir.

    Checks both staged and unstaged changes.

    Args:
        repo: The git.Repo to inspect.
        papers_dir: Subdirectory name containing paper markdown files.

    Returns:
        List of file names (e.g. ["2301.00001.md"]).
    """
    changed: set[str] = set()

    # Unstaged changes (working tree vs index)
    for diff in repo.index.diff(None):
        path = diff.a_path or diff.b_path
        if path and path.startswith(papers_dir + "/") and path.endswith(".md"):
            changed.add(Path(path).name)

    # Staged changes (index vs HEAD) — handle empty repo (no commits yet)
    try:
        for diff in repo.index.diff("HEAD"):
            path = diff.a_path or diff.b_path
            if path and path.startswith(papers_dir + "/") and path.endswith(".md"):
                changed.add(Path(path).name)
    except git.BadName:
        # No commits yet; every staged file is new
        for entry in repo.index.entries:
            entry_path = entry[0]
            if entry_path.startswith(papers_dir + "/") and entry_path.endswith(".md"):
                changed.add(Path(entry_path).name)

    # Untracked files
    for untracked in repo.untracked_files:
        if untracked.startswith(papers_dir + "/") and untracked.endswith(".md"):
            changed.add(Path(untracked).name)

    return sorted(changed)


def sync_to_git(
    repo_dir: Path,
    message: str | None = None,
    papers_dir: str = "papers",
) -> bool:
    """Pull, stage, commit, and push changes to the git remote.

    Args:
        repo_dir: Root directory of the git repository.
        message: Commit message override. Auto-generated if None.
        papers_dir: Subdirectory containing paper markdown files.

    Returns:
        True on full success, False if any step failed or there was nothing
        to commit.
    """
    import typer

    # Open repo
    try:
        repo = git.Repo(repo_dir)
    except git.InvalidGitRepositoryError:
        typer.echo(
            f"Not a git repository: {repo_dir}\n"
            "Run: paper-manager init --git-remote <url>",
            err=True,
        )
        raise

    # ------------------------------------------------------------------
    # Step 1 — Pull
    # ------------------------------------------------------------------
    has_remote = bool(repo.remotes)
    if not has_remote:
        typer.echo("Warning: no remote configured — skipping pull.", err=True)
    else:
        # Determine branch name
        try:
            branch = repo.active_branch.name
        except TypeError:
            branch = "main"

        # Prefer "main", fall back to "master"
        remote = repo.remote("origin")
        remote_branches = [ref.remote_head for ref in remote.refs] if remote.refs else []
        if branch not in remote_branches:
            branch = "master" if "master" in remote_branches else branch

        try:
            repo.git.pull("--rebase", "origin", branch)
        except git.GitCommandError as exc:
            err_str = str(exc).lower()
            if "conflict" in err_str or "rebase" in err_str:
                try:
                    repo.git.rebase("--abort")
                except git.GitCommandError:
                    pass
                typer.echo(
                    "Warning: pull --rebase encountered a conflict. "
                    "Rebase aborted. Resolve conflicts manually.",
                    err=True,
                )
                return False
            # Network / unreachable remote — warn but continue
            typer.echo(
                f"Warning: could not reach remote (pull skipped): {exc}",
                err=True,
            )

    # ------------------------------------------------------------------
    # Step 2 — Stage papers/ and templates/
    # ------------------------------------------------------------------
    dirs_to_stage: list[str] = []
    for d in (papers_dir, "templates"):
        if (repo_dir / d).exists():
            dirs_to_stage.append(d)

    if dirs_to_stage:
        try:
            repo.index.add(dirs_to_stage)
        except git.GitCommandError as exc:
            typer.echo(f"Warning: could not stage files: {exc}", err=True)

    # ------------------------------------------------------------------
    # Step 3 — Commit
    # ------------------------------------------------------------------
    changed_files = get_changed_papers(repo, papers_dir)

    # Build auto commit message
    if message is None:
        if not changed_files:
            message = "Sync papers"
        elif len(changed_files) <= 5:
            message = "Add: " + ", ".join(changed_files)
        else:
            shown = ", ".join(changed_files[:2])
            extra = len(changed_files) - 2
            message = f"Add: {shown} (+{extra} more)"

    # Check whether anything is actually staged
    try:
        staged_diffs = repo.index.diff("HEAD")
    except git.BadName:
        # No commits yet — anything in the index is staged
        staged_diffs = list(repo.index.entries)

    if not staged_diffs:
        typer.echo("Nothing to commit.")
        return False

    try:
        repo.index.commit(message)
    except git.GitCommandError as exc:
        typer.echo(f"Warning: commit failed: {exc}", err=True)
        return False

    # ------------------------------------------------------------------
    # Step 4 — Push
    # ------------------------------------------------------------------
    if not has_remote:
        typer.echo("Warning: no remote configured — skipping push.", err=True)
        return False

    try:
        repo.remote("origin").push()
    except git.GitCommandError as exc:
        typer.echo(f"Warning: push failed: {exc}", err=True)
        return False

    return True


def get_new_files_from_pull(repo: git.Repo, before_sha: str) -> list[Path]:
    """Return paths of .md files added by a pull since before_sha.

    Compares the current HEAD to before_sha and returns newly added
    markdown files, used to trigger re-indexing after a pull.

    Args:
        repo: The git.Repo to inspect.
        before_sha: The commit SHA before the pull was executed.

    Returns:
        List of absolute Path objects for new .md files.
    """
    try:
        before_commit = repo.commit(before_sha)
        after_commit = repo.head.commit
        diffs = before_commit.diff(after_commit)
        new_files: list[Path] = []
        for diff in diffs:
            # A = added file
            if diff.change_type == "A" and diff.b_path and diff.b_path.endswith(".md"):
                new_files.append(Path(repo.working_dir) / diff.b_path)
        return new_files
    except git.GitCommandError as exc:
        import typer
        typer.echo(f"Warning: could not diff commits: {exc}", err=True)
        return []
    except ValueError as exc:
        import typer
        typer.echo(f"Warning: invalid SHA {before_sha!r}: {exc}", err=True)
        return []
