from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str


def transform(subject, loop):
    # start with value = 1
    value = 1
    # for loop
    for _ in range(0, loop):
        #   value = value * subject
        #   value = value % 20201227
        value = (value * subject) % 20201227
    return value

    # card transform 7, loop_card => public_key_car
    # door transform 7, loop_door => public_key_door

    # card transform public_key_door, loop_door => encryption_key
    # door transform public_key_card, loop_door => encryption_key
    # Both values are the same

    # Transform 7, loop 8 = 5764801
    # Transform 7, loop 11 = 17807724
    # Transform 17807724, loop 8 = 14897079
    # Transform 5764801, loop 11 = 14897079


def find_loop(public_key):
    value = 1
    loop = 0
    while value != public_key:
        loop = loop + 1
        value = (value * 7) % 20201227
    return loop


def test():
    assert transform(7, 8) == 5764801
    assert transform(7, 11) == 17807724
    assert transform(17807724, 8) == 14897079
    assert transform(5764801, 11) == 14897079
    assert find_loop(5764801) == 8
    assert find_loop(17807724) == 11
    print("✅ Valid test")


def real():
    public_key_card = 9232416
    public_key_door = 14144084
    loop_card = find_loop(public_key_card)
    loop_door = find_loop(public_key_door)
    encryption_key_card = transform(public_key_door, loop_card)
    encryption_key_door = transform(public_key_card, loop_door)
    assert encryption_key_card == encryption_key_door
    encryption_key = encryption_key_door
    print(f"Part 1: {encryption_key}")
    assert encryption_key == 1478097


test()
real()
