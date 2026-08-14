import re

CATEGORY_PATTERNS = {
    "Software & IT": re.compile(
        r"\b("
        r"software|developer|programmer|backend|front[\s-]?end|"
        r"full[\s-]?stack|devops|cloud|cybersecurity|security engineer|"
        r"systems engineer|site reliability|sre|information technology|IT"
        r")\b",
        re.IGNORECASE,
    ),
    "Data & AI": re.compile(
        r"\b("
        r"data scientist|data engineer|data analyst|machine learning|"
        r"artificial intelligence|AI engineer|analytics|business intelligence"
        r")\b",
        re.IGNORECASE,
    ),
    "Product & Design": re.compile(
        r"\b("
        r"product manager|product management|product designer|"
        r"UX|UI|user experience|graphic designer|design researcher"
        r")\b",
        re.IGNORECASE,
    ),
    "Engineering": re.compile(
        r"\b("
        r"mechanical|electrical|civil|chemical|industrial|"
        r"manufacturing engineer|hardware engineer|quality engineer"
        r")\b",
        re.IGNORECASE,
    ),
    "Finance & Accounting": re.compile(
        r"\b("
        r"finance|financial|accounting|accountant|audit|auditor|"
        r"tax|treasury|controller"
        r")\b",
        re.IGNORECASE,
    ),
    "Sales & Marketing": re.compile(
        r"\b("
        r"sales|marketing|advertising|brand|communications|"
        r"account executive|business development"
        r")\b",
        re.IGNORECASE,
    ),
    "Operations & Supply Chain": re.compile(
        r"\b("
        r"operations|supply chain|logistics|procurement|warehouse|"
        r"inventory|transportation"
        r")\b",
        re.IGNORECASE,
    ),
    "People & Legal": re.compile(
        r"\b("
        r"human resources|HR|recruiter|recruiting|talent acquisition|"
        r"legal|attorney|counsel|compliance"
        r")\b",
        re.IGNORECASE,
    ),
}


def classify_job_category(title: str) -> str:
    for category, pattern in CATEGORY_PATTERNS.items():
        if pattern.search(title):
            return category

    return "Other"
