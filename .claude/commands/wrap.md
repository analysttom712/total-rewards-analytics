---
description: End today's session (verify, quiz, safety scan, commit, PR, log, learning loop, blog draft)
---
Wrap up today's session.

1. Run the checks for what changed (`ruff check`, `ruff format --check`, `pytest`, `dbt build`, or open the report). Show the results. Fix only what today's ticket needs.
2. Quiz: 3 questions on today's concept (one tied to a cert objective). Ask one at a time and score them. Skip this if `/quiz` already ran today; use that score.
3. **Public-repo safety scan** (CLAUDE.md 2a): `git status`, `git diff --staged`. Check for secrets, real-looking data, employer or vendor names, local paths with his username, AWS IDs, and personal details in screenshots. Flag anything found before committing.
4. Thomas commits with a clear message, pushes, and opens a PR with `gh pr create` that links the issue (`Closes #N` in the **body**). Review the diff like a senior teammate; Thomas merges.
5. Append to `docs/LEARNING_LOG.md`: date · day number · ticket · concept · what shipped · quiz score · blockers · next ticket.
6. Update `docs/SKILLS_MATRIX.md` ratings that changed (0–4), with a one-line reason. Add an ADR to `docs/DECISIONS.md` if a design choice was made.
7. **Learning loop** (the part that makes the next session better):
   - `docs/REVIEW_QUEUE.md`: add every concept taught today (box 1, due next session). Move quizzed items between boxes using the rules at the top of the file. Retire box-5 hits.
   - `docs/COACHING.md`: add a **Signals** row in section 7 (quiz %, highest hint rung, errors read himself / with help, one-line note) and a **retro line** in section 9 (what clicked · what to change). If something new worked or failed, fold it into the matching rule in sections 1–5, following the file's maintenance rules: strengthen an existing rule instead of adding a duplicate, and keep the file under ~150 lines.
   - **Adjustment rules check:** compare the last 3 Signals rows against the adjustment rules in COACHING.md section 8. Say which rule fires (or "none"), apply it to the NEXT and NEXT +1 plans, and update the "Current status" line in section 8.
   - `docs/GLOSSARY.md`: add every new symbol or term from today with its real name, plain English and a job analogy.
   - `docs/CHEATSHEET.md`: add a collapsible **day section** (`Day N · Mon DD · ticket`) with today's commands and patterns, one nested `<details>` per topic. Update the "Every session" quick reference only if a daily command changed.
   - `docs/RESOURCES.md`: add any useful link found today (check it loads first).
   - `docs/TODAYS_LESSON_PLAN.md`: tick today's ✅ "Done when" boxes and agenda status. If today's work ran short or long, shift the NEXT and NEXT +1 plans to match, so the next `/standup` starts from an accurate plan.
   - Every ~10 sessions (or 2 weeks): run the sprint review (CLAUDE.md section 4), including the docs cleanup in CLAUDE.md section 6.
8. Run the `/blog` steps to draft today's post.
9. Tell Thomas in two lines what he did today and what's next, plus the review items due next session.
10. End with: "Close this chat now and start a new one for the next session; everything it needs is in the files." (CLAUDE.md section 4: one session = one chat.)

$ARGUMENTS
