"""Print 25 fake Northwind Mutual employees and create a dataframe for them."""

from datetime import date
from pathlib import Path

import pandas as pd
from faker import Faker
from job_catalog import JOBS

AS_OF = date(2026, 11, 1)
EARLIEST_HIRE = date(2016, 11, 1)

fake = Faker()


def build_employees(count: int) -> list:
    """Build 'count' fake employees, starting from the same seed everytime"""
    Faker.seed(42)
    employees = []
    for employee_id in range(100001, 100001 + count):
        employees.append(make_employee(employee_id))
    return employees


def make_employee(employee_id: int) -> dict:
    """Generate a fake employee record."""
    job_row = fake.random_element(JOBS)
    name = fake.first_name() + " " + fake.last_name()
    hire_date = fake.date_between(start_date=EARLIEST_HIRE, end_date=AS_OF)
    salary = fake.pyint(
        min_value=job_row["salary_min"], max_value=job_row["salary_max"]
    )

    return {
        "employee_id": employee_id,
        "name": name,
        "hire_date": hire_date,
        "job_code": job_row["job_code"],
        "job_title": job_row["job_title"],
        "grade": job_row["grade"],
        "salary": salary,
    }


def main() -> None:
    """Generate the employees, show a preview and write the CSV."""
    employees = build_employees(25)
    df = pd.DataFrame(employees)
    df["hire_date"] = pd.to_datetime(df["hire_date"])
    print(df.head())
    print(df.shape)
    print(df.dtypes)
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    df.to_csv("data/raw/employees.csv", index=False)


if __name__ == "__main__":
    main()
