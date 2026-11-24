# Architecture Decisions

Short records: decision · options considered · why. These are interview talking points.

## ADR-001: Job catalog starts as a Python constant (2026-11-23)
- **Decision:** the job catalog (job code, title, grade, salary min/max) is a list of dicts in `generator/job_catalog.py`.
- **Options:** Python constant; a CSV the generator reads; a dbt seed.
- **Why:** five rows, read only by the generator, and it teaches lists and dicts. When the catalog grows and dbt needs the ranges (the `comp_grade_ranges` raw table, compa-ratio marts), the generator will write it out as a raw table, the way a real HCM extract would deliver it.
