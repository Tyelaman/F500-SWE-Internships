from requests import RequestException

from src.companies import load_companies
from src.connectors.greenhouse import (
    fetch_greenhouse_jobs,
    normalize_greenhouse_job,
)
from src.models import Job


def collect_jobs() -> tuple[list[Job], set[str], set[str]]:
    companies = load_companies()
    collected_jobs = []
    successful_companies = set()
    failed_companies = set()

    for company in companies:
        source = company["source"]
        company_name = company["name"]

        try:
            if source == "greenhouse":
                raw_jobs = fetch_greenhouse_jobs(
                    company["identifier"]
                )

                successful_companies.add(company_name)

                for raw_job in raw_jobs:
                    job = normalize_greenhouse_job(
                        raw_job=raw_job,
                        company_name=company_name,
                        fortune_rank=company["fortune_rank"],
                    )

                    if job is not None:
                        collected_jobs.append(job)
            else:
                print(
                    f"Skipping {company_name}: "
                    f"unsupported source '{source}'"
                )

        except RequestException as error:
            failed_companies.add(company_name)

            print(
                f"Failed to fetch jobs for "
                f"{company_name}: {error}"
            )

    return (
        collected_jobs,
        successful_companies,
        failed_companies,
    )