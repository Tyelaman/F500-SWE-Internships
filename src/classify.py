import re


INTERNSHIP_PATTERN = re.compile(
    r"\b(intern|internship|internships|co[\s-]?op)\b",
    re.IGNORECASE,
)

EXCLUDED_PATTERN = re.compile(
    r"\b("
    r"part[\s-]?time|"
    r"contract|contractor|"
    r"temporary|seasonal|freelance"
    r")\b",
    re.IGNORECASE,
)


def classify_employment_type(title: str) -> str | None:
    if INTERNSHIP_PATTERN.search(title):
        return "internship"

    if EXCLUDED_PATTERN.search(title):
        return None

    return "full-time"