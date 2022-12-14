from enum import Enum


class Action(str, Enum):
    CREATE = "create"
    CHANGE = "change"
    INFO = "info"
    RESET = "reset"

    @classmethod
    def all(cls):
        return list(map(lambda c: c.value, cls))
