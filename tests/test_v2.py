import json
from datetime import UTC, datetime

import pytest

from src.companies import validate_companies
from src.enrichment import apply_cached_enrichment, cache_key
from src.keywords import extract_keywords
from src.models import Job
from src.pipeline import filter_public_jobs
from src.readme import generate_markdown_files
from src.salary import extract_salary
from src.sponsorship import DOES_NOT_SUPPORT_H1B, SUPPORTS_H1B, UNKNOWN, classify_sponsorship


@pytest.mark.parametrize(
    "text",
    [
        "H-1B sponsorship is available for this position.",
        "We provide employment-based immigration sponsorship for this role.",
    ],
)
def test_positive_sponsorship(text):
    assert classify_sponsorship(text).status == SUPPORTS_H1B


@pytest.mark.parametrize(
    "text",
    [
        "No visa sponsorship is available.",
        "Candidates must be authorized to work without sponsorship now or in the future.",
    ],
)
def test_negative_sponsorship(text):
    assert classify_sponsorship(text).status == DOES_NOT_SUPPORT_H1B


@pytest.mark.parametrize(
    "text", ["", "Visa sponsorship may be available.", "STEM OPT eligible.", "CPT accepted."]
)
def test_ambiguous_sponsorship_is_unknown(text):
    assert classify_sponsorship(text).status == UNKNOWN


def test_negative_overrides_positive():
    text = "We sponsor H-1B visas. This position is not eligible for visa sponsorship."
    assert classify_sponsorship(text).status == DOES_NOT_SUPPORT_H1B


@pytest.mark.parametrize(
    ("text", "minimum", "maximum", "period"),
    [
        ("Salary: $120,000 - $160,000 per year", 120000, 160000, "year"),
        ("Pay is $30 - $40 per hour", 30, 40, "hour"),
        ("Compensation: $6,000 per month", 6000, 6000, "month"),
    ],
)
def test_salary_ranges(text, minimum, maximum, period):
    salary = extract_salary(text)
    assert (salary.minimum, salary.maximum, salary.period) == (minimum, maximum, period)


def test_bonus_is_not_salary():
    assert extract_salary("Signing bonus: $10,000 per year").minimum is None


def test_keyword_aliases_and_boundaries():
    assert extract_keywords("Amazon Web Services, Postgres, K8s and NodeJS") == [
        "Node.js",
        "AWS",
        "Kubernetes",
        "PostgreSQL",
    ]
    assert "C" not in extract_keywords("Compliance manager")


def test_general_keywords():
    assert extract_keywords("Supply chain procurement and logistics") == [
        "supply chain",
        "logistics",
        "procurement",
    ]


def test_company_validation():
    valid = [{"name": "Example", "fortune_rank": 1, "source": "lever", "identifier": "example"}]
    assert validate_companies(valid) == valid
    with pytest.raises(ValueError, match="missing"):
        validate_companies([{"name": "Bad"}])
    with pytest.raises(ValueError, match="Duplicate"):
        validate_companies(valid + valid)


def make_job(status=SUPPORTS_H1B, employment="full-time"):
    return Job(
        "Example",
        1,
        "Analyst",
        "Austin, TX",
        "https://example.test/job",
        "lever",
        "1",
        employment,
        h1b_status=status,
        sponsorship_evidence="H-1B sponsorship is available.",
    )


def test_public_filter_excludes_unknown_and_negative():
    jobs = [make_job(), make_job(UNKNOWN), make_job(DOES_NOT_SUPPORT_H1B)]
    assert filter_public_jobs(jobs) == [jobs[0]]


def test_backward_compatible_model_loading():
    old = {
        "company": "A",
        "fortune_rank": 1,
        "title": "T",
        "location": "Austin, TX",
        "url": "u",
        "source": "lever",
        "external_id": "1",
        "employment_type": "full-time",
    }
    assert Job.from_dict(old).h1b_status == UNKNOWN


def test_fresh_cache_is_applied_before_detail_fetch():
    job = make_job(UNKNOWN)
    cache = {
        cache_key(job): {
            "h1b_status": SUPPORTS_H1B,
            "sponsorship_evidence": "H-1B sponsorship is available.",
            "enriched_at": datetime.now(UTC).isoformat(),
        }
    }

    assert apply_cached_enrichment(job, cache)
    assert job.h1b_status == SUPPORTS_H1B


def test_generated_outputs_filter_public_jobs(tmp_path, monkeypatch):
    import src.readme as readme

    monkeypatch.setattr(readme, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(readme, "README_PATH", tmp_path / "README.md")
    monkeypatch.setattr(readme, "README_TEMPLATE_PATH", tmp_path / "README_TEMPLATE.md")
    monkeypatch.setattr(readme, "JOBS_DIRECTORY", tmp_path / "jobs")
    monkeypatch.setattr(readme, "DOCS_DIRECTORY", tmp_path / "docs")
    monkeypatch.setattr(readme, "INTERNSHIPS_PATH", tmp_path / "jobs/internships.md")
    monkeypatch.setattr(readme, "FULL_TIME_PATH", tmp_path / "jobs/full-time.md")
    monkeypatch.setattr(readme, "load_companies", lambda: [])
    (tmp_path / "README_TEMPLATE.md").write_text(
        "{{TOTAL_COUNT}} {{INTERNSHIP_COUNT}} {{FULL_TIME_COUNT}} {{SALARY_COUNT}} "
        "{{COMPANY_COUNT}} {{LAST_UPDATED}} {{COMPANY_ROWS}}"
    )
    generate_markdown_files(
        [
            make_job(),
            make_job(UNKNOWN),
            make_job(DOES_NOT_SUPPORT_H1B),
            make_job(SUPPORTS_H1B, "internship"),
        ]
    )
    site_jobs = json.loads((tmp_path / "docs/jobs.json").read_text())
    assert len(site_jobs) == 2
    assert all(job["h1b_status"] == SUPPORTS_H1B for job in site_jobs)
    assert (tmp_path / "README.md").read_text().startswith("2 1 1")
