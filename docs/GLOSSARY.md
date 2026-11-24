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
| **seed** | A starting number that makes "random" output repeat exactly. | A saved filter state you can reapply. |
| **deterministic** | Same input → same output, every time. | A refresh that always ties out. |

</details>

<details>
<summary><b>pandas</b></summary>

| Term | Plain English | Like… |
|---|---|---|
| **DataFrame** | A table in Python. | A Power Query table; an R tibble. |
| **column** / **Series** | One column of a DataFrame. | A column. |
| **index** | Row labels pandas adds (0, 1, 2…). Not a data column. | The row numbers in the Power Query preview. |
| **dtype** | A column's data type: `int64`, `str`, `datetime64`, `object`. | The ABC/123/calendar icon on a column header. |
| **`object` dtype** | "Type unknown" / mixed. Needs a type step. | ABC123 (Any). |
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
| **amend** | Rewrite the last commit (only before pushing). | Correcting an unposted entry. |
| **`git restore`** | Throw away uncommitted edits to a file; back to the last commit. | Undo to last save. |

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

</details>
