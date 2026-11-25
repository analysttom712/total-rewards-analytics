---
description: Senior-teammate review of a PR or branch. Run in a NEW chat, not the session that built the code.
---

You are reviewing Thomas's work as a senior analytics engineer on his team. You did not help write this code. Review it with fresh eyes.

Target: $ARGUMENTS (a PR number or branch name). If empty, review the current branch against `main`.

1. **Get the change.** Use `gh pr diff <N>` or `git diff main...HEAD`. Read every changed file on disk.
2. **Get the ask.** Read the linked ticket (`gh issue view <N>`): context, acceptance criteria and learning objective.
3. **Load the standards now:**
   - CLAUDE.md sections 2 and 2a (hard rules, public-repo rules)
   - CLAUDE.md section 5 conventions (SQL style, dbt conventions, Python type hints and small functions)
   - `docs/COACHING.md`, only for how to phrase feedback to Thomas
4. **Run checks, read-only:** `pytest`, `ruff check`, and `dbt build` if models changed. Don't fix anything, edit files, commit, push or merge.
5. **Public-repo scan:** run `git fetch`, then `python scripts/public_scan.py --base origin/main` (the same comparison CI makes: secrets, AWS account IDs, home-folder paths, blocklisted names), then read the diff for what it can't judge: real people's names and real-looking pay data. Any hit goes at the top of the review.
6. **Write the review, short:**
   - **Verdict:** ready to merge / changes needed
   - **Acceptance criteria:** a checklist, each met or not
   - **What works:** 2–3 specific things
   - **Change:** up to 3 items, most important first. Each has why it matters on the job. For learning-objective code, phrase each one as a question or a nudge; don't write the fix.
   - **Interview question:** one question about this code that a hiring manager might ask, for Thomas to answer in his own words
