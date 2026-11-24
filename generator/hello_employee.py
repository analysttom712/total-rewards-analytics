"""Print ten fake Northwind Mutual employees."""

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
for employee_id in range(100001, 100011):
    employees.append(make_employee(employee_id))
print(len(employees))
print(employees[0])
print(employees[-1])

for employee in employees:
    print(employee)
