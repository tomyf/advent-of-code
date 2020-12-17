from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str

SIZE = 25


def prepare_cube(data: List[str]):
    cube: List[List[List[str]]] = []
    for x in range(0, SIZE):
        cube.append([])
        for y in range(0, SIZE):
            cube[x].append([])
            for _ in range(0, SIZE):
                cube[x][y].append(".")
    # Set input data
    for (index_row, row) in enumerate(data):
        for (index_col, c) in enumerate(row):
            cube[SIZE//2 + index_row][SIZE//2 + index_col][SIZE//2] = c
    return cube


def prepare_cube_4(data: List[str]):
    cube: List[List[List[List[str]]]] = []
    for x in range(0, SIZE):
        cube.append([])
        for y in range(0, SIZE):
            cube[x].append([])
            for z in range(0, SIZE):
                cube[x][y].append([])
                for _ in range(0, SIZE):
                    cube[x][y][z].append(".")
    # Set input data
    for (index_row, row) in enumerate(data):
        for (index_col, c) in enumerate(row):
            cube[SIZE//2 + index_row][SIZE//2 + index_col][SIZE//2][SIZE//2] = c
    return cube


def count_active(data: List[str], steps: int) -> int:
    cube = prepare_cube(data)
    active = 0
    for _ in range(0, steps):
        cube = process(cube)
    for x in range(0, SIZE):
        for y in range(0, SIZE):
            for z in range(0, SIZE):
                active = active + 1 if cube[x][y][z] == "#" else active
    return active


def count_active_4(data: List[str], steps: int) -> int:
    cube = prepare_cube_4(data)
    active = 0
    for _ in range(0, steps):
        print("Step ", _ + 1)
        cube = process_4(cube)
    for x in range(0, SIZE):
        for y in range(0, SIZE):
            for z in range(0, SIZE):
                for w in range(0, SIZE):
                    active = active + 1 if cube[x][y][z][w] == "#" else active
    return active


def process(cube: List[List[List[str]]]) -> List[List[List[str]]]:
    new_cube: List[List[List[str]]] = []
    for x in range(0, SIZE):
        new_cube.append([])
        for y in range(0, SIZE):
            new_cube[x].append([])
            for z in range(0, SIZE):
                new_cube[x][y].append(new_value(cube, x, y, z))
    return new_cube


def process_4(cube: List[List[List[List[str]]]]) -> List[List[List[List[str]]]]:
    new_cube: List[List[List[List[str]]]] = []
    for x in range(0, SIZE):
        new_cube.append([])
        for y in range(0, SIZE):
            new_cube[x].append([])
            for z in range(0, SIZE):
                new_cube[x][y].append([])
                for w in range(0, SIZE):
                    new_cube[x][y][z].append(new_value_4(cube, x, y, z, w))
    return new_cube


def new_value(cube: List[List[List[str]]], x: int, y: int, z: int) -> str:
    if cube[x][y][z] == "#":
        # Active cube
        return "#" if 2 <= count_active_neighbours(cube, x, y, z) <= 3 else "."
    else:
        # Inactive cube
        return "#" if count_active_neighbours(cube, x, y, z) == 3 else "."


def new_value_4(cube: List[List[List[List[str]]]], x: int, y: int, z: int, w: int) -> str:
    if cube[x][y][z][w] == "#":
        # Active cube
        return "#" if 2 <= count_active_neighbours_4(cube, x, y, z, w) <= 3 else "."
    else:
        # Inactive cube
        return "#" if count_active_neighbours_4(cube, x, y, z, w) == 3 else "."


def get(cube, x, y, z):
    if x >= 0 and x < len(cube) and y >= 0 and y < len(cube[x]) and z >= 0 and z < len(cube[x][y]):
        return cube[x][y][z]
    else:
        return None


def get_4(cube, x, y, z, w):
    if x >= 0 and x < len(cube) and y >= 0 and y < len(cube[x]) and z >= 0 and z < len(cube[x][y]) and w >= 0 and w < len(cube[x][y][z]):
        return cube[x][y][z][w]
    else:
        return None


def count_active_neighbours(cube: List[List[List[str]]], x: int, y: int, z: int) -> str:
    neighbours = [
        get(cube, x-1, y-1, z-1),
        get(cube, x-1, y-1, z),
        get(cube, x-1, y-1, z+1),
        get(cube, x-1, y, z-1),
        get(cube, x-1, y, z),
        get(cube, x-1, y, z+1),
        get(cube, x-1, y+1, z-1),
        get(cube, x-1, y+1, z),
        get(cube, x-1, y+1, z+1),
        get(cube, x, y-1, z-1),
        get(cube, x, y-1, z),
        get(cube, x, y-1, z+1),
        get(cube, x, y, z-1),
        get(cube, x, y, z+1),
        get(cube, x, y+1, z-1),
        get(cube, x, y+1, z),
        get(cube, x, y+1, z+1),
        get(cube, x+1, y-1, z-1),
        get(cube, x+1, y-1, z),
        get(cube, x+1, y-1, z+1),
        get(cube, x+1, y, z-1),
        get(cube, x+1, y, z),
        get(cube, x+1, y, z+1),
        get(cube, x+1, y+1, z-1),
        get(cube, x+1, y+1, z),
        get(cube, x+1, y+1, z+1)
    ]
    return sum(1 for neighbour in neighbours if neighbour == "#")


def count_active_neighbours_4(cube: List[List[List[List[str]]]], x: int, y: int, z: int, w: int) -> str:
    neighbours = []
    possibles = [-1, 0, 1]
    for i in possibles:
        for j in possibles:
            for k in possibles:
                for l in possibles:
                    if (i, j, k, l) != (0, 0, 0, 0):
                        neighbours.append(get_4(cube, x+i, y+j, z+k, w+l))
    return sum(1 for neighbour in neighbours if neighbour == "#")


def test():
    test_data = read_file_list_str("test.txt")
    # SKIP TESTS to speed up
    # assert count_active(test_data, 6) == 112
    # assert count_active_4(test_data, 6) == 848
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    # part1 = count_active(real_data, 6)
    # print(f"Part 1: {part1}")
    # assert part1 == 304
    part2 = count_active_4(real_data, 6)
    print(f"Part 2: {part2}")
    assert part2 == 1868


test()
real()
