from typing import List, Tuple
from y2021.libs.read_file import read_file_list_int


def compare_measures(l: List[int]):
    return len([1 for (index, el) in enumerate(l) if index > 0 and el > l[index-1]])


def sum_3_measures(l: List[int]):
    return [sum(l[i:i+3]) for i in range(0, len(l)-2)]


def test():
    test_data = read_file_list_int("test.txt")
    assert compare_measures(test_data) == 7
    assert compare_measures(sum_3_measures(test_data)) == 5
    print("✅ Valid test")


def real():
    real_data = read_file_list_int("data.txt")
    print(f"Part 1: {compare_measures(real_data)}")
    print(f"Part 2: {compare_measures(sum_3_measures(real_data))}")


test()
real()
