from __future__ import annotations

import os
import re

import inquirer
from git import InvalidGitRepositoryError
from git.exc import GitCommandError
from rich.columns import Columns
from rich.console import Console

from ..cli.actions import Action
from ..cli.service import CLIService
from ..dto.create_branch import (
    AnswersToChangeBranchInputDto,
    AnswersToCreateBranchInputDto,
)
from ..entity.task import TaskType
from ..repository.git_repository import SubModuleRepository
from ..settings import BASEDIR, DEBUG
from ..utils import get_loggedin_user, get_or_create_env, is_first_time_user

user = get_loggedin_user()
console = Console()


class CLIAssistant:
    def __init__(self, action: str) -> None:
        console.log(f":smiley: Hello there {user}!", style="bold green")

        self.__alaya_root: str | None = None
        self.__action = action
        self.__root_repository: SubModuleRepository | None = None

    def get_project_root(self):
        return (
            str(BASEDIR / "tmp")
            if DEBUG
            else os.getenv("ALAYA_ROOT", self.__alaya_root)
        )

    def assist_first_time_user(self):
        console.print("Looks like this is your first time here", style="bold orange4")
        console.print(":raccoon: Let's get you set up", style="bold orange4")
        self.questions = [
            inquirer.Text(
                "alaya_path",
                message="Full path of your Alaya directory (something like '/home/user/path') ",
                validate=lambda _, x: len(x) > 0,
            ),
        ]
        answers = inquirer.prompt(
            questions=self.questions, raise_keyboard_interrupt=True
        )
        get_or_create_env("ALAYA_ROOT", answers["alaya_path"])
        console.log(
            f":thumbs_up: All set! using {answers['alaya_path']} as your root dir",
            style="bold green",
        )
        self.__alaya_root = answers["alaya_path"]

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
                choices=self.__root_repository.list(),
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
            if self.__action not in Action.all():
                return console.print(
                    f"[ERROR] Unknown action [bold red]{self.__action}[/bold red]. Valid choices are {Action.all()}",
                    style="red",
                )

            if is_first_time_user():
                self.assist_first_time_user()

            project_root = self.get_project_root()
            cli_handler = CLIService(project_root)
            self.__root_repository = SubModuleRepository(project_root)

            if self.__action == Action.CREATE.value:
                answers = self.assist_create_branch()
                cli_handler.handle_create_branch(
                    AnswersToCreateBranchInputDto(**answers)
                )

            elif self.__action == Action.CHANGE.value:
                answers = self.assist_change_branch()
                cli_handler.handle_change_branch(
                    AnswersToChangeBranchInputDto(**answers)
                )
            elif self.__action == Action.INFO.value:
                console.print(f"Your current project path: '{project_root}'")
                console.print(
                    f"Your current root branch is [green]'{self.__root_repository.get()}'[/green]"
                )
                console.print("Your submodules status are: ")
                console.print(
                    Columns(self.__root_repository.list(detailed=True)),
                    style="bold green",
                )
        except KeyboardInterrupt:
            console.print("Seeya! Exiting...", style="green")
        except InvalidGitRepositoryError:
            console.print("Invalid git repository provided", style="red")
        except (ValueError, GitCommandError):
            console.print_exception()
        else:
            console.log("✓ All done! 🍀", style="bold green")
