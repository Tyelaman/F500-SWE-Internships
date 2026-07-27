import pytest

from src.connectors.workday import parse_workday_url
from src.connectors.workday import fetch_workday_jobs
from src.connectors.workday import normalize_workday_job


def test_parses_workday_url():
    config = parse_workday_url(
        "https://workday.wd5.myworkdayjobs.com/en-US/Workday"
    )

    assert config["base_url"] == (
        "https://workday.wd5.myworkdayjobs.com"
    )
    assert config["tenant"] == "workday"
    assert config["locale"] == "en-US"
    assert config["site"] == "Workday"


def test_rejects_invalid_workday_url():
    with pytest.raises(ValueError):
        parse_workday_url("not-a-url")


def test_rejects_url_without_site():
    with pytest.raises(ValueError):
        parse_workday_url(
            "https://example.wd5.myworkdayjobs.com/en-US"
        )

class FakeResponse:
    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self.data


def test_fetches_all_workday_pages(monkeypatch):
    requested_offsets = []

    def fake_post(url, json, timeout):
        requested_offsets.append(json["offset"])

        if json["offset"] == 0:
            return FakeResponse(
                {
                    "total": 3,
                    "jobPostings": [
                        {
                            "title": "Software Engineer",
                            "externalPath": "/job/software-engineer",
                        },
                        {
                            "title": "Data Analyst",
                            "externalPath": "/job/data-analyst",
                        },
                    ],
                }
            )

        return FakeResponse(
            {
                "total": 3,
                "jobPostings": [
                    {
                        "title": "Product Manager",
                        "externalPath": "/job/product-manager",
                    }
                ],
            }
        )

    monkeypatch.setattr(
        "src.connectors.workday.requests.post",
        fake_post,
    )

    jobs = fetch_workday_jobs(
        "https://example.wd5.myworkdayjobs.com/en-US/Careers"
    )

    assert len(jobs) == 3
    assert requested_offsets == [0, 2]
    assert jobs[0]["title"] == "Software Engineer"

    assert jobs[0]["_workday_config"]["tenant"] == "example"
    assert jobs[0]["_workday_config"]["site"] == "Careers"

def test_normalizes_workday_internship():
    raw_job = {
        "title": "Software Engineering Intern",
        "locationsText": "Boston, MA",
        "postedOn": "Posted 2 Days Ago",
        "bulletFields": [
            "Full time",
            "R-12345",
        ],
        "externalPath": (
            "/job/Boston-MA/"
            "Software-Engineering-Intern_R-12345"
        ),
        "_workday_config": {
            "base_url": (
                "https://example.wd5.myworkdayjobs.com"
            ),
            "tenant": "example",
            "locale": "en-US",
            "site": "Careers",
        },
    }

    job = normalize_workday_job(
        raw_job=raw_job,
        company_name="Example Company",
        fortune_rank=100,
    )

    assert job is not None
    assert job.company == "Example Company"
    assert job.employment_type == "internship"
    assert job.category == "Software & IT"
    assert job.location == "Boston, MA"
    assert job.source == "workday"
    assert job.external_id == raw_job["externalPath"]

    assert job.url == (
        "https://example.wd5.myworkdayjobs.com"
        "/en-US/Careers"
        "/job/Boston-MA/"
        "Software-Engineering-Intern_R-12345"
    )

def test_normalizes_workday_full_time_job():
    raw_job = {
        "title": "Senior Data Scientist",
        "locationsText": "New York, NY",
        "bulletFields": [
            "Full time",
            "R-45678",
        ],
        "externalPath": (
            "/job/New-York-NY/"
            "Senior-Data-Scientist_R-45678"
        ),
        "_workday_config": {
            "base_url": (
                "https://example.wd5.myworkdayjobs.com"
            ),
            "tenant": "example",
            "locale": "en-US",
            "site": "Careers",
        },
    }

    job = normalize_workday_job(
        raw_job=raw_job,
        company_name="Example Company",
        fortune_rank=100,
    )

    assert job is not None
    assert job.employment_type == "full-time"
    assert job.category == "Data & AI"

def test_excludes_part_time_workday_job():
    raw_job = {
        "title": "Customer Support Associate",
        "locationsText": "Chicago, IL",
        "bulletFields": ["Part-time"],
        "externalPath": "/job/support-associate",
        "_workday_config": {
            "base_url": (
                "https://example.wd5.myworkdayjobs.com"
            ),
            "tenant": "example",
            "locale": "en-US",
            "site": "Careers",
        },
    }

    job = normalize_workday_job(
        raw_job=raw_job,
        company_name="Example Company",
        fortune_rank=100,
    )

    assert job is None