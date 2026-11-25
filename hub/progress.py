"""The progress file: what Thomas typed and marked on the site.

Takes in: one answer or one self-mark at a time.
Puts out: `hub/progress.local.json` (gitignored), which `/standup` reads.

Every write goes to a temporary file first and is then swapped into place, so
a crash mid-save can't leave a half-written file. Every read-change-write
also holds one lock, because the server answers each request on its own thread:
without it, two saves at once would overwrite each other.
"""

from __future__ import annotations

import json
import os
import threading
from datetime import datetime
from pathlib import Path

VERSION = 1
MARKS = {"correct": "✓", "partial": "½", "missed": "✗"}
MAX_ANSWER_CHARS = 4000

# One save at a time: load, change and write happen as a single step.
_SAVE_LOCK = threading.Lock()


class ProgressError(ValueError):
    """The request or the file on disk is not usable; the message says why."""


def empty() -> dict:
    return {"version": VERSION, "answers": {}}


def load(path: Path) -> dict:
    """Read the file. A missing file is an empty record; a broken one is an
    error, so it is never silently replaced."""
    if not path.exists():
        return empty()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        raise ProgressError(f"{path.name} is not valid JSON: {err}") from err
    if not isinstance(data, dict) or not isinstance(data.get("answers"), dict):
        raise ProgressError(f"{path.name} does not look like a progress file")
    return data


def _write(path: Path, data: dict) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def save_answer(
    path: Path,
    *,
    item_id: str,
    lesson: str,
    question: str,
    concept: str,
    answer: str,
) -> dict:
    """Store a typed answer. A changed answer clears the old self-mark."""
    if not isinstance(answer, str) or not answer.strip():
        raise ProgressError("The answer is empty.")
    if len(answer) > MAX_ANSWER_CHARS:
        raise ProgressError(f"The answer is over {MAX_ANSWER_CHARS} characters.")

    with _SAVE_LOCK:
        data = load(path)
        previous = data["answers"].get(item_id, {})
        unchanged = previous.get("answer") == answer
        entry = {
            "lesson": lesson,
            "question": question,
            "concept": concept,
            "answer": answer,
            "answered_at": _now(),
            "self_mark": previous.get("self_mark") if unchanged else None,
            "official_mark": previous.get("official_mark") if unchanged else None,
        }
        data["answers"][item_id] = entry
        _write(path, data)
    return entry


def save_self_mark(path: Path, *, item_id: str, mark: str) -> dict:
    """Store Thomas's own mark. It is provisional until `/standup` grades it."""
    if mark not in MARKS:
        raise ProgressError(f"Unknown mark: {mark!r}.")
    with _SAVE_LOCK:
        data = load(path)
        entry = data["answers"].get(item_id)
        if entry is None:
            raise ProgressError("Save an answer before marking it.")
        entry["self_mark"] = mark
        entry["marked_at"] = _now()
        _write(path, data)
    return entry


def save_task(path: Path, *, lesson: str, task: str, done: bool) -> dict:
    """Tick or untick one hand-marked task on a lesson's task list."""
    if not isinstance(done, bool):
        raise ProgressError("A task is either done or not done.")
    with _SAVE_LOCK:
        data = load(path)
        tasks = data.setdefault("tasks", {})
        tasks.setdefault(lesson, {})[task] = done
        _write(path, data)
    return {"lesson": lesson, "task": task, "done": done}


def summary(path: Path) -> str:
    """Plain-text read-back of the file, for `/standup` and for checking a save."""
    data = load(path)
    answers = data["answers"]
    ticked = [
        f"{lesson}: {task}"
        for lesson, tasks in data.get("tasks", {}).items()
        for task, done in tasks.items()
        if done
    ]
    if not answers and not ticked:
        return "No answers saved yet."
    lines = [f"{len(answers)} answer(s) in {path.name}:"]
    if ticked:
        lines.insert(0, "Tasks ticked: " + ", ".join(ticked))
    for item_id, entry in answers.items():
        self_mark = MARKS.get(entry.get("self_mark") or "", "not marked")
        official = entry.get("official_mark") or "not graded"
        lines += [
            "",
            f"[{item_id}] {entry.get('lesson', '?')} · {entry.get('answered_at', '?')}",
            f"  Q: {entry.get('question', '')}",
            f"  A: {entry.get('answer', '')}",
            f"  Self-mark: {self_mark} (provisional) · Official: {official}",
        ]
    return "\n".join(lines)
