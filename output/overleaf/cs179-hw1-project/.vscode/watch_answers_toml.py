#!/usr/bin/env python3
from __future__ import annotations

import fcntl
import subprocess
import sys
import time
from pathlib import Path

POLL_INTERVAL_SECONDS = 0.5


def acquire_single_instance_lock(workspace_root: Path):
    lock_path = workspace_root / ".vscode" / "watch_answers_toml.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_file = lock_path.open("w", encoding="utf-8")
    try:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("watcher: already running", flush=True)
        lock_file.close()
        return None
    lock_file.write(f"{time.time()}\n")
    lock_file.flush()
    return lock_file


def get_mtime_ns(path: Path) -> int:
    if not path.exists():
        return -1
    return path.stat().st_mtime_ns


def run_build(workspace_root: Path) -> int:
    build_script = workspace_root / ".vscode" / "build_hw1.py"
    main_tex = workspace_root / "source" / "main.tex"
    cmd = [sys.executable, str(build_script), str(main_tex)]
    print(f"watcher: build start ({time.strftime('%H:%M:%S')})", flush=True)
    result = subprocess.run(cmd, cwd=workspace_root, check=False)
    print(f"watcher: build exit code {result.returncode}", flush=True)
    return result.returncode


def main() -> int:
    workspace_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    answers_toml = workspace_root / "source" / "answers.toml"

    print("watcher: started", flush=True)
    lock_file = acquire_single_instance_lock(workspace_root)
    if lock_file is None:
        print("watcher: ready", flush=True)
        return 0
    if not answers_toml.exists():
        print(f"watcher: missing {answers_toml}", flush=True)
        return 1

    last_mtime = get_mtime_ns(answers_toml)
    print("watcher: ready", flush=True)

    while True:
        time.sleep(POLL_INTERVAL_SECONDS)
        current_mtime = get_mtime_ns(answers_toml)
        if current_mtime == last_mtime:
            continue

        # wait for writes to settle
        time.sleep(0.2)
        settled_mtime = get_mtime_ns(answers_toml)
        if settled_mtime != current_mtime:
            # still changing; pick up on next loop
            continue

        last_mtime = settled_mtime
        run_build(workspace_root)


if __name__ == "__main__":
    raise SystemExit(main())
