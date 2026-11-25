"""Read the learning docs into plain Python records.

Takes in: the Markdown text of the docs Claude maintains.
Puts out: lessons, review-queue items, glossary terms and a day's commands.

Like a Power Query source step: it only reads and shapes; it never writes to
the docs and keeps no copy of them.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

_SEPARATOR = re.compile(r"^\|?\s*:?-{3,}")
_CODE_SPAN = re.compile(r"`([^`]+)`")
_DAY_RANGE = re.compile(r"Day\s+(\d+)(?:\s*[–-]\s*(\d+))?")
_TAG = re.compile(r"<[^>]+>")


# --- tables ----------------------------------------------------------------


def split_row(line: str) -> list[str]:
    """Split one Markdown table row into cells.

    A `|` inside a `code span`, or written as `\\|`, is text, not a divider.
    """
    text = line.strip().removeprefix("|")
    if text.endswith("|") and not text.endswith("\\|"):
        text = text[:-1]

    cells: list[str] = []
    current: list[str] = []
    in_code = False
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "\\" and text[i + 1 : i + 2] == "|":
            current.append("|")
            i += 2
            continue
        if ch == "`":
            in_code = not in_code
        if ch == "|" and not in_code:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
        i += 1
    cells.append("".join(current).strip())
    return cells


def find_tables(text: str) -> list[list[dict[str, str]]]:
    """Every Markdown table in `text`, each as a list of {column: cell} rows."""
    lines = text.splitlines()
    tables: list[list[dict[str, str]]] = []
    i = 0
    while i < len(lines) - 1:
        is_header = lines[i].lstrip().startswith("|")
        if not (is_header and _SEPARATOR.match(lines[i + 1].strip())):
            i += 1
            continue
        header = split_row(lines[i])
        rows: list[dict[str, str]] = []
        i += 2
        while i < len(lines) and lines[i].lstrip().startswith("|"):
            cells = split_row(lines[i])
            # Short rows are padded and long rows trimmed, so one odd row
            # can't shift every column after it.
            cells = (cells + [""] * len(header))[: len(header)]
            rows.append(dict(zip(header, cells, strict=True)))
            i += 1
        tables.append(rows)
    return tables


def find_table(text: str, *columns: str) -> list[dict[str, str]]:
    """The first table that has all of `columns`, or [] if there is none."""
    for rows in find_tables(text):
        if rows and all(column in rows[0] for column in columns):
            return rows
    return []


# --- lessons (docs/LEARNING_LOG.md) -----------------------------------------


@dataclass(frozen=True)
class Lesson:
    """One row of the learning log = one session = one lesson."""

    date: str
    day: str
    ticket: str
    concept: str
    shipped: str
    quiz: str
    blockers: str
    next_up: str

    @property
    def slug(self) -> str:
        """URL-safe name, e.g. '003 (pt 2)' -> 'day-003-pt-2'."""
        return "day-" + re.sub(r"[^a-z0-9]+", "-", self.day.lower()).strip("-")

    @property
    def day_number(self) -> int | None:
        match = re.match(r"\s*(\d+)", self.day)
        return int(match.group(1)) if match else None

    @property
    def issue_number(self) -> int | None:
        match = re.search(r"#(\d+)", self.ticket)
        return int(match.group(1)) if match else None


def parse_lessons(log_text: str) -> list[Lesson]:
    rows = find_table(log_text, "Date", "Day", "Ticket", "Concept")
    return [
        Lesson(
            date=row["Date"],
            day=row["Day"],
            ticket=row["Ticket"],
            concept=row["Concept"],
            shipped=row.get("Shipped", ""),
            quiz=row.get("Quiz", ""),
            blockers=row.get("Blockers", ""),
            next_up=row.get("Next", ""),
        )
        for row in rows
        if row["Day"].strip()
    ]


# --- knowledge checks (docs/REVIEW_QUEUE.md) --------------------------------


@dataclass(frozen=True)
class QueueItem:
    """One concept in the review queue; `question` is empty until one is written."""

    concept: str
    box: str
    result: str
    next_due: str
    where_taught: str
    question: str

    @property
    def item_id(self) -> str:
        """Stable key for the progress file, derived from the concept text."""
        return "q-" + hashlib.sha1(self.concept.encode("utf-8")).hexdigest()[:10]

    @property
    def days(self) -> set[int]:
        return days_taught(self.where_taught)


def days_taught(where_taught: str) -> set[int]:
    """'Day 3 + review' -> {3}; 'Day 1–3' -> {1, 2, 3}; no day -> set()."""
    match = _DAY_RANGE.search(where_taught)
    if not match:
        return set()
    first = int(match.group(1))
    last = int(match.group(2)) if match.group(2) else first
    return set(range(first, last + 1))


def parse_queue(queue_text: str) -> list[QueueItem]:
    rows = find_table(queue_text, "Concept", "Box", "Where taught")
    return [
        QueueItem(
            concept=row["Concept"],
            box=row["Box"],
            result=row.get("Result", ""),
            next_due=row.get("Next due", ""),
            where_taught=row["Where taught"],
            question=row.get("Question", ""),
        )
        for row in rows
        if row["Concept"].strip()
    ]


def checks_for_lesson(lesson: Lesson, queue: list[QueueItem]) -> list[QueueItem]:
    """Queue items taught on this lesson's day that have a question written."""
    day = lesson.day_number
    return [item for item in queue if item.question and day in item.days]


# --- new terms (docs/GLOSSARY.md) -------------------------------------------


@dataclass(frozen=True)
class Term:
    name: str
    details: dict[str, str]


def parse_glossary(glossary_text: str) -> list[Term]:
    terms: list[Term] = []
    for rows in find_tables(glossary_text):
        for row in rows:
            columns = list(row)
            name = row[columns[0]]
            if name.strip():
                terms.append(Term(name, {c: row[c] for c in columns[1:]}))
    return terms


def _normal(code: str) -> str:
    """`range()` , `.append()` and `range` all compare equal."""
    return re.sub(r"\s+", "", code).removesuffix("()").lstrip(".")


def terms_for_lesson(lesson: Lesson, terms: list[Term]) -> list[Term]:
    """Glossary terms named in the lesson's Concept cell.

    The glossary has no day column, so this matches on the words themselves:
    a term's `code` appears as `code` in the concept, or its plain name
    appears as a whole word.
    """
    concept = lesson.concept
    concept_codes = {_normal(code) for code in _CODE_SPAN.findall(concept)}
    plain_concept = concept.replace("`", "").replace("*", "")
    found: list[Term] = []
    for term in terms:
        term_codes = {_normal(code) for code in _CODE_SPAN.findall(term.name)}
        plain_name = term.name.replace("`", "").replace("*", "").strip()
        by_code = bool(term_codes & concept_codes)
        by_name = (
            not term_codes
            and len(plain_name) >= 5
            and re.search(
                r"(?<!\w)" + re.escape(plain_name) + r"s?(?!\w)",
                plain_concept,
                re.IGNORECASE,
            )
        )
        if by_code or by_name:
            found.append(term)
    return found


# --- commands (docs/CHEATSHEET.md) ------------------------------------------


def cheatsheet_day(cheatsheet_text: str, day_number: int) -> tuple[str, str] | None:
    """(title, Markdown) of one day's section, with its drop-downs turned into
    headings so the content shows on the page. None if the day has no section.
    """
    lines = cheatsheet_text.splitlines()
    start = re.compile(rf"<summary><b>(Day\s+0*{day_number}\b.*?)</b></summary>")
    for index, line in enumerate(lines):
        match = start.search(line)
        if not match:
            continue
        title = _TAG.sub("", match.group(1)).strip()
        body: list[str] = []
        depth = 1
        for inner in lines[index + 1 :]:
            stripped = inner.strip()
            if stripped.startswith("<details"):
                depth += 1
            elif stripped == "</details>":
                depth -= 1
                if depth == 0:
                    break
            elif stripped.startswith("<summary>") and stripped.endswith("</summary>"):
                heading = stripped[len("<summary>") : -len("</summary>")]
                body.append(f"### {heading}")
            else:
                body.append(inner)
        return title, "\n".join(body).strip()
    return None


# --- whole reference docs (cheatsheet, glossary, resources) -----------------

_SUMMARY = re.compile(r"<summary>(.*)</summary>")


def flatten_details(text: str, top_level: int = 2) -> str:
    """Turn every <details> drop-down into a heading, so the content is on the
    page. A drop-down inside another becomes a smaller heading. The doc's own
    `# Title` line is dropped because the page supplies the title.
    """
    out: list[str] = []
    depth = 0
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
        if not in_fence:
            if stripped.startswith("<details"):
                depth += 1
                continue
            if stripped == "</details>":
                depth = max(0, depth - 1)
                continue
            summary = _SUMMARY.fullmatch(stripped)
            if summary:
                level = min(6, top_level + max(depth, 1) - 1)
                out.append(f"{'#' * level} {_TAG.sub('', summary.group(1)).strip()}")
                continue
            if stripped.startswith("# ") and not out:
                continue
        out.append(line)
    return "\n".join(out).strip()


# --- grade signals (docs/COACHING.md section 7) -----------------------------


def signals_for_lesson(lesson: Lesson, coaching_text: str) -> dict[str, str]:
    """The Signals row whose Day matches this lesson exactly, or {}."""
    rows = find_table(coaching_text, "Day", "Quiz %", "Highest hint rung")
    for row in rows:
        if row["Day"].strip() == lesson.day.strip():
            return row
    return {}


# --- reading files ----------------------------------------------------------


def read_doc(docs_dir: Path, name: str) -> str:
    """A doc's text, or '' if it doesn't exist (a missing doc is not an error)."""
    path = docs_dir / name
    return path.read_text(encoding="utf-8") if path.exists() else ""
