import json
import re
from datetime import UTC, datetime
from pathlib import Path

from src.companies import load_companies
from src.models import Job
from src.salary import format_salary
from src.sponsorship import SUPPORTS_H1B

PROJECT_ROOT = Path(__file__).resolve().parent.parent
README_PATH = PROJECT_ROOT / "README.md"
README_TEMPLATE_PATH = PROJECT_ROOT / "README_TEMPLATE.md"
JOBS_DIRECTORY = PROJECT_ROOT / "jobs"
DOCS_DIRECTORY = PROJECT_ROOT / "docs"
INTERNSHIPS_PATH = JOBS_DIRECTORY / "internships.md"
FULL_TIME_PATH = JOBS_DIRECTORY / "full-time.md"
CATEGORY_ORDER = [
    "Software & IT",
    "Data & AI",
    "Product & Design",
    "Engineering",
    "Finance & Accounting",
    "Sales & Marketing",
    "Operations & Supply Chain",
    "People & Legal",
    "Other",
]


def clean_markdown(text: str) -> str:
    return str(text).replace("|", "/").replace("\n", " ").strip()


def create_category_slug(category: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", category.lower()).strip("-")


def parse_updated_at(value: str) -> datetime:
    if not value:
        return datetime.min.replace(tzinfo=UTC)
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime.min.replace(tzinfo=UTC)


def format_updated_at(value: str) -> str:
    parsed = parse_updated_at(value)
    return "—" if parsed.year == 1 else parsed.strftime("%b %d, %Y")


def create_job_table(jobs: list[Job]) -> str:
    lines = [
        "| Rank | Company | Position | Location | Category | Salary | Keywords "
        "| Sponsorship | Apply |",
        "|---:|---|---|---|---|---|---|---|---|",
    ]
    for job in jobs:
        keywords = " · ".join(clean_markdown(item) for item in job.keywords[:5]) or "—"
        salary = format_salary(job.salary_min, job.salary_max, job.salary_period)
        lines.append(
            f"| {job.fortune_rank} | {clean_markdown(job.company)} "
            f"| {clean_markdown(job.title)} | {clean_markdown(job.location)} "
            f"| {clean_markdown(job.category)} | {salary} | {keywords} "
            f"| H-1B ✓ | [Apply]({job.url}) |"
        )
    if not jobs:
        lines.append("| — | — | No qualifying positions found | — | — | — | — | — | — |")
    return "\n".join(lines)


def create_category_sections(jobs: list[Job]) -> str:
    if not jobs:
        return create_job_table([])
    grouped: dict[str, list[Job]] = {}
    for job in jobs:
        grouped.setdefault(job.category or "Other", []).append(job)
    categories = [name for name in CATEGORY_ORDER if name in grouped]
    categories.extend(sorted(set(grouped) - set(categories)))
    links = " · ".join(
        f"[{name} ({len(grouped[name])})](#{create_category_slug(name)})" for name in categories
    )
    sections = []
    for name in categories:
        category_jobs = sorted(
            grouped[name], key=lambda job: parse_updated_at(job.updated_at), reverse=True
        )
        sections.append(
            f'<a id="{create_category_slug(name)}"></a>\n\n'
            f"## {name}\n\nOpen positions: {len(category_jobs)}\n\n"
            f"{create_job_table(category_jobs)}\n\n"
            "[Back to categories](#categories) · [Back to README](../README.md)"
        )
    return f"## Categories\n\n{links}\n\n" + "\n\n".join(sections)


def public_jobs(jobs: list[Job]) -> list[Job]:
    return [job for job in jobs if job.h1b_status == SUPPORTS_H1B]


def generate_markdown_files(jobs: list[Job]) -> None:
    jobs = public_jobs(jobs)
    JOBS_DIRECTORY.mkdir(exist_ok=True)
    DOCS_DIRECTORY.mkdir(exist_ok=True)
    internships = sorted(
        (job for job in jobs if job.employment_type == "internship"),
        key=lambda job: parse_updated_at(job.updated_at),
        reverse=True,
    )
    full_time = sorted(
        (job for job in jobs if job.employment_type == "full-time"),
        key=lambda job: parse_updated_at(job.updated_at),
        reverse=True,
    )
    updated = datetime.now(UTC).strftime("%B %d, %Y at %H:%M UTC")
    INTERNSHIPS_PATH.write_text(
        f"# F500Tracker sponsored internships\n\nLast updated: {updated}\n\n"
        f"Qualifying internships: {len(internships)}\n\n"
        f"{create_category_sections(internships)}\n",
        encoding="utf-8",
    )
    FULL_TIME_PATH.write_text(
        f"# F500Tracker sponsored full-time positions\n\nLast updated: {updated}\n\n"
        f"Qualifying positions: {len(full_time)}\n\n"
        f"{create_category_sections(full_time)}\n",
        encoding="utf-8",
    )
    companies = sorted(load_companies(), key=lambda item: item["fortune_rank"])
    rows = "\n".join(
        f"| {item['fortune_rank']} | {clean_markdown(item['name'])} | {item['source'].title()} |"
        for item in companies
    )
    salary_count = sum(job.salary_min is not None for job in jobs)
    content = README_TEMPLATE_PATH.read_text(encoding="utf-8")
    replacements = {
        "LAST_UPDATED": updated,
        "COMPANY_COUNT": len(companies),
        "INTERNSHIP_COUNT": len(internships),
        "FULL_TIME_COUNT": len(full_time),
        "TOTAL_COUNT": len(jobs),
        "SALARY_COUNT": salary_count,
        "COMPANY_ROWS": rows,
    }
    for key, value in replacements.items():
        content = content.replace("{{" + key + "}}", str(value))
    README_PATH.write_text(content, encoding="utf-8")
    compact = [
        {
            "company": job.company,
            "title": job.title,
            "location": job.location,
            "employment_type": job.employment_type,
            "category": job.category,
            "salary": format_salary(job.salary_min, job.salary_max, job.salary_period),
            "salary_min": job.salary_min,
            "keywords": job.keywords[:8],
            "sponsorship_evidence": job.sponsorship_evidence,
            "h1b_status": job.h1b_status,
            "url": job.url,
        }
        for job in jobs
    ]
    (DOCS_DIRECTORY / "jobs.json").write_text(
        json.dumps(compact, indent=2) + "\n", encoding="utf-8"
    )
