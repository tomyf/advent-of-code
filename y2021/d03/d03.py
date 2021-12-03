from typing import List, Tuple
from y2021.libs.read_file import read_file_list_str


def find_gamma_epsilon(l: List[str], to_str: bool = False):
    gamma = "".join([
        "1"
        if [number[index] for number in l].count("1") >= [number[index] for number in l].count("0")
        else "0"
        for index in range(0, len(l[0]))
    ])
    epsilon = "".join([
        "0"
        if [number[index] for number in l].count("1") >= [number[index] for number in l].count("0")
        else "1"
        for index in range(0, len(l[0]))
    ])
    if to_str:
        return gamma, epsilon
    else:
        return int(gamma, 2), int(epsilon, 2)


def find_O2_CO2(l: List[str]):
    O2_l = l
    step_O2 = 0
    while len(O2_l) > 1:
        gamma_O2, _ = find_gamma_epsilon(O2_l, to_str=True)
        O2_l = [
            number for number in O2_l
            if number[step_O2] == gamma_O2[step_O2]
        ]
        step_O2 = step_O2 + 1
    O2_value = O2_l[0]

    CO2_l = l
    step_CO2 = 0
    while len(CO2_l) > 1:
        _, epsilon_CO2 = find_gamma_epsilon(CO2_l, to_str=True)
        CO2_l = [
            number for number in CO2_l
            if number[step_CO2] == epsilon_CO2[step_CO2]
        ]
        step_CO2 = step_CO2 + 1
    CO2_value = CO2_l[0]

    return int(O2_value, 2), int(CO2_value, 2)


def test():
    test_data = read_file_list_str("test.txt")
    gamma, epsilon = find_gamma_epsilon(test_data)
    assert gamma * epsilon == 198
    O2, CO2 = find_O2_CO2(test_data)
    assert O2 * CO2 == 230
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    gamma, epsilon = find_gamma_epsilon(real_data)
    print(f"Part 1: gamma={gamma}, epsilon={epsilon}, result={gamma * epsilon}")
    O2, CO2 = find_O2_CO2(real_data)
    print(f"Part 2: O2={O2}, CO2={CO2}, result={O2 * CO2}")


test()
real()
