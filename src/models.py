from dataclasses import asdict, dataclass


@dataclass
class Job:
    company: str
    title: str
    location: str
    url: str
    source: str
    external_id: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            company=data["company"],
            title=data["title"],
            location=data["location"],
            url=data["url"],
            source=data["source"],
            external_id=data["external_id"],
        )