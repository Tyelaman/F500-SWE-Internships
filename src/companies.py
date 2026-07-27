import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
COMPANIES_PATH = PROJECT_ROOT / "data" / "companies.json"


def load_companies() -> list[dict]:
    if not COMPANIES_PATH.exists():
        return []

    with open(COMPANIES_PATH, "r", encoding="utf-8") as file:
        return json.load(file)