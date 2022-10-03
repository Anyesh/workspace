from dataclasses import dataclass, field

from .task import TaskType


@dataclass
class Ticket:
    id: str
    description: str
    type: str = field(default=TaskType.STORY.value)
    name_for_branch: str = field(init=False)

    def __post_init__(self):
        self.id = self.id.upper()
        self.description = self.description.lower()
        self.name_for_branch = (
            f"{self.type}/{self.id}-{'-'.join(self.description.lower().split())}"
        )
