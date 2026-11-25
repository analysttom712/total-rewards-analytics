# SQL practice set (Phase 2)

Answered business questions, written by Thomas, run in DuckDB against the raw tables the generator writes. Milestone **M2** is 20 of these, each with the business question, the SQL and the expected result. The tickets that produce them are drafted in [`docs/backlog/phase-2.md`](../../docs/backlog/phase-2.md).

Scaffolding only: the folder, this README and [`_template.sql`](_template.sql). Every query in here is Thomas's own work.

## One file per question

```text
sql/practice/
  _template.sql                 copy this for every new question
  001_job_pay_ranges.sql        P2-01  (test: tests/test_sql_practice_001.py)
  002_headcount_by_dept.sql     P2-02
  ...
  020_payroll_vs_gl.sql         P2-10
```

- **Name:** three-digit number, then what it answers, in snake_case. The number is the order you wrote it, so the folder reads like a course.
- **Header comment:** the business question in the manager's words, the grain ("one row per ..."), the source tables, the as-of date if there is one, and the expected result.
- **Expected result:** filled in *after* you run the query and check it another way (a hand count, a second query, the answer key). Write down how you checked it. This is the same habit as noting the tie-out on a reconciliation before you sign it.

## How to run one

From the repo root, with the venv active (`.venv\Scripts\Activate.ps1`):

```powershell
python -c "import duckdb; print(duckdb.connect('warehouse/northwind.duckdb').sql(open('sql/practice/002_headcount_by_dept.sql').read()))"
```

P2-02 builds `warehouse/northwind.duckdb`; until then, P2-01 runs only through its test (`python -m pytest tests/test_sql_practice_001.py`), which loads the job catalog into an in-memory database.

The DuckDB command-line tool or the VS Code SQL extensions are nicer for exploring. Choosing one is part of P2-02.

## Style (what employers expect)

- Lowercase keywords, snake_case names, one CTE per logical step, explicit `join ... on` (never a comma join).
- Say the grain before you write the query. After every join, check the row count did what you expected.
- No `select *` in a finished answer: list the columns the manager asked for.

These are the same conventions the dbt models will use in Phase 3, so the practice queries turn into staging and mart models with little rewriting.
