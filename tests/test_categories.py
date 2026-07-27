from src.categories import classify_job_category


def test_software_categories():
    assert classify_job_category("Backend Software Engineer") == "Software & IT"
    assert classify_job_category("Cybersecurity Analyst") == "Software & IT"


def test_data_categories():
    assert classify_job_category("Machine Learning Engineer") == "Data & AI"
    assert classify_job_category("Senior Data Scientist") == "Data & AI"


def test_business_categories():
    assert classify_job_category("Financial Analyst") == "Finance & Accounting"
    assert classify_job_category("Marketing Manager") == "Sales & Marketing"
    assert (
        classify_job_category("Supply Chain Coordinator")
        == "Operations & Supply Chain"
    )


def test_unknown_category():
    assert classify_job_category("Regional General Manager") == "Other"