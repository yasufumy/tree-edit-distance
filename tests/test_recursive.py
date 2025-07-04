from tree_edit_distance.core import TreeNode
from tree_edit_distance.recursive import TreeMatcher


def test_find_minimum_cost(test_cases: list[tuple[TreeNode, TreeNode, int]]) -> None:
    for t1, t2, expected_cost in test_cases:
        matcher = TreeMatcher.new(t1, t2)
        assert matcher.find_minimum_cost() == expected_cost
