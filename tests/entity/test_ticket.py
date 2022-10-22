from ward import raises, test
from workspace.entity.task import TaskType
from workspace.entity.ticket import Ticket


@test("branch name is post initialized after all ticket attributes are provided")
def _():
    t1 = Ticket(id="AUS-1", description="Ability to void sent claim")
    t2 = Ticket(id="AUS-2", description="test", type=TaskType.SUBTASK)
    t3 = Ticket(
        id="AUS-3",
        description="test   ",
    )
    assert t1.name_for_branch == "story/AUS-1-ability-to-void-sent-claim"
    assert t2.name_for_branch == "subtask/AUS-2-test"
    assert t3.name_for_branch == "story/AUS-3-test"
