from collections import Counter
from dataclasses import FrozenInstanceError

from tests.config import fake_repo
from ward import raises, test
from workspace.dto.create_branch import CheckoutBranchInputDto, CreateBranchInputDto
from workspace.entity.branch import Branch
from workspace.use_case.checkout_branch import CheckoutBranch
from workspace.use_case.create_branch import CreateBranch


@test("checkout a branch happy path")
def _(repo=fake_repo):
    input_dto = CheckoutBranchInputDto(name="story/AUS-101")
    CheckoutBranch(repo).execute(input_dto=input_dto)

    assert repo.get() == "story/AUS-101"
