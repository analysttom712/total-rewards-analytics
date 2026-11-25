# Phase 3 ticket drafts: dbt Core on DuckDB

**Status: drafts.** Not GitHub issues yet; Thomas approves them in the PR first. Less detailed than Phase 2 on purpose: they get sharpened at the Phase 2 sprint review, when the generator tables and the practice queries exist. Lesson outlines are in [`lessons-phase-2-4.md`](lessons-phase-2-4.md); the planned folder layout and the dbt version check are in [`models/README.md`](../../models/README.md).

**Phase goal (M3):** `dbt build` green (documented warnings only), 40+ tests including `assert_all_planted_anomalies_caught`, lineage graph screenshot in the README. **Check:** explain the layering choices, one snapshot and the headline anomaly test.

**The thin-slice rule for this phase:** each ticket takes one business question from raw table to a mart you can query, with its tests, rather than building all of staging first. The Phase 2 practice query for the same question is the starting point; the dbt version must return the same answer.

| ID | Title | Builds | Blocked by | Est. |
|---|---|---|---|---|
| P3-01 | dbt project on DuckDB: first source, first staging model, first tests | `stg_hcm__job` | P2-02; `requirements.txt` change approved | 1–2 |
| P3-02 | Staging for HR core and comp, with generic tests | `stg_hcm__*` | P3-01, G-comp | 2 |
| P3-03 | Seeds and the first intermediate model | seeds, `int_assignment_current` | P3-02 | 1 |
| P3-04 | The `as_of_filter` macro and `fct_compa_ratio` | macro, `int_salary_as_of`, `fct_compa_ratio` | P3-03, P2-06 | 2 |
| P3-05 | Snapshots and `dim_employee` (SCD Type 2, rehires) | snapshot, `dim_employee` | P3-04 | 2 |
| P3-06 | Benefits: `fct_benefit_cost_pepm` | benefits staging + mart | P3-02, G-benefits | 1–2 |
| P3-07 | Payroll: gross-to-net and `fct_payroll_gl_tieout` | payroll staging, intermediate, mart | P3-02, P2-10, G-payroll, G-gl | 2 |
| P3-08 | Recon: `fct_carrier_reconciliation` with reason codes | carrier staging, `int_carrier_members_deduped`, mart | P3-03, P2-08 | 2 |
| P3-09 | `fct_total_rewards_statement` and `dim_date` | mart + date dimension | P3-05, P3-06, P3-07 | 2 |
| P3-10 | `assert_all_planted_anomalies_caught`, docs and lineage (M3) | singular test, docs site | all of the above, G-anomalies | 1–2 |

Labels on every Phase 3 ticket: `phase-3`, `dbt`, `cert:dbt`. Extra labels are listed per ticket.

---

## P3-01 · dbt project on DuckDB: first source, first staging model, first tests

**Labels:** `phase-3`, `dbt`, `cert:dbt`, `python`
**Blocked by:** P2-02 (the warehouse exists); Thomas approves the `requirements.txt` change proposed in the PR that added these drafts

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> The SQL answers are good, but they live in a folder of files that nobody runs in order. I want them to become a pipeline: one command that rebuilds everything, tests it, and tells me if anything broke.

### Acceptance criteria
- [ ] `dbt-core` and `dbt-duckdb` added to `requirements.txt` (pinned as proposed in `models/README.md`); `dbt --version` shows both
- [ ] `dbt_project.yml` created by you, with `models/`, `seeds/`, `snapshots/` and `macros/` paths; the `tests/` folder clash decided and written as an ADR in `docs/DECISIONS.md` (see `models/README.md`)
- [ ] An ADR records "dbt Core v1, not v2" (or your different choice) with the reason
- [ ] `profiles.yml` in `%USERPROFILE%\.dbt\` pointing at `warehouse/northwind.duckdb`; `dbt debug` passes; `git status` shows no profile in the repo
- [ ] `_hcm__sources.yml` declares the raw tables; `stg_hcm__job.sql` selects from `{{ source(...) }}`, renames to snake_case, casts types
- [ ] `unique` and `not_null` tests on the job key; `dbt build` green
- [ ] You explain `dbt run` vs `dbt test` vs `dbt build`, and run one model with `--select`
- [ ] PR with `Closes #N`

### Learning objective
- dbt project structure, `profiles.yml`, sources, `ref()` vs `source()`, the view materialization; `dbt build`, node selection
- Staging model = a Power Query query that only renames, retypes and cleans, with no business logic
- **Cert:** dbt Analytics Engineering: "Developing and optimizing dbt models", "Debugging data modeling errors"

### Estimate
1–2 sessions.

---

## P3-02 · Staging for HR core and comp, with generic tests

**Labels:** `phase-3`, `dbt`, `cert:dbt`
**Blocked by:** P3-01; G-comp (`hr_person`, `hr_assignment`, `hr_org`, `comp_salary`, `comp_grade_ranges`)

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> Every report starts from the same handful of HR tables, and every analyst cleans them differently. Clean them once, the same way for everyone, and put a check on each one so we hear about bad data before a report does.

### Acceptance criteria
- [ ] One staging model per HR-core and comp raw table, each a view, each 1:1 with its source
- [ ] Every model has a primary-key test; at least one `relationships` test (assignment → org) and one `accepted_values` test (assignment status)
- [ ] `dbt_utils` installed via `packages.yml`; one `dbt_utils.unique_combination_of_columns` test on an effective-dated table (why a single-column key isn't enough there goes in the YAML description)
- [ ] Column descriptions on at least the keys
- [ ] PR with `Closes #N`

### Learning objective
- Generic tests (`unique`, `not_null`, `accepted_values`, `relationships`), packages, `dbt deps`; the grain of an effective-dated table
- **Cert:** dbt Analytics Engineering: "Implementing dbt tests", "Implementing and maintaining external dependencies"

### Estimate
2 sessions.

---

## P3-03 · Seeds and the first intermediate model

**Labels:** `phase-3`, `dbt`, `cert:dbt`
**Blocked by:** P3-02

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> Reason codes on our exception reports are typed differently every month. Keep one official list of reason codes and plan codes that the reports read from, and build one table that answers "what job and department is each person in right now?".

### Acceptance criteria
- [ ] `seeds/reason_codes.csv` and `seeds/plan_codes.csv` (small, hand-written, synthetic) with tests on their keys
- [ ] `int_assignment_current.sql`: one row per active assignment, current job and department. Explain why it's an intermediate model and not a mart
- [ ] A `relationships` test from a staging model to a seed
- [ ] PR with `Closes #N`

### Learning objective
- Seeds (when to use them, when not); the intermediate layer's job; `ephemeral` vs `view` materialization (try both, keep one, say why)
- **Cert:** dbt Analytics Engineering: "Developing and optimizing dbt models" (seeds, materializations)

### Estimate
1 session.

---

## P3-04 · The `as_of_filter` macro and `fct_compa_ratio`

**Labels:** `phase-3`, `dbt`, `cert:dbt`
**Blocked by:** P3-03; P2-06 (the as-of SQL you already wrote)

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> The June 30 compa-ratio report was right, but it took a day. I want compa-ratio for any date I ask for, built the same way every time, so auditors get the same answer whoever runs it.

### Acceptance criteria
- [ ] `macros/as_of_filter.sql`: a macro you write that produces the effective-date condition for a given table alias and date
- [ ] `int_salary_as_of.sql` uses the macro; the as-of date comes from a project variable (`var`) with a default
- [ ] `fct_compa_ratio` (table materialization) returns the same rows as your `012_compa_ratio_as_of.sql` for the same date (show the comparison query)
- [ ] Tests: one row per employee per as-of date; compa-ratio not null for active employees
- [ ] `dbt build --vars` with two different dates gives two different, correct answers
- [ ] PR with `Closes #N`

### Test ideas (singular tests)
- The planted "paid below grade minimum" employees from `_answer_key.csv` have compa-ratio below the range minimum ÷ midpoint

### Learning objective
- Jinja, macros, `var()`; turning a repeated SQL pattern into one tested building block (compare to a Power Query custom function invoked per table)
- **Cert:** dbt Analytics Engineering: "Developing and optimizing dbt models" (Jinja, macros, variables)

### Estimate
2 sessions.

---

## P3-05 · Snapshots and `dim_employee` (SCD Type 2, rehires)

**Labels:** `phase-3`, `dbt`, `cert:dbt`
**Blocked by:** P3-04

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> When someone is rehired, half our reports count them twice and the other half lose their first stint. I want one employee table that keeps every version of a person's job and department, marks which one is current, and handles rehires correctly.

### Acceptance criteria
- [ ] A snapshot on the assignment extract with a strategy you choose (timestamp or check) and explain
- [ ] Load the extract twice with a change in between (a second generator run with a later `AS_OF`, or a hand-edited copy) and show the snapshot closing one row and opening another
- [ ] `dim_employee`: one row per employee per version, with valid-from / valid-to and `is_current`; exactly one current row per active assignment
- [ ] A rehire from the generator shows both employment periods; the planted duplicate-person rehire is caught by a test
- [ ] PR with `Closes #N`

### Learning objective
- Snapshots, SCD Type 2, `dbt_valid_from` / `dbt_valid_to`; surrogate vs natural keys; why `employee_id` alone isn't unique in assignment tables
- HCM effective dating ↔ SCD Type 2: the same idea from two directions
- **Cert:** dbt Analytics Engineering: "Developing and optimizing dbt models" (snapshots); PL-300 "Model the data" (slowly changing dimensions)

### Estimate
2 sessions.

---

## P3-06 · Benefits: `fct_benefit_cost_pepm`

**Labels:** `phase-3`, `dbt`, `cert:dbt`
**Blocked by:** P3-02; G-benefits (`benefit_plans`, `benefit_elections`, `benefit_premium_rates`)

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> Leadership asks every quarter what benefits cost per employee per month, split between what we pay and what employees pay, by plan and tier.

### Acceptance criteria
- [ ] Staging for the three benefits tables; intermediate model joining elections to rates in effect for each month
- [ ] `fct_benefit_cost_pepm` at a grain you state in the YAML (e.g. one row per plan, tier and month)
- [ ] Employer + employee premium = total premium on every row (a test)
- [ ] PR with `Closes #N`

### Learning objective
- Choosing a fact table's grain; joining to effective-dated rates (reusing `as_of_filter`)
- **Cert:** dbt Analytics Engineering: "Developing and optimizing dbt models"; PL-300 "Model the data" (fact grain)

### Estimate
1–2 sessions.

---

## P3-07 · Payroll: gross-to-net and `fct_payroll_gl_tieout`

**Labels:** `phase-3`, `dbt`, `cert:dbt`
**Blocked by:** P3-02; P2-09 and P2-10 (the practice versions); G-payroll, G-gl

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> The payroll-to-GL tie-out is done in a spreadsheet every period. Make it a table that rebuilds itself and fails loudly when a period doesn't tie.

### Acceptance criteria
- [ ] Staging for `pay_periods`, `pay_codes`, `payroll_results`, `gl_postings`
- [ ] An intermediate gross-to-net model at employee × pay period grain
- [ ] `fct_payroll_gl_tieout`: one row per period with the same statuses as `019_payroll_vs_gl_by_period.sql`
- [ ] A singular test that fails when any period is `out_of_balance`, configured to **warn** for the two planted periods (documented as a known warning, per M3)
- [ ] PR with `Closes #N`

### Learning objective
- Singular tests; test severity (`warn` vs `error`); documented warnings
- Manual reconciliation → dbt test: the core idea of this whole project
- **Cert:** dbt Analytics Engineering: "Implementing dbt tests" (singular tests, severity)

### Estimate
2 sessions.

---

## P3-08 · Recon: `fct_carrier_reconciliation` with reason codes

**Labels:** `phase-3`, `dbt`, `cert:dbt`
**Blocked by:** P3-03 (reason-code seed); P2-08 (the practice version); G-benefits (carrier files)

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> Every carrier exception needs a reason code and a dollar impact, so I can decide which ones to chase first.

### Acceptance criteria
- [ ] Staging for both carrier file formats (`a` and `b`), conformed to the same columns
- [ ] `int_carrier_members_deduped` with a uniqueness test on the cleaned member key
- [ ] `fct_carrier_reconciliation`: one row per exception, `reason_code` from the seed, monthly premium impact
- [ ] Every carrier anomaly in `_answer_key.csv` appears with the expected reason code
- [ ] PR with `Closes #N`

### Learning objective
- Conforming two sources to one shape (`union all` in a model); reusable cleanup via a macro
- **Cert:** dbt Analytics Engineering: "Developing and optimizing dbt models", "Implementing dbt tests"

### Estimate
2 sessions.

---

## P3-09 · `fct_total_rewards_statement` and `dim_date`

**Labels:** `phase-3`, `dbt`, `cert:dbt`
**Blocked by:** P3-05, P3-06, P3-07; G-benefits (401(k), PTO tables) for the retirement and PTO lines

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> Employees don't see what their package is worth beyond their paycheck. I want a statement per employee per year: salary, bonus, what we pay toward their benefits, their 401(k) match and the value of their paid time off.

### Acceptance criteria
- [ ] `dim_date` (a calendar table, by a method you choose and explain) with pay-period and fiscal columns
- [ ] `fct_total_rewards_statement`: one row per employee per plan year, one column per reward component, plus a total
- [ ] Each component ties to its own mart (a test per component)
- [ ] PR with `Closes #N`

### Learning objective
- Building a mart from other marts vs from intermediate models (and which to choose); date dimensions
- **Cert:** dbt Analytics Engineering: "Developing and optimizing dbt models"; PL-300 "Model the data" (date tables)

### Estimate
2 sessions.

---

## P3-10 · `assert_all_planted_anomalies_caught`, docs and lineage (M3)

**Labels:** `phase-3`, `dbt`, `cert:dbt`
**Blocked by:** P3-04 to P3-09; G-anomalies (`_answer_key.csv` complete)

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> Before I trust this platform, prove it: every problem we planted in the test data must be caught by some check, and I want a picture of how the data flows.

### Acceptance criteria
- [ ] `assert_all_planted_anomalies_caught.sql`: a singular test that returns any answer-key row no mart or test flagged (zero rows = pass)
- [ ] 40+ tests in total (`dbt ls --resource-type test | measure` in PowerShell); count in the PR
- [ ] Descriptions on every mart and its key columns; `dbt docs generate`; lineage graph screenshot in the README
- [ ] `dbt build` green with only documented warnings; tick M3 in `docs/CURRICULUM.md`; `docs/RESUME_LINES.md` updated with real numbers only
- [ ] PR with `Closes #N`

### Learning objective
- Testing the tests: the answer key as the known-correct list; docs and lineage; the M3 interview check
- **Cert:** dbt Analytics Engineering: "Developing and optimizing dbt models" (documentation), "Implementing dbt tests"

### Estimate
1–2 sessions.
