import re
from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str

RE_INSTRUCTION = re.compile(r"^([NSEWLRF])(\d+)$")


def handle_instructions(instructions: List[str]) -> Tuple[int, int]:
    # Position is (EAST, NORTH)
    ship_position = (0, 0)
    waypoint_offset_from_ship = (10, 1)
    for instruction in instructions:
        operand, value = RE_INSTRUCTION.match(instruction).groups()
        ship_position, waypoint_offset_from_ship = process_instruction(operand, int(value), ship_position, waypoint_offset_from_ship)
    return abs(ship_position[0]) + abs(ship_position[1])


def process_instruction(operand: str, value: int, position: Tuple[int, int], waypoint_offset_from_ship: Tuple[int, int]) -> Tuple[int, Tuple[int, int], Tuple[int, int]]:
    east, north = position
    east_wp, north_wp = waypoint_offset_from_ship
    # Operand F : Forward
    if operand == "F":
        return (east + value * east_wp, north + value * north_wp), (east_wp, north_wp)
    # Operand N : North
    if operand == "N":
        return (east, north), (east_wp, north_wp + value)
    # Operand S : South
    if operand == "S":
        return (east, north), (east_wp, north_wp - value)
    # Operand E : East
    if operand == "E":
        return (east, north), (east_wp + value, north_wp)
    # Operand W : West
    if operand == "W":
        return (east, north), (east_wp - value, north_wp)
    # Operand L : turn Left
    if operand == "L":
        return (east, north), rotate_left((east_wp, north_wp), value)
    # Operand R : turn Right
    if operand == "R":
        return (east, north), rotate_left((east_wp, north_wp), -value)
    # Error case
    raise Exception("Unknown operand: ", operand)


def rotate_left(position: Tuple[int, int], angle: int) -> Tuple[int, int]:
    times = (angle // 90) % 4
    x, y = position
    for _ in range(0, times):
        x, y = -y, x
    return x, y


def test():
    test_data = read_file_list_str("test.txt")
    assert handle_instructions(test_data) == 286
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    part2 = handle_instructions(real_data)
    print(f"Part 2: {part2}")
    assert part2 == 45763


test()
real()
