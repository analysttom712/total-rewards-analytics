# Coaching Playbook

How I learn best, written down so every session builds on the last. `/standup` reads this before teaching; `/wrap` adds a retro and a signals row. Every 2 weeks the sprint review applies the adjustment rules.

## What works

- **One action per message.** Say the goal in business terms, connect it to something I know, give exactly one thing to do, then wait.
- **Show the data before using it.** Print or paste the actual row/dict/table before asking me to pull a value out of it (Day 3: `job_row`).
- **Say where every value comes from.** "Already in `job_row`" isn't enough; show `job_row` and the exact lookup.
- **Power Query / Power BI comparisons land:** "Changed Type", ABC123 (Any), custom function invoked per row, `let` steps, Column tools format vs data type.
- **Payroll / accounting comparisons land:** exclusive cutoff date (`range` stop), payment referencing an invoice (`Closes #N`), posted journal entry (commit).
- **Real names for symbols.** Tell me what `""` *is* (a string literal), not just what it does. Add it to `docs/GLOSSARY.md`.
- **Tables mapping "what I wrote" vs "what it should be".**
- **Reading the error out loud** (type, line, plain-English meaning) before fixing it.
- **Running it to see the real output** and spot-checks (count, first row, last row).
- **Predict before running.** "What will `jobs[3]` return?", then run it. Day 3 review: 6/6 lookup predictions reasoned correctly.
- **Hands-on Git on real work.** Staging, unstaging and committing the actual learning-loop files made the four states stick (then shipped PR #15).
- **Exam-style multiple choice** for cert questions.

## What doesn't work

- Bundling a lesson, an example and a coding task in one message.
- Generic examples that don't map to today's task (Day 2: copied the `plans` example verbatim).
- Skipping the "where does this come from" step.
- Assuming I know which terminal/editor/website I'm in.
- Assuming I know which **file** I'm typing in. When pasted code looks odd, check `git status` first (Day 3 review: practice code went into `hello_employee.py`).
- AI inline suggestions (grey ghost text) during practice: they write code I didn't reason through. Esc, or toggle them off.
- Diagrams in a code box: they get run as commands. Diagrams go in a `text` box.

## Session agenda format

Every `/standup` shows today's agenda before teaching:

| Block | Time | What |
|---|---|---|
| Standup + review | 10 min | yesterday · due review questions |
| Lesson | 15–20 min | today's concept, with new terms named |
| Build | 60–75 min | the ticket, one step at a time |
| Check | 10 min | run it · `/quiz` |
| Ship | 10 min | commit → PR → merge |
| Cert study | 15 min | the next Microsoft Learn / cert module (see `docs/RESOURCES.md`) |

Plus: 2–3 links for today's concept from `docs/RESOURCES.md`, and the new terms I'll meet today.

## Signals

One row per session (filled in by `/wrap`).

| Date | Day | Quiz % | Highest hint rung | Errors I read myself / with help | Note |
|---|---|---|---|---|---|
| 2026-11-22 | 001 | 17% | partial code | ~0 / ~4 | First Git + Python; mechanics were the hard part |
| 2026-11-23 | 002 | 83% | partial code | ~1 / ~5 | Reset to one-step pace worked |
| 2026-11-24 | 003 | 17% (wrap) · 50% (/quiz) | partial code | ~2 / ~7 | Naming (list vs loop var vs row); range stop |
| 2026-11-24 | 003 review | 70% (/quiz 3.5/5) | partial code (premium loop) | 4 / 4 | Predictions strong (lookups, shape, dtypes, `range`); typed into the wrong file, AI autocomplete took over |

Days 1–3 error counts are estimates from the log (`~`); counted exactly from Day 4.

Hint rungs: **nudge** → **bigger hint** → **partial code**.

## Adjustment rules (applied at each sprint review, every 2 weeks)

- Quiz average < 60% **or** most steps needed partial code → smaller steps, split the next ticket, more worked examples.
- Quiz average > 80% **and** most steps solved at nudge → stretch ticket, fewer hints, ask before telling more often.
- A concept missed 3 times → its own mini-ticket (see `docs/REVIEW_QUEUE.md`).
- Errors read myself goes up over time → hand me error reading first, before any hint.

## Retro log

Two lines per session: what clicked, what to change. Newest at the bottom.

- **2026-11-22 (Day 1):** Clicked: commit = posted journal entry; PR = recon sent for review. Change: say which window (terminal / editor / GitHub) every time.
- **2026-11-23 (Day 2):** Clicked: filling in the job table in plain words before any Python. Change: never jump from a generic example to the real task without mapping it.
- **2026-11-24 (Day 3):** Clicked: Power Query "Changed Type" for `to_datetime`; three-names table for the loop; payroll cutoff for `range`. Change: show the data (e.g. `job_row`) before asking me to use it; give real names and deeper insight for symbols; show a daily agenda with resources.
- **2026-11-24 (Day 3 review):** Clicked: Git states by doing them on real files; `print` = card visual vs `return` = measure; predicting errors before running. Change: confirm which file he's editing before reviewing code; keep practice in the REPL or a scratch file; turn off inline suggestions for learning-objective code.
