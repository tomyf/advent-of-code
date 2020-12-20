from math import sqrt
from typing import List
from y2020.libs.read_file import read_file_list_str
from copy import copy

TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3


class Tile:
    def __init__(self, id, image: str = None, pixels: List[List[str]] = None):
        self.id = id
        self.pixels = [
            [pixel for pixel in line]
            for line in image.split("\n")
        ] if image else pixels

    def matches(self, tile, relative_position: int):
        if relative_position == RIGHT:
            # Last column of current tile = 1st column of right tile
            return all(
                self.pixels[x][-1] == tile.pixels[x][0]
                for (x, row) in enumerate(self.pixels)
            )
        elif relative_position == BOTTOM:
            # Last row of current tile = 1st row of bottom tile
            return self.pixels[-1] == tile.pixels[0]
        else:
            raise Exception(f"INVALID POSITION: {relative_position}")

    def rotate(self):
        # prepare new rows
        pixels = [
            [None] * len(line) for line in self.pixels
        ]
        for (x, row) in enumerate(self.pixels):
            for (y, pixel) in enumerate(row):
                # (x,y) => (y, max-x)
                pixels[y][len(row)-x-1] = pixel
        # return new tile
        return Tile(self.id, pixels=pixels)

    def flip(self):
        # prepare new rows
        pixels = [
            [None] * len(line) for line in self.pixels
        ]
        for (x, row) in enumerate(self.pixels):
            pixels[x] = row[::-1]
        return Tile(self.id, pixels=pixels)

    def __str__(self) -> str:
        pixels = "\n".join("".join(l) for l in self.pixels)
        return f"""Tile {self.id}:
{pixels}
"""


def generate_tile_variations(tile):
    return [
        (f"{tile.id}", tile),
        (f"{tile.id}-R1", tile.rotate()),
        (f"{tile.id}-R2", tile.rotate().rotate()),
        (f"{tile.id}-R3", tile.rotate().rotate().rotate()),
        (f"{tile.id}-F", tile.flip()),
        (f"{tile.id}-R1-F", tile.flip().rotate()),
        (f"{tile.id}-R2-F", tile.flip().rotate().rotate()),
        (f"{tile.id}-R3-F", tile.flip().rotate().rotate().rotate()),
    ]


class Image:
    def __init__(self, tiles):
        self.tiles: List[Tile] = tiles
        self.tiles_variations: dict = {}
        self.links: dict = self.build_links()
        self.arrangement = self.build_arrangement()

    def print(self):
        # arrangement = [ [(1, T), (2, T)], [(3, T), (4, T)]]
        for (i, row) in enumerate(self.arrangement):
            for j in range(0, len(row[0][1].pixels)):
                line = ""
                for (_, tile) in row:
                    line = line + "".join(tile.pixels[j])
                print(line)

    def build_links(self):
        links = {}
        count = 0
        for tile in self.tiles:
            print("Build links:", count)
            count = count + 1
            for (id, tv) in generate_tile_variations(tile):
                self.tiles_variations[id] = tv
                links[id] = {
                    "BOTTOM": [],
                    "RIGHT": [],
                }
                for other_tile in [t for t in self.tiles if t.id != tile.id]:
                    for (ido, tvo) in generate_tile_variations(other_tile):
                        if tv.matches(tvo, BOTTOM):
                            links[id]["BOTTOM"].append(ido)
                        if tv.matches(tvo, RIGHT):
                            links[id]["RIGHT"].append(ido)
        return links

    def build_arrangement(self):
        possibilities = []
        # Instantiate possibilities with all rotated and flipped tiles
        for tile in self.tiles:
            for (idv, tv) in generate_tile_variations(tile):
                possibilities.append([[(idv, tv)]])
        # Compute max grid size
        SIZE = int(sqrt(len(self.tiles)))
        # Loop
        iter = 0
        while len(possibilities) >= 1:
            iter = iter + 1
            current = possibilities.pop()
            seen_tiles_ids = [
                tile.id
                for row in current
                for (idv, tile) in row
            ]

            if len(seen_tiles_ids) == len(self.tiles):
                return current

            index = sum(len(row) for row in current)
            if iter % 10000 == 0:
                print("Current possibility length:", index, f"(iter={iter})", f"({len(possibilities)})")
            x, y = index // SIZE, index % SIZE
            new_possibilities = []
            if y > 0 and x > 0:
                # BOTTOM AND RIGHT
                id_top = current[x-1][y][0]
                id_left = current[x][y-1][0]
                for possible_tile_idv in [idv for idv in self.links[id_left]["RIGHT"] if idv[0:4] not in seen_tiles_ids]:
                    if possible_tile_idv in [idv for idv in self.links[id_top]["BOTTOM"]]:
                        t = self.tiles_variations[possible_tile_idv]
                        p = [c[:] for c in current]
                        p[x].append((possible_tile_idv, t))
                        new_possibilities.append(p)
            elif y > 0:
                # RIGHT
                id_left = current[x][y-1][0]
                for possible_tile_idv in [idv for idv in self.links[id_left]["RIGHT"] if idv[0:4] not in seen_tiles_ids]:
                    t = self.tiles_variations[possible_tile_idv]
                    p = [c[:] for c in current]
                    p[x].append((possible_tile_idv, t))
                    new_possibilities.append(p)
            else:
                # BOTTOM
                id_top = current[x-1][0][0]
                # matching tiles
                for possible_tile_idv in [idv for idv in self.links[id_top]["BOTTOM"] if idv[0:4] not in seen_tiles_ids]:
                    t = self.tiles_variations[possible_tile_idv]
                    p = [c[:] for c in current]
                    p.append([])
                    p[x].append((possible_tile_idv, t))
                    new_possibilities.append(p)

            if new_possibilities:
                for new_possibility in new_possibilities:
                    possibilities.append(new_possibility)


def build_tiles(file: List[str]):
    id = None
    image_lines = []
    tiles = []
    for line in file:
        if line.startswith("Tile"):
            id = line.replace("Tile ", "").replace(":", "")
        elif line:
            image_lines.append(line)
        elif line == "":
            tiles.append(Tile(id, "\n".join(image_lines)))
            id = None
            image_lines = []
    return tiles


def get_arrangement_product(file):
    tiles = build_tiles(file)
    image = Image(tiles)
    arrangement = [
        [int(tile.id[0:4]) for (id, tile) in row]
        for row in image.arrangement
    ]
    print(arrangement)
    image.print()
    return arrangement[0][0] * arrangement[0][-1] * arrangement[-1][0] * arrangement[-1][-1]


def test():
    test_data = read_file_list_str("test.txt")
    assert get_arrangement_product(test_data) == 20899048083289
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    part1 = get_arrangement_product(real_data)
    print(f"Part 1: {part1}")
    assert part1 == 45443966642567
    # Arrangement P1: [[3613, 2341, 1487, 1091, 3709, 1483, 3209, 1019, 2029, 1319, 3229, 3457], [3673, 1847, 2287, 1223, 3929, 3637, 1697, 2459, 1327, 3557, 3947, 1123], [1453, 2129, 3911, 2707, 1069, 3313, 1039, 1279, 3697, 2131, 1913, 3329], [2861, 2393, 1451, 3917, 3863, 3701, 1879, 1481, 3121, 3923, 1607, 3583], [2309, 2207, 1901, 1597, 3769, 2437, 1933, 1181, 3671, 3119, 1187, 2801], [3109, 3517, 1801, 2957, 2797, 1613, 2917, 2339, 2963, 3391, 1543, 3049], [2423, 2791, 2143, 3877, 2477, 1949, 1811, 3083, 3203, 1399, 3221, 3301], [3847, 2789, 2857, 2833, 2969, 1229, 2293, 1571, 2699, 3389, 2441, 1361], [3499, 3067, 1831, 2999, 3989, 3251, 1163, 3541, 1193, 3307, 2741, 3607], [1103, 2113, 1051, 3089, 3001, 1621, 2897, 2879, 1129, 2819, 2039, 2011], [2803, 2689, 3761, 2531, 2647, 3019, 3371, 3511, 2609, 2903, 1409, 1277], [2539, 1459, 3767, 3739, 1321, 1733, 3343, 3163, 2549, 2543, 3023, 1433]]


test()
real()
