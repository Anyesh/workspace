from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Branch:
    name: str
    base_branch: str = field(default="develop")
    created_at: str = field(init=False, default_factory=datetime.now().__str__)
