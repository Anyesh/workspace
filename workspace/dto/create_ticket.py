from dataclasses import dataclass


@dataclass(kw_only=True, slots=True)
class CreateTicketInputDto:
    id: str
    description: str
    type: str
