from __future__ import annotations

from abc import ABC, abstractmethod

from workspace.entity.branch import Branch


class BaseRepository(ABC):
    @abstractmethod
    def create(self, entity) -> None:
        ...

    @abstractmethod
    def get(self, *args, **kwargs) -> str:
        ...

    @abstractmethod
    def list(self) -> list[str]:
        ...


class AbstractGitRepository(BaseRepository):
    @abstractmethod
    def stash(self) -> None:
        ...

    @abstractmethod
    def pull(self) -> None:
        ...

    @abstractmethod
    def stash_pop(self, entity: Branch) -> None:
        ...

    @abstractmethod
    def set(self, entity_name: str) -> None:
        ...
