# Cheatsheet

Commands and patterns I've used so far, grouped by when I need them. Updated at each `/wrap`.

Click a section to open it. In VS Code's preview (Ctrl+Shift+V) and on GitHub, each one expands.

<details>
<summary><b>Short <code>PS></code> prompt (for screenshots)</b></summary>

The normal prompt shows the full folder path, which includes my Windows username. Hide it before any screenshot that goes public.

**Turn it on:** in the terminal I'm going to screenshot:
```powershell
function prompt { "PS> " }
```
```powershell
cls
```
Then run the script for the shot:
```powershell
python generator/hello_employee.py
```

**Turn it off:** pick one:
- **New terminal (easiest):** click the 🗑 trash icon on the terminal panel, press **Ctrl + `** for a fresh one, then turn the venv back on:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **Or leave it:** the short prompt doesn't break anything. It only hides which folder I'm in (`pwd` shows it).

The short prompt only lasts in the terminal where I typed it. Every new terminal starts with the normal prompt.

</details>

<details>
<summary><b>Start of session</b></summary>

```powershell
cd <repo folder>                     # open the repo in a terminal
.\.venv\Scripts\Activate.ps1         # turn on the venv; prompt shows (.venv)
git switch main                      # go to main
git pull                             # get anything merged on GitHub
git status                           # what's changed? (run this a lot)
```

If activation is blocked by PowerShell's execution policy:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

</details>

<details>
<summary><b>Work on a ticket (GitHub flow)</b></summary>

```powershell
gh issue list                        # see open tickets
git switch -c <issue#>-<short-name>  # CREATE a new branch, e.g. 1-job-catalog
git switch <branch-name>             # GO TO a branch that already exists (no -c)
git branch                           # list branches; * marks where I am
git branch -d <branch-name>          # delete a branch (only if it's safe)
```

- Each `git switch -c` with a typo makes another new branch. Use `-c` once, then drop it.

- A **branch** is a sticky note pointing at a commit. Committing on a branch moves only that note. `main` stays put until the PR is merged.
- Work in the editor, **save the file**, then check in the terminal.

</details>

<details>
<summary><b>Run and check code</b></summary>

```powershell
python generator/hello_employee.py   # run a script
ruff check generator                 # lint; fix anything it reports
ruff check generator --fix           # let ruff fix the simple ones (e.g. import order)
ruff format generator/<file>.py      # FORMATTER: fix spacing/quotes/layout (doesn't change behavior)
ruff format --check generator        # preview what format would change, without changing it
pip install -r requirements.txt      # install packages listed in requirements
```

- `ruff check` = **linter** (finds mistakes). `ruff format` = **formatter** (tidies layout). Passing ruff ≠ correct code: it checks grammar, not meaning.
- Format only the files your ticket touched, so the PR stays about one thing.

</details>

<details>
<summary><b>Ship it</b></summary>

```powershell
git status                           # check: no secrets, no data files, right files only
git add <file>                       # stage (or `git add .` after checking status)
git commit -m "Short description of what changed"
git push -u origin <branch-name>     # first push of a new branch
gh pr create --title "..." --body "Closes #N. ..."   # open the PR; Closes #N goes in the BODY
gh pr edit <N> --body "Closes #1. ..."   # add/fix the PR body after the fact
gh pr merge <N> --merge --delete-branch  # merge and clean up the branch
```

- `gh pr create --fill` copies the commit message as the title and leaves the **body empty**, so there's no `Closes #N`. Add it.

- `Closes #N` in the PR links the PR to the ticket and closes the ticket when the PR merges, so anyone can trace why a change was made.
- Fix the last commit message (before pushing): `git commit --amend`

</details>

<details>
<summary><b>Python basics</b></summary>

| Python | R | Power Query |
|---|---|---|
| list `[a, b, c]`: by position | vector / `list()` | `{a, b, c}` |
| dict `{"key": value}`: by name | named list | record `[key = value]` |
| list of dicts: rows with named fields | data frame | table |

```python
plans = [
    {"plan_code": "MED-PPO", "monthly_premium": 650},
    {"plan_code": "MED-HDHP", "monthly_premium": 480},
]
len(plans)                     # 2
plans[0]                       # first row (Python counts from 0!)
plans[0]["monthly_premium"]    # 650
plans[-1]                      # last row
```

- `plans[2]` here → `IndexError: list index out of range`. The last valid position is `len(plans) - 1`.
- Import from my own file in the same folder: `from plans import PLANS` (constants in ALL_CAPS).
- One row = one dict; text in quotes, numbers without quotes or commas (`100000`, not `100,000`).
- Pick a random row (seeded): `row = fake.random_element(JOBS)`, then `row["job_title"]`.
- Whole number in a range (seeded): `fake.pyint(min_value=..., max_value=...)` (or `fake.random_int(min, max)`).
- Order matters with a seed: each `fake.` call takes the next number, so moving a call changes everything after it.
- Inside an f-string that uses `"`, use `'` for dict keys: `f"Job: {row['job_title']}"`.
- f-strings: `print(f"Salary: ${salary:,}")` → `Salary: $120,000`

</details>

<details>
<summary><b>Functions</b></summary>

```python
def annual_premium(monthly: int) -> int:
    """Turn a monthly premium into an annual one."""
    return monthly * 12

annual_premium(480)    # 5760
```

| Piece | Meaning |
|---|---|
| `def name(...)` | define a function (Power Query custom function / R `function()`) |
| `(monthly: int)` | the **input** and its type, inside the parentheses |
| `-> int` | the **output** type, after the parentheses |
| `"""..."""` | docstring: one line on what it does |
| `return` | hand the answer back. **R returns the last line automatically; Python doesn't** (no `return` = `None`) |
| indentation (4 spaces) | what's inside the function; Python's version of `{ }` |

- The function only sees what you pass in. `monthly` is a placeholder, not "the medical plan".
- Variables made inside a function exist only inside it (like steps inside a Power Query `let`). Hand them out with `return`.
- Don't overwrite a parameter inside the function (`employee_id = 100001` would give every employee the same ID).
- Values that already exist in a row are pulled out, not re-made: `job_row["grade"]`.

</details>

<details>
<summary><b>Loops and range</b></summary>

```python
range(5, 8)            # 5, 6, 7   ← the stop number is LEFT OUT
range(100001, 100011)  # 100001 … 100010 = 10 numbers
```

- **stop − start = how many numbers.** (Not the two numbers you typed.)

Build a list in a loop:
```python
employees = []                                     # the table (empty), plural name
for employee_id in range(100001, 100011):          # the loop variable: one number each time
    employees.append(make_employee(employee_id))   # make one row, add it to the table

for employee in employees:                         # loop over the rows, singular name
    print(employee)
```

- `for X in ...` puts each value into X, so **never reuse the list's name** as the loop variable.
- Indented lines repeat; the first unindented line runs once, after the loop.
- List → look up by **position** `employees[0]`; dict → by **name** `employees[0]["name"]`.

</details>

<details>
<summary><b>pandas DataFrames</b></summary>

A DataFrame is a real table: Power Query table = R tibble = pandas DataFrame.

```python
import pandas as pd                # standard nickname, always `pd`

plans = [
    {"plan_code": "MED-PPO",  "monthly_premium": 650},
    {"plan_code": "MED-HDHP", "monthly_premium": 480},
]
df = pd.DataFrame(plans)           # list of dicts → table: each dict = a row, each key = a column
print(df)
```
```
  plan_code  monthly_premium
0   MED-PPO              650
1  MED-HDHP              480
```

- `df` = the usual name for "the DataFrame I'm working on".
- The `0, 1` on the left is the **index**: row numbers pandas adds (counts from 0).

| Inspect | Shows | R |
|---|---|---|
| `df.head()` | first 5 rows | `head(df)` |
| `df.shape` | `(rows, columns)` | `dim(df)` |
| `df.dtypes` | each column's data type | `str(df)` / `glimpse(df)` |

- `df.shape` and `df.dtypes` have **no `()`**: they're facts about the table, not actions. `df.head()` **has** `()`: it does something.
- `df.shape` → `(2, 2)`: just two numbers. The index is **not** counted as a column.

**Reading dtypes:**

| dtype | Means | Power Query |
|---|---|---|
| `int64` | whole number | Whole Number |
| `str` | text | Text |
| `datetime64` | date / date-time | Date / Date-Time |
| `object` | "type unknown" | ABC123 (Any): needs a type step |

**Change a column's type** (Power Query "Changed Type"):
```python
df["hire_date"] = pd.to_datetime(df["hire_date"])   # pick column → convert → put it back
```

**Dates:** keep them as a real date type; write them as **YYYY-MM-DD** (ISO 8601). It sorts correctly, is unambiguous, and every tool reads it. MM-DD-YYYY is a *display* format: set it in Power BI, or only on an output copy for a vendor spec:
```python
df["hire_date"].dt.strftime("%m-%d-%Y")   # → text, loses the date type; do this last
```

**Write a CSV:**
```python
from pathlib import Path

Path("data/raw").mkdir(parents=True, exist_ok=True)   # make the folder(s) if missing
df.to_csv("data/raw/employees.csv", index=False)      # index=False = no junk 0,1,2 column
```
- `to_csv` won't create folders; `mkdir` does. `parents=True` = make every level; `exist_ok=True` = don't crash if it's already there.
- Paths are relative to where you **run** the script from (the repo root).
- Generated data (`data/raw/`) is git-ignored: the code + seed are the source, not the file.

**Import order** (ruff `I001`): three groups, blank line between:
1. built into Python: `from pathlib import Path`
2. installed with pip: `import pandas as pd`, `from faker import Faker`
3. my own files: `from job_catalog import JOBS`

`import x` lines before `from x import y` lines. `ruff check generator --fix` sorts it.

**VS Code:** Rainbow CSV extension (mechatroner) colors each column; `Align` in the status bar lines them up.

</details>

<details>
<summary><b>Faker and seeds</b></summary>

```python
from faker import Faker
Faker.seed(42)       # same seed → same fake data every run
fake = Faker()
fake.first_name(), fake.last_name()
fake.date_between(start_date="-10y", end_date="today")
```

Faker also has `random_element` and `random_int`. Look them up when the ticket needs them.

</details>

<details>
<summary><b>Reading errors</b></summary>

- Read **bottom-up**. The last line is the error type and reason, e.g. `IndexError: ...`.
- Above it are the file and line number where the error happened.
- `NameError: name 'x' is not defined` → the variable doesn't exist (typo, or renamed in one place only).
- `ImportError: cannot import name 'X'` → the file was found but has no `X` in it.
- ruff `F401` = imported but unused (finish the code; don't `--fix` away an import you're about to use).
- ruff `F821` = undefined name (same as NameError, caught before running).
- ruff `F841` = assigned but never used (made inside a function but never returned).
- `invalid-syntax` → fix the **first** error first; later ones are often knock-ons.
- `AttributeError: 'int' object has no attribute 'append'` → you're calling a list method on a number (name reused, or typo like `apend`).
- `TypeError: list indices must be integers ... not str` → asked a list for a column name; pick a row first: `employees[0]["name"]`.
- git `pathspec ... did not match any files` → that file doesn't exist (not created/saved, or misspelled).
- git `a branch named 'x' already exists` → drop the `-c`.

</details>

<details>
<summary><b>Gotchas I've hit</b></summary>

- Terminal vs. editor vs. GitHub website: know which one you're in.
- File not saved, or saved in the wrong folder → the script runs old code or "file not found".
- `.gitkeep` only exists so Git tracks an empty folder. It has nothing to do with branches.
- A passing `ruff check` on an empty file proves nothing: check that the file has content (size 0 = not saved).
- Rename a variable everywhere: click it in VS Code, press **F2**, type the new name.
- `end_date="today"` moves every day, so a seed only reproduces the same data within one day (fix in #9).

</details>

<details>
<summary><b>VS Code layout</b></summary>

- Terminal on the right: right-click the **TERMINAL** tab → **Panel Position → Right**.
- Terminal beside a file: Ctrl+Shift+P → `Terminal: Create New Terminal in Editor Area to the Side`.
- This cheatsheet as a reading pane: open `docs/CHEATSHEET.md`, press **Ctrl+K** then **V** (preview to the side).
- **Ctrl + `** jumps between code and terminal. A new terminal needs `.\.venv\Scripts\Activate.ps1`.
- Short prompt for screenshots: `function prompt { "PS> " }` (lasts for that terminal only).

</details>
