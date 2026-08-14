from dataclasses import asdict, dataclass, field


@dataclass
class Job:
    company: str
    fortune_rank: int
    title: str
    location: str
    url: str
    source: str
    external_id: str
    employment_type: str
    category: str = "Other"
    h1b_status: str = "unknown"
    sponsorship_evidence: str = ""
    h1b_mentioned: bool = False
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: str = ""
    salary_period: str = ""
    salary_text: str = ""
    keywords: list[str] = field(default_factory=list)
    updated_at: str = ""
    first_seen_at: str = ""
    enriched_at: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            company=data["company"],
            fortune_rank=data["fortune_rank"],
            title=data["title"],
            location=data["location"],
            url=data["url"],
            source=data["source"],
            external_id=data["external_id"],
            employment_type=data["employment_type"],
            category=data.get("category", "Other"),
            h1b_status=data.get("h1b_status", "unknown"),
            sponsorship_evidence=data.get("sponsorship_evidence", ""),
            h1b_mentioned=data.get("h1b_mentioned", False),
            salary_min=data.get("salary_min"),
            salary_max=data.get("salary_max"),
            salary_currency=data.get("salary_currency", ""),
            salary_period=data.get("salary_period", ""),
            salary_text=data.get("salary_text", ""),
            keywords=list(data.get("keywords") or []),
            updated_at=data.get("updated_at", ""),
            first_seen_at=data.get("first_seen_at", ""),
            enriched_at=data.get("enriched_at", ""),
        )
