from typing import List


class Node:
    def __init__(self) -> None:
        self.value = None
        self.next = None
        self.previous = None


class CupGame:
    def __init__(self, cups: List[int], debug=False) -> None:
        prev = None
        first_cup = None

        self.cups = {}

        cups = cups + [i for i in range(10, 1000001)]
        for c in cups:
            cup = Node()
            cup.value = c
            self.cups[c] = cup
            cup.prev = prev
            if first_cup:
                cup.prev.next = cup
            else:
                first_cup = cup
            prev = cup

        # Link the millionth cup...
        prev.next = first_cup

        self.current_cup = self.cups[cups[0]]
        self.count = 0
        self.debug = debug

    def remove_three_following_cups(self):
        removed_cups = []
        cup_to_rm = self.current_cup.next
        cup_to_rm.prev = None
        for _ in range(0, 3):
            removed_cups.append(cup_to_rm)
            cup_to_rm = cup_to_rm.next
        # Create links
        last_rm_cup = cup_to_rm.prev
        last_rm_cup.next = None
        next_cup_of_current = cup_to_rm
        self.current_cup.next = next_cup_of_current
        next_cup_of_current.prev = self.current_cup
        return removed_cups

    def insert_after_specific_cup(self, target, cups):
        target_cup = target
        after_cup = target_cup.next

        first_cup = cups[0]
        target_cup.next = first_cup
        first_cup.prev = target_cup

        last_cup = cups[-1]
        last_cup.next = after_cup
        after_cup.prev = last_cup

    def find_target_cup(self, current_cup, removed_cups):
        removed_cups_ids = [node.value for node in removed_cups]
        target_id = current_cup.value
        while True:
            target_id = target_id - 1
            if target_id <= 0:
                target_id = int(1e6)
            if target_id not in removed_cups_ids:
                return self.cups[target_id]

    def play_round(self):
        self.count = self.count + 1
        if self.debug or self.count % 100000 == 0:
            print(f"-- move {self.count} --")
        current_cup = self.current_cup
        # if self.debug:
        #     display_cups = ", ".join(f"({c})" if c == current_cup else str(c) for c in self.cups)
        #     print(f"cups: {display_cups}")
        removed_cups = self.remove_three_following_cups()
        # if self.debug:
        #     display_removed_cups = ", ".join(str(c) for c in removed_cups)
        #     print(f"pick up: {display_removed_cups}")
        target_cup = self.find_target_cup(current_cup, removed_cups)
        # if self.debug:
        #     print(f"destination: {target_cup}")
        self.insert_after_specific_cup(target_cup, removed_cups)
        # Set new current cup
        self.current_cup = current_cup.next

    def get_res_after_one(self):
        cup_one = self.cups[1]
        return [
            cup_one.next.value,
            cup_one.next.next.value
        ]


def process_game(data, max_moves):
    cup_game = CupGame([int(cup) for cup in data])
    while cup_game.count < max_moves:
        cup_game.play_round()
    return cup_game.get_res_after_one()


def test():
    test_data = "389125467"
    assert process_game(test_data, int(1e7)) == [934001, 159792]
    print("✅ Valid test")


def real():
    real_data = "156794823"
    part1 = process_game(real_data, int(1e7))
    print(f"Part 1: {part1}")
    # Res is 36807*312400 = 11498506800


test()
real()
