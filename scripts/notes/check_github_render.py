#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path("/Users/jensonphan/cs179")
DEFAULT_PATH = ROOT / "02_probability_main" / "README.md"
DEFAULT_CONTEXT = "jensonp/cs179-chapter-2-probability"
API_URL = "https://api.github.com/markdown"
PAGE_TEMPLATE = "https://github.com/{context}/blob/{branch}/{path}"
USER_AGENT = "codex-github-render-check"


def post_markdown_to_github(path: Path, context: str, timeout: int) -> str:
    payload = json.dumps(
        {
            "text": path.read_text(),
            "mode": "gfm",
            "context": context,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/vnd.github+json",
            "User-Agent": USER_AGENT,
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def fetch_github_page(url: str, timeout: int) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def report_api_checks(path: Path, html: str) -> int:
    errors = 0
    math_tag_count = html.count("<math-renderer")
    print(f"[API] {path}")
    print(f"      GitHub API returned {math_tag_count} math-renderer tag(s).")
    if "Unable to render expression." in html:
        print("      [ERROR] GitHub API HTML already contains a render failure marker.")
        errors += 1
    if "$$" in html or "$" in html:
        # The API keeps raw math delimiters inside <math-renderer>; that is expected.
        print("      Note: raw math delimiters remain inside <math-renderer> tags until GitHub's page layer renders them.")
    return errors


def report_live_checks(url: str, html: str) -> int:
    errors = 0
    print(f"[LIVE] {url}")
    if "Unable to render expression." in html:
        count = html.count("Unable to render expression.")
        print(f"      [ERROR] Live GitHub page shows {count} render failure marker(s).")
        errors += 1
    else:
        print("      No live GitHub render failure markers found.")
    if "math-error" in html:
        count = html.count("math-error")
        print(f"      [ERROR] Live GitHub page contains {count} math-error marker(s).")
        errors += 1
    return errors


def build_live_url(context: str, branch: str, repo_path: str) -> str:
    quoted_path = urllib.parse.quote(repo_path)
    return PAGE_TEMPLATE.format(context=context, branch=branch, path=quoted_path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check a markdown file with GitHub's own markdown API and, optionally, "
            "the live rendered GitHub page."
        )
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=str(DEFAULT_PATH),
        help="Local markdown file to check.",
    )
    parser.add_argument(
        "--context",
        default=DEFAULT_CONTEXT,
        help="GitHub repo context in owner/repo form.",
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="Branch name for live page checks.",
    )
    parser.add_argument(
        "--repo-path",
        help=(
            "Repo-relative path for the live GitHub page check. "
            "If omitted, the script only uses the GitHub markdown API."
        ),
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="Network timeout in seconds.",
    )
    args = parser.parse_args()

    path = Path(args.path)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        print(f"[ERROR] missing file: {path}")
        return 1

    total_errors = 0

    try:
        api_html = post_markdown_to_github(path, args.context, args.timeout)
        total_errors += report_api_checks(path, api_html)
    except urllib.error.URLError as exc:
        print(f"[ERROR] GitHub markdown API request failed: {exc}")
        return 1

    if args.repo_path:
        live_url = build_live_url(args.context, args.branch, args.repo_path)
        try:
            live_html = fetch_github_page(live_url, args.timeout)
            total_errors += report_live_checks(live_url, live_html)
        except urllib.error.URLError as exc:
            print(f"[ERROR] Live GitHub page request failed: {exc}")
            return 1

    if total_errors == 0:
        print("PASS: GitHub renderer checks found no live render failures.")
        return 0

    print(f"FAIL: {total_errors} GitHub render issue(s) found.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
