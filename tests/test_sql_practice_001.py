"""Test-first check for backlog ticket P2-01 (docs/backlog/phase-2.md).

Thomas writes the SQL in sql/practice/001_job_pay_ranges.sql. This file only
states what the Total Rewards manager expects to see; it does not say how.

The test is skipped until the ticket starts. To start P2-01, delete the
`pytestmark = pytest.mark.skip(...)` line below, run `python -m pytest`, and
read the failure before writing any SQL.

The expected numbers are golden values taken from today's job catalog
(generator/job_catalog.py). If the catalog changes, these values change with it.
"""

import importlib.util
from pathlib import Path

import duckdb
import pytest

pytestmark = pytest.mark.skip(
    reason="Test-first exercise for backlog ticket P2-01: delete this line to start it"
)

REPO = Path(__file__).resolve().parents[1]
SQL_FILE = REPO / "sql" / "practice" / "001_job_pay_ranges.sql"
CATALOG_FILE = REPO / "generator" / "job_catalog.py"
CATALOG_COLUMNS = ("job_code", "job_title", "grade", "salary_min", "salary_max")


def load_jobs() -> list[dict]:
    """Read JOBS straight from the catalog file, wherever the package layout ends up."""
    spec = importlib.util.spec_from_file_location("job_catalog", CATALOG_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.JOBS


@pytest.fixture
def result() -> list[dict]:
    """Run Thomas's query against an in-memory hr_job table; one dict per result row."""
    if not SQL_FILE.exists():
        pytest.fail(f"Create {SQL_FILE.relative_to(REPO)} (copy sql/practice/_template.sql)")

    con = duckdb.connect()  # in memory: nothing is written to disk
    con.execute(
        "create table hr_job (job_code integer, job_title varchar, grade integer, "
        "salary_min integer, salary_max integer)"
    )
    rows = [tuple(job[col] for col in CATALOG_COLUMNS) for job in load_jobs()]
    con.executemany("insert into hr_job values (?, ?, ?, ?, ?)", rows)

    cursor = con.execute(SQL_FILE.read_text(encoding="utf-8"))
    names = [column[0] for column in cursor.description]
    return [dict(zip(names, values)) for values in cursor.fetchall()]


def row_for(result: list[dict], job_title: str) -> dict:
    matches = [row for row in result if row["job_title"] == job_title]
    assert len(matches) == 1, f"expected exactly one row for {job_title!r}"
    return matches[0]


def test_one_row_per_job(result):
    # The manager wants every job in the catalog, each listed once.
    assert len(result) == len(load_jobs())
    assert len({row["job_code"] for row in result}) == len(result)


def test_shows_the_columns_the_manager_asked_for(result):
    expected = {"job_code", "job_title", "grade", "salary_min", "range_midpoint",
                "salary_max", "range_spread_pct"}
    assert expected <= set(result[0])


def test_range_midpoint_matches_the_published_ranges(result):
    # Golden values: the midpoint the comp team publishes for these two jobs.
    assert row_for(result, "Total Rewards Manager")["range_midpoint"] == 135000
    assert row_for(result, "Payroll Coordinator")["range_midpoint"] == 82500


def test_range_spread_is_a_percent_with_one_decimal(result):
    # Golden values: how wide each range is, as a percent, rounded to one decimal.
    assert float(row_for(result, "Compensation Analyst")["range_spread_pct"]) == 25.0
    assert float(row_for(result, "Benefits Specialist")["range_spread_pct"]) == 16.7


def test_highest_grade_is_listed_first(result):
    grades = [row["grade"] for row in result]
    assert grades == sorted(grades, reverse=True)
