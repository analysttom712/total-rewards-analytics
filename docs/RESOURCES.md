# Resources

Curated links by topic. `/standup` picks 2–3 for the day's concept; add new ones only after checking they load. Prefer official docs.

<details>
<summary><b>Cert path</b></summary>

| Cert | Start here | Notes |
|---|---|---|
| **GH-900 GitHub Foundations** (now) | [Learning path: GitHub Foundations](https://learn.microsoft.com/en-us/training/paths/github-foundations/) · [Study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-900) · [Cert page](https://learn.microsoft.com/en-us/credentials/certifications/github-foundations/) | Modules include *Introduction to Git*, *Working with GitHub repositories*, *Collaboration features (issues, pull requests…)*. Pass mark 700. Check the cert page for current renewal rules. |
| **PL-300 Power BI Data Analyst** | [Cert page](https://learn.microsoft.com/en-us/credentials/certifications/data-analyst-associate/) | Phase 4 or sooner. |
| **AWS Cloud Practitioner (CLF-C02)** | [Cert page](https://aws.amazon.com/certification/certified-cloud-practitioner/) | Phase 6. Also clears WGU *Cloud Foundations*. |
| **dbt Analytics Engineering** | [dbt Learn](https://learn.getdbt.com/) | Phase 8. |

**Suggested GH-900 order (one module per session):** Introduction to Git → Introduction to GitHub → Working with GitHub repositories → Collaboration features. Each one matches something we've already done in the repo.

</details>

<details>
<summary><b>Git and GitHub</b></summary>

- [Pro Git book (free)](https://git-scm.com/book/en/v2): chapters 1–3 cover everything so far (commits, branches).
- [GitHub Docs: Get started](https://docs.github.com/en/get-started)
- [Linking a pull request to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue): closing keywords (`Closes #N`), and why they only work when the PR targets the default branch.
- [GitHub CLI manual](https://cli.github.com/manual/): `gh issue`, `gh pr create`, `gh pr merge`.
- [About merge methods on GitHub](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github): merge commit vs squash vs rebase (GH-900).

</details>

<details>
<summary><b>Python</b></summary>

- [The Python Tutorial](https://docs.python.org/3/tutorial/): section 3 (strings, lists), 4 (`for`, `range`, functions), 5 (dicts).
- [Python docs: strings](https://docs.python.org/3/tutorial/introduction.html#text): quotes, escaping, triple quotes.
- [f-strings](https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals)
- [pathlib](https://docs.python.org/3/library/pathlib.html): `Path`, `mkdir`.
- [threading: Lock objects](https://docs.python.org/3/library/threading.html#lock-objects): how a lock makes threads take turns (the hub fix in PR #33).

</details>

<details>
<summary><b>pandas</b></summary>

- [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html): the fastest tour.
- [Comparison with R](https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_r.html): tidyverse → pandas side by side.
- [Comparison with spreadsheets](https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_spreadsheets.html): Excel → pandas.
- [`to_datetime`](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html) · [`to_csv`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html)

</details>

<details>
<summary><b>Tools</b></summary>

- [Ruff docs](https://docs.astral.sh/ruff/): rule codes (search "F401", "I001").
- [pytest: Get started](https://docs.pytest.org/en/stable/getting-started.html): next ticket (#9).
- [Faker docs](https://faker.readthedocs.io/)
- [VS Code docs](https://code.visualstudio.com/docs)

</details>

<details>
<summary><b>Later phases</b></summary>

- [DuckDB docs](https://duckdb.org/docs/) (Phase 2)
- [dbt docs](https://docs.getdbt.com/) (Phase 3)
- [Power BI docs](https://learn.microsoft.com/en-us/power-bi/) (Phase 4)

</details>
