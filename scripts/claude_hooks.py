"""Claude Code hooks for this repo (wired up in .claude/settings.json).

One script, three modes, each reading the hook's JSON from stdin:

  pre-commit-scan  PreToolUse (Bash/PowerShell). If the command runs `git commit`,
                   run scripts/public_scan.py first. Exit 2 blocks the commit on a
                   hit AND on any scan error (fail closed); stderr goes to Claude.
  post-edit-ruff   PostToolUse (file edits). `ruff check` the edited Python file
                   (never --fix). Reports to Claude; never blocks.
  stop-pytest      Stop. If there are uncommitted changes AND a .py file changed since
                   the last run (fingerprint in .claude/stop-pytest.state.json), run
                   pytest (60 s cap) and show Thomas the result, unless it's the same
                   as last time. Never blocks: red tests are often intentional here
                   (test-first exercises Thomas is solving). /wrap runs the full suite.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

PROJECT = Path(
    os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[1]
)
PYTHON = sys.executable  # the venv's python: settings.json launches us with it
LINT_SUFFIXES = {".py", ".pyi", ".ipynb"}
STATE_FILE = PROJECT / ".claude" / "stop-pytest.state.json"  # gitignored
PYTEST_TIMEOUT = 60  # seconds

# `git [global options] commit`, including `git -C <path> commit` and `-c k=v`.
GIT_COMMIT = re.compile(
    r"(?<![\w./-])git(?:\.exe)?(?:\s+(?:-C|-c)\s+(?:\"[^\"]*\"|'[^']*'|\S+)"
    r"|\s+--?[\w-]+(?:=\S+)?)*\s+commit\b"
)


def is_git_commit(command: str) -> bool:
    """True if any part of a shell command runs `git commit`."""
    return bool(GIT_COMMIT.search(command))


def repo_for(command: str) -> Path:
    """The repo the commit runs in: the `git -C <path>` target, else the project."""
    match = re.search(r"\bgit(?:\.exe)?\s+-C\s+(\"[^\"]*\"|'[^']*'|\S+)", command)
    if match:
        raw = match.group(1).strip("\"'")
        # Git Bash writes C:\x as /c/x; Windows Python needs the drive letter back.
        if os.name == "nt":
            raw = re.sub(r"^/([a-zA-Z])(?=/|$)", r"\1:", raw)
        path = Path(raw)
        return path if path.is_absolute() else PROJECT / path
    return PROJECT


def pre_commit_scan(event: dict) -> int:
    command = (event.get("tool_input") or {}).get("command") or ""
    if not is_git_commit(command):
        return 0
    repo = repo_for(command)
    scanner = PROJECT / "scripts" / "public_scan.py"
    try:
        result = subprocess.run(
            [PYTHON, str(scanner)],
            cwd=repo,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as err:
        print(
            f"Commit blocked: the public-repo scan could not run ({err}).",
            file=sys.stderr,
        )
        return 2
    if result.returncode == 0:
        return 0
    if result.returncode == 1:
        print(
            "Commit blocked by the public-repo scan. Remove these before committing:\n"
            + result.stdout,
            file=sys.stderr,
        )
    else:
        print(
            "Commit blocked: the public-repo scan could not run "
            f"(exit {result.returncode}).\n{result.stdout}{result.stderr}",
            file=sys.stderr,
        )
    return 2  # fail closed: hits and errors both block


def post_edit_ruff(event: dict) -> int:
    tool_input = event.get("tool_input") or {}
    file_path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    path = Path(file_path)
    if path.suffix not in LINT_SUFFIXES or not path.exists():
        return 0
    try:
        result = subprocess.run(
            [PYTHON, "-m", "ruff", "check", str(path)],
            cwd=PROJECT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as err:
        report(f"ruff check could not run on {path.name}: {err}", to_claude=True)
        return 0
    if result.returncode != 0:
        output = (result.stdout + result.stderr).strip()
        report(
            f"ruff check {path.name} (report only, not fixed):\n{output}",
            to_claude=True,
        )
    return 0


def git_lines(*args: str) -> list[str] | None:
    """Output lines of a git command run in the project, or None if it failed."""
    result = subprocess.run(
        ["git", *args],
        cwd=PROJECT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout.splitlines() if result.returncode == 0 else None


def python_fingerprint() -> str:
    """Path, size and modified time of every tracked or new (not ignored) .py file."""
    files = git_lines("ls-files", "--cached", "--others", "--exclude-standard")
    parts = []
    for name in sorted(files or []):
        path = PROJECT / name
        if path.suffix == ".py" and path.exists():
            info = path.stat()
            parts.append(f"{name}:{info.st_size}:{info.st_mtime_ns}")
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


def load_state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_state(fingerprint: str, summary: str) -> None:
    state = {"fingerprint": fingerprint, "summary": summary}
    STATE_FILE.write_text(json.dumps(state), encoding="utf-8")


def pytest_summary(stdout: str, returncode: int) -> str:
    """pytest's last line without the timing ('in 0.12s'), so results compare."""
    if returncode == 5:
        return "no tests collected"
    lines = [line.strip(" =") for line in stdout.splitlines() if line.strip()]
    last = lines[-1] if lines else f"exit {returncode}"
    return re.sub(r"\s+in [\d.]+s\b.*$", "", last)


def stop_pytest(event: dict) -> int:
    """Run pytest only when .py files changed; speak only when the result changed."""
    if event.get("stop_hook_active"):
        return 0
    if not git_lines("status", "--porcelain"):  # clean tree (or git failed)
        return 0
    fingerprint = python_fingerprint()
    previous = load_state()
    if fingerprint == previous.get("fingerprint"):
        return 0  # no .py file changed since the last run: stay silent
    try:
        result = subprocess.run(
            [PYTHON, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
            cwd=PROJECT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=PYTEST_TIMEOUT,
        )
        summary = pytest_summary(result.stdout, result.returncode)
    except subprocess.TimeoutExpired:
        summary = f"timed out after {PYTEST_TIMEOUT}s (run it in /wrap)"
    except OSError as err:
        summary = f"could not run ({err})"
    save_state(fingerprint, summary)
    if summary != previous.get("summary"):
        report(f"pytest: {summary}", to_claude=False)
    return 0  # never block: red tests can be an exercise in progress


def report(message: str, *, to_claude: bool) -> None:
    """Non-blocking output: additionalContext reaches Claude, systemMessage the user."""
    payload: dict = {"systemMessage": message}
    if to_claude:
        payload["hookSpecificOutput"] = {
            "hookEventName": "PostToolUse",
            "additionalContext": message,
        }
    print(json.dumps(payload))


MODES = {
    "pre-commit-scan": pre_commit_scan,
    "post-edit-ruff": post_edit_ruff,
    "stop-pytest": stop_pytest,
}


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] not in MODES:
        print(f"usage: claude_hooks.py {{{'|'.join(MODES)}}}", file=sys.stderr)
        return 1
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        event = {}
    if argv[1] == "pre-commit-scan" and not event:
        print("Commit check could not read the hook input; blocking.", file=sys.stderr)
        return 2
    return MODES[argv[1]](event)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
