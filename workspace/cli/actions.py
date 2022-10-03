from enum import Enum


class Action(Enum):
    CREATE = "create"
    CHANGE = "change"
    INFO = "info"

    @classmethod
    def all(cls):
        return list(map(lambda c: c.value, cls))
