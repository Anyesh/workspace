from git import Repo
from tests.config import FakeGitDir, fake_repo
from ward import raises, test
from workspace.dto.create_branch import CheckoutBranchInputDto, CreateBranchInputDto
from workspace.entity.branch import Branch
from workspace.repository.git_repository import GitRepository
from workspace.settings import BASEDIR
from workspace.use_case.checkout_branch import CheckoutBranch
from workspace.use_case.create_branch import CreateBranch


@test("running create method creates a git branch with given name")
def _():
    with FakeGitDir(BASEDIR / "tmp") as git_dir:
        _branch_name = "story/AUS-101"
        _base_branch = "master"

        repository = GitRepository(str(git_dir))
        branch = Branch(name=_branch_name, base_branch=_base_branch)
        repository.create(branch)

        assert repository.list() == ["master", _branch_name]


@test("running set method sets a git branch to given name")
def _():
    with FakeGitDir(BASEDIR / "tmp") as git_dir:
        _branch_name = "story/AUS-101"
        _base_branch = "master"

        repository = GitRepository(str(git_dir))
        branch = Branch(name=_branch_name, base_branch=_base_branch)
        repository.create(branch)
        repository.set(_branch_name)

        assert repository.get().name == _branch_name
