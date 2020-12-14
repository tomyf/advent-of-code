import re
from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str

RE_NUM = re.compile(r"^mem\[(\d+)\] = (\d+)$")


def compute_value(value: int, mask: str) -> int:
    bin_value = bin(value).replace("0b", "").rjust(len(mask), "0")
    res = ""
    for (index, m) in enumerate(mask):
        if m == "X":
            res = res + bin_value[index]
        if m == "0":
            res = res + "0"
        if m == "1":
            res = res + "1"
    return int(res, 2)


def change_memory(memory: dict, address: int, value: int, mask: str) -> None:
    bin_address = bin(address).replace("0b", "").rjust(len(mask), "0")
    res = ""
    tmp_mask = ""
    for (index, m) in enumerate(mask):
        if m == "0":
            res = res + bin_address[index]
        if m == "1":
            res = res + m
        if m == "2":
            res = res + "0"
        if m == "X":
            # fork and stop current loop here
            rest_mask = mask[index+1:]
            change_memory(memory, address, value, tmp_mask + "2" + rest_mask)
            change_memory(memory, address, value, tmp_mask + "1" + rest_mask)
            return
        # Acc with the processed mask
        tmp_mask = tmp_mask + m
    # End of loop reached : write in memory
    memory[int(res, 2)] = value


def process_program(instructions: List[str]) -> int:
    memory = {}
    mask = None
    for instruction in instructions:
        if instruction.startswith("mask = "):
            _, mask = instruction.split(" = ")
        else:
            address, value = RE_NUM.match(instruction).groups()
            memory[int(address)] = compute_value(int(value), mask)
    # sum memory
    return sum(value for value in memory.values())


def process_program_2(instructions: List[str]) -> int:
    memory = {}
    mask = None
    for instruction in instructions:
        if instruction.startswith("mask = "):
            _, mask = instruction.split(" = ")
        else:
            address, value = RE_NUM.match(instruction).groups()
            change_memory(memory, int(address), int(value), mask)
    # sum memory
    return sum(value for value in memory.values())


def test():
    test_data = read_file_list_str("test.txt")
    assert process_program(test_data) == 165
    test2 = read_file_list_str("test2.txt")
    assert process_program_2(test2) == 208
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    part1 = process_program(real_data)
    print(f"Part 1: {part1}")
    assert part1 == 14722016054794
    part2 = process_program_2(real_data)
    print(f"Part 2: {part2}")
    assert part2 == 3618217244644


test()
real()
