from __future__ import annotations

import inquirer
from rich.console import Console

from ..dto.create_branch import (
    AnswersToChangeBranchInputDto,
    AnswersToCreateBranchInputDto,
    CheckoutBranchInputDto,
    CreateBranchInputDto,
)
from ..dto.create_ticket import CreateTicketInputDto
from ..exception.branch import GitBranchChangeException
from ..repository.git_repository import GitRepository
from ..repository.json_repository import JSONRepository, save_answer
from ..use_case.checkout_branch import CheckoutBranch
from ..use_case.create_branch import CreateBranch
from ..use_case.create_ticket import CreateTicket
from ..utils import common_choice_helper, get_loggedin_user

console = Console()
user = get_loggedin_user()

_cache_repository = JSONRepository()


#! TODO: Organize this
@save_answer(repository=JSONRepository())
def assist_base_branch_selection(app: str, repository: GitRepository) -> dict:
    questions = [
        inquirer.List(
            "base_branch",
            message=f"Which branch you want to base '{app}' on?",
            default="develop",
            choices=common_choice_helper(
                repository.list(), _cache_repository.get_recent_branches()
            ),
            carousel=True,
        )
    ]

    return inquirer.prompt(questions=questions, raise_keyboard_interrupt=True)


class CLIService:
    def __init__(self, project_root: str) -> None:
        self.__project_root = project_root

    def handle_change_branch(self, answers: AnswersToChangeBranchInputDto) -> None:
        """Find a branch by id from local db and checkout that branch for all apps"""

        for app in answers.apps:
            console.print(f"⚙ changing branch of {app} ..", style="bold blue")
            repository = GitRepository(f"{self.__project_root}/{app}")

            match_branch = repository.find_by_id(answers.ticket_id)
            if match_branch is None:
                console.print(f"Branch not found for {app}", style="bold red")
                continue
                # raise GitBranchChangeException(
                #     f"No branch found with id {answers.ticket_id}"
                # )

            # Saving any unsaved changes of current branch
            repository.stash()

            # Popping any previos saved changes
            repository.stash_pop(match_branch)
            input_dto = CheckoutBranchInputDto(name=match_branch)
            console.print(f"⚙ checking out {match_branch} ..", style="bold blue")
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
            console.print(f"⚙ creating branch on {app} ..", style="bold blue")
            repository = GitRepository(f"{self.__project_root}/{app}")
            any_match = repository.find_by_id(answers.ticket_id)
            if any_match:
                # TODO: Remove this duplicate
                console.print(
                    f"Branch already exists with same id {any_match}",
                    style="bold green",
                )
                console.print("⚙ saving any unsaved changes", style="bold blue")
                repository.stash()
                console.print("Checking out to existing branch", style="bold green")
                checkout_input_dto = CheckoutBranchInputDto(
                    name=any_match,
                )
                CheckoutBranch(repository).execute(input_dto=checkout_input_dto)
                continue

            base_branch_answer = assist_base_branch_selection(app, repository)
            input_dto = CreateBranchInputDto(
                name=ticket.name_for_branch,
                base_branch=base_branch_answer["base_branch"],
            )
            checkout_input_dto = CheckoutBranchInputDto(
                name=base_branch_answer["base_branch"],
            )
            console.print("⚙ saving any unsaved changes", style="bold orange1")
            repository.stash()
            console.print(
                f"⚙ checking out '{base_branch_answer['base_branch']}' ..",
                style="bold green",
            )
            CheckoutBranch(repository).execute(input_dto=checkout_input_dto)
            console.print("⚙ pulling latest changes", style="bold blue")

            if repository.get().tracking_branch() is None:
                console.print(
                    "⚠ no tracking branch found. Nothing to pull.", style="bold orange1"
                )
            else:
                repository.pull()
            repository.sync_submodules()
            CreateBranch(repository).execute(input_dto=input_dto)
            console.print(
                f"⚙ checking out {ticket.name_for_branch} ..", style="bold blue"
            )
