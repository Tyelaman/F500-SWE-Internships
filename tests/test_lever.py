from src.connectors.lever import normalize_lever_job


def test_normalizes_lever_internship():
    raw_job = {
        "id": "intern-123",
        "text": "Software Engineering Intern",
        "categories": {
            "location": "New York, NY",
            "commitment": "Intern",
            "team": "Engineering",
            "department": "Technology",
        },
        "applyUrl": "https://example.com/apply/intern-123",
    }

    job = normalize_lever_job(
        raw_job,
        company_name="Example Company",
        fortune_rank=100,
    )

    assert job is not None
    assert job.external_id == "intern-123"
    assert job.employment_type == "internship"
    assert job.category == "Software & IT"
    assert job.source == "lever"


def test_normalizes_lever_full_time_job():
    raw_job = {
        "id": "data-456",
        "text": "Senior Data Scientist",
        "categories": {
            "location": "Remote",
            "commitment": "Full-time",
            "team": "Data",
            "department": "Engineering",
        },
        "hostedUrl": "https://example.com/jobs/data-456",
    }

    job = normalize_lever_job(
        raw_job,
        company_name="Example Company",
        fortune_rank=100,
    )

    assert job is not None
    assert job.employment_type == "full-time"
    assert job.category == "Data & AI"
    assert job.location == "Remote"


def test_excludes_part_time_lever_job():
    raw_job = {
        "id": "part-time-789",
        "text": "Customer Support Associate",
        "categories": {
            "location": "Chicago, IL",
            "commitment": "Part-time",
        },
    }

    job = normalize_lever_job(
        raw_job,
        company_name="Example Company",
        fortune_rank=100,
    )

    assert job is None