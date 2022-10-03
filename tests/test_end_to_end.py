from ward import test
from workspace.dto.create_branch import CheckoutBranchInputDto, CreateBranchInputDto
from workspace.repository.git_repository import GitRepository
from workspace.settings import BASEDIR
from workspace.use_case.checkout_branch import CheckoutBranch
from workspace.use_case.create_branch import CreateBranch

from tests.config import FakeGitDir


@test("end to end create and checkout to created branch happy path")
def _():
    with FakeGitDir(BASEDIR / "tmp") as git_dir:
        _branch_name = "story/AUS-101"
        _base_branch = "master"

        repository = GitRepository(str(git_dir))
        input_dto = CreateBranchInputDto(
            name=_branch_name,
            base_branch=_base_branch,
        )
        checkout_input_dto = CheckoutBranchInputDto(
            name=_base_branch,
        )

        CheckoutBranch(repository).execute(input_dto=checkout_input_dto)
        CreateBranch(repository).execute(input_dto=input_dto)

        assert repository.get().name == _branch_name
