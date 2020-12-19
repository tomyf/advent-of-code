import re
from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str

RE_SIMPLE_RULE = re.compile(r"^(\d+): \"(.)\"$")


def add_rule(rule, rules):
    id, text = rule.split(":")
    rule_to_add = []
    current_branch = []
    for token in text.split(" "):
        token: str
        if token.isdigit():
            current_branch.append(token)
        elif token == "|":
            rule_to_add.append(current_branch)
            current_branch = []
    # out of loop: append current branch to rule
    rule_to_add.append(current_branch)
    rules[id] = rule_to_add


def check_evaluable_rule(rule, rules):
    match = RE_SIMPLE_RULE.match(rule)
    # Check if simple rule
    if match:
        id, value = match.groups()
        rules[id] = value
        return True
    # Else, try to list all rules within it and check if they are available
    if all(rules.get(id) is not None for id in rule[2:].split(" ") if id.isdigit()):
        # All sub-rules are already defined
        add_rule(rule, rules)
        return True

    # No match: abort
    return False


def generate_regex(id, rules):
    rule = rules[id]
    if isinstance(rule, str):
        return rule
    # rule is a list
    branches_list = []
    for branch in rule:
        branches_list.append("".join(generate_regex(id, rules) for id in branch))
    expr = "|".join(branches_list)
    res = f"({expr})" if len(branches_list) > 1 else expr
    rules[id] = res
    return res


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
    # Prepare regex from rule 0 and add "strict" match
    reg_str = generate_regex("0", rules)
    reg_str = f"^{reg_str}$"
    print(reg_str)
    reg = re.compile(reg_str)
    return sum(1 for message in messages if reg.match(message))


def test():
    test_data = read_file_list_str("test.txt")
    assert process_file(test_data) == 2
    print("✅ Valid test - Part 1")


def real():
    real_data = read_file_list_str("data.txt")
    part1 = process_file(real_data)
    print(f"Part 1: {part1}")
    assert part1 == 104


test()
real()
