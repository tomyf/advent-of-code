from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str


def rotate(image):
    new_image = [
        [None] * len(line) for line in image
    ]
    for (x, row) in enumerate(image):
        for (y, pixel) in enumerate(row):
            new_image[y][len(row)-x-1] = pixel
    return new_image


def flip(image):
    new_image = [
        [None] * len(line) for line in image
    ]
    for (x, row) in enumerate(image):
        new_image[x] = row[::-1]
    return new_image


def pi(image):
    for x in range(0, len(image)):
        print("".join(image[x]))
    print("------")


def print_monsters(image: List[str]):
    return [
        pi(image),
        pi(rotate(image)),
        pi(rotate(rotate(image))),
        pi(rotate(rotate(rotate(image)))),
        pi(flip(image)),
        pi(rotate(flip(image))),
        pi(rotate(rotate(flip(image)))),
        pi(rotate(rotate(rotate(flip(image))))),
    ]


def real():
    image = read_file_list_str("image.txt")
    print(f"Part 2: {print_monsters(image)}")
    # Found 21 monsters in valid image
    # Answer is below 1907
    # 1 monster = 15 #
    # Total # = 1922
    # Answer = 1922-15*21 = 1607


real()
