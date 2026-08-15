from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor

from requests import RequestException

from src.companies import load_companies
from src.connectors.greenhouse import (
    fetch_greenhouse_jobs,
    get_greenhouse_description,
    normalize_greenhouse_job,
)
from src.connectors.lever import (
    fetch_lever_jobs,
    get_lever_description,
    normalize_lever_job,
)
from src.connectors.workday import (
    fetch_workday_jobs,
    get_workday_description,
    normalize_workday_job,
)
from src.enrichment import apply_cached_enrichment, enrich_job, load_cache, save_cache
from src.locations import is_us_location
from src.models import Job
from src.sponsorship import DOES_NOT_SUPPORT_H1B, SUPPORTS_H1B, UNKNOWN

CONNECTORS = {
    "greenhouse": (
        fetch_greenhouse_jobs,
        normalize_greenhouse_job,
        get_greenhouse_description,
    ),
    "lever": (
        fetch_lever_jobs,
        normalize_lever_job,
        get_lever_description,
    ),
    "workday": (
        fetch_workday_jobs,
        normalize_workday_job,
        get_workday_description,
    ),
}
WORKDAY_DETAIL_WORKERS = 8


def _fetch_description(
    raw_job: dict,
    get_description: Callable[[dict], str],
) -> tuple[str, Exception | None]:
    try:
        return get_description(raw_job), None
    except Exception as error:
        return "", error


def fetch_descriptions(
    raw_jobs: list[dict],
    get_description: Callable[[dict], str],
    *,
    concurrent: bool = False,
) -> list[tuple[str, Exception | None]]:
    if not concurrent or len(raw_jobs) < 2:
        return [_fetch_description(raw_job, get_description) for raw_job in raw_jobs]

    with ThreadPoolExecutor(max_workers=WORKDAY_DETAIL_WORKERS) as executor:
        return list(
            executor.map(
                lambda raw_job: _fetch_description(raw_job, get_description),
                raw_jobs,
            )
        )


def filter_public_jobs(jobs: list[Job]) -> list[Job]:
    return list(jobs)


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
    cache = load_cache()
    evaluated_jobs = 0

    for index, company in enumerate(companies, start=1):
        source = company["source"]
        company_name = company["name"]

        connector = CONNECTORS.get(source)

        if connector is None:
            print(f"Skipping {company_name}: unsupported source '{source}'")
            continue

        fetch_jobs, normalize_job, get_description = connector
        print(f"[{index}/{len(companies)}] {company_name}")
        eligible_jobs = []

        try:
            raw_jobs = fetch_jobs(company["identifier"])
            successful_companies.add(company_name)
            eligible_jobs = []
            status_counts = {SUPPORTS_H1B: 0, DOES_NOT_SUPPORT_H1B: 0, UNKNOWN: 0}

            for raw_job in raw_jobs:
                job = normalize_job(
                    raw_job=raw_job,
                    company_name=company_name,
                    fortune_rank=company["fortune_rank"],
                )

                if job is None or not is_us_location(job.location):
                    continue
                eligible_jobs.append((job, raw_job))

            jobs_needing_details = [
                (job, raw_job)
                for job, raw_job in eligible_jobs
                if not apply_cached_enrichment(job, cache)
            ]
            descriptions = fetch_descriptions(
                [raw_job for _, raw_job in jobs_needing_details],
                get_description,
                concurrent=source == "workday",
            )
            for (job, _), (description, error) in zip(
                jobs_needing_details, descriptions, strict=True
            ):
                if error is not None:
                    print(f"  detail failed for {job.external_id}: {error}")
                enrich_job(job, description, cache)
            for job, _ in eligible_jobs:
                status_counts[job.h1b_status] = status_counts.get(job.h1b_status, 0) + 1
                collected_jobs.append(job)

            print(f"  raw jobs: {len(raw_jobs)}")
            print(f"  U.S. eligible: {len(eligible_jobs)}")
            print(f"  public jobs: {len(eligible_jobs)}")
            print(f"  supports_h1b: {status_counts[SUPPORTS_H1B]}")
            print(f"  does_not_support_h1b: {status_counts[DOES_NOT_SUPPORT_H1B]}")
            print(f"  unknown: {status_counts[UNKNOWN]}")
            print("  status: success")

        except (RequestException, ValueError, KeyError, TypeError) as error:
            failed_companies.add(company_name)
            print("  status: failed")
            print(f"  error: {error}")

        evaluated_jobs += len(eligible_jobs)

    deduplicated_jobs = deduplicate_jobs(collected_jobs)
    save_cache(cache)
    print(f"Jobs evaluated: {evaluated_jobs}")

    return (
        deduplicated_jobs,
        successful_companies,
        failed_companies,
    )
