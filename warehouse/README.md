# Local warehouse (DuckDB)

This folder holds the local DuckDB database file for Phases 2–5. DuckDB stands in for AWS Athena until Phase 6: same SQL ideas, no cloud bill.

| File | What it is | In Git? |
|---|---|---|
| `northwind.duckdb` | The database: raw tables loaded from `data/raw/` (Phase 2), then dbt's staging, intermediate and mart models (Phase 3) | **No.** Gitignored (`warehouse/*.duckdb`). Rebuild it from the generator |
| `northwind.duckdb.wal` | DuckDB's write-ahead log, present while a write is in progress | No (gitignored) |
| `README.md` | This file | Yes |

## Rules

- **Never commit the database.** It is generated data, like `data/raw/` (CLAUDE.md rule 9). Delete it and rebuild whenever you like: `python -m generator`, then the load step from ticket P2-02.
- **One writer at a time.** DuckDB lets one process open the file for writing. If a query says the file is locked, close the other tool (a Python session, the DuckDB CLI, VS Code, or Power BI) first.
- **The file name is a decision, not a law.** `northwind.duckdb` is the proposed name; P2-02 and the dbt profile (P3-01) both point here, so change it in both places if you rename it.

Power BI connects to the marts through exported Parquet files instead of this file directly; see [`powerbi/README.md`](../powerbi/README.md).
