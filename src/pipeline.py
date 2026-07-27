from requests import RequestException

from src.companies import load_companies
from src.connectors.greenhouse import (
    fetch_greenhouse_jobs,
    normalize_greenhouse_job,
)
from src.connectors.lever import (
    fetch_lever_jobs,
    normalize_lever_job,
)
from src.connectors.workday import (
    fetch_workday_jobs,
    normalize_workday_job,
)
from src.models import Job


CONNECTORS = {
    "greenhouse": (
        fetch_greenhouse_jobs,
        normalize_greenhouse_job,
    ),
    "lever": (
        fetch_lever_jobs,
        normalize_lever_job,
    ),
    "workday": (
        fetch_workday_jobs,
        normalize_workday_job,
    ),
}


def deduplicate_jobs(jobs: list[Job]) -> list[Job]:
    unique_jobs = {}

    for job in jobs:
        key = (
            job.source,
            job.company.lower().strip(),
            job.external_id,
        )

        unique_jobs[key] = job

    return list(unique_jobs.values())


def collect_jobs() -> tuple[list[Job], set[str], set[str]]:
    companies = load_companies()
    collected_jobs = []
    successful_companies = set()
    failed_companies = set()

    for company in companies:
        source = company["source"]
        company_name = company["name"]

        connector = CONNECTORS.get(source)

        if connector is None:
            print(
                f"Skipping {company_name}: "
                f"unsupported source '{source}'"
            )
            continue

        fetch_jobs, normalize_job = connector

        try:
            raw_jobs = fetch_jobs(company["identifier"])
            successful_companies.add(company_name)

            for raw_job in raw_jobs:
                job = normalize_job(
                    raw_job=raw_job,
                    company_name=company_name,
                    fortune_rank=company["fortune_rank"],
                )

                if job is not None:
                    collected_jobs.append(job)

        except RequestException as error:
            failed_companies.add(company_name)

            print(
                f"Failed to fetch jobs for "
                f"{company_name}: {error}"
            )

    deduplicated_jobs = deduplicate_jobs(collected_jobs)

    return (
        deduplicated_jobs,
        successful_companies,
        failed_companies,
    )