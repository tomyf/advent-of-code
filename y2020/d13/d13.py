from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str


def find_earliest_bus(data: List[str]) -> int:
    earliest_possible_timestamp, bus_ids = int(data[0]), [int(bus_id) for bus_id in data[1].split(",") if bus_id != "x"]
    for i in range(0, max(bus_ids)):
        for bus_id in bus_ids:
            if (earliest_possible_timestamp + i) % bus_id == 0:
                return i * bus_id


def is_matching(timestamp: int, bus_ids: List) -> bool:
    # for (offset, value) in enumerate(bus_ids):
    #     if value != "x":
    #         if (timestamp + offset) % value != 0:
    #             return False
    # return True
    return all((timestamp + offset) % value == 0 for (offset, value) in enumerate(bus_ids) if value != "x")


def find_earliest_timestamp(data: List[str]) -> int:
    bus_details = [(offset, int(bus_id)) for (offset, bus_id) in enumerate(data[1].split(",")) if bus_id != "x"]
    # Increment at least with the first bus id (eg: 7)
    timestamp = increment = bus_details[0][1]
    # For all buses except the first one
    for (offset, bus_id) in bus_details[1:]:
        # While the current bus does not match the current rule with the timestamp (eg: (7x + 1 mod 13 != 0))
        while (timestamp + offset) % bus_id != 0:
            # Increment with the previous valid increment (7)
            timestamp = timestamp + increment
        # Now the current bus is valid, so multiply the increment with its id so it is still valid for the current bus and all the previous one
        increment = increment * bus_id
    return timestamp


def test():
    test_data = read_file_list_str("test.txt")
    assert find_earliest_bus(test_data) == 295
    assert find_earliest_timestamp(test_data) == 1068781
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    part1 = find_earliest_bus(real_data)
    print(f"Part 1: {part1}")
    assert part1 == 138
    part2 = find_earliest_timestamp(real_data)
    print(f"Part 2: {part2}")
    assert part2 == 226845233210288


test()
real()
