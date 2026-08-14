from urllib.parse import urlparse

from src import http as requests
from src.categories import classify_job_category
from src.classify import classify_employment_type
from src.models import Job

PAGE_SIZE = 20


def parse_workday_url(careers_url: str) -> dict[str, str]:
    parsed_url = urlparse(careers_url)

    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValueError("Invalid Workday careers URL")

    host_parts = parsed_url.netloc.split(".")

    if len(host_parts) < 4:
        raise ValueError("Invalid Workday hostname")

    tenant = host_parts[0]

    path_parts = [part for part in parsed_url.path.split("/") if part]

    if len(path_parts) < 2:
        raise ValueError("Workday URL must contain a locale and site name")

    locale = path_parts[0]
    site = path_parts[1]

    return {
        "base_url": (f"{parsed_url.scheme}://{parsed_url.netloc}"),
        "tenant": tenant,
        "locale": locale,
        "site": site,
    }


def fetch_workday_jobs(careers_url: str) -> list[dict]:
    config = parse_workday_url(careers_url)

    endpoint = f"{config['base_url']}/wday/cxs/{config['tenant']}/{config['site']}/jobs"

    jobs = []
    offset = 0

    while True:
        response = requests.post(
            endpoint,
            json={
                "appliedFacets": {},
                "limit": PAGE_SIZE,
                "offset": offset,
                "searchText": "",
            },
            timeout=20,
        )

        response.raise_for_status()
        data = response.json()

        page_jobs = data.get("jobPostings", [])

        for raw_job in page_jobs:
            job = raw_job.copy()
            job["_workday_config"] = config
            jobs.append(job)

        total = data.get("total", len(jobs))

        if not page_jobs or len(jobs) >= total:
            break

        offset += len(page_jobs)

    return jobs


def get_workday_description(raw_job: dict) -> str:
    if raw_job.get("jobDescription"):
        return raw_job["jobDescription"]
    config = raw_job.get("_workday_config") or {}
    path = raw_job.get("externalPath", "").lstrip("/")
    if not config or not path:
        return ""
    endpoint = f"{config['base_url']}/wday/cxs/{config['tenant']}/{config['site']}/{path}"
    response = requests.get(endpoint, timeout=20)
    response.raise_for_status()
    data = response.json()
    raw_job["_source_updated_at"] = data.get("startDate", "")
    return data.get("jobPostingInfo", {}).get("jobDescription", "") or data.get(
        "jobDescription", ""
    )


def normalize_workday_job(
    raw_job: dict,
    company_name: str,
    fortune_rank: int,
) -> Job | None:
    title = raw_job.get("title", "Unknown Position")
    location = raw_job.get("locationsText") or "Unknown"

    bullet_fields = raw_job.get("bulletFields") or []
    employment_text = " ".join([title] + [str(field) for field in bullet_fields])

    employment_type = classify_employment_type(employment_text)

    if employment_type is None:
        return None

    category = classify_job_category(title)

    config = raw_job.get("_workday_config") or {}
    external_path = raw_job.get("externalPath", "")

    base_url = config.get("base_url", "")
    locale = config.get("locale", "")
    site = config.get("site", "")

    if base_url and locale and site and external_path:
        url = f"{base_url}/{locale}/{site}{external_path}"
    else:
        url = ""

    return Job(
        company=company_name,
        fortune_rank=fortune_rank,
        title=title,
        location=location,
        url=url,
        source="workday",
        external_id=external_path,
        employment_type=employment_type,
        category=category,
        updated_at="",
    )
