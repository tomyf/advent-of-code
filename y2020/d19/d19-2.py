import re
from copy import copy
from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str

RE_SIMPLE_RULE = re.compile(r"^(\d+): \"(.)\"$")


class Rule:
    def __init__(self, id, rules):
        self.id = id
        self.value = None
        self.branches: List[List[Rule]] = [[]]
        self.rules: dict = rules
        self.rules[id] = self

    def add_rule(self, id):
        if id != self.id:
            self.branches[-1].append(self.rules.get(id))
        else:
            self.branches[-1].append(self)

    def set_value(self, value):
        self.value = value

    def add_branch(self):
        self.branches.append([])

    def match(self, message: str) -> List:
        if self.value:
            if message:
                return [(message[0] == self.value, message[1:])]
            else:
                return [(False, message)]
        frontier = [(message, copy(branch)) for branch in self.branches]
        state = frontier[0]
        possibilities = []
        while state:
            # print(frontier)
            # Extract first element of frontier
            msg_state, rules_state = state
            frontier = frontier[1:]
            if not rules_state:
                possibilities.append((True, msg_state))
            else:
                rule = rules_state[0]
                matches = [(is_valid, msg) for is_valid, msg in rule.match(msg_state) if is_valid]
                if matches:
                    for (is_valid, msg) in matches:
                        frontier.append((msg, rules_state[1:]))
            if frontier:
                state = frontier[0]
            else:
                state = None
        return possibilities


def check_evaluable_rule(rule, rules):
    match = RE_SIMPLE_RULE.match(rule)
    # Check if simple rule
    if match:
        id, value = match.groups()
        node = Rule(id, rules)
        node.set_value(value)
        return True
    # Else, try to list all rules within it and check if they are available
    rule_id = rule.split(":")[0]
    if all(rules.get(id) is not None for id in rule[2:].split(" ") if id.isdigit() and id != rule_id):
        # All sub-rules are already defined
        rule_node = Rule(rule_id, rules)
        for token in rule[2:].split(" "):
            if token.isdigit():
                rule_node.add_rule(token)
            elif token == "|":
                rule_node.add_branch()
        return True

    # No match: abort
    return False


def process_file(lines: List[str]):
    rules_file: List[str]
    messages: List[str]
    index_of_sep = lines.index("")
    rules_file, messages = lines[0:index_of_sep], lines[index_of_sep+1:]
    rules = {}
    i = len(rules_file)
    while len(rules_file) > 0 and i > 0:
        rules_to_delete = []
        for rule_text in rules_file:
            if check_evaluable_rule(rule_text, rules):
                rules_to_delete.append(rule_text)
        for rule in rules_to_delete:
            rules_file.remove(rule)
        # max iter watchdog
        i = i-1
    # Rules are parsed
    res = 0
    for message in messages:
        if any(res == (True, "") for res in rules.get("0").match(message)):
            res = res + 1
    return res


def test():
    test_data = read_file_list_str("test.txt")
    assert process_file(test_data) == 2
    print("✅ Valid test - Part 1")
    test_data2 = read_file_list_str("test2.txt")
    assert process_file(test_data2) == 12
    print("✅ Valid test - Part 2")


def real():
    real_data = read_file_list_str("data.txt")
    part1 = process_file(real_data)
    print(f"Part 1: {part1}")
    assert part1 == 104
    real_data_2 = read_file_list_str("data2.txt")
    part2 = process_file(real_data_2)
    print(f"Part 2: {part2}")
    assert part2 == 314


test()
real()
