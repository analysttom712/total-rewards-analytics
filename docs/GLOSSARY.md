# Glossary

Every symbol and term I've met, with its **real name**, what it does, and what it's like in work I already know. Added to at each `/wrap`. Open in VS Code preview (Ctrl+Shift+V) and click a section.

<details>
<summary><b>Python symbols</b></summary>

| Symbol | Real name | What it does | Like… |
|---|---|---|---|
| `"text"` or `'text'` | **string literal** (the quotes are **delimiters**) | Marks the characters between them as **text data**, not a name or a command. `"salary"` is the word salary; `salary` (no quotes) is a variable holding a number. Single and double quotes do the same thing; pick one style (ruff format uses `"`). | Excel: `="Total"` shows the word Total; `=Total` looks up a named range called Total. Power Query: `"Text"` vs a step name. |
| `"it's"` / `'say "hi"'` | mixing quote types | Use the other kind of quote when the text contains a quote. | Same as needing `""` inside an Excel text formula. |
| `"""..."""` | **triple-quoted string**; as the first line of a file or function it's a **docstring** | Text that can span lines. A docstring is the built-in description that tools and `help()` read. | The description field on a Power BI measure. |
| `f"Job: {title}"` | **f-string** (formatted string literal) | Text with `{placeholders}` filled in from variables when it runs. `{salary:,}` adds thousands separators. | Mail merge; Excel `="Job: "&A2`; DAX `FORMAT()`. |
| `#` | **comment** | Everything after it on the line is ignored by Python; notes for humans. | `//` in M, `--` in SQL. |
| `=` | **assignment** | Stores the value on the right in the name on the left. Not "equals". | Naming a step in Power Query. |
| `==` | **equality comparison** | Asks "are these equal?", answers `True`/`False`. | `=` inside an Excel `IF()`. |
| `( )` | **parentheses / call** | After a name, *runs* it: `df.head()`. Also groups math and holds a function's parameters. | Invoking a custom function. |
| `[ ]` | **brackets**: list literal or **subscript** | `[1, 2]` makes a list; `x[0]` / `row["grade"]` looks something up inside `x`. | Power Query `{0}` (row) and `[Column]` (field). |
| `{ }` | **braces**: dict literal | `{"grade": 4}` makes a dict (key: value pairs). Inside f-strings, marks a placeholder. | A Power Query record `[grade = 4]`. |
| `:` | colon | Ends a line that starts a block (`def`, `for`) and separates key: value in a dict, or name: type in a type hint. | — |
| indentation (4 spaces) | **block** | Lines indented under `def`/`for` belong to it. Python uses indentation where R uses `{ }`. | Nested steps inside a `let`. |
| `->` | **return annotation** | In `def f(x: int) -> dict:`, says what type the function hands back. | The output data type of a custom function. |
| `.` | **attribute access** | `df.shape`, `fake.first_name()`: "the thing that belongs to". | `Table.RowCount(...)` style namespacing. |
| `,` (trailing) | **trailing comma** | Allowed after the last item; makes adding the next item a one-line change. | — |
| `>>>` / `...` | **REPL prompt** / **continuation prompt** | `>>>` waits for a new line of Python. `...` means "this block isn't finished": press Enter on an empty `...` line to run it. | A formula bar waiting for Enter. |
| `x = f(...)` vs `f(...)` | **assignment** vs **call** | `annual_premium = (...)` *stores* a value under that name; `annual_premium(monthly)` *runs* the function. Inside `append( )` you want the call. | Naming a step vs invoking a function. |
| `:=` | **walrus operator** (assignment expression) | Assigns *and* returns a value in one go. Seen once from autocomplete; not needed yet. | — |
| `a <= b <= c` | **chained comparison** | `True` only when `b` is between `a` and `c`, ends included. `100000 <= 104572 <= 125000` → `True`. | SQL `BETWEEN`; "is this salary inside the band?" |
| `assert` | **assert statement** | `assert <something true>`: does nothing if it's `True`, stops with `AssertionError` if it's `False`. The check inside every pytest test. | A tie-out that must equal zero, or the recon fails. |
| `x,` (stray) | **accidental tuple** | A trailing comma after a single value makes a tuple (a fixed list): `d = date(...),` stores `(date,)`, not a date. | — |

</details>

<details>
<summary><b>Python concepts</b></summary>

| Term | Plain English | Like… |
|---|---|---|
| **variable** | A name that points at a value. | A named cell / Power Query step name. |
| **data type** (`int`, `str`, `float`, `bool`) | What kind of value: whole number, text, decimal, true/false. | Power Query column types. |
| **list** | Ordered collection, looked up by position from 0. | A Power Query list `{a, b, c}`; R vector. |
| **dict** (dictionary) | Key → value pairs, looked up by name. | A Power Query record; one row of a table. |
| **list of dicts** | Rows with named fields: a table. | A table built from records. |
| **index / position** | Where an item sits; first is `0`, last is `-1`. | Row number (zero-based). |
| **function** | A reusable recipe: inputs in, result out. | Power Query custom function; R `function()`. |
| **parameter** vs **argument** | Parameter = the placeholder name in `def f(employee_id)`; argument = the actual value you pass, `f(100001)`. | The column you invoke a function *on* vs the value in that row. |
| **return value** | What a function hands back with `return`. No `return` → `None`. | The output of a custom function. R returns the last line automatically; Python doesn't. |
| **type hint** | A label saying what type a parameter or return should be. Not enforced at run time; tools read it. | Setting a parameter's type in a Power Query function. |
| **scope** | Where a variable can be seen. Variables made inside a function only exist inside it. | Steps inside one query's `let` aren't visible to another query. |
| **loop** (`for`) | Repeat the indented lines once per item. | `List.Generate`; filling a formula down. |
| **`range(a, b)`** | Numbers from `a` up to **but not including** `b`. Count = `b − a`. | An exclusive pay-period cutoff date. |
| **method** | A function that belongs to an object: `employees.append(...)`. | — |
| **module** | A `.py` file you can import from. | A shared query you reference. |
| **package** | A folder of modules, or something installed with `pip`. | An add-in. |
| **import** | Bring code from a module into this file. | `source("x.R")`; referencing another query. |
| **standard library** | Modules built into Python (e.g. `pathlib`); nothing to install. | Built-in Excel functions. |
| **third-party package** | Installed with `pip` from `requirements.txt` (pandas, Faker). | A custom visual from AppSource. |
| **`None`** | Python's "no value". | `null` in M; blank in DAX. |
| **vectorized** | Math applied to a whole column at once: `df["monthly_premium"] * 12`. No loop. | A Power Query custom column; a DAX calculated column. |
| **`IndexError`** | Asked for a **position** that doesn't exist (`jobs[3]` in a 3-item list). | A row number past the end of the table. |
| **`KeyError`** | Asked a dict for a **key** it doesn't have (`row["salary"]`). | A column name that isn't in the table. |
| **`TypeError`** | The wrong **kind** of value for the operation (`jobs["grade"]`: a list needs a number, not text). | Text in a numeric column. |
| **seed** | A starting number that makes "random" output repeat exactly. | A saved filter state you can reapply. |
| **deterministic** | Same input → same output, every time. | A refresh that always ties out. |
| **`set`** | A collection that keeps only **distinct** values, in no order: `set([1, 2, 2])` → `{1, 2}`. | Power Query *Remove Duplicates*; DAX `DISTINCT`. |
| **`len()`** | **length**: how many items are in a list, set or dict. | `COUNTROWS`. |
| **uniqueness check** | `len(set(ids)) == len(ids)`: a duplicate makes the set shorter, so the check fails. | `DISTINCTCOUNT(id) = COUNTROWS(table)`. |
| **main guard** (`if __name__ == "__main__":`) | Code under it runs only when the file is run directly, not when it's imported. | A refresh button that only fires when you click it, not when another report references the query. |
| **import side effect** | Code at the top level of a module runs the moment the module is imported. | Opening a workbook that runs a macro on open. |
| **pytest** | The test runner: finds files named `test_*.py` and functions named `test_*`, runs them and reports passed / failed. | Running every recon check in the close checklist in one click. |
| **false pass** | A test that passes without checking anything, e.g. an `assert` inside an `if` that never matches. "Passed" checked nobody. | A Merge that matched zero rows: an empty exceptions tab that looks like a clean tie-out. |
| **break it on purpose** | Plant a bug to see the test fail, then remove it. The bug must change **only one side** of the check (the code, not the rule it's checked against). | Keying a test exception to prove the recon catches it. |

</details>

<details>
<summary><b>pandas</b></summary>

| Term | Plain English | Like… |
|---|---|---|
| **DataFrame** | A table in Python. | A Power Query table; an R tibble. |
| **column** / **Series** | One column of a DataFrame. | A column. |
| **index** | Row labels pandas adds (0, 1, 2…). Not a data column. | The row numbers in the Power Query preview. |
| **dtype** | A column's data type: `int64`, `str`, `datetime64`, `object`. | The ABC/123/calendar icon on a column header. |
| **`object` / `str` dtype** | Text, or "type unknown". pandas 3 labels text columns `str`; older pandas said `object`. Needs a type step if it should be a date or number. | ABC123 (Any) / ABC (Text). |
| **`datetime64[us]`** | A real date-time column. `[us]` = microsecond precision (µs). | The calendar icon on a Power Query column. |
| **`dtype: object`** (last line of `df.dtypes`) | Describes the printed list of type names itself, not your data. Ignore it. | A report footer. |
| **`pd.to_datetime`** | Convert a column to a date type. | "Changed Type" → Date. |
| **`df.head()` / `df.shape` / `df.dtypes`** | First 5 rows / (rows, columns) / each column's type. | Preview / row and column count / column types. |
| **CSV** | Comma-separated values: plain-text table, one row per line. | Excel's "CSV (Comma delimited)". |
| **delimiter** | The character that separates fields (`,` in a CSV). | The "Delimiter" setting in Power Query's CSV import. |
| **ISO 8601 date** | `YYYY-MM-DD`. Sorts correctly, unambiguous, every tool reads it. | Power BI Date data type (format is separate). |

</details>

<details>
<summary><b>Git and GitHub</b></summary>

| Term | Plain English | Like… |
|---|---|---|
| **repository (repo)** | A project folder plus its full history. | A workbook with every version kept. |
| **commit** | A saved snapshot with a message. | A posted journal entry. |
| **staging** (`git add`) | Choosing which changes go into the next commit. | Selecting entries for the next batch. |
| **branch** | A separate line of work; commits there don't touch `main`. | Your desktop copy of a PBIX while the published one stays put. |
| **`main`** | The trusted, shared version. | The published report. |
| **remote / `origin`** | The copy on GitHub. | SharePoint copy vs local copy. |
| **push** / **pull** | Send commits up / bring them down. | Upload / sync. |
| **pull request (PR)** | A request to merge a branch into `main`, with review. | Sending a reconciliation for review before posting. |
| **merge** | Combine a branch into `main`. | Posting after approval. |
| **issue** | A ticket: the ask, acceptance criteria, discussion. | A request in a ticketing system. |
| **closing keyword** | `Closes #12` in the PR body: closes issue 12 when the PR merges into the default branch. Also `Fixes`, `Resolves`. | A payment referencing an invoice number clears that invoice. |
| **`.gitignore`** | List of files Git should never track (venv, secrets, generated data). | An exclusion list. |
| **`.gitkeep`** | Empty placeholder file so Git tracks an empty folder (Git ignores empty folders). | — |
| **amend** (`git commit --amend`) | Replace the last commit with a corrected one (new message or files). It gets a **new commit ID**, so only amend before pushing. | Correcting an unposted entry: it gets a new entry number. |
| **`git restore`** | Throw away uncommitted edits to a file; back to the last commit. | Undo to last save. |
| **`git restore --staged`** | Take a file **out of the batch** (unstage). Edits are kept. | Pulling a timecard out of the approval batch. |
| **staged + modified** | `git add` takes a **snapshot**; edit again and the file shows in both sections. `git add` again to update. | The batch holds the old timecard after the employee corrects hours. |
| **working tree clean** | Every file matches the last commit; nothing to add or commit. | All entries posted. |
| **upstream** (`-u`) | The GitHub branch your local branch is linked to. After `push -u`, plain `git push` works. `[gone]` = its GitHub copy was deleted. | The SharePoint file your local copy syncs to. |
| **`HEAD`** | "The branch/commit I'm on right now." | "This workbook". |
| **squash merge** | Combine all of a PR's commits into one commit on `main`. | Posting a batch as one summarized entry. |
| **`git branch -d` vs `-D`** | `-d` deletes a branch only if its commits are in `main`'s history; after a squash merge they aren't, so it refuses. `-D` deletes anyway: compare the contents with `main` first. | Shredding a draft only after confirming the posted entry matches it. |
| **worktree** | A second working folder for the same repo, with a different branch checked out. A branch open in one worktree can't be switched to in another. | A second copy of the workbook open on another tab, locked to one version. |

</details>

<details>
<summary><b>Tools and terminal</b></summary>

| Term | Plain English | Like… |
|---|---|---|
| **terminal / shell** | A text window where you type commands. PowerShell is the Windows one. | — |
| **prompt** | The text before your cursor (`PS C:\...>`). | — |
| **virtual environment (venv)** | A project's own private copy of Python packages. `(.venv)` shows it's on. | A separate Power BI environment per client. |
| **linter** (`ruff check`) | Finds mistakes and style problems. | A formula error checker. |
| **formatter** (`ruff format`) | Rewrites layout to a standard style; doesn't change behavior. | Power Query's "Format" button. |
| **relative path** | A location measured from where you are (`data/raw/x.csv`). | "Two folders down from here". |
| **absolute path** | A full location from the drive (`C:\...`). Avoid in a public repo (shows your username). | A full UNC path. |
| **extension** (VS Code) | An add-on, e.g. Rainbow CSV. | An Excel add-in. |
| **`cd`** | **change directory**: move the terminal to another folder. Git acts on the repo you're standing in. | Opening a different folder in File Explorer. |
| **`CommandNotFoundException`** | PowerShell read the first word as a command and found none by that name. | Keying a pay code that doesn't exist. |
| **LF / CRLF** | Invisible end-of-line characters: LF (Linux/Mac) vs CRLF (Windows). Git's warning about converting them is harmless. | `2026-11-24` vs `11/24/2026`: same date, different format. |
| **`U+0016`** | The invisible code Ctrl+V sends. Some REPLs take it as text → `SyntaxError`. Paste with right-click instead. | — |
| **inline suggestions** | VS Code's AI autocomplete (grey ghost text, Tab accepts). Turn off for practice. | Autofill guessing the wrong formula. |
| **unsaved changes** (white dot on a tab) | Edits that exist only in the editor, not on disk. Git and pytest can't see them. Close the tab and choose **Don't Save** to drop them; once saved, use `git restore`. | Power Query edits you haven't clicked *Close & Apply* on. |
| **`>>` prompt** (PowerShell) | **continuation prompt**: PowerShell thinks the command isn't finished, usually an unclosed quote. Ctrl+C cancels. | A formula bar waiting for the closing bracket. |

</details>

<details>
<summary><b>Data engineering ideas</b></summary>

| Term | Plain English | Like… |
|---|---|---|
| **reproducible** | Anyone can regenerate the same output from code + seed. | A refresh that always ties out. |
| **generated data** | Output made by code; not committed (code is the source). | A report export; you keep the PBIX, not every export. |
| **raw zone** | Where source files land unchanged. | The untouched source extract. |
| **grain** | What one row represents ("one row per employee"). | The granularity of a fact table. |
| **range inversion** | A lower grade paying more than a higher one. | A comp structure red flag. |
| **thread** | One line of work inside a running program. A web server often gives each request its own thread, so two can run at the same moment. | Two payroll clerks working the same batch at once. |
| **race condition / lost update** | Two threads read the same old data, change it and write it back; the last write erases the first one's change. | Two people editing the same workbook; whoever saves last wins. |
| **lock** (`threading.Lock`) | Makes threads take turns: only one may run the locked steps at a time; the others wait. | Checking out a shared file so nobody else can edit it until you check it in. |
| **golden value** | An expected answer worked out by hand and typed into a test, not recomputed by the same formula. | Tying a report to a control total from another system. |
| **`on` vs `where` (left join)** | A condition in `on` decides which rows *match*; unmatched rows stay, with NULLs. The same condition in `where` filters *after* the join and drops them. | A Power Query left merge vs filtering the merged column afterwards. |
| **constant** (`AS_OF`, `JOBS`) | A name set once at the top of a module and never reassigned. `ALL_CAPS` is a promise to the reader; Python doesn't enforce it. | The "Period end" parameter on a report's cover page: change it in one place and the whole report follows. |
| **`datetime.date`** (`date(2026, 11, 1)`) | A real calendar date value from the built-in `datetime` module, built as year, month, day. `date(2026, 31, 12)` raises `ValueError: month must be in 1..12`. | Power Query `#date(2026, 11, 1)`: a date value, not the text "2026-11-01". |
| **as-of date** | The fixed date a dataset or report is run for. Nothing reads today's clock. | A payroll register run "as of 10/31", which ties out no matter when it's re-run. |
| **file hash** (`Get-FileHash`, SHA-256) | A 64-character fingerprint of a file's exact bytes. One changed character gives a completely different hash. | A control total that's sensitive to every comma, not just the amounts. |
| **slice** (`items[1:25]`) | Takes a range of positions and returns a **list**, even if it's empty. `items[0]` returns one item. | Filtering a table to rows 2–25 vs picking one row. |
| **`timedelta`** (`timedelta(days=1)`) | A length of time you can add to a date. `date + 1` is a `TypeError`. | Adding "30 days" to an effective date, not just the number 30. |
| **`ModuleNotFoundError`** | Python can't find a package. If the package is installed, usually the venv isn't active. | Opening a report on a machine without the connector installed. |
| **`NameError`** | Python looked for a variable with that name and found none. Often means missing quotes: `first[hire_date]` vs `first["hire_date"]`. | A DAX measure referencing a column that doesn't exist. |

</details>
