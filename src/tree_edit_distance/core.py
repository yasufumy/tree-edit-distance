from collections.abc import Callable, Generator, Sequence
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Traversed[T]:
    value: T
    index: int
    leftmost_leaf_index: int
    is_keyroot: bool


@dataclass(frozen=True)
class PostorderTraversal[T]:
    nodes: Sequence[Traversed[T]]

    def __len__(self) -> int:
        return len(self.nodes)

    def __iter__(self) -> Generator[Traversed[T]]:
        yield from self.nodes

    def get_subtree(self, node: Traversed[T]) -> Sequence[Traversed[T]]:
        return self.nodes[node.leftmost_leaf_index : node.index + 1]

    @property
    def keyroots(self) -> Sequence[Traversed[T]]:
        return [node for node in self.nodes if node.is_keyroot]


@dataclass(frozen=True)
class Tree[T]:
    node: T
    children: Sequence["Tree[T]"] = field(default_factory=list)

    def postorder(self) -> PostorderTraversal[T]:
        nodes: list[Traversed[T]] = []

        def _traverse(tree: Tree[T], is_keyroot: bool) -> int:
            if not tree.children:
                leftmost_leaf_index = len(nodes)
            else:
                leftmost_leaf_index = _traverse(tree.children[0], is_keyroot=False)
                for child in tree.children[1:]:
                    _traverse(child, is_keyroot=True)

            nodes.append(
                Traversed(tree.node, len(nodes), leftmost_leaf_index, is_keyroot)
            )
            return leftmost_leaf_index

        _traverse(self, True)

        return PostorderTraversal(nodes)


@dataclass(frozen=True)
class Cost[T]:
    delete: Callable[[T], int]
    insert: Callable[[T], int]
    relabel: Callable[[T, T], int]

    @classmethod
    def default(cls) -> "Cost[T]":
        return cls(
            delete=lambda _: 1,
            insert=lambda _: 1,
            relabel=lambda node1, node2: 1 if node1 != node2 else 0,
        )


def distance[T](tree1: Tree[T], tree2: Tree[T], cost: Cost[T]) -> int:
    traversal1 = tree1.postorder()
    traversal2 = tree2.postorder()

    if not traversal1:
        return sum(cost.delete(node.value) for node in traversal2)
    if not traversal2:
        return sum(cost.insert(node.value) for node in traversal1)

    keyroots1 = traversal1.keyroots
    keyroots2 = traversal2.keyroots

    tree_dist: list[list[int]] = [[0] * len(traversal2) for _ in range(len(traversal1))]

    def _distance(root1: Traversed[T], root2: Traversed[T]) -> None:
        nodes1 = traversal1.get_subtree(root1)
        nodes2 = traversal2.get_subtree(root2)

        forest_dist = [[0] * (len(nodes2) + 1) for _ in range(len(nodes1) + 1)]

        for i, node1 in enumerate(nodes1, 1):
            forest_dist[i][0] = forest_dist[i - 1][0] + cost.delete(node1.value)
        for j, node2 in enumerate(nodes2, 1):
            forest_dist[0][j] = forest_dist[0][j - 1] + cost.insert(node2.value)

        for i, node1 in enumerate(nodes1, 1):
            for j, node2 in enumerate(nodes2, 1):
                cost_deletion = forest_dist[i - 1][j] + cost.delete(node1.value)
                cost_insertion = forest_dist[i][j - 1] + cost.insert(node2.value)

                preceding_siblings1 = (
                    node1.leftmost_leaf_index - root1.leftmost_leaf_index
                )
                preceding_siblings2 = (
                    node2.leftmost_leaf_index - root2.leftmost_leaf_index
                )

                if preceding_siblings1 == 0 and preceding_siblings2 == 0:
                    cost_relabel = forest_dist[i - 1][j - 1] + cost.relabel(
                        node1.value, node2.value
                    )
                    tree_dist[node1.index][node2.index] = forest_dist[i][j] = min(
                        cost_deletion, cost_insertion, cost_relabel
                    )
                else:
                    cost_relabel = (
                        forest_dist[preceding_siblings1][preceding_siblings2]
                        + tree_dist[node1.index][node2.index]
                    )
                    forest_dist[i][j] = min(cost_deletion, cost_insertion, cost_relabel)

    for keyroot1 in keyroots1:
        for keyroot2 in keyroots2:
            _distance(keyroot1, keyroot2)

    return tree_dist[-1][-1]
