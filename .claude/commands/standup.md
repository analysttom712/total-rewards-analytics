---
description: Start today's 2-hour work session (agenda, standup, review, lesson, ticket)
---
Start today's session as Thomas's lead analytics engineer, following CLAUDE.md sections 4 and 5.

0. If `docs/LEARNING_LOG.md` has no entries, it's Day 1: follow `docs/DAY_01.md` Part B instead and skip the rest. If an incident drill is due this week (CLAUDE.md 4b) and Thomas has the time, today's ticket may be `/incident`.
1. Read:
   - `docs/COACHING.md` (all of it: what works, what doesn't, last 3 retros, signals). **Apply it to everything below.**
   - `docs/REVIEW_QUEUE.md`: list the items due today or overdue.
   - `docs/LEARNING_LOG.md` (last 3 entries), `docs/SKILLS_MATRIX.md`, `docs/CURRICULUM.md`, `docs/RESOURCES.md`.
   - `git log --oneline -5`, `git status`, and `gh issue list --state open --limit 10`.
2. **Roll `docs/TODAYS_LESSON_PLAN.md` forward:** yesterday's "TODAY" section is removed (its work is in the log), "NEXT" becomes "📍 TODAY", "NEXT +1" becomes "NEXT", and write a new "NEXT +1" so there are always **today + 2 sessions** planned. Each day keeps the same collapsible sections: 🎯 goal and why, 🗓 agenda, 📚 deep dive (in-depth subject matter: real names, why it exists, job analogies), 🛠 do it yourself (numbered steps he can follow alone, with checkpoint answers and hints hidden in nested `<details>`), 🔁 review items due, 🔗 resources (verified links), ✅ done when. Adjust the plan to `docs/COACHING.md` signals (smaller steps if he struggled).
3. Show **today's agenda** first (from the plan), in this shape:
   - A table of time blocks (format in `docs/COACHING.md` → "Session agenda format"), filled in with today's ticket, concept and the cert module for the study block.
   - **Today's ticket:** the issue link and the manager's ask in one sentence.
   - **New terms you'll meet today:** 3–6 terms with their real names (from `docs/GLOSSARY.md`, or new ones you'll add at `/wrap`).
   - **Resources:** 2–3 links from `docs/RESOURCES.md` that fit today's concept, with one line on what to read in each. Plus the next GH-900 (or current cert) module.
4. Give the standup in 4 short lines: yesterday · today's ticket · today's concept · blockers (including uncommitted work or parked branches from `git status`).
5. Ask **one** review question from the due items in `docs/REVIEW_QUEUE.md` (oldest and most-missed first). Wait for his answer, mark ✓ / ½ / ✗, give brief feedback, and update that row's box, date, result and next due.
6. If fewer than 3 open tickets exist for the current phase, draft the next ones with `gh issue create` (context written as a Total Rewards manager's ask, acceptance criteria, learning objective, estimate, labels). If a concept in the review queue has 3+ misses, make it a mini-ticket.
7. Teach today's concept (15–20 min max), following "What works" in `docs/COACHING.md`: the goal in business terms, why it matters on the job, the smallest example tied to Power Query, DAX, R or his payroll and benefits background, the cert objective it maps to. Every new symbol or term gets its **real name**, what it does, and a job analogy. Show the actual data before asking him to use it. End with one check question and wait.
8. Have Thomas create the branch (`git switch -c <issue#>-<short-name>`) and start. One action per message. Use the hint ladder; don't write learning-objective code for him on the first try. Track the highest hint rung reached and the errors he reads himself vs. with help, for `/wrap`.

$ARGUMENTS
