from dataclasses import FrozenInstanceError

from tests.config import fake_branch_repo
from ward import raises, test
from workspace.dto.create_branch import CreateBranchInputDto
from workspace.entity.branch import Branch
from workspace.use_case.create_branch import CreateBranch

# @test("cheackout a branch happy path")
# def _(repo=fake_branch_repo):
#     input_dto = CreateBranchInputDto(name="story/AUS-101", base_branch="develop")
#     CreateBranch(repo).execute(input_dto=input_dto)

#     created_branch = repo.get()

#     assert isinstance(created_branch, Branch)
#     assert created_branch.name == "story/AUS-101"
#     assert created_branch.base_branch == "develop"


# @test("branch once created should not be open to modification")
# def _(repo=fake_branch_repo):
#     input_dto = CreateBranchInputDto(name="story/AUS-101", base_branch="develop")
#     CreateBranch(repo).execute(input_dto=input_dto)

#     created_branch = repo.get()
#     with raises(FrozenInstanceError):
#         created_branch.name = "story/AUS-102"
