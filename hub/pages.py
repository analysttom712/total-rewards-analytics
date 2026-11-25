"""Turn records into HTML pages.

Takes in: records from `parse.py` and the saved progress.
Puts out: one HTML string per page.

Two kinds of text reach a page and they are treated differently:
- text from the docs is Markdown that Claude and Thomas wrote; it is rendered.
- text Thomas typed on the site is escaped with `html.escape`, so it can only
  ever show as plain text, never run as HTML.

Every page has the same frame, laid out like a course site: a top bar of
areas, a left table of contents (a tick when a lesson has nothing left, a
count when it does), and course resources at the bottom of that list.
"""

from __future__ import annotations

import re
from html import escape

import markdown

from hub import ISSUES_URL
from hub.parse import Lesson, QueueItem, Term, checks_for_lesson
from hub.progress import MARKS

# slug -> (title, file in docs/, one-line description)
REFERENCE = {
    "cheatsheet": ("Cheatsheet", "CHEATSHEET.md", "Commands and patterns, by day"),
    "glossary": (
        "Glossary",
        "GLOSSARY.md",
        "Every symbol and term, with a job analogy",
    ),
    "resources": (
        "Resources",
        "RESOURCES.md",
        "Links by topic and the cert study path",
    ),
}


# --- Markdown helpers ---------------------------------------------------------


def render_markdown(text: str) -> str:
    return markdown.markdown(text, extensions=["tables", "fenced_code"])


def render_inline(text: str) -> str:
    """Markdown for a single phrase, without the wrapping <p>."""
    # A phrase that starts with "#2 ..." is a ticket number, not a heading.
    if text.startswith("#"):
        text = "\\" + text
    html = render_markdown(text).strip()
    if html.startswith("<p>") and html.endswith("</p>") and html.count("<p>") == 1:
        return html[3:-4]
    return html


def _split_items(cell: str, separators: str = ";") -> list[str]:
    """A log cell packs several points into one line; split them on ';'
    only where it is safe (outside `code` and (parentheses))."""
    items: list[str] = []
    current: list[str] = []
    depth = 0
    in_code = False
    for ch in cell:
        if ch == "`":
            in_code = not in_code
        elif not in_code and ch in "([":
            depth += 1
        elif not in_code and ch in ")]":
            depth = max(0, depth - 1)
        if ch in separators and not in_code and depth == 0:
            items.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    items.append("".join(current).strip())
    return [item for item in items if item]


def _bullets(cell: str, separators: str = ";") -> str:
    items = _split_items(cell, separators)
    if len(items) <= 1:
        return f"<p>{render_inline(cell)}</p>"
    rows = "".join(f"<li>{render_inline(item)}</li>" for item in items)
    return f"<ul>{rows}</ul>"


# --- drop-down sections ("folds") ---------------------------------------------


def split_sections(text: str, level: int) -> tuple[str, list[tuple[str, str]]]:
    """Cut Markdown at each heading of `level` (2 means `## `).

    Returns (text before the first such heading, [(heading, body), ...]).
    A `##` inside a code block is code, not a heading.
    """
    marker = "#" * level + " "
    intro: list[str] = []
    sections: list[tuple[str, list[str]]] = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith(marker):
            sections.append((line[len(marker) :].strip(), []))
        elif sections:
            sections[-1][1].append(line)
        else:
            intro.append(line)
    return "\n".join(intro), [(title, "\n".join(body)) for title, body in sections]


def render_folds(
    sections: list[tuple[str, str]], prefix: str = ""
) -> tuple[str, list[tuple[str, str]]]:
    """Each section as a closed drop-down. Returns (html, [(id, title), ...])
    so the page can list them under "On this page"."""
    html: list[str] = []
    index: list[tuple[str, str]] = []
    used: set[str] = set()
    for title, body in sections:
        base = prefix + (
            re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "section"
        )
        slug = base
        number = 2
        while slug in used:
            slug = f"{base}-{number}"
            number += 1
        used.add(slug)
        index.append((slug, title))
        html.append(
            f'<details class="fold" id="{slug}"><summary>{render_inline(title)}</summary>'
            f'<div class="fold-body">{render_markdown(body)}</div></details>'
        )
    return "".join(html), index


def _jump_list(index: list[tuple[str, str]]) -> str:
    if not index:
        return ""
    links = "".join(
        f'<li><a href="#{slug}">{render_inline(title)}</a></li>'
        for slug, title in index
    )
    return (
        '<nav class="jump" aria-label="On this page">'
        f'<p class="cell-label">On this page</p><ul>{links}</ul>'
        '<div class="row"><button type="button" class="fold-all" data-open="true">Open all</button>'
        '<button type="button" class="fold-all" data-open="false">Close all</button></div>'
        "</nav>"
    )


# --- the frame every page shares ---------------------------------------------


# The task list at the top of every lesson. The two below are ticked by hand;
# "answer the knowledge checks" ticks itself from the saved answers.
MANUAL_TASKS = {
    "terms": ("Read the new terms", "#terms"),
    "commands": ("Open the commands and try one", "#commands"),
}


def lesson_progress(
    lesson: Lesson, queue: list[QueueItem], answers: dict, tasks: dict
) -> tuple[int, int]:
    """(done, total) for one lesson: each knowledge check answered and each
    hand-ticked task counts as one."""
    checks = checks_for_lesson(lesson, queue)
    ticked = tasks.get(lesson.slug, {})
    done = sum(1 for item in checks if item.item_id in answers)
    done += sum(1 for key in MANUAL_TASKS if ticked.get(key))
    return done, len(checks) + len(MANUAL_TASKS)


def build_sidebar(
    lessons: list[Lesson],
    queue: list[QueueItem],
    answers: dict,
    tasks: dict,
    current: str,
) -> str:
    """The left table of contents. `current` is the path of the open page."""

    def item(label: str, href: str, badge: str = "") -> str:
        here = ' aria-current="page"' if href == current else ""
        return f'<a class="side-item" href="{escape(href)}"{here}><span>{label}</span>{badge}</a>'

    def count(number: int, what: str) -> str:
        return f'<span class="badge" title="{number} {escape(what)}">{number}</span>'

    tick = '<span class="tick" title="Nothing left to do here">✓</span>'
    rows = [item("Table of contents", "/", count(len(lessons), "lessons"))]
    rows.append('<p class="side-head">Lessons</p>')
    for lesson in lessons:
        done, total = lesson_progress(lesson, queue, answers, tasks)
        left = total - done
        badge = count(left, "tasks left") if left else tick
        label = f"Day {escape(lesson.day)}: {render_inline(lesson.ticket)}"
        rows.append(item(label, f"/lesson/{lesson.slug}", badge))
    rows.append(
        f'<p class="side-head">Course resources {count(len(REFERENCE), "resources")}</p>'
    )
    for slug, (title, _file, _about) in REFERENCE.items():
        rows.append(item(escape(title), f"/reference/{slug}"))
    return "".join(rows)


def page(
    title: str,
    body: str,
    *,
    side: str = "",
    area: str = "content",
    crumbs: list[tuple[str, str]] | None = None,
) -> str:
    trail = "".join(
        f'<a href="{escape(href)}">{escape(label)}</a><span aria-hidden="true">›</span>'
        for label, href in (crumbs or [])
    )

    def area_link(key: str, label: str, href: str) -> str:
        here = ' aria-current="true"' if key == area else ""
        return f'<a href="{href}"{here}>{label}</a>'

    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · Learning hub</title>
<script src="/static/theme.js"></script>
<link rel="stylesheet" href="/static/hub.css">
</head>
<body>
<header class="top">
  <a class="brand" href="/">Learning hub</a>
  <span class="tag">Total Rewards Analytics · Northwind Mutual (fictional)</span>
  <button type="button" class="theme-toggle" aria-label="Switch between light and dark mode">☾ Dark mode</button>
</header>
<nav class="areas" aria-label="Course areas">
  {area_link("content", "Content", "/")}
  {area_link("reference", "Course resources", "/reference")}
</nav>
<div class="layout">
<aside class="side"><nav aria-label="Table of contents">{side}</nav></aside>
<main>
<nav class="crumbs" aria-label="Breadcrumb">{trail}<span>{escape(title)}</span></nav>
{body}
</main>
</div>
<footer>Built from the docs on every page load. Nothing here is a second copy.</footer>
<script src="/static/hub.js"></script>
</body>
</html>
"""


def _progress_bar(done: int, total: int, what: str) -> str:
    if not total:
        return ""
    percent = round(100 * done / total)
    return f"""<div class="progress">
<progress value="{done}" max="{total}">{percent}%</progress>
<p><strong>{percent} %</strong> · {done} of {total} {escape(what)}</p>
</div>"""


# --- home ---------------------------------------------------------------------


def render_home(
    lessons: list[Lesson],
    queue: list[QueueItem],
    answers: dict,
    tasks: dict,
    side: str,
) -> str:
    cards = []
    done_all = total_all = 0
    for lesson in lessons:
        done, total = lesson_progress(lesson, queue, answers, tasks)
        done_all += done
        total_all += total
        status = f"{done} of {total} tasks done"
        cards.append(
            f"""<li><a class="card" href="/lesson/{escape(lesson.slug)}">
<span class="kicker">Day {escape(lesson.day)} · {escape(lesson.date)} · <span class="state done">Done</span></span>
<span class="card-title">{render_inline(lesson.ticket)}</span>
<span class="note">{escape(status)}</span></a></li>"""
        )
    body = f"""<h1>Table of contents</h1>
<p class="lead">Each row of the learning log is a lesson. The map of phases and
the work-ahead lessons arrive in slice 2.</p>
{_progress_bar(done_all, total_all, "tasks done")}
<h2>Lessons</h2>
<ul class="cards">{"".join(cards) or "<li>No lessons in the learning log yet.</li>"}</ul>"""
    return page("Table of contents", body, side=side)


# --- lesson -------------------------------------------------------------------


def _term_rows(terms: list[Term]) -> str:
    if not terms:
        return (
            '<p class="gap">No glossary terms matched this lesson\'s log entry. '
            'The full list is in <a href="/reference/glossary">the glossary</a>.</p>'
        )
    rows = "".join(
        '<tr><th scope="row">{}</th><td>{}</td></tr>'.format(
            render_inline(term.name),
            "<br>".join(
                f'<span class="cell-label">{escape(column)}:</span> '
                f"{render_inline(value)}"
                for column, value in term.details.items()
                if value
            ),
        )
        for term in terms
    )
    return f'<table class="terms"><tbody>{rows}</tbody></table>'


def _check(number: int, lesson: Lesson, item: QueueItem, saved: dict) -> str:
    answer = saved.get("answer", "")
    self_mark = saved.get("self_mark")
    official = saved.get("official_mark")
    status = f"Saved {saved['answered_at']}" if saved.get("answered_at") else ""
    if official:
        mark_line = f"Official mark: {escape(str(official))}"
    elif self_mark in MARKS:
        mark_line = f"Your mark: {MARKS[self_mark]} (provisional until /standup)"
    else:
        mark_line = ""
    buttons = ""
    for key, symbol, label in (
        ("correct", "✓", "Got it"),
        ("partial", "½", "Partly"),
        ("missed", "✗", "Missed it"),
    ):
        pressed = ' aria-pressed="true"' if self_mark == key else ""
        buttons += (
            f'<button type="button" class="mark" data-mark="{key}"{pressed}>'
            f"{symbol} {label}</button>"
        )
    field = f"answer-{item.item_id}"
    return f"""<article class="check" data-item="{escape(item.item_id)}" data-lesson="{escape(lesson.slug)}">
<h3>Question {number}</h3>
<div class="question">{render_markdown(item.question)}</div>
<form class="answer-form">
  <label for="{field}">Your answer (from memory, before you look)</label>
  <textarea id="{field}" name="answer" rows="4" maxlength="4000" required>{escape(answer)}</textarea>
  <div class="row">
    <button type="submit">Save answer</button>
    <span class="status" role="status">{escape(status)}</span>
  </div>
</form>
<div class="row">
  <button type="button" class="show-answer"{"" if answer else " disabled"}>Show answer</button>
  <span class="hint">Save an answer first; then check it.</span>
</div>
<div class="answer-key" hidden>
  <p class="cell-label">From the review queue</p>
  <div class="key-text">{render_markdown(item.concept)}</div>
  <p>How did you do? Your mark is provisional; the official one comes at <code>/standup</code>.</p>
  <div class="row marks">{buttons}</div>
</div>
<p class="mark-line" role="status">{mark_line}</p>
</article>"""


def render_lesson(
    lesson: Lesson,
    *,
    terms: list[Term],
    commands: tuple[str, str] | None,
    checks: list[QueueItem],
    signals: dict[str, str],
    answers: dict,
    tasks: dict,
    side: str,
) -> str:
    issue = lesson.issue_number
    ticket_link = (
        f' <a href="{ISSUES_URL}/{issue}">Ticket #{issue} on GitHub</a>'
        if issue
        else ""
    )
    if commands:
        intro, topics_md = split_sections(commands[1], 3)
        folds, _index = render_folds(topics_md, prefix="cmd-")
        commands_html = (
            f'<p class="cell-label">{escape(commands[0])}</p>'
            '<p class="note">Open a topic to see its commands. Each code block has a '
            "Copy button; click any <code>inline code</code> to copy it.</p>"
            + render_markdown(intro)
            + folds
            + '<p class="note">Every day\'s commands are in '
            '<a href="/reference/cheatsheet">the cheatsheet</a>.</p>'
        )
    else:
        commands_html = (
            '<p class="gap">The cheatsheet has no section for this day. See '
            '<a href="/reference/cheatsheet">the full cheatsheet</a>.</p>'
        )
    if checks:
        checks_html = "".join(
            _check(number, lesson, item, answers.get(item.item_id, {}))
            for number, item in enumerate(checks, start=1)
        )
    else:
        checks_html = (
            '<p class="gap">No review-queue item for this day has a question '
            "written yet.</p>"
        )
    answered = sum(1 for item in checks if item.item_id in answers)

    grade_rows = [("Quiz (learning log)", render_inline(lesson.quiz or "not recorded"))]
    for column in ("Quiz %", "Highest hint rung", "Errors I read myself / with help"):
        if signals.get(column):
            grade_rows.append((column, render_inline(signals[column])))
    marked = [answers[i.item_id] for i in checks if i.item_id in answers]
    if marked:
        tally = ", ".join(
            MARKS.get(entry.get("self_mark") or "", "not marked") for entry in marked
        )
        grade_rows.append(("Knowledge checks here (provisional)", escape(tally)))
    grade_html = "".join(
        f'<tr><th scope="row">{escape(label)}</th><td>{value}</td></tr>'
        for label, value in grade_rows
    )

    ticked = tasks.get(lesson.slug, {})
    done = answered + sum(1 for key in MANUAL_TASKS if ticked.get(key))
    total = len(checks) + len(MANUAL_TASKS)

    task_rows = ""
    for key, (label, href) in MANUAL_TASKS.items():
        checked = " checked" if ticked.get(key) else ""
        task_rows += (
            f'<li><input type="checkbox" class="task" id="task-{key}" '
            f'data-lesson="{escape(lesson.slug)}" data-task="{key}"{checked}>'
            f'<label for="task-{key}">{escape(label)}</label> '
            f'<a href="{href}">Go</a></li>'
        )
    if checks:
        all_answered = " checked" if answered == len(checks) else ""
        task_rows += (
            f'<li><input type="checkbox" id="task-checks" disabled{all_answered}>'
            f'<label for="task-checks">Answer the knowledge checks '
            f"({answered} of {len(checks)} answered; ticks itself)</label> "
            '<a href="#check">Go</a></li>'
        )
    shipped = _split_items(lesson.shipped)
    more = " and more" if len(shipped) > 1 else ""
    built_line = (
        f"<p>What came out of it: {render_inline(shipped[0])}{more}. "
        '<a href="#built">See what I built</a>.</p>'
        if shipped
        else ""
    )

    body = f"""<p class="kicker">Lesson · Day {escape(lesson.day)} · {escape(lesson.date)} · <span class="state done">Done</span></p>
<h1>{render_inline(lesson.ticket)}</h1>
{_progress_bar(done, total, "tasks done")}

<section id="overview"><h2>Overview</h2>
<p>This session's work: {render_inline(lesson.ticket)}.{ticket_link or " No ticket for this session."}</p>
{built_line}
</section>

<section id="objectives"><h2>Learning objectives</h2>
<p>What this lesson covered, from the learning log:</p>
{_bullets(lesson.concept, separators=";,")}
</section>

<section id="tasks"><h2>Task list</h2>
<ul class="tasks">{task_rows}</ul>
<p class="note">More on this page: <a href="#why">why it matters</a> ·
<a href="#built">what I built</a> · <a href="#grade">my grade</a> ·
<a href="#next">what came next</a>.</p>
</section>

<section id="why"><h2>Why it matters on the job</h2>
<p class="gap">The docs don't record this for past lessons. It lives in the
ticket's Context on GitHub{" (linked above)" if issue else ""}; from slice 3,
<code>/wrap</code> can write it into the learning log.</p>
</section>

<section id="built"><h2>What I built</h2>
{_bullets(lesson.shipped)}
<h3>What was hard</h3>
{_bullets(lesson.blockers)}
</section>

<section id="terms" class="copyable"><h2>New terms</h2>
<p class="note">Glossary terms named in this lesson's log entry.</p>
{_term_rows(terms)}
</section>

<section id="commands" class="copyable"><h2>Commands</h2>
{commands_html}
</section>

<section id="check"><h2>Knowledge check</h2>
{checks_html}
</section>

<section id="grade"><h2>My grade</h2>
<table class="grade"><tbody>{grade_html}</tbody></table>
</section>

<section id="next"><h2>What came next</h2>
{_bullets(lesson.next_up)}
</section>"""
    return page(
        f"Day {lesson.day}", body, side=side, crumbs=[("Table of contents", "/")]
    )


# --- course resources ---------------------------------------------------------


def render_reference_index(side: str) -> str:
    cards = "".join(
        f"""<li><a class="card" href="/reference/{slug}">
<span class="card-title">{escape(title)}</span>
<span class="note">{escape(about)} · <code>docs/{escape(file)}</code></span></a></li>"""
        for slug, (title, file, about) in REFERENCE.items()
    )
    body = f"""<h1>Course resources</h1>
<p class="lead">The whole reference docs, shown in full. Each page is built
from its file in <code>docs/</code> when you open it.</p>
<ul class="cards">{cards}</ul>"""
    return page("Course resources", body, side=side, area="reference")


def render_reference(slug: str, flattened_markdown: str, side: str) -> str:
    """One whole doc. `flattened_markdown` has its drop-downs already turned
    into headings (see `parse.flatten_details`)."""
    title, file, _about = REFERENCE[slug]
    intro, sections = split_sections(flattened_markdown, 2)
    folds, index = render_folds(sections)
    body = f"""<h1>{escape(title)}</h1>
<p class="note">Built from <code>docs/{escape(file)}</code>. Open a section to
read it. Each code block has a Copy button; click any <code>inline code</code>
to copy it.</p>
{_jump_list(index)}
<div class="doc copyable">{render_markdown(intro)}{folds}</div>"""
    return page(
        title,
        body,
        side=side,
        area="reference",
        crumbs=[("Course resources", "/reference")],
    )


def render_not_found(what: str, side: str = "") -> str:
    body = (
        f"<h1>Not found</h1><p>{escape(what)}</p>"
        '<p><a href="/">Back to the table of contents</a></p>'
    )
    return page("Not found", body, side=side)
