from dataclasses import dataclass


@dataclass(slots=True)
class CreateTicketInputDto:
    id: str
    description: str
    type: str
