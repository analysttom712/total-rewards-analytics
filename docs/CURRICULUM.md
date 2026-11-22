# Curriculum: Analytics Engineer track (about 2 hours a day, about 12 months)

Week counts assume 5 sessions a week. If life happens, the order matters more than the dates. Each phase ends with a **milestone** (something that works) and a **check** (Thomas explains it out loud as if in an interview).

Cert exams are scheduled when the skills are there. A target window is listed for each.

---

## Phase 0: Setup and Git basics (week 1)
**Learn:** what Git is (commits, branches, remotes), GitHub repos, issues, pull requests, `.gitignore`, the GitHub CLI.
**Build:** create the repo, venv, folder structure, first README, first issue → branch → PR → merge.
**Milestone:** M0: `python --version`, `git log`, `gh pr list` all work; first PR merged.
**Cert tie-in:** GH-900 (Git basics, repositories, collaboration). Take GH-900 by end of Phase 1. The fee is waived for students verified through GitHub Education, so get verified while still enrolled.

## Phase 1: Python fundamentals through the data generator (weeks 2–5)
**Learn:** Python basics (variables, lists, dicts, loops, functions), modules, virtual environments, pandas DataFrames, writing CSV/Parquet, Faker, random seeds, simple tests with pytest, linting with ruff. Compare each one to the R/tidyverse he knows.
**Build:**
- `generator/` package: org structure → jobs and grades → employees with hire, term and death events → salary history → benefits elections → payroll runs → 401(k) → PTO → GL
- Plant the anomalies and write `_answer_key.csv`
- pytest checks: row counts, no duplicate IDs, the seed reproduces the same output
**Milestone:** M1: `python -m generator` writes every raw table plus the answer key, reproducibly.
**Check:** explain why a fixed seed matters, and how the generator creates effective-dated history.

## Phase 2: SQL for analytics engineering (weeks 6–10)
**Learn (in DuckDB):** SELECT/WHERE/GROUP BY review, all join types (and how joins duplicate rows), CTEs, CASE, window functions (ROW_NUMBER, LAG, running totals, ranking), date logic, effective-dated as-of joins, deduplication patterns, null handling, set operations, query-plan basics.
**Build:** a `sql/practice/` folder of answered business questions against raw data:
- Compa-ratio by employee as of a date
- Merit increase % by department
- Gross-to-net for one pay period
- Find carrier members not in HR
- Payroll vs. GL by period
**Milestone:** M2: 20 practice queries, each with the business question, the SQL and the expected result.
**Check:** explain an as-of join and a window-function dedupe without notes.

## Phase 3: dbt core (weeks 11–17)
**Learn:**
- dbt project structure, sources and `ref()`, staging/intermediate/marts layering
- materializations (view, table, ephemeral, incremental)
- generic and singular tests; `dbt_utils`
- seeds, Jinja and macros (`as_of_filter`)
- snapshots (SCD Type 2) for job/comp history
- docs and lineage, `dbt build` vs. `run`/`test`, selectors
**Build:**
- all staging models
- intermediate as-of models
- marts for comp, benefits, payroll, recon and total rewards
- 40+ tests, including `assert_all_planted_anomalies_caught`
**Milestone:** M3: `dbt build` green (documented warnings only); lineage graph screenshot in the README.
**Check:** explain the layering choices, one snapshot and the headline anomaly test.
**Cert tie-in:** this phase is most of the dbt Analytics Engineering exam outline. dbt recommends about 6 months of dbt experience, so target the exam in **Phase 8**.

## Phase 4: Power BI on the marts (weeks 18–22)
**Learn:**
- Connecting to DuckDB/Parquet; star schema from the marts
- DAX on a clean model (most logic now lives upstream in dbt; teach why)
- Calculation groups or field parameters
- Row-level security (managers see only their team)
- PBIP/TMDL format saved in Git
- Deployment concepts; performance analyzer
**Build:**
- **Total Rewards dashboard:** comp, benefits cost, payroll, recon exceptions
- **Employee total rewards statement** page (drill-through)
- RLS roles
**Milestone:** M4: PBIP committed; screenshots in the README; RLS demo.
**Cert tie-in:** **PL-300.** Schedule it in this phase, or earlier: Thomas's daily work already covers most of it. Focus extra study on RLS, workspace/app deployment, Direct Lake vs. DirectQuery vs. Import, and Copilot items.

## Phase 5: Engineering practices (weeks 23–26)
**Learn:**
- GitHub Actions CI: run ruff, pytest and `dbt build` on every PR
- Branch protection; code review habits
- `dbt source freshness`
- Data contracts and model versioning (concepts)
- Writing ADRs in `docs/DECISIONS.md`
- Basic orchestration ideas (what Airflow, Dagster and Step Functions do)
**Build:** `.github/workflows/ci.yml`; a PR template; a failing-test demo PR that CI blocks.
**Milestone:** M5: CI green badge in the README; a PR blocked by a failing test, then fixed.

## Phase 6: AWS (weeks 27–34)
**Learn (cost guardrails first):**
- AWS account, root MFA, IAM users/roles and least privilege, AWS Budgets
- S3, Glue Data Catalog, Athena; Parquet and partitioning; Athena scan limits
- boto3 basics; the dbt Athena adapter; dbt cross-database macros (`adapter.dispatch`)
- GitHub Actions to AWS with OIDC (no stored keys)
**Build (the HCM → AWS integration):**
0. Mock HCM REST API (FastAPI, local) with paging, plus full and delta extract files from the generator
1. $5 budget alert → S3 bucket (`raw/hcm/<object>/extract_date=.../`, results/) → Python ingestion script (boto3) that pulls the mock API and extract files and lands them unchanged, then writes partitioned Parquet
1b. Package the ingestion as an AWS Lambda on an EventBridge schedule (free-tier sized). Document the real-world SFTP/Transfer Family pattern in DECISIONS.md, but don't create it (hourly billing)
2. Glue catalog → Athena workgroup with a scan limit
3. `dbt build --target athena` with the same models (fix dialect gaps with macros)
4. `aws/teardown.md` + `aws/iam-policy.json`
**Milestone:** M6: same dbt project green on both DuckDB and Athena; teardown tested.
**Cert tie-in:** **AWS Cloud Practitioner (CLF-C02)** early in this phase. Start an AWS Data Engineer Associate study list (S3, Glue, Athena, IAM, Lambda, Kinesis concepts), but don't take it yet; AWS recommends years of hands-on work.

## Phase 7: Data engineering stretch (weeks 35–42)
**Learn:**
- Incremental loads and change data capture patterns (new pay periods arrive monthly)
- Idempotent pipelines; ingestion from a mock API (a small FastAPI or JSON files)
- Python data validation (pydantic or pandera)
- **PySpark basics locally** (DataFrames, transformations), because DP-700 and data engineering roles expect it
- Optional: rebuild one domain in a **Microsoft Fabric free trial** (lakehouse → semantic model) for DP-600 practice
**Build:**
- An incremental dbt model for `payroll_results`
- A mock "new pay period arrives" pipeline
- One PySpark job that produces the same output as a dbt model (compare them)
- Optional Fabric lakehouse version
**Milestone:** M7: incremental loads work; PySpark job matches the dbt output.
**Cert tie-in:** **DP-600** if the Fabric trial is used (lakehouse, T-SQL, KQL, semantic models).

## Phase 8: Capstone polish and career (weeks 43–48)
**Learn:** telling the project story; interview walkthroughs; system-design basics for analytics engineering.
**Build:**
- Final README (problem → architecture → what tests catch → screenshots → what I'd do next)
- A 5-minute demo video script
- `docs/RESUME_LINES.md` finalized from real results
- Mock interviews: dbt, SQL live-coding, "walk me through your pipeline"
**Milestone:** M8: repo public and polished; demo recorded.
**Cert tie-in:** **dbt Analytics Engineering exam** (about 6 months of dbt by now). Plan the AWS Data Engineer Associate and DP-700 for year 2, on the job.

---

## Milestone checklist
- [ ] M0 Setup + first PR
- [ ] M1 Data generator + answer key
- [ ] M2 SQL practice set
- [ ] M3 dbt build green + lineage
- [ ] M4 Power BI + total rewards statement + RLS
- [ ] M5 CI on every PR
- [ ] M6 Same project on AWS Athena + teardown
- [ ] M7 Incremental + PySpark parity
- [ ] M8 Public, polished, demo recorded

## Cert checklist (target windows)
- [ ] GH-900 GitHub Foundations: end of Phase 1 (free while a verified student)
- [ ] PL-300: Phase 4 or sooner
- [ ] CLF-C02 AWS Cloud Practitioner: Phase 6
- [ ] DP-600 Fabric Analytics Engineer: Phase 7 (optional Fabric trial)
- [ ] dbt Analytics Engineering: Phase 8
- [ ] Year 2: AWS Data Engineer Associate, DP-700
