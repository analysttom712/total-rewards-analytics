"""Tests for scripts/public_scan.py (tooling, not a learning exercise).

Every fake secret is built by joining pieces ("AKIA" + "Z" * 16) so this file's
own source never matches a scan rule and can be committed through the scan.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "public_scan.py"
_spec = importlib.util.spec_from_file_location("public_scan", SCRIPT)
public_scan = importlib.util.module_from_spec(_spec)
sys.modules["public_scan"] = public_scan  # dataclasses needs the module registered
_spec.loader.exec_module(public_scan)

RULES = public_scan.build_rules([])


def make_diff(*added: str, path: str = "docs/notes.md", start: int = 1) -> str:
    """A minimal `git diff --unified=0` that adds the given lines to one file."""
    header = (
        f"diff --git a/{path} b/{path}\n"
        f"--- a/{path}\n"
        f"+++ b/{path}\n"
        f"@@ -0,0 +{start},{len(added)} @@\n"
    )
    return header + "".join(f"+{line}\n" for line in added)


def rules_hit(*added: str) -> list[str]:
    return [hit.rule for hit in public_scan.scan_diff(make_diff(*added), RULES)]


# Each fake value must be caught by its rule.
@pytest.mark.parametrize(
    ("line", "rule"),
    [
        ("key = " + "AKIA" + "Z" * 16, "aws-access-key"),
        ("token: " + "ghp_" + "a" * 36, "github-token"),
        ("ANTHROPIC=" + "sk-" + "ant-" + "b" * 24, "api-key"),
        ("-----BEGIN " + "RSA PRIVATE KEY-----", "private-key"),
        ("password" + ' = "' + "x" * 20 + '"', "secret-assignment"),
        ("arn:aws:iam::" + "1234" * 3 + ":role/demo", "aws-account-id"),
        ("ssn " + "123" + "-45-" + "6789", "ssn"),
        ("tax_id," + "123" + "45" + "6789", "ssn-no-dashes"),
        ("emp," + "9876" + "54321" + ",x", "ssn-no-dashes"),
        ("C:" + "\\Users\\" + "fakeuser\\Documents", "windows-user-path"),
        ("cd /c/" + "Users/" + "fakeuser/repo", "windows-user-path"),
    ],
)
def test_fake_secret_is_caught(line, rule):
    assert rule in rules_hit(line)


# Ordinary project content must not trip the scan.
@pytest.mark.parametrize(
    "line",
    [
        "hire_date = 2026-11-25",
        "employee_id = 100001",
        "profiles.yml lives in %USERPROFILE%\\.dbt\\",
        "C:" + "\\Users\\" + "<name>\\.dbt",
        "C:" + "\\Users\\" + "Public\\Documents",
        "salary = fake.pyint(min_value=75000, max_value=150000)",
        "AKIA is the prefix of an AWS access key ID",
        "phone 5551234567 has 10 digits, not 9",
        "version 1.123456789 is a decimal",
    ],
)
def test_normal_line_is_clean(line):
    assert rules_hit(line) == []


# Synthetic SSNs start with 000 or 666 (never issued by the SSA) and are allowed.
@pytest.mark.parametrize(
    "line",
    ["ssn,000-12-3456", "ssn,666-12-3456", "ssn,000123456", "ssn,666123456"],
)
def test_synthetic_ssn_is_allowed(line):
    assert rules_hit(line) == []


# Any other area number is flagged, with or without hyphens.
@pytest.mark.parametrize(
    ("line", "rule"),
    [
        ("ssn," + "001" + "-12-" + "3456", "ssn"),
        ("ssn," + "665" + "-12-" + "3456", "ssn"),
        ("ssn," + "667" + "12" + "3456", "ssn-no-dashes"),
        ("ssn," + "900" + "12" + "3456", "ssn-no-dashes"),
    ],
)
def test_non_synthetic_ssn_is_flagged(line, rule):
    assert rule in rules_hit(line)


def test_removed_lines_are_ignored():
    diff = make_diff("plain line") + "-" + "AKIA" + "Z" * 16 + "\n"
    assert public_scan.scan_diff(diff, RULES) == []


def test_hit_reports_file_and_line_number():
    diff = make_diff("fine", "ssn " + "123" + "-45-" + "6789", path="x.py", start=10)
    [hit] = public_scan.scan_diff(diff, RULES)
    assert (hit.file, hit.line, hit.rule) == ("x.py", 11, "ssn")


def test_preview_is_masked():
    key = "AKIA" + "Z" * 16
    [hit] = public_scan.scan_diff(make_diff("key " + key), RULES)
    assert key not in str(hit)


def test_added_line_starting_with_plus_plus_is_content_not_a_header():
    diff = make_diff("++ " + "AKIA" + "Z" * 16)
    assert [h.rule for h in public_scan.scan_diff(diff, RULES)] == ["aws-access-key"]


def test_secret_file_name_is_caught():
    diff = make_diff("A=1", path="config/.env")
    assert "secret-file" in [h.rule for h in public_scan.scan_diff(diff, RULES)]


def test_blocklist_word_is_whole_word_and_case_insensitive(tmp_path):
    blocklist = tmp_path / "blocklist.txt"
    blocklist.write_text("# comment\n\nAcmeCorp\n", encoding="utf-8")
    rules = public_scan.build_rules(public_scan.load_blocklist(blocklist))
    diff = make_diff("worked at acmecorp", "acmecorporation is a different word")
    hits = public_scan.scan_diff(diff, rules)
    assert [(h.line, h.rule) for h in hits] == [(1, "blocklist")]


def test_blocklist_hit_never_prints_any_part_of_the_word():
    rules = public_scan.build_rules(["AcmeCorp"])
    [hit] = public_scan.scan_diff(make_diff("worked at AcmeCorp"), rules)
    assert str(hit) == "docs/notes.md:1: [blocklist] (word hidden)"
    assert "acme" not in str(hit).lower()


def test_missing_blocklist_means_no_words(tmp_path):
    assert public_scan.load_blocklist(tmp_path / "nope.txt") == []


def test_main_exit_codes(monkeypatch, capsys):
    monkeypatch.setattr(public_scan, "git_diff", lambda base: make_diff("hello"))
    assert public_scan.main([]) == 0

    leaked = make_diff("ssn " + "123" + "-45-" + "6789")
    monkeypatch.setattr(public_scan, "git_diff", lambda base: leaked)
    assert public_scan.main([]) == 1
    assert "docs/notes.md:1: [ssn]" in capsys.readouterr().out
