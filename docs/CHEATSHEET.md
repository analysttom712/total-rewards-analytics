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
git switch -c <issue#>-<short-name>  # new branch, e.g. 1-job-catalog
```

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
```

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

## Gotchas I've hit

- Terminal vs. editor vs. GitHub website: know which one you're in.
- File not saved, or saved in the wrong folder → the script runs old code or "file not found".
- `.gitkeep` only exists so Git tracks an empty folder. It has nothing to do with branches.
