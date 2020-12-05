from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str


def decode_bsp(bsp: str) -> Tuple[int, int, int]:
    row_bsp, column_bsp = bsp[0:7], bsp[7:]
    row_binary = row_bsp.replace("F", "0").replace("B", "1")
    column_binary = column_bsp.replace("R", "1").replace("L", "0")
    row = int(row_binary, 2)
    column = int(column_binary, 2)
    id = row * 8 + column
    return row, column, id


def find_missing_seat(seats_ids: List[int]):
    for i in range(0, 128 * 8):
        if i not in seats_ids and (i-1) in seats_ids and (i+1) in seats_ids:
            return i


def test():
    assert decode_bsp("FBFBBFFRLR") == (44, 5, 357)
    assert decode_bsp("BFFFBBFRRR") == (70, 7, 567)
    assert decode_bsp("FFFBBBFRRR") == (14, 7, 119)
    assert decode_bsp("BBFFBBFRLL") == (102, 4, 820)
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    seats_ids = [decode_bsp(bsp)[2] for bsp in real_data]
    max_id = max(seats_ids)
    print(f"Part 1: {max_id}")
    assert max_id == 822
    # -------
    missing_seat = find_missing_seat(seats_ids)
    print(f"Part 2: {missing_seat}")
    assert missing_seat == 705


test()
real()
