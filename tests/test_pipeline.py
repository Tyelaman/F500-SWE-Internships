from src.models import Job
from src.pipeline import deduplicate_jobs, fetch_descriptions


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


def test_concurrent_descriptions_preserve_input_order(monkeypatch):
    worker_counts = []

    class FakeExecutor:
        def __init__(self, max_workers):
            worker_counts.append(max_workers)

        def __enter__(self):
            return self

        def __exit__(self, *_):
            return None

        def map(self, function, values):
            return [function(value) for value in reversed(list(values))][::-1]

    monkeypatch.setattr("src.pipeline.ThreadPoolExecutor", FakeExecutor)
    results = fetch_descriptions(
        [{"id": "first"}, {"id": "second"}],
        lambda raw_job: raw_job["id"],
        concurrent=True,
    )

    assert worker_counts == [8]
    assert results == [("first", None), ("second", None)]


def test_description_failure_is_isolated():
    def get_description(raw_job):
        if raw_job["id"] == "bad":
            raise ValueError("bad detail")
        return raw_job["id"]

    results = fetch_descriptions(
        [{"id": "good"}, {"id": "bad"}],
        get_description,
        concurrent=False,
    )

    assert results[0] == ("good", None)
    assert results[1][0] == ""
    assert isinstance(results[1][1], ValueError)
