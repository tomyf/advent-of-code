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
        elif self.right is None:
            self.right = value
        else:
            current = self
            while current.right is not None:
                current = current.right
            current.right = value

    def set_op(self, c: str):
        if self.op is None:
            self.op = c
            return self
        else:
            if c == "*":
                current = self
                # while current.op == "+" and current.parent is not None:
                #     current = current.parent
                # Replace left with node with (left, op, right, self) for "*"
                node = Node()
                node.left = current.left
                node.right = current.right
                node.op = current.op
                node.parent = current
                current.left = node
                current.op = c
                current.right = None
                return current
            else:
                # Replace right with node with (right, c, None, self) for "+" and return current node
                current = self
                while isinstance(current.right, Node) and current.right.op == "+":
                    current = current.right
                node = Node()
                node.left = current.right
                node.op = c
                node.right = None
                node.parent = current
                current.right = node
                return self

    def add_nested(self):
        node = Node()
        node.parent = self
        if self.left is None:
            self.left = node
        elif self.right is None:
            self.right = node
        else:
            current = self
            while current.right is not None:
                current = current.right
            current.right = node
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


def evaluate_line(line, debug=False):
    root = Node()
    current = root
    for c in line:
        if c.isspace():
            continue
        if debug:
            print(root)
        if c.isdigit():
            current.set_value(c)
        if c in ["*", "+"]:
            current = current.set_op(c)
        if c == "(":
            current = current.add_nested()
        if c == ")":
            current = current.parent
    if debug:
        print(root)
    return root.compute()


def evaluate_lines(lines):
    return sum(evaluate_line(line) for line in lines)


def test():
    assert evaluate_line("1+3") == 4
    assert evaluate_line("1 + 2 * 3 + 4 * 5 + 6") == 231
    assert evaluate_line("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert evaluate_line("2 * 3 + (4 * 5)") == 46
    assert evaluate_line("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
    assert evaluate_line("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
    assert evaluate_line("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    part2 = evaluate_lines(real_data)
    print(f"Part 2: {part2}")


test()
real()
