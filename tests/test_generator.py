from hello_employee import build_employees


def test_same_seed_same_employees():
    first = build_employees(25)
    second = build_employees(25)
    assert first == second
