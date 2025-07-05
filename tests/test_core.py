from tree_edit_distance.core import Cost, Tree, distance


def test_distance(test_cases: list[tuple[Tree[str], Tree[str], int]]) -> None:
    cost = Cost[str].default()
    for t1, t2, expected_cost in test_cases:
        assert distance(t1, t2, cost) == expected_cost
