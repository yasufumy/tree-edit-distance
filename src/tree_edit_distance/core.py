from collections.abc import MutableMapping, Sequence
from dataclasses import dataclass, field


@dataclass(frozen=True)
class TreeNode:
    label: str
    children: Sequence["TreeNode"] = field(default_factory=list)


@dataclass(frozen=True)
class PostorderNode:
    label: str
    leftmost_leaf_index: int


def traverse_postorder(root: TreeNode) -> Sequence[PostorderNode]:
    nodes: list[PostorderNode] = []

    def _traverse(node: TreeNode) -> int:
        if not node.children:
            leftmost_leaf_index = len(nodes)
        else:
            leftmost_leaf_index = _traverse(node.children[0])
            for child in node.children[1:]:
                _traverse(child)

        nodes.append(PostorderNode(node.label, leftmost_leaf_index))
        return leftmost_leaf_index

    _traverse(root)

    return nodes


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


@dataclass(frozen=True)
class TreeMatcher:
    cost_function: CostFunction
    traversal1: Sequence[PostorderNode]
    traversal2: Sequence[PostorderNode]
    treedist_memo: MutableMapping[tuple[int, int], int]
    forestdist_memo: MutableMapping[tuple[int, int, int, int], int]

    def find_minimum_cost(self) -> int:
        if not self.traversal1:
            return sum(self.cost_function.insert(node) for node in self.traversal2)
        if not self.traversal2:
            return sum(self.cost_function.delete(node) for node in self.traversal1)
        return self.__treedist(len(self.traversal1) - 1, len(self.traversal2) - 1)

    @classmethod
    def new(cls, root1: TreeNode, root2: TreeNode) -> "TreeMatcher":
        return cls(
            cost_function=CostFunction(),
            traversal1=traverse_postorder(root1),
            traversal2=traverse_postorder(root2),
            treedist_memo={},
            forestdist_memo={},
        )

    def __treedist(self, i: int, j: int) -> int:
        key = (i, j)
        if key not in self.treedist_memo:
            self.treedist_memo[key] = self.__forestdist(i, j, i, j)
        return self.treedist_memo[key]

    def __forestdist(self, i: int, j: int, i_root: int, j_root: int) -> int:
        key = (i, j, i_root, j_root)
        if key in self.forestdist_memo:
            return self.forestdist_memo[key]

        l_i_root = self.traversal1[i_root].leftmost_leaf_index
        l_j_root = self.traversal2[j_root].leftmost_leaf_index
        node_i = self.traversal1[i]
        node_j = self.traversal2[j]

        if i < l_i_root and j < l_j_root:
            self.forestdist_memo[key] = 0
            return 0
        elif j < l_j_root:
            self.forestdist_memo[key] = self.__forestdist(
                i - 1, j, i_root, j_root
            ) + self.cost_function.delete(node_i)
            return self.forestdist_memo[key]
        elif i < l_i_root:
            self.forestdist_memo[key] = self.__forestdist(
                i, j - 1, i_root, j_root
            ) + self.cost_function.insert(node_j)
            return self.forestdist_memo[key]

        cost_insertion = self.__forestdist(
            i, j - 1, i_root, j_root
        ) + self.cost_function.insert(node_j)

        cost_deletion = self.__forestdist(
            i - 1, j, i_root, j_root
        ) + self.cost_function.delete(node_i)

        l_i = node_i.leftmost_leaf_index
        l_j = node_j.leftmost_leaf_index

        if l_i == l_i_root and l_j == l_j_root:
            cost_renaming = self.__forestdist(
                i - 1, j - 1, i_root, j_root
            ) + self.cost_function.rename(node_i, node_j)
        else:
            cost_renaming = self.__forestdist(
                l_i - 1, l_j - 1, i_root, j_root
            ) + self.__treedist(i, j)

        self.forestdist_memo[key] = min(cost_insertion, cost_deletion, cost_renaming)
        return self.forestdist_memo[key]
