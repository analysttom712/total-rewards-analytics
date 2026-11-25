# Architecture Decisions

Short records: decision · options considered · why. These are interview talking points.

## ADR-001: Job catalog starts as a Python constant (2026-11-23)
- **Decision:** the job catalog (job code, title, grade, salary min/max) is a list of dicts in `generator/job_catalog.py`.
- **Options:** Python constant; a CSV the generator reads; a dbt seed.
- **Why:** five rows, read only by the generator, and it teaches lists and dicts. When the catalog grows and dbt needs the ranges (the `comp_grade_ranges` raw table, compa-ratio marts), the generator will write it out as a raw table, the way a real HCM extract would deliver it.

## ADR-002: Synthetic SSNs start with 000 or 666 (2026-11-25)
- **Decision:** every SSN the generator produces starts with `000` or `666`. The public-repo scan allows SSN-shaped values (hyphenated or 9 digits) only with those prefixes.
- **Options:** no SSNs at all; Faker's `ssn()`; reserved prefixes.
- **Why:** carrier files and HR extracts are keyed on SSN, so the reconciliation work needs them. Faker's `ssn()` can produce numbers that look valid and may belong to a real person. `000` and `666` are area numbers the SSA never issues, so a synthetic SSN can never be a real one, and the scan can tell synthetic from suspicious with a two-prefix rule.

## ADR-003: Enforce the most important rules with tools, not wording (2026-11-25)
- **Decision:** the rules whose failure can't be undone on a public repo (no secrets, no employer or vendor names, no real-looking identifiers, nothing merged to `main` without review) are enforced by tools in layers. `CLAUDE.md` still states them, but no longer carries them alone.
- **Options:** wording only in `CLAUDE.md`; a single pre-commit hook; layered tools (chosen).
- **Why:** an instruction can be misread or forgotten, and Git history on a public repo is permanent. Each layer below covers a gap in the one before it.

| Layer | Where | Enforces | Known gap |
|---|---|---|---|
| Claude Code deny rules | `.claude/settings.json` | Claude can't read or edit `.env` files, `~/.dbt/` or `~/.aws/`; can't run `gh pr merge`, force-push, push to `main` by name, `git reset --hard`, `git clean`, discard uncommitted work, delete a branch with `-D`, or commit with `--no-verify` / `-n` | Rules match the command text Claude writes, so they are a guardrail, not a security boundary: a bare `git push` while on `main` never says "main". A script that opens a file itself is not covered by the read rules |
| Posting deny rules | Thomas's user settings, not this repo | Claude can't call the posting tools of his social, chat and scheduling connectors | Rules name each connector by its ID: a re-added connector needs its rules re-added. The browser isn't covered; that stays a wording rule (Claude drafts, Thomas posts) |
| Git pre-commit hook | `.githooks/pre-commit` (one-time `git config core.hooksPath .githooks`) | Every commit by anyone runs `scripts/public_scan.py`; a hit or a scan error blocks the commit | Skipped by `git commit --no-verify`. `ruff check` only reports here, so work in progress can always be committed to a branch when a session has to stop |
| Claude Code hooks | `.claude/settings.json` + `scripts/claude_hooks.py` | Before any commit Claude runs: the scan, failing closed (exit 2 on a hit or an error). After file edits: `ruff check` on the file, reported, never auto-fixed. At stop: `pytest`, reported | Windows-only paths (`.venv/Scripts/python.exe`). When one command stages a file and commits it, this scan runs before the file is staged; the git hook still scans it |
| CI | `.github/workflows/checks.yml` | Every PR and every push to `main`: the scan (with the blocklist from the `SCAN_BLOCKLIST` secret, failing closed if it's missing), `ruff check`, `pytest`. Lint errors and failing tests block the merge here | Fork PRs don't receive secrets, so names aren't checked on them; every other rule is |
| Branch protection on `main` | GitHub repo settings | A PR is required, the `checks` job must pass, force pushes are blocked | Set up by Thomas after the first CI run. This is the real enforcement layer: GitHub applies it no matter which command, tool or person pushes |

- **Why tests report instead of block (stop hook, pre-commit):** in this repo a red test is often intentional. Test-first exercises give Thomas a failing test to solve, and blocking on it would push Claude to write his learning code for him. So local tools report test and lint results, and only CI and branch protection block, at the point where work is claimed to be finished (the merge).
- **Why the scan fails closed but lint doesn't:** a leaked name or key can't be taken back; a lint error can be fixed in the next commit.
- **Emergency bypass:** Thomas can still run `git commit --no-verify` himself. Claude can't: the deny rules block it, and CI and branch protection still check whatever reaches GitHub.
- **Blocklist handling:** the names are the secret. They live only in the gitignored `.scan-blocklist.local.txt` and the `SCAN_BLOCKLIST` secret, and the scanner never prints any part of a matched word, because CI logs on a public repo are public.
- **Still wording only:** real people's names and real-looking pay data that match no pattern, screenshots, the tone of blog posts, and "he learns by doing". A script can't judge these, so `CLAUDE.md` section 2a and `/wrap` keep the by-eye check.

## ADR-004: The hub's progress file saves one at a time, behind a lock (2026-11-25)
- **Decision:** every save to `hub/progress.local.json` (answer, self-mark, task tick) holds one shared `threading.Lock` for the whole load → change → write. A write the disk refuses returns a JSON error instead of a dropped connection. Shipped in PR #33.
- **Options:** a lock around each save (chosen); a server that handles one request at a time; SQLite instead of a JSON file.
- **Why:** the review of PR #30 found that two saves at once overwrote each other. In a test of 20 saves fired together, only 1–2 were kept, and the rest failed with `PermissionError`. A lock is a few lines and keeps the file readable by hand, which `/standup` relies on. It only covers one running copy of the hub, though. If a second writer arrives (two hub copies, or `/wrap` writing while the hub runs in slice 3), revisit SQLite, which handles locking across processes.
- **Open, Thomas's call:** a knowledge check's ID is a hash of its Concept wording, so rewording a concept in `REVIEW_QUEUE.md` drops its saved answer from the lesson page. Options: add a stable ID column to the queue, or accept the risk and say so in `docs/site/BRIEF.md`.
