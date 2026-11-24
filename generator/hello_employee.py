"""Print one fake Northwind Mutual employee."""
from faker import Faker
from job_catalog import JOBS

Faker.seed(42)
fake = Faker()
job_row = fake.random_element(JOBS)

employee_id = 100001
name = fake.first_name() + " " + fake.last_name()
hire_date = fake.date_between(start_date='-10y', end_date='today')
salary = fake.pyint(min_value=job_row["salary_min"], max_value=job_row["salary_max"])

print(f"Employee ID: {employee_id}")
print(f"Name: {name}")
print(f"Hire Date: {hire_date}")
print(f"Job: {job_row['job_title']}")
print(f"Salary: ${salary:,}")
