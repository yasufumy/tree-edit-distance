import json
from pathlib import Path

import pytest

from tests.helper import create_tree
from tree_edit_distance.core import Tree


@pytest.fixture
def test_cases() -> list[tuple[Tree[str], Tree[str], int]]:
    file = Path(__file__).parent / "correctness_test_cases.json"
    with open(file) as f:
        data = json.load(f)

    return [(create_tree(x["t1"]), create_tree(x["t2"]), x["d"]) for x in data]
