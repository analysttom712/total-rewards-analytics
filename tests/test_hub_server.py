"""Tests for hub/server.py and hub/pages.py (tooling, not a learning exercise).

Each test starts the real server on a free port against a tiny set of docs in
a temporary folder, so the repo's own docs and progress file are never touched.
"""

import http.client
import json
import threading

import pytest

from hub import parse, progress
from hub.server import HubConfig, create_server, is_allowed_host, is_allowed_save

LOG = """| Date | Day | Ticket | Concept | Shipped | Quiz | Blockers | Next |
|---|---|---|---|---|---|---|---|
| 2026-01-05 | 003 | #2 Functions and loops | `range()` | A loop | 1/3 | Naming | #3 |
"""
QUEUE = """| Concept | Box | Last seen | Result | Misses | Next due | Where taught | Question |
|---|---|---|---|---|---|---|---|
| `range(a, b)` stops before `b` | 2 | 2026-01-05 | ✓ | 2 | 2026-01-07 | Day 3 | What does `list(range(5, 8))` return? |
"""


@pytest.fixture
def site(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "LEARNING_LOG.md").write_text(LOG, encoding="utf-8")
    (docs / "REVIEW_QUEUE.md").write_text(QUEUE, encoding="utf-8")
    config = HubConfig(docs_dir=docs, progress_path=tmp_path / "progress.json", port=0)
    server = create_server(config)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    item_id = parse.parse_queue(QUEUE)[0].item_id
    yield {"port": port, "config": config, "item_id": item_id}
    server.shutdown()
    server.server_close()


def request(site, method, path, *, body=None, headers=None):
    port = site["port"]
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    send = {"Host": f"127.0.0.1:{port}", **(headers or {})}
    data = json.dumps(body).encode("utf-8") if body is not None else None
    connection.request(method, path, body=data, headers=send)
    response = connection.getresponse()
    text = response.read().decode("utf-8")
    connection.close()
    return response.status, text


def save(site, *, origin, answer="[5, 6, 7]", host=None):
    headers = {"Content-Type": "application/json"}
    if origin is not None:
        headers["Origin"] = origin
    if host is not None:
        headers["Host"] = host
    body = {"item_id": site["item_id"], "lesson": "day-003", "answer": answer}
    return request(site, "POST", "/api/answer", body=body, headers=headers)


def own_origin(site):
    return f"http://127.0.0.1:{site['port']}"


# --- the origin rule, as a pure function ------------------------------------


def test_only_the_sites_own_host_and_origin_may_save():
    assert is_allowed_save("127.0.0.1:8765", "http://127.0.0.1:8765", 8765)
    assert is_allowed_save("localhost:8765", "http://localhost:8765", 8765)
    assert not is_allowed_save("127.0.0.1:8765", "https://example.com", 8765)
    assert not is_allowed_save("127.0.0.1:8765", None, 8765)
    assert not is_allowed_save("127.0.0.1:8765", "null", 8765)
    assert not is_allowed_save("127.0.0.1:8765", "http://127.0.0.1:9999", 8765)
    assert not is_allowed_save("example.com", "http://127.0.0.1:8765", 8765)
    assert not is_allowed_host(None, 8765)


# --- through the running server ---------------------------------------------


def test_the_lesson_page_is_built_from_the_docs(site):
    status, html = request(site, "GET", "/lesson/day-003")
    assert status == 200
    assert "<h1>#2 Functions and loops</h1>" in html  # "#2" stays a ticket number
    assert "<code>list(range(5, 8))</code>" in html  # the question, rendered
    assert request(site, "GET", "/lesson/day-999")[0] == 404
    status, home = request(site, "GET", "/")
    assert status == 200
    assert '<html lang="en" data-theme="light">' in home  # light by default
    assert 'class="theme-toggle"' in home


def test_a_save_from_this_site_is_written_and_read_back(site):
    status, text = save(site, origin=own_origin(site))
    assert status == 200 and json.loads(text)["ok"] is True
    entry = progress.load(site["config"].progress_path)["answers"][site["item_id"]]
    assert entry["answer"] == "[5, 6, 7]"
    assert entry["question"] == "What does `list(range(5, 8))` return?"

    status, text = request(site, "GET", "/api/progress")
    assert json.loads(text)["answers"][site["item_id"]]["answer"] == "[5, 6, 7]"


@pytest.mark.parametrize("origin", ["https://example.com", "null", None])
def test_a_save_from_anywhere_else_is_rejected_and_writes_nothing(site, origin):
    status, _ = save(site, origin=origin)
    assert status == 403
    assert not site["config"].progress_path.exists()


def test_a_request_addressed_to_another_host_is_rejected(site):
    status, _ = save(site, origin=own_origin(site), host="example.com")
    assert status == 403
    assert request(site, "GET", "/", headers={"Host": "example.com"})[0] == 403
    assert not site["config"].progress_path.exists()


def test_a_save_must_be_json_and_name_a_real_question(site):
    headers = {"Origin": own_origin(site), "Content-Type": "text/plain"}
    assert request(site, "POST", "/api/answer", body={}, headers=headers)[0] == 415

    headers["Content-Type"] = "application/json"
    body = {"item_id": "q-not-real", "lesson": "day-003", "answer": "x"}
    assert request(site, "POST", "/api/answer", body=body, headers=headers)[0] == 400
    assert not site["config"].progress_path.exists()


def test_a_typed_answer_is_shown_as_text_never_as_html(site):
    nasty = '</textarea><script>alert("x")</script><b>bold</b>'
    assert save(site, origin=own_origin(site), answer=nasty)[0] == 200
    _, html = request(site, "GET", "/lesson/day-003")
    assert "<script>alert" not in html
    assert "<b>bold</b>" not in html
    assert "&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;" in html


def test_a_self_mark_is_saved_and_shown_as_provisional(site):
    save(site, origin=own_origin(site))
    headers = {"Origin": own_origin(site), "Content-Type": "application/json"}
    body = {"item_id": site["item_id"], "mark": "partial"}
    assert request(site, "POST", "/api/mark", body=body, headers=headers)[0] == 200
    _, html = request(site, "GET", "/lesson/day-003")
    assert "Your mark: ½ (provisional until /standup)" in html


def test_static_files_are_limited_to_the_known_names(site):
    assert request(site, "GET", "/static/hub.css")[0] == 200
    assert request(site, "GET", "/static/hub.js")[0] == 200
    assert request(site, "GET", "/static/theme.js")[0] == 200
    assert request(site, "GET", "/static/../server.py")[0] == 404
    assert request(site, "GET", "/static/progress.local.json")[0] == 404


def tick(site, task, done=True, lesson="day-003"):
    headers = {"Origin": own_origin(site), "Content-Type": "application/json"}
    body = {"lesson": lesson, "task": task, "done": done}
    return request(site, "POST", "/api/task", body=body, headers=headers)[0]


def test_the_table_of_contents_counts_down_to_a_tick(site):
    # One knowledge check + two hand-ticked tasks = 3 things to do.
    _, html = request(site, "GET", "/")
    assert 'title="3 tasks left">3</span>' in html
    assert "0 of 3 tasks done" in html

    save(site, origin=own_origin(site))
    assert tick(site, "terms") == 200
    _, html = request(site, "GET", "/")
    assert 'title="1 tasks left">1</span>' in html

    assert tick(site, "commands") == 200
    _, html = request(site, "GET", "/")
    assert "tasks left" not in html and 'class="tick"' in html

    assert tick(site, "terms", done=False) == 200  # unticking counts back up
    assert 'title="1 tasks left">1</span>' in request(site, "GET", "/")[1]


def test_a_lesson_opens_with_overview_objectives_and_a_task_list(site):
    assert tick(site, "terms") == 200
    _, html = request(site, "GET", "/lesson/day-003")
    for heading in ("Overview", "Learning objectives", "Task list"):
        assert f"<h2>{heading}</h2>" in html
    assert 'data-task="terms" checked>' in html
    assert 'data-task="commands">' in html
    assert "(0 of 1 answered; ticks itself)" in html


def test_only_real_tasks_on_real_lessons_can_be_ticked(site):
    assert tick(site, "not-a-task") == 400
    assert tick(site, "terms", lesson="day-999") == 400
    assert tick(site, "terms", done="yes") == 400
    assert not site["config"].progress_path.exists()


def test_course_resources_show_a_whole_doc_as_dropdown_sections(site):
    docs = site["config"].docs_dir
    (docs / "CHEATSHEET.md").write_text(
        "# Cheatsheet\n\n<details>\n<summary><b>Day 1 · Setup</b></summary>\n\n"
        "```powershell\ngit status\n```\n\n</details>\n",
        encoding="utf-8",
    )
    status, html = request(site, "GET", "/reference/cheatsheet")
    assert status == 200
    # Each day is a closed drop-down, listed under "On this page".
    assert '<details class="fold" id="day-1-setup">' in html and "git status" in html
    assert '<a href="#day-1-setup">' in html
    assert request(site, "GET", "/reference")[0] == 200
    assert (
        request(site, "GET", "/reference/glossary")[0] == 200
    )  # missing doc: empty page
    assert request(site, "GET", "/reference/secrets")[0] == 404


def test_split_sections_ignores_headings_inside_code():
    from hub.pages import render_folds, split_sections

    lines = [
        "intro",
        "",
        "## One",
        "",
        "```",
        "## not a heading",
        "```",
        "",
        "## One",
        "",
        "body two",
    ]
    intro, sections = split_sections(chr(10).join(lines), 2)
    assert intro.strip() == "intro"
    assert [title for title, _ in sections] == ["One", "One"]
    assert "## not a heading" in sections[0][1]
    _, index = render_folds(sections)
    assert [slug for slug, _ in index] == ["one", "one-2"]  # ids stay unique
