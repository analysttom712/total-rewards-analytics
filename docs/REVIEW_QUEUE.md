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

| Concept | Box | Last seen | Result | Misses | Next due | Where taught |
|---|---|---|---|---|---|---|
| `range(a, b)` stops before `b`; stop − start = count | 1 | 2026-11-24 | ½ | 2 | 2026-11-25 | Day 3 |
| `Closes #N`: exact form (`Closes #12`), goes in the PR body, closes on merge | 1 | 2026-11-24 | ½ | 3 | 2026-11-25 | Day 1–3 |
| `object` dtype = type unknown; `pd.to_datetime` = "Changed Type" | 1 | 2026-11-24 | ✗ | 1 | 2026-11-25 | Day 3 |
| `to_csv(index=False)`: why (no junk index column) | 1 | 2026-11-24 | ½ | 1 | 2026-11-25 | Day 3 |
| `return`: Python needs it, R doesn't | 1 | 2026-11-24 | ✗ | 1 | 2026-11-25 | Day 3 |
| List by position `[0]` vs dict by name `["name"]` | 1 | 2026-11-24 | ✗ | 1 | 2026-11-25 | Day 3 |
| `git switch` (go to) vs `git switch -c` (create) | 1 | 2026-11-23 | ½ | 1 | 2026-11-25 | Day 2 |
| `.gitkeep` = lets Git track an empty folder | 1 | 2026-11-22 | ✗ | 1 | 2026-11-25 | Day 1 |
| Import groups: built-in / pip / my files | 1 | 2026-11-24 | new | 0 | 2026-11-25 | Day 3 |
| `Path(...).mkdir(parents=True, exist_ok=True)` | 1 | 2026-11-24 | new | 0 | 2026-11-25 | Day 3 |
| Store dates as ISO `YYYY-MM-DD`; MM-DD-YYYY is display | 1 | 2026-11-24 | new | 0 | 2026-11-25 | Day 3 |
| Type hints: input inside `()`, output after `->` | 2 | 2026-11-24 | ✓ | 1 | 2026-11-26 | Day 3 |
| Branch vs `main`: commits on a branch don't change `main` | 2 | 2026-11-23 | ✓ | 1 | 2026-11-25 | Day 1–2 |
| Lists count from 0; `[-1]` = last | 2 | 2026-11-23 | ✓ | 0 | 2026-11-25 | Day 2 |
| Seed: same order of random calls → same output | 2 | 2026-11-23 | ✓ | 0 | 2026-11-25 | Day 2 |
| Higher grade → higher pay range (no inversions) | 2 | 2026-11-24 | ✓ | 0 | 2026-11-26 | Day 2 |

## Retired (✓ at box 5)

| Concept | Retired on |
|---|---|
| | |
