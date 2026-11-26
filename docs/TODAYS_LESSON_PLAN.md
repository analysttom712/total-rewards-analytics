# Today's Lesson Plan

Today plus the next **2 sessions**, always planned ahead. Each day has the goal, the agenda, an in-depth **deep dive**, a **do-it-yourself** path with hidden checkpoint answers, the review items due, resources, and "done when".

**How to use it:** open with **Ctrl+Shift+V** and click a day. If I'm not around, follow the *Do it yourself* section step by step: try each checkpoint before opening its answer. `/standup` rolls this forward every session; `/wrap` marks what got done.

---


<details>
<summary><b>📍 TODAY · Wed Nov 25 · Day 5 · Issue #9 part 2: unique IDs + salaries in range, then ship #9</b></summary>

<details>
<summary>🎯 Goal and why it matters</summary>

Finish #9. The manager asked for proof of three things; part 1 proved the first (same seed → same employees). Today you prove the other two: **every employee ID is unique** and **every salary sits inside its job's pay range**. Then you break one on purpose, read the failure, and open the PR with `Closes #9`.

These are the two checks you already run by hand on every census file: "no duplicate employee IDs" and "nobody paid outside their band". In Phase 3 they become the dbt tests `unique` and `accepted_range`.

The hire-date drift fix moved to its own day (#19, Day 6) so today stays one ticket and one new idea.

</details>

<details>
<summary>🗓 Agenda</summary>

| Block | What |
|---|---|
| Standup + review | the map · Day 4 recap · `return` vs `print` review question |
| Lesson | `set` (distinct values) and the chained comparison `a <= b <= c` |
| Build | test 2 (unique IDs), test 3 (salary in range), break one on purpose |
| Check | `python -m pytest` → 3 passed · `ruff check` · `/quiz` |
| Ship | commit → PR with `Closes #9` → `/review` in a new chat → merge |
| Cert study | GH-900: *Introduction to GitHub* (issues and pull requests) |

</details>

<details>
<summary>📚 Deep dive: sets, distinct counts and range checks</summary>

**The data you're testing.** `build_employees(25)` returns a **list of dicts**. The first one:

```text
{'employee_id': 100001, 'name': 'Angel Hill', 'hire_date': datetime.date(2020, 9, 10),
 'job_code': 1, 'job_title': 'Compensation Analyst', 'grade': 4, 'salary': 104572}
```

And the job it points at, `JOBS[0]` in `generator/job_catalog.py`:

```text
{'job_code': 1, 'job_title': 'Compensation Analyst', 'grade': 4,
 'salary_min': 100000, 'salary_max': 125000}
```

The link between them is `job_code`. Same as a relationship between an employee table and a job table in Power BI.

**`set`: a collection that keeps only distinct values.** `set([100001, 100002, 100002])` → `{100001, 100002}`. Curly braces, no duplicates, no order.

| Check | Python | Power BI / Power Query |
|---|---|---|
| Are all IDs unique? | `len(set(ids)) == len(ids)` | `DISTINCTCOUNT(id) = COUNTROWS(table)` |
| | | Row count before vs after *Remove Duplicates* |

If any ID repeats, the set is shorter than the list, the `==` is `False`, and the `assert` fails.

**`len()` = length:** how many items are in a list or set. Like `COUNTROWS`.

**Chained comparison `a <= b <= c`:** true only when `b` is between `a` and `c`, ends included. It's SQL's `BETWEEN`. `100000 <= 104572 <= 125000` → `True`.

**Why a test needs a loop here:** one `assert` checks one thing. To check 25 salaries, you loop over the employees and assert inside the loop. The first salary out of range stops the test and shows you which one. A recon that stops at the first exception and points at the row.

</details>

<details>
<summary>🛠 Do it yourself</summary>

Window for all code steps: **editor**, file `tests/test_generator.py` (check the tab says `test_generator.py`). Inline suggestions are off in this repo; if grey text appears anyway, press Esc.

1. **Goal: prove no employee ID repeats.** Add a second test function below the first.
   - Fill in:
     ```python
     def test_employee_ids_are_unique():
         employees = build_employees(25)
         ids = []
         for e in employees:
             ids.append(e[____])
         assert len(____) == len(____)
     ```
   - Clues: which dict key holds the ID (look at the first employee above)? Which side of `==` gets duplicates squeezed out?
   - Where: after the last line of `test_same_seed_same_employees` (`assert first == second`), two blank lines, then the new function at indent 0, body at 4, loop body at 8.
   - Check: `python -m pytest tests/test_generator.py` (terminal, repo root) → `2 passed`.
   <details><summary>Hint (bigger, only after a try)</summary>

   The key is a string literal in square brackets. One side of the `==` wraps `ids` in `set(...)`.
   </details>
   <details><summary>Checkpoint answer</summary>

   ```python
   ids.append(e["employee_id"])
   assert len(set(ids)) == len(ids)
   ```
   </details>
2. **Goal: prove every salary is inside its job's range.** Third test. You need `JOBS` too, so first change the import line at the top.
   - Fill in (import):
     ```python
     from hello_employee import build_employees
     from job_catalog import ____
     ```
   - Fill in (test):
     ```python
     def test_salaries_inside_pay_range():
         employees = build_employees(25)
         for e in employees:
             for job in JOBS:
                 if job["job_code"] == e[____]:
                     assert job[____] <= e["salary"] <= job[____]
     ```
   - Clues: which key links an employee to a job? Which two job keys hold the bottom and top of the band?
   - Where: the import goes on the line right after `from hello_employee import build_employees`; the test goes after `test_employee_ids_are_unique`, two blank lines, indent 0 / 4 / 8 / 12 / 16.
   - Check: → `3 passed`.
   <details><summary>Checkpoint answer</summary>

   `from job_catalog import JOBS` · `e["job_code"]` · `job["salary_min"] <= e["salary"] <= job["salary_max"]`
   </details>
3. **Goal: see the test catch a real problem.** In `generator/job_catalog.py`, temporarily change job 1's `"salary_min": 100000` to `110000`. Predict first: will test 3 fail, and for which employee? Run pytest. Read the failure bottom-up: which line, what were the three numbers? Write that down for the PR description. Then put `100000` back and rerun → `3 passed`.
   <details><summary>What you should see</summary>

   `F` for `test_salaries_inside_pay_range`, an `AssertionError` showing something like `assert 110000 <= 104572`. Angel Hill (100001) was paid 104,572, inside the real band but below the fake new minimum.
   </details>
4. **Goal: ship.** `ruff check`, `ruff format --check`, `git status` (only `tests/test_generator.py` and docs should show), commit, push, open the PR. The body's first line is `Closes #9`; add the failure you read in step 3.

</details>

<details>
<summary>🔁 Review items due</summary>

From `docs/REVIEW_QUEUE.md`: `return` vs `print` (3 misses, mini-ticket #20), list position vs dict key, apply ×12 once, `git add` is a snapshot, `restore --staged` vs `restore`, lookup errors, import groups, `mkdir`, ISO dates. Today's tests lean on two of them: `build_employees` must **return** its list, and `e["employee_id"]` is a dict lookup by name.

</details>

<details>
<summary>🔗 Resources</summary>

- [pytest: How to write and report assertions](https://docs.pytest.org/en/stable/how-to/assert.html): what pytest prints when an `assert` fails.
- [Python tutorial: sets](https://docs.python.org/3/tutorial/datastructures.html#sets): the first two paragraphs are enough.
- [GH-900 path](https://learn.microsoft.com/en-us/training/paths/github-foundations/): *Introduction to GitHub*.

</details>

<details>
<summary>✅ Done when</summary>

- [ ] `python -m pytest tests/test_generator.py` → `3 passed`
- [ ] You saw test 3 fail on purpose and wrote down what it said
- [ ] `ruff check` clean
- [ ] PR open with `Closes #9`; `/review` run in a new chat; merged

</details>

</details>

---

<details>
<summary><b>NEXT · Thu Nov 26 · Day 6 · Issue #19: run the generator as of a fixed date</b></summary>

<details>
<summary>🎯 Goal and why it matters</summary>

The manager re-ran the employee file two days apart and some hire dates moved. The cause: `end_date="today"` in `make_employee`. Today you make the generator run **as of** a fixed date, so the file is byte-identical no matter when it's run, and pin it with a golden-value test.

Every report you sign off on is run "as of" a period end. This is the first step toward effective dating and as-of joins in Phase 2.

</details>

<details>
<summary>🗓 Agenda</summary>

| Block | What |
|---|---|
| Standup + review | the map · Day 5 recap · 1 due review question |
| Lesson | as-of dates; constants (`ALL_CAPS`); `datetime.date`; golden values |
| Build | `AS_OF` constant → hash the CSV → golden-value test → break it on purpose |
| Check | pytest, ruff, `/quiz` |
| Ship | PR with `Closes #19` |
| Cert study | GH-900: *Working with GitHub repositories* |

</details>

<details>
<summary>📚 Deep dive: as-of dates, constants and golden values</summary>

**Why the dates drift.** `fake.date_between(start_date="-10y", end_date="today")` picks a random day in a window that ends *today*. Tomorrow the window has moved by a day, so the same random draw lands on a different date. Same seed, different answer.

**The fix: an as-of constant.**
```python
from datetime import date

AS_OF = date(2026, 11, 1)
```
- `datetime` is a built-in module (import group 1); `date(year, month, day)` builds a date.
- `ALL_CAPS` names a **constant**: set once at the top, never changed. Like a report parameter "Period end = 11/01/2026".
- Then `end_date=AS_OF`.

**Proving it's fixed: a file hash.** `Get-FileHash data/raw/employees.csv` prints a fingerprint of the file's exact bytes. Same hash = identical file.

**Golden value test.** Type the expected answer in by hand: the first employee's hire date after the fix. If anything makes the output drift, the test fails. (You met this word in Review 1: don't recompute the formula inside the test.)

</details>

<details>
<summary>🛠 Do it yourself</summary>

0. From `main` after #9 merged: `git switch -c 19-as-of-date`.
1. Fingerprint before: `python generator/hello_employee.py`, then `Get-FileHash data/raw/employees.csv`.
2. Add the `datetime` import (built-in group, top) and the `AS_OF` constant (after the imports, before `fake = Faker()`).
3. In `make_employee`, replace `"today"` with the constant.
   <details><summary>Checkpoint</summary>

   `hire_date = fake.date_between(start_date="-10y", end_date=AS_OF)`
   </details>
4. Run the script and print `employees[0]["hire_date"]`. Write that date down.
5. Golden test in `tests/test_generator.py`: assert `build_employees(1)[0]["hire_date"] == date(____, ____, ____)` with the date from step 4.
6. Break it on purpose (change the day by one), read the failure, put it back.
7. Hash again: does it still match tomorrow? (Re-run tomorrow at standup to prove it.)
8. Ship with `Closes #19`.

</details>

<details>
<summary>🔗 Resources</summary>

- [datetime.date](https://docs.python.org/3/library/datetime.html#date-objects)
- [Get-FileHash](https://learn.microsoft.com/powershell/module/microsoft.powershell.utility/get-filehash)
- [GH-900 path](https://learn.microsoft.com/en-us/training/paths/github-foundations/)

</details>

<details>
<summary>✅ Done when</summary>

- [ ] No `"today"` left in the generator
- [ ] Golden test passes; seen failing once on purpose
- [ ] PR merged with `Closes #19`

</details>

</details>

---


<details>
<summary><b>NEXT +1 · Fri Nov 27 · Day 7 · Issue #14: make the generator a package (<code>python -m generator</code>)</b></summary>

<details>
<summary>🎯 Goal and why it matters</summary>

The manager's ask: *one command that builds every file, from anywhere in the repo.* Right now the generator is a script called `hello_employee.py`. After today it's a **package** you run with `python -m generator`, the way real data tools are run.

This is a **refactor**: the structure changes, the output doesn't. Proving "the output is identical" is a skill reviewers look for in every refactor PR, and your tests from #9 do half the proving for you.

</details>

<details>
<summary>🗓 Agenda</summary>

| Block | What |
|---|---|
| Standup + review | 1 due review question |
| Lesson | Module vs package; `__init__.py`, `__main__.py`, `python -m`; package imports |
| Build | Move code into `generator/employees.py`, add `__main__.py`, update imports and tests |
| Check + ship | Output identical, pytest, ruff, `/quiz`, PR with `Closes #14` |
| Cert study | GH-900: *Introduction to GitHub* (pull requests and code review) |

</details>

<details>
<summary>📚 Deep dive: modules, packages and <code>python -m</code></summary>

| Term | What it is | Power BI version |
|---|---|
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

0. From `main` after #19 is merged: `git switch -c 14-generator-package`.
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
