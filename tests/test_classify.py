from src.classify import classify_employment_type


def test_internship_titles():
    assert classify_employment_type("Software Engineering Intern") == "internship"
    assert classify_employment_type("Finance Internship") == "internship"
    assert classify_employment_type("Mechanical Engineering Co-op") == "internship"
    assert classify_employment_type("Product Design Coop") == "internship"


def test_full_time_titles():
    assert classify_employment_type("Senior Data Analyst") == "full-time"
    assert classify_employment_type("Manager, Internal Audit") == "full-time"
    assert classify_employment_type("International Sales Manager") == "full-time"


def test_excluded_titles():
    assert classify_employment_type("Part-Time Cashier") is None
    assert classify_employment_type("Contract Data Analyst") is None
    assert classify_employment_type("Temporary Warehouse Associate") is None
    assert classify_employment_type("Seasonal Delivery Driver") is None
