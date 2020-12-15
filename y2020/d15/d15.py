from typing import List, Tuple


def get_nth_number(numbers: List[int], nth: int) -> int:
    indexes = {}
    for (index, value) in enumerate(numbers):
        indexes[value] = indexes.get(value) or []
        indexes[value].insert(0, index)
    for _ in range(len(numbers), nth):
        if _ % 1e5 == 0:
            print(_, len(indexes))
        l = len(numbers)
        last_number = numbers[l - 1]
        nb = None
        try:
            # throws if number was not already present: compute its age
            nb = l - indexes[last_number][-2] - 1  # numbers[::-1].index(last_number, 1)
            numbers.append(nb)
        except:
            nb = 0
            numbers.append(nb)
        # insert to fast age records
        indexes[nb] = indexes.get(nb) or []
        indexes[nb].append(l)
    # print(numbers, indexes)
    return numbers[-1]


def test():
    # Simple cases
    assert get_nth_number([0, 3, 6], 4) == 0
    assert get_nth_number([0, 3, 6], 5) == 3
    assert get_nth_number([0, 3, 6], 6) == 3
    assert get_nth_number([0, 3, 6], 7) == 1
    assert get_nth_number([0, 3, 6], 8) == 0
    assert get_nth_number([0, 3, 6], 9) == 4
    assert get_nth_number([0, 3, 6], 10) == 0
    # All cases part 1
    assert get_nth_number([1, 3, 2], 2020) == 1
    assert get_nth_number([2, 1, 3], 2020) == 10
    assert get_nth_number([1, 2, 3], 2020) == 27
    assert get_nth_number([2, 3, 1], 2020) == 78
    assert get_nth_number([3, 2, 1], 2020) == 438
    assert get_nth_number([3, 1, 2], 2020) == 1836
    # All cases part 2
    # print("PART 2 TESTS")
    # Commented out tests in order to speed up....
    # assert get_nth_number([0, 3, 6], 30000000) == 175594
    # assert get_nth_number([1, 3, 2], 30000000) == 2578
    # assert get_nth_number([2, 1, 3], 30000000) == 3544142
    # assert get_nth_number([1, 2, 3], 30000000) == 261214
    # assert get_nth_number([2, 3, 1], 30000000) == 6895259
    # assert get_nth_number([3, 2, 1], 30000000) == 18
    # assert get_nth_number([3, 1, 2], 30000000) == 362
    print("✅ Valid test")


def real():
    part1 = get_nth_number([9, 6, 0, 10, 18, 2, 1], 2020)
    print(f"Part 1: {part1}")
    assert part1 == 1238
    part2 = get_nth_number([9, 6, 0, 10, 18, 2, 1], 30000000)
    print(f"Part 2: {part2}")
    assert part2 == 3745954


test()
real()
