from collections.abc import Sequence
from dataclasses import dataclass, field


@dataclass(frozen=True)
class TreeNode:
    label: str
    children: Sequence["TreeNode"] = field(default_factory=list)


@dataclass(frozen=True)
class PostorderNode:
    label: str
    index: int
    leftmost_leaf_index: int
    is_keyroot: bool


@dataclass(frozen=True)
class CostFunction:
    insertion_cost: int = 1
    deletion_cost: int = 1
    renaming_cost: int = 1

    def insert(self, node: PostorderNode) -> int:
        return self.insertion_cost

    def delete(self, node: PostorderNode) -> int:
        return self.deletion_cost

    def rename(self, node1: PostorderNode, node2: PostorderNode) -> int:
        return self.renaming_cost if node1.label != node2.label else 0


def traverse_postorder(root: TreeNode) -> Sequence[PostorderNode]:
    nodes: list[PostorderNode] = []

    def _traverse(node: TreeNode, is_keyroot: bool) -> int:
        if not node.children:
            leftmost_leaf_index = len(nodes)
        else:
            leftmost_leaf_index = _traverse(node.children[0], is_keyroot=False)
            for child in node.children[1:]:
                _traverse(child, is_keyroot=True)

        nodes.append(
            PostorderNode(node.label, len(nodes), leftmost_leaf_index, is_keyroot)
        )
        return leftmost_leaf_index

    _traverse(root, True)

    return nodes
