from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str


def count_toboggan_trees(map: List[str], slope: Tuple[int, int]):
    # Slope is a Tuple : (dx, dy) = (right, down)
    x, y = (0, 0)
    dx, dy = slope
    trees_count = 0
    map_width = len(map[0])

    # while we're still in the "forest"
    while y < len(map) - dy:
        x = (x + dx) % map_width
        y = y + dy
        trees_count = trees_count + 1 if map[y][x] == '#' else trees_count
    return trees_count


def test():
    test_data = read_file_list_str("test.txt")
    slopes = {
        (1, 1): 2,
        (3, 1): 7,
        (5, 1): 3,
        (7, 1): 4,
        (1, 2): 2
    }
    for slope, expected_count in slopes.items():
        assert count_toboggan_trees(test_data, slope) == expected_count
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    slopes = {
        (1, 1): 2,
        (3, 1): 7,
        (5, 1): 3,
        (7, 1): 4,
        (1, 2): 2
    }
    product = 1
    for slope, expected_count in slopes.items():
        count = count_toboggan_trees(real_data, slope)
        print(slope, count)
        product = product * count
    print(f"Total product of trees: {product}")


test()
real()
