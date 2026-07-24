from dataclasses import dataclass


@dataclass
class Job:
    company: str
    title: str
    location: str
    url: str
    source: str
    external_id: str