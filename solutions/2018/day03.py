import functools
import hashlib
import itertools
import json
import math
import operator
import os
import re
import sys
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
from pathlib import Path
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, NamedTuple, Optional, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_bar, alive_it
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = '#1 @ 1,3: 4x4\n#2 @ 3,1: 4x4\n#3 @ 5,5: 2x2\n'
INPUT = aoc.get_input(YEAR, DAY)

class Point(NamedTuple):
    row: int
    col: int

@dataclass
class Rectangle:
    claim_id: int
    inches_from_left: int
    inches_from_top: int
    width: int
    height: int

    def get_coordinates(self) -> list[Point]:
        start = Point(row=self.inches_from_top,
                      col=self.inches_from_left)
        output_list = []
    
        for row in range(self.height):
            for col in range(self.width):
                pt_row = start.row + row
                pt_col = start.col + col
                output_list.append(Point(pt_row, pt_col))
        return output_list

def make_rectangle_dict(rectangle_list: list[Rectangle]
                        ) -> dict[int, list[Point]]:
    return {rect.claim_id: rect.get_coordinates() for rect in rectangle_list}

def count_overlaps(rectangle_dict: dict[int, list[Point]]) -> int:
    raw_count = sum(len(v) for v in rectangle_dict.values())

    point_set = set()
    for point_list in rectangle_dict.values():
        point_set.update({p for p in point_list})

    return raw_count - len(point_set)   

def parse_data(data: str) -> list[Rectangle]:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        id, _ , inches, rect = line.split(' ')
        id = int(id.removeprefix('#'))
        inches_from_left, inches_from_top = (
            [int(x) for x in inches.removesuffix(':').split(',')])
        width, height = [int(x) for x in rect.split('x')]
        output_list.append(Rectangle(id, inches_from_left, 
                                     inches_from_top, width, height))
    return output_list
    
def part_one(data: str):
    rectangle_list = parse_data(data)
    rectangle_dict = make_rectangle_dict(rectangle_list)
    return count_overlaps(rectangle_dict)

def part_two(data: str):
    ...

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()