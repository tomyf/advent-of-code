from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str


def count_yeses(data: List[str]) -> int:
    groups = []
    current_group = ""
    for form in data:
        if not form:
            groups.append(current_group)
            current_group = ""
        else:
            current_group = current_group + form
    # Groups are formed
    unique_questions_per_group = [
        len(set([letter for letter in group]))
        for group in groups
    ]
    # Count total
    return sum(unique_questions_per_group)


def count_all_yeses(data: List[str]) -> int:
    groups = []
    current_group = []
    for form in data:
        if not form:
            groups.append(current_group)
            current_group = []
        else:
            current_group.append(form)
    # Groups are formed
    counter = 0
    for group in groups:
        for question_ord in range(ord("a"), ord("z") + 1):
            question = chr(question_ord)
            if all(question in form for form in group):
                counter = counter + 1
    return counter


def test():
    test_data = read_file_list_str("test.txt")
    assert count_yeses(test_data) == 11
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    part_1 = count_yeses(real_data)
    print(f"Part 1: {part_1}")
    assert part_1 == 6170
    part_2 = count_all_yeses(real_data)
    print(f"Part 2: {part_2}")


test()
real()
