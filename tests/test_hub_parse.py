"""Tests for hub/parse.py (tooling, not a learning exercise)."""

from pathlib import Path

from hub import parse

LOG = """# Learning Log

| Date | Day | Ticket | Concept | Shipped | Quiz | Blockers | Next |
|---|---|---|---|---|---|---|---|
| 2026-01-05 | 003 | #2 make_employee(): functions and loops | Functions (`def`, `return`), `for` loops, `range()` | A function; a loop | 1/3 | Naming | #3 next |
| 2026-01-05 | 003 (pt 2) | Deep review | The `a | b` operator | Notes | 2/5 | None | #9 |
"""

QUEUE = """## Active

| Concept | Box | Last seen | Result | Misses | Next due | Where taught | Question |
|---|---|---|---|---|---|---|---|
| `range(a, b)` stops before `b` | 2 | 2026-01-05 | ✓ | 2 | 2026-01-07 | Day 3 | What does `list(range(5, 8))` return? |
| Branch vs `main` | 2 | 2026-01-04 | ✓ | 1 | 2026-01-06 | Day 1–2 | Does a commit on a branch change `main`? |
| Import groups | 1 | 2026-01-05 | new | 0 | 2026-01-06 | Day 3 | |
"""


def test_split_row_keeps_a_pipe_inside_code():
    assert parse.split_row("| `a | b` | plain |") == ["`a | b`", "plain"]


def test_split_row_keeps_an_escaped_pipe():
    assert parse.split_row(r"| a \| b | c |") == ["a | b", "c"]


def test_find_table_picks_the_table_with_the_named_columns():
    text = "| A | B |\n|---|---|\n| 1 | 2 |\n\n| C | D |\n|---|---|\n| 3 | 4 |\n"
    assert parse.find_table(text, "C") == [{"C": "3", "D": "4"}]
    assert parse.find_table(text, "Z") == []


def test_a_short_row_is_padded_not_shifted():
    text = "| A | B | C |\n|---|---|---|\n| 1 | 2 |\n"
    assert parse.find_table(text, "A") == [{"A": "1", "B": "2", "C": ""}]


def test_each_log_row_becomes_one_lesson():
    lessons = parse.parse_lessons(LOG)
    assert [lesson.slug for lesson in lessons] == ["day-003", "day-003-pt-2"]
    first = lessons[0]
    assert first.day_number == 3
    assert first.issue_number == 2
    assert first.quiz == "1/3"
    assert lessons[1].issue_number is None
    assert lessons[1].concept == "The `a | b` operator"


def test_days_taught_reads_single_days_and_ranges():
    assert parse.days_taught("Day 3 + review") == {3}
    assert parse.days_taught("Day 1–3") == {1, 2, 3}
    assert parse.days_taught("somewhere else") == set()


def test_checks_are_this_days_items_that_have_a_question():
    lesson = parse.parse_lessons(LOG)[0]
    checks = parse.checks_for_lesson(lesson, parse.parse_queue(QUEUE))
    assert [item.concept for item in checks] == ["`range(a, b)` stops before `b`"]


def test_queue_without_a_question_column_still_parses():
    text = QUEUE.replace(" Question |", "").replace("---|\n", "\n", 1)
    items = parse.parse_queue(text)
    assert items and all(item.question == "" for item in items)


def test_item_id_is_stable_and_differs_per_concept():
    items = parse.parse_queue(QUEUE)
    assert items[0].item_id == parse.parse_queue(QUEUE)[0].item_id
    assert len({item.item_id for item in items}) == len(items)


def test_terms_match_on_code_and_on_whole_names():
    glossary = (
        "| Symbol | Real name |\n|---|---|\n"
        "| `range()` | range |\n| `->` | return annotation |\n\n"
        "| Term | Plain English |\n|---|---|\n"
        "| function | a named block |\n| list | ordered values |\n"
    )
    lesson = parse.parse_lessons(LOG)[0]
    found = parse.terms_for_lesson(lesson, parse.parse_glossary(glossary))
    assert [term.name for term in found] == ["`range()`", "function"]


def test_cheatsheet_day_turns_dropdowns_into_headings():
    text = (
        "<details>\n<summary><b>Day 2 · Lists</b></summary>\n\nother day\n\n</details>\n\n"
        "<details>\n<summary><b>Day 3 · Functions</b></summary>\n\n"
        "<details>\n<summary>Loops</summary>\n\n```python\nfor i in range(3):\n```\n\n"
        "</details>\n\n</details>\n\nafter\n"
    )
    title, body = parse.cheatsheet_day(text, 3)
    assert title == "Day 3 · Functions"
    assert body.startswith("### Loops")
    assert "for i in range(3):" in body
    assert "<details" not in body and "after" not in body and "other day" not in body
    assert parse.cheatsheet_day(text, 9) is None


def test_signals_row_matches_the_day_exactly():
    coaching = (
        "| Date | Day | Quiz % | Highest hint rung |\n|---|---|---|---|\n"
        "| 2026-01-05 | 003 | 17% | partial code |\n"
    )
    lessons = parse.parse_lessons(LOG)
    assert parse.signals_for_lesson(lessons[0], coaching)["Quiz %"] == "17%"
    assert parse.signals_for_lesson(lessons[1], coaching) == {}


def test_the_real_docs_parse():
    """Smoke test: the repo's own docs still produce lessons and queue items."""
    docs = Path(__file__).resolve().parents[1] / "docs"
    lessons = parse.parse_lessons(parse.read_doc(docs, "LEARNING_LOG.md"))
    queue = parse.parse_queue(parse.read_doc(docs, "REVIEW_QUEUE.md"))
    assert lessons and queue
    assert len({lesson.slug for lesson in lessons}) == len(lessons)
    assert parse.read_doc(docs, "NO_SUCH_DOC.md") == ""


def test_flatten_details_shows_dropdown_content_under_headings():
    text = (
        "# Cheatsheet\n\nIntro line.\n\n"
        "<details>\n<summary><b>Day 1 · Setup</b></summary>\n\n"
        "<details>\n<summary>Start of session</summary>\n\n"
        "```powershell\n# a comment, not a heading\ngit status\n```\n\n"
        "</details>\n\n</details>\n"
    )
    flat = parse.flatten_details(text)
    assert "<details" not in flat and "<summary" not in flat
    assert "# Cheatsheet" not in flat
    assert "\n## Day 1 · Setup\n" in flat
    assert "\n### Start of session\n" in flat
    assert "# a comment, not a heading" in flat
    assert flat.startswith("Intro line.")
