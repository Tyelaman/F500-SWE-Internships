import requests

from src.classify import classify_employment_type
from src.models import Job

BASE_URL = "https://boards-api.greenhouse.io/v1/boards"


def fetch_greenhouse_jobs(board_token: str) -> list[dict]:
    url = f"{BASE_URL}/{board_token}/jobs"

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    data = response.json()

    return data.get("jobs", [])

def normalize_greenhouse_job(
    raw_job: dict,
    company_name: str,
    fortune_rank: int,
) -> Job | None:
    title = raw_job.get("title", "Unknown Position")
    location = raw_job.get("location", {}).get("name", "Unknown")

    employment_type = classify_employment_type(title)

    if employment_type is None:
        return None

    return Job(
        company=company_name,
        fortune_rank=fortune_rank,
        title=title,
        location=location,
        url=raw_job.get("absolute_url", ""),
        source="greenhouse",
        external_id=str(raw_job.get("id", "")),
        employment_type=employment_type,
        updated_at=raw_job.get("updated_at", ""),
    )