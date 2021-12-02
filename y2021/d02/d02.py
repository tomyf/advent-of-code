from typing import List, Tuple
from y2021.libs.read_file import read_file_list_str

# PART 1
# Tuple of position is (depth, horiz)
MAP_COMMANDS = {
    "forward": (0, 1),
    "up": (-1, 0),
    "down": (1, 0)
}


def process_command(command: str, position: Tuple[int, int]):
    direction, units_str = command.split(" ")
    units = int(units_str)
    depth, horiz = position
    increment_depth, increment_horiz = tuple(x * units for x in MAP_COMMANDS[direction])
    return (depth + increment_depth, horiz + increment_horiz)


def process_commands(commands: List[str], start: Tuple[int, int]):
    depth, horiz = start
    for command in commands:
        depth, horiz = process_command(command, (depth, horiz))
    return depth * horiz

# PART 2


def process_command_2(command: str, position: Tuple[int, int, int]):
    direction, units_str = command.split(" ")
    units = int(units_str)
    depth, horiz, aim = position
    if direction == "up":
        return (depth, horiz, aim - units)
    elif direction == "down":
        return (depth, horiz, aim + units)
    else:  # forward
        return (depth + units * aim, horiz + units, aim)


def process_commands_2(commands: List[str], start: Tuple[int, int, int]):
    depth, horiz, aim = start
    for command in commands:
        depth, horiz, aim = process_command_2(command, (depth, horiz, aim))
    return depth * horiz


def test():
    test_data = read_file_list_str("test.txt")
    assert process_commands(test_data, (0, 0)) == 150
    assert process_commands_2(test_data, (0, 0, 0)) == 900
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    print(f"Part 1: {process_commands(real_data, (0, 0))}")
    print(f"Part 2: {process_commands_2(real_data, (0, 0, 0))}")


test()
real()
