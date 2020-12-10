from functools import lru_cache
from typing import List, Tuple
from y2020.libs.read_file import read_file_list_int


def prepare_joltages(input_list: List[int]) -> List[int]:
    joltages = input_list.copy()
    # Add source (0)
    joltages.append(0)
    joltages.sort()
    # Add device's adapter (max + 3)
    joltages.append(joltages[-1] + 3)
    return joltages


def get_joltage_difference_distribution(input_list: List[int]) -> List[int]:
    joltages = prepare_joltages(input_list)
    differences = [
        joltages[i+1] - joltages[i]
        for i in range(0, len(joltages) - 1)
    ]
    return [
        differences.count(diff)
        for diff in range(1, 4)
    ]


def count_possible_arrangements(input_list: List[int]) -> int:
    joltages = prepare_joltages(input_list)
    # build list of possibilities as list of tuples
    possibilities = [()] * (max(joltages) + 1)
    for i in joltages:
        # For each adapter, list the reachable adapters as a tuple
        possibilities[i] = tuple(x for x in joltages if 1 <= x - i <= 3)
    # For LRU cache usage, convert everything to tuples
    t = tuple(possibilities)
    return count_rec(0, t)


@lru_cache(250)
def count_rec(current_joltage, possibilities):
    # LRU cache with size 250 is enough for the tests
    if not possibilities[current_joltage]:
        # End of route
        return 1
    return sum(count_rec(x, possibilities) for x in possibilities[current_joltage])


def test():
    test1 = read_file_list_int("test_1.txt")
    assert get_joltage_difference_distribution(test1) == [7, 0, 5]
    assert count_possible_arrangements(test1) == 8
    test2 = read_file_list_int("test_2.txt")
    assert get_joltage_difference_distribution(test2) == [22, 0, 10]
    assert count_possible_arrangements(test2) == 19208
    assert get_joltage_difference_distribution([1, 2, 3, 6, 7, 8]) == [5, 0, 2]
    assert count_possible_arrangements([1, 2, 3, 6, 7, 8]) == 8
    print(get_joltage_difference_distribution([1, 2, 3, 4, 5]))
    assert get_joltage_difference_distribution([1, 2, 3, 4, 5]) == [5, 0, 1]
    print("✅ Valid test")


def real():
    real_data = read_file_list_int("data.txt")
    part1 = get_joltage_difference_distribution(real_data)
    print(f"Part 1: {part1} => {part1[0] * part1[2]}")
    assert part1[0] * part1[2] == 2414
    part2 = count_possible_arrangements(real_data)
    print(f"Part 2: {part2}")
    assert part2 == 21156911906816


test()
real()
