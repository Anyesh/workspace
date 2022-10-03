from workspace.dto.create_branch import CreateBranchInputDto
from workspace.entity.branch import Branch
from workspace.interface.repository import AbstractGitRepository


class CreateBranch:
    def __init__(self, repository: AbstractGitRepository):
        self._repository = repository

    def execute(self, input_dto: CreateBranchInputDto) -> None:

        branch = Branch(
            name=input_dto.name,
            base_branch=input_dto.base_branch,
        )
        self._repository.create(branch)
