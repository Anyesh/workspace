from dataclasses import FrozenInstanceError

from tests.config import fake_repo
from ward import raises, test
from workspace.dto.create_ticket import CreateTicketInputDto
from workspace.entity.branch import Branch
from workspace.entity.task import TaskType
from workspace.entity.ticket import Ticket
from workspace.use_case.create_ticket import CreateTicket


@test("create a ticket happy path")
def _(repo=fake_repo):
    input_dto = CreateTicketInputDto(
        id="aus-101", description="test test", type=TaskType.STORY.value
    )
    CreateTicket(repo).execute(input_dto=input_dto)

    created_ticket = repo.list()[-1]

    assert isinstance(created_ticket, Ticket)


@test("creating a ticket creates name for branch from it's description and id")
def _(repo=fake_repo):
    input_dto = CreateTicketInputDto(
        id="aus-101", description="test test", type=TaskType.STORY.value
    )
    CreateTicket(repo).execute(input_dto=input_dto)

    created_ticket = repo.list()[-1]

    assert isinstance(created_ticket, Ticket)
    assert created_ticket.name_for_branch == "story/AUS-101-test-test"
