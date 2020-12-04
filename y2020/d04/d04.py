import re
from typing import Dict, List
from y2020.libs.read_file import read_file_list_str

RE_HEIGHT = re.compile(r"^(\d+)(in|cm)$")
RE_HAIR_COLOR = re.compile(r"^#[0-9a-f]{6}$")


def prepare_passports(file: List[str]) -> List[Dict]:
    passports = []
    current = {}
    for line in file:
        # Handle new passport
        if not line:
            passports.append(current)
            current = {}
        else:
            # Handle attributes
            for attribute in line.split(" "):
                key, value = attribute.split(":")
                current[key] = value
    # Last passport has no empty line after it
    passports.append(current)
    return passports


def is_valid_passport(passport: dict) -> bool:
    mandatory_attributes = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    return all(mandatory_attribute in passport for mandatory_attribute in mandatory_attributes)


def is_valid_passport_part2(passport: dict) -> bool:
    if not is_valid_passport(passport):
        return False
    # Check each attribute
    if not(1920 <= int(passport["byr"]) <= 2002):
        return False
    if not(2010 <= int(passport["iyr"]) <= 2020):
        return False
    if not(2020 <= int(passport["eyr"]) <= 2030):
        return False
    try:
        height, unit = RE_HEIGHT.match(passport["hgt"]).groups()
        if unit == "in" and not (59 <= int(height) <= 76):
            return False
        if unit == "cm" and not (150 <= int(height) <= 193):
            return False
    except:
        # Regex match was None
        return False
    if RE_HAIR_COLOR.match(passport["hcl"]) is None:
        return False
    if passport["ecl"] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        return False
    pid: str = passport["pid"]
    if len(pid) != 9 or not pid.isdigit:
        return False
    # All are valid : return True
    return True


def count_valid_passports(file: List[str]) -> int:
    passports = prepare_passports(file)
    return sum(1 for passport in passports if is_valid_passport(passport))


def count_valid_passports_part2(file: List[str]) -> int:
    passports = prepare_passports(file)
    return sum(1 for passport in passports if is_valid_passport_part2(passport))


def test():
    test_data = read_file_list_str("test.txt")
    assert count_valid_passports(test_data) == 2
    test_invalid_data = read_file_list_str("test_invalid.txt")
    assert count_valid_passports_part2(test_invalid_data) == 0
    test_valid_data = read_file_list_str("test_valid.txt")
    assert count_valid_passports_part2(test_valid_data) == 4
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    print(f"Valid passports part 1: {count_valid_passports(real_data)}")
    print(f"Valid passports part 2: {count_valid_passports_part2(real_data)}")


test()
real()
