from dataclasses import FrozenInstanceError

from tests.config import fake_repo
from ward import raises, test
from workspace.dto.create_ticket import CreateTicketInputDto
from workspace.entity.branch import Branch
from workspace.entity.task import TaskType
from workspace.entity.ticket import Ticket
from workspace.use_case.create_ticket import CreateTicket


@test("create a ticket happy path")
def _():
    input_dto = CreateTicketInputDto(
        id="aus-101", description="test test", type=TaskType.STORY.value
    )
    ticket = CreateTicket(None).execute(input_dto=input_dto)

    assert isinstance(ticket, Ticket)


@test("creating a ticket creates name for branch from it's description and id")
def _():
    input_dto = CreateTicketInputDto(
        id="aus-101", description="test test", type=TaskType.STORY.value
    )
    ticket = CreateTicket(None).execute(input_dto=input_dto)

    assert isinstance(ticket, Ticket)
    assert ticket.name_for_branch == "story/AUS-101-test-test"
