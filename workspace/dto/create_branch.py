from dataclasses import dataclass


@dataclass(slots=True)
class CreateBranchInputDto:
    name: str
    base_branch: str


@dataclass(slots=True)
class CheckoutBranchInputDto:
    name: str


@dataclass(slots=True)
class AnswersToCreateBranchInputDto:
    apps: list
    ticket_id: str
    ticket_description: str
    ticket_type: str


@dataclass(slots=True)
class AnswersToChangeBranchInputDto:
    apps: list
    ticket_id: str
