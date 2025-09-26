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

class Rectangle(NamedTuple):
    claim_id: int
    inches_from_left: int
    inches_from_top: int
    width: int
    height: int

def parse_data(data: str) -> list[Rectangle]:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        id, _ , inches, rect = line.split(' ')
        id = int(id.removeprefix('#'))
        inches_from_left, inches_from_top = [int(x) for x in inches.removesuffix(':').split(',')]
        width, height = [int(x) for x in rect.split('x')]
        output_list.append(Rectangle(id, inches_from_left, inches_from_top, width, height))
    return output_list
    
def part_one(data: str):
    rectangle_list = parse_data(data)
    print(rectangle_list)

def part_two(data: str):
    ...

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()