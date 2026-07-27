from src.models import Job
from src.readme import (
    create_category_sections,
    create_category_slug,
)


def create_test_job(
    category: str,
    external_id: str,
) -> Job:
    return Job(
        company="Example Company",
        fortune_rank=100,
        title="Example Position",
        location="Austin, TX",
        url="https://example.com/job",
        source="workday",
        external_id=external_id,
        employment_type="full-time",
        category=category,
    )


def test_creates_category_slug():
    assert (
        create_category_slug("Software & IT")
        == "software-it"
    )

    assert (
        create_category_slug("Data & AI")
        == "data-ai"
    )


def test_creates_category_navigation():
    jobs = [
        create_test_job(
            "Software & IT",
            "software-1",
        ),
        create_test_job(
            "Data & AI",
            "data-1",
        ),
    ]

    markdown = create_category_sections(jobs)

    assert (
        "[Software & IT (1)](#software-it)"
        in markdown
    )

    assert (
        "[Data & AI (1)](#data-ai)"
        in markdown
    )

    assert '<a id="software-it"></a>' in markdown
    assert '<a id="data-ai"></a>' in markdown

    assert (
        "[Back to categories](#categories)"
        in markdown
    )