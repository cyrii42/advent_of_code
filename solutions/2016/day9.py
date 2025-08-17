import functools
import hashlib
import itertools
import json
import math
import operator
import os
import pathlib
import re
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from typing import Callable, Generator, Literal, NamedTuple, Optional, Protocol, Self

import numpy as np
import pandas as pd
import polars as pl
from alive_progress import alive_it
from rich import print
from rich.table import Table

import advent_of_code as aoc

PART_ONE_TESTS = [
    ('ADVENT', 'ADVENT', 6),
    ('A(1x5)BC', 'ABBBBBC', 7),
    ('(3x3)XYZ', 'XYZXYZXYZ', 9),
    ('A(2x2)BCD(2x2)EFG', 'ABCBCDEFEFG', 11),
    ('(6x1)(1x3)A', '(1x3)A', 6),
    ('X(8x2)(3x3)ABCY', 'X(3x3)ABC(3x3)ABCY', 18)
]

CURRENT_FILE = pathlib.Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day'))

INPUT = aoc.get_input(YEAR, DAY)

def parse_data(data: str):
    line_list = data.splitlines()

def part_one_tests():
    ...
    
def part_one(data: str):
    __ = parse_data(data)
    print(data)

def part_two(data: str):
    __ = parse_data(data)



def main():
    part_one_tests()
    print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

    random_tests()

def random_tests():
    ...

       
if __name__ == '__main__':
    main()