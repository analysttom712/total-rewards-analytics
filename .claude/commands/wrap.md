---
description: End today's session (verify, quiz, safety scan, commit, PR, log, blog draft)
---
Wrap up today's session.

1. Run the checks for what changed (`ruff check`, `pytest`, `dbt build`, or open the report). Show the results. Fix only what today's ticket needs.
2. Quiz: 3 questions on today's concept (one tied to a cert objective). Score them.
3. **Public-repo safety scan** (CLAUDE.md 2a): `git status`, `git diff --staged`. Check for secrets, real-looking data, employer or vendor names, local paths with his username, AWS IDs. Flag anything found before committing.
4. Thomas commits with a clear message, pushes, and opens a PR with `gh pr create` that links the issue ("Closes #N"). Review the diff like a senior teammate; Thomas merges.
5. Append to `docs/LEARNING_LOG.md`: date · day number · ticket · concept · what shipped · quiz score · blockers · next ticket.
6. Update `docs/SKILLS_MATRIX.md` ratings that changed (0–4), with a one-line reason. Add an ADR to `docs/DECISIONS.md` if a design choice was made.
7. Run the `/blog` steps to draft today's post.
8. Tell Thomas in two lines what he did today and what's next.

$ARGUMENTS
