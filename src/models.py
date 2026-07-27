from dataclasses import asdict, dataclass


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
    updated_at: str = ""
    first_seen_at: str = ""

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
            updated_at=data.get("updated_at", ""),
            first_seen_at=data.get("first_seen_at", ""),
        )