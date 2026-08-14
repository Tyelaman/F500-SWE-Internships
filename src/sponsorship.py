import html
import re
from dataclasses import dataclass

SUPPORTS_H1B = "supports_h1b"
DOES_NOT_SUPPORT_H1B = "does_not_support_h1b"
UNKNOWN = "unknown"

NEGATIVE_PATTERNS = [
    re.compile(pattern, re.I)
    for pattern in (
        r"(?:no|not (?:available|eligible)|without)\s+"
        r"(?:employment\s+|immigration\s+|visa\s+|h-?1b\s+)?sponsorship",
        r"(?:do not|does not|cannot|can't|unable to|will not|won't)\s+"
        r"(?:provide\s+)?(?:visa\s+|immigration\s+|employment\s+|h-?1b\s+)?"
        r"sponsor(?:ship)?",
        r"(?:must|need to)\s+(?:be\s+)?(?:permanently\s+)?authorized to work"
        r"[^.]{0,90}without[^.]{0,30}sponsorship",
        r"(?:not|ineligible)\s+(?:be\s+)?eligible for (?:immigration|visa|h-?1b) sponsorship",
        r"not require sponsorship (?:now|currently)(?:\s+or\s+in\s+the\s+future)?",
    )
]
POSITIVE_PATTERNS = [
    re.compile(pattern, re.I)
    for pattern in (
        r"h-?1b (?:visa )?sponsorship (?:is )?(?:available|provided|offered)",
        r"(?:we|company|employer) (?:will |can |do )?sponsor h-?1b",
        r"(?:eligible for|provide(?:s|d)?|offer(?:s|ed)?) (?:u\.s\. )?"
        r"employment[- ]based immigration sponsorship",
        r"(?:immigration|employment visa) sponsorship (?:is )?"
        r"(?:available|provided|offered) (?:for (?:this|the) (?:role|position))?",
    )
]
H1B_PATTERN = re.compile(r"\bh-?1b\b", re.I)
TAG_PATTERN = re.compile(r"<[^>]+>")


@dataclass(frozen=True)
class SponsorshipResult:
    status: str
    evidence: str = ""
    h1b_mentioned: bool = False


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(TAG_PATTERN.sub(" ", text or ""))).strip()


def _excerpt(text: str, match: re.Match) -> str:
    start = max(text.rfind(".", 0, match.start()) + 1, match.start() - 80)
    end = text.find(".", match.end())
    if end == -1 or end - start > 260:
        end = min(len(text), match.end() + 100)
    return text[start : end + 1].strip()[:280]


def classify_sponsorship(description: str) -> SponsorshipResult:
    text = _clean(description)
    mentioned = bool(H1B_PATTERN.search(text))
    if not text:
        return SponsorshipResult(UNKNOWN)
    for pattern in NEGATIVE_PATTERNS:
        match = pattern.search(text)
        if match:
            return SponsorshipResult(DOES_NOT_SUPPORT_H1B, _excerpt(text, match), mentioned)
    for pattern in POSITIVE_PATTERNS:
        match = pattern.search(text)
        if match:
            return SponsorshipResult(SUPPORTS_H1B, _excerpt(text, match), mentioned)
    return SponsorshipResult(UNKNOWN, h1b_mentioned=mentioned)
