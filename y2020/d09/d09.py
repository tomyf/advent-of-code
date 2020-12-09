from typing import List, Tuple
from y2020.libs.read_file import read_file_list_int


def get_first_invalid_number(data: List[int]) -> int:
    preamble_length, numbers = data[0], data[1:]
    return process(
        preamble_length=preamble_length,
        preamble=[],
        index=0,
        numbers=numbers
    )


def process(preamble_length: int, preamble: List[int], index: int, numbers: List[int]):
    # Abort when end is reached
    if index >= len(numbers):
        return None
    # Add current number to preamble and remove the first one
    if len(preamble) == preamble_length:
        preamble.pop(0)
    preamble.append(numbers[index])

    # If preamble is full, check next number
    if len(preamble) == preamble_length:
        # If invalid, return current number
        next_number = numbers[index + 1]
        if not is_valid_number_with_preamble(next_number, preamble):
            return next_number

    return process(
        preamble_length=preamble_length,
        preamble=preamble,
        index=index + 1,
        numbers=numbers
    )


def is_valid_number_with_preamble(n: int, preamble: List[int]) -> bool:
    for x in preamble:
        if any(True for y in preamble if x != y and x + y == n):
            return True
    return False


def find_contiguous_sum_elements(target: int, data: List[int]):
    numbers = data[1:]
    for (index, current_elt) in enumerate(numbers):
        if current_elt == target:
            continue
        elts = []
        sum = 0
        offset = 0
        while sum < target:
            elt = numbers[index + offset]
            sum = sum + elt
            elts.append(elt)
            offset = offset + 1
        if sum == target:
            return elts


def find_encryption_weakness(test_data):
    invalid_number = get_first_invalid_number(test_data)
    elements = find_contiguous_sum_elements(invalid_number, test_data)
    return min(elements) + max(elements)


def test():
    test_data = read_file_list_int("test.txt")
    assert get_first_invalid_number(test_data) == 127
    assert find_encryption_weakness(test_data) == 62
    print("✅ Valid test")


def real():
    real_data = read_file_list_int("data.txt")
    part1 = get_first_invalid_number(real_data)
    print(f"Part 1: {part1}")
    assert part1 == 1930745883
    part2 = find_encryption_weakness(real_data)
    print(f"Part 2: {part2}")
    assert part2 == 268878261


test()
real()
