from collections.abc import Sequence
from dataclasses import dataclass

from tree_edit_distance.core import (
    CostFunction,
    PostorderNode,
    TreeNode,
    traverse_postorder,
)


@dataclass(frozen=True)
class TreeMatcher:
    cost_function: CostFunction
    traversal1: Sequence[PostorderNode]
    traversal2: Sequence[PostorderNode]

    @classmethod
    def new(cls, root1: TreeNode, root2: TreeNode) -> "TreeMatcher":
        return cls(
            cost_function=CostFunction(),
            traversal1=traverse_postorder(root1),
            traversal2=traverse_postorder(root2),
        )

    def find_minimum_cost(self) -> int:
        """
        Calculates the edit distance between two trees.
        """
        if not self.traversal1:
            return sum(self.cost_function.insert(node) for node in self.traversal2)
        if not self.traversal2:
            return sum(self.cost_function.delete(node) for node in self.traversal1)

        keyroots1 = [i for i, node in enumerate(self.traversal1) if node.is_keyroot]
        keyroots2 = [i for i, node in enumerate(self.traversal2) if node.is_keyroot]

        treedist: list[list[int]] = [
            [0] * len(self.traversal2) for _ in range(len(self.traversal1))
        ]
        for i_keyroot in keyroots1:
            for j_keyroot in keyroots2:
                self.__compute_treedist(i_keyroot, j_keyroot, treedist)

        return treedist[-1][-1]

    def __compute_treedist(
        self, i_root: int, j_root: int, treedist: list[list[int]]
    ) -> None:
        """
        Computes treedist for a pair of subtrees rooted at given keyroots.
        """
        l_i_root = self.traversal1[i_root].leftmost_leaf_index
        l_j_root = self.traversal2[j_root].leftmost_leaf_index

        nodes1 = self.traversal1[l_i_root : i_root + 1]
        nodes2 = self.traversal2[l_j_root : j_root + 1]

        forestdist = [[0] * (len(nodes2) + 1) for _ in range(len(nodes1) + 1)]

        for i, node1 in enumerate(nodes1, 1):
            forestdist[i][0] = forestdist[i - 1][0] + self.cost_function.delete(node1)
        for j, node2 in enumerate(nodes2, 1):
            forestdist[0][j] = forestdist[0][j - 1] + self.cost_function.insert(node2)

        for i, node1 in enumerate(nodes1, 1):
            l1 = node1.leftmost_leaf_index
            for j, node2 in enumerate(nodes2, 1):
                l2 = node2.leftmost_leaf_index

                cost_deletion = forestdist[i - 1][j] + self.cost_function.delete(node1)
                cost_insertion = forestdist[i][j - 1] + self.cost_function.insert(node2)

                if l1 == l_i_root and l2 == l_j_root:
                    cost_renaming = forestdist[i - 1][
                        j - 1
                    ] + self.cost_function.rename(node1, node2)
                    treedist[node1.index][node2.index] = forestdist[i][j] = min(
                        cost_deletion, cost_insertion, cost_renaming
                    )
                else:
                    cost_renaming = (
                        forestdist[l1 - l_i_root][l2 - l_j_root]
                        + treedist[node1.index][node2.index]
                    )
                    forestdist[i][j] = min(cost_deletion, cost_insertion, cost_renaming)
