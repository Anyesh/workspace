from dataclasses import dataclass


@dataclass(kw_only=True, slots=True)
class CreateBranchInputDto:
    name: str
    base_branch: str


@dataclass(kw_only=True, slots=True)
class CheckoutBranchInputDto:
    name: str


@dataclass(kw_only=True, slots=True)
class AnswersToCreateBranchInputDto:
    apps: list
    ticket_id: str
    ticket_description: str
    ticket_type: str


@dataclass(kw_only=True, slots=True)
class AnswersToChangeBranchInputDto:
    apps: list
    ticket_id: str
