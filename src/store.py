import json
from pathlib import Path

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