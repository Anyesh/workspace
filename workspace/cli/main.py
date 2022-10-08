import argh

from .actions import Action
from .assistant import CLIAssistant


@argh.arg("action", choices=Action.all(), help="Action to perform")
@argh.arg("ticket_id", help="Ticket ID to use for the action", nargs="?")
def app(action: str, ticket_id: str):
    CLIAssistant(action, quick_ticket_id=ticket_id).run()


def cli():
    argh.dispatch_command(app)
