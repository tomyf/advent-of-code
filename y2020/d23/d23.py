from typing import List


class CupGame:
    def __init__(self, cups: List[int], debug=False) -> None:
        self.cups = cups
        self.index = -1
        self.count = 0
        self.debug = debug

    def get_current_cup(self):
        return self.cups[self.index]

    def remove_three_following_cups(self):
        removed_cups = []
        for _ in range(0, 3):
            # Remove next one
            index = self.index + 1
            if index >= len(self.cups):
                index = 0
            removed_cups.append(self.cups.pop(index))
        return removed_cups

    def insert_after_specific_cup(self, target, cups):
        index = self.cups.index(target)
        self.cups = self.cups[:index + 1] + cups + self.cups[index+1:]

    def find_target_cup(self, current_cup):
        target = current_cup
        while True:
            target = target - 1
            if target <= 0:
                return max(self.cups)
            if target in self.cups:
                return target

    def play_round(self):
        self.count = self.count + 1
        if self.debug:
            print(f"-- move {self.count} --")
        self.index = (self.index + 1) % len(self.cups)
        current_cup = self.cups[self.index]
        display_cups = ", ".join(f"({c})" if c == current_cup else str(c) for c in self.cups)
        if self.debug:
            print(f"cups: {display_cups}")
        removed_cups = self.remove_three_following_cups()
        display_removed_cups = ", ".join(str(c) for c in removed_cups)
        if self.debug:
            print(f"pick up: {display_removed_cups}")
        target_cup = self.find_target_cup(current_cup)
        if self.debug:
            print(f"destination: {target_cup}")
        self.insert_after_specific_cup(target_cup, removed_cups)
        # Reset the index to current cup
        self.index = self.cups.index(current_cup)

    def get_res_after_one(self):
        index_one = self.cups.index(1)
        res = ""
        for i in range(0, len(self.cups) - 1):
            index = (index_one + 1 + i) % len(self.cups)
            res = res + str(self.cups[index])
        return res


def process_game(data, max_moves):
    cup_game = CupGame([int(cup) for cup in data])
    while cup_game.count < max_moves:
        cup_game.play_round()
    return cup_game.get_res_after_one()


def test():
    test_data = "389125467"
    assert process_game(test_data, 10) == "92658374"
    assert process_game(test_data, 100) == "67384529"
    print("✅ Valid test")


def real():
    real_data = "156794823"
    part1 = process_game(real_data, 100)
    print(f"Part 1: {part1}")


test()
real()
