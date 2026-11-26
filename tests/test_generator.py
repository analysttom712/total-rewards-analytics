from hello_employee import build_employees
from job_catalog import JOBS


def test_same_seed_same_employees():
    first = build_employees(25)
    second = build_employees(25)
    assert first == second


def test_employee_ids_are_unique():
    employees = build_employees(25)
    ids = []
    for e in employees:
        ids.append(e["employee_id"])
    assert len(ids) == len(set(ids))


def test_salaries_inside_pay_range():
    employees = build_employees(25)
    for e in employees:
        for job in JOBS:
            if job["job_code"] == e["job_code"]:
                assert job["salary_min"] <= e["salary"] <= job["salary_max"]
