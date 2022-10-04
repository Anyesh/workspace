from __future__ import annotations

import inquirer
from git.exc import GitCommandError
from rich.console import Console

from ..dto.create_branch import (
    AnswersToChangeBranchInputDto,
    AnswersToCreateBranchInputDto,
    CheckoutBranchInputDto,
    CreateBranchInputDto,
)
from ..dto.create_ticket import CreateTicketInputDto
from ..repository.git_repository import GitRepository
from ..repository.json_repository import JSONRepository
from ..use_case.checkout_branch import CheckoutBranch
from ..use_case.create_branch import CreateBranch
from ..use_case.create_ticket import CreateTicket
from ..utils import get_loggedin_user

console = Console()
user = get_loggedin_user()


class CLIService:
    def __init__(self, project_root: str) -> None:
        self.__project_root = project_root

    def handle_change_branch(self, answers: AnswersToChangeBranchInputDto) -> None:
        """Find a branch by id from local db and checkout that branch for all apps"""

        for app in answers.apps:
            console.log(f"⚙ changing branch of {app} ..", style="bold blue")
            repository = GitRepository(f"{self.__project_root}/{app}")

            match_branch = repository.find_by_id(answers.ticket_id)
            if match_branch is None:
                raise GitCommandError("No branch found with that id", "git branch -a")

            # Saving any unsaved changes of current branch
            repository.stash()

            # Popping any previos saved changes
            repository.stash_pop(match_branch)
            input_dto = CheckoutBranchInputDto(
                name=match_branch,
            )
            console.log(f"⚙ checking out {match_branch} ..", style="bold blue")
            CheckoutBranch(repository).execute(input_dto=input_dto)

    def handle_create_branch(self, answers: AnswersToCreateBranchInputDto) -> None:
        """Create a new branch for all apps"""

        ticket_input = CreateTicketInputDto(
            id=answers.ticket_id,
            description=answers.ticket_description,
            type=answers.ticket_type,
        )

        ticket = CreateTicket(None).execute(input_dto=ticket_input)

        for app in answers.apps:
            console.log(f"⚙ creating branch on {app} ..", style="bold blue")
            repository = GitRepository(f"{self.__project_root}/{app}")

            # TODO: Remove this coupling
            questions = [
                inquirer.List(
                    "base_branch",
                    message=f"Which branch you want to base {app} on?",
                    default="develop",
                    choices=repository.list(),
                    carousel=True,
                )
            ]

            answer = inquirer.prompt(questions=questions, raise_keyboard_interrupt=True)

            input_dto = CreateBranchInputDto(
                name=ticket.name_for_branch,
                base_branch=answer["base_branch"],
            )
            checkout_input_dto = CheckoutBranchInputDto(
                name=answer["base_branch"],
            )
            console.log("⚙ saving any unsaved changes", style="bold orange1")
            repository.stash()
            console.log(
                f"⚙ checking out {answer['base_branch']} ..", style="bold orange1"
            )
            CheckoutBranch(repository).execute(input_dto=checkout_input_dto)
            console.log("⚙ pulling latest changes", style="bold orange1")

            if repository.get().tracking_branch() is None:
                console.log(
                    "⚠ no tracking branch found. Nohing to pull.", style="bold orange1"
                )
            else:
                repository.pull()
            repository.sync_submodules()
            CreateBranch(repository).execute(input_dto=input_dto)
            console.log(
                f"⚙ checking out {ticket.name_for_branch} ..", style="bold green"
            )
