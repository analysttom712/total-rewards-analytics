"""Tests for scripts/claude_hooks.py (tooling, not a learning exercise)."""

import importlib.util
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "claude_hooks.py"
_spec = importlib.util.spec_from_file_location("claude_hooks", SCRIPT)
claude_hooks = importlib.util.module_from_spec(_spec)
sys.modules["claude_hooks"] = claude_hooks
_spec.loader.exec_module(claude_hooks)

# Split from the subcommand so shell guards don't read test data as commands.
GIT = "git"


@pytest.mark.parametrize(
    "command",
    [
        GIT + ' commit -m "Add tests"',
        GIT + ' -C /c/repo commit -m "Add tests"',
        GIT + ' -C "C:/My Repo" commit -m "x"',
        GIT + " -c user.name=x commit -m y",
        GIT + " add a.py && " + GIT + ' commit -m "x"',
        GIT + ".exe commit --amend",
    ],
)
def test_git_commit_is_detected(command):
    assert claude_hooks.is_git_commit(command)


@pytest.mark.parametrize(
    "command",
    [
        GIT + " status",
        GIT + " log --oneline -5",
        GIT + " log --grep commit",
        GIT + " show HEAD:commit.txt",
        "python -m pytest",
    ],
)
def test_other_commands_are_ignored(command):
    assert not claude_hooks.is_git_commit(command)


def test_repo_for_uses_the_dash_c_path(tmp_path):
    assert claude_hooks.repo_for(GIT + f' -C "{tmp_path}" commit -m x') == tmp_path


@pytest.mark.skipif(sys.platform != "win32", reason="Git Bash paths exist on Windows")
def test_repo_for_converts_git_bash_paths():
    repo = claude_hooks.repo_for(GIT + " -C /c/Some/Repo commit -m x")
    assert repo == Path("C:/Some/Repo")


def test_scan_error_blocks_the_commit(monkeypatch):
    def broken_run(*args, **kwargs):
        raise OSError("scanner missing")

    monkeypatch.setattr(claude_hooks.subprocess, "run", broken_run)
    event = {"tool_input": {"command": GIT + ' commit -m "x"'}}
    assert claude_hooks.pre_commit_scan(event) == 2


def test_pytest_summary_drops_the_timing():
    out = "....\n========== 1 failed, 49 passed in 0.12s ==========\n"
    assert claude_hooks.pytest_summary(out, 1) == "1 failed, 49 passed"


@pytest.fixture
def stop_env(monkeypatch, tmp_path, capsys):
    """Stop-hook helpers faked: dirty tree, fixed fingerprint, counted pytest runs."""
    monkeypatch.setattr(claude_hooks, "STATE_FILE", tmp_path / "state.json")
    monkeypatch.setattr(claude_hooks, "git_lines", lambda *a: [" M x.py"])
    monkeypatch.setattr(claude_hooks, "python_fingerprint", lambda: "fp-1")
    runs = []

    class Done:
        returncode = 0
        stdout = "== 3 passed in 0.05s ==\n"

    def fake_run(*args, **kwargs):
        runs.append(args)
        return Done()

    monkeypatch.setattr(claude_hooks.subprocess, "run", fake_run)
    return runs, capsys


def test_stop_runs_once_then_stays_silent_until_a_py_file_changes(
    stop_env, monkeypatch
):
    runs, capsys = stop_env
    assert claude_hooks.stop_pytest({}) == 0
    assert "pytest: 3 passed" in capsys.readouterr().out
    assert claude_hooks.stop_pytest({}) == 0  # same fingerprint: no run, no output
    assert len(runs) == 1
    assert capsys.readouterr().out == ""


def test_stop_does_not_repeat_an_unchanged_result(stop_env, monkeypatch):
    runs, capsys = stop_env
    claude_hooks.stop_pytest({})
    capsys.readouterr()
    monkeypatch.setattr(claude_hooks, "python_fingerprint", lambda: "fp-2")
    claude_hooks.stop_pytest({})  # .py changed, so pytest runs, but same result
    assert len(runs) == 2
    assert capsys.readouterr().out == ""


def test_stop_timeout_is_one_line_and_never_blocks(stop_env, monkeypatch):
    _, capsys = stop_env

    def slow_run(*args, **kwargs):
        raise claude_hooks.subprocess.TimeoutExpired(cmd="pytest", timeout=60)

    monkeypatch.setattr(claude_hooks.subprocess, "run", slow_run)
    assert claude_hooks.stop_pytest({}) == 0
    assert "timed out after 60s" in capsys.readouterr().out


def test_stop_is_silent_on_a_clean_tree(stop_env, monkeypatch):
    runs, capsys = stop_env
    monkeypatch.setattr(claude_hooks, "git_lines", lambda *a: [])
    assert claude_hooks.stop_pytest({}) == 0
    assert runs == []
    assert capsys.readouterr().out == ""


def test_non_commit_command_is_never_scanned(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("scanner should not run")

    monkeypatch.setattr(claude_hooks.subprocess, "run", fail_if_called)
    event = {"tool_input": {"command": GIT + " status"}}
    assert claude_hooks.pre_commit_scan(event) == 0
