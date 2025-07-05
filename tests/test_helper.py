from tests.helper import create_tree
from tree_edit_distance.core import Tree


def test_create_tree() -> None:
    text = "{a{b}{c}{d{e}}}"
    expected = Tree("a", [Tree("b"), Tree("c"), Tree("d", [Tree("e")])])
    assert create_tree(text) == expected
