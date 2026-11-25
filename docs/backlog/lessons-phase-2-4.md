# Lesson outlines: Phases 2–4

One outline per ticket in [`phase-2.md`](phase-2.md), [`phase-3.md`](phase-3.md) and [`phase-4.md`](phase-4.md). `/standup` turns the day's outline into the lesson block, following [`docs/COACHING.md`](../COACHING.md): one concept at a time, show the data first, Thomas predicts before running, one hint rung per real attempt.

**What's here and what isn't.** Each outline has the concept, why it matters on the job, a Power BI / payroll analogy, a hint ladder and 2–3 resources. The ladder stops at **partial code with `____` blanks**; there are no full solutions anywhere in this file. Rung 3 is folded shut under "Show the partial code" (COACHING.md: one rung per real attempt, partial code last), so reading ahead takes a deliberate click. Phase 4 rungs stop at partial *steps* in words, because the DAX is Thomas's.

**Resources.** The top-level links (DuckDB, dbt, Power BI docs, cert pages) are in [`docs/RESOURCES.md`](../RESOURCES.md). The deeper links below are pages inside those same sites, each checked to load on 2026-11-25. The PR that adds this file proposes adding them to `RESOURCES.md` when each lesson is taught.

Analogy key, used throughout: Power Query step → staging model · DAX measure → mart column / semantic layer · manual reconciliation → dbt test · HCM effective dating → as-of join / SCD Type 2.

---

## Phase 2: SQL in DuckDB

### P2-01 · First DuckDB query: the published pay ranges
- **Concept:** `select` with computed columns and aliases; `order by`; `round`; integer vs decimal division.
- **Why on the job:** every comp question starts from the range table. Midpoint and spread are the first numbers a comp committee asks for.
- **Analogy:** a computed column is a Power Query "Add Column → Custom Column"; `order by` is sorting the table visual. The test is a recon check that states the expected totals before you build anything.
- **Hint ladder:**
  1. *Nudge:* "Which columns does the manager want that aren't in `hr_job` yet? Write each as a sentence in business words first."
  2. *Bigger hint:* "A new column is `<expression> as <name>` in the select list. The midpoint is halfway between two columns you already have. Spread compares the width of the range to its bottom."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     ```sql
     select
         job_code,
         job_title,
         grade,
         salary_min,
         ____ as range_midpoint,
         salary_max,
         round(____, 1) as range_spread_pct
     from hr_job
     order by ____
     ```

     </details>
- **Resources:** [DuckDB: SELECT](https://duckdb.org/docs/stable/sql/query_syntax/select) · [DuckDB Python API](https://duckdb.org/docs/stable/clients/python/overview) · [pytest: Get started](https://docs.pytest.org/en/stable/getting-started.html)

### P2-02 · Load the raw files into a local warehouse; headcount by department
- **Concept:** loading CSVs into a database file; type detection; `group by` and `count`; idempotent loads.
- **Why on the job:** the raw zone is "the files exactly as delivered". Every analytics engineer writes a load step that can be re-run without doubling data.
- **Analogy:** DuckDB's CSV reader guessing types = Power Query's automatic "Changed Type" step (and it can guess wrong in the same ways: leading zeros, dates). Re-running a load = refreshing a query, which replaces the data; it never appends a second copy.
- **Hint ladder:**
  1. *Nudge:* "What should happen to the table if it already exists when you run the load again? Say it in words."
  2. *Bigger hint:* "DuckDB can read a CSV straight inside a `select` with a reader function. `create or replace table` answers the re-run question."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     ```sql
     create or replace table ____ as
     select * from read_csv('data/raw/____.csv');
     ```
     and for headcount: `select ____, count(*) ... group by ____ order by ____ desc`.

     </details>
- **Resources:** [DuckDB: CSV import](https://duckdb.org/docs/stable/data/csv/overview) · [DuckDB: GROUP BY](https://duckdb.org/docs/stable/sql/query_syntax/groupby) · [DuckDB: date functions](https://duckdb.org/docs/stable/sql/functions/date)

### P2-03 · Joins and fan-out
- **Concept:** inner, left, full and anti joins; one-to-many vs many-to-many; fan-out; grain.
- **Why on the job:** the most common wrong number in reporting is a join that silently duplicates rows. "What's the grain?" is the first question in every analytics engineering interview.
- **Analogy:** Power Query Merge Queries (Left Outer, Inner, Left Anti are the same join kinds). Fan-out = a Power BI many-to-many relationship that inflates totals. A row-count check before and after = footing a report before you sign it.
- **Hint ladder:**
  1. *Nudge:* "Before joining, how many rows do you expect afterwards, and why? Write the number down."
  2. *Bigger hint:* "For 'missing department', keep every employee and look for the rows where the org side came back empty. For the fan-out demo, join to something with more than one row per key."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     ```sql
     select e.employee_id, e.department_code
     from employees as e
     left join hr_org as o
         on ____ = ____
     where ____ is null
     ```

     </details>
- **Resources:** [DuckDB: FROM and JOIN](https://duckdb.org/docs/stable/sql/query_syntax/from) · [Power BI: star schema guidance](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema)

### P2-04 · CASE and CTEs: below minimum or above maximum
- **Concept:** `case when` buckets; CTEs as named steps; boundary conditions.
- **Why on the job:** "who's out of range" is a standing comp-committee report; boundaries (exactly at the minimum) are where audits find mistakes.
- **Analogy:** `case` = Power Query conditional column or DAX `SWITCH(TRUE(), ...)`. Each CTE = one applied step you can click on and inspect.
- **Hint ladder:**
  1. *Nudge:* "List the three buckets and the rule for each in plain words, including what happens at exactly the min and exactly the max."
  2. *Bigger hint:* "First CTE: bring salary and the range together on one row. Second CTE: add the bucket. Final select: just the columns asked for. `case` checks conditions top to bottom and stops at the first true one."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     ```sql
     with salary_with_range as (
         select ____ from ____ join ____ on ____
     ),
     bucketed as (
         select *,
             case
                 when salary ____ salary_min then 'below_min'
                 when ____ then 'above_max'
                 else ____
             end as range_status
         from salary_with_range
     )
     select ____ from bucketed
     ```

     </details>
- **Resources:** [DuckDB: CASE](https://duckdb.org/docs/stable/sql/expressions/case) · [DuckDB: WITH (CTEs)](https://duckdb.org/docs/stable/sql/query_syntax/with)

### P2-05 · Window functions I
- **Concept:** `over (partition by … order by …)`; `row_number` / `rank` / `dense_rank`; `sum() over`; `qualify`.
- **Why on the job:** top-N per group, share of total and running totals come up weekly, and they're the most-asked SQL interview topic.
- **Analogy:** a window function = a DAX measure that looks at a group without collapsing rows (`RANKX`, `CALCULATE` with `ALLEXCEPT`). `group by` = Power Query "Group By", which does collapse rows.
- **Hint ladder:**
  1. *Nudge:* "Do you want one row per department, or one row per employee with department information next to it? That decides `group by` vs window."
  2. *Bigger hint:* "Partition = the group the calculation restarts in. Order = the order inside it. `qualify` filters on a window result the way `having` filters on an aggregate."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     ```sql
     select
         department_code, employee_id, salary,
         ____() over (partition by ____ order by ____ desc) as salary_rank
     from ____
     qualify salary_rank <= ____
     ```

     </details>
- **Resources:** [DuckDB: window functions](https://duckdb.org/docs/stable/sql/functions/window_functions) · [DuckDB: QUALIFY](https://duckdb.org/docs/stable/sql/query_syntax/qualify) · [Mode: SQL window functions tutorial](https://mode.com/sql-tutorial/sql-window-functions)

### P2-06 · Effective dating: compa-ratio as of a date
- **Concept:** effective-dated rows, open end dates (`9999-12-31`), range join on dates, DuckDB `asof join`.
- **Why on the job:** HCM data is effective-dated. Audits ask "as of June 30", and the wrong answer is usually "today's salary with June's headcount".
- **Analogy:** this *is* HCM effective dating, done in SQL. In Power BI terms: picking the row whose start/end dates bracket a slicer date. Payroll analogy: using the rate in effect on the pay date, not the rate today.
- **Hint ladder:**
  1. *Nudge:* "For one employee with three salary rows, which row was in effect on June 30? Write the rule that picks it, using the start and end dates."
  2. *Bigger hint:* "The rule appears once per effective-dated table (salary, assignment, range). For the table in `from`, it goes in the `where`. For each table you join, it goes in that join's `on`: in a left join, putting it in the `where` instead would quietly drop the employees with no matching row. Put the as-of date in a one-row CTE so it's written once."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     ```sql
     with params as (select date '____' as as_of_date)
     select ...
     from comp_salary as s
     cross join params as p
     join hr_assignment as a
         on a.employee_id = s.employee_id
        and p.as_of_date ____ a.effective_start
        and p.as_of_date ____ a.effective_end
     where p.as_of_date ____ s.effective_start and ____
     ```

     </details>
- **Resources:** [DuckDB: FROM and JOIN (ASOF joins section)](https://duckdb.org/docs/stable/sql/query_syntax/from) · [DuckDB: date functions](https://duckdb.org/docs/stable/sql/functions/date)

### P2-07 · Window functions II: merit increase % (LAG)
- **Concept:** `lag` / `lead`; percent change; average vs median; separating merit from promotion.
- **Why on the job:** merit-cycle cost and merit % by department are the headline numbers after every cycle.
- **Analogy:** `lag` = DAX "previous value" (time intelligence like `PREVIOUSMONTH`), but per employee. Payroll analogy: comparing this period's rate to last period's on a rate-change audit.
- **Hint ladder:**
  1. *Nudge:* "For one employee, list their salary rows in date order. What does 'previous salary' mean for the first row?"
  2. *Bigger hint:* "`lag(column) over (partition by <who> order by <when>)`. Percent change = change ÷ old value. Filter to merit rows *after* computing the previous salary, or a promotion row will become someone's 'previous'."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     ```sql
     select
         employee_id, effective_start, salary, change_reason,
         lag(____) over (partition by ____ order by ____) as previous_salary
     from comp_salary
     ```

     </details>
- **Resources:** [DuckDB: window functions](https://duckdb.org/docs/stable/sql/functions/window_functions) · [Mode: SQL window functions tutorial](https://mode.com/sql-tutorial/sql-window-functions)

### P2-08 · Messy IDs, dedupe and set operations
- **Concept:** string cleanup; dedupe with `row_number` + `qualify`; `union` / `except` / `intersect`; anti joins.
- **Why on the job:** carrier files never match HR keys cleanly. This is the carrier reconciliation done by hand today, made repeatable.
- **Analogy:** Power Query Trim + "Remove Duplicates" (which keeps the *first* row, often not the one you want); a Left Anti merge for "on their file, not ours". Manual recon: the two-column VLOOKUP with `#N/A` meaning "not found".
- **Hint ladder:**
  1. *Nudge:* "Write three carrier IDs that are really the same person. What steps make them identical?"
  2. *Bigger hint:* "Clean the ID first, in its own CTE. Then number the rows per cleaned ID in an order that puts the row you want to keep first, and keep row 1. `except` compares whole rows, so select only the key on both sides."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     ```sql
     with cleaned as (
         select *, lpad(trim(____), ____, '0') as member_key from carrier_eligibility_file_a
     )
     select * from cleaned
     qualify row_number() over (partition by ____ order by ____ desc) = 1
     ```

     </details>
- **Resources:** [DuckDB: set operations](https://duckdb.org/docs/stable/sql/query_syntax/setops) · [DuckDB: QUALIFY](https://duckdb.org/docs/stable/sql/query_syntax/qualify)

### P2-09 · Conditional aggregation: gross-to-net
- **Concept:** long to wide with `sum(case when …)` and DuckDB `pivot`; checking nothing was dropped.
- **Why on the job:** payroll results come as one row per pay code; every payroll review needs them side by side.
- **Analogy:** Power Query Pivot Column. Payroll: the gross-to-net register, with a foot-and-cross-foot check.
- **Hint ladder:**
  1. *Nudge:* "Which pay-code categories become columns? How will you know a pay code didn't fall through the cracks?"
  2. *Bigger hint:* "One `sum(case when category = '...' then amount end)` per column, grouped by employee. Then compare the total of all columns to the total of the long table."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     ```sql
     select
         r.employee_id,
         sum(case when c.category = '____' then r.amount end) as gross_pay,
         ____
     from payroll_results as r
     join pay_codes as c on ____
     where r.pay_period_id = ____
     group by ____
     ```

     </details>
- **Resources:** [DuckDB: GROUP BY](https://duckdb.org/docs/stable/sql/query_syntax/groupby) · [DuckDB: CASE](https://duckdb.org/docs/stable/sql/expressions/case)

### P2-10 · Nulls, tie-outs and query plans
- **Concept:** `null` vs `0`; `coalesce`; nulls in joins and aggregates; full outer join; `explain analyze`.
- **Why on the job:** a tie-out that drops the period with no GL posting reports "tied" when it isn't. That's the worst kind of wrong.
- **Analogy:** the payroll-to-GL reconciliation workbook, with a "missing" status instead of a blank cell. A query plan = Power BI's Performance Analyzer for SQL.
- **Hint ladder:**
  1. *Nudge:* "If a period has payroll but no GL rows, what does an inner join do to it? What does `sum` return over zero rows?"
  2. *Bigger hint:* "Total each side per period in its own CTE first, then join the two totals with a join that keeps periods from either side. Decide the status with `case`, checking the missing case first."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     ```sql
     with payroll as (select pay_period_id, sum(amount) as payroll_total from ____ group by 1),
          gl as (select ____ )
     select
         coalesce(p.pay_period_id, g.pay_period_id) as pay_period_id,
         ____
     from payroll as p
     ____ join gl as g on ____
     ```

     </details>
- **Resources:** [DuckDB: NULL values](https://duckdb.org/docs/stable/sql/data_types/nulls) · [DuckDB: EXPLAIN ANALYZE](https://duckdb.org/docs/stable/guides/meta/explain_analyze)

---

## Phase 3: dbt on DuckDB

### P3-01 · dbt project, first source, first staging model
- **Concept:** what dbt is (SQL files + a dependency graph + tests); `profiles.yml`; `source()` vs `ref()`; `dbt run` / `test` / `build`; node selection.
- **Why on the job:** dbt is the standard tool for analytics engineering; "walk me through your dbt project" is a standard interview question.
- **Analogy:** a staging model = a Power Query query that only renames, retypes and trims, no business logic. `ref()` = referencing another query by name instead of copying it. `dbt build` = Refresh All, plus every check.
- **Hint ladder:**
  1. *Nudge:* "Open your P2-01 query. Which parts are 'cleanup' and which are 'business logic'? Only the cleanup belongs in staging."
  2. *Bigger hint:* "A source is declared in YAML (source name, table names); the model selects from `{{ source('<source>', '<table>') }}`. Tests go in a YAML file next to the model under `data_tests:`."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     ```yaml
     sources:
       - name: ____
         schema: main
         tables:
           - name: ____
     ```
     ```sql
     select
         ____ as job_code,
         ____
     from {{ source('____', '____') }}
     ```

     </details>
- **Resources:** [dbt: How we structure our projects](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview) · [dbt: sources](https://docs.getdbt.com/docs/build/sources) · [dbt: DuckDB setup](https://docs.getdbt.com/docs/core/connect-data-platform/duckdb-setup)

### P3-02 · Staging for HR core and comp, with generic tests
- **Concept:** generic tests (`unique`, `not_null`, `accepted_values`, `relationships`); packages and `dbt deps`; grain of effective-dated tables.
- **Why on the job:** tests on staging are the early-warning system: bad data is caught at the door, not in the CFO's report.
- **Analogy:** manual reconciliation checks → dbt tests. `relationships` = "every assignment's department exists in the org table", the VLOOKUP check you'd do by hand.
- **Hint ladder:**
  1. *Nudge:* "For each table, what makes a row unique? For `comp_salary`, is `employee_id` enough?"
  2. *Bigger hint:* "When one column isn't unique, the key is a combination; `dbt_utils` has a test for exactly that. `packages.yml` lists the package; `dbt deps` installs it."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     ```yaml
     models:
       - name: stg_hcm__salary
         data_tests:
           - dbt_utils.unique_combination_of_columns:
               combination_of_columns: [____, ____]
     ```

     </details>
- **Resources:** [dbt: data tests](https://docs.getdbt.com/docs/build/data-tests) · [dbt_utils package](https://hub.getdbt.com/dbt-labs/dbt_utils/latest/)

### P3-03 · Seeds and the first intermediate model
- **Concept:** seeds (small, hand-maintained lookups in Git); the intermediate layer; `view` vs `table` vs `ephemeral`.
- **Why on the job:** reason codes typed differently each month break every trend chart; a seed is the one official list.
- **Analogy:** a seed = an "Enter Data" table in Power BI, but version-controlled and tested. Intermediate model = a staging query you reference but never load to the report (Power Query "Enable load" off).
- **Hint ladder:**
  1. *Nudge:* "Which lookups change only when a person decides they should? Those are seed candidates. Which are delivered by a system? Those aren't."
  2. *Bigger hint:* "A CSV in `seeds/` becomes a table after `dbt seed` (or `dbt build`), and you `ref()` it like a model. Materialization is set in the model's `config()` or in `dbt_project.yml`."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     `{{ config(materialized='____') }}` at the top of `int_assignment_current.sql`, then a `where` that keeps only ____ rows.

     </details>
- **Resources:** [dbt: seeds](https://docs.getdbt.com/docs/build/seeds) · [dbt: materializations](https://docs.getdbt.com/docs/build/materializations)

### P3-04 · The `as_of_filter` macro and `fct_compa_ratio`
- **Concept:** Jinja; macros; `var()`; turning a repeated pattern into one tested building block.
- **Why on the job:** the same as-of logic is needed in a dozen models. Written once, it's right everywhere, or wrong everywhere and fixed in one place.
- **Analogy:** a macro = a Power Query custom function you invoke per table. `var()` = a report parameter.
- **Hint ladder:**
  1. *Nudge:* "Look at your P2-06 condition. Which parts change from table to table (the alias, the date), and which stay the same?"
  2. *Bigger hint:* "A macro takes those changing parts as arguments and returns SQL text. Call it inside a model with `{{ as_of_filter(...) }}`. Check the compiled SQL in `target/compiled/` to see what it produced."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     ```sql
     {% macro as_of_filter(table_alias, as_of_date) %}
         ____
     {% endmacro %}
     ```

     </details>
- **Resources:** [dbt: Jinja and macros](https://docs.getdbt.com/docs/build/jinja-macros) · [dbt: node selection syntax](https://docs.getdbt.com/reference/node-selection/syntax)

### P3-05 · Snapshots and `dim_employee`
- **Concept:** snapshots; SCD Type 2; `dbt_valid_from` / `dbt_valid_to`; surrogate keys; rehires.
- **Why on the job:** extracts often only show "now". Snapshots keep history you'd otherwise lose, and SCD Type 2 is a standard interview topic.
- **Analogy:** HCM effective dating ↔ SCD Type 2: the HCM keeps history for you; a snapshot builds it yourself from repeated "current" extracts. Payroll analogy: keeping every rate change with its effective date instead of overwriting the rate.
- **Hint ladder:**
  1. *Nudge:* "If the extract only shows today's job, how would you know someone's job last month? What would you have to save on every run?"
  2. *Bigger hint:* "A snapshot needs a unique key and a strategy: `timestamp` (an updated-at column tells you what changed) or `check` (compare listed columns). Run it, change the source, run it again, and look at the valid-from/valid-to columns."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     in the snapshot YAML: `unique_key: ____`, `strategy: ____`, and either `updated_at: ____` or `check_cols: [____]`.

     </details>
- **Resources:** [dbt: snapshots](https://docs.getdbt.com/docs/build/snapshots) · [Power BI: star schema guidance (SCD section)](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema)

### P3-06 · Benefits: `fct_benefit_cost_pepm`
- **Concept:** choosing a fact table's grain; joining to effective-dated rates.
- **Why on the job:** "cost per employee per month" is the standard benefits KPI; the grain decides what it can be sliced by.
- **Analogy:** the grain of a fact table = the level of detail of a Power BI table; a measure can roll up from it but never drill below it.
- **Hint ladder:**
  1. *Nudge:* "Say the grain in one sentence: one row per ____. Which slicers does that allow, and which does it rule out?"
  2. *Bigger hint:* "Build months first (from `dim_date` or a date spine), then which elections were active each month, then the rate in effect that month, reusing `as_of_filter`."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     a YAML description line that states the grain, plus a `dbt_utils.unique_combination_of_columns` test on ____, ____ and ____.

     </details>
- **Resources:** [dbt: How we structure our projects](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview) · [Power BI: star schema guidance](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema)

### P3-07 · Payroll: `fct_payroll_gl_tieout`
- **Concept:** singular tests; test severity (`warn` / `error`); documented warnings.
- **Why on the job:** the period-end tie-out stops being a spreadsheet and becomes a check that runs on every build.
- **Analogy:** manual reconciliation → dbt test, in its purest form. Severity `warn` = a reconciling item you've documented and accepted; `error` = one that stops the close.
- **Hint ladder:**
  1. *Nudge:* "A singular test passes when it returns zero rows. What query returns the periods that *don't* tie?"
  2. *Bigger hint:* "Put that query in a `.sql` file in dbt's tests folder, selecting from `ref('fct_payroll_gl_tieout')`. Severity is set in a `config()` block at the top."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     `{{ config(severity='____') }}` then `select * from {{ ref('____') }} where status = '____'`.

     </details>
- **Resources:** [dbt: data tests (singular tests, severity)](https://docs.getdbt.com/docs/build/data-tests)

### P3-08 · Recon: `fct_carrier_reconciliation`
- **Concept:** conforming two sources to one shape; reusable cleanup macros; reason codes from a seed.
- **Why on the job:** every carrier sends a different file layout; the reconciliation only works once they share one shape.
- **Analogy:** Power Query "Append Queries" after renaming columns to match. The exceptions list with reason codes = the recon workbook's "reconciling items" tab.
- **Hint ladder:**
  1. *Nudge:* "Put the two carrier layouts side by side. Which columns mean the same thing under different names?"
  2. *Bigger hint:* "One staging model per file that renames to a shared set of columns, then `union all` in the intermediate model. The ID cleanup from P2-08 becomes a macro both use."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     `select ____ as member_key, ____ as plan_code, 'a' as source_file from {{ ref('stg_carrier__eligibility_a') }} union all select ____`.

     </details>
- **Resources:** [DuckDB: set operations](https://duckdb.org/docs/stable/sql/query_syntax/setops) · [dbt: Jinja and macros](https://docs.getdbt.com/docs/build/jinja-macros)

### P3-09 · `fct_total_rewards_statement` and `dim_date`
- **Concept:** date dimensions; building a mart from other marts vs from intermediate models.
- **Why on the job:** the total rewards statement is the deliverable employees actually see; every line must tie to its source.
- **Analogy:** `dim_date` = the date table you mark in Power BI; the statement = a drill-through page, but computed and tested upstream.
- **Hint ladder:**
  1. *Nudge:* "List the five reward components. Which mart or intermediate model already has each one, at what grain?"
  2. *Bigger hint:* "Bring each component to employee × plan-year grain in its own CTE, then join them on that key. A date spine (`generate_series` in DuckDB, or the `dbt_utils.date_spine` macro) builds `dim_date`."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     `with salary as (select employee_id, plan_year, sum(____) as salary from {{ ref('____') }} group by 1, 2), ...`

     </details>
- **Resources:** [Power BI: date tables](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-date-tables) · [dbt_utils package](https://hub.getdbt.com/dbt-labs/dbt_utils/latest/)

### P3-10 · `assert_all_planted_anomalies_caught`, docs and lineage
- **Concept:** testing the tests with an answer key (a known-correct list of what should be caught); docs and lineage.
- **Why on the job:** "how do you know your tests work?" is the follow-up question that separates a good interview answer from a great one.
- **Analogy:** an auditor planting known errors in a sample to check the controls catch them.
- **Hint ladder:**
  1. *Nudge:* "For each row in the answer key, which mart or test should flag it? Make that mapping a column."
  2. *Bigger hint:* "Load the answer key as a source or seed. The test selects answer-key rows that have no match in the union of flagged rows from the marts. Zero rows = every anomaly caught."
  3. *Partial code:* open only after a real attempt at rung 2.
     <details><summary>Show the partial code</summary>

     `select k.* from {{ ref('____') }} as k left join flagged as f on ____ where f.____ is null`.

     </details>
- **Resources:** [dbt: documentation](https://docs.getdbt.com/docs/build/documentation) · [dbt Analytics Engineering exam](https://www.getdbt.com/certifications/analytics-engineer-certification-exam)

---

## Phase 4: Power BI on the marts

Rung 3 in this phase is partial *steps*, not partial DAX.

### P4-01 · Connect to the marts; PBIP in Git
- **Concept:** Import vs DirectQuery vs Direct Lake; Power Query parameters; PBIP and TMDL as source control.
- **Why on the job:** teams now review Power BI changes in pull requests like code; a `.pbix` on a desktop can't be reviewed.
- **Analogy:** PBIP = saving the model as text files, so a change to a measure is a visible diff, the same as a commit to a `.sql` file.
- **Hint ladder:**
  1. *Nudge:* "Where will the marts live in Phase 6? Which connection choice survives that move with the least rework?"
  2. *Bigger hint:* "Create a parameter for the folder path first, then point the Parquet source at it. Save as PBIP, then change one thing and run `git diff`."
  3. *Partial steps:* open only after a real attempt at rung 2.
     <details><summary>Show the partial steps</summary>

     parameter `MartsFolder` → Get Data → Parquet → file path built from the parameter → load `fct_compa_ratio` → check row count against DuckDB → Save as PBIP.

     </details>
- **Resources:** [PBIP overview](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview) · [Power Query Parquet connector](https://learn.microsoft.com/en-us/power-query/connectors/parquet) · [PL-300 study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/pl-300)

### P4-02 · Star schema
- **Concept:** star schema, cardinality, filter direction, role-playing dates, date tables, the SCD2 key choice.
- **Why on the job:** most "wrong total" tickets in Power BI are model problems, not DAX problems.
- **Analogy:** Thomas already builds these; the new part is that every table arrives clean from dbt, so the model is only relationships.
- **Hint ladder:**
  1. *Nudge:* "For each fact, which dimensions does it need, and on which key?"
  2. *Bigger hint:* "Draw it in `text` first (facts in the middle). Every arrow points from a dimension to a fact. A fact with two dates gets one active relationship and one inactive."
  3. *Partial steps:* open only after a real attempt at rung 2.
     <details><summary>Show the partial steps</summary>

     load dims → load facts → create relationships from `powerbi-model-plan.md` → mark `dim_date` → hide keys → screenshot model view.

     </details>
- **Resources:** [Power BI: star schema guidance](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) · [Power BI: date tables](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-date-tables)

### P4-03 · Compensation page
- **Concept:** thin measures on a clean model; field parameters; calculation groups.
- **Why on the job:** when the logic lives in dbt, DAX stays short, and short DAX is easier to review and faster.
- **Analogy:** DAX measure → mart column: anything that can be a column in dbt should be; measures only aggregate.
- **Hint ladder:**
  1. *Nudge:* "Which of these numbers does a mart column already hold? Which need an aggregate only?"
  2. *Bigger hint:* "A weighted average and a simple average of compa-ratio give different answers. Decide which the committee means before writing it."
  3. *Partial steps:* open only after a real attempt at rung 2.
     <details><summary>Show the partial steps</summary>

     create a display folder → write the average compa-ratio measure → check it against a DuckDB query on the mart → add a field parameter with department and job.

     </details>
- **Resources:** [Field parameters](https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-field-parameters) · [Calculation groups](https://learn.microsoft.com/en-us/power-bi/transform-model/calculation-groups)

### P4-04 · Benefits, payroll and exceptions pages; performance
- **Concept:** visual choice per question; Performance Analyzer.
- **Why on the job:** a slow report doesn't get used; finding the slow visual is a routine PL-300 task.
- **Analogy:** Performance Analyzer = `explain analyze` from P2-10, for visuals.
- **Hint ladder:**
  1. *Nudge:* "What single question does each page answer? Which visual answers it fastest for the reader?"
  2. *Bigger hint:* "Start recording in Performance Analyzer, refresh visuals, sort by duration. Look at DAX query time vs visual display time."
  3. *Partial steps:* open only after a real attempt at rung 2.
     <details><summary>Show the partial steps</summary>

     record → find the slowest visual → change one thing (fewer fields, a simpler measure, or a pre-aggregated mart column) → record again → note both times.

     </details>
- **Resources:** [Performance Analyzer](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-performance-analyzer)

### P4-05 · Total rewards statement (drill-through)
- **Concept:** drill-through pages; single-entity page design.
- **Why on the job:** the statement is the one report employees see; it has to be right line by line.
- **Analogy:** the tie-out habit again: two employees checked by hand against the mart.
- **Hint ladder:**
  1. *Nudge:* "Which field identifies the person the page is about?"
  2. *Bigger hint:* "Put that field in the page's drill-through well; any visual showing it on another page then offers drill-through."
  3. *Partial steps:* open only after a real attempt at rung 2.
     <details><summary>Show the partial steps</summary>

     new page → drill-through field → statement visuals from `fct_total_rewards_statement` → back button → test from two source pages.

     </details>
- **Resources:** [Drill-through](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-drillthrough)

### P4-06 · Row-level security
- **Concept:** static vs dynamic RLS; a security table built and tested upstream; RLS after publishing.
- **Why on the job:** pay data is the most sensitive data in a company; RLS mistakes are incidents.
- **Analogy:** a manager-access list maintained in HR, tested like any other recon, instead of typed into the report.
- **Hint ladder:**
  1. *Nudge:* "What does the report know about the person viewing it? How does that connect to their team?"
  2. *Bigger hint:* "The role filters one table (the access table or `dim_employee`) by the signed-in user. The relationships carry the filter to the facts. Facts without an employee key aren't filtered."
  3. *Partial steps:* open only after a real attempt at rung 2.
     <details><summary>Show the partial steps</summary>

     build the access table in dbt with a test → load it → relate it → create the Manager role with a filter on the user → "View as" two managers → compare totals.

     </details>
- **Resources:** [RLS in Power BI](https://learn.microsoft.com/en-us/power-bi/enterprise/service-admin-rls) · [RLS guidance](https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance)
