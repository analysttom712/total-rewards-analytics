# Today's Lesson Plan

Today plus the next **2 sessions**, always planned ahead. Each day has the goal, the agenda, an in-depth **deep dive**, a **do-it-yourself** path with hidden checkpoint answers, the review items due, resources, and "done when".

**How to use it:** open with **Ctrl+Shift+V** and click a day. If I'm not around, follow the *Do it yourself* section step by step: try each checkpoint before opening its answer. `/standup` rolls this forward every session; `/wrap` marks what got done.

---

<details>
<summary><b>📍 TODAY · Mon Nov 24 · Day 3 review: deep review before #9</b></summary>

<details>
<summary>🎯 Goal and why it matters</summary>

Slow down and consolidate everything from Days 1–3 so Issue #9 (testing) feels solid. Testing is reading code carefully and predicting what it does, so every concept here gets used again tomorrow.

</details>

<details>
<summary>🗓 Agenda</summary>

| Block | Time | Status |
|---|---|---|
| 1. Where am I typing? + Python REPL + quotes | 10 min | ✅ done |
| 2. The Git pipeline | 20 min | ▶ in progress |
| 3. Python building blocks: lists vs dicts | 20 min | |
| 4. Functions and loops | 20 min | |
| 5. pandas and CSV | 15 min | |
| 6. `/quiz` on everything | 10 min | |

</details>

<details>
<summary>📚 Block 2 deep dive: the Git pipeline</summary>

Git tracks every file in one of **four states**. `git status` names them for you:

| `git status` heading | State | What it means | Accounting version |
|---|---|---|---|
| *Untracked files* | untracked | A new file Git has **never** recorded. It won't be in any commit until you `git add` it. | A draft that isn't in the ledger at all |
| *Changes not staged for commit* | modified | A tracked file you changed and saved, but haven't picked for the next commit. | An edited draft entry |
| *Changes to be committed* | staged | Picked with `git add`. Exactly these go into the next commit. | Entries selected for this batch |
| *(not listed)* | committed / unchanged | Matches the last commit. Nothing to do. | Posted |

**Why staging exists:** it lets one commit hold one idea. You might change 5 files but only want 2 of them in "Add job catalog". Staging is choosing the batch.

**The same file can appear twice** (staged *and* modified): you staged it, then edited it again. The staged copy is the old snapshot; `git add` again to update it.

**Undo at each stage:**

| Want to… | Command |
|---|---|
| Unstage (keep the edits) | `git restore --staged <file>` |
| Throw away unsaved-to-Git edits | `git restore <file>` ⚠️ can't be undone |
| Fix the last commit message (not pushed yet) | `git commit --amend -m "..."` |

</details>

<details>
<summary>🛠 Block 2: do it yourself</summary>

1. Run `git status`. For each file, name its state using the table above.
   <details><summary>Checkpoint answer</summary>

   On the `learning-loop` branch: files under *Changes not staged* (e.g. `CLAUDE.md`, `.claude/commands/*.md`, `docs/CHEATSHEET.md`) are **modified**: tracked, edited, not yet picked. Files under *Untracked* (`docs/COACHING.md`, `docs/GLOSSARY.md`, `docs/RESOURCES.md`, `docs/REVIEW_QUEUE.md`, `docs/TODAYS_LESSON_PLAN.md`) are **new**: Git has never seen them.
   </details>
2. Stage one file: `git add docs/GLOSSARY.md`. Run `git status` again. Where did it move?
   <details><summary>Checkpoint answer</summary>

   From *Untracked* to *Changes to be committed*. It's now in the batch.
   </details>
3. Unstage it: `git restore --staged docs/GLOSSARY.md`. Run `git status`. Where is it now? Did you lose any content?
   <details><summary>Checkpoint answer</summary>

   Back to *Untracked*. Nothing is lost: `--staged` only takes it out of the batch; the file is untouched.
   </details>
4. Explain in one sentence: why does `Closes #N` only close the issue at merge, not at push?
   <details><summary>Checkpoint answer</summary>

   Pushing only uploads commits to your **branch** on GitHub; the issue closes when the work reaches the default branch (`main`), which only happens when the PR merges.
   </details>

</details>

<details>
<summary>📚 Block 3 deep dive: lists vs dicts</summary>

| | List | Dict |
|---|---|---|
| Brackets | `[ ]` | `{ }` to make, `[ ]` to look up |
| Look up by | **position**: `jobs[0]` (first), `jobs[-1]` (last) | **key name**: `row["grade"]` |
| Order | Ordered: position is the meaning | Keys are labels; order is just the order you typed |
| Missing item | `IndexError: list index out of range` | `KeyError: 'grade'` |
| Like | A column of values / rows in a table | One row with named columns / a record |

**A list of dicts is a table.** Two lookups, always in this order: **row first, then column**: `JOBS[2]["job_title"]` → row 2 (third row), column `job_title`. Asking the whole list for a column name (`JOBS["job_title"]`) is a `TypeError`, because a list has positions, not names.

**Why `0` is first:** a position is an **offset**: "how many steps from the start". The first item is 0 steps away.

</details>

<details>
<summary>🛠 Block 3: do it yourself (in the REPL: type <code>python</code>)</summary>

Type this in (one line at a time, or paste the block):

```python
jobs = [
    {"job_code": 1, "job_title": "Compensation Analyst", "grade": 4},
    {"job_code": 3, "job_title": "Payroll Coordinator", "grade": 1},
    {"job_code": 5, "job_title": "Total Rewards Manager", "grade": 5},
]
```

Predict each answer **before** pressing Enter:

1. `len(jobs)`
2. `jobs[1]["job_title"]`
3. `jobs[-1]["grade"]`
4. `jobs[3]`
5. `jobs["grade"]`
6. `jobs[0]["salary"]`

<details><summary>Checkpoint answers</summary>

1. `3`
2. `'Payroll Coordinator'` (position 1 = second row)
3. `5` (last row's grade)
4. `IndexError`: there are only positions 0, 1, 2
5. `TypeError`: a list needs a position, not a column name
6. `KeyError: 'salary'`: that row has no `salary` key. New error type: it's the dict version of `IndexError`.
</details>

</details>

<details>
<summary>📚 Block 4 deep dive: functions and loops</summary>

**A function call is a substitution.** `annual_premium(480)` means: run the recipe with `monthly` = 480, and the whole call is replaced by whatever `return` hands back. That's why you can write `total = annual_premium(480) + annual_premium(650)`.

**Parameter vs argument:** `monthly` (in the `def` line) is the **parameter**, the placeholder. `480` (in the call) is the **argument**, the real value. Power Query: the function's input name vs the value in the row you invoke it on.

**`return` vs `print`:** `print` *shows* a value on screen and hands back nothing (`None`). `return` *hands the value back* so other code can use it. A function that prints but doesn't return is like a report that shows a number you can't reference in another measure.

**`range(start, stop)`** counts from `start` up to but **not including** `stop`. Count = `stop − start`. Why exclusive? So ranges join without overlap: `range(0, 10)` + `range(10, 20)` covers 0–19 exactly once, like back-to-back pay periods where each period ends where the next begins.

**A loop that builds a list** always has the same three lines: empty list → `for` → `.append(...)`.

</details>

<details>
<summary>🛠 Block 4: do it yourself (REPL)</summary>

1. Write and call it:
   ```python
   def annual_premium(monthly: int) -> int:
       return monthly * 12
   ```
   (In the REPL, press Enter on an empty `...` line to finish the function.) Then predict and run: `annual_premium(480) + annual_premium(650)`.
2. Now write `def shout(monthly: int): print(monthly * 12)` (no return). Predict what `x = shout(480)` then `x` shows.
3. Predict, then run `list(range(3, 7))`. (`list(...)` makes the range visible.) How many numbers?
4. Write a loop that builds `premiums` = annual premiums for `[650, 480, 75]`.

<details><summary>Checkpoint answers</summary>

1. `5760 + 7800 = 13560`
2. `shout(480)` **prints** 5760, but `x` is `None` (nothing was returned). Typing `x` shows nothing.
3. `[3, 4, 5, 6]`: 4 numbers (7 − 3).
4. ```python
   premiums = []
   for monthly in [650, 480, 75]:
       premiums.append(annual_premium(monthly))
   premiums   # [7800, 5760, 900]
   ```
</details>

</details>

<details>
<summary>📚 Block 5 deep dive: pandas and CSV</summary>

**DataFrame = list of dicts with superpowers:** typed columns, one-line summaries, and file output. Each dict → a row, each key → a column, plus an **index** (row labels, not data).

**dtypes are the column types.** `int64`, `float64`, `str`, `datetime64`, `bool`, and `object` (= "Python things pandas didn't type", Power Query's ABC123 Any). When a column comes in as `object` but should be a date or number, add a "Changed Type" step (`pd.to_datetime`, `pd.to_numeric`).

**CSV is plain text.** It has no types: every value is just characters separated by commas. Types come back when a tool reads it (Excel guesses, Power BI detects, pandas infers). That's why dates go out as ISO `YYYY-MM-DD`: every reader guesses them correctly.

**`index=False`**: without it, the index (0, 1, 2…) is written as an unnamed first column.

</details>

<details>
<summary>🛠 Block 5: do it yourself (REPL)</summary>

```python
import pandas as pd
df = pd.DataFrame([
    {"plan_code": "MED-PPO", "monthly_premium": 650, "effective": "2026-01-01"},
    {"plan_code": "DEN-STD", "monthly_premium": 75, "effective": "2026-01-01"},
])
```

1. Predict `df.shape`.
2. Predict `df.dtypes` for `effective`. Then fix it with a "Changed Type" step and check again.
3. Add an annual column: `df["annual_premium"] = df["monthly_premium"] * 12`. Predict the new `df.shape`.
4. Run `print(df.to_csv(index=False))` (prints the CSV text instead of saving a file). Then run it without `index=False`. What changed?

<details><summary>Checkpoint answers</summary>

1. `(2, 3)`
2. `str` (text). Fix: `df["effective"] = pd.to_datetime(df["effective"])` → `datetime64`.
3. `(2, 4)`: a new column. Multiplying a whole column at once is like a Power Query custom column: no loop needed.
4. Without `index=False`, every line starts with `0,` or `1,` and the header starts with an empty field (`,plan_code,...`): the junk column.
</details>

</details>

<details>
<summary>🔁 Review items covered today</summary>

Branch vs main · `git switch` vs `-c` · `.gitkeep` · `Closes #N` · lists from 0 · list vs dict lookup · `return` · type hints · `range` stop · `object` dtype · `index=False` · ISO dates. Results go into `docs/REVIEW_QUEUE.md` after `/quiz`.

</details>

<details>
<summary>🔗 Resources</summary>

- [GH-900: GitHub Foundations path](https://learn.microsoft.com/en-us/training/paths/github-foundations/): *Introduction to Git* module (matches Block 2).
- [Pro Git, 2.2 Recording changes](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository): the four file states, in depth.
- [Python tutorial: lists](https://docs.python.org/3/tutorial/introduction.html#lists) · [dicts](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
- [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)

</details>

<details>
<summary>✅ Done when</summary>

- [ ] You can name a file's Git state from `git status` without the table
- [ ] Block 3–5 checkpoints answered (right or wrong, you tried first)
- [ ] `/quiz` run and the review queue updated
- [ ] Learning-loop PR shipped

</details>

</details>

---

<details>
<summary><b>NEXT · Tue Nov 25 · Day 4 · Issue #9 part 1: make the code testable + your first test</b></summary>

<details>
<summary>🎯 Goal and why it matters</summary>

The manager's ask: *proof, not a promise*, that the same seed gives the same employees. A **test** is that proof, written as code that runs every time.

This is your manual reconciliation checks, automated. In Phase 3 the same idea becomes dbt tests; in Phase 5, CI runs them on every PR. Employers ask about testing in every analytics engineering interview.

</details>

<details>
<summary>🗓 Agenda</summary>

| Block | Time | What |
|---|---|---|
| Standup + review | 10 min | 1 due review question |
| Lesson A | 15 min | What a test is; `assert`; how pytest finds tests |
| Build A | 30 min | Make the script importable: `build_employees()` + `main()` + the main guard |
| Lesson B | 10 min | Reading pytest output (pass, fail) |
| Build B | 30 min | First test: same seed → same employees |
| Check + ship | 20 min | run, `/quiz`, commit (PR waits for part 2) |
| Cert study | 15 min | GH-900: *Introduction to GitHub* |

</details>

<details>
<summary>📚 Deep dive: tests, assert, and import side effects</summary>

**`assert` is a tie-out check.** `assert total_payroll == gl_total` means "this must be true; if not, stop and report". If it's true, nothing happens. If it's false, the test **fails** and shows both values. Exactly like a recon that either ties or shows the variance.

**How pytest finds tests (naming is the contract):**

| Rule | Example |
|---|---|
| Files named `test_*.py` | `tests/test_generator.py` |
| Functions named `test_*` | `def test_same_seed_same_employees():` |
| Run from the repo root | `python -m pytest` |

**Reading the output:** each test prints `.` (pass) or `F` (fail). A failure shows the `assert` line and the actual values on each side. Read it bottom-up, like any error.

**The problem we have to fix first: import side effects.** Right now `hello_employee.py` *does everything the moment it's loaded*: builds employees, prints, writes the CSV. A test has to **import** the file to use `make_employee`, and that import would run the whole script. That's a side effect: loading the code changes things.

**The fix (a standard Python pattern):**
1. Put the "build 25 employees" loop inside a function, `build_employees(count: int) -> list`.
2. Put the "print and write the CSV" part inside a function, `main()`.
3. At the bottom:
   ```python
   if __name__ == "__main__":
       main()
   ```

**What `__name__` is:** Python sets a hidden variable called `__name__` in every file. When you **run** the file (`python generator/hello_employee.py`), it's `"__main__"`. When another file **imports** it, it's the file's name, `"hello_employee"`. So the guard means "only run `main()` when this file is run directly, not when it's imported". Power BI version: a query that's a **function** (only runs when invoked) vs a query that **loads to the model** (runs on every refresh).

**One more catch: the seed.** `Faker.seed(42)` at the top of the file runs **once**, at import. A test that calls `build_employees(25)` twice would get *different* people the second time, because the random sequence has moved on. So the seed moves **inside** `build_employees`: every call starts the sequence from 42. That's what makes "same seed → same output" true *within one run*.

**Scaffolding I'll add (not a learning objective):** a small `pyproject.toml` that tells pytest where the generator code lives.

</details>

<details>
<summary>🛠 Do it yourself</summary>

1. Branch: `git switch -c 9-first-pytest`.
2. In `hello_employee.py`, wrap the loop in `def build_employees(count: int) -> list:` that returns `employees`. Move `Faker.seed(42)` to the first line inside it.
   <details><summary>Hint (nudge)</summary>

   Same pattern as `make_employee`: `def` line, docstring, indented body, `return` at the end. The loop's `range` stop becomes `100001 + count`.
   </details>
3. Wrap the DataFrame, prints and CSV lines in `def main() -> None:`. Its first line calls `build_employees(25)`.
4. Add the main guard at the bottom. Run the script: the output must be **identical** to before.
   <details><summary>Checkpoint</summary>

   Same 5 rows in `head()`, `(25, 7)`, same dtypes, and the CSV still written. If nothing prints, the guard or the `main()` call is missing.
   </details>
5. Create `tests/test_generator.py` with one test:
   ```python
   from hello_employee import build_employees


   def test_same_seed_same_employees():
       first = build_employees(25)
       second = build_employees(25)
       assert first == second
   ```
   Run `python -m pytest`. Expected: `1 passed`.
6. Break it on purpose: temporarily move `Faker.seed(42)` back outside the function. Run pytest. Read the failure. Then put it back.
   <details><summary>What you should see</summary>

   `F` and `AssertionError`, with the two lists shown as different. That proves the test actually catches the bug it's meant to catch: a test that can't fail is worth nothing.
   </details>

</details>

<details>
<summary>🔁 Review items due</summary>

From `docs/REVIEW_QUEUE.md`: the box-1 items (oldest/most-missed first), e.g. `range` stop, `Closes #N`, `object` dtype, `return`.

</details>

<details>
<summary>🔗 Resources</summary>

- [pytest: Get started](https://docs.pytest.org/en/stable/getting-started.html): first test, reading output.
- [Python docs: `__main__`](https://docs.python.org/3/library/__main__.html): the main guard, from the source.
- [GH-900 path](https://learn.microsoft.com/en-us/training/paths/github-foundations/): *Introduction to GitHub*.

</details>

<details>
<summary>✅ Done when</summary>

- [ ] Script output identical to before the refactor
- [ ] `python -m pytest` → `1 passed`
- [ ] You've seen it fail on purpose and read the failure
- [ ] Committed on `9-first-pytest` (PR after part 2)

</details>

</details>

<details>
<summary><b>NEXT +1 · Wed Nov 26 · Day 5 · Issue #9 part 2: more tests + fix the hire-date drift</b></summary>

<details>
<summary>🎯 Goal and why it matters</summary>

Finish #9: prove every employee ID is unique and every salary sits inside its pay range, then fix the bug you found on Day 3 (hire dates shift by a day because `end_date="today"` moves). After this, the generator's core promises are guarded by tests.

</details>

<details>
<summary>🗓 Agenda</summary>

| Block | Time | What |
|---|---|---|
| Standup + review | 10 min | 1 due review question |
| Lesson | 15 min | Sets (distinct values); as-of dates |
| Build | 60 min | 2 tests + the drift fix + a test that would have caught it |
| Check + ship | 20 min | pytest, ruff, `/quiz`, PR with `Closes #9` |
| Cert study | 15 min | GH-900: *Working with GitHub repositories* |

</details>

<details>
<summary>📚 Deep dive: sets, as-of dates, and tests that catch drift</summary>

**A `set` keeps only distinct values.** `set([1, 2, 2, 3])` → `{1, 2, 3}`. So "all IDs unique" is: `len(set(ids)) == len(ids)`. If any ID repeats, the set is shorter. Power BI version: `DISTINCTCOUNT(id) = COUNTROWS(table)`; Power Query: row count before and after Remove Duplicates.

**Building a list of one column from a list of dicts** (list comprehension, a one-line loop):
```python
ids = [e["employee_id"] for e in employees]
```
Read it as: "for each employee `e`, take its `employee_id`". Same as the 3-line append loop, written compactly. Like selecting one column.

**The salary-in-range test** needs each employee's job range. Look it up by `job_code` in `JOBS`, then:
```python
assert job["salary_min"] <= e["salary"] <= job["salary_max"]
```
`a <= b <= c` is a **chained comparison**: true only if b is between a and c (inclusive).

**The hire-date drift is an "as-of" problem.** `end_date="today"` means the data depends on *when* you ran it. Real HCM extracts and payroll reports always run **as of** a fixed date (period end), so results tie out no matter when you rerun them. The fix is a constant at the top of the file:
```python
from datetime import date

AS_OF = date(2026, 11, 1)
```
…and `end_date=AS_OF`. ALL_CAPS = a constant (a value set once, not changed). This is the first step toward effective dating, which is central to the whole platform.

**A test that would have caught it:** a **golden value** test: pin one known output. `build_employees(1)[0]["hire_date"]` must equal a specific date. If anything makes the output drift (a moving date, a changed call order), this fails.

</details>

<details>
<summary>🛠 Do it yourself</summary>

1. Test: unique IDs. Build 25, make the `ids` list, assert the set length equals the list length.
2. Test: salaries in range. For each employee, find the job in `JOBS` with the same `job_code`, assert min ≤ salary ≤ max.
   <details><summary>Hint (bigger)</summary>

   ```python
   for e in employees:
       job = next(j for j in JOBS if j["job_code"] == e["job_code"])
       assert ...
   ```
   `next(...)` takes the first match, like a lookup.
   </details>
3. Fix the drift: add `AS_OF`, use it as `end_date`. Rerun the script: hire dates may shift once (that's expected), then stay fixed forever.
4. Golden-value test: assert the first employee's hire date equals the date the script now prints for Angel Hill (or whoever is first).
5. Break one test on purpose (change an expected value), read the failure, note what it said for the PR description, then fix it.
6. `python -m pytest` → `4 passed`. Ship: PR body starts with `Closes #9`.

</details>

<details>
<summary>🔗 Resources</summary>

- [pytest: assertions](https://docs.pytest.org/en/stable/how-to/assert.html)
- [Python tutorial: sets](https://docs.python.org/3/tutorial/datastructures.html#sets) · [list comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- [datetime.date](https://docs.python.org/3/library/datetime.html#date-objects)

</details>

<details>
<summary>✅ Done when</summary>

- [ ] 4 tests pass; one was seen failing on purpose
- [ ] Hire dates no longer change from day to day
- [ ] PR merged with `Closes #9`
- [ ] Next up: #14 (package) or #13 (org structure + first `merge`)

</details>

</details>
