"""Print one fake Northwind Mutual employee."""
from faker import Faker

Faker.seed(42)
fake = Faker()

employee_id = 100001
name = fake.first_name() + " " + fake.last_name()
hire_date = fake.date_between(start_date='-10y', end_date='today')
job = "Compensation Analyst"
salary = 120000

print(f"Employee ID: {employee_id}")
print(f"Name: {name}")
print(f"Hire Date: {hire_date}")
print(f"Job: {job}")
print(f"Salary: ${salary:,}")
 
