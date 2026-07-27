from src.models import Job
from src.pipeline import deduplicate_jobs


def create_job(external_id: str) -> Job:
    return Job(
        company="Example Company",
        fortune_rank=100,
        title="Software Engineer",
        location="New York, NY",
        url="https://example.com/jobs/123",
        source="greenhouse",
        external_id=external_id,
        employment_type="full-time",
        category="Software & IT",
    )


def test_removes_exact_duplicates():
    first_job = create_job("123")
    duplicate_job = create_job("123")

    jobs = deduplicate_jobs([first_job, duplicate_job])

    assert len(jobs) == 1


def test_keeps_different_external_ids():
    first_job = create_job("123")
    second_job = create_job("456")

    jobs = deduplicate_jobs([first_job, second_job])

    assert len(jobs) == 2