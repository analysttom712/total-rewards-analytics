# Power BI model plan (Phase 4 prep)

A plan for the semantic model, drawn from the planned marts in [`docs/PROJECT_SPEC.md`](../PROJECT_SPEC.md) ("dbt layout"). It is a starting point for P4-02, not a decision: the grains below follow the spec, and some will change once the marts exist. **No DAX here.** Measures are Thomas's work in the Phase 4 tickets ([`phase-4.md`](phase-4.md)).

Setup steps for saving the model in Git (PBIP / TMDL) are in [`powerbi/README.md`](../../powerbi/README.md).

## Why most logic is already done

By Phase 4, dbt has done the joins, the as-of logic, the dedupe and the reconciliations. Power BI's job is to relate a few clean tables and add measures. That's the reason for the layering: logic in dbt is tested, versioned and reusable by any tool; logic in Power Query or DAX is tested only by eye and used only by this report.

## Fact tables

| Table (from mart) | Grain: one row per ... | Keys to dimensions | Main numbers | Notes |
|---|---|---|---|---|
| `fct_compa_ratio` | employee × month-end as-of date | employee, job, department, date | salary, range min/mid/max, compa-ratio | The mart in P3-04 is built for one as-of date. **Open decision:** run it for each month-end so the report can trend it (a periodic snapshot fact) |
| `fct_merit_cycle_cost` | employee × merit cycle | employee, department, date (effective date) | old salary, new salary, increase amount, increase % | Promotions flagged, not mixed in |
| `fct_benefit_cost_pepm` | plan × tier × month (spec) | plan, date | employer premium, employee premium, enrolled count | **Open decision:** at this grain, the manager RLS role can't filter it (no employee key). Either add an employee × plan × month fact, or leave the benefits page company-wide and say so |
| `fct_payroll_gl_tieout` | pay period | pay period, date | payroll total, GL total, difference, status | Company-level; outside manager RLS. For the Total Rewards team role only |
| `fct_carrier_reconciliation` | exception | employee (nullable: "not in HR" rows have none), plan, reason code, date | monthly premium impact | Nullable key: decide how blank employees show in visuals |
| `fct_total_rewards_statement` | employee × plan year | employee, date (plan year) | salary, bonus, employer benefits, 401(k) match, PTO value, total | Drives the statement drill-through page |

## Dimension tables

| Table | Grain | Source | Notes |
|---|---|---|---|
| `dim_employee` | employee version (SCD Type 2) | P3-05 | Has `is_current`, valid-from / valid-to, manager. Display name is a synthetic Faker name |
| `dim_job` | job | P3-02 | Grade, family |
| `dim_department` | department | `hr_org` | Legal entity → business unit → department → cost center hierarchy |
| `dim_date` | day | P3-09 | Mark as date table; pay-period and plan-year columns |
| `dim_pay_period` | pay period | `pay_periods` | Could fold into `dim_date`; decide in P4-02 |
| `dim_benefit_plan` | plan × tier | `benefit_plans`, seed | |
| `dim_reason_code` | reason code | seed (P3-03) | Exception categories for the recon page |

## Relationships

```text
                 dim_date ──────────────┐ (one active date relationship per fact;
                    │                   │  other date columns inactive = role-playing)
   dim_department ──┼── fct_compa_ratio ─┤
   dim_job ─────────┤   fct_merit_cycle_cost
   dim_employee ────┤   fct_total_rewards_statement
                    └── fct_carrier_reconciliation ── dim_reason_code
   dim_benefit_plan ─── fct_benefit_cost_pepm,  fct_carrier_reconciliation
   dim_pay_period ───── fct_payroll_gl_tieout
```

- **One-to-many, single direction,** dimension → fact, everywhere. No fact-to-fact relationships: facts meet through shared dimensions.
- **SCD Type 2 employee key.** Two choices to weigh in P4-02: facts carry the surrogate key of the employee version that was valid at the time (history shows the department the person was in *then*), or facts carry `employee_id` and relate to current rows only (history shows today's department). The first is correct for audits; the second is simpler. The spec's `dim_employee` with a current flag supports both.
- **Hide keys and raw number columns** in report view; expose measures instead (the PL-300 habit).

## Row-level security idea

- **Role "Manager":** a manager sees only their own team. Dynamic RLS: a small security table maps each manager's sign-in (synthetic, e.g. `mgr.d1001@northwind.example`) to the employees they manage, built in dbt from `dim_employee`'s manager column so the logic is tested upstream. The role filters `dim_employee` by the signed-in user; the filter flows to the facts through the relationships.
- **Role "Total Rewards":** sees everything, including the company-level facts (payroll vs GL, benefits PEPM).
- **Facts with no employee key** (`fct_payroll_gl_tieout`, `fct_benefit_cost_pepm` at plan grain) aren't filtered by the Manager role. Decide in P4-06: hide those pages from managers through the app audience, or add an employee-grain fact.
- **Test it** with Desktop's "View as" → role + other user, for one manager with a small team and one with nested teams.
- All user names and emails are synthetic and use the reserved `example` domain.

## Measures to write (names only; the DAX is Thomas's)

Average compa-ratio · count below minimum / above maximum · merit cycle cost · merit % (weighted) · employer cost PEPM · employee cost PEPM · payroll vs GL difference · open exceptions · exception dollar impact · total rewards value. Most are a simple sum or ratio over columns dbt already computed, which is the point of the layering.
