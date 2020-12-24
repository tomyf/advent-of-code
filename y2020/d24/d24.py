from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str

EAST = 0
SOUTH_EAST = 1
SOUTH_WEST = 2
WEST = 3
NORTH_WEST = 4
NORTH_EAST = 5


def read_line(line: str) -> List[int]:
    i = 0
    res = []
    while i < len(line):
        cur = line[i]
        if cur == "e":
            res.append(EAST)
        elif cur == "w":
            res.append(WEST)
        else:
            cur = cur + line[i+1]
            # Double increment i
            if cur == "se":
                res.append(SOUTH_EAST)
            elif cur == "sw":
                res.append(SOUTH_WEST)
            elif cur == "ne":
                res.append(NORTH_EAST)
            elif cur == "nw":
                res.append(NORTH_WEST)
            i = i + 1
        i = i + 1
    return res


def coordinates(tile: List[int]) -> Tuple[int, int]:
    e = tile.count(EAST)
    w = tile.count(WEST)
    se = tile.count(SOUTH_EAST)
    sw = tile.count(SOUTH_WEST)
    ne = tile.count(NORTH_EAST)
    nw = tile.count(NORTH_WEST)
    z = nw - se
    return (
        e - w - z,
        ne - sw + z
    )


def process_tiles(file: List[str]) -> List[Tuple[int, int]]:
    tiles = []
    for line in file:
        tile_count = read_line(line)
        tile = coordinates(tile_count)
        tiles.append(tile)
    return tiles


def count_black_from_tiles(tiles: List[int]) -> int:
    count_black = 0
    for tile in set(tiles):
        if tiles.count(tile) % 2 == 1:
            count_black = count_black + 1
    return count_black


def count_black_tiles(file: List[str]) -> int:
    tiles = process_tiles(file)
    return count_black_from_tiles(tiles)


def generate_neighbours(tile: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = tile
    return [
        (x-1, y),
        (x-1, y+1),
        (x, y+1),
        (x, y-1),
        (x+1, y-1),
        (x+1, y)
    ]


def iterations(file: List[str], number) -> int:
    init_flips = process_tiles(file)
    black_tiles = list(set(t for t in init_flips if init_flips.count(t) % 2 == 1))
    new_black_tiles = black_tiles
    for _ in range(0, number):
        new_black_tiles = set()
        for tile in black_tiles:
            neighbours = generate_neighbours(tile)
            count_black_neighbours = 0
            count_black_neighbours = sum(1 for neighbour in neighbours if neighbour in black_tiles)
            if 1 <= count_black_neighbours <= 2:
                new_black_tiles.add(tile)
            # Check neighbours now
            for white_neighbour in (neighbour for neighbour in neighbours if neighbour not in black_tiles):
                w_neighbours = generate_neighbours(white_neighbour)
                w_count_black_neighbours = sum(1 for w_neighbour in w_neighbours if w_neighbour in black_tiles)
                if w_count_black_neighbours == 2:
                    new_black_tiles.add(white_neighbour)
        black_tiles = new_black_tiles
    return len(black_tiles)


def test():
    test_data = read_file_list_str("test.txt")
    assert count_black_tiles(test_data) == 10
    assert iterations(test_data, 1) == 15
    assert iterations(test_data, 2) == 12
    assert iterations(test_data, 3) == 25
    assert iterations(test_data, 10) == 37
    assert iterations(test_data, 100) == 2208
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    part1 = count_black_tiles(real_data)
    print(f"Part 1: {part1}")
    assert part1 == 391
    part2 = iterations(real_data, 100)
    print(f"Part 2: {part2}")
    assert part2 == 3876


test()
real()
