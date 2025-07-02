import json
from pathlib import Path

import pytest

from tree_edit_distance.core import TreeMatcher, TreeNode


def create_tree(text: str) -> TreeNode:
    tree_stack: list[tuple[TreeNode, int]] = []
    stack = []
    for letter in text:
        if letter == "{":
            stack.append("")
        elif letter == "}":
            label = stack.pop()
            children = []
            while tree_stack and tree_stack[-1][1] > len(stack):
                child, _ = tree_stack.pop()
                children.append(child)
            children.reverse()
            tree_stack.append((TreeNode(label, children), len(stack)))
        else:
            stack[-1] += letter
    return tree_stack[0][0]


def test_create_tree() -> None:
    text = "{a{b}{c}{d{e}}}"
    expected = TreeNode(
        "a", [TreeNode("b"), TreeNode("c"), TreeNode("d", [TreeNode("e")])]
    )
    assert create_tree(text) == expected


@pytest.fixture
def test_cases() -> list[tuple[TreeNode, TreeNode, int]]:
    file = Path(__file__).parent / "correctness_test_cases.json"
    with open(file) as f:
        data = json.load(f)

    return [(create_tree(x["t1"]), create_tree(x["t2"]), x["d"]) for x in data]


def test_find_minimum_cost(test_cases: list[tuple[TreeNode, TreeNode, int]]) -> None:
    for t1, t2, expected_cost in test_cases:
        matcher = TreeMatcher.new(t1, t2)
        assert matcher.find_minimum_cost() == expected_cost
