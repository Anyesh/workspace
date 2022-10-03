from dataclasses import dataclass


@dataclass
class CreateTicketInputDto:
    id: str
    description: str
    type: str
