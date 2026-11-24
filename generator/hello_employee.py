"""Print 25 fake Northwind Mutual employees and create a dataframe for them."""

from pathlib import Path

import pandas as pd
from faker import Faker
from job_catalog import JOBS

Faker.seed(42)
fake = Faker()


def make_employee(employee_id: int) -> dict:
    """Generate a fake employee record."""
    job_row = fake.random_element(JOBS)
    name = fake.first_name() + " " + fake.last_name()
    hire_date = fake.date_between(start_date="-10y", end_date="today")
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


employees = []
for employee_id in range(100001, 100026):
    employees.append(make_employee(employee_id))
df = pd.DataFrame(employees)
df["hire_date"] = pd.to_datetime(df["hire_date"])
print(df.head())
print(df.shape)
print(df.dtypes)
Path("data/raw").mkdir(parents=True, exist_ok=True)
df.to_csv("data/raw/employees.csv", index=False)
