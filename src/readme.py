from datetime import datetime, timezone
from pathlib import Path
import re
from src.companies import load_companies

from src.models import Job


PROJECT_ROOT = Path(__file__).resolve().parent.parent
README_PATH = PROJECT_ROOT / "README.md"
README_TEMPLATE_PATH = PROJECT_ROOT / "README_TEMPLATE.md"
JOBS_DIRECTORY = PROJECT_ROOT / "jobs"
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
    return text.replace("|", "/").replace("\n", " ").strip()

def create_category_slug(category: str) -> str:
    return re.sub(
        r"[^a-z0-9]+",
        "-",
        category.lower(),
    ).strip("-")

def create_job_table(jobs: list[Job]) -> str:
    lines = [
        "| Rank | Company | Position | Location | Updated | Apply |",
        "|---:|---|---|---|---|---|",
    ]

    for job in jobs:
        company = clean_markdown(job.company)
        title = clean_markdown(job.title)
        location = clean_markdown(job.location)
        apply_link = f"[Apply]({job.url})"
        updated = format_updated_at(job.updated_at)

        row = (
            f"| {job.fortune_rank} "
            f"| {company} "
            f"| {title} "
            f"| {location} "
            f"| {updated} "
            f"| {apply_link} |"
        )

        lines.append(row)

    if not jobs:
        lines.append("| — | — | No positions found | — | — | — |")

    return "\n".join(lines)

def create_category_sections(jobs: list[Job]) -> str:
    if not jobs:
        return create_job_table([])

    jobs_by_category = {}

    for job in jobs:
        category = job.category or "Other"

        if category not in jobs_by_category:
            jobs_by_category[category] = []

        jobs_by_category[category].append(job)

    categories = []

    for category in CATEGORY_ORDER:
        if category in jobs_by_category:
            categories.append(category)

    extra_categories = sorted(
        category
        for category in jobs_by_category
        if category not in CATEGORY_ORDER
    )

    categories.extend(extra_categories)

    category_links = []

    for category in categories:
        slug = create_category_slug(category)
        count = len(jobs_by_category[category])

        category_links.append(
            f"[{category} ({count})](#{slug})"
        )

    navigation = (
        "## Categories\n\n"
        + " · ".join(category_links)
    )

    sections = []

    for category in categories:
        category_jobs = jobs_by_category[category]

        category_jobs.sort(
            key=lambda job: parse_updated_at(
                job.updated_at
            ),
            reverse=True,
        )

        slug = create_category_slug(category)

        section = (
            f'<a id="{slug}"></a>\n\n'
            f"## {category}\n\n"
            f"Open positions: {len(category_jobs)}\n\n"
            f"{create_job_table(category_jobs)}\n\n"
            f"[Back to categories](#categories)"
        )

        sections.append(section)

    return (
        f"{navigation}\n\n"
        + "\n\n".join(sections)
    )

def generate_markdown_files(jobs: list[Job]) -> None:
    JOBS_DIRECTORY.mkdir(exist_ok=True)

    internships = []
    full_time_jobs = []

    for job in jobs:
        if job.employment_type == "internship":
            internships.append(job)
        elif job.employment_type == "full-time":
            full_time_jobs.append(job)

    internships.sort(
        key=lambda job: parse_updated_at(job.updated_at),
        reverse=True,
    )

    full_time_jobs.sort(
        key=lambda job: parse_updated_at(job.updated_at),
        reverse=True,
    )

    updated_at = datetime.now(timezone.utc).strftime("%B %d, %Y at %H:%M UTC")

    internships_content = (
        "# Fortune 500 Internships\n\n"
        f"Last updated: {updated_at}\n\n"
        f"Open internships: {len(internships)}\n\n"
        f"{create_category_sections(internships)}\n"
    )

    full_time_content = (
        "# Fortune 500 Full-Time Positions\n\n"
        f"Last updated: {updated_at}\n\n"
        f"Open full-time positions: {len(full_time_jobs)}\n\n"
        f"{create_category_sections(full_time_jobs)}\n"
    )

    companies = sorted(
        load_companies(),
        key=lambda company: company["fortune_rank"],
    )

    company_rows = "\n".join(
        (
            f"| {company['fortune_rank']} "
            f"| {clean_markdown(company['name'])} "
            f"| {company['source'].title()} |"
        )
        for company in companies
    )

    readme_template = README_TEMPLATE_PATH.read_text(
        encoding="utf-8"
    )

    readme_content = (
        readme_template
        .replace("{{LAST_UPDATED}}", updated_at)
        .replace(
            "{{COMPANY_COUNT}}",
            str(len(companies)),
        )
        .replace(
            "{{INTERNSHIP_COUNT}}",
            str(len(internships)),
        )
        .replace(
            "{{FULL_TIME_COUNT}}",
            str(len(full_time_jobs)),
        )
        .replace(
            "{{TOTAL_COUNT}}",
            str(len(jobs)),
        )
        .replace(
            "{{COMPANY_ROWS}}",
            company_rows,
        )
    )

    INTERNSHIPS_PATH.write_text(internships_content, encoding="utf-8")
    FULL_TIME_PATH.write_text(full_time_content, encoding="utf-8")
    README_PATH.write_text(readme_content, encoding="utf-8")

def parse_updated_at(value: str) -> datetime:
    if not value:
        return datetime.min.replace(tzinfo=timezone.utc)

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)


def format_updated_at(value: str) -> str:
    if not value:
        return "—"

    try:
        updated_at = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return updated_at.strftime("%b %d, %Y")
    except ValueError:
        return "—"