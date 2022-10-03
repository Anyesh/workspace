from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True, frozen=True)
class Branch:
    name: str
    base_branch: str = field(default="develop")
    created_at: str = field(init=False, default_factory=datetime.now().__str__)
