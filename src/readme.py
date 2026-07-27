from datetime import datetime, timezone
from pathlib import Path

from src.models import Job


PROJECT_ROOT = Path(__file__).resolve().parent.parent
README_PATH = PROJECT_ROOT / "README.md"
JOBS_DIRECTORY = PROJECT_ROOT / "jobs"
INTERNSHIPS_PATH = JOBS_DIRECTORY / "internships.md"
FULL_TIME_PATH = JOBS_DIRECTORY / "full-time.md"


def clean_markdown(text: str) -> str:
    return text.replace("|", "/").replace("\n", " ").strip()


def create_job_table(jobs: list[Job]) -> str:
    lines = [
        "| Rank | Company | Position | Location | Apply |",
        "|---:|---|---|---|---|",
    ]

    for job in jobs:
        company = clean_markdown(job.company)
        title = clean_markdown(job.title)
        location = clean_markdown(job.location)
        apply_link = f"[Apply]({job.url})"

        row = (
            f"| {job.fortune_rank} "
            f"| {company} "
            f"| {title} "
            f"| {location} "
            f"| {apply_link} |"
        )

        lines.append(row)

    if not jobs:
        lines.append("| — | — | No positions found | — | — |")

    return "\n".join(lines)


def generate_markdown_files(jobs: list[Job]) -> None:
    JOBS_DIRECTORY.mkdir(exist_ok=True)

    internships = []
    full_time_jobs = []

    for job in jobs:
        if job.employment_type == "internship":
            internships.append(job)
        elif job.employment_type == "full-time":
            full_time_jobs.append(job)

    internships.sort(key=lambda job: (job.fortune_rank, job.company, job.title))
    full_time_jobs.sort(key=lambda job: (job.fortune_rank, job.company, job.title))

    updated_at = datetime.now(timezone.utc).strftime("%B %d, %Y at %H:%M UTC")

    internships_content = (
        "# Fortune 500 Internships\n\n"
        f"Last updated: {updated_at}\n\n"
        f"Open internships: {len(internships)}\n\n"
        f"{create_job_table(internships)}\n"
    )

    full_time_content = (
        "# Fortune 500 Full-Time Positions\n\n"
        f"Last updated: {updated_at}\n\n"
        f"Open full-time positions: {len(full_time_jobs)}\n\n"
        f"{create_job_table(full_time_jobs)}\n"
    )

    readme_content = (
        "# Fortune 500 Job Tracker\n\n"
        "An automatically updated collection of positions from supported "
        "Fortune 500 company career pages.\n\n"
        f"**Last updated:** {updated_at}\n\n"
        f"**Internships:** {len(internships)}  \n"
        f"**Full-time positions:** {len(full_time_jobs)}  \n"
        f"**Total positions:** {len(jobs)}\n\n"
        "## Job Lists\n\n"
        "- [Internships](jobs/internships.md)\n"
        "- [Full-Time Positions](jobs/full-time.md)\n\n"
        "Listings are collected from official company hiring platforms. "
        "Always confirm that a position is still available before applying.\n"
    )

    INTERNSHIPS_PATH.write_text(internships_content, encoding="utf-8")
    FULL_TIME_PATH.write_text(full_time_content, encoding="utf-8")
    README_PATH.write_text(readme_content, encoding="utf-8")