import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

from src.keywords import extract_keywords
from src.models import Job
from src.salary import extract_salary
from src.sponsorship import classify_sponsorship

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_PATH = PROJECT_ROOT / "data" / "enrichment_cache.json"
CACHE_TTL = timedelta(days=7)


def cache_key(job: Job) -> str:
    return f"{job.source}:{job.company}:{job.external_id}"


def load_cache(path: Path = CACHE_PATH) -> dict[str, dict]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Invalid enrichment cache: {error}") from error
    return data if isinstance(data, dict) else {}


def save_cache(cache: dict[str, dict], path: Path = CACHE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _fresh(entry: dict, updated_at: str) -> bool:
    if updated_at and entry.get("source_updated_at"):
        return updated_at == entry["source_updated_at"]
    try:
        enriched = datetime.fromisoformat(entry["enriched_at"].replace("Z", "+00:00"))
    except (KeyError, TypeError, ValueError):
        return False
    return datetime.now(UTC) - enriched < CACHE_TTL


def apply_entry(job: Job, entry: dict) -> None:
    for name in (
        "h1b_status",
        "sponsorship_evidence",
        "h1b_mentioned",
        "salary_min",
        "salary_max",
        "salary_currency",
        "salary_period",
        "salary_text",
        "keywords",
        "enriched_at",
    ):
        if name in entry:
            setattr(job, name, entry[name])


def apply_cached_enrichment(job: Job, cache: dict[str, dict]) -> bool:
    entry = cache.get(cache_key(job), {})
    if not entry or not _fresh(entry, job.updated_at):
        return False
    apply_entry(job, entry)
    return True


def enrich_job(job: Job, description: str, cache: dict[str, dict]) -> bool:
    key = cache_key(job)
    if apply_cached_enrichment(job, cache):
        return True
    now = datetime.now(UTC).isoformat()
    sponsorship = classify_sponsorship(description)
    salary = extract_salary(description)
    keywords = extract_keywords(f"{job.title} {description}")
    entry = {
        "source": job.source,
        "company": job.company,
        "external_id": job.external_id,
        "source_updated_at": job.updated_at,
        "h1b_status": sponsorship.status,
        "sponsorship_evidence": sponsorship.evidence,
        "h1b_mentioned": sponsorship.h1b_mentioned,
        "salary_min": salary.minimum,
        "salary_max": salary.maximum,
        "salary_currency": salary.currency,
        "salary_period": salary.period,
        "salary_text": salary.text,
        "keywords": keywords,
        "enriched_at": now,
    }
    cache[key] = entry
    apply_entry(job, entry)
    return False
