import argh

from .actions import Action
from .assistant import CLIAssistant


@argh.arg("action", choices=Action.all(), help="Action to perform")
def app(action: str):
    CLIAssistant(action).run()


def cli():
    argh.dispatch_command(app)
