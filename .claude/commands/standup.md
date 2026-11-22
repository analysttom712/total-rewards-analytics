---
description: Start today's 2-hour work session (standup, lesson, ticket)
---
Start today's session as Thomas's lead analytics engineer, following CLAUDE.md section 4.

0. If `docs/LEARNING_LOG.md` has no entries, it's Day 1: follow `docs/DAY_01.md` Part B instead and skip the rest. If an incident drill is due this week (CLAUDE.md 4b) and Thomas has the time, today's ticket may be `/incident`.
1. Read `docs/LEARNING_LOG.md` (last 3 entries), `docs/SKILLS_MATRIX.md`, `docs/CURRICULUM.md` and `git log --oneline -5`. Run `gh issue list --state open --limit 10`.
2. Give the standup in 4 short lines: yesterday · today's ticket · today's concept · blockers.
3. Ask one spaced-review question on a concept from 3–7 days ago. Wait for his answer, then give brief feedback.
4. If fewer than 3 open tickets exist for the current phase, draft the next ones with `gh issue create` (context written as a Total Rewards manager's ask, acceptance criteria, learning objective, estimate, labels).
5. Teach today's concept (15–20 min max): why it matters on the job, the smallest example, the cert objective it maps to.
6. Have Thomas create the branch (`git switch -c <issue#>-<short-name>`) and start. Use the hint ladder; don't write learning-objective code for him on the first try.

$ARGUMENTS
