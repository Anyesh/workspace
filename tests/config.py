import shutil
from pathlib import Path

from git import Repo
from ward import fixture
from workspace.interface.repository import AbstractGitRepository


class FakeGitDir:
    def __init__(self, git_dir: Path):
        self.git_dir = git_dir

    def setup_test_git_submodule_directory(self):
        submodule_1 = self.git_dir / "submodule_1"
        submodule_2 = self.git_dir / "submodule_2"

        self.git_dir.mkdir(exist_ok=True)
        submodule_1.mkdir(exist_ok=True)
        submodule_2.mkdir(exist_ok=True)

        repo = Repo.init(self.git_dir)

        submodule_1_repo = Repo.init(submodule_1)
        (submodule_1 / "sub_file1").touch()
        (submodule_1 / "sub_file2").touch()
        submodule_1_repo.index.add(["sub_file1", "sub_file2"])
        submodule_1_repo.index.commit("initial commit 1")
        repo.git.submodule("add", str(submodule_1))
        submodule_1_repo.git.submodule("init")
        submodule_1_repo.index.commit("submodule 1 added")

        submodule_2_repo = Repo.init(submodule_2)
        (submodule_2 / "sub_file1").touch()
        (submodule_2 / "sub_file2").touch()
        submodule_2_repo.index.add(["sub_file1", "sub_file2"])
        submodule_2_repo.index.commit("initial commit 2")
        repo.git.submodule("add", str(submodule_2))
        submodule_2_repo.git.submodule("init")
        submodule_2_repo.index.commit("submodule 2 added")
        return self

    def __enter__(self):
        self.setup_test_git_submodule_directory()
        return self.git_dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        # remove created directory and files
        if self.git_dir.exists():
            shutil.rmtree(self.git_dir)


class FakeBranchRepository(AbstractGitRepository, list):
    def __init__(self, repo: str) -> None:
        self.repo = repo

    def create(self, entity: str):
        self.append(entity)

    def stash(self):
        pass

    def stash_pop(self, entity):
        pass

    def pull(self):
        pass

    def get(self) -> str:
        return self[-1]

    def set(self, entity_name: str):
        pass

    def list(self) -> list[str]:
        return self


@fixture
def fake_branch_repo():
    repo = FakeBranchRepository("/repo")
    yield repo
    repo.clear()
