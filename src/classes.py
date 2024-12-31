from dataclasses import dataclass
from typing import Optional


@dataclass
class Job:
    title: str
    company: str
    type: Optional[str] = None
    description: Optional[str] = None
    salary: Optional[float] = None
    location: Optional[str] = None
    link: Optional[str] = None
