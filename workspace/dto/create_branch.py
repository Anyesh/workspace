from dataclasses import dataclass


@dataclass
class CreateBranchInputDto:
    name: str
    base_branch: str


@dataclass
class CheckoutBranchInputDto:
    name: str


@dataclass
class AnswersToCreateBranchInputDto:
    apps: list
    ticket_id: str
    ticket_description: str
    ticket_type: str


@dataclass
class AnswersToChangeBranchInputDto:
    apps: list
    ticket_id: str
