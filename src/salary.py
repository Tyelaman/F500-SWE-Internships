import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Salary:
    minimum: float | None = None
    maximum: float | None = None
    currency: str = ""
    period: str = ""
    text: str = ""


AMOUNT = r"\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)\s*([kK]?)"
RANGE = re.compile(
    AMOUNT
    + r"\s*(?:-|–|—|to)\s*"
    + AMOUNT
    + r"\s*(?:per\s+|/\s*)?(year|annually|annual|hour|hourly|month|monthly)\b",
    re.I,
)
SINGLE = re.compile(
    AMOUNT + r"\s*(?:per\s+|/\s*)(year|annually|annual|hour|hourly|month|monthly)\b", re.I
)
BONUS_CONTEXT = re.compile(r"(?:bonus|equity|stock|rsu|relocation|401\s*\(?k\)?)", re.I)


def _number(value: str, suffix: str) -> float:
    number = float(value.replace(",", ""))
    return number * 1000 if suffix.lower() == "k" else number


def _period(value: str) -> str:
    value = value.lower()
    if value.startswith("year") or value.startswith("annual"):
        return "year"
    if value.startswith("month"):
        return "month"
    return "hour"


def extract_salary(text: str) -> Salary:
    for pattern, ranged in ((RANGE, True), (SINGLE, False)):
        for match in pattern.finditer(text or ""):
            context = (text or "")[max(0, match.start() - 35) : match.end()]
            if BONUS_CONTEXT.search(context):
                continue
            if ranged:
                minimum = _number(match.group(1), match.group(2))
                maximum = _number(match.group(3), match.group(4))
                period = _period(match.group(5))
            else:
                minimum = maximum = _number(match.group(1), match.group(2))
                period = _period(match.group(3))
            if minimum <= maximum:
                return Salary(minimum, maximum, "USD", period, match.group(0).strip())
    return Salary()


def format_salary(minimum: float | None, maximum: float | None, period: str) -> str:
    if minimum is None:
        return "Not disclosed"
    suffix = {"year": "yr", "month": "mo", "hour": "hr"}.get(period, period)

    def compact(value: float) -> str:
        return f"${value / 1000:g}k" if value >= 1000 else f"${value:g}"

    if maximum is not None and maximum != minimum:
        return f"{compact(minimum)}–{compact(maximum)}/{suffix}"
    return f"{compact(minimum)}/{suffix}"
