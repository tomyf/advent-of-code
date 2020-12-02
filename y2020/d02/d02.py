import re

from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str

RE_POLICY = re.compile(r"^(\d+)-(\d+) (.): (.+)$")

##########
# PART 1 #
##########


def is_valid_password(min: int, max: int, letter: str, password: str) -> bool:
    return min <= password.count(letter) <= max


def count_valid_passwords(password_entries: List[str]) -> int:
    counter = 0
    for password_entry in password_entries:
        min, max, letter, password = RE_POLICY.match(password_entry).groups()
        counter = counter + 1 if is_valid_password(int(min), int(max), letter, password) else counter
    return counter


##########
# PART 2 #
##########
def is_valid_password_part2(pos_1: int, pos_2: int, letter: str, password: str) -> bool:
    return (password[pos_1-1] == letter) != (password[pos_2-1] == letter)


def count_valid_passwords_part2(password_entries: List[str]) -> int:
    counter = 0
    for password_entry in password_entries:
        pos_1, pos_2, letter, password = RE_POLICY.match(password_entry).groups()
        counter = counter + 1 if is_valid_password_part2(int(pos_1), int(pos_2), letter, password) else counter
    return counter


def test():
    test_data = read_file_list_str("test.txt")
    assert is_valid_password(1, 2, "a", "baabaa") is False
    assert count_valid_passwords(test_data) == 2
    assert count_valid_passwords_part2(test_data) == 1


def real():
    data = read_file_list_str("data.txt")
    print(f"Part 1: {count_valid_passwords(data)}")
    print(f"Part 2: {count_valid_passwords_part2(data)}")


test()
real()
