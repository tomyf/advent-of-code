import re
from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str

RE_INSTRUCTION = re.compile(r"^([NSEWLRF])(\d+)$")

EAST = 0
SOUTH = 1
WEST = 2
NORTH = 3


def handle_instructions(instructions: List[str]) -> Tuple[int, int]:
    position = (0, 0)
    direction = EAST
    for instruction in instructions:
        operand, value = RE_INSTRUCTION.match(instruction).groups()
        direction, position = process_instruction(operand, int(value), direction, position)
    return abs(position[0]) + abs(position[1])


def process_instruction(operand: str, value: int, direction: int, position: Tuple[int, int]) -> Tuple[int, Tuple[int, int]]:
    east, north = position
    # Operand F : Forward
    if operand == "F":
        if direction == EAST:
            return direction, (east + value, north)
        if direction == SOUTH:
            return direction, (east, north - value)
        if direction == WEST:
            return direction, (east - value, north)
        if direction == NORTH:
            return direction, (east, north + value)
    # Operand N : North
    if operand == "N":
        return direction, (east, north + value)
    # Operand S : South
    if operand == "S":
        return direction, (east, north - value)
    # Operand E : East
    if operand == "E":
        return direction, (east + value, north)
    # Operand W : West
    if operand == "W":
        return direction, (east - value, north)
    # Operand L : turn Left
    if operand == "L":
        return (direction - value//90) % 4, (east, north)
    # Operand R : turn Right
    if operand == "R":
        return (direction + value//90) % 4, (east, north)
    # Error case
    raise Exception("Unknown operand: ", operand)


def test():
    test_data = read_file_list_str("test.txt")
    assert handle_instructions(test_data) == 25
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    part1 = handle_instructions(real_data)
    print(f"Part 1: {part1}")
    assert part1 == 759


test()
real()
