# Tree Edit Distance

This is a Python package for computing the tree edit distance between two trees by Zhang and Shasha (1989).

## Basic Usage

The following two trees are used as an example:

```mermaid
graph TD
    subgraph Tree2
        t2f(("f"))
        t2c(("c"))
        t2e(("e"))
        t2d(("d"))
        t2a(("a"))
        t2b(("b"))

        t2f --- t2c
        t2f --- t2e
        t2c --- t2d
        t2d --- t2a
        t2d --- t2b
    end

    subgraph Tree1
        t1f(("f"))
        t1d(("d"))
        t1e(("e"))
        t1a(("a"))
        t1c(("c"))
        t1b(("b"))

        t1f --- t1d
        t1f --- t1e
        t1d --- t1a
        t1d --- t1c
        t1c --- t1b
    end
```

You can compute the tree edit distance between two trees using the `distance` function from the `tree_edit_distance.core` module. Below is an example of how to use it:


```py
from tree_edit_distance.core import Tree, Cost, distance


t1: Tree[str] = Tree("f", [Tree("d", [Tree("a"), Tree("c", [Tree("b")])]), Tree("e")])
t2: Tree[str] = Tree("f", [Tree("c", [Tree("d", [Tree("a"), Tree("b")])]), Tree("e")])

cost = Cost[str].default()

assert distance(t1, t2, cost) == 2
```
