from tinydb import Query, TinyDB
from workspace.entity.branch import Branch
from workspace.entity.ticket import Ticket
from workspace.interface.repository import BaseRepository


class JSONRepository(BaseRepository):
    def __init__(self, repo=None) -> None:
        self.db = TinyDB("db.json")

    def create(self, entity: Ticket):
        self.db.insert(
            {"id": entity.id, "description": entity.description, "type": entity.type}
        )

    def get(self, *args, **kwargs) -> str:
        ...

    def get_by_id(self, id: str) -> Ticket | None:
        ticket = Query()
        _match = self.db.search(ticket.id == id.upper())
        return Ticket(**_match[0]) if _match else None

    def set(self, entity_name: str):
        ...

    def list(self) -> list[str]:
        return self.db.all()
