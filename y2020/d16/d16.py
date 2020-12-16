import re
from typing import List, Tuple
from y2020.libs.read_file import read_file

RE_RULE = re.compile(r"^(.+?): (\d+)-(\d+) or (\d+)-(\d+)$")


def prepare_data(file: str) -> dict:
    input_rules, input_your_ticket, input_nearby_tickets = file.split("\n\n")
    rules_txt = input_rules.split("\n")
    rules = {}
    all_rules = []
    for rule_txt in rules_txt:
        id, min1_s, max1_s, min2_s, max2_s = RE_RULE.match(rule_txt).groups()
        min1 = int(min1_s)
        max1 = int(max1_s)
        min2 = int(min2_s)
        max2 = int(max2_s)
        ranges = list(range(min1, max1 + 1)) + list(range(min2, max2 + 1))
        rules[id] = ranges
        all_rules = all_rules + ranges
    ticket = [int(field) for field in input_your_ticket.split("\n")[1].split(",")]
    nearby_tickets = [
        [int(field) for field in input_nearby_ticket.split(",")]
        for input_nearby_ticket in input_nearby_tickets.split("\n")[1:]
    ]
    res = {
        "rules": rules,
        "all_rules": all_rules,
        "ticket": ticket,
        "nearby_tickets": nearby_tickets
    }
    return res


def sum_invalid_fields(file: str) -> int:
    data = prepare_data(file)
    return sum(
        sum(id for id in nearby_ticket if id not in data["all_rules"])
        for nearby_ticket in data["nearby_tickets"]
    )


def build_ticket(file: str) -> dict:
    data = prepare_data(file)
    valid_tickets = [data["ticket"]] + [
        nearby_ticket for nearby_ticket in data["nearby_tickets"]
        if sum(id for id in nearby_ticket if id not in data["all_rules"]) == 0
    ]

    # Prepare list of possibilities
    possible_fields: List[List[str]] = []
    for _ in data["ticket"]:
        possibilities = []
        for rule in data["rules"]:
            possibilities.append(rule)
        possible_fields.append(possibilities)

    # Strike out possible fields
    for valid_ticket in valid_tickets:
        for (index, value) in enumerate(valid_ticket):
            for (id, ranges) in data["rules"].items():
                if not value in ranges:
                    possible_fields[index].remove(id)

    # Loop on possible fields until length = 1 in every row
    while any(len(possibilities) > 1 for possibilities in possible_fields):
        for possibilities in possible_fields:
            if len(possibilities) == 1:
                # remove from all
                unique_possibility = possibilities[0]
                for possibilities_2ndloop in possible_fields:
                    if len(possibilities_2ndloop) > 1 and unique_possibility in possibilities_2ndloop:
                        possibilities_2ndloop.remove(unique_possibility)

    ticket = {
        name: data["ticket"][index]
        for (index, [name]) in enumerate(possible_fields)
    }
    return ticket


def test():
    test_data = read_file("test.txt")
    assert sum_invalid_fields(test_data) == 71
    test_data2 = read_file("test2.txt")
    assert build_ticket(test_data2) == {"row": 11, "class": 12, "seat": 13}
    print("✅ Valid test")


def real():
    real_data = read_file("data.txt")
    part1 = sum_invalid_fields(real_data)
    print(f"Part 1: {part1}")
    assert part1 == 26941
    # Part 2
    ticket = build_ticket(real_data)
    part2 = 1
    for (key, value) in ticket.items():
        if key.startswith("departure"):
            part2 = part2 * value
    print(f"Part 2: {part2}")


test()
real()
