from git import Repo
from ward import raises, test
from workspace.dto.create_branch import CreateBranchInputDto
from workspace.repository.git_repository import GitRepository
from workspace.settings import BASEDIR
from workspace.use_case.create_branch import CreateBranch

# @test("something here")
# def _():
#     repository = GitRepository(str(BASEDIR / "tmp"))
#     input_dto = CreateBranchInputDto(
#         id="AUS-1", description="claim is claim", base_branch="develop"
#     )
#     CreateBranch(repository).execute(input_dto=input_dto)
