import functools
import hashlib
import itertools
import json
import math
import operator
import os
import sys
import re
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum, StrEnum
from pathlib import Path
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, NamedTuple, Optional, Self, Any

import numpy as np
import pandas as pd
import polars as pl
import networkx as nx
from alive_progress import alive_bar, alive_it
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = aoc.get_example(YEAR, DAY)
INPUT = aoc.get_input(YEAR, DAY)

class Point(NamedTuple):
    row: int
    col: int

class RedTile(Point):
    pass

def parse_data_part_one(data: str) -> list[RedTile]:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        col, row = [int(x) for x in line.split(',')]
        output_list.append(RedTile(row, col))
    return output_list
    
def part_one(data: str):
    red_tile_list = parse_data_part_one(data)

    max_area = 0
    for p1, p2 in itertools.permutations(red_tile_list, 2):
        width = abs(p1.col - p2.col) + 1
        height = abs(p1.row - p2.row) + 1
        area = width * height
        max_area = max(max_area, area)
    return max_area

def part_two(data: str):
    ...



def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()