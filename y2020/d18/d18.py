from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str


class Node:
    def __init__(self) -> None:
        self.left = None
        self.op = None
        self.right = None
        self.parent = None

    def __str__(self) -> str:
        return f"({self.left} {self.op} {self.right})"

    def set_value(self, c: str):
        value = int(c)
        if self.left is None:
            self.left = value
        else:
            self.right = value

    def set_op(self, c: str):
        if self.op is None:
            self.op = c
        else:
            # Replace left with node with (left, op, right, self)
            node = Node()
            node.left = self.left
            node.right = self.right
            node.op = self.op
            node.parent = self
            self.left = node
            self.op = c
            self.right = None

    def add_nested(self):
        node = Node()
        node.parent = self
        if self.left is None:
            self.left = node
        else:
            self.right = node
        return node

    def get_left(self):
        if isinstance(self.left, Node):
            return self.left.compute()
        else:
            return self.left

    def get_right(self):
        if isinstance(self.right, Node):
            return self.right.compute()
        else:
            return self.right

    def compute(self):
        left = self.get_left()
        right = self.get_right()
        if self.op == "+":
            return left + right
        elif self.op == "*":
            return left * right


def evaluate_line(line):
    root = Node()
    current = root
    for c in line:
        if c.isdigit():
            current.set_value(c)
        if c in ["*", "+"]:
            current.set_op(c)
        if c == "(":
            current = current.add_nested()
        if c == ")":
            current = current.parent
    return root.compute()


def evaluate_lines(lines):
    return sum(evaluate_line(line) for line in lines)


def test():
    test_data = read_file_list_str("test.txt")
    assert evaluate_line("1+3") == 4
    assert evaluate_line("1+2*3+4*5+6") == 71
    assert evaluate_line("2*3+(4*5)") == 26
    assert evaluate_line("(4*5)+(2*3)") == 26
    assert evaluate_line("(4*5)+2*3") == 66
    assert evaluate_line("((4+1)+2)+3") == 10
    assert evaluate_lines(test_data) == 26335
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    part1 = evaluate_lines(real_data)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


test()
real()
