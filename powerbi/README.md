# Power BI (Phase 4, planned)

The Total Rewards report and semantic model will live here as a **Power BI Project (PBIP)**: plain-text files Git can diff, instead of one binary `.pbix`. The model plan is in [`docs/backlog/powerbi-model-plan.md`](../docs/backlog/powerbi-model-plan.md); the tickets are in [`docs/backlog/phase-4.md`](../docs/backlog/phase-4.md).

Nothing is built yet. These are the setup steps for P4-01.

## Setup: save the model as PBIP with TMDL

1. **Power BI Desktop, current version.** Check *File → Options and settings → Options → Preview features*. If you see "Power BI Project (.pbip) save option", "Store semantic model using TMDL format" or "Store reports using enhanced metadata format (PBIR)", turn them on and restart. If they aren't listed, they've become standard in your version and there's nothing to turn on.
2. **Connect to the marts** (method decided in P4-01; the proposal is Parquet files exported from the dbt marts, read with the Parquet connector in Import mode).
3. **Use a folder path with no user name in it.** The public-repo scan blocks home-folder paths, and the PBIP files store the data source path in plain text. Put the exported marts somewhere neutral (for example `C:\data\northwind\marts\`) and point a Power Query parameter at it, so the path appears once and is easy to change.
4. **Save as a project:** *File → Save as → Power BI project files (\*.pbip)*, into this `powerbi/` folder, named `NorthwindTotalRewards`. You'll get:

   ```text
   powerbi/
     NorthwindTotalRewards.pbip              the file you open
     NorthwindTotalRewards.SemanticModel/    the model: tables, relationships, measures (TMDL text files)
     NorthwindTotalRewards.Report/           the report pages and visuals
   ```

5. **Check what Git will see** before the first commit: `git status`. The root `.gitignore` already excludes `**/.pbi/localSettings.json` and `**/.pbi/cache.abf` (your local settings and the imported data cache). Power BI may also write its own `.gitignore` in the project folder; keep it. No `.pbix` file and no data file should be listed.
6. **Commit, then make one small change** (rename a measure or add a description) and look at `git diff`. You'll see the change as a few lines of TMDL, which is how a reviewer will read your model changes in a PR.
7. **Run the public scan's by-eye check on screenshots** before they go in the README: synthetic names only, no file paths, no real company names in titles.

## What never goes in this folder

- `.pbix` files (binary, no useful diff) and any exported data
- Real names, real pay data, or any employer or vendor branding (CLAUDE.md sections 2 and 2a)
- Credentials: Parquet files need none, and an ODBC route must not store one in the model

## References

- [Power BI Desktop projects (PBIP)](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview)
- [Semantic model folder and TMDL](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset)
- [TMDL overview](https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview)
