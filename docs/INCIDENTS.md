# Incident Drills (planned breakage)

Moved out of CLAUDE.md. Read by `/incident`. The safety rules also stay in CLAUDE.md section 4a.

Thomas is preparing for real jobs, where pipelines break. Drills train troubleshooting. Run them with `/incident`.

**When they start:** only once there's something working to break. Each level unlocks when its phase milestone is done.

| Level | Unlocks after | Example faults |
|---|---|---|
| 1 | Phase 1, week 3 (generator runs) | Typo'd column name, wrong data type (salary as text), missing package, changed seed so tests fail |
| 2 | M2 (SQL set) | Join fan-out duplicating employees, NULLs dropping rows, off-by-one date filter, overlapping effective-dated rows |
| 3 | M3 (dbt green) | Broken `ref()`, upstream **HCM column rename** in a new extract, duplicate keys in a delta file, late-arriving pay period, a test turned off |
| 4 | M4 (Power BI) | Ambiguous relationship, RLS showing other teams, refresh fails after schema change, totals don't match the mart |
| 5 | M5 (CI) | CI red on main, merge conflict, a (fake) key staged for commit, flaky test |
| 6 | M6 (AWS) | IAM AccessDenied, new S3 partition not in the Glue catalog, Athena scan limit hit, Lambda timeout, wrong region, budget alert fired |
| 7 | M7+ | **Multi-fault "Monday morning Sev-1":** payroll delta + carrier file + GL tie-out all off; root cause spans layers; includes a stakeholder update email |

**Cadence:**
- Level 1–2: **one announced drill a week** ("today's ticket is an incident").
- From Level 3: **one drill a week, sometimes unannounced** (it shows up as a normal business ticket).
- At each phase milestone: an **"on-call week"** with 2–3 drills and a written postmortem for each.
- Never more than 2 drills a week. Never on a day Thomas says he's short on time. Never more than one level above what he's shown he can handle.

**Rules:** faults go only on an `incident/NNN` branch. They're always reversible, never touch `main` directly, never create billable AWS resources and never use real secrets. Every drill ends with a postmortem in `docs/incidents/` and a **new test that would have caught it**. That's the habit employers want to see.
