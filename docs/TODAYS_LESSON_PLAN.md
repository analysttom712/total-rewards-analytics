# Today's Lesson Plan

Today plus the next **2 sessions**, always planned ahead. Each day has the goal, the agenda, an in-depth **deep dive**, a **do-it-yourself** path with hidden checkpoint answers, the review items due, resources, and "done when".

**How to use it:** open with **Ctrl+Shift+V** and click a day. If I'm not around, follow the *Do it yourself* section step by step: try each checkpoint before opening its answer. `/standup` rolls this forward every session; `/wrap` marks what got done.

---

<details>
<summary><b>📍 TODAY · Mon Nov 24 · Day 4 · Issue #9 part 1: make the code testable + your first test</b></summary>

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

0. Warm-up: `ruff format generator/job_catalog.py` (it's been unformatted since Day 2), then `ruff format --check generator` → all formatted.
1. Branch: `git switch -c 9-first-pytest`. **Before typing any code, check the tab name says `hello_employee.py`**, and press Esc on any grey autocomplete text.
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

From `docs/REVIEW_QUEUE.md` (box 1): `return` vs `print` (2 misses), apply ×12 once, `git add` is a snapshot, list position vs dict key, `git restore --staged` vs `git restore`, lookup errors, import groups, `mkdir`, ISO dates. Today's test uses `return` directly: `build_employees` must **return** the list or the test compares `None == None`.

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
<summary><b>NEXT · Tue Nov 25 · Day 5 · Issue #9 part 2: more tests + fix the hire-date drift</b></summary>

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

---

<details>
<summary><b>NEXT +1 · Wed Nov 26 · Day 6 · Issue #14: make the generator a package (<code>python -m generator</code>)</b></summary>

<details>
<summary>🎯 Goal and why it matters</summary>

The manager's ask: *one command that builds every file, from anywhere in the repo.* Right now the generator is a script called `hello_employee.py`. After today it's a **package** you run with `python -m generator`, the way real data tools are run.

This is a **refactor**: the structure changes, the output doesn't. Proving "the output is identical" is a skill reviewers look for in every refactor PR, and your tests from #9 do half the proving for you.

</details>

<details>
<summary>🗓 Agenda</summary>

| Block | Time | What |
|---|---|---|
| Standup + review | 10 min | 1 due review question |
| Lesson | 20 min | Module vs package; `__init__.py`, `__main__.py`, `python -m`; package imports |
| Build | 60 min | Move code into `generator/employees.py`, add `__main__.py`, update imports and tests |
| Check + ship | 20 min | Output identical, pytest, ruff, `/quiz`, PR with `Closes #14` |
| Cert study | 15 min | GH-900: *Introduction to GitHub* (pull requests and code review) |

</details>

<details>
<summary>📚 Deep dive: modules, packages and <code>python -m</code></summary>

| Term | What it is | Power BI version |
|---|---|---|
| **module** | One `.py` file you can import (`job_catalog.py`) | One query |
| **package** | A folder of modules with an `__init__.py` in it (`generator/`) | A query group |
| **`__init__.py`** | Marks the folder as a package. Can be empty. | The group's folder icon |
| **`__main__.py`** | What runs when you type `python -m generator` | The query that loads to the model |
| **`python -m generator`** | "Run the package named `generator`" (`-m` = **module mode**) | Refresh the whole model, not one query |

**Why `-m` works from the repo root:** Python looks for `generator` in the folder you're standing in. So `cd` to the repo root once, and every command works the same way. That's why the manager's ask says "from anywhere *in the repo*": one standard place to stand.

**Package imports name the package.** Inside a package, imports start from the package name:

```text
before:  from job_catalog import JOBS
after:   from generator.job_catalog import JOBS
```

Like a fully qualified table name in SQL (`schema.table`): no guessing which `JOBS` you mean.

**Renaming a file in Git: `git mv`.** `git mv generator/hello_employee.py generator/employees.py` moves the file *and* stages the rename, so its history follows it. Like renaming a query instead of deleting it and building a new one.

**How to prove a refactor didn't change anything:** run the old version and the new version and compare the CSVs. A **hash** is a fingerprint of a file's exact bytes. Same hash = identical file, to the last comma.

```powershell
Get-FileHash data/raw/employees.csv
```

Run it before and after: the `Hash` value must match. Payroll version: the register total ties before and after a system change.

</details>

<details>
<summary>🛠 Do it yourself</summary>

0. From `main` after #9 is merged: `git switch -c 14-generator-package`.
1. Record the fingerprint *before* changing anything: `python generator/hello_employee.py`, then `Get-FileHash data/raw/employees.csv`. Copy the hash into a note.
2. Rename the module: `git mv generator/hello_employee.py generator/employees.py`.
3. Create `generator/__init__.py` (empty is fine; a one-line docstring is nicer).
4. Create `generator/__main__.py` that imports `main` from `generator.employees` and calls it.
   <details><summary>Hint (nudge)</summary>

   Two lines: an import line, then a call. Same `from x import y` shape you already use for `JOBS`.
   </details>
   <details><summary>Hint (partial code)</summary>

   ```python
   from generator.employees import ____

   ____()
   ```
   </details>
5. In `employees.py`, change the catalog import to the package form.
   <details><summary>Checkpoint</summary>

   `from generator.job_catalog import JOBS`
   </details>
6. Run `python -m generator`, then `Get-FileHash data/raw/employees.csv`. Does the hash match step 1?
   <details><summary>If it doesn't match</summary>

   Something changed the random call order or the seed. Compare `head()` with yesterday's output to find the first row that differs.
   </details>
7. Update the test import to `from generator.employees import build_employees`. I'll update the pytest config (scaffolding). `python -m pytest` must still pass.
8. `ruff check`, then ship: PR body starts with `Closes #14`, and mentions the matching hash as the proof.

</details>

<details>
<summary>🔁 Review items due</summary>

Whatever `docs/REVIEW_QUEUE.md` shows as due on Nov 26, most-missed first. Likely: `range` stop, `Closes #N`, `.gitkeep`, `switch -c`, type hints, `index=False`.

</details>

<details>
<summary>🔗 Resources</summary>

- [Python tutorial: modules and packages](https://docs.python.org/3/tutorial/modules.html): sections 6.1 and 6.4.
- [Python docs: `__main__`](https://docs.python.org/3/library/__main__.html): `__main__.py` in packages.
- [GH-900 path](https://learn.microsoft.com/en-us/training/paths/github-foundations/): pull requests and code review.

</details>

<details>
<summary>✅ Done when</summary>

- [ ] `python -m generator` writes `data/raw/employees.csv`
- [ ] The CSV hash matches the pre-refactor hash
- [ ] Tests pass with the package import
- [ ] PR merged with `Closes #14`

</details>

</details>
