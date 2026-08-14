from src import http as requests
from src.categories import classify_job_category
from src.classify import classify_employment_type
from src.models import Job

BASE_URL = "https://api.lever.co/v0/postings"


def fetch_lever_jobs(site_name: str) -> list[dict]:
    url = f"{BASE_URL}/{site_name}"

    response = requests.get(
        url,
        params={"mode": "json"},
        timeout=20,
    )

    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list):
        return []

    return data


def get_lever_description(raw_job: dict) -> str:
    parts = [raw_job.get("descriptionPlain") or raw_job.get("description") or ""]
    for item in raw_job.get("lists") or []:
        parts.extend((item.get("text", ""), item.get("content", "")))
    parts.append(raw_job.get("additionalPlain") or raw_job.get("additional") or "")
    return " ".join(part for part in parts if part)


def normalize_lever_job(
    raw_job: dict,
    company_name: str,
    fortune_rank: int,
) -> Job | None:
    title = raw_job.get("text", "Unknown Position")
    categories = raw_job.get("categories") or {}

    location = categories.get("location") or "Unknown"
    commitment = categories.get("commitment") or ""
    team = categories.get("team") or ""
    department = categories.get("department") or ""

    employment_text = f"{title} {commitment}"
    employment_type = classify_employment_type(employment_text)

    if employment_type is None:
        return None

    category_text = f"{title} {team} {department}"
    category = classify_job_category(category_text)

    return Job(
        company=company_name,
        fortune_rank=fortune_rank,
        title=title,
        location=location,
        url=(raw_job.get("applyUrl") or raw_job.get("hostedUrl", "")),
        source="lever",
        external_id=str(raw_job.get("id", "")),
        employment_type=employment_type,
        category=category,
        updated_at="",
    )
