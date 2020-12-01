from typing import List
import os
import sys


def read_file(path: str) -> str:
    return open(os.path.join(sys.path[0], path), "r").read()


def read_file_list_int(path: str) -> List[int]:
    return [int(n) for n in read_file(path).split("\n")]
