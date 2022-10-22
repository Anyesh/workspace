from enum import Enum


class TaskType(str, Enum):
    STORY = "story"
    SUBTASK = "subtask"
    BUGFIX = "bugfix"
    HOTFIX = "hotfix"
    RELEASE = "release"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
