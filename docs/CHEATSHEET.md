# Cheatsheet

Commands and patterns, organized by the day I learned them. Updated at each `/wrap`.

Click a day to open it, then click a topic. Works in VS Code's preview (Ctrl+Shift+V) and on GitHub. Terms and symbols: see `docs/GLOSSARY.md`.

<details>
<summary><b>⚡ Every session (quick reference)</b></summary>

**Start:**
```powershell
.\.venv\Scripts\Activate.ps1         # turn on the venv; prompt shows (.venv)
git switch main                      # go to main
git pull                             # get anything merged on GitHub
git status                           # what's changed?
gh issue list                        # open tickets
git switch -c <issue#>-<short-name>  # new branch for the ticket
```

**Check:**
```powershell
python generator/hello_employee.py
ruff check generator
ruff format --check generator
```

**Ship:**
```powershell
git status
git add <file>
git commit -m "What changed"
git push -u origin <branch-name>
gh pr create --title "..." --body "Closes #N. ..."
gh pr merge <N> --merge --delete-branch
```

**Study site (learning hub):**
```powershell
python -m hub                        # start it, then open http://127.0.0.1:8765
python -m hub --progress             # print the answers and marks I've saved
```
Ctrl+C in that terminal stops it. In VS Code: Terminal → Run Task… → Start learning hub.

</details>

---

<details>
<summary><b>Day 1 · Nov 22 · Project skeleton + first fake employee</b></summary>

<details>
<summary>Start of session</summary>

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
<summary>Work on a ticket (GitHub flow)</summary>

```powershell
gh issue list                        # see open tickets
git switch -c <issue#>-<short-name>  # create a new branch, e.g. 1-job-catalog
```

- A **branch** is a sticky note pointing at a commit. Committing on a branch moves only that note. `main` stays put until the PR is merged.
- Work in the editor, **save the file**, then check in the terminal.

</details>

<details>
<summary>Run and check code</summary>

```powershell
python generator/hello_employee.py   # run a script
ruff check generator                 # lint; fix anything it reports
ruff check generator --fix           # let ruff fix the simple ones (e.g. import order)
pip install -r requirements.txt      # install packages listed in requirements
```

</details>

<details>
<summary>Ship it</summary>

```powershell
git status                           # check: no secrets, no data files, right files only
git add <file>                       # stage (or `git add .` after checking status)
git commit -m "Short description of what changed"
git push -u origin <branch-name>     # first push of a new branch
gh pr create                         # open the PR
```

- `Closes #N` in the PR links the PR to the ticket and closes the ticket when the PR merges, so anyone can trace why a change was made.
- Fix the last commit message (before pushing): `git commit --amend`

</details>

<details>
<summary>First Python script: Faker and seeds</summary>

```python
from faker import Faker
Faker.seed(42)       # same seed → same fake data every run
fake = Faker()
fake.first_name(), fake.last_name()
fake.date_between(start_date="-10y", end_date="today")
```

- f-strings: `print(f"Salary: ${salary:,}")` → `Salary: $120,000`

</details>

<details>
<summary>Reading errors (the basics)</summary>

- Read **bottom-up**. The last line is the error type and reason, e.g. `IndexError: ...`.
- Above it are the file and line number where the error happened.

</details>

<details>
<summary>Gotchas</summary>

- Terminal vs. editor vs. GitHub website: know which one you're in.
- File not saved, or saved in the wrong folder → the script runs old code or "file not found".
- `.gitkeep` only exists so Git tracks an empty folder. It has nothing to do with branches.

</details>

</details>

<details>
<summary><b>Day 2 · Nov 23 · Job catalog: lists and dicts (#1)</b></summary>

<details>
<summary>Branches: create vs go to vs delete</summary>

```powershell
git switch -c <issue#>-<short-name>  # CREATE a new branch
git switch <branch-name>             # GO TO a branch that already exists (no -c)
git branch                           # list branches; * marks where I am
git branch -d <branch-name>          # delete a branch (only if it's safe)
```

- Each `git switch -c` with a typo makes another new branch. Use `-c` once, then drop it.

</details>

<details>
<summary>PRs: fix the body, merge</summary>

```powershell
gh pr edit <N> --body "Closes #1. ..."   # add/fix the PR body after the fact
gh pr merge <N> --merge --delete-branch  # merge and clean up the branch
```

- `gh pr create --fill` copies the commit message as the title and leaves the **body empty**, so there's no `Closes #N`. Add it.

</details>

<details>
<summary>Lists and dicts</summary>

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

</details>

<details>
<summary>Faker: pick a row, pick a number</summary>

- Pick a random row (seeded): `row = fake.random_element(JOBS)`, then `row["job_title"]`.
- Whole number in a range (seeded): `fake.pyint(min_value=..., max_value=...)` (or `fake.random_int(min, max)`).
- Order matters with a seed: each `fake.` call takes the next number, so moving a call changes everything after it.
- Inside an f-string that uses `"`, use `'` for dict keys: `f"Job: {row['job_title']}"`.

</details>

<details>
<summary>Reading errors</summary>

- `NameError: name 'x' is not defined` → the variable doesn't exist (typo, or renamed in one place only).
- `ImportError: cannot import name 'X'` → the file was found but has no `X` in it.
- ruff `F401` = imported but unused (finish the code; don't `--fix` away an import you're about to use).
- ruff `F821` = undefined name (same as NameError, caught before running).
- git `pathspec ... did not match any files` → that file doesn't exist (not created/saved, or misspelled).
- git `a branch named 'x' already exists` → drop the `-c`.

</details>

<details>
<summary>Short <code>PS></code> prompt (for screenshots)</summary>

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
<summary>Gotchas</summary>

- A passing `ruff check` on an empty file proves nothing: check that the file has content (size 0 = not saved).
- Rename a variable everywhere: click it in VS Code, press **F2**, type the new name.

</details>

</details>

<details>
<summary><b>Day 3 · Nov 24 · Functions and loops (#2), first DataFrame (#3)</b></summary>

<details>
<summary>Functions</summary>

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
<summary>Loops and range</summary>

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
<summary>ruff: linter vs formatter</summary>

```powershell
ruff format generator/<file>.py      # FORMATTER: fix spacing/quotes/layout (doesn't change behavior)
ruff format --check generator        # preview what format would change, without changing it
```

- `ruff check` = **linter** (finds mistakes). `ruff format` = **formatter** (tidies layout). Passing ruff ≠ correct code: it checks grammar, not meaning.
- Format only the files your ticket touched, so the PR stays about one thing.

</details>

<details>
<summary>PRs that close the ticket</summary>

```powershell
gh pr create --title "..." --body "Closes #N. ..."   # Closes #N goes in the BODY
```

- Exact form: `Closes #12` (no extra words between). `Fixes #12` and `Resolves #12` work too.
- The title is free text for humans; it doesn't close anything.
- The issue closes when the PR **merges** into `main`.

</details>

<details>
<summary>pandas DataFrames</summary>

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

</details>

<details>
<summary>Write a CSV and import order</summary>

```python
from pathlib import Path

Path("data/raw").mkdir(parents=True, exist_ok=True)   # make the folder(s) if missing
df.to_csv("data/raw/employees.csv", index=False)      # index=False = no junk 0,1,2 column
```
- `to_csv` won't create folders; `mkdir` does. `parents=True` = make every level; `exist_ok=True` = don't crash if it's already there.
- Paths are relative to where you **run** the script from (the repo root).
- Generated data (`data/raw/`) is git-ignored: the code + seed are the source, not the file.
- Close the CSV in Excel before re-running: Windows locks open files (`PermissionError`).

**Import order** (ruff `I001`): three groups, blank line between:
1. built into Python: `from pathlib import Path`
2. installed with pip: `import pandas as pd`, `from faker import Faker`
3. my own files: `from job_catalog import JOBS`

`import x` lines before `from x import y` lines. `ruff check generator --fix` sorts it.

</details>

<details>
<summary>Reading errors</summary>

- ruff `F841` = assigned but never used (made inside a function but never returned).
- `invalid-syntax` → fix the **first** error first; later ones are often knock-ons.
- `AttributeError: 'int' object has no attribute 'append'` → you're calling a list method on a number (name reused, or typo like `apend`).
- `TypeError: list indices must be integers ... not str` → asked a list for a column name; pick a row first: `employees[0]["name"]`.

</details>

<details>
<summary>Git: undo an uncommitted change, park work</summary>

```powershell
git restore <file>                   # throw away uncommitted edits; back to the last commit
git commit --amend -m "Fixed message"   # fix the last commit message (only before pushing)
```

- Untracked and uncommitted files follow you when you switch branches. Commit (or park) them on the right branch first.

</details>

<details>
<summary>VS Code layout and extensions</summary>

- Terminal on the right: right-click the **TERMINAL** tab → **Panel Position → Right**.
- Terminal beside a file: Ctrl+Shift+P → `Terminal: Create New Terminal in Editor Area to the Side`.
- This cheatsheet as a reading pane: open `docs/CHEATSHEET.md`, press **Ctrl+Shift+V** (or **Ctrl+K** then **V** for preview to the side).
- **Ctrl + `** jumps between code and terminal. A new terminal needs `.\.venv\Scripts\Activate.ps1`.
- Hide the minimap: **View → Appearance → Minimap**.
- Rainbow CSV extension (mechatroner) colors each column; `Align` in the status bar lines them up.

</details>

<details>
<summary>Gotchas</summary>

- `end_date="today"` moves every day, so a seed only reproduces the same data within one day (fix in #9).

</details>

</details>

<details>
<summary><b>Day 3 review · Nov 24 · Deep review session</b></summary>

<details>
<summary>Where am I typing?</summary>

| Place | What it's for | How to tell | Like… |
|---|---|---|---|
| **Editor** (VS Code file tabs) | Writing and saving files | File name on the tab; ● = unsaved | Power Query's Advanced Editor |
| **Terminal** (bottom panel) | **Running** commands: `python`, `git`, `ruff`, `gh` | `(.venv) PS C:\...>` | Clicking Refresh: it runs things |
| **GitHub website** | The shared copy: PRs, issues, review | A browser at github.com | The Power BI Service |

Rule: **write in the editor → save → run in the terminal → share on GitHub.**

</details>

<details>
<summary>The Python REPL (scratchpad)</summary>

```powershell
python           # start it; the prompt becomes >>>
```
```python
exit()           # leave it; back to PS>
```

- **REPL** = Read, Evaluate, Print, Loop. Type one line, see the answer. Nothing is saved; you can't break anything. Like the R console or VBA's Immediate window.
- `>>>` = ready for a new line. `...` = "your last line isn't finished". **Ctrl + C** cancels it (prints `KeyboardInterrupt`).

</details>

<details>
<summary>Quotes, names and types</summary>

```python
"salary"          # 'salary'  → a string literal: the TEXT s-a-l-a-r-y
salary            # NameError → a name: Python looks up what's stored under it
salary = 104572   # assignment: store 104572 under the name salary
salary            # 104572
type(salary)      # <class 'int'>  whole number
type("salary")    # <class 'str'>  text
```

- **Quotes = "take this literally". No quotes = "go look it up".** Excel: `="Total"` vs `=Total` (`#NAME?` = Python's `NameError`).
- Quotes come in **pairs**: `"salary` → `SyntaxError: unterminated string literal`.
- `"salary"` and `'salary'` are the same value; Python *displays* text with single quotes.
- `int` and `str` are the same types pandas shows as `int64` and `str` in `df.dtypes`.

</details>

<details>
<summary>The Git pipeline (one picture)</summary>

```
 EDITOR              STAGING             LOCAL HISTORY        GITHUB              MAIN
 (working folder)    ("the batch")       (your commits)       (origin)            (the trusted copy)
 you edit + save  →  git add        →    git commit      →    git push       →    PR → review → merge
 "modified"          "to be committed"   "a posted entry"     "uploaded"          "Closes #N fires here"
```

| Stage | Command | Accounting version |
|---|---|---|
| Edit and save | (VS Code, Ctrl+S) | Drafting journal entries |
| Stage | `git add <file>` | Selecting which entries go in this batch |
| Commit | `git commit -m "..."` | Posting the batch, with a description |
| Push | `git push` | Sending the posted batch to the shared ledger |
| PR → merge | `gh pr create` → `gh pr merge` | Review and approval, then it's in the official books (`main`) |

- A **branch** is your own ledger copy. Nothing reaches `main` until a PR merges it.
- `Closes #N` (in the PR **body**) closes the issue at the **merge** step, not before.
- `git status` tells you which stage every changed file is in. Run it before every `git add` and every commit.

</details>

<details>
<summary>Staging and unstaging, hands-on</summary>

```powershell
git add docs/GLOSSARY.md docs/COACHING.md   # name files, separated by spaces (not commas)
git restore --staged docs/GLOSSARY.md       # out of the batch, edits kept
git restore generator/hello_employee.py     # ⚠️ throws away uncommitted edits
```

- `git add .` stages everything in the folder. Naming files is safer: you see exactly what goes in.
- `restore --staged` sends a file back to its state **before** `git add` (new file → Untracked, edited file → Modified).
- `git status` headings are **states**, not files: all 11 staged files sat under one heading.
- `nothing to commit, working tree clean` = everything's committed.

</details>

<details>
<summary>Push, PR, merge</summary>

```powershell
git push -u origin learning-loop
```
```powershell
gh pr merge --squash --delete-branch
```
```powershell
git switch main; git pull
```

- `-u` links the branch to GitHub on the first push; after that, plain `git push`.
- `origin` = your GitHub copy. `HEAD` = the branch you're on.
- In the push output, read `[new branch]` and `set up to track`; skip the "objects" lines.
- Open the PR with `gh pr create --title "..." --body "..."`.

</details>

<details>
<summary>Lists vs dicts: lookups and their errors</summary>

```python
jobs[1]["job_title"]   # row first (position), then column (key)
jobs[-1]               # last row
```

| You type | Error | Meaning |
|---|---|---|
| `jobs[3]` (3 rows) | `IndexError` | no such **position** |
| `jobs["grade"]` | `TypeError` | a list needs a number, not text |
| `jobs[0]["salary"]` | `KeyError` | no such **key** in that row |

- `[1]` is a position, never a value inside the row.

</details>

<details>
<summary>Functions: return vs print, apply once</summary>

```python
def annual_premium(monthly: int) -> int:
    return monthly * 12           # hands the value back

premiums = []
for monthly in [650, 480, 75]:
    premiums.append(annual_premium(monthly))   # [7800, 5760, 900]
```

- `print` shows a value and hands back `None`: a card visual. `return` hands it back: a measure.
- `annual_premium(monthly * 12)` multiplies twice (93,600). Transform once.

</details>

<details>
<summary>pandas: quick checks</summary>

```python
df.shape                                            # (rows, columns)
df.dtypes                                           # ignore the last "dtype: object" line
df["effective"] = pd.to_datetime(df["effective"])   # str → datetime64[us]
df["annual_premium"] = df["monthly_premium"] * 12   # vectorized: no loop
print(df.to_csv(index=False))                       # preview the CSV text
```

- pandas 3 calls text columns `str` (older notes say `object`).

</details>

<details>
<summary>Gotchas</summary>

- Check **which file** you're typing in before writing practice code.
- Paste into the REPL with **right-click**, not Ctrl+V (`U+0016`).
- Grey ghost text = AI autocomplete. Press **Esc** during practice.
- A box marked `text` is a diagram, not a command.

</details>

</details>

<details>
<summary><b>Review 1 · Nov 25 · PR reviews (#30, #31) and a fix (#33)</b></summary>

<details>
<summary>Look at a PR before merging</summary>

```powershell
gh pr view 30                                  # description, linked issue
gh pr diff 30                                  # every changed line
gh pr checks 30                                # did CI pass?
git fetch                                      # get GitHub's latest first
python scripts/public_scan.py --base origin/main   # the same scan CI runs
```

Then run `/review` in a **new chat**, so the review isn't done by the chat that built the code.

</details>

<details>
<summary>A fix found after the PR merged</summary>

```powershell
git switch -c fix/short-name origin/main       # new branch from the latest main; uncommitted edits come along
git add path/one.py path/two.py                # name the files
git commit -m "What the fix does"
git push -u origin fix/short-name
gh pr create --base main --title "..." --body "..."
```

- The old PR is closed. Commits on its branch won't reach `main`.
- `switch -c` refuses if `main` changed the same files. That's Git protecting your edits.

</details>

<details>
<summary>Delete a branch after a squash merge</summary>

```powershell
git diff fix/short-name origin/main -- path/one.py   # nothing printed = main has it all
git branch -D fix/short-name                         # -d would refuse after a squash
git push origin --delete fix/short-name              # the GitHub copy
```

</details>

<details>
<summary>Worktrees</summary>

```powershell
git worktree list                              # every working folder and its branch
cd <worktree folder>                           # commit a worktree's branch from inside it
```

A branch checked out in a worktree can't be switched to anywhere else.

</details>

<details>
<summary>Left join: on vs where</summary>

```sql
-- keeps all employees; no match = NULL department
from employees as e
left join hr_assignment as a
    on a.employee_id = e.employee_id
   and date '2026-06-30' between a.effective_start and a.effective_end
```

The same date check in `where` drops the unmatched employees, so the left join acts like an inner join.

</details>

<details>
<summary>Gotchas</summary>

- Two saves at once can erase each other (a race). A lock makes them take turns.
- Before deleting a branch, check its PR is merged **and** its contents are on `main`.

</details>

</details>
