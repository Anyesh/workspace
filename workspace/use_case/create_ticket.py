from workspace.dto.create_ticket import CreateTicketInputDto
from workspace.entity.ticket import Ticket
from workspace.repository.json_repository import JSONRepository


class CreateTicket:
    def __init__(self, repository: JSONRepository):
        self._repository = repository

    def execute(self, input_dto: CreateTicketInputDto) -> Ticket:

        ticket = Ticket(
            id=input_dto.id,
            description=input_dto.description,
            type=input_dto.type,
        )
        self._repository.create(ticket)
        return ticket
