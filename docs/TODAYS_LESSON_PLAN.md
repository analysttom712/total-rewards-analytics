# Today's Lesson Plan

Today plus the next **2 sessions**, always planned ahead. Each day has the goal, the agenda, an in-depth **deep dive**, a **do-it-yourself** path with hidden checkpoint answers, the review items due, resources, and "done when".

**How to use it:** open with **Ctrl+Shift+V** and click a day. If I'm not around, follow the *Do it yourself* section step by step: try each checkpoint before opening its answer. `/standup` rolls this forward every session; `/wrap` marks what got done.

---


<details>
<summary><b>📍 TODAY · Sat Nov 28 · Day 6 · Issue #19: run the generator as of a fixed date</b></summary>

> **Resume here (Day 6 stopped at CI).** Steps 0–7 are done: PR #46 is open on `19-as-of-date`. Left to do: (1) read the CI failure on #46 yourself (test name, `>` line, both dates); (2) find why Linux draws a different hire date for the same seed (the plan is in the `docs/LEARNING_LOG.md` resume note); (3) fix it and get CI green; (4) re-check `Get-FileHash` = `D39A00DE…8347`; (5) `/review` in a new chat, then merge. Then roll to #14.

<details>
<summary>🎯 Goal and why it matters</summary>

The manager re-ran the employee file two days apart and some hire dates moved. **It already happened in this repo:** Day 5's notes show Angel Hill (100001) hired `2020-09-10`; running the same code on Nov 28 gives `2020-09-13`. Same seed, no code change, different answer.

The cause is in `make_employee`: `fake.date_between(start_date="-10y", end_date="today")`. Both ends of that window are measured from *today*, so the window slides one day every day. Today you pin both ends to fixed dates, prove the CSV is identical, and add a **golden-value** test that fails loudly if the date ever drifts again.

Every report you sign off on is run "as of" a period end. This is the first step toward effective dating and as-of joins in Phase 2.

**Pace (adjustment rule 1 from Day 5):** a worked example before each build step; you read every error first, before any hint. The `Closes #N` drill (#36, 10 min) fits into the Ship block, on this PR.

</details>

<details>
<summary>🗓 Agenda</summary>

| Block | What |
|---|---|
| Standup + review | the map · Day 5 recap · 1 due review question |
| Lesson | as-of dates · constants (`ALL_CAPS`) · `datetime.date` · golden values |
| Build | fingerprint before → `datetime` import + constants → fix the window → golden test → break it on purpose |
| Check | `python -m pytest` → 4 passed · `ruff check` · `/quiz` |
| Ship | #36 drill → PR with `Closes #19` → `/review` in a new chat → merge |
| Cert study | GH-900: *Working with GitHub repositories* |

</details>

<details>
<summary>📚 Deep dive: as-of dates, constants and golden values</summary>

**Why the dates drift.** Faker turns `"-10y"` into "today minus 10 years" and `"today"` into today's date, every time it runs. So the window is:

```text
run on Nov 25:   2016-11-25 ──────────────── 2026-11-25
run on Nov 26:   2016-11-26 ──────────────── 2026-11-26   (both ends slid one day)
```

The seed makes the *random draw* the same (say "a point 39% of the way along"), but 39% of a different window is a different date. A payroll report run "for the last 12 months" gives a different answer every day; a report run "for Jan 1 to Dec 31, 2026" never does.

**The fix pins both ends.** Fixing only `end_date` isn't enough: `"-10y"` still slides.

**`datetime.date`: a real date value.** `datetime` is a **built-in module** (import group 1, no pip install). Inside it, `date(year, month, day)` builds one calendar date:

```python
from datetime import date

date(2026, 11, 1)   # → datetime.date(2026, 11, 1)
```

Power Query version: `#date(2026, 11, 1)`. It's a date *value*, not the text `"2026-11-01"`.

**Constants: `ALL_CAPS` names.** A **constant** is a value set once at the top of a module and never changed while the program runs. Python doesn't enforce it; the capital letters are a promise to the reader ("don't reassign this"). You already use one: `JOBS` in `job_catalog.py`. Report version: the parameter "Period end = 11/01/2026" on a report's cover page. Change it in one place and the whole report follows.

**Golden value test.** Type the expected answer in by hand (from a run you checked), not recomputed by the same code. If anything makes the output drift, the test fails. Recon version: tying a report to a control total from another system.

**File hash: proof of "identical".** `Get-FileHash <file>` prints a fingerprint of the file's exact bytes (SHA-256). One changed character → a completely different hash. Same hash = identical file, to the last comma.

</details>

<details>
<summary>🛠 Do it yourself</summary>

Windows: **terminal** = the VS Code terminal at the repo root (`total-rewards-analytics`). **Editor** = the file named in each step. Inline suggestions are off; if grey text appears, press Esc.

0. **Goal: start the ticket on its own branch.** Terminal: `git switch main`, `git pull`, then `git switch -c 19-as-of-date`. Check: `git branch` shows `* 19-as-of-date`. Uncommitted doc edits from the last two sessions come along in the working folder. That's fine as long as step 7 stages only the two ticket files by name, never everything at once.

1. **Goal: fingerprint the file before changing anything.** Terminal:
   ```powershell
   python generator/hello_employee.py
   ```
   ```powershell
   Get-FileHash data/raw/employees.csv
   ```
   Copy the `Hash` value into a note. Also note the first row's `hire_date` from the printed `head()`. (Predict: will this hash match tomorrow's if we change nothing?)

2. **Goal: one place that says "this file is as of Nov 1, 2026".**
   - **Task:** using the built-in `datetime` module's `date`, add an import and two constants.
   - **Fill in:**
     ```python
     from datetime import ____
     ```
     ```python
     AS_OF = date(____, ____, ____)
     EARLIEST_HIRE = date(2016, 11, 1)
     ```
   - **Clues:** which name inside `datetime` builds a calendar date (see the deep dive)? `AS_OF` is the period-end date the ticket uses: November 1, 2026, as year, month, day.
   - **Where it goes:**
     1. File: `generator/hello_employee.py` (tab says `hello_employee.py`).
     2. Spot: the import goes **before** `from pathlib import Path` (built-ins sort alphabetically, `datetime` before `pathlib`). The two constants go **after** `from job_catalog import JOBS` and its blank line, **before** `fake = Faker()`.
     3. Action: insert (nothing is replaced).
     4. Indent: 0 (top level) for all three lines.
     5. Before → after:
        ```text
        before:                              after:
        from pathlib import Path             from datetime import date
                                             from pathlib import Path
        import pandas as pd                  ...
        ...                                  from job_catalog import JOBS
        from job_catalog import JOBS
                                             AS_OF = date(2026, 11, 1)
        fake = Faker()                       EARLIEST_HIRE = date(2016, 11, 1)

                                             fake = Faker()
        ```
   - **Check:** terminal `ruff check generator` → `All checks passed!` (`date` is used by the constants, so no F401 "imported but unused"). The constants aren't used yet; that's step 3.

3. **Goal: draw hire dates from the fixed window, never "today".**
   - **Worked example first** (a different field, same shape):
     ```text
     before:  fake.date_between(start_date="-30d", end_date="today")
     after:   fake.date_between(start_date=PERIOD_START, end_date=PERIOD_END)
     ```
     Each text string becomes a constant name, no quotes (quotes would make it the literal text `"PERIOD_START"`).
   - **Task:** in `make_employee`, replace both text ends of the hire-date window with your constants.
   - **Fill in:**
     ```python
     hire_date = fake.date_between(start_date=____, end_date=____)
     ```
   - **Clues:** which constant is the earliest anyone could be hired? Which is the as-of date?
   - **Where it goes:** file `generator/hello_employee.py`; spot: the line `hire_date = fake.date_between(start_date="-10y", end_date="today")`; action: replace `"-10y"` and `"today"` (quotes included) and nothing else; indent stays 4.
   - **Check:** terminal `python generator/hello_employee.py`. The first row's `hire_date` changed from step 1. Write the new date down; step 4 needs it.
   <details><summary>Hint (bigger, only after a try)</summary>

   Two names, no quote marks around either. The start of the window comes first.
   </details>
   <details><summary>Checkpoint answer</summary>

   `hire_date = fake.date_between(start_date=EARLIEST_HIRE, end_date=AS_OF)` · first employee's hire date becomes `2020-08-18`.
   </details>

4. **Goal: a test that fails loudly if the date ever drifts.**
   - **Task:** add a golden-value test that builds one employee and compares its `hire_date` to the date you wrote down, typed by hand with `date(...)`.
   - **Fill in:**
     ```python
     def test_first_hire_date_is_pinned():
         first = build_employees(1)[____]
         assert first[____] == date(____, ____, ____)
     ```
   - **Clues:** `build_employees(1)` returns a list with one dict in it: which position is the only one? Which key holds the hire date (look at the dict keys in `make_employee`'s `return`)? The date is the one you wrote down in step 3, as year, month, day.
   - **Where it goes:**
     1. File: `tests/test_generator.py` (tab says `test_generator.py`).
     2. Spot: first add `from datetime import date` as the **first line** of the file, then a blank line, above `from hello_employee import build_employees`. The test goes after the last line of the file, `assert job["salary_min"] <= e["salary"] <= job["salary_max"]`, with two blank lines before it.
     3. Action: insert.
     4. Indent: `def` at 0, body at 4.
   - **Check:** terminal `python -m pytest` → `4 passed` in `tests/test_generator.py`.

5. **Goal: see the golden test catch drift.** Predict first: if you put `end_date="today"` back, does the test fail, and what two dates will it print? Make that one change in `hello_employee.py`, save, run `python -m pytest tests/test_generator.py`. Read the failure bottom-up: test name, line, the two dates. Write it as one sentence for the PR. Then undo (Ctrl+Z, save) and rerun → `4 passed`.
   <details><summary>What you should see</summary>

   `FAILED ... test_first_hire_date_is_pinned` with `assert datetime.date(2020, 9, 13) == datetime.date(2020, 8, 18)` if run on Nov 28 (the left date slides one day per calendar day). That's the planted bug in the code (the window), not in the rule (the golden date), so the test can fail.
   </details>

6. **Goal: prove the file no longer depends on the day.** Terminal: run the script, `Get-FileHash data/raw/employees.csv`, note the hash. At tomorrow's standup, run both again: the hash must match. (Today's hash won't match step 1's: the dates changed on purpose.)

7. **Goal: ship.** `ruff check`, `ruff format --check`, `git status` (only `generator/hello_employee.py` and `tests/test_generator.py`), commit, push, PR. **#36 drill first:** without a hint, write the PR body's first line that closes #19 on merge.

</details>

<details>
<summary>🔁 Review items due</summary>

From `docs/REVIEW_QUEUE.md` (due Nov 28 or earlier: nearly the whole queue after two days off). Asked at standup: `return` vs `print` (5 misses, mini-ticket #20). In the Ship block: `Closes #N` (4 misses, #36). Golden values come up in step 4. The rest wait for `/quiz`: list `[0]` vs dict `["name"]`, `KeyError` vs `IndexError`, apply ×12 once, false pass.

</details>

<details>
<summary>🔗 Resources</summary>

- [Python docs: `datetime.date` objects](https://docs.python.org/3/library/datetime.html#date-objects): the constructor `date(year, month, day)` and `date.today()` (the thing we're removing).
- [Faker docs](https://faker.readthedocs.io/): search for `date_between`; it shows `start_date` / `end_date` accept a `date` object, not just text like `"-30y"`.
- [PowerShell: `Get-FileHash`](https://learn.microsoft.com/powershell/module/microsoft.powershell.utility/get-filehash): the first example.
- [GH-900 path](https://learn.microsoft.com/en-us/training/paths/github-foundations/): *Working with GitHub repositories*.

</details>

<details>
<summary>✅ Done when</summary>

- [x] No `"today"` or `"-10y"` left in the generator; `AS_OF` and `EARLIEST_HIRE` at the top
- [x] Golden test passes; seen failing once on purpose (sentence written for the PR)
- [x] `ruff check` clean; `python -m pytest` passes **locally** (101 passed, 5 skipped)
- [ ] **CI green on PR #46.** It fails on Linux: the golden test gets 2019-01-25, not 2020-08-18
- [x] `Closes #19` written without a hint (#36) · [ ] PR merged
- [ ] Next session: the CSV hash still matches `D39A00DE…8347`

</details>

</details>

---

<details>
<summary><b>NEXT · Day 7 · Issue #14: make the generator a package (<code>python -m generator</code>)</b></summary>

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

0. From `main` after #19 is merged (CI green): `git switch -c 14-generator-package`. Check the golden test still passes after the rename: it guards the refactor too.
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

Whatever `docs/REVIEW_QUEUE.md` shows as due that day, most-missed first. Likely: list vs dict lookup, `KeyError` vs `IndexError`, `range` stop, type hints.

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

---

<details>
<summary><b>NEXT +1 · Day 8 · Issue #13 part 1: an org catalog and a department for every employee</b></summary>

<details>
<summary>🎯 Goal and why it matters</summary>

The manager's ask: *every cost report is cut by department and cost center, and the fake employees don't belong to any department.* #13 is 1–2 sessions, so per adjustment rule 1 it's split: **part 1 (this day)** builds the org catalog and gives each employee a seeded `department_code`; **part 2** does the pandas `merge` and the before/after row-count check.

Org keys are the spine of every Total Rewards report: legal entity → business unit → department → cost center. Same hierarchy you filter by in Power BI.

</details>

<details>
<summary>🗓 Agenda</summary>

| Block | What |
|---|---|
| Standup + review | re-run yesterday's `Get-FileHash` (must match) · 1 due review question |
| Lesson | Org keys (LE → BU → dept → cost center); a catalog as a list of dicts (you built `JOBS` on Day 2) |
| Build | `generator/org_catalog.py` with `ORGS` → `make_employee` picks a department → test: every `department_code` exists in `ORGS` |
| Check | pytest, ruff, `/quiz` |
| Ship | PR (part 1, no `Closes`: the issue stays open for part 2. Write `Part of #13`) |
| Cert study | GH-900: *Collaboration features* (issues) |

</details>

<details>
<summary>📚 Deep dive: org keys and why the call order matters</summary>

**The hierarchy.** One row per department, carrying its parents:

```text
legal_entity  business_unit  department_code  department_name   cost_center
LE01          BU100          D1001-FIN        Finance           CC1001
LE01          BU100          D1002-HR         Human Resources   CC1002
LE01          BU200          D2001-OPS        Operations        CC2001
```

This is a **flattened dimension**: every row repeats its parents, like a Power BI `dim_department` table with LE and BU columns so a slicer can filter at any level.

**A catalog is a list of dicts.** `ORGS` has the same shape as `JOBS`: each dict is one row, the keys are the column names.

**Warning: a new random call shifts every value after it.** The seed hands out random numbers in a fixed order. If `make_employee` picks a department *before* the name, every name, hire date and salary changes, and yesterday's golden test fails. Put the new pick **last** so earlier values don't move. (Predict at build time: what would the golden test say if the pick went first?)

</details>

<details>
<summary>🛠 Do it yourself</summary>

0. From `main` after #14 merged: `git switch -c 13-org-catalog`.
1. Create `generator/org_catalog.py` with a docstring and `ORGS = [ ... ]`: 2 business units, 5 departments, the five keys above. (Scaffolding-style; copy the shape of `JOBS`.)
2. In `make_employee`, after the salary line, pick one org row with the same seeded tool you used for `job_row`.
   <details><summary>Hint (nudge)</summary>

   Which `fake.` method picked a job from `JOBS`?
   </details>
   <details><summary>Hint (partial code)</summary>

   ```python
   org_row = fake.____(ORGS)
   ```
   </details>
3. Add `"department_code": org_row[____]` to the returned dict.
4. Run pytest: does the golden hire-date test still pass? (It should if the pick is last.)
5. Test: every employee's `department_code` is one of the codes in `ORGS` (build a `set` of valid codes, then assert each employee's code is `in` it).
6. Ship with `Part of #13` in the body.

</details>

<details>
<summary>🔗 Resources</summary>

- [Python tutorial: sets](https://docs.python.org/3/tutorial/datastructures.html#sets): membership with `in`.
- [Faker: `random_element`](https://faker.readthedocs.io/en/master/providers/baseprovider.html#faker.providers.BaseProvider.random_element)
- [GH-900 path](https://learn.microsoft.com/en-us/training/paths/github-foundations/): collaboration features.

</details>

<details>
<summary>✅ Done when</summary>

- [ ] `ORGS` has 2+ business units and 5+ departments
- [ ] Every employee has a `department_code` that exists in `ORGS` (tested)
- [ ] Golden hire-date test still passes (the pick went last)
- [ ] PR merged with `Part of #13`; #13 stays open for part 2 (merge + row counts)

</details>

</details>
