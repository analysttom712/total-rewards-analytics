# Cheatsheet

Commands and patterns I've used so far, grouped by when I need them. Updated at each `/wrap`.

---

## Start of session

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

## Work on a ticket (GitHub flow)

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

## Run and check code

```powershell
python generator/hello_employee.py   # run a script
ruff check generator                 # lint; fix anything it reports
ruff check generator --fix           # let ruff fix the simple ones (e.g. import order)
pip install -r requirements.txt      # install packages listed in requirements
```

## Ship it

```powershell
git status                           # check: no secrets, no data files, right files only
git add <file>                       # stage (or `git add .` after checking status)
git commit -m "Short description of what changed"
git push -u origin <branch-name>     # first push of a new branch
gh pr create                         # open the PR; body includes "Closes #N"
gh pr edit <N> --body "Closes #1. ..."   # add/fix the PR body after the fact
gh pr merge <N> --merge --delete-branch  # merge and clean up the branch
```

- `gh pr create --fill` copies the commit message as the title and leaves the **body empty**, so there's no `Closes #N`. Add it.

- `Closes #N` in the PR links the PR to the ticket and closes the ticket when the PR merges, so anyone can trace why a change was made.
- Fix the last commit message (before pushing): `git commit --amend`

---

## Python basics

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

## Faker and seeds

```python
from faker import Faker
Faker.seed(42)       # same seed → same fake data every run
fake = Faker()
fake.first_name(), fake.last_name()
fake.date_between(start_date="-10y", end_date="today")
```

Faker also has `random_element` and `random_int`. Look them up when the ticket needs them.

## Reading errors

- Read **bottom-up**. The last line is the error type and reason, e.g. `IndexError: ...`.
- Above it are the file and line number where the error happened.
- `NameError: name 'x' is not defined` → the variable doesn't exist (typo, or renamed in one place only).
- `ImportError: cannot import name 'X'` → the file was found but has no `X` in it.
- ruff `F401` = imported but unused (finish the code; don't `--fix` away an import you're about to use).
- ruff `F821` = undefined name (same as NameError, caught before running).
- git `pathspec ... did not match any files` → that file doesn't exist (not created/saved, or misspelled).
- git `a branch named 'x' already exists` → drop the `-c`.

## Gotchas I've hit

- Terminal vs. editor vs. GitHub website: know which one you're in.
- File not saved, or saved in the wrong folder → the script runs old code or "file not found".
- `.gitkeep` only exists so Git tracks an empty folder. It has nothing to do with branches.
- A passing `ruff check` on an empty file proves nothing: check that the file has content (size 0 = not saved).
- Rename a variable everywhere: click it in VS Code, press **F2**, type the new name.
