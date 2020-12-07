import re
from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str

RE_RULE = re.compile(r"^(\d+) (.+)$")


class Node:
    def __init__(self, color: str, children: List):
        self.color = color
        self.children: List[Tuple[int, Node]] = children


class Tree:
    def __init__(self):
        self.nodes = {}

    def get_node(self, color: str) -> Node:
        return self.nodes.get(color, None)

    def save_node(self, node: Node):
        self.nodes[node.color] = node

    def add_node(self, color: str, rules: List[Tuple[int, str]]):
        children = []
        for (rule_quantity, rule_color) in rules:
            rule_node = self.get_node(rule_color)
            if not rule_node:
                rule_node = Node(rule_color, None)
                self.save_node(rule_node)
            children.append((int(rule_quantity), rule_node))
        # Get or Create the new node with its children
        node = self.get_node(color)
        if node:
            node.children = children
        else:
            node = Node(color, children)
            self.save_node(node)


def build_tree(data: List[str]) -> Tree:
    tree = Tree()
    for line in data:
        color, color_rules = line.split(" bags contain ")
        rules = []
        # Remove last dot and remove " bags" and " bag"
        color_rules = color_rules[:-1].replace(" bags", "").replace(" bag", "")
        if color_rules != "no other":
            rules = [RE_RULE.match(rule).groups() for rule in color_rules.split(", ")]
        # (color, rules) is something like :
        # - vibrant plum // [('5', 'faded blue'), ('6', 'dotted black'), ('12', 'aeazeaze')]
        # - faded blue // None
        tree.add_node(color, rules)
    return tree


def node_allowed_color(node: Node, tree: Tree, color: str):
    if node.color == color:
        return True
    if node.children is None:
        return False
    return any(True for (count, child) in node.children if node_allowed_color(child, tree, color))


def count_root_bags_containing_color(tree: Tree, color: str):
    # Subtract 1 since a bag cannot contain itself
    return sum(1 for node in tree.nodes.values() if node_allowed_color(node, tree, color)) - 1


def count_bags_from_color(tree: Tree, color: str):
    node = tree.get_node(color)
    if not node.children:
        return 0
    # Else, sum the number of bags of each child times its number for the current color
    return sum(
        count + count * count_bags_from_color(tree, child.color)
        for (count, child) in node.children
    )


def test():
    test_data = read_file_list_str("test.txt")
    tree = build_tree(test_data)
    result = count_root_bags_containing_color(tree, "shiny gold")
    print(f"Total for shiny gold: {result}")
    assert result == 4
    part2 = count_bags_from_color(tree, "shiny gold")
    print(f"Test 2: total count 1: {part2}")
    test_data2 = read_file_list_str("test_part2.txt")
    tree_2 = build_tree(test_data2)
    part2_test2 = count_bags_from_color(tree_2, "shiny gold")
    print(f"Test 2: total count 2: {part2_test2}")
    assert part2 == 32
    assert part2_test2 == 126
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    tree = build_tree(real_data)
    result = count_root_bags_containing_color(tree, "shiny gold")
    print(f"Total for shiny gold: {result}")
    assert result == 126
    result2 = count_bags_from_color(tree, "shiny gold")
    print(f"Total for shiny gold: {result2}")
    assert result2 == 220149


test()
real()
