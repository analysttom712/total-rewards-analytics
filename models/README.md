# dbt models (Phase 3, planned)

Nothing here runs yet. This README records the planned layout from [`docs/PROJECT_SPEC.md`](../docs/PROJECT_SPEC.md) ("dbt layout") and the version check for the packages, so Phase 3 starts from a known state. The tickets are drafted in [`docs/backlog/phase-3.md`](../docs/backlog/phase-3.md). Creating `dbt_project.yml` and every model is Thomas's work in those tickets.

## Planned layout

```text
models/
  staging/                    1:1 cleanup of each raw table (views)
    hcm/                      _hcm__sources.yml, stg_hcm__person.sql, stg_hcm__assignment.sql, ...
    carrier/                  stg_carrier__eligibility_a.sql, stg_carrier__eligibility_b.sql
    finance/                  stg_finance__gl_postings.sql
  intermediate/               as-of logic, deduped carrier members, gross-to-net building blocks
    int_salary_as_of.sql, int_assignment_as_of.sql, int_carrier_members_deduped.sql, ...
  marts/
    comp/                     fct_compa_ratio, fct_merit_cycle_cost
    benefits/                 fct_benefit_cost_pepm
    payroll/                  fct_payroll_gl_tieout
    recon/                    fct_carrier_reconciliation
    total_rewards/            fct_total_rewards_statement
    core/                     dim_employee, dim_job, dim_department, dim_date (shared dimensions)
snapshots/                    SCD Type 2 on assignment and salary history
tests/                        (repo root tests/ is pytest; dbt singular tests go in dbt's own tests path, set in P3-01)
seeds/                        reason codes, plan codes, small lookups
macros/                       as_of_filter and friends
```

Naming follows dbt Labs' "How we structure our dbt projects" guide: `stg_<source>__<object>`, `int_<what it does>`, `fct_` / `dim_` for marts. `core/` for shared dimensions is a proposal (the spec lists `dim_employee`, `dim_job`, `dim_date` without a folder).

**Open decision for P3-01:** dbt's singular tests live in a folder called `tests/` by default, and this repo already uses `tests/` for pytest. Options: point dbt's `test-paths` at `tests/dbt/`, or move the dbt project into a subfolder. P3-01 asks Thomas to choose and write the ADR.

## Package check (2026-11-25)

Checked on PyPI and with a trial install in a throwaway venv (Python 3.13, the version in `.python-version`):

| Package | Latest | Python 3.13 | Notes |
|---|---|---|---|
| `dbt-core` | 1.12.7 (2026-11-12) | Yes (classifiers 3.10–3.14) | dbt Core **v1**, Apache 2.0, a Python package |
| `dbt-duckdb` | 1.11.1 (2026-10-26) | Yes (classifiers 3.10–3.14) | Requires `duckdb>=1.0.0`, no upper limit |
| `duckdb` | 2.0.1 (already in `requirements.txt`) | Yes | |

Trial result: `pip install dbt-core dbt-duckdb` next to `duckdb==2.0.1` resolved cleanly, and `dbt build` on a one-model project (a view plus `unique` and `not_null` tests) passed: 3 of 3.

**dbt v2 notice.** The v1 CLI now prints that "dbt v2 is available, and is the default for new installations." Per dbt's docs ([install](https://docs.getdbt.com/docs/local/install-dbt), [upgrading to v2](https://docs.getdbt.com/docs/dbt-versions/dbt-upgrade/upgrading-to-v2)), v2 is a Rust rewrite shipped as a single binary (`pip install dbt` installs it too), its adapters are not the Python adapter packages, its adapter list shows DuckDB as "CLI only", and v1 "remains fully supported". `dbt-core` and the v2 `dbt` package can't share one Python environment.

**Recommendation:** stay on dbt Core v1 (`dbt-core` + `dbt-duckdb`) for Phases 3–7. It is the documented DuckDB path, the Athena adapter planned for Phase 6 is a v1 Python adapter, the dbt Analytics Engineering exam page lists "Supported version - 1.11" (a v1 release), and it matches most dbt material in `docs/RESOURCES.md`. Revisit at the Phase 3 sprint review; record the choice as an ADR in P3-01.

**Proposed `requirements.txt` change** (not made here; it's in the PR description for Thomas to approve at P3-01):

```text
dbt-core>=1.12,<1.13
dbt-duckdb>=1.11,<1.12
```

Pinning to the minor version keeps a surprise major release (or the v2 package) from arriving on a plain `pip install -r requirements.txt`.

## Profile

`profiles.yml` lives in `%USERPROFILE%\.dbt\` and never in this repo (CLAUDE.md rule 6; also gitignored). The DuckDB profile only needs a file path (`warehouse/northwind.duckdb`), no password, but the rule holds so the Athena profile in Phase 6 follows the same habit.
