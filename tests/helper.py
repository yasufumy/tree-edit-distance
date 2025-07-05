from tree_edit_distance.core import Tree


def create_tree(text: str) -> Tree[str]:
    tree_stack: list[tuple[Tree[str], int]] = []
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
            tree_stack.append((Tree(label, children), len(stack)))
        else:
            stack[-1] += letter
    return tree_stack[0][0]
