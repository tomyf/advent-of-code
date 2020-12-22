from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str


def compute_score(file: List[str]):
    sep = file.index("")
    player1_deck, player2_deck = [int(c) for c in file[1:sep]], [int(c) for c in file[sep+2:]]
    while len(player1_deck) * len(player2_deck) > 0:
        card1 = player1_deck.pop(0)
        card2 = player2_deck.pop(0)
        if card1 > card2:
            player1_deck.append(card1)
            player1_deck.append(card2)
        else:
            player2_deck.append(card2)
            player2_deck.append(card1)
    winner_deck = player1_deck if len(player1_deck) > 0 else player2_deck
    return sum((len(winner_deck)-index) * card for (index, card) in enumerate(winner_deck))


def recursive_combat(deck1, deck2, game=1):
    seen_games = set()
    round = 0
    while len(deck1) * len(deck2) > 0:
        # round = round + 1
        # print("")
        # print(f"--- Round {round} of game {game}")
        # print("P1", deck1)
        # print("P2", deck2)
        if (tuple(deck1), tuple(deck2)) in seen_games:
            return 1
        seen_games.add((tuple(deck1), tuple(deck2)))
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if len(deck1) >= card1 and len(deck2) >= card2:
            if recursive_combat(deck1[:card1], deck2[:card2], game + 1) == 1:
                deck1.append(card1)
                deck1.append(card2)
            else:
                deck2.append(card2)
                deck2.append(card1)
        elif card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)
    # print("--- End ---")
    # print("P1", deck1)
    # print("P2", deck2)
    return 1 if deck1 else 2


def compute_score_p2(file: List[str]):
    sep = file.index("")
    deck1, deck2 = [int(c) for c in file[1:sep]], [int(c) for c in file[sep+2:]]
    winner_deck = deck1 if recursive_combat(deck1, deck2) == 1 else deck2
    print(winner_deck)
    return sum((len(winner_deck)-index) * card for (index, card) in enumerate(winner_deck))


def test():
    test_data = read_file_list_str("test.txt")
    assert compute_score(test_data) == 306
    assert compute_score_p2(test_data) == 291
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    part1 = compute_score(real_data)
    print(f"Part 1: {part1}")
    assert part1 == 33010
    part2 = compute_score_p2(real_data)
    print(f"Part 2: {part2}")
    assert part2 == 32769


test()
real()
