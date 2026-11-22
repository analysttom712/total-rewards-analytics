---
description: Run a pipeline incident drill (tutor breaks something; Thomas troubleshoots)
---
Run an incident drill per CLAUDE.md section 4b.

1. Read `docs/incidents/README.md` (drill history) and `docs/CURRICULUM.md` to find the current phase. Pick a fault at or one level below the current drill level. Don't repeat a fault type from the last 3 drills.
2. On a new branch `incident/NNN`, inject exactly the fault(s) for this level. Use a vague commit message ("incident NNN setup"). Never touch `main` directly, never break anything outside the repo, never create AWS resources that bill, and never inject real secrets (use obviously fake ones like `AKIAFAKEFAKEFAKE0000`).
3. Give Thomas only what a real on-call analyst would get: a short "ticket from the business," e.g. *"Hi, the benefits cost dashboard shows 2x the employees in Finance this morning. Can you look? –Total Rewards Manager"*. Include the symptom, not the cause. Start a timer (note the time).
4. Coach with the debugging method, not the answer:
   reproduce → read the error / check row counts → find what changed (`git log`, `git diff`, source freshness) → isolate the layer (raw → staging → intermediate → mart → report) → form a hypothesis → test it → fix → **add a test so it can't happen again**.
   Hint ladder: at most 3 hints, each one more specific. Hint 3 names the layer, never the fix.
5. When it's resolved, or after 60 min, reveal the root cause and compare it to his path.
6. Thomas writes the postmortem at `docs/incidents/NNN-<slug>.md`: summary, impact, timeline, root cause, fix, the test added, what he'd do differently. Blameless tone.
7. Log the drill in `docs/incidents/README.md`: number, date, level, fault type, time to resolve, hints used. Update SKILLS_MATRIX "Troubleshooting".
8. Merge the fix (with the new test) through a PR. Delete the incident branch.
9. Offer a `/blog` angle: "Today my pipeline broke on purpose, and here's how I found it."

$ARGUMENTS
