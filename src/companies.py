import json
from pathlib import Path

SUPPORTED_SOURCES = {"greenhouse", "lever", "workday"}


PROJECT_ROOT = Path(__file__).resolve().parent.parent
COMPANIES_PATH = PROJECT_ROOT / "data" / "companies.json"


def validate_companies(companies: object) -> list[dict]:
    if not isinstance(companies, list):
        raise ValueError("Company configuration must be a JSON array")

    names: set[str] = set()
    identifiers: set[tuple[str, str]] = set()
    for index, company in enumerate(companies, start=1):
        if not isinstance(company, dict):
            raise ValueError(f"Company #{index} must be an object")
        missing = {"name", "fortune_rank", "source", "identifier"} - company.keys()
        if missing:
            raise ValueError(f"Company #{index} is missing: {', '.join(sorted(missing))}")
        name = company["name"]
        rank = company["fortune_rank"]
        source = company["source"]
        identifier = company["identifier"]
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Company #{index} has an invalid name")
        if isinstance(rank, bool) or not isinstance(rank, int) or rank <= 0:
            raise ValueError(f"{name} has an invalid Fortune rank")
        if source not in SUPPORTED_SOURCES:
            raise ValueError(f"{name} uses unsupported source '{source}'")
        if not isinstance(identifier, str) or not identifier.strip():
            raise ValueError(f"{name} has an invalid identifier")
        normalized_name = name.casefold().strip()
        source_key = (source, identifier.casefold().strip())
        if normalized_name in names:
            raise ValueError(f"Duplicate company name: {name}")
        if source_key in identifiers:
            raise ValueError(f"Duplicate source/identifier: {source}/{identifier}")
        names.add(normalized_name)
        identifiers.add(source_key)
    return companies


def load_companies(path: Path = COMPANIES_PATH) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as file:
        return validate_companies(json.load(file))
