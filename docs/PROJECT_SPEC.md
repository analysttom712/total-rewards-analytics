# Project Spec: Total Rewards Analytics Platform

Moved out of CLAUDE.md so it only loads when a task needs it. Read the relevant section before creating tickets or touching the generator, dbt models or architecture.

**Total Rewards Analytics Platform for Northwind Mutual (fictional, ~1,500 employees).**

One platform covering the whole Total Rewards department: compensation, benefits, payroll, PTO and total cost of employment. It answers the questions a Total Rewards team actually gets asked.

## Business questions it must answer
- **Compensation**
  - Where does each employee sit in their pay range? (compa-ratio, range penetration)
  - Who's below minimum or above maximum?
  - What did the merit cycle cost? How much did promotions add?
  - Pay-equity *analysis pattern*: comparing pay for similar roles across groups. Synthetic data only; frame it as the method, never as findings about real people.
- **Benefits**
  - Enrollment by plan and tier; employer vs. employee premium cost; cost per employee per month.
  - Does our enrollment match the carrier's eligibility file? (exceptions)
  - Retiree and surviving-spouse coverage accuracy.
- **Payroll**
  - Gross-to-net by pay period; deductions tie to benefit elections; taxes simplified.
  - Payroll register ties to the general ledger every period.
- **Total rewards**
  - A **total rewards statement** per employee: salary + bonus + employer benefit cost + retirement match + PTO value.
  - Total cost of employment by department.
- **Ops / quality**
  - Every reconciliation has an exceptions list with reason codes and dollar impact.

## The integration story: HCM → AWS
Northwind Mutual runs a cloud **HCM system** (core HR, compensation, benefits, payroll) and a separate **financials system** (GL). It's building an **AWS data platform** for Total Rewards analytics. This project simulates that integration end to end, the way real teams do it:

1. **Outbound from the HCM system (simulated by the Python generator).** HCM systems commonly get data out in two ways, and we mock both:
   - **Scheduled extract files:** report-based extracts that drop delimited files on a schedule, with full and changes-only ("delta") runs, effective-dated rows and an open end date of `9999-12-31`.
   - **REST API:** a small local mock API (FastAPI) returning JSON shaped like typical HCM REST resources (employees, jobs, compensation, benefit elections), with offset paging and a next-page flag and nested child objects.
2. **Land in AWS:** a Python ingestion job (boto3; later AWS Lambda on an EventBridge schedule) writes raw files to **S3** as `raw/hcm/<object>/extract_date=YYYY-MM-DD/`, never modified after landing (immutable raw zone).
3. **Catalog and query:** **AWS Glue Data Catalog** tables over S3; **Athena** for SQL; raw → Parquet conversion.
4. **Transform:** **dbt** (DuckDB locally, Athena on AWS): staging conforms HCM structures, intermediate handles effective dating and deltas, marts answer the Total Rewards questions.
5. **Serve:** Power BI semantic model over the marts.
6. **Outbound to vendors:** carrier eligibility files (one CSV, one simplified 834-style) and a 401(k) contribution file are *generated from the marts*, then reconciled back against the carrier's own file (the recon loop).
7. **CI and ops:** GitHub Actions runs tests on every PR; data-quality tests and source-freshness checks act as the monitoring.

Cost note: real integrations often use SFTP (AWS Transfer Family), but that bills hourly. **Don't create it.** Simulate the SFTP drop by uploading straight to S3, and explain the real pattern in `docs/DECISIONS.md`.

**Public-post rule:** the project and blog describe a *fictional* company's HCM-to-AWS integration. Never mention Thomas's actual employer, its vendors (including its HR system) or its technology plans. Keep HR vendor product names and vendor-specific table names out of the repo; use the generic names below.

## Architecture (built in phases, see docs/CURRICULUM.md)
```
HCM system (simulated): extract files + mock REST API  (Python generator / FastAPI)
    → ingestion (Python boto3 → later Lambda + EventBridge)
    → S3 raw zone (partitioned by extract_date) → Glue Catalog → Athena
      (DuckDB mirrors this locally for Phases 1–5)
    → dbt: staging → intermediate → marts (+ snapshots, tests, docs)
    → Power BI semantic model (PBIP in Git) → dashboards + total rewards statement
    → outbound carrier / 401(k) files → reconciliation marts
    → GitHub Actions CI runs dbt build + tests on every pull request
```

## Simulated HCM source objects (generic naming)
| Domain | Raw tables |
|---|---|
| HR core | `hr_person` (date-tracked), `hr_assignment` (job, dept, manager, status history), `hr_org`, `hr_job` |
| Compensation | `comp_salary` (salary history, effective-dated), `comp_grade_ranges` (min/mid/max by grade and year), `comp_merit_cycle`, `comp_bonus_payments` |
| Benefits | `benefit_plans`, `benefit_elections`, `benefit_premium_rates`, `hr_dependents` (dependents/spouses), `carrier_eligibility_file_a/b` (different formats on purpose) |
| Payroll | `pay_periods`, `payroll_results` (earnings, deductions, employer taxes by pay code), `pay_codes` |
| Retirement | `ret_401k_contributions` (employee deferral + employer match) |
| Time off | `pto_accruals`, `pto_balances` |
| Finance | `gl_postings` (payroll, benefits and bonus expense accounts by period) |

**Key design: people, employment periods, assignments, orgs (HCM-style)**
- `employee_id` (e.g., `1001`) is permanent for the person's whole life in the system, across rehires.
- Each employment period gets a sequence number. The **assignment number = employee_id + sequence**: `1001-1` for the first hire, `1001-2` after a rehire (or a second concurrent assignment). Keep `employment_period_id` and `assignment_id` as separate surrogate IDs.
- **Past employees are first-class:** terminations (voluntary, involuntary), retirements (who keep retiree benefits), deaths (surviving spouses stay covered), **rehires** (same person number, new `-N` assignment), leaves of absence, and transfers.
- **Org keys:** legal entity → business unit → department → cost center, each with its own code (e.g., `LE01`, `BU100`, `D1001-FIN`). Some people **transfer between legal entities**, which ends one assignment and starts another.
- **Mix at `standard` scale (approx.):** ~1,500 active, ~700 terminated, ~200 retirees, ~30 deceased with surviving spouses, ~60 rehires, ~40 concurrent assignments, ~30 legal-entity transfers.
- **Planted key anomalies** (textbook data-quality patterns, invented for testing; not drawn from any employer): a rehire created as a duplicate person (new person number for the same person); the carrier still enrolled under the old `-1` assignment; payroll charged to an ended assignment; a terminated employee's benefits never end-dated; a retiree's assignment status flipped back to active.
- **Teaching moments:** grain ("one row per what?"), surrogate vs. natural keys, why `employee_id` alone isn't a unique key in assignment-level tables, and how `dim_employee` handles rehires (SCD Type 2 + current flag).

**Data volume: one `--scale` flag in the generator**
| Scale | Employees | History | Approx. total rows | Use for |
|---|---|---|---|---|
| `tiny` | 100 | 3 months | ~15K | Learning, unit tests, CI (seconds to run) |
| `standard` | 1,500 active (~2,400 people ever, with terms, retirees, dependents) | 3 years, biweekly payroll (78 pay periods) | ~2M | The real platform, Power BI, AWS |
| `large` | 15,000 | 3 years | ~20M | Phase 7 performance work: incremental models, partitioning, PySpark |

Biggest table at `standard`: `payroll_results`, about 1.4M rows (1,500 × 78 periods × ~12 pay codes). Then the carrier files (~180K), PTO (~115K) and 401(k) (~95K). Everything else is under 25K rows.

**Don't commit generated data.** Only the generator code and a small `data/sample/` (the `tiny` scale) go in Git. GitHub blocks files over 100 MB, and regenerating from the seed is the point. `data/raw/` is gitignored.

**Planted anomalies** (textbook data-quality patterns, invented for testing; not drawn from any employer; recorded in `data/raw/_answer_key.csv`; tests must prove each one is caught):
- Employees paid below grade minimum / above maximum
- Benefit deduction in payroll doesn't match the election
- Carrier file missing a covered spouse; carrier billing a terminated or deceased member
- Tier mismatches; duplicate carrier rows; messy IDs (leading zeros, spaces)
- 401(k) match calculated wrong for a handful of people
- Payroll register vs. GL out of balance in two periods (one rounding, one structural)
- Salary change with no matching assignment change (orphan comp record)

## dbt layout
- `staging/`: 1:1 cleanup per raw table (views)
- `intermediate/`: as-of logic, deduped carrier members, gross-to-net building blocks
- `marts/`, grouped by domain: `comp/`, `benefits/`, `payroll/`, `total_rewards/`, `recon/`
  - examples: `fct_compa_ratio`, `fct_merit_cycle_cost`, `fct_benefit_cost_pepm`, `fct_carrier_reconciliation`, `fct_payroll_gl_tieout`, `fct_total_rewards_statement`, `dim_employee`, `dim_job`, `dim_date`
- `snapshots/`: SCD Type 2 on employee job/comp (teach why)
- `tests/`: singular tests, including `assert_all_planted_anomalies_caught.sql`
- `seeds/`: reason codes, plan codes, small lookups

## Resume lines (only when true)

Keep a running draft in `docs/RESUME_LINES.md`, updated only from what's merged and passing. Example target (fill in real numbers):

"Built a Total Rewards analytics platform (synthetic data): Python data generator, dbt models on DuckDB and AWS Athena covering compensation, benefits, payroll and GL reconciliation, N automated data-quality tests in GitHub Actions CI, and a Power BI semantic model with a per-employee total rewards statement."
