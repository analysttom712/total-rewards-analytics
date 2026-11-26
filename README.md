# Total Rewards Analytics Platform

A build-in-public analytics engineering project: a Total Rewards (compensation, benefits, payroll, PTO) analytics platform for a fictional company, **Northwind Mutual**, simulating an **HCM → AWS** data integration, built with **Python, SQL, dbt, Power BI, GitHub Actions and AWS**.

> All data in this repository is **synthetic**, generated with Python/Faker. No real people, employers or carriers are represented.

## The business problem
Total Rewards teams answer questions like: *Are we paying people inside their ranges? What does our benefits program cost per employee? Does payroll tie to the general ledger? Does our carrier's eligibility file match who we actually cover? What is each employee's total compensation package worth?* This project builds the data platform that answers them, with automated tests that catch the errors a reconciliation analyst would otherwise find by hand.

## Status
Day 5, Phase 1 (the data generator). Built and passing so far:
- A seeded Python generator (Faker) that creates fictional employees with unique IDs, a job from a 5-job catalog, and a salary inside that job's pay band
- 25 employees written to a CSV with pandas
- pytest tests proving the output is reproducible, the employee IDs are unique and every salary sits inside its pay band

Next: run the generator as of a fixed date, so re-runs on different days produce identical files. Follow along in [`docs/blog/`](docs/blog/) and the [learning log](docs/LEARNING_LOG.md).

## Working in this repo
One-time setup after cloning, from the repo root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
git config core.hooksPath .githooks
```

The last line turns on the pre-commit hook in `.githooks/`. Every commit runs
`scripts/public_scan.py` (secrets, account IDs, SSN-shaped numbers, home-folder
paths, and any word in your local, gitignored `.scan-blocklist.local.txt`), which
blocks the commit on a hit. It also runs `ruff check`, which only reports, so work
in progress can always be committed to a branch. CI (`.github/workflows/checks.yml`)
runs the scan, ruff and pytest on every pull request and on every push to `main`,
and lint errors block the merge there.

CI reads the blocklist from a repository secret named `SCAN_BLOCKLIST` (the same
content as `.scan-blocklist.local.txt`, one word per line) and fails if the secret
is missing. To set or update it:

```powershell
Get-Content .scan-blocklist.local.txt -Raw | gh secret set SCAN_BLOCKLIST
```

## Learning hub (local study site)
A small local site that lays the learning docs out like a course. It builds
every page from `docs/` when you open it, so it is never a second copy. From
the repo root, with the venv on:

```powershell
python -m hub
```

Then open <http://127.0.0.1:8765>. In VS Code: **Terminal → Run Task… → Start learning hub**.

Answers typed on the site save to `hub/progress.local.json`, which is gitignored.
`python -m hub --progress` prints what is saved. The plan is in
[`docs/site/BRIEF.md`](docs/site/BRIEF.md).

## Roadmap
See [`docs/CURRICULUM.md`](docs/CURRICULUM.md): Python data generator → SQL → dbt → Power BI → CI → AWS (S3/Glue/Athena) → incremental loads & PySpark.

## Acknowledgments
How this repo works with AI (a short always-loaded instruction file, rules enforced
by tools instead of wording, alignment before building, thin end-to-end slices) is
adapted from ideas in two AI Engineer talks:

- Matt Pocock, [Full Walkthrough: Workflow for AI Coding](https://youtu.be/-QFHIoCo-Ko)
- Lydia Hallie, [Rethinking Claude Code Best Practices](https://youtu.be/vlfCjWuv4es)

## Author
Thomas Baynum · [GitHub](https://github.com/analysttom712)
