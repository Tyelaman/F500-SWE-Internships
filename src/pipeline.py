from requests import RequestException

from src.companies import load_companies
from src.connectors.greenhouse import (
    fetch_greenhouse_jobs,
    normalize_greenhouse_job,
)
from src.models import Job


def collect_jobs() -> list[Job]:
    companies = load_companies()
    collected_jobs = []

    for company in companies:
        source = company["source"]

        try:
            if source == "greenhouse":
                raw_jobs = fetch_greenhouse_jobs(company["identifier"])

                for raw_job in raw_jobs:
                    job = normalize_greenhouse_job(
                        raw_job=raw_job,
                        company_name=company["name"],
                        fortune_rank=company["fortune_rank"],
                    )

                    if job is not None:
                        collected_jobs.append(job)
            else:
                print(
                    f"Skipping {company['name']}: "
                    f"unsupported source '{source}'"
                )

        except RequestException as error:
            print(
                f"Failed to fetch jobs for "
                f"{company['name']}: {error}"
            )

    return collected_jobs