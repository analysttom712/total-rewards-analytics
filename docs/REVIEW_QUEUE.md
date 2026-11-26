# Review Queue

Spaced repetition for every concept I've been taught. `/standup` and `/quiz` ask what's **due**; `/wrap` and `/quiz` move items between boxes.

**How the boxes work**

| Box | Review again in | Move up when | Move down when |
|---|---|---|---|
| 1 | next session | ✓ → box 2 | ✗ or ½ → stays in box 1 |
| 2 | 2 days | ✓ → box 3 | ✗ or ½ → box 1 |
| 3 | 4 days | ✓ → box 4 | ✗ or ½ → box 1 |
| 4 | 7 days | ✓ → box 5 | ✗ or ½ → box 1 |
| 5 | 14 days | ✓ → **retired** (move to the bottom table) | ✗ or ½ → box 1 |

Rules: ask due items oldest-first, misses before new items, at most 3 review questions per session outside `/quiz`. A concept that hits ✗ three times gets its own mini-ticket.

## Active

| Concept | Box | Last seen | Result | Misses | Next due | Where taught | Question |
|---|---|---|---|---|---|---|---|
| `range(a, b)` stops before `b`; stop − start = count | 2 | 2026-11-24 | ✓ | 2 | 2026-11-26 | Day 3 | Predict the output: what does `list(range(5, 8))` return, and how many items is that? |
| `Closes #N`: exact form (`Closes #12`, nothing between keyword and `#N`), goes in the PR body, closes on merge | 1 | 2026-11-26 | ½ | 4 | 2026-11-27 | Day 1–3 | Does `fixes issue #19` in a PR body close #19 on merge? Write the line that does. |
| `object` / `str` dtype (text, pandas 3 says `str`); `pd.to_datetime` = "Changed Type" | 2 | 2026-11-24 | ✓ | 1 | 2026-11-26 | Day 3 | |
| `to_csv(index=False)`: why (no junk index column) | 2 | 2026-11-24 | ✓ | 1 | 2026-11-26 | Day 3 | |
| `return`: Python needs it, R doesn't; `print` shows, `return` hands back (else `None`) | 1 | 2026-11-25 | ½ | 4 | 2026-11-26 | Day 3 + review | Predict the output: a function's only line is `print(5)`. You run `x = f()`. What shows on screen, and what is in `x`? |
| List by position `[0]` vs dict by name `["name"]` (position ≠ value inside) | 1 | 2026-11-26 | ✗ | 2 | 2026-11-27 | Day 3 + review | `employee = {"salary": 104572}`; what does `employee[0]` raise, and how do you get the salary? |
| `git switch` (go to) vs `git switch -c` (create) | 2 | 2026-11-24 | ✓ | 1 | 2026-11-26 | Day 2 | |
| `.gitkeep` = lets Git track an empty folder | 2 | 2026-11-24 | ✓ | 1 | 2026-11-26 | Day 1 | |
| Import groups: built-in / pip / my files | 1 | 2026-11-24 | new | 0 | 2026-11-25 | Day 3 | |
| `Path(...).mkdir(parents=True, exist_ok=True)` | 1 | 2026-11-24 | new | 0 | 2026-11-25 | Day 3 | |
| Store dates as ISO `YYYY-MM-DD`; MM-DD-YYYY is display | 1 | 2026-11-24 | new | 0 | 2026-11-25 | Day 3 | |
| `git add` is a snapshot: a file can be staged **and** modified at once | 1 | 2026-11-24 | ½ | 1 | 2026-11-25 | Day 3 review | |
| `git restore --staged` (unstage, keep edits) vs `git restore` (discard edits) | 1 | 2026-11-24 | new | 0 | 2026-11-25 | Day 3 review | |
| Lookup errors: `IndexError` (position) / `KeyError` (key) / `TypeError` (wrong kind) | 1 | 2026-11-26 | ✗ | 1 | 2026-11-27 | Day 3 review | |
| Apply a transform once (`annual_premium(monthly)`, not `(monthly * 12)`); call with `()` | 1 | 2026-11-26 | ½ | 2 | 2026-11-27 | Day 3 review | |
| Type hints: input inside `()`, output after `->` | 2 | 2026-11-24 | ✓ | 1 | 2026-11-26 | Day 3 | In `def make_employee(employee_id: int) -> dict:`, which part describes the input and which describes the output? |
| Branch vs `main`: commits on a branch don't change `main` | 2 | 2026-11-23 | ✓ | 1 | 2026-11-25 | Day 1–2 | |
| Lists count from 0; `[-1]` = last | 3 | 2026-11-24 | ✓ | 0 | 2026-11-28 | Day 2 | |
| Seed: same order of random calls → same output | 2 | 2026-11-23 | ✓ | 0 | 2026-11-25 | Day 2 | |
| Higher grade → higher pay range (no inversions) | 2 | 2026-11-24 | ✓ | 0 | 2026-11-26 | Day 2 | |
| Lost update: two threads read the same old file, the last write wins; a lock makes read-change-write take turns | 2 | 2026-11-25 | ✓ | 0 | 2026-11-27 | Review 1 | |
| Squash merge = one new commit on `main`; `git branch -d` refuses (it checks history), so compare contents, then `-D` | 2 | 2026-11-25 | ✓ | 0 | 2026-11-27 | Review 1 | |
| Left join: an as-of rule in `where` drops unmatched rows (acts like inner); in `on` keeps them with NULLs | 2 | 2026-11-25 | ✓ | 0 | 2026-11-27 | Review 1 | |
| Golden values: type the expected answer in by hand, don't recompute the formula in the test | 1 | 2026-11-25 | new | 0 | 2026-11-26 | Review 1 | |
| A key built from text that gets edited (a hash of the wording) breaks the join when the text changes; use a stable ID | 1 | 2026-11-25 | new | 0 | 2026-11-26 | Review 1 | |
| A fix found after a PR merged goes on a new branch from `main` and its own PR | 1 | 2026-11-25 | new | 0 | 2026-11-26 | Review 1 | |
| `len(set(ids)) == len(ids)`: uniqueness check (DAX `DISTINCTCOUNT = COUNTROWS`) | 2 | 2026-11-26 | ✓ | 0 | 2026-11-28 | Day 5 | |
| Chained comparison `a <= b <= c` = SQL `BETWEEN` (ends included) | 1 | 2026-11-25 | new | 0 | 2026-11-27 | Day 5 | |
| False pass: an `assert` inside an `if` that never matches runs 0 times, so "passed" checked nobody | 1 | 2026-11-26 | ½ | 1 | 2026-11-27 | Day 5 | A salary test joins on the wrong key and reports `1 passed`. How many salaries did it check, and what should you ask of any perfect result? |
| Break it on purpose: plant the bug in the code, not in the rule it's checked against (else both move and the test can't fail) | 1 | 2026-11-26 | new | 0 | 2026-11-27 | Day 5 | |
| `git commit --amend`: replaces the last commit with a new ID; only before pushing | 1 | 2026-11-26 | new | 0 | 2026-11-27 | Day 5 | |
| Unsaved editor changes (white dot) aren't on disk; Git and pytest only see saved files | 1 | 2026-11-26 | new | 0 | 2026-11-27 | Day 5 | |
| pytest finds `test_*.py` files and `test_*` functions; `assert` = the check | 1 | 2026-11-25 | new | 0 | 2026-11-27 | Day 4 | |
| Main guard `if __name__ == "__main__":` stops code running on import | 1 | 2026-11-25 | new | 0 | 2026-11-27 | Day 4 | |

## Retired (✓ at box 5)

| Concept | Retired on |
|---|---|
| | |
