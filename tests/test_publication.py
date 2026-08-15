import json
from pathlib import Path

from src.models import Job
from src.sponsorship import DOES_NOT_SUPPORT_H1B, SUPPORTS_H1B, UNKNOWN
from src.store import save_jobs


def _job(status: str, external_id: str, salary_min=None) -> Job:
    return Job(
        company="Example",
        fortune_rank=1,
        title="Engineer",
        location="Austin, TX",
        url=f"https://example.test/{external_id}",
        source="lever",
        external_id=external_id,
        employment_type="full-time",
        h1b_status=status,
        salary_min=salary_min,
    )


def test_public_json_keeps_every_status_and_missing_salary(tmp_path, monkeypatch):
    import src.store as store

    output = tmp_path / "jobs.json"
    monkeypatch.setattr(store, "JOBS_PATH", output)
    jobs = [
        _job(SUPPORTS_H1B, "positive"),
        _job(UNKNOWN, "unknown"),
        _job(DOES_NOT_SUPPORT_H1B, "negative"),
    ]

    save_jobs(jobs)

    records = json.loads(output.read_text())
    assert len(records) == 3
    assert {record["h1b_status"] for record in records} == {
        SUPPORTS_H1B,
        UNKNOWN,
        DOES_NOT_SUPPORT_H1B,
    }
    assert all("sponsorship_evidence" in record for record in records)
    assert all(record["salary_min"] is None for record in records)


def test_frontend_has_sponsorship_filter():
    script = (Path(__file__).parents[1] / "docs" / "app.js").read_text(encoding="utf-8")
    assert '$("sponsorship").value' in script
    assert "j.h1b_status" in script
