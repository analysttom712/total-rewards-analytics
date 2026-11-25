# Backlog: ticket drafts for Phases 2–4

Drafts of the tickets that come after Phase 1, prepared ahead so each phase starts ready to teach. **None of these are GitHub issues yet.** Thomas approves them, then they're created with `gh issue create` a few at a time (CLAUDE.md section 4 keeps 3–5 ready ahead). Once a draft becomes an issue, the issue is the source of truth: mark the draft `→ #N` here rather than keeping two copies in sync.

| File | What's in it |
|---|---|
| [`phase-2.md`](phase-2.md) | SQL in DuckDB: 10 tickets, 20 practice queries (M2). The most detailed |
| [`phase-3.md`](phase-3.md) | dbt Core on DuckDB: 10 tickets (M3) |
| [`phase-4.md`](phase-4.md) | Power BI on the marts: 6 tickets (M4) |
| [`lessons-phase-2-4.md`](lessons-phase-2-4.md) | Per ticket: concept, why it matters, Power BI analogy, hint ladder (no full solutions), resources |
| [`powerbi-model-plan.md`](powerbi-model-plan.md) | Star-schema plan: facts, dimensions, grain, relationships, RLS idea |

Related scaffolding: [`sql/practice/`](../../sql/practice/README.md), [`warehouse/`](../../warehouse/README.md), [`models/`](../../models/README.md) (planned dbt layout and the package check), [`powerbi/`](../../powerbi/README.md) (PBIP setup steps).

## Who writes what

Everything tagged as a learning objective is Thomas's first attempt (CLAUDE.md rule 3): every practice query, every dbt model, macro and test, every DAX measure and the Power BI model. These drafts prepare the ground around that work: the business ask, the acceptance criteria, the lesson outline, and in one case a test-first check (`tests/test_sql_practice_001.py` for P2-01, skipped until the ticket starts). Where a test needs data that doesn't exist yet, the test idea is written into the ticket instead.

## IDs and dependencies

- `P2-03` = Phase 2, ticket 3. Replaced by the issue number when created.
- `#9`, `#13`, `#14`, `#19`, `#20` are the open Phase 1 issues. Only #13, #14 and #19 gate SQL work: they give employees a department, make `python -m generator` write the raw files, and pin the as-of date so results don't drift. #9 and #20 don't block anything here.
- **Generator tables that don't have tickets yet.** Most Phase 2 SQL needs raw tables the generator doesn't write today. They're grouped below so the Phase 1 backlog can be written to match. Each will need its own Phase 1 ticket (or several):

| Group | Raw tables (names from `docs/PROJECT_SPEC.md`) | Unblocks |
|---|---|---|
| **G-comp** | `hr_assignment`, `hr_person`, `comp_salary` (effective-dated), `comp_grade_ranges` | P2-06, P3-02, P3-04, P3-05 |
| **G-merit** | `comp_merit_cycle` (or merit/promotion reason on `comp_salary`) | P2-07 |
| **G-benefits** | `benefit_plans`, `benefit_elections`, `benefit_premium_rates`, `hr_dependents`, `carrier_eligibility_file_a/b`, `ret_401k_contributions`, `pto_balances` | P2-08, P3-06, P3-08, P3-09 |
| **G-payroll** | `pay_periods`, `pay_codes`, `payroll_results` | P2-09, P3-07 |
| **G-gl** | `gl_postings` | P2-10, P3-07 |
| **G-anomalies** | the planted anomalies and `data/raw/_answer_key.csv` | P2-08, P2-10, P3-10 |

**What can start now:** P2-01 needs only the job catalog, which is already merged. Everything else in Phase 2 waits on #13, #14 and #19 (P2-02 to P2-05) or on the generator groups above (P2-06 onward).

## Labels

Each draft lists its labels. All of them exist today (checked 2026-11-25) except `phase-2`, `phase-3`, `phase-4`, `cert:PL-300` and `cert:dbt`, which need creating once (`gh label create`) when the first issue of each kind is made.
