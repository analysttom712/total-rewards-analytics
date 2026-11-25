"""Tests for hub/progress.py (tooling, not a learning exercise)."""

import json

import pytest

from hub import progress

ANSWER = {
    "item_id": "q-abc",
    "lesson": "day-003",
    "question": "What does it return?",
    "concept": "It stops before b",
}


def test_a_missing_file_reads_as_empty(tmp_path):
    assert progress.load(tmp_path / "none.json") == progress.empty()


def test_an_answer_is_saved_and_read_back(tmp_path):
    path = tmp_path / "progress.json"
    progress.save_answer(path, **ANSWER, answer="[5, 6, 7]")
    entry = progress.load(path)["answers"]["q-abc"]
    assert entry["answer"] == "[5, 6, 7]"
    assert entry["lesson"] == "day-003"
    assert entry["self_mark"] is None
    assert entry["answered_at"]
    assert list(tmp_path.iterdir()) == [path]  # no temporary file left behind


def test_a_self_mark_is_saved_and_a_changed_answer_clears_it(tmp_path):
    path = tmp_path / "progress.json"
    progress.save_answer(path, **ANSWER, answer="first try")
    progress.save_self_mark(path, item_id="q-abc", mark="partial")
    assert progress.load(path)["answers"]["q-abc"]["self_mark"] == "partial"

    progress.save_answer(path, **ANSWER, answer="first try")  # same text: mark kept
    assert progress.load(path)["answers"]["q-abc"]["self_mark"] == "partial"

    progress.save_answer(path, **ANSWER, answer="second try")
    assert progress.load(path)["answers"]["q-abc"]["self_mark"] is None


@pytest.mark.parametrize("answer", ["", "   ", "x" * (progress.MAX_ANSWER_CHARS + 1)])
def test_empty_and_oversized_answers_are_refused(tmp_path, answer):
    path = tmp_path / "progress.json"
    with pytest.raises(progress.ProgressError):
        progress.save_answer(path, **ANSWER, answer=answer)
    assert not path.exists()


def test_an_unknown_mark_or_a_mark_without_an_answer_is_refused(tmp_path):
    path = tmp_path / "progress.json"
    with pytest.raises(progress.ProgressError):
        progress.save_self_mark(path, item_id="q-abc", mark="correct")
    progress.save_answer(path, **ANSWER, answer="an answer")
    with pytest.raises(progress.ProgressError):
        progress.save_self_mark(path, item_id="q-abc", mark="perfect")


def test_a_broken_file_is_an_error_and_is_not_overwritten(tmp_path):
    path = tmp_path / "progress.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(progress.ProgressError):
        progress.save_answer(path, **ANSWER, answer="an answer")
    assert path.read_text(encoding="utf-8") == "{not json"

    path.write_text(json.dumps(["a", "list"]), encoding="utf-8")
    with pytest.raises(progress.ProgressError):
        progress.load(path)


def test_summary_reads_back_what_was_saved(tmp_path):
    path = tmp_path / "progress.json"
    assert progress.summary(path) == "No answers saved yet."
    progress.save_answer(path, **ANSWER, answer="[5, 6, 7]")
    progress.save_self_mark(path, item_id="q-abc", mark="correct")
    text = progress.summary(path)
    assert "[5, 6, 7]" in text and "✓" in text and "day-003" in text
