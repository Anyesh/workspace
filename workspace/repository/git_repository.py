from functools import lru_cache
from typing import overload

from git import Repo
from tinydb import Query, TinyDB
from workspace.entity.branch import Branch
from workspace.interface.repository import AbstractGitRepository


class GitRepository(AbstractGitRepository):
    def __init__(self, repo: str) -> None:
        self.repo = Repo(repo)

    def create(self, entity: Branch):
        self.repo.git.checkout("-b", entity.name)

    def stash(self):
        self.repo.git.add(".")
        current_branch = self.get()
        self.repo.git.stash("save", f"ws-stash-{current_branch}".lower())

    def stash_pop(self, entity: Branch):
        stash_name = f"ws-stash-{entity.name}".lower()

        stash_list = self.repo.git.stash("list").split("\n")
        stash_map = {x.split(":")[0]: x.split(":")[-1].strip() for x in stash_list if x}
        for k, v in stash_map.items():
            if v == stash_name:
                self.repo.git.stash("pop", k)
                break

    def pull(self):
        self.repo.git.pull()

    def get(self) -> str:
        return self.repo.active_branch

    def set(self, entity_name: str):
        self.repo.git.checkout(entity_name)

    @lru_cache
    def list(self) -> list[str]:
        return [ref.strip() for ref in self.repo.git.branch("-a").split("\n")]


class SubModuleRepository(GitRepository):
    def __init__(self, repo: str) -> None:
        super().__init__(repo)

    @lru_cache
    def list(self, detailed=False) -> list[str]:
        res = self.repo.git.execute(
            ["git", "submodule", "status"],
            with_extended_output=False,
            as_process=False,
            stdout_as_string=True,
        )
        if detailed:
            return res.split("\n")
        _, module, _ = zip(*[x.split() for x in res.split("\n")])
        return list(module)
