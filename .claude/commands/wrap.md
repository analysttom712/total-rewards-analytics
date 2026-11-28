---
description: End today's session (verify, quiz, log, learning loop, blog draft, safety scan, one commit and PR)
---
Wrap up today's session. Everything below is written on today's branch (the one `/standup` started) and ships in **one PR** at the end: the ticket's code and the session's notes together. Don't open the PR until the notes are written.

1. Run the checks for what changed (`ruff check`, `ruff format --check`, `dbt build`, or open the report), and always run the full test suite once: `python -m pytest`. Show the results, pass/fail counts included. A red test that belongs to a test-first exercise Thomas is still solving is expected: say so instead of fixing it. Fix only what today's ticket needs.
2. Quiz: 3 questions on today's concept (one tied to a cert objective). Ask one at a time and score them. Skip this if `/quiz` already ran today; use that score.
3. Append to `docs/LEARNING_LOG.md`: date · day number · ticket · concept · what shipped · quiz score · blockers · next ticket. Rewrite the resume note at the bottom so it is true today: remove open items that were settled.
   - **Every session, update the `## Status` section of `README.md`:** the day number and phase, a short list of what's built and passing (per hard rule 4: today's ticket only if its tests pass; it merges in the same PR as this line), and the next ticket.
   - **`docs/RESUME_LINES.md`:** add or tighten a line only when a curriculum milestone (`docs/CURRICULUM.md`) has merged to `main` with CI green. Each line names what was built and the tools, with no metric that isn't measured in the repo. No milestone merged today means no change; an empty file is correct until then.
4. Update `docs/SKILLS_MATRIX.md` ratings that changed (0–4), with a one-line reason. Add an ADR to `docs/DECISIONS.md` if a design choice was made.
5. **Learning loop** (the part that makes the next session better):
   - `docs/REVIEW_QUEUE.md` (rules at the top of the file):
     - Add every concept taught today at box 1, due next session, unless a row for it already exists. `/wrap` is the only command that adds rows.
     - Then move only the items this wrap's quiz asked (step 2). Items `/standup` or `/quiz` already moved today stay where they are.
     - If `/quiz` held results for concepts that had no row yet, add those rows now with their result.
     - Retire box-5 hits.
   - `docs/COACHING.md`: add a **Signals** row in section 7 (quiz %, highest hint rung, errors read himself / with help, one-line note) and a **retro line** in section 9 (what clicked · what to change). If something new worked or failed, fold it into the matching rule in sections 1–5, following the file's maintenance rules: strengthen an existing rule instead of adding a duplicate, and keep the file under ~150 lines.
   - **Adjustment rules check:** compare the last 3 Signals rows against the adjustment rules in COACHING.md section 8. Say which rule fires (or "none"), apply it to the NEXT and NEXT +1 plans, and update the "Current status" line in section 8.
   - `docs/GLOSSARY.md`: add every new symbol or term from today with its real name, plain English and a job analogy.
   - `docs/CHEATSHEET.md`: add a collapsible **day section** (`Day N · Mon DD · ticket`) with today's commands and patterns, one nested `<details>` per topic. Update the "Every session" quick reference only if a daily command changed.
   - `docs/RESOURCES.md`: add any useful link found today (check it loads first).
   - `docs/TODAYS_LESSON_PLAN.md`: tick today's ✅ "Done when" boxes and agenda status. If today's work ran short or long, shift the NEXT and NEXT +1 plans to match, so the next `/standup` starts from an accurate plan.
   - Every ~10 sessions (or 2 weeks): run the sprint review (CLAUDE.md section 4), including the docs cleanup in CLAUDE.md section 6.
6. Run the `/blog` steps to draft today's post.
7. **Public-repo safety check** (CLAUDE.md 2a): `scripts/public_scan.py` runs on every commit and covers secrets, AWS IDs, home-folder paths and blocklisted names. Review `git status` and `git diff --staged` for what it can't judge: real people's names, real-looking data, and personal details in screenshots. Flag anything found before committing.
8. **One commit, one PR.** Thomas commits with a clear message (his git config, no co-author lines: hard rule 7) and pushes.
   - Ticket finished: open the PR with `gh pr create`, with `Closes #N` in the **body**. For a learning-objective ticket, suggest `/review` in a new chat before he merges (CLAUDE.md section 5). Thomas merges.
   - Ticket not finished: push the branch and open no PR. The log's resume note names the branch and the exact next step.
9. Tell Thomas in two lines what he did today and what's next, plus the review items due next session.
10. End with: "Close this chat now and start a new one for the next session; everything it needs is in the files." (CLAUDE.md section 4: one session = one chat.)

$ARGUMENTS
