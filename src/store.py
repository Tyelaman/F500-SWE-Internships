import json
from pathlib import Path
from datetime import datetime, timezone

from src.models import Job


PROJECT_ROOT = Path(__file__).resolve().parent.parent
JOBS_PATH = PROJECT_ROOT / "data" / "jobs.json"


def save_jobs(jobs: list[Job]) -> None:
    job_data = []

    for job in jobs:
        job_data.append(job.to_dict())

    with open(JOBS_PATH, "w", encoding="utf-8") as file:
        json.dump(job_data, file, indent=2)

def load_jobs() -> list[Job]:
    if not JOBS_PATH.exists():
        return []

    with open(JOBS_PATH, "r", encoding="utf-8") as file:
        job_data = json.load(file)

    jobs = []

    for data in job_data:
        jobs.append(Job.from_dict(data))

    return jobs

def merge_jobs(
    collected_jobs: list[Job],
    existing_jobs: list[Job],
) -> list[Job]:
    existing_by_id = {}

    for job in existing_jobs:
        key = f"{job.source}:{job.external_id}"
        existing_by_id[key] = job

    now = datetime.now(timezone.utc).isoformat()
    merged_jobs = []

    for job in collected_jobs:
        key = f"{job.source}:{job.external_id}"
        existing_job = existing_by_id.get(key)

        if existing_job is not None:
            job.first_seen_at = existing_job.first_seen_at or now
        else:
            job.first_seen_at = now

        merged_jobs.append(job)

    return merged_jobs