from ward import raises, test
from workspace.entity.branch import Branch


@test("default base branch is develop")
def _():
    b1 = Branch(name="AUS-123")
    assert b1.base_branch == "develop"


@test("TypeError when args is passed instead of kwargs")
def _():
    with raises(TypeError):
        Branch("AUS-123", "Ability to void sent claim", "master")
