---
description: Start today's work session (map, agenda, standup, review, lesson, ticket)
---
Start today's session as Thomas's lead analytics engineer, following CLAUDE.md sections 4 and 5 and `docs/COACHING.md`.

0. If an incident drill is due this week (cadence in `docs/INCIDENTS.md`) and Thomas has the time, today's ticket may be `/incident`.
1. Read:
   - `docs/COACHING.md` (all of it: reply rules, code steps, errors, agenda, signals, adjustment rules, last 3 retros). **Apply it to everything below.**
   - `docs/REVIEW_QUEUE.md`: list the items due today or overdue.
   - `docs/LEARNING_LOG.md` (last 3 entries), `docs/SKILLS_MATRIX.md`, `docs/CURRICULUM.md`, `docs/RESOURCES.md`.
   - `git log --oneline -5`, `git status`, and `gh issue list --state open --limit 10`.
   - If the last `docs/LEARNING_LOG.md` entry stopped mid-ticket, today **resumes** from its next-step note instead of starting a new ticket (COACHING.md section 6).
2. **Get on today's branch before editing any file.** Every note this session writes (lesson plan, review queue, log) ships on this branch, in the session's one PR.
   - If `git status` shows uncommitted changes on `main`, stop and sort them out with Thomas first (commit them to the branch they belong to, or stash them). Don't carry them into today's branch.
   - Resuming: Thomas switches to the parked branch (`git switch <branch>`).
   - New ticket: Thomas pulls `main` and creates the branch (`git switch -c <issue#>-<short-name>`).
3. **Roll `docs/TODAYS_LESSON_PLAN.md` forward** (skip this when resuming: today is still the same "📍 TODAY"). The last session's "TODAY" section is removed (its work is in the log), "NEXT" becomes "📍 TODAY", "NEXT +1" becomes "NEXT", and write a new "NEXT +1" so there are always **today + 2 sessions** planned. Each day keeps the same collapsible sections: 🎯 goal and why, 🗓 agenda, 📚 deep dive (in-depth subject matter: real names, why it exists, job analogies), 🛠 do it yourself (numbered steps he can follow alone, written in the COACHING.md section 2 code-step format, with checkpoint answers and hints hidden in nested `<details>`), 🔁 review items due, 🔗 resources (verified links), ✅ done when. Adjust the plan to the COACHING.md signals and adjustment rules (smaller steps if he struggled).
4. **Open with the map** (COACHING.md section 1): one short screen with what the project builds → where today's ticket fits → what "done today" looks like, as numbered steps. Handle known risks now (COACHING.md section 3), e.g. inline suggestions off.
5. Then show **today's agenda** (from the plan):
   - The block table from COACHING.md section 6 (in order, no durations), filled in with today's ticket, concept and the cert module for the study block.
   - **Today's ticket:** the issue link and the manager's ask in one sentence.
   - **New terms you'll meet today:** 3–6 terms with their real names (from `docs/GLOSSARY.md`, or new ones you'll add at `/wrap`).
   - **Resources:** 2–3 links from `docs/RESOURCES.md` that fit today's concept, with one line on what to read in each. Plus the next GH-900 (or current cert) module.
6. Give the standup in 4 short lines: yesterday · today's ticket · today's concept · blockers (including parked branches from `git status`).
7. Ask **one** review question from the due items in `docs/REVIEW_QUEUE.md` (oldest and most-missed first). Wait for his answer, mark ✓ / ½ / ✗, give brief feedback, and update that row's box, date, result, misses and next due. Standup moves only this one item.
8. **Tickets: draft, show, then create.** If fewer than 3 open tickets exist for the current phase, draft the next ones (context written as a Total Rewards manager's ask, acceptance criteria, learning objective, estimate, labels). If a queue item's Misses has reached 3 and it has no mini-ticket yet, draft one for it. Show each draft in chat and run `gh issue create` only after Thomas OKs it: the repo is public.
9. Teach today's concept **before the build** (COACHING.md section 6), following COACHING.md sections 1 and 5: the goal in business terms, why it matters on the job, the smallest example tied to Power Query, DAX, R or his payroll and benefits background, the cert objective it maps to. Every new symbol or term gets its **real name**, what it does, and a job analogy. Show the actual data before asking him to use it. End with one check question and wait.
10. Start the build. One action per message. Every code step uses the COACHING.md section 2 format (Task, Fill in, Clues, Where it goes, Check) and its hint ladder. After each step, say "Step N of M done: <what's now true>. Next: <goal>." Track the highest hint rung reached and the errors he reads himself vs. with help, for `/wrap`.

$ARGUMENTS
