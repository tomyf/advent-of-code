from typing import List, Tuple
from y2020.libs.read_file import read_file_list_int


def find_two_entries(numbers: List[int], match: int) -> Tuple[int, int]:
    # Find the 2 numbers whose sum equals "match"
    for a in numbers:
        for b in numbers:
            if a + b == match:
                return (a, b)
    return None


def find_three_entries(numbers: List[int], match: int) -> Tuple[int, int, int]:
    # Find the 2 numbers whose sum equals "match"
    for a in numbers:
        for b in numbers:
            for c in numbers:
                if a + b + c == match:
                    return (a, b, c)
    return None


def test():
    # Test list
    test_list = read_file_list_int("test.txt")
    assert find_two_entries(test_list, 2020) == (1721, 299)
    assert find_three_entries(test_list, 2020) == (979, 366, 675)


def real():
    # Real case
    real_list = read_file_list_int("data.txt")
    print("2 entries (part 1):")
    (value_a, value_b) = find_two_entries(real_list, 2020)
    print(f"{value_a} * {value_b} = {value_a * value_b}")
    print()
    print("3 entries (part 2):")
    (value_a, value_b, value_c) = find_three_entries(real_list, 2020)
    print(f"{value_a} * {value_b} * {value_c} = {value_a * value_b * value_c}")


test()
real()
