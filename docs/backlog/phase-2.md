# Phase 2 ticket drafts: SQL for analytics engineering (DuckDB)

**Status: drafts.** None of these are GitHub issues yet. Thomas approves them in the PR, then they're created with `gh issue create` a few at a time (CLAUDE.md section 4 keeps 3–5 ready). IDs like `P2-03` become real issue numbers then.

Read [`README.md`](README.md) in this folder for the ID scheme and the generator tables each ticket waits on. Lesson outlines (concept, analogy, hint ladder, resources) are in [`lessons-phase-2-4.md`](lessons-phase-2-4.md).

**Phase goal (M2):** 20 practice queries in `sql/practice/`, each with the business question, the SQL and the expected result. **Check:** explain an as-of join and a window-function dedupe without notes.

| ID | Title | Queries | Blocked by | Est. |
|---|---|---|---|---|
| P2-01 | First DuckDB query: the published pay ranges | 001 | none (test-first check ready) | 1 |
| P2-02 | Load the raw files into a local warehouse; headcount by department | 002–003 | #14, #13, #19 | 1–2 |
| P2-03 | Joins and fan-out: who's missing a department, and why counts double | 004–006 | P2-02 | 1–2 |
| P2-04 | CASE and CTEs: who's below minimum or above maximum (today) | 007–008 | P2-02 | 1 |
| P2-05 | Window functions I: rank, top-N per group, running totals | 009–011 | P2-02 | 1–2 |
| P2-06 | Effective dating: compa-ratio by employee as of a date | 012–013 | G-comp | 2 |
| P2-07 | Window functions II: merit increase % by department (LAG) | 014–015 | P2-06, G-merit | 1–2 |
| P2-08 | Messy IDs, dedupe and set operations: carrier members not in HR | 016–017 | G-benefits | 2 |
| P2-09 | Conditional aggregation: gross-to-net for one pay period | 018 | G-payroll | 1 |
| P2-10 | Nulls, tie-outs and query plans: payroll vs GL by period | 019–020 | P2-09, G-gl | 1–2 |

Labels on every Phase 2 ticket: `phase-2`, `sql`. Extra labels are listed per ticket.

---

## P2-01 · First DuckDB query: the published pay ranges

**Labels:** `phase-2`, `sql`, `cert:PL-300`
**Blocked by:** nothing. Uses only `generator/job_catalog.py`, which is already merged. Can start in parallel with the Phase 1 tickets.
**Test-first check:** `tests/test_sql_practice_001.py` (skipped until the ticket starts).

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> Before anyone asks me where people sit in their ranges, I need the ranges themselves on one page: every job, its grade, the minimum, the midpoint and the maximum, and how wide each range is as a percent. Highest grade first, because that's how the comp committee reads it.

### Acceptance criteria
- [ ] Delete the `pytestmark = pytest.mark.skip(...)` line in `tests/test_sql_practice_001.py`, run `python -m pytest`, and say in the PR what the failure told you
- [ ] `sql/practice/001_job_pay_ranges.sql` copied from `_template.sql`, header filled in (question, grain, source table, expected result)
- [ ] The query returns one row per job with `job_code`, `job_title`, `grade`, `salary_min`, `range_midpoint`, `salary_max`, `range_spread_pct` (spread as a percent of the minimum, one decimal), highest grade first
- [ ] Before running the test, predict the Total Rewards Manager midpoint and the Compensation Analyst spread by hand; note the prediction in the header
- [ ] `python -m pytest` green with the test un-skipped; `ruff check` passes; PR with `Closes #N`

### Learning objective
- `select`, computed columns and aliases, arithmetic and `round`, `order by`; integer vs decimal division (predict first)
- DuckDB as an in-process database: no server, the same idea as Power BI's in-memory engine
- Reading a test that states a business expectation, then making it pass (the dbt test habit, early)
- **Cert:** PL-300 "Prepare the data" (profile and shape data). Range midpoint and spread are standard comp vocabulary.

### Estimate
1 session.

---

## P2-02 · Load the raw files into a local warehouse; headcount by department

**Labels:** `phase-2`, `sql`, `python`
**Blocked by:** #14 (`python -m generator` writes the raw files), #13 (`hr_org` and `department_code` on employees), #19 (fixed `AS_OF` date so counts don't drift between runs)

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> I keep getting headcount from three places and they never match. I want one place the raw HR files land, loaded exactly as delivered, and one headcount-by-department number I can trust because I can see how it was counted.

### Acceptance criteria
- [ ] A small, re-runnable load step (a Python script or a `.sql` file run by Python; your choice, explained in the PR) that creates `warehouse/northwind.duckdb` and loads every CSV in `data/raw/` into a table of the same name. Running it twice gives the same result (no doubled rows)
- [ ] The job catalog is loaded too, as table `hr_job`, from `generator/job_catalog.py` (ADR-001: the generator doesn't write it as a file yet). P2-03 and P2-04 need it for the salary ranges
- [ ] For each table, the loaded row count matches the CSV's row count; print both
- [ ] `002_headcount_by_dept.sql`: active headcount by department, largest first, with a total row or a check that the departments sum to the total
- [ ] `003_hires_by_year.sql`: hires per calendar year, using a date function on `hire_date`
- [ ] Each file's header has its expected result and how you checked it
- [ ] `warehouse/northwind.duckdb` does **not** appear in `git status` (confirm it's ignored); PR with `Closes #N`

### Test ideas (write when the data exists; Thomas or Claude, test-first)
- After the load, every table in `data/raw/` exists in the warehouse with the same row count as its CSV
- Running the load twice leaves row counts unchanged (idempotent: the word to learn here)
- Headcount by department sums to total active headcount

### Learning objective
- `create table ... as select`, DuckDB's CSV reader and type detection (compare to Power Query's "Changed Type" step it adds automatically)
- `group by`, `count(*)` vs `count(column)`, `having`; date parts (`year(...)`, `date_trunc`)
- Idempotent loads: why "run it twice, get the same answer" matters for every pipeline
- **Cert:** PL-300 "Prepare the data" (get data from sources, resolve data import errors)

### Estimate
1–2 sessions.

---

## P2-03 · Joins and fan-out: who's missing a department, and why counts double

**Labels:** `phase-2`, `sql`, `cert:PL-300`
**Blocked by:** P2-02

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> Last month a department cost report showed 40 more people than we employ. Someone joined two tables and nobody checked the count. I want three things: payroll cost by department that ties to total payroll, a list of anyone with no department or a department code that doesn't exist, and a short note showing how the bad report could have happened.

### Acceptance criteria
- [ ] `004_salary_cost_by_dept.sql`: employees joined to `hr_org` and the job catalog; total annual salary by department. The department totals sum to the company total (show the check)
- [ ] `005_employees_without_valid_dept.sql`: employees whose department is missing or not in `hr_org` (a left join + filter, or an anti join; try both and say which you'd keep)
- [ ] `006_fanout_demo.sql`: on purpose, join to a table where the key isn't unique and show the row count jump; then fix it. Header explains the cause in one sentence
- [ ] Before each join, write the expected row count in the header; after, compare
- [ ] PR with `Closes #N`

### Test ideas
- Department salary totals sum to the company salary total (a tie-out test: the dbt `equal_rowcount` / reconciliation idea)
- `005` returns zero rows on clean data; plant one bad department code and it returns exactly one

### Learning objective
- Inner, left, full and anti joins (`anti join` / `not exists`); one-to-many vs many-to-many; join fan-out
- Grain: "one row per what?" before and after every join
- **Cert:** PL-300 "Model the data" (relationships, cardinality: the same one-to-many idea as a Power BI relationship)

### Estimate
1–2 sessions.

---

## P2-04 · CASE and CTEs: who's below minimum or above maximum (today)

**Labels:** `phase-2`, `sql`
**Blocked by:** P2-02 (uses current salary on the employee file plus the job catalog; the effective-dated version is P2-06)

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> The comp committee wants a list of everyone paid below their range minimum or above their maximum, and a count of how many are in each bucket. Show me where each person sits in the range, too, so I can see who's close to the edge.

### Acceptance criteria
- [ ] `007_range_position.sql`: one row per employee with salary, min, max, a `range_status` of `below_min` / `in_range` / `above_max`, and range penetration (where in the range the salary sits, 0% at min, 100% at max). Written as a chain of CTEs, one step each
- [ ] `008_range_status_summary.sql`: count and total salary by `range_status`
- [ ] Explain in the PR what happens at exactly the minimum and exactly the maximum, and which bucket those people land in
- [ ] PR with `Closes #N`

### Test ideas
- Every employee lands in exactly one bucket (bucket counts sum to headcount)
- A salary equal to `salary_min` is `in_range`; one dollar below is `below_min` (boundary test with two hand-made rows)
- Penetration is 0 at the minimum and 100 at the maximum

### Learning objective
- `case when` (compare to a DAX `SWITCH(TRUE(), ...)` or a Power Query conditional column)
- CTEs as named steps (compare to Power Query's applied steps; each CTE is one step you can inspect)
- Boundary conditions: `<` vs `<=` at range edges
- **Cert:** PL-300 "Prepare the data" (conditional columns)

### Estimate
1 session.

---

## P2-05 · Window functions I: rank, top-N per group, running totals

**Labels:** `phase-2`, `sql`
**Blocked by:** P2-02

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> Three quick ones for the department heads: the three highest-paid people in each department, each person's salary as a percent of their department's total, and a running count of hires by month so I can see when we grew.

### Acceptance criteria
- [ ] `009_top3_salary_by_dept.sql`: top three per department, with ties handled on purpose (say which ranking function and why)
- [ ] `010_salary_share_of_dept.sql`: each person's salary and their share of the department total, **without** a `group by` subquery
- [ ] `011_running_hires_by_month.sql`: hires per month and a running total
- [ ] For `009`, show what changes if you swap the ranking function for one of the other two
- [ ] PR with `Closes #N`

### Test ideas
- `009` returns at most 3 rows per department, or more only when there's a tie, matching the ranking function chosen
- Shares in `010` sum to 100% per department
- The last running total in `011` equals total hires

### Learning objective
- `over (partition by ... order by ...)`; `row_number`, `rank`, `dense_rank`; `sum() over`; `qualify`
- Window vs `group by`: a window keeps every row (compare to a DAX measure using `ALLEXCEPT` vs a summarized table)
- **Cert:** dbt Analytics Engineering (SQL fluency is assumed throughout); PL-300 analogues in DAX `RANKX`

### Estimate
1–2 sessions.

---

## P2-06 · Effective dating: compa-ratio by employee as of a date

**Labels:** `phase-2`, `sql`, `cert:PL-300`
**Blocked by:** G-comp: generator tables `comp_salary` (effective-dated salary history), `comp_grade_ranges` (min/mid/max by grade and year) and `hr_assignment` (job and department history). No generator ticket exists for these yet.

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> Auditors asked where everyone sat in their range **on June 30**, not today. People have changed jobs and had raises since then, and ranges are updated every January. I need compa-ratio for every employee who was active on that date, using the salary, job and range that were in effect on that date.

### Acceptance criteria
- [ ] `012_compa_ratio_as_of.sql`: one row per employee active on the as-of date, with the salary, grade and range midpoint in effect that day, and compa-ratio (salary ÷ midpoint). The as-of date appears in exactly one place in the query
- [ ] Row count equals active headcount on that date (checked with a separate query). No one appears twice
- [ ] `013_compa_ratio_as_of_asof_join.sql`: the same answer using DuckDB's `asof join`; both files return identical results (show the check)
- [ ] Explain in the PR how an open end date (`9999-12-31`) and an effective date equal to the as-of date are handled
- [ ] PR with `Closes #N`

### Test ideas
- Change the as-of date to the day before a known raise: the old salary appears; the day of the raise: the new one
- No employee has more than one row for a given as-of date (the grain test)
- An employee terminated before the as-of date does not appear; one hired on the as-of date does
- `012` and `013` return identical rows

### Learning objective
- Effective dating: `effective_start <= as_of and as_of < effective_end` (or `<=`; pick and defend), open end dates
- The as-of join, two ways: range join and DuckDB `asof join`
- This is HCM effective dating turned into SQL, and the pattern behind dbt's `as_of_filter` macro (P3-04) and SCD Type 2 (P3-05)
- **Cert:** PL-300 (point-in-time analysis concepts); dbt Analytics Engineering (snapshots build on this)

### Estimate
2 sessions. Split if the first session ends before `012` is right.

---

## P2-07 · Window functions II: merit increase % by department (LAG)

**Labels:** `phase-2`, `sql`
**Blocked by:** P2-06; G-merit: generator table `comp_merit_cycle` (or merit-reason rows in `comp_salary`)

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> The merit cycle closed. The CFO wants average merit increase percent by department, and I want to make sure promotions aren't hiding inside the merit numbers.

### Acceptance criteria
- [ ] `014_salary_change_history.sql`: each salary row with the previous salary and the percent change, per employee, in date order
- [ ] `015_merit_pct_by_dept.sql`: average and median merit increase percent by department for the cycle, merit changes only (promotions excluded, with the rule stated in the header)
- [ ] An employee's first salary row has no previous salary: show how you handled it and why
- [ ] PR with `Closes #N`

### Test ideas
- The first salary row per employee has a null previous salary, not zero
- An employee with one merit increase of 3% shows 3.0 (golden value from the generator once it exists)
- Promotion rows never appear in `015`

### Learning objective
- `lag` / `lead`, partitioning by employee, ordering by effective date; percent change; average vs median
- **Cert:** PL-300 analogue: time-intelligence comparisons (previous value)

### Estimate
1–2 sessions.

---

## P2-08 · Messy IDs, dedupe and set operations: carrier members not in HR

**Labels:** `phase-2`, `sql`
**Blocked by:** G-benefits: generator tables `hr_dependents`, `benefit_elections` and `carrier_eligibility_file_a` with the planted anomalies (duplicate carrier rows, leading zeros and spaces in IDs, a terminated member still billed)

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> The carrier billed us for people I don't recognize. Their file has duplicates and their IDs don't look like ours. Give me a clean list of carrier members we can't find in HR, and the reverse: people we cover who aren't on their file.

### Acceptance criteria
- [ ] `016_carrier_members_deduped.sql`: carrier rows with IDs cleaned (trim, consistent zero-padding) and duplicates removed, keeping one row per member by a rule you state (e.g. latest file row)
- [ ] `017_carrier_vs_hr_exceptions.sql`: members on the carrier file but not in HR, and covered in HR but not on the carrier file, with a `reason_code` column (`not_in_hr`, `not_on_carrier`)
- [ ] Do it once with `except` and once with an anti join; note which one keeps the columns you need for the exceptions list
- [ ] Each planted carrier anomaly from `_answer_key.csv` shows up in your output (list them in the PR)
- [ ] PR with `Closes #N`

### Test ideas
- After dedupe, the member key is unique
- `'  000123'`, `'123'` and `'000123'` all clean to the same ID
- Every carrier-related row in `_answer_key.csv` appears in `017`

### Learning objective
- String cleanup (`trim`, `lpad`, casting); dedupe with `row_number()` + `qualify`; `union` / `union all` / `except` / `intersect`; anti joins
- This is the carrier reconciliation done by hand today, as a query; it becomes `fct_carrier_reconciliation` in P3-08
- **Cert:** dbt Analytics Engineering (dedupe patterns, `unique` tests)

### Estimate
2 sessions.

---

## P2-09 · Conditional aggregation: gross-to-net for one pay period

**Labels:** `phase-2`, `sql`
**Blocked by:** G-payroll: generator tables `pay_periods`, `pay_codes` and `payroll_results`

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> Payroll asked us to check one pay period end to end: for each employee, gross pay, pre-tax deductions, taxes, post-tax deductions and net pay, side by side. Net has to equal gross minus everything else for every person.

### Acceptance criteria
- [ ] `018_gross_to_net_one_period.sql`: one row per employee for the chosen pay period, with a column per pay-code category, built from the long `payroll_results` table
- [ ] A check column (or a second query) proving net = gross − deductions − taxes for every row, with any exceptions listed
- [ ] PR with `Closes #N`

### Test ideas
- Net equals gross minus deductions minus taxes for every employee (zero exceptions on clean data)
- The sum of all category columns equals the sum of `payroll_results.amount` for the period (nothing dropped by the pivot)

### Learning objective
- Long-to-wide: `sum(case when ... then amount end)` and DuckDB `pivot` (compare to Power Query Pivot Column)
- **Cert:** PL-300 "Prepare the data" (pivot/unpivot)

### Estimate
1 session.

---

## P2-10 · Nulls, tie-outs and query plans: payroll vs GL by period

**Labels:** `phase-2`, `sql`
**Blocked by:** P2-09; G-gl: generator table `gl_postings` with the two planted out-of-balance periods

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> Finance says payroll and the general ledger don't tie in two periods. I need a period-by-period tie-out: payroll register total, GL total, difference, and a flag when the difference is more than a rounding cent. Some periods have no GL posting at all; those must show up, not disappear.

### Acceptance criteria
- [ ] `019_payroll_vs_gl_by_period.sql`: one row per pay period, payroll total, GL total, difference, `status` (`tied`, `rounding`, `out_of_balance`, `missing_gl`)
- [ ] A period with no GL rows appears with `missing_gl`, not dropped and not shown as tied
- [ ] Both planted periods from `_answer_key.csv` are flagged; say which is rounding and which is structural
- [ ] `020_query_plan.sql`: `explain analyze` on `019`, with three sentences in the header on what the plan shows (which join, where the time went)
- [ ] M2 check: 20 queries in `sql/practice/`, each with an expected result. Tick M2 in `docs/CURRICULUM.md`
- [ ] PR with `Closes #N`

### Test ideas
- Every pay period appears exactly once (row count = number of pay periods)
- The two planted periods are flagged and no others
- `null` amounts are treated as zero only where the business rule says so (state the rule)

### Learning objective
- Null handling: `coalesce`, `is null`, nulls in joins and aggregates, `null` vs `0`; full outer join for tie-outs
- Reading a query plan (`explain`, `explain analyze`)
- **Cert:** PL-300 (data-quality profiling); dbt Analytics Engineering (tie-out tests)

### Estimate
1–2 sessions.
