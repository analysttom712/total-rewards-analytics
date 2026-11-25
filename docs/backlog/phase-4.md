# Phase 4 ticket drafts: Power BI on the marts

**Status: drafts.** Not GitHub issues yet; Thomas approves them in the PR first. The least detailed of the three phases: they get sharpened once the marts exist. The model plan (facts, dimensions, grain, relationships, RLS idea) is in [`powerbi-model-plan.md`](powerbi-model-plan.md); PBIP setup steps are in [`powerbi/README.md`](../../powerbi/README.md); lesson outlines are in [`lessons-phase-2-4.md`](lessons-phase-2-4.md).

**Phase goal (M4):** PBIP committed; screenshots in the README; RLS demo. **Cert:** PL-300, schedulable in this phase or earlier.

| ID | Title | Blocked by | Est. |
|---|---|---|---|
| P4-01 | Connect Power BI to the marts and save the project in Git (PBIP) | P3-04 (first mart) | 1–2 |
| P4-02 | Star schema: relationships, date table, hidden keys | P4-01, P3-05, P3-09 | 1–2 |
| P4-03 | Compensation page: measures on a clean model | P4-02 | 2 |
| P4-04 | Benefits, payroll and recon exceptions pages; performance check | P4-02, P3-06, P3-07, P3-08 | 2 |
| P4-05 | Employee total rewards statement (drill-through) | P4-03, P3-09 | 1–2 |
| P4-06 | Row-level security: managers see only their team (M4) | P4-05 | 2 |

Labels on every Phase 4 ticket: `phase-4`, `powerbi`, `cert:PL-300`.

---

## P4-01 · Connect Power BI to the marts and save the project in Git (PBIP)

**Labels:** `phase-4`, `powerbi`, `cert:PL-300`, `git`
**Blocked by:** P3-04 (`fct_compa_ratio` exists); can start with one mart

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> Our current reports are files on someone's desktop, and nobody knows what changed between versions. The new report should be built on the tested tables and saved so every change can be reviewed like the SQL is.

### Acceptance criteria
- [ ] Choose how Power BI reads the marts and write an ADR with the options: (a) dbt exports marts as Parquet → Parquet connector, Import mode (proposed); (b) DuckDB ODBC driver; (c) a community DuckDB connector. Include what each means for Phase 6, when the marts move to Athena
- [ ] The data path has no user name in it and appears in one Power Query parameter (see `powerbi/README.md` step 3)
- [ ] `fct_compa_ratio` loaded; row count in Power BI matches `dbt show` / a DuckDB count
- [ ] Saved as PBIP in `powerbi/`; `git status` shows no `.pbix`, no cache, no local settings
- [ ] One small model change shown as a TMDL diff in the PR description
- [ ] PR with `Closes #N`

### Learning objective
- Import vs DirectQuery vs Direct Lake (when each fits; why Import here); Power Query parameters; PBIP and TMDL as source control for a model
- **Cert:** PL-300 "Prepare the data" (choose between DirectLake, DirectQuery and Import; create and modify parameters)

### Estimate
1–2 sessions.

---

## P4-02 · Star schema: relationships, date table, hidden keys

**Labels:** `phase-4`, `powerbi`, `cert:PL-300`
**Blocked by:** P4-01; P3-05 (`dim_employee`), P3-09 (`dim_date`)

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> Last year's model had arrows going in every direction and totals that changed depending on which slicer you touched first. Keep it simple: a few clean tables, related one way.

### Acceptance criteria
- [ ] All planned facts and dimensions loaded (or the subset that exists, listed in the PR)
- [ ] Relationships one-to-many, single direction, dimension → fact; no bi-directional filters, with the reason stated if you add one
- [ ] `dim_date` marked as the date table; any second date on a fact is an inactive relationship
- [ ] The SCD Type 2 employee key decision from `powerbi-model-plan.md` made and written as an ADR
- [ ] Keys and raw numeric columns hidden; a model-view screenshot in the PR
- [ ] PR with `Closes #N`

### Learning objective
- Star schema, cardinality, cross-filter direction, role-playing dates, date tables
- **Cert:** PL-300 "Model the data" (design and implement a data model)

### Estimate
1–2 sessions.

---

## P4-03 · Compensation page: measures on a clean model

**Labels:** `phase-4`, `powerbi`, `cert:PL-300`
**Blocked by:** P4-02

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> One page for the comp committee: average compa-ratio by department and grade, who's out of range, and what the merit cycle cost, with a switch to view it by department or by job.

### Acceptance criteria
- [ ] Measures you write for average compa-ratio, count out of range and merit cycle cost; each one ties to a dbt query result (show the check)
- [ ] A field parameter (or calculation group: try one, explain the choice) that switches the breakdown between department and job
- [ ] Measures in a display folder with descriptions
- [ ] Explain in the PR which logic you kept out of DAX because dbt already does it
- [ ] PR with `Closes #N`

### Learning objective
- Measures vs calculated columns; keeping DAX thin on a clean model; field parameters and calculation groups
- **Cert:** PL-300 "Model the data" (create model calculations by using DAX; calculation groups)

### Estimate
2 sessions.

---

## P4-04 · Benefits, payroll and recon exceptions pages; performance check

**Labels:** `phase-4`, `powerbi`, `cert:PL-300`
**Blocked by:** P4-02; P3-06, P3-07, P3-08

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> Three more views: what benefits cost per employee per month, whether payroll tied to the GL each period, and the open carrier exceptions with their dollar impact, biggest first. And it has to open fast.

### Acceptance criteria
- [ ] Benefits PEPM page (employer vs employee), payroll-vs-GL page (status by period), exceptions page (by reason code and dollar impact)
- [ ] Totals on each page tie to the matching mart (show the checks)
- [ ] Performance Analyzer run on each page; the slowest visual named and one change tried, with before/after times in the PR
- [ ] PR with `Closes #N`

### Learning objective
- Choosing visuals for a question; Performance Analyzer; why a clean model is usually the biggest performance win
- **Cert:** PL-300 "Visualize and analyze the data" (create reports; identify and fix performance issues)

### Estimate
2 sessions.

---

## P4-05 · Employee total rewards statement (drill-through)

**Labels:** `phase-4`, `powerbi`, `cert:PL-300`
**Blocked by:** P4-03; P3-09 (`fct_total_rewards_statement`)

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> From any list of people, I want to right-click a name and see that person's total rewards statement: salary, bonus, benefits we pay for, 401(k) match and PTO value, with a total.

### Acceptance criteria
- [ ] A drill-through page keyed on employee, reachable from the comp page and the exceptions page
- [ ] Each statement line ties to `fct_total_rewards_statement` for two employees you check by hand
- [ ] Synthetic employees only in screenshots; no file paths visible
- [ ] PR with `Closes #N`

### Learning objective
- Drill-through, page design for a single-entity report
- **Cert:** PL-300 "Visualize and analyze the data" (drill-through, report navigation)

### Estimate
1–2 sessions.

---

## P4-06 · Row-level security: managers see only their team (M4)

**Labels:** `phase-4`, `powerbi`, `cert:PL-300`
**Blocked by:** P4-05; a manager-access table built in dbt (add to P3-05 or a small new P3 ticket)

### Context
> From: Total Rewards Manager, Northwind Mutual
>
> We want to give people managers this report, but a manager must only ever see their own team's pay. Show me it works before anyone gets access.

### Acceptance criteria
- [ ] A Manager role with dynamic RLS on the employee dimension, using a manager-access table built and tested in dbt (synthetic sign-ins on the `example` domain)
- [ ] A Total Rewards role that sees everything
- [ ] Decision on facts with no employee key (see `powerbi-model-plan.md`), written in the PR
- [ ] "View as" tested for two managers; screenshots in the PR show different totals
- [ ] Short notes on how RLS behaves once published (workspace roles vs RLS roles, app audiences); nothing is published
- [ ] M4: PBIP committed, README screenshots, RLS demo; tick M4 in `docs/CURRICULUM.md`
- [ ] PR with `Closes #N`

### Learning objective
- Static vs dynamic RLS; where security logic should live (tested upstream vs in the model); deployment concepts
- **Cert:** PL-300 "Manage and secure Power BI" (implement row-level security; workspace and app access)

### Estimate
2 sessions.
