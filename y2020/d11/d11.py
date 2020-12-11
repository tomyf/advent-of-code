from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str


def count_occupied_around_seat(map: List[List[str]], x: int, y: int) -> int:
    positions = [
        (x-1, y-1),
        (x-1,   y),
        (x-1, y+1),
        (x, y-1),
        (x, y+1),
        (x+1, y-1),
        (x+1,   y),
        (x+1, y+1)
    ]
    counter = 0
    for (a, b) in positions:
        if a < 0 or b < 0:
            continue
        try:
            counter = (counter + 1) if map[a][b] == '#' else counter
        except:
            pass
    return counter


def check(map, x, y, dx, dy):
    # print("-----")
    # print(x, y, dx, dy)
    while 0 <= x+dx < len(map) and 0 <= y+dy < len(map[x]):
        # print(x, y, map[x+dx][y+dy])
        if map[x+dx][y+dy] == '#':
            return True
        if map[x+dx][y+dy] == 'L':
            return False
        x = x + dx
        y = y + dy
    return False


def count_occupied_seen_seat(map: List[List[str]], x: int, y: int) -> int:
    deltas = [
        (-1, -1),
        (-1,  0),
        (-1, +1),
        (0, -1),
        (0, +1),
        (+1, -1),
        (+1,  0),
        (+1, +1)
    ]
    counter = 0
    for (dx, dy) in deltas:
        counter = (counter + 1) if check(map, x, y, dx, dy) else counter
    return counter


def prepare_map(data: List[str]) -> List[List[str]]:
    return [
        [c for c in line]
        for line in data
    ]


def map_hash(map: List[List[str]]) -> str:
    return "".join("".join(line) for line in map)


def generate_new_map(map: List[List[str]], checker, allowed_neighbours) -> List[List[str]]:
    new_map = [None] * len(map)
    for x in range(0, len(map)):
        new_map[x] = []
        for y in range(0, len(map[x])):
            if map[x][y] == 'L' and checker(map, x, y) == 0:
                new_map[x].append('#')
            elif map[x][y] == '#' and checker(map, x, y) >= allowed_neighbours:
                new_map[x].append('L')
            else:
                new_map[x].append(map[x][y])
    return new_map


def count_eventually_occupied_seats(data: List[str], checker, allowed_neighbours):
    map = prepare_map(data)
    old_map_hash = map_hash(map)
    new_map = map
    new_map_hash = None
    while new_map_hash != old_map_hash:
        new_map = generate_new_map(new_map, checker, allowed_neighbours)
        old_map_hash = new_map_hash
        new_map_hash = map_hash(new_map)
    # New map is stable
    return sum(sum(1 for seat in line if seat == '#') for line in new_map) if new_map_hash == old_map_hash else -1


def test():
    test_data = read_file_list_str("test.txt")
    assert count_eventually_occupied_seats(test_data, count_occupied_around_seat, 4) == 37
    test_data2 = read_file_list_str("test_2.txt")
    map2 = prepare_map(test_data2)
    assert check(map2, 1, 1, 0, 1) == False
    assert count_occupied_seen_seat(map2, 1, 1) == 0
    assert check(map2, 1, 3, 0, 1) == True
    assert count_occupied_seen_seat(map2, 1, 3) == 1
    assert count_eventually_occupied_seats(test_data, count_occupied_seen_seat, 5) == 26
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    part1 = count_eventually_occupied_seats(real_data, count_occupied_around_seat, 4)
    print("Part1:", part1)
    assert part1 == 2310
    part2 = count_eventually_occupied_seats(real_data, count_occupied_seen_seat, 5)
    print("Part2:", part2)
    assert part2 == 2074


test()
real()
