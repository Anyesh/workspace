from workspace.dto.create_ticket import CreateTicketInputDto
from workspace.entity.ticket import Ticket
from workspace.interface.repository import BaseRepository


class CreateTicket:
    def __init__(self, repository=None):
        self._repository = repository

    def execute(self, input_dto: CreateTicketInputDto) -> Ticket:

        # self._repository.create(ticket)
        return Ticket(
            id=input_dto.id,
            description=input_dto.description,
            type=input_dto.type,
        )
