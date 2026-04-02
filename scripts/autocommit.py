#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import os
import subprocess
import sys
import time
from pathlib import Path


def run_git(
    args: list[str],
    *,
    cwd: Path,
    check: bool = False,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        check=check,
        capture_output=True,
        text=True,
    )


def repo_root(path: Path) -> Path:
    result = run_git(["rev-parse", "--show-toplevel"], cwd=path, check=True)
    return Path(result.stdout.strip())


def git_dir(path: Path) -> Path:
    result = run_git(["rev-parse", "--git-dir"], cwd=path, check=True)
    raw = result.stdout.strip()
    git_path = Path(raw)
    return git_path if git_path.is_absolute() else (path / git_path)


def repo_busy(git_path: Path) -> bool:
    markers = [
        git_path / "MERGE_HEAD",
        git_path / "CHERRY_PICK_HEAD",
        git_path / "REBASE_HEAD",
        git_path / "rebase-apply",
        git_path / "rebase-merge",
    ]
    return any(marker.exists() for marker in markers)


def working_tree_dirty(path: Path) -> bool:
    result = run_git(["status", "--porcelain"], cwd=path)
    return bool(result.stdout.strip())


def current_branch(path: Path) -> str:
    result = run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=path, check=True)
    return result.stdout.strip()


def changed_paths(path: Path) -> set[str]:
    paths: set[str] = set()
    for args in (
        ["diff", "--name-only"],
        ["diff", "--cached", "--name-only"],
        ["ls-files", "--others", "--exclude-standard"],
    ):
        result = run_git(args, cwd=path)
        for line in result.stdout.splitlines():
            name = line.strip()
            if name:
                paths.add(name)
    return paths


def last_change_mtime(path: Path, relpaths: set[str]) -> float | None:
    latest: float | None = None
    for rel in relpaths:
        try:
            stat = (path / rel).stat()
        except FileNotFoundError:
            continue
        if latest is None or stat.st_mtime > latest:
            latest = stat.st_mtime
    return latest


def staged_changes_exist(path: Path) -> bool:
    result = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=str(path))
    if result.returncode == 0:
        return False
    if result.returncode == 1:
        return True
    raise RuntimeError("git diff --cached --quiet failed")


def commit_message(prefix: str) -> str:
    now = dt.datetime.now().astimezone()
    return f"{prefix} {now:%Y-%m-%d %H:%M:%S %Z}"


def push_if_configured(path: Path) -> None:
    upstream = run_git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], cwd=path)
    if upstream.returncode != 0:
        print("note: no upstream configured; skipping push", file=sys.stderr)
        return
    result = subprocess.run(["git", "push"], cwd=str(path))
    if result.returncode != 0:
        print("warning: git push failed", file=sys.stderr)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Auto-commit (and optionally push) after a period of inactivity.")
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Path inside the target git repo.")
    parser.add_argument(
        "--idle-seconds",
        type=int,
        default=300,
        help="Only commit if the newest changed file is at least this old (seconds).",
    )
    parser.add_argument(
        "--message-prefix",
        default="auto: save",
        help="Commit message prefix (timestamp is appended).",
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Push after creating an auto-commit (only when a commit was made).",
    )
    parser.add_argument(
        "--allow-detached",
        action="store_true",
        help="Allow committing on a detached HEAD (default: skip).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would happen but do not commit or push.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    repo = repo_root(args.repo.resolve())
    git_path = git_dir(repo)

    if repo_busy(git_path):
        print("note: repo is mid-merge/rebase; skipping", file=sys.stderr)
        return 0

    if not working_tree_dirty(repo):
        return 0

    branch = current_branch(repo)
    if branch == "HEAD" and not args.allow_detached:
        print("note: detached HEAD; skipping (use --allow-detached to override)", file=sys.stderr)
        return 0

    paths = changed_paths(repo)
    mtime = last_change_mtime(repo, paths)
    now = time.time()

    if mtime is not None and (now - mtime) < args.idle_seconds:
        return 0

    msg = commit_message(args.message_prefix)
    if args.dry_run:
        print(f"would commit in {repo}: {msg}")
        if args.push:
            print("would push")
        return 0

    add_result = subprocess.run(["git", "add", "-A"], cwd=str(repo))
    if add_result.returncode != 0:
        print("warning: git add failed", file=sys.stderr)
        return 1

    if not staged_changes_exist(repo):
        return 0

    commit_result = subprocess.run(["git", "commit", "-m", msg], cwd=str(repo))
    if commit_result.returncode != 0:
        print("warning: git commit failed", file=sys.stderr)
        return 1

    if args.push:
        push_if_configured(repo)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

