import os
import re
from enum import Enum

import inquirer
from git.exc import GitCommandError
from rich import pretty, traceback
from rich.console import Console

from .dto.create_branch import (
    AnswersToChangeBranchInputDto,
    AnswersToCreateBranchInputDto,
    CheckoutBranchInputDto,
    CreateBranchInputDto,
)
from .dto.create_ticket import CreateTicketInputDto
from .entity.task import TaskType
from .repository.git_repository import GitRepository, SubModuleRepository
from .repository.json_repository import JSONRepository
from .settings import BASEDIR, DEBUG
from .use_case.checkout_branch import CheckoutBranch
from .use_case.create_branch import CreateBranch
from .use_case.create_ticket import CreateTicket
from .utils import get_or_create_env, is_first_time_user

console = Console()
pretty.install()
traceback.install(show_locals=False)
user = os.getlogin()


class ACTIONS(Enum):
    CREATE = "create"
    CHANGE = "change"
    INFO = "info"

    @classmethod
    def all(cls):
        return list(map(lambda c: c.value, cls))


class CLIHandler:
    def __init__(self, project_root: str) -> None:
        self.project_root = project_root
        self.root_repository = SubModuleRepository(project_root)
        self.json_repo = JSONRepository()

    def handle_change_branch(self, answers: AnswersToChangeBranchInputDto):
        for app in answers.apps:
            console.print(f"⚙ changing branch of {app} ..", style="bold blue")
            repository = GitRepository(f"{self.project_root}/{app}")

            match_branch = self.json_repo.get_by_id(answers.ticket_id)
            if match_branch is None:
                raise GitCommandError("No branch found with that id", "git branch -a")
            console.print(f"⚙ checking out {match_branch} ..", style="bold orange1")
            input_dto = CheckoutBranchInputDto(
                name=match_branch.name_for_branch,
            )
            CheckoutBranch(repository).execute(input_dto=input_dto)

    def handle_create_branch(self, answers: AnswersToCreateBranchInputDto):
        ticket_input = CreateTicketInputDto(
            id=answers.ticket_id,
            description=answers.ticket_description,
            type=answers.ticket_type,
        )

        ticket = CreateTicket(self.json_repo).execute(input_dto=ticket_input)

        for app in answers.apps:
            console.print(f"⚙ creating branch on {app} ..", style="bold blue")
            repository = GitRepository(f"{self.project_root}/{app}")

            questions = [
                inquirer.List(
                    "base_branch",
                    message=f"Which branch you want to base {app} on?",
                    default="develop",
                    choices=repository.list(),
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
            console.print(f"⚙ saving any unsaved changes", style="bold orange1")
            repository.stash()
            console.print(
                f"⚙ checking out {answer['base_branch']} ..", style="bold orange1"
            )
            CheckoutBranch(repository).execute(input_dto=checkout_input_dto)
            console.print(f"⚙ pulling latest changes", style="bold orange1")
            repository.pull()
            CreateBranch(repository).execute(input_dto=input_dto)


class CLIAssistant:
    def __init__(self, action: str) -> None:
        console.print(f":smiley: Hello there {user or 'friend'}!", style="bold green")

        self.alaya_root: str | None = None
        self.action = action
        self.root_repository = SubModuleRepository("")

    def get_project_root(self):
        return (
            str(BASEDIR / "dummy")
            if DEBUG
            else os.getenv("ALAYA_ROOT", self.alaya_root)
        )

    def assist_first_time_user(self):
        console.print("Looks like this is your first time here", style="bold orange4")
        console.print(":raccoon: Let's get you set up", style="bold orange4")
        self.questions = [
            inquirer.Text(
                "alaya_path",
                message="Full path of your Alaya directory (something like '/home/user/alaya') ",
                validate=lambda _, x: len(x) > 0,
            ),
        ]
        answers = inquirer.prompt(
            questions=self.questions, raise_keyboard_interrupt=True
        )
        get_or_create_env("ALAYA_ROOT", answers["alaya_path"])
        console.print(
            f":thumbs_up: All set! using {answers['alaya_path']} as your root dir",
            style="bold green",
        )
        self.alaya_root = answers["alaya_path"]

    def common_questions(self):
        return [
            inquirer.Text(
                "ticket_id",
                message="Which Jira ticket are you working on?",
                validate=lambda _, x: re.match(r"^[A-Za-z]+-\d+$", x),
            ),
            inquirer.Checkbox(
                "apps",
                message="Which apps are you working on?",
                choices=self.root_repository.list(),
            ),
        ]

    def assist_create_branch(self):

        questions = [
            *self.common_questions(),
            inquirer.Text(
                "ticket_description",
                message="Short Description",
                validate=lambda _, x: len(x) > 3,
            ),
            inquirer.List(
                "ticket_type",
                message="Ticket Type",
                choices=TaskType.list(),
            ),
        ]
        return inquirer.prompt(questions, raise_keyboard_interrupt=True)

    def assist_change_branch(self):
        questions = self.common_questions()
        return inquirer.prompt(questions, raise_keyboard_interrupt=True)

    def run(self) -> None:
        try:
            if self.action not in ACTIONS.all():
                return console.print(
                    f"[ERROR] Unknown action [bold red]{self.action}[/bold red]. Valid choices are {ACTIONS.all()}",
                    style="red",
                )

            if is_first_time_user():
                self.assist_first_time_user()

            project_root = self.get_project_root()
            cli_handler = CLIHandler(project_root)
            self.root_repository = SubModuleRepository(project_root)

            if self.action == ACTIONS.CREATE.value:
                answers = self.assist_create_branch()
                cli_handler.handle_create_branch(
                    AnswersToCreateBranchInputDto(**answers)
                )

            elif self.action == ACTIONS.CHANGE.value:
                answers = self.assist_change_branch()
                cli_handler.handle_change_branch(
                    AnswersToChangeBranchInputDto(**answers)
                )

        except (ValueError, GitCommandError):
            console.print_exception()
        else:
            console.print("✓ All done! 🍀", style="bold green")


def app(action: str):
    CLIAssistant(action).run()


if __name__ == "__main__":
    app("change")
