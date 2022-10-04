from workspace.dto.create_branch import CheckoutBranchInputDto, CreateBranchInputDto
from workspace.entity.branch import Branch
from workspace.interface.repository import AbstractGitRepository


class CheckoutBranch:
    def __init__(self, repository: AbstractGitRepository):
        self._repository = repository

    def execute(self, input_dto: CheckoutBranchInputDto) -> None:

        branch = Branch(name=input_dto.name)
        self._repository.set(branch.name)
