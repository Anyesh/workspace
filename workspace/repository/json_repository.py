from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, is_dataclass
from functools import partial
from lib2to3.pytree import Base

from tinydb import Query, TinyDB
from tinydb.table import Document
from workspace.entity.ticket import Ticket
from workspace.interface.repository import BaseRepository
from workspace.settings import BASEDIR

# TODO!: Improve this whole repository
class JSONRepository(BaseRepository):
    def __init__(self, repo=None) -> None:
        self.db = TinyDB(str(BASEDIR / "db.json"))

    def create(self, result: dict):
        self.db.insert(result)

    def get(self, *args, **kwargs) -> str:
        ...

    def get_most_common_apps(self) -> list:
        app = Query()
        apps = self.db.search(app.apps.exists())
        if not apps:
            return []
        data = [x["apps"] for x in apps]
        data = [item for sublist in data for item in sublist]
        data = Counter(data).most_common()
        return [x[0] for x in data]

    def get_recent_branches(self) -> list[str]:
        branch = Query()
        branches = self.db.search(branch.name.exists())
        if not branches:
            return []
        sorted_branches = sorted(branches, key=lambda x: x["created_at"], reverse=True)
        return [x["name"] for x in sorted_branches]

    def set(self, entity_name: str):
        ...

    def list(self) -> list[str]:
        return self.db.all()


# persist result decorator


def save_answer(repository: BaseRepository):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result:
                repository.create({**result, "called_by": func.__name__})
            return result

        return wrapper

    return decorator


jr = JSONRepository()
print(jr.get_most_common_apps())
print(jr.get_recent_branches())
