"""The local web server.

Takes in: browser requests on 127.0.0.1.
Puts out: pages built fresh from the docs, and saved answers in the progress file.

It listens on this PC only. Every request must name the site's own address in
its Host header, and every save must also come from the site's own pages
(Origin header); anything else gets 403.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from hub import pages, parse, progress

STATIC_TYPES = {
    "hub.css": "text/css; charset=utf-8",
    "hub.js": "text/javascript; charset=utf-8",
    "theme.js": "text/javascript; charset=utf-8",
}
MAX_BODY_BYTES = 16_384


@dataclass(frozen=True)
class HubConfig:
    docs_dir: Path
    progress_path: Path
    port: int
    static_dir: Path = Path(__file__).resolve().parent / "static"


def allowed_hosts(port: int) -> set[str]:
    return {f"127.0.0.1:{port}", f"localhost:{port}"}


def is_allowed_host(host: str | None, port: int) -> bool:
    """True only when the request was addressed to this site."""
    return host in allowed_hosts(port)


def is_allowed_save(host: str | None, origin: str | None, port: int) -> bool:
    """True only when a save was sent to this site *by* this site's own page.

    A page on another website can make the browser send a request here; the
    browser then reports that other site in the Origin header, and it is refused.
    A missing Origin is refused too.
    """
    if not is_allowed_host(host, port):
        return False
    return origin in {f"http://{name}" for name in allowed_hosts(port)}


def make_handler(config: HubConfig) -> type[BaseHTTPRequestHandler]:
    class HubHandler(BaseHTTPRequestHandler):
        server_version = "LearningHub"

        # -- helpers ---------------------------------------------------------

        def _port(self) -> int:
            return self.server.server_address[1]

        def _send(self, status: int, body: str, content_type: str) -> None:
            data = body.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'")
            self.end_headers()
            self.wfile.write(data)

        def _html(self, status: int, body: str) -> None:
            self._send(status, body, "text/html; charset=utf-8")

        def _json(self, status: int, payload: dict) -> None:
            self._send(status, json.dumps(payload), "application/json")

        def _doc(self, name: str) -> str:
            return parse.read_doc(config.docs_dir, name)

        def _lessons(self) -> list[parse.Lesson]:
            return parse.parse_lessons(self._doc("LEARNING_LOG.md"))

        # -- GET -------------------------------------------------------------

        def do_GET(self) -> None:
            if not is_allowed_host(self.headers.get("Host"), self._port()):
                self._html(403, "Forbidden")
                return
            path = self.path.split("?", 1)[0]
            if path.startswith("/static/"):
                self._static(path.removeprefix("/static/"))
                return
            if path == "/api/progress":
                self._progress()
                return

            # Every page shares the same left table of contents, so read what
            # it needs once: the lessons, the queue and the saved answers.
            lessons = self._lessons()
            queue = parse.parse_queue(self._doc("REVIEW_QUEUE.md"))
            try:
                saved = progress.load(config.progress_path)
            except progress.ProgressError as err:
                self._html(500, pages.render_not_found(f"Progress file problem: {err}"))
                return
            answers = saved["answers"]
            tasks = saved.get("tasks", {})
            side = pages.build_sidebar(lessons, queue, answers, tasks, path)

            if path == "/":
                self._html(200, pages.render_home(lessons, queue, answers, tasks, side))
            elif path.startswith("/lesson/"):
                slug = path.removeprefix("/lesson/")
                lesson = next((x for x in lessons if x.slug == slug), None)
                if lesson is None:
                    self._html(
                        404, pages.render_not_found("No lesson with that name.", side)
                    )
                else:
                    self._lesson(lesson, queue, answers, tasks, side)
            elif path == "/reference":
                self._html(200, pages.render_reference_index(side))
            elif path.removeprefix("/reference/") in pages.REFERENCE:
                slug = path.removeprefix("/reference/")
                text = parse.flatten_details(self._doc(pages.REFERENCE[slug][1]))
                self._html(200, pages.render_reference(slug, text, side))
            else:
                self._html(
                    404, pages.render_not_found("No page at that address.", side)
                )

        def _lesson(
            self,
            lesson: parse.Lesson,
            queue: list[parse.QueueItem],
            answers: dict,
            tasks: dict,
            side: str,
        ) -> None:
            day = lesson.day_number
            html = pages.render_lesson(
                lesson,
                terms=parse.terms_for_lesson(
                    lesson, parse.parse_glossary(self._doc("GLOSSARY.md"))
                ),
                commands=(
                    parse.cheatsheet_day(self._doc("CHEATSHEET.md"), day)
                    if day is not None
                    else None
                ),
                checks=parse.checks_for_lesson(lesson, queue),
                signals=parse.signals_for_lesson(lesson, self._doc("COACHING.md")),
                answers=answers,
                tasks=tasks,
                side=side,
            )
            self._html(200, html)

        def _static(self, name: str) -> None:
            # Only the known file names are served, so no path can escape.
            if name not in STATIC_TYPES:
                self._html(404, pages.render_not_found("No such file."))
                return
            text = (config.static_dir / name).read_text(encoding="utf-8")
            self._send(200, text, STATIC_TYPES[name])

        def _progress(self) -> None:
            try:
                self._json(200, progress.load(config.progress_path))
            except progress.ProgressError as err:
                self._json(500, {"ok": False, "error": str(err)})

        # -- POST ------------------------------------------------------------

        def do_POST(self) -> None:
            headers = self.headers
            if not is_allowed_save(
                headers.get("Host"), headers.get("Origin"), self._port()
            ):
                self._json(
                    403,
                    {"ok": False, "error": "Saves are only accepted from this site."},
                )
                return
            if (
                headers.get("Content-Type", "").split(";")[0].strip()
                != "application/json"
            ):
                self._json(415, {"ok": False, "error": "Send JSON."})
                return
            try:
                length = int(headers.get("Content-Length", "0"))
            except ValueError:
                length = -1
            if not 0 < length <= MAX_BODY_BYTES:
                self._json(
                    413, {"ok": False, "error": "Request is empty or too large."}
                )
                return
            try:
                body = json.loads(self.rfile.read(length).decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                body = None
            if not isinstance(body, dict):
                self._json(400, {"ok": False, "error": "Request is not valid JSON."})
                return

            try:
                if self.path == "/api/answer":
                    entry = self._save_answer(body)
                elif self.path == "/api/mark":
                    entry = progress.save_self_mark(
                        config.progress_path,
                        item_id=str(body.get("item_id", "")),
                        mark=str(body.get("mark", "")),
                    )
                elif self.path == "/api/task":
                    entry = self._save_task(body)
                else:
                    self._json(404, {"ok": False, "error": "No such action."})
                    return
            except progress.ProgressError as err:
                self._json(400, {"ok": False, "error": str(err)})
                return
            except OSError as err:
                # The disk refused the write (file open elsewhere, disk full).
                # Say so, rather than dropping the connection with no reply.
                self._json(
                    500, {"ok": False, "error": f"Could not write the file: {err}"}
                )
                return
            self._json(200, {"ok": True, "entry": entry})

        def _save_task(self, body: dict) -> dict:
            slug = body.get("lesson")
            if not any(lesson.slug == slug for lesson in self._lessons()):
                raise progress.ProgressError("That lesson is not in the learning log.")
            if body.get("task") not in pages.MANUAL_TASKS:
                raise progress.ProgressError("That task is not on the task list.")
            return progress.save_task(
                config.progress_path,
                lesson=slug,
                task=body["task"],
                done=body.get("done"),
            )

        def _save_answer(self, body: dict) -> dict:
            # The question and concept are looked up in the docs here; the
            # browser only says *which* item it is answering.
            queue = parse.parse_queue(self._doc("REVIEW_QUEUE.md"))
            item = next(
                (q for q in queue if q.item_id == body.get("item_id") and q.question),
                None,
            )
            if item is None:
                raise progress.ProgressError(
                    "That question is not in the review queue."
                )
            slug = body.get("lesson")
            if not any(lesson.slug == slug for lesson in self._lessons()):
                raise progress.ProgressError("That lesson is not in the learning log.")
            return progress.save_answer(
                config.progress_path,
                item_id=item.item_id,
                lesson=slug,
                question=item.question,
                concept=item.concept,
                answer=body.get("answer", ""),
            )

        def log_message(self, format: str, *args: object) -> None:
            # One short line per request, without the client address.
            print(f"  {format % args}")

    return HubHandler


def create_server(config: HubConfig) -> ThreadingHTTPServer:
    """A server bound to 127.0.0.1 (this PC only). Port 0 picks a free port."""
    return ThreadingHTTPServer(("127.0.0.1", config.port), make_handler(config))
