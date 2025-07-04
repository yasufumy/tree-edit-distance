from tests.helper import create_tree
from tree_edit_distance.core import TreeNode


def test_create_tree() -> None:
    text = "{a{b}{c}{d{e}}}"
    expected = TreeNode(
        "a", [TreeNode("b"), TreeNode("c"), TreeNode("d", [TreeNode("e")])]
    )
    assert create_tree(text) == expected
