# Learning Hub: brief

Agreed 2026-11-25. Tracking issues: #24 (slice 1), #25, #26, #27, #28, #29 (GitHub Pages). Each is blocked by the one before it.

## Problem

My study material is spread over nine docs that Claude maintains, and my first
study site (a separate MkDocs repo) was read-only and easy to lose. I want one
local site, laid out like a course, that I can work in, and that tells Claude at
`/standup` how I'm doing. The docs stay the single source; the hub never holds a
copy of their content.

## User stories

1. **Map.** On the home page I see what the platform builds, every phase
   including AWS, where I am and what's next.
2. **Course layout.** Learning path → modules (curriculum phases) → lessons,
   with clear sections and headers and few dropdowns.
3. **Done lessons.** Each row of `docs/LEARNING_LOG.md` is one lesson: the goal,
   why it matters on the job, what I built and how it works, new terms,
   commands, a knowledge check and my grade. Its ticket is a link.
4. **Working ahead.** Planned sessions from `docs/TODAYS_LESSON_PLAN.md` (today
   + 3 ahead) are lessons I can open early: goal, concept, do-it-yourself path,
   checkpoint answers hidden until I ask. Curriculum order only.
5. **Lesson states.** done / in progress / available to work ahead / upcoming
   (milestones only).
6. **Knowledge checks.** Free-text questions from a `Question` column in
   `docs/REVIEW_QUEUE.md`, worded as "predict the output" where it fits. I type
   an answer, reveal the concept and self-mark. The self-mark is provisional.
7. **Cert questions.** A separate small set in `docs/CERT_QUESTIONS.md`:
   original exam-style multiple choice, tagged with exam and objective,
   auto-graded, never moving review-queue boxes.
8. **Gradebook.** Quiz scores and hint-rung trend (COACHING signals), skills
   matrix 0–4, cert path progress, kept apart from concept grades.
9. **The loop.** My answers and marks save to `hub/progress.local.json`
   (gitignored). `/standup` reads it first: it gives official grades (only
   these move boxes) and, for work-ahead lessons, reviews what I did like a PR
   and quizzes me instead of re-teaching. `/wrap` writes the log row and
   carries scores into the public docs, so the lesson turns "done" with no
   duplicate.
10. **Can't lose it.** `python -m hub` starts it at `http://127.0.0.1:8765`.
    The command and URL are in the README, the CHEATSHEET and a VS Code task
    ("Start learning hub").

11. **Course frame.** Every page has the layout of a course site (the model is
    D2L Brightspace): a top bar of areas, a left table of contents where each
    lesson shows a tick or a count of what's left, and a progress bar at the
    top of a lesson. A lesson opens with Overview, Learning objectives and a
    Task list whose ticks save to the progress file. Long content (a day's
    commands, each reference section) sits in drop-downs; every code block has
    a Copy button. Structure only; no school or vendor branding.
12. **Course resources.** The whole Cheatsheet, Glossary and Resources docs each
    have a page, with drop-downs turned into headings and a jump list. (Added
    2026-11-25 after the slice 1 review; in slice 1.)

## How it works

Plain HTML/CSS/JS and Python; standard library plus the `markdown` package.
No framework, no build step: pages are built from the docs on each request.

| Piece | Takes in | Puts out |
|---|---|---|
| `hub/parse.py` | the Markdown docs | records: lessons, terms, queue items, phases |
| `hub/pages.py` | records + progress file | HTML for home, lesson, gradebook |
| `hub/server.py` | browser requests | pages; saved answers |
| `hub/progress.py` | an answer or lesson mark | validated JSON, written safely |
| `hub/static/hub.js` | clicks and typing | save requests |

Safety: the server listens on 127.0.0.1 only. Save requests are accepted only
when Origin and Host are the site's own address. Typed answers are escaped on
display, never rendered as HTML.

## Slices

Each slice is one issue, blocked by the one before, shipped as its own PR.

| # | Issue | Done when I can see | Who |
|---|---|---|---|
| 1 | #24 | One real lesson page (Day 3) from the docs, one knowledge check that saves and is read back; origin check, escaping and their tests; command + URL in README, CHEATSHEET, VS Code task | Claude |
| 2 | #25 | Home map and every lesson in its state, including work-ahead marking | Claude |
| 3 | #26 | The `/standup` + `/wrap` loop: progress file read first, work-ahead review, official grades, plan 3 sessions ahead | Claude; Thomas reviews the rule changes |
| 4 | #27 | Gradebook and the cert question set | Claude |
| 5 | #28 | Proposal to retire the old MkDocs `learning-hub` repo, with a side-by-side content list. Nothing deleted, archived or changed until Thomas approves | Claude proposes; Thomas decides |
| 6 | #29 | Read-only version (map, lessons, published grades; no answer boxes, no progress file) on GitHub Pages, custom subdomain, HTTPS enforced, domain verified. `phase-5`; the deploy workflow is a learning objective. Check the current GitHub Pages docs first | Thomas, with Claude teaching |

## Working rules

- Hub work alternates with learning sessions and never replaces one. The
  parked Day 4 branch (`9-first-pytest`) comes first at the next learning
  session.
- The hub is tooling, so Claude writes it and explains the pieces. All repo
  rules apply: synthetic data only, no employer or vendor names, the scan
  passes, Thomas merges.
- Slice 1 adds a column to `docs/REVIEW_QUEUE.md`, which `9-first-pytest` also
  edits; expect one table conflict when that branch merges `main`.

## Out of scope

Search; accounts; hosting the interactive part; editing the docs from the
site; AI grading inside the site; jumping ahead of curriculum order.

## Done criteria (slices 1–5)

- `python -m hub` starts it; the URL is in README, CHEATSHEET and the VS Code task.
- Every page is built from the docs; the hub holds no copy of their content.
- Every log row is a lesson; planned sessions are work-ahead lessons; later
  phases show milestones only.
- An answer or mark made on the site appears in `hub/progress.local.json`, and
  `/standup` reads it.
- Tests cover the parsers, the progress file, the origin check and escaping;
  `checks` is green.
- The scan passes; the progress file and answers are never committed.
- Each hub PR gets a fresh-chat `/review` before Thomas merges it.
