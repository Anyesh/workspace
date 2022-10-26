from __future__ import annotations

import re
from functools import lru_cache
import subprocess

from git import Head, Repo
from workspace.entity.branch import Branch
from workspace.interface.repository import AbstractGitRepository
from workspace.repository.json_repository import JSONRepository


# TODO: Modify repository to return Branch instance on get and list
class GitRepository(AbstractGitRepository):
    def __init__(self, repo: str) -> None:
        self.repo = Repo(repo)
        self._persistent_repo = JSONRepository()

    def create(self, entity: Branch):
        self.repo.git.checkout("-b", entity.name)
        self._persistent_repo.create(entity.__dict__)

    def stash(self):
        current_branch = self.get()
        for submodule in self.repo.submodules:
            submodule.module().git.add(all=True)
            submodule.module().git.stash("save", f"ws-stash-{current_branch}".lower())

        self.repo.git.add(all=True)
        self.repo.git.stash("save", f"ws-stash-{current_branch}".lower())

    @staticmethod
    def _pop(repo, stash_list, stash_name):
        stash_list = repo.git.stash("list").split("\n")
        stash_map = {x.split(":")[0]: x.split(":")[-1].strip() for x in stash_list if x}
        for k, v in stash_map.items():
            if v == stash_name:
                repo.git.stash("pop", k)
                break

    def stash_pop(self, entity_name: str):

        stash_name = f"ws-stash-{entity_name}".lower()
        stash_list = self.repo.git.stash("list").split("\n")

        self._pop(self.repo, stash_list, stash_name)
        for submodule in self.repo.submodules:
            self._pop(submodule.module(), stash_list, stash_name)

    def pull(self):
        self.repo.git.pull()
        for submodule in self.repo.submodules:
            submodule.module().git.pull("origin", submodule.branch)

    def sync_submodules(self):
        self.repo.git.submodule("update")

    def get(self) -> Head:
        return self.repo.active_branch

    def get_info(self) -> str:
        ...

    def set(self, entity_name: str):
        self.repo.git.checkout(entity_name)

    def find_by_id(self, id: str) -> str | None:
        pattern = re.compile(r"(\w+\/)([A-Z]+-\d+)(-*.*)")
        _list = self.list()

        match = None
        for x in _list:
            m = pattern.match(x)
            if m and m[2] == id.upper():
                match = x
                break
        return match

    def list(self) -> list[str]:
        return [
            ref.replace("*", "").strip() for ref in self.repo.git.branch().split("\n")
        ]


class SubModuleRepository(GitRepository):
    def __init__(self, repo: str) -> None:
        super().__init__(repo)

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
